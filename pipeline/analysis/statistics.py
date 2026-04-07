import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import statsmodels.stats.multitest as multitest


def compare_models(results_by_model: dict[str, list]) -> pd.DataFrame:
    """
    Run pairwise McNemar tests between all model pairs.
    Returns DataFrame: model_a, model_b, statistic, p_value, p_adjusted, significant
    """
    from itertools import combinations
    from statsmodels.stats.contingency_tables import mcnemar

    models = list(results_by_model.keys())
    rows = []

    for m1, m2 in combinations(models, 2):
        df1 = pd.DataFrame(results_by_model[m1])
        df2 = pd.DataFrame(results_by_model[m2])
        merged = df1.merge(df2, on="question_id", suffixes=("_1", "_2"))

        b = ((merged["is_correct_1"] == True) & (merged["is_correct_2"] == False)).sum()
        c = ((merged["is_correct_1"] == False) & (merged["is_correct_2"] == True)).sum()
        table = [[0, b], [c, 0]]

        result = mcnemar(table, exact=True)
        rows.append({
            "model_a": m1,
            "model_b": m2,
            "statistic": result.statistic,
            "p_value": result.pvalue,
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        _, p_adj, _, _ = multitest.multipletests(df["p_value"], method="holm")
        df["p_adjusted"] = p_adj
        df["significant"] = df["p_adjusted"] < 0.05
    return df


def subgroup_chi_square(results: list, groupby_col: str) -> pd.DataFrame:
    """Chi-square test for accuracy differences across subgroups within each model."""
    df = pd.DataFrame(results)
    rows = []
    for model, model_df in df.groupby("model_name"):
        contingency = pd.crosstab(model_df[groupby_col], model_df["is_correct"])
        chi2, p, dof, _ = chi2_contingency(contingency)
        rows.append({
            "model": model,
            "groupby": groupby_col,
            "chi2": round(chi2, 4),
            "p_value": round(p, 4),
            "dof": dof,
        })
    return pd.DataFrame(rows)


def effect_size_cohens_h(p1: float, p2: float) -> float:
    """Cohen's h effect size for two proportions."""
    return 2 * np.arcsin(np.sqrt(p1)) - 2 * np.arcsin(np.sqrt(p2))
