# USMLE LLM Evaluation

A systematic, reproducible evaluation of eight frontier large language models on USMLE Step 1 and Step 2 CK-style questions, with dedicated analysis of implications for international medical graduate (IMG) students.

## What This Project Does

This project benchmarks eight LLMs — GPT-4o, GPT-4o-mini, Claude 3.5 Sonnet, Claude 3 Haiku, Gemini 1.5 Pro, Gemini 1.5 Flash, Llama 3.3 70B, and DeepSeek R1 Distill 70B — on a stratified sample of 200 USMLE-style questions (100 Step 1, 100 Step 2 CK) drawn from the publicly available MedQA dataset.

Key features:

- **Standardized evaluation**: All models receive the same zero-shot, chain-of-thought prompt at temperature=0, ensuring fair, reproducible comparisons.
- **Stratified sampling**: Questions are sampled proportionally across 15 medical subjects and balanced across three difficulty levels, with a fixed random seed for exact reproducibility.
- **IMG perspective analysis**: A keyword-based lexicon identifies questions with US-centric clinical assumptions, and accuracy gaps between IMG-relevant and non-IMG questions are quantified per model.
- **Rigorous statistics**: Pairwise McNemar tests with Holm-Bonferroni correction, chi-square subgroup tests, and Cohen's h effect sizes.
- **Cost-aware**: All API responses are cached to disk — you never pay twice for the same question-model pair. Total study cost: approximately $50–$200 across all models.
- **Expert annotation**: The medical co-author provides 1–5 reasoning quality scores on a random subsample, enabling qualitative validation beyond simple accuracy.

## Why This Matters

Medical students — particularly international medical graduates — increasingly use AI chatbots for USMLE preparation. This study provides the most comprehensive multi-model, multi-step comparison to date, and is the first to systematically examine whether LLMs perform differently on questions that embed US-specific healthcare assumptions.

## Key Findings

> **Results will be published here after the evaluation pipeline is run.** See the [Results](results.md) page for the planned output structure.

## Quick Links

- [Getting Started](getting-started.md) — Set up and run the pipeline in 10 minutes
- [Models](models.md) — Details on all eight evaluated LLMs
- [Dataset](dataset.md) — MedQA dataset and sampling methodology
- [IMG Perspective](img-perspective.md) — The international medical graduate angle
- [Results](results.md) — Findings (published after evaluation)

## Paper Citation

<!-- TODO: Replace with actual citation when preprint is posted -->
```
Nelavala, S. S., & [Last Name], B. (2025). Large language model performance on
USMLE-style questions: A systematic evaluation with implications for international
medical graduates. [Journal TBD].
```

## Authors

| Name | Role |
|------|------|
| **Stanley Sujith Nelavala** | Pipeline, statistics, writing |
| **Blessie [Last Name]** | Medical expertise, annotation, clinical interpretation |
