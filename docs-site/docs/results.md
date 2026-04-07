# Results

!!! note "Results pending"
    The evaluation pipeline has not yet been run. This page will be updated with actual findings once the study is complete. The structure below shows what will be reported.

## What Will Be Reported

### Overall Accuracy

A horizontal bar chart (Figure 1) and summary table showing accuracy with 95% confidence intervals for each of the eight models on the combined 200-question sample. Models will be ranked from highest to lowest accuracy.

### Step 1 vs. Step 2 CK

A grouped comparison showing whether models perform differently on basic science questions (Step 1) versus clinical reasoning questions (Step 2 CK). Based on prior literature, we expect Step 2 CK to be more challenging — particularly for open-weight models.

### Subject-Level Heatmap

A heatmap (Figure 2) showing model accuracy across 15 medical subjects. This is the most granular view of model strengths and weaknesses and is the most useful output for students deciding which subjects to trust AI explanations on.

### Difficulty Analysis

Accuracy breakdown by question difficulty (easy / medium / hard) for each model.

### IMG Perspective

The accuracy gap between IMG-relevant and non-IMG questions (Figure 3), per model, with Fisher's exact test p-values. This is the novel contribution of this study.

### Pairwise Statistical Comparisons

A 8×8 heatmap of McNemar p-values (Holm-Bonferroni corrected), highlighting statistically significant performance differences.

### Expert Annotation

Mean reasoning quality scores (1–5) from the medical co-author, per model, with notes on patterns observed.

## Where to Find Results

After running the pipeline:

```
evaluation/results/
├── accuracy_by_model.csv
├── accuracy_by_subject.csv
├── mcnemar_tests.csv
├── img_gap_analysis.csv
└── cost_log.json

evaluation/figures/
├── fig1_accuracy_by_model.pdf
├── fig1_accuracy_by_model.png
├── fig3_img_gap.pdf
└── fig3_img_gap.png
```

## Paper

The full results will be reported in the companion paper submitted to JMIR Medical Education. A preprint will be linked here when available.
