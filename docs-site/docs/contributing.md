# Contributing

## Development Setup

```bash
git clone https://github.com/ssnelavala-masstcs/usmle-llm-eval  # TODO: Replace URL
cd usmle-llm-eval
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
```

Run the test suite to verify everything is working:

```bash
pytest tests/ -v
```

All tests mock external API calls and pass without real API keys.

## Adding a New Model

1. Add an entry to `MODELS` in `pipeline/config.py` with `provider`, `model_id`, and cost fields.
2. If the provider is new, create `pipeline/models/<provider>_model.py` extending `LLMModel` from `pipeline/models/base.py`. Implement `answer_question()` with:
   - The `@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))` decorator from `tenacity`
   - `temperature=0`
   - Returns a `ModelResponse` dataclass
3. Register the new provider in `pipeline/models/registry.py`.
4. Add tests in `tests/test_models.py` using mocked API responses.

## Adding New Question Sets

To evaluate on a different question source:

1. Write a loader function in `pipeline/dataset/loader.py` that returns a list of dicts conforming to the `Question` schema in `pipeline/dataset/schema.py`.
2. Save the questions to `data/sampled/<name>.json`.
3. Pass the file to script 03: `python scripts/03_run_evaluation.py --questions data/sampled/<name>.json`.

## Contributing Expert Annotations

If you are a medical professional and would like to contribute expert annotations:

1. Request the annotation sheet from the authors (generated via `pipeline/evaluation/annotator.py`).
2. Fill in the `expert_score` (1–5), `expert_notes`, and `img_bias_detected` (yes/no) columns.
3. Return the completed CSV to the authors for merging via `merge_annotations()`.

See Appendix C of the paper for the full annotation rubric.

## Pull Request Guidelines

- Keep PRs focused — one logical change per PR.
- All new code must have corresponding tests.
- Ensure `pytest tests/ -v` passes before submitting.
- Do not commit `.env` files or API keys.
- Follow the existing code style (no comments unless logic is non-obvious, no type annotations on unchanged code).

## Docs Contributions

The docs site is built with MkDocs Material. To preview locally:

```bash
cd docs-site
pip install mkdocs-material mkdocs-minify-plugin
mkdocs serve
```

Then open `http://localhost:8000`.
