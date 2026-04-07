import time
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import LLMModel, ModelResponse
from pipeline.config import MODELS, settings


class GroqModel(LLMModel):
    def __init__(self, model_name: str):
        config = MODELS[model_name]
        super().__init__(model_name, config["model_id"])
        self.client = Groq(api_key=settings.groq_api_key)
        self.cost_config = config

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))
    def answer_question(self, question: dict) -> ModelResponse:
        prompt = self.format_prompt(question)
        start = time.perf_counter()
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=512,
            )
            latency_ms = (time.perf_counter() - start) * 1000
            raw = response.choices[0].message.content or ""
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            return ModelResponse(
                model_name=self.model_name,
                question_id=question["id"],
                raw_response=raw,
                selected_answer=self.extract_answer(raw),
                reasoning=raw,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms,
                cost_usd=0.0,  # Groq free tier
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
                cost_usd=0.0,
                error=str(e),
            )
