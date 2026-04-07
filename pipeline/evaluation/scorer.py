import pandas as pd
import numpy as np
from scipy import stats
from pipeline.dataset.schema import EvalResult


def compute_accuracy(results: list[EvalResult], group_by: str = None) -> pd.DataFrame:
    """
    Compute accuracy overall or grouped by a field (subject, difficulty, step, model_name).
    Returns a DataFrame with columns: [group, n, correct, accuracy, ci_lower, ci_upper]
    """
    df = pd.DataFrame([r.model_dump() for r in results])

    def acc_with_ci(correct, n):
        if n == 0:
            return 0.0, 0.0, 0.0
        p = correct / n
        se = np.sqrt(p * (1 - p) / n)
        ci = stats.norm.ppf(0.975) * se
        return round(p, 4), round(max(0, p - ci), 4), round(min(1, p + ci), 4)

    if group_by is None:
        n = len(df)
        correct = int(df["is_correct"].sum())
        acc, ci_lo, ci_hi = acc_with_ci(correct, n)
        return pd.DataFrame([{
            "group": "overall", "n": n, "correct": correct,
            "accuracy": acc, "ci_lower": ci_lo, "ci_upper": ci_hi,
        }])

    rows = []
    for group_val, sub in df.groupby(group_by):
        n = len(sub)
        correct = int(sub["is_correct"].sum())
        acc, ci_lo, ci_hi = acc_with_ci(correct, n)
        rows.append({
            "group": group_val, "n": n, "correct": correct,
            "accuracy": acc, "ci_lower": ci_lo, "ci_upper": ci_hi,
        })
    return pd.DataFrame(rows).sort_values("accuracy", ascending=False)
