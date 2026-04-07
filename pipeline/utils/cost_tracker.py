import json
from pathlib import Path
from collections import defaultdict
from pipeline.config import settings


class CostTracker:
    def __init__(self):
        self.records = defaultdict(
            lambda: {"cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0, "calls": 0}
        )

    def record(self, model_name: str, cost: float, input_tokens: int, output_tokens: int):
        r = self.records[model_name]
        r["cost_usd"] += cost
        r["input_tokens"] += input_tokens
        r["output_tokens"] += output_tokens
        r["calls"] += 1

    def summary(self) -> dict:
        total = sum(r["cost_usd"] for r in self.records.values())
        return {"total_cost_usd": round(total, 4), "by_model": dict(self.records)}

    def save(self, path: Path = None):
        path = path or settings.cost_log_file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.summary(), indent=2))
        print(f"Cost log saved to {path}")
