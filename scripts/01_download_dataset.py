#!/usr/bin/env python3
"""Download and cache MedQA dataset from HuggingFace."""
from pipeline.config import settings
from pipeline.dataset.loader import download_medqa

if __name__ == "__main__":
    settings.ensure_dirs()
    questions = download_medqa()
    print(f"Downloaded {len(questions)} total questions.")
    by_step: dict[str, int] = {}
    for q in questions:
        by_step[q["step"]] = by_step.get(q["step"], 0) + 1
    for step, count in by_step.items():
        print(f"  {step}: {count} questions")
