from datasets import load_dataset
from pathlib import Path
import json
from pipeline.config import settings
import hashlib


def download_medqa(cache_dir: Path = None) -> list[dict]:
    """
    Download MedQA-USMLE from HuggingFace and cache locally.
    Dataset: GBaker/MedQA-USMLE-4-options
    Returns list of raw question dicts.
    """
    cache_dir = cache_dir or settings.data_dir / "raw"
    cache_file = cache_dir / "medqa_all.json"

    if cache_file.exists():
        print(f"Loading cached dataset from {cache_file}")
        return json.loads(cache_file.read_text())

    print("Downloading MedQA-USMLE from HuggingFace...")
    dataset = load_dataset("GBaker/MedQA-USMLE-4-options", trust_remote_code=True)

    all_questions = []
    for split in ["train", "validation", "test"]:
        if split in dataset:
            for item in dataset[split]:
                q = {
                    "id": hashlib.md5(item["question"].encode()).hexdigest()[:12],
                    "question": item["question"],
                    "options": {
                        "A": item["options"]["A"],
                        "B": item["options"]["B"],
                        "C": item["options"]["C"],
                        "D": item["options"]["D"],
                    },
                    "answer": item["answer_idx"],
                    "subject": item.get("meta_info", "General"),
                    "step": _infer_step(item),
                    "difficulty": _infer_difficulty(item),
                    "question_type": _infer_question_type(item["question"]),
                    "img_relevant": False,
                    "source": f"MedQA-USMLE-{split}",
                }
                all_questions.append(q)

    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(all_questions, indent=2))
    print(f"Cached {len(all_questions)} questions to {cache_file}")
    return all_questions


def _infer_step(item: dict) -> str:
    """Infer Step 1 vs Step 2 CK from metadata or heuristics."""
    question_text = item.get("question", "").lower()
    step2_keywords = [
        "management", "next step", "most appropriate treatment",
        "hospitalized", "emergency department", "clinic visit",
        "follow-up", "discharge", "days later", "weeks later",
    ]
    if any(kw in question_text for kw in step2_keywords):
        return "step2ck"
    return "step1"


def _infer_difficulty(item: dict) -> str:
    """Rough difficulty heuristic based on question length."""
    q_len = len(item.get("question", "").split())
    if q_len < 60:
        return "easy"
    elif q_len < 120:
        return "medium"
    return "hard"


def _infer_question_type(question_text: str) -> str:
    text_lower = question_text.lower()
    if any(kw in text_lower for kw in ["year-old", "presents with", "history of"]):
        return "clinical_vignette"
    if any(kw in text_lower for kw in ["lab", "serum", "mg/dl", "level shows"]):
        return "laboratory_data"
    return "single_best_answer"
