#!/usr/bin/env python3
"""Run full statistical analysis on evaluation results."""
import json
from pathlib import Path
from pipeline.config import settings
from pipeline.evaluation.scorer import compute_accuracy
from pipeline.analysis.statistics import compare_models, subgroup_chi_square
from pipeline.analysis.img_perspective import img_accuracy_gap_analysis
from pipeline.dataset.schema import EvalResult

if __name__ == "__main__":
    settings.ensure_dirs()
    results_dir = settings.results_dir
    all_results = []
    results_by_model: dict[str, list] = {}

    for result_file in results_dir.glob("*.json"):
        if "cost_log" in result_file.name:
            continue
        data = json.loads(result_file.read_text())
        results = [EvalResult(**r) for r in data]
        model_name = results[0].model_name if results else result_file.stem
        results_by_model[model_name] = [r.model_dump() for r in results]
        all_results.extend([r.model_dump() for r in results])

    if not all_results:
        print("No results found. Run 03_run_evaluation.py first.")
        raise SystemExit(1)

    # Overall accuracy by model
    print("\n=== Overall Accuracy by Model ===")
    all_eval = [EvalResult(**r) for r in all_results]
    acc_df = compute_accuracy(all_eval, group_by="model_name")
    print(acc_df.to_string(index=False))
    acc_df.to_csv(results_dir / "accuracy_by_model.csv", index=False)

    # Accuracy by subject
    print("\n=== Accuracy by Subject (all models) ===")
    subj_df = compute_accuracy(all_eval, group_by="subject")
    print(subj_df.to_string(index=False))
    subj_df.to_csv(results_dir / "accuracy_by_subject.csv", index=False)

    # Statistical comparison
    print("\n=== Pairwise McNemar Tests ===")
    mcnemar_df = compare_models(results_by_model)
    print(mcnemar_df.to_string(index=False))
    mcnemar_df.to_csv(results_dir / "mcnemar_tests.csv", index=False)

    # IMG perspective analysis
    print("\n=== IMG Accuracy Gap Analysis ===")
    img_df = img_accuracy_gap_analysis(all_results)
    print(img_df.to_string(index=False))
    img_df.to_csv(results_dir / "img_gap_analysis.csv", index=False)

    print("\nAnalysis complete. Results saved to", results_dir)
