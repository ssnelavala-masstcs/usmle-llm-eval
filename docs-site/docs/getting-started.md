# Getting Started

This guide walks you through setting up the project and running the full evaluation pipeline from scratch.

## Prerequisites

- Python 3.11+
- Git
- API keys for at least one provider (see note on cost below)

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/[github-username]/usmle-llm-eval  # TODO: Replace URL
cd usmle-llm-eval
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure API keys**

```bash
cp .env.example .env
```

Edit `.env` and fill in your API keys:

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
GROQ_API_KEY=gsk_...
```

!!! warning "Cost warning"
    Running all 8 models on 200 questions costs approximately **$50–$200** depending on current API pricing. The paid models (OpenAI, Anthropic, Google) account for almost all of this cost. Llama 3.3 70B and DeepSeek R1 via Groq are **free** on the Groq free tier.

    The disk cache (`ENABLE_CACHE=true` in `.env`) ensures you never pay twice for the same question-model pair. Do not delete the `.cache/` directory between runs.

!!! tip "Run free models first"
    If you want to explore the pipeline without spending money, set `--models llama-3.3-70b,deepseek-r1-70b` in step 3 to run only the Groq-hosted free models first.

## Running the Pipeline

Run the six scripts in order:

**Step 1 — Download the dataset**

```bash
python scripts/01_download_dataset.py
```

Downloads MedQA-USMLE from HuggingFace and caches it to `data/raw/medqa_all.json`. Takes ~2–5 minutes on first run; subsequent runs load from cache instantly.

**Step 2 — Sample questions**

```bash
python scripts/02_sample_questions.py --n 100 --seed 42
```

Produces `data/sampled/step1_sample.json` and `data/sampled/step2ck_sample.json`, each containing 100 stratified questions. Also tags IMG-relevant questions. `--seed 42` is the default; changing it produces a different but reproducible sample.

**Step 3 — Run evaluation**

```bash
# All models on Step 1:
python scripts/03_run_evaluation.py --models all --questions data/sampled/step1_sample.json

# All models on Step 2 CK:
python scripts/03_run_evaluation.py --models all --questions data/sampled/step2ck_sample.json

# Single model only:
python scripts/03_run_evaluation.py --models gpt-4o --questions data/sampled/step1_sample.json
```

Results are saved to `evaluation/results/<model_name>_<step>.json`. API responses are cached automatically.

**Step 4 — Statistical analysis**

```bash
python scripts/04_run_analysis.py
```

Reads all result JSONs from `evaluation/results/`, computes accuracy tables, pairwise McNemar tests, and IMG gap analysis. Saves CSVs to `evaluation/results/`.

**Step 5 — Generate figures**

```bash
python scripts/05_generate_figures.py
```

Produces PDF and PNG figures in `evaluation/figures/`.

**Step 6 — Export LaTeX tables**

```bash
python scripts/06_export_results.py
```

Converts result CSVs to LaTeX `\begin{table}` environments, saved to `paper/sections/table_*.tex`.

## Cache Behavior

The disk cache lives in `.cache/` (configured by `CACHE_DIR` in `.env`). Each entry is keyed by `<model_name>:<question_id>`. To force a re-run without cache:

```bash
python scripts/03_run_evaluation.py --no-cache --models gpt-4o --questions data/sampled/step1_sample.json
```

To clear the entire cache:

```python
from pipeline.utils.cache import ResponseCache
ResponseCache().clear()
```

## Running Tests

```bash
pytest tests/ -v
```

All tests mock external API calls and run without requiring real API keys.
