# Statistical Analysis

All statistical analyses are implemented in `pipeline/analysis/statistics.py` and run via `scripts/04_run_analysis.py`.

## Primary Comparison: McNemar's Test

**Why McNemar?** Each model answers the same 200 questions, creating a natural paired design. McNemar's test is the correct paired binary test for this structure — it asks: "Does model A get questions right that model B gets wrong (and vice versa), more often than chance?"

**How it works**: For each model pair (A, B), we build a 2×2 discordant-pairs table:

|  | B Correct | B Wrong |
|--|-----------|---------|
| **A Correct** | (ignored) | b |
| **A Wrong** | c | (ignored) |

The McNemar statistic tests whether `b ≠ c`. We use the exact binomial version (`statsmodels.stats.contingency_tables.mcnemar(exact=True)`) for robustness with small cell counts.

**Correction for multiple comparisons**: With 8 models, there are $\binom{8}{2} = 28$ pairwise tests. We apply the **Holm-Bonferroni step-down procedure**, which is uniformly more powerful than the Bonferroni correction while still controlling the family-wise error rate at α = 0.05.

## Effect Size: Cohen's h

For pairwise accuracy differences, we report **Cohen's h**:

$$h = 2\arcsin(\sqrt{p_1}) - 2\arcsin(\sqrt{p_2})$$

Interpretation guidelines (Cohen, 1988):

| |h| | Interpretation |
|-------|----------------|
| 0.20 | Small effect |
| 0.50 | Medium effect |
| 0.80 | Large effect |

## Subgroup Analysis: Chi-Square

Within each model, we test whether accuracy varies significantly across subgroups (e.g., medical subject or difficulty level) using a **chi-square test of independence** on the accuracy-by-subgroup contingency table.

```python
from pipeline.analysis.statistics import subgroup_chi_square

# Test whether subject explains accuracy variance for each model
df = subgroup_chi_square(results, groupby_col="subject")
```

## IMG Gap: Fisher's Exact Test

For the IMG vs. non-IMG accuracy comparison, we use **Fisher's exact test** rather than chi-square because cell counts for IMG-relevant questions may be small. The test is two-tailed.

## Confidence Intervals

All accuracy estimates are reported with **95% normal-approximation confidence intervals**:

$$\text{CI} = \hat{p} \pm 1.96 \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

## Reading the Output CSVs

After running `scripts/04_run_analysis.py`, the CSVs in `evaluation/results/` contain:

**`accuracy_by_model.csv`**

| Column | Description |
|--------|-------------|
| `group` | Model name |
| `n` | Total questions answered |
| `correct` | Number correct |
| `accuracy` | Proportion correct |
| `ci_lower` / `ci_upper` | 95% CI bounds |

**`mcnemar_tests.csv`**

| Column | Description |
|--------|-------------|
| `model_a`, `model_b` | Model pair |
| `statistic` | McNemar test statistic |
| `p_value` | Unadjusted p-value |
| `p_adjusted` | Holm-Bonferroni adjusted p-value |
| `significant` | Boolean: `p_adjusted < 0.05` |

**`img_gap_analysis.csv`**

| Column | Description |
|--------|-------------|
| `model` | Model name |
| `img_accuracy` | Accuracy on IMG-relevant questions |
| `non_img_accuracy` | Accuracy on non-IMG questions |
| `accuracy_gap` | `non_img_accuracy - img_accuracy` |
| `p_value` | Fisher's exact p-value |
| `significant` | Boolean: `p_value < 0.05` |
