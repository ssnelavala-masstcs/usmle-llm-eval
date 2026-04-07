"""Subgroup breakdown analysis by subject, difficulty, question type, and step."""
import pandas as pd
from pipeline.evaluation.scorer import compute_accuracy
from pipeline.dataset.schema import EvalResult


def breakdown_by_all_dims(results: list[EvalResult]) -> dict[str, pd.DataFrame]:
    """
    Compute accuracy breakdowns across all key dimensions.
    Returns a dict of dimension name → DataFrame.
    """
    dimensions = ["model_name", "subject", "difficulty", "question_type", "step", "img_relevant"]
    return {dim: compute_accuracy(results, group_by=dim) for dim in dimensions}


def model_by_subject_pivot(results: list[EvalResult]) -> pd.DataFrame:
    """
    Return a pivot table: model × subject → accuracy.
    Useful for heatmap generation.
    """
    df = pd.DataFrame([r.model_dump() for r in results])
    pivot = df.groupby(["model_name", "subject"])["is_correct"].mean().unstack(fill_value=0)
    return pivot.round(3)


def model_by_difficulty_pivot(results: list[EvalResult]) -> pd.DataFrame:
    """Return a pivot table: model × difficulty → accuracy."""
    df = pd.DataFrame([r.model_dump() for r in results])
    pivot = df.groupby(["model_name", "difficulty"])["is_correct"].mean().unstack(fill_value=0)
    return pivot.round(3)
