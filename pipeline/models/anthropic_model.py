import time
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import LLMModel, ModelResponse
from pipeline.config import MODELS, settings


class AnthropicModel(LLMModel):
    def __init__(self, model_name: str):
        config = MODELS[model_name]
        super().__init__(model_name, config["model_id"])
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.cost_config = config

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))
    def answer_question(self, question: dict) -> ModelResponse:
        prompt = self.format_prompt(question)
        start = time.perf_counter()
        try:
            response = self.client.messages.create(
                model=self.model_id,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}],
            )
            latency_ms = (time.perf_counter() - start) * 1000
            raw = response.content[0].text
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost = (
                input_tokens / 1000 * self.cost_config["cost_per_1k_input"]
                + output_tokens / 1000 * self.cost_config["cost_per_1k_output"]
            )
            return ModelResponse(
                model_name=self.model_name,
                question_id=question["id"],
                raw_response=raw,
                selected_answer=self.extract_answer(raw),
                reasoning=raw,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms,
                cost_usd=cost,
            )
        except Exception as e:
            return ModelResponse(
                model_name=self.model_name,
                question_id=question["id"],
                raw_response="",
                selected_answer="X",
                reasoning="",
                input_tokens=0,
                output_tokens=0,
                latency_ms=0,
                cost_usd=0,
                error=str(e),
            )
