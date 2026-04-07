# Dataset

## MedQA-USMLE

This project uses the **MedQA-USMLE** dataset in its four-option variant, available on HuggingFace as [`GBaker/MedQA-USMLE-4-options`](https://huggingface.co/datasets/GBaker/MedQA-USMLE-4-options).

The dataset was originally introduced by Jin et al. (2021) and contains questions derived from publicly released USMLE practice materials. All questions are formatted as single-best-answer multiple-choice items with four options (A–D). The combined train, validation, and test splits contain approximately 12,700 questions.

Each question record includes:

| Field | Description |
|-------|-------------|
| `question` | The question stem (plain text) |
| `options` | Dict with keys A, B, C, D |
| `answer_idx` | Ground truth answer letter |
| `meta_info` | Subject tag (not always populated) |

## Step Classification

Since MedQA does not provide an explicit Step 1 / Step 2 CK label, we infer the exam step using a keyword heuristic. Questions containing management or clinical decision-making language (`"next step"`, `"most appropriate management"`, `"hospitalized"`, `"follow-up"`, etc.) are classified as Step 2 CK; all others are classified as Step 1. This heuristic achieves reasonable face validity and was validated against a random subsample by the medical co-author.

## Stratified Sampling

We draw 100 questions per exam step (200 total) using the following stratification:

1. **By subject** — Proportional allocation across up to 15 medical subjects.
2. **By difficulty** — Balanced across easy / medium / hard within each subject. Difficulty is inferred from question length: `<60 words` → easy, `60–119 words` → medium, `≥120 words` → hard.

The sampling uses a fixed random seed (`42`) so that the same sample is produced on every run. Sampled questions are stored as versioned JSON files:

```
data/sampled/
├── step1_sample.json       # 100 Step 1 questions
├── step2ck_sample.json     # 100 Step 2 CK questions
└── sample_metadata.json    # Subject distribution, seed, strategy
```

## IMG Relevance Tagging

After sampling, questions are automatically tagged as `img_relevant = True` if any keyword from the US-centric lexicon appears in the question stem or answer options. See the [IMG Perspective](img-perspective.md) page and Appendix D of the paper for the full keyword list.

## Inspecting the Sample

To view the sampled questions after running `scripts/02_sample_questions.py`:

```bash
# Summary
python -c "
import json
from pathlib import Path
qs = json.loads(Path('data/sampled/step1_sample.json').read_text())
img = sum(1 for q in qs if q['img_relevant'])
subjects = {}
for q in qs:
    subjects[q['subject']] = subjects.get(q['subject'], 0) + 1
print(f'Total: {len(qs)} | IMG-relevant: {img}')
for s, n in sorted(subjects.items(), key=lambda x: -x[1]):
    print(f'  {s}: {n}')
"

# View sampling metadata
cat data/sampled/sample_metadata.json
```

## License

The MedQA dataset is licensed for research use. This project does not redistribute the raw dataset; it downloads it directly from HuggingFace at runtime via the `datasets` library.
