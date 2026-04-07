# USMLE LLM Evaluation

Systematic evaluation of large language model performance on USMLE Step 1 and Step 2 CK-style questions, with a focus on the international medical graduate (IMG) perspective.

## Authors
- **Stanley Sujith Nelavala** — pipeline, statistics, writing
- **Blessie [Last Name]** — medical expertise, annotation, clinical interpretation <!-- TODO: Replace with full name -->

## Quick Start

```bash
git clone https://github.com/[github-username]/usmle-llm-eval  # TODO: Replace with actual URL
cd usmle-llm-eval
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
python scripts/01_download_dataset.py
python scripts/02_sample_questions.py
python scripts/03_run_evaluation.py --models all --questions data/sampled/step1_sample.json
python scripts/04_run_analysis.py
python scripts/05_generate_figures.py
python scripts/06_export_results.py
```

## Models Evaluated
| Model | Provider | Notes |
|-------|----------|-------|
| GPT-4o | OpenAI | Flagship |
| GPT-4o-mini | OpenAI | Cost-efficient |
| Claude 3.5 Sonnet | Anthropic | Latest reasoning |
| Claude 3 Haiku | Anthropic | Fast/cheap |
| Gemini 1.5 Pro | Google | Long context |
| Gemini 1.5 Flash | Google | Fast |
| Llama 3.3 70B | Groq (free) | Open-source |
| DeepSeek R1 Distill 70B | Groq (free) | Reasoning model |

## Docs
See the [full documentation site](https://[github-username].github.io/usmle-llm-eval/) <!-- TODO -->

## Paper
Targeting JMIR Medical Education. Preprint link: <!-- TODO: Add when available -->
