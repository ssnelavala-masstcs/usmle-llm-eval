# Running the Evaluation

## Overview

The evaluation pipeline consists of six scripts that must be run in order. Each script is idempotent — running it again will not duplicate work if outputs already exist or if the cache is warm.

```
01_download_dataset.py  →  02_sample_questions.py  →  03_run_evaluation.py
                                                            ↓
06_export_results.py    ←  05_generate_figures.py   ←  04_run_analysis.py
```

## Script Reference

### Script 01 — Download Dataset

```bash
python scripts/01_download_dataset.py
```

**What it does**: Downloads `GBaker/MedQA-USMLE-4-options` from HuggingFace, normalizes all splits (train/validation/test) into a unified question schema, and caches the result to `data/raw/medqa_all.json`.

**Output**: `data/raw/medqa_all.json` (~12,700 questions, ~50MB)

**Time**: ~2–5 minutes on first run; instant on subsequent runs (cache hit).

---

### Script 02 — Sample Questions

```bash
python scripts/02_sample_questions.py [--n 100] [--seed 42]
```

**What it does**: Loads the cached dataset, applies the IMG keyword tagger, and draws a stratified sample of `n` questions per exam step.

**Output**:

- `data/sampled/step1_sample.json`
- `data/sampled/step2ck_sample.json`
- `data/sampled/sample_metadata.json`

**Options**:

| Flag | Default | Description |
|------|---------|-------------|
| `--n` | 100 | Questions per step (200 total) |
| `--seed` | 42 | Random seed for reproducibility |

---

### Script 03 — Run Evaluation

```bash
python scripts/03_run_evaluation.py \
  [--models all] \
  [--questions data/sampled/step1_sample.json] \
  [--no-cache]
```

**What it does**: For each selected model, sends every question in the specified file to the model API, records the response, and saves results to `evaluation/results/<model>_<step>.json`.

**Output**: One JSON file per model per step, e.g.:
```
evaluation/results/gpt-4o_step1.json
evaluation/results/claude-3-5-sonnet_step1.json
...
```

**Options**:

| Flag | Default | Description |
|------|---------|-------------|
| `--models` | `all` | Model keys (comma-separated) or `all` |
| `--questions` | `data/sampled/step1_sample.json` | Path to question JSON |
| `--no-cache` | off | Bypass disk cache (forces API re-calls) |

!!! warning "Run both steps"
    Run script 03 twice — once for Step 1 and once for Step 2 CK — to get the full dataset:
    ```bash
    python scripts/03_run_evaluation.py --models all --questions data/sampled/step1_sample.json
    python scripts/03_run_evaluation.py --models all --questions data/sampled/step2ck_sample.json
    ```

**Cost log**: After each run, `evaluation/results/cost_log.json` is updated with cumulative token usage and USD cost per model.

---

### Script 04 — Statistical Analysis

```bash
python scripts/04_run_analysis.py
```

**What it does**: Reads all `*.json` files in `evaluation/results/` (excluding `cost_log.json`), computes:

- Overall accuracy by model (with 95% CIs)
- Accuracy by subject
- Pairwise McNemar tests (Holm-Bonferroni corrected)
- IMG accuracy gap analysis

**Output CSVs** in `evaluation/results/`:

- `accuracy_by_model.csv`
- `accuracy_by_subject.csv`
- `mcnemar_tests.csv`
- `img_gap_analysis.csv`

---

### Script 05 — Generate Figures

```bash
python scripts/05_generate_figures.py
```

**What it does**: Reads the CSVs from script 04 and generates publication-quality figures.

**Output** in `evaluation/figures/`:

- `fig1_accuracy_by_model.pdf` / `.png`
- `fig3_img_gap.pdf` / `.png`

(Figure 2 — subject heatmap — requires the full merged results DataFrame and is generated separately via `pipeline/analysis/plots.py`.)

---

### Script 06 — Export LaTeX Tables

```bash
python scripts/06_export_results.py
```

**What it does**: Converts each CSV in `evaluation/results/` to a LaTeX `\begin{table}` environment with `booktabs` formatting.

**Output** in `paper/sections/`:

- `table_accuracy_by_model.tex`
- `table_accuracy_by_subject.tex`
- `table_mcnemar_tests.tex`
- `table_img_gap_analysis.tex`

Include these in the paper by adding `\input{sections/table_accuracy_by_model}` to `paper/sections/results.tex`.
