"""
IMG Perspective Analysis

Identifies and analyzes questions that may disadvantage International Medical
Graduate (IMG) students due to:
1. US healthcare system-specific knowledge (insurance, referral patterns, CPT codes)
2. US-specific drug names vs. generic/international names
3. US clinical guidelines vs. international standards
4. Cultural/demographic assumptions specific to North American patients
"""

import re
import pandas as pd

US_CENTRIC_KEYWORDS = [
    # Healthcare system
    "medicaid", "medicare", "insurance", "prior authorization", "hmo", "ppo",
    "primary care physician", "referral", "emergency medical treatment",
    # US-specific drugs (brand names common in US)
    "tylenol", "advil", "motrin", "zofran", "ambien", "ativan",
    # US guidelines
    "acip", "uspstf", "ama guidelines", "joint commission",
    # Demographic assumptions
    "inner city", "rural clinic", "community health center",
]


def tag_img_relevant(questions: list[dict]) -> list[dict]:
    """Tag questions with potential US-centric bias."""
    for q in questions:
        text = (q["question"] + " ".join(q["options"].values())).lower()
        q["img_relevant"] = any(kw in text for kw in US_CENTRIC_KEYWORDS)
    return questions


def img_accuracy_gap_analysis(results: list[dict]) -> pd.DataFrame:
    """
    Compare model accuracy on IMG-relevant vs non-IMG-relevant questions.
    Returns DataFrame showing accuracy gap and statistical significance.
    """
    from scipy.stats import fisher_exact

    df = pd.DataFrame(results)
    rows = []

    for model, model_df in df.groupby("model_name"):
        img_q = model_df[model_df["img_relevant"] == True]
        non_img_q = model_df[model_df["img_relevant"] == False]

        if len(img_q) == 0 or len(non_img_q) == 0:
            continue

        img_acc = img_q["is_correct"].mean()
        non_img_acc = non_img_q["is_correct"].mean()

        table = [
            [int(img_q["is_correct"].sum()), len(img_q) - int(img_q["is_correct"].sum())],
            [int(non_img_q["is_correct"].sum()), len(non_img_q) - int(non_img_q["is_correct"].sum())],
        ]
        _, p_val = fisher_exact(table)

        rows.append({
            "model": model,
            "img_accuracy": round(img_acc, 4),
            "non_img_accuracy": round(non_img_acc, 4),
            "accuracy_gap": round(non_img_acc - img_acc, 4),
            "img_n": len(img_q),
            "non_img_n": len(non_img_q),
            "p_value": round(p_val, 4),
            "significant": p_val < 0.05,
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.sort_values("accuracy_gap", ascending=False)
