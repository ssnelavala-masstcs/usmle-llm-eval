#!/usr/bin/env python3
"""Run all models on sampled questions."""
import json
import argparse
from pathlib import Path
from pipeline.config import settings, MODELS
from pipeline.models.registry import get_model
from pipeline.evaluation.runner import EvaluationRunner
from pipeline.utils.cache import ResponseCache
from pipeline.utils.cost_tracker import CostTracker

parser = argparse.ArgumentParser()
parser.add_argument("--models", default="all", help="Comma-separated model names or 'all'")
parser.add_argument("--questions", default="data/sampled/step1_sample.json")
parser.add_argument("--no-cache", action="store_true")
args = parser.parse_args()

if __name__ == "__main__":
    settings.ensure_dirs()
    questions = json.loads(Path(args.questions).read_text())
    print(f"Loaded {len(questions)} questions from {args.questions}")

    model_names = list(MODELS.keys()) if args.models == "all" else args.models.split(",")
    cache = ResponseCache()
    if args.no_cache:
        cache.enabled = False
    cost_tracker = CostTracker()

    for name in model_names:
        print(f"\n{'='*50}")
        print(f"Running: {name}")
        model = get_model(name)
        runner = EvaluationRunner(model, cache=cache, cost_tracker=cost_tracker)
        step = Path(args.questions).stem.replace("_sample", "")
        out = settings.results_dir / f"{name}_{step}.json"
        results = runner.run(questions, output_file=out)
        correct = sum(1 for r in results if r.is_correct)
        print(f"  Accuracy: {correct}/{len(results)} = {correct/len(results):.1%}")

    cost_tracker.save()
    print(f"\nTotal cost: ${cost_tracker.summary()['total_cost_usd']:.4f}")
