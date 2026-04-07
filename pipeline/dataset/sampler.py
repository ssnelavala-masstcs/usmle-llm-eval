import json
import random
from collections import defaultdict
from pathlib import Path
from pipeline.config import settings


def stratified_sample(
    questions: list[dict],
    n_per_step: int = 100,
    seed: int = 42,
) -> dict[str, list[dict]]:
    """
    Produce a stratified sample of n_per_step questions per exam step.
    Stratify by subject (proportional) and difficulty (balanced).
    Returns {"step1": [...], "step2ck": [...]}.
    """
    random.seed(seed)
    by_step = defaultdict(list)
    for q in questions:
        by_step[q["step"]].append(q)

    result = {}
    for step, qs in by_step.items():
        by_subject = defaultdict(list)
        for q in qs:
            by_subject[q["subject"]].append(q)

        sampled = []
        subjects = list(by_subject.keys())
        per_subject = max(1, n_per_step // len(subjects))

        for subject in subjects:
            subject_qs = by_subject[subject]
            by_diff = defaultdict(list)
            for q in subject_qs:
                by_diff[q["difficulty"]].append(q)
            per_diff = max(1, per_subject // 3)
            for diff_qs in by_diff.values():
                random.shuffle(diff_qs)
                sampled.extend(diff_qs[:per_diff])

        random.shuffle(sampled)
        sampled = sampled[:n_per_step]

        # Pad to exactly n_per_step if stratification fell short
        if len(sampled) < n_per_step:
            sampled_ids = {q["id"] for q in sampled}
            remaining = [q for q in qs if q["id"] not in sampled_ids]
            random.shuffle(remaining)
            sampled.extend(remaining[: n_per_step - len(sampled)])

        result[step] = sampled

    return result


def save_samples(samples: dict[str, list[dict]], data_dir: Path = None):
    data_dir = data_dir or settings.data_dir / "sampled"
    data_dir.mkdir(parents=True, exist_ok=True)

    metadata = {"sampling_strategy": "stratified_by_subject_and_difficulty", "seed": 42}

    for step, qs in samples.items():
        path = data_dir / f"{step}_sample.json"
        path.write_text(json.dumps(qs, indent=2))
        print(f"Saved {len(qs)} {step} questions to {path}")

        subject_counts = defaultdict(int)
        for q in qs:
            subject_counts[q["subject"]] += 1
        metadata[f"{step}_subject_distribution"] = dict(subject_counts)
        metadata[f"{step}_n"] = len(qs)

    (data_dir / "sample_metadata.json").write_text(json.dumps(metadata, indent=2))
