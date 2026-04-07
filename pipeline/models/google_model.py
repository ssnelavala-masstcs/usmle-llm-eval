import time
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import LLMModel, ModelResponse
from pipeline.config import MODELS, settings


class GoogleModel(LLMModel):
    def __init__(self, model_name: str):
        config = MODELS[model_name]
        super().__init__(model_name, config["model_id"])
        self.cost_config = config
        # Import here to avoid module-level deprecation warnings
        try:
            from google import genai as google_genai
            self._client = google_genai.Client(api_key=settings.google_api_key)
            self._use_new_sdk = True
        except ImportError:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=settings.google_api_key)
            self._model_instance = genai_legacy.GenerativeModel(config["model_id"])
            self._use_new_sdk = False

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))
    def answer_question(self, question: dict) -> ModelResponse:
        prompt = self.format_prompt(question)
        start = time.perf_counter()
        try:
            if self._use_new_sdk:
                from google.genai import types as genai_types
                response = self._client.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                    config=genai_types.GenerateContentConfig(
                        temperature=0,
                        max_output_tokens=512,
                    ),
                )
                latency_ms = (time.perf_counter() - start) * 1000
                raw = response.text
                input_tokens = response.usage_metadata.prompt_token_count
                output_tokens = response.usage_metadata.candidates_token_count
            else:
                import google.generativeai as genai_legacy
                response = self._model_instance.generate_content(
                    prompt,
                    generation_config=genai_legacy.types.GenerationConfig(
                        temperature=0,
                        max_output_tokens=512,
                    ),
                )
                latency_ms = (time.perf_counter() - start) * 1000
                raw = response.text
                input_tokens = response.usage_metadata.prompt_token_count
                output_tokens = response.usage_metadata.candidates_token_count

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
