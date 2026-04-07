import json
import time
from pathlib import Path
from tqdm import tqdm
from pipeline.config import settings
from pipeline.dataset.schema import EvalResult
from pipeline.utils.cache import ResponseCache
from pipeline.utils.cost_tracker import CostTracker
from pipeline.utils.logger import get_logger

logger = get_logger(__name__)


class EvaluationRunner:
    def __init__(self, model, cache: ResponseCache = None, cost_tracker: CostTracker = None):
        self.model = model
        self.cache = cache or ResponseCache()
        self.cost_tracker = cost_tracker or CostTracker()

    def run(self, questions: list[dict], output_file: Path = None) -> list[EvalResult]:
        results = []
        output_file = output_file or (
            settings.results_dir / f"{self.model.model_name}_{int(time.time())}.json"
        )
        settings.results_dir.mkdir(parents=True, exist_ok=True)

        for q in tqdm(questions, desc=f"Evaluating {self.model.model_name}"):
            cache_key = f"{self.model.model_name}:{q['id']}"

            cached = self.cache.get(cache_key)
            if cached:
                results.append(EvalResult(**cached))
                continue

            response = self.model.answer_question(q)
            self.cost_tracker.record(
                self.model.model_name,
                response.cost_usd,
                response.input_tokens,
                response.output_tokens,
            )

            result = EvalResult(
                question_id=q["id"],
                model_name=self.model.model_name,
                selected_answer=response.selected_answer,
                correct_answer=q["answer"],
                is_correct=(response.selected_answer == q["answer"]),
                subject=q["subject"],
                step=q["step"],
                difficulty=q["difficulty"],
                question_type=q["question_type"],
                img_relevant=q.get("img_relevant", False),
                latency_ms=response.latency_ms,
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                cost_usd=response.cost_usd,
                error=response.error,
            )
            results.append(result)
            self.cache.set(cache_key, result.model_dump())

        output_file.write_text(
            json.dumps([r.model_dump() for r in results], indent=2)
        )
        logger.info(f"Saved {len(results)} results to {output_file}")
        return results
