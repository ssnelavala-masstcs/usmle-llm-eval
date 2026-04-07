# CLAUDE.md — Project Context for AI Agents

## Project
LLM Performance on USMLE-Style Questions: A Systematic Evaluation

## Authors
- Stanley Sujith Nelavala (pipeline, statistics, writing)
- Blessie [Last Name] (medical expertise, annotation, clinical interpretation)  <!-- TODO: Replace [Last Name] with Blessie's actual surname -->

## Target Journals
- Primary: JMIR Medical Education (IF 12.5)
- Secondary: Cureus, BMC Medical Education

## Novel Angle
IMG (International Medical Graduate) student perspective + Step 2 CK focus.
Most existing papers only cover Step 1 and general physician audiences.

## Stack
- Python 3.11
- HuggingFace datasets (MedQA)
- OpenAI, Anthropic, Google, Groq APIs
- pandas, scipy, statsmodels, matplotlib, seaborn
- pytest
- MkDocs + Material theme (GitHub Pages)
- LaTeX (apa7 class, biblatex/biber)

## Models Evaluated
- GPT-4o, GPT-4o-mini (OpenAI)
- Claude 3.5 Sonnet, Claude 3 Haiku (Anthropic)
- Gemini 1.5 Pro, Gemini 1.5 Flash (Google)
- Llama 3.3 70B (via Groq)
- DeepSeek R1 Distill Llama 70B (via Groq)

## Key Env Vars
OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY
RESULTS_DIR=evaluation/results
DATA_DIR=data
CACHE_DIR=.cache

## Cost Budget
~$50–$200 total. Use cache.py to avoid re-running paid API calls.
Prefer Groq (free tier) for Llama/DeepSeek.

## Dataset
MedQA (USMLE) from HuggingFace: GBaker/MedQA-USMLE-4-options
Filter to Step 1 and Step 2 CK. Sample 100 questions each, stratified by subject.

## Run Order
1. python scripts/01_download_dataset.py
2. python scripts/02_sample_questions.py
3. python scripts/03_run_evaluation.py --models all --questions data/sampled/step1_sample.json
4. python scripts/04_run_analysis.py
5. python scripts/05_generate_figures.py
6. python scripts/06_export_results.py

## Known TODOs
- Replace [Last Name] placeholders with Blessie's actual name
- Replace ssnelavala-masstcs placeholders with actual GitHub username
- Fill in Results section after running evaluation
- Add Blessie's institution affiliation to paper/main.tex
