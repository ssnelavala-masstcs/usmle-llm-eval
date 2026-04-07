"""
Expert annotation interface for Blessie.
Generates a CSV annotation sheet from evaluation results, and
reads back annotations into the results.
"""
import json
import pandas as pd
from pathlib import Path
from pipeline.config import settings


def generate_annotation_sheet(
    results_file: Path,
    questions_file: Path,
    output_path: Path = None,
) -> Path:
    """
    Create a CSV sheet for expert (Blessie) to annotate model answers.
    Columns: question_id, question_text, correct_answer, model_name,
             model_answer, model_reasoning, expert_score (blank), expert_notes (blank),
             img_bias_detected (blank)
    """
    results = json.loads(results_file.read_text())
    questions = {q["id"]: q for q in json.loads(questions_file.read_text())}

    rows = []
    for r in results:
        q = questions.get(r["question_id"], {})
        rows.append({
            "question_id": r["question_id"],
            "question_text": q.get("question", ""),
            "options": str(q.get("options", {})),
            "correct_answer": r["correct_answer"],
            "model_name": r["model_name"],
            "model_answer": r["selected_answer"],
            "is_correct": r["is_correct"],
            "subject": r["subject"],
            "step": r["step"],
            "expert_score": "",        # Blessie fills this in (1-5)
            "expert_notes": "",        # Blessie fills this in
            "img_bias_detected": "",   # Blessie fills this in (yes/no)
        })

    df = pd.DataFrame(rows)
    output_path = output_path or (
        settings.data_dir / "annotations" / f"annotation_{results_file.stem}.csv"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Annotation sheet saved to {output_path}")
    print("Instructions for Blessie: Fill in 'expert_score' (1-5), 'expert_notes', and 'img_bias_detected' (yes/no)")
    return output_path


def merge_annotations(results_file: Path, annotation_file: Path) -> list[dict]:
    """Merge expert annotations back into results."""
    results = json.loads(results_file.read_text())
    annotations = pd.read_csv(annotation_file)
    ann_dict = annotations.set_index(["question_id", "model_name"])[
        ["expert_score", "expert_notes", "img_bias_detected"]
    ].to_dict("index")

    for r in results:
        key = (r["question_id"], r["model_name"])
        if key in ann_dict:
            r["expert_score"] = ann_dict[key].get("expert_score")
            r["expert_notes"] = ann_dict[key].get("expert_notes")
    return results
