# IMG Perspective

## Background

International medical graduates (IMGs) represent approximately 25% of the active physician workforce in the United States, yet consistently show lower first-attempt pass rates on USMLE examinations compared to US/Canadian graduates. One contributing factor is that many USMLE questions embed assumptions about the US healthcare system, clinical epidemiology, and drug naming conventions that are less familiar to physicians trained outside North America.

As LLMs become widely used as study aids — particularly by IMGs who may not have access to expensive commercial question banks — it is important to ask: **do these models perform less reliably on the very questions that most disadvantage IMG students?**

## What "IMG-Relevant" Means

We define an IMG-relevant question as one that references knowledge specific to the US healthcare context in ways that would be unfamiliar to a physician trained in another country. This includes:

| Category | Examples |
|----------|---------|
| **US Insurance / Financing** | Medicaid, Medicare, prior authorization, HMO, PPO |
| **US Referral Patterns** | "refers to primary care physician", "emergency medical treatment" |
| **US Brand-Name Drugs** | Tylenol (acetaminophen), Advil (ibuprofen), Zofran (ondansetron) |
| **US Guideline Bodies** | ACIP vaccine schedules, USPSTF recommendations |
| **US Demographic Context** | "inner city clinic", "community health center" |

Note that IMG-relevance does not mean the question is unfair — it is part of what a US-licensed physician must know. It simply means that a well-qualified physician from another country may face an additional knowledge burden that is unrelated to their clinical competence.

## How Tagging Works

Questions are tagged automatically using a keyword lexicon (`pipeline/analysis/img_perspective.py`):

```python
from pipeline.analysis.img_perspective import tag_img_relevant

questions = tag_img_relevant(questions)
# Each question gets q["img_relevant"] = True or False
```

The lexicon matches case-insensitively against the question stem and all four answer options. Any match → `img_relevant = True`.

This automated tagging was validated by the medical co-author, who reviewed a random 20% subsample and confirmed or corrected each label.

## Analysis

The IMG gap analysis compares model accuracy on IMG-relevant vs. non-IMG questions using Fisher's exact test:

```python
from pipeline.analysis.img_perspective import img_accuracy_gap_analysis

df = img_accuracy_gap_analysis(all_results)
# Returns: model, img_accuracy, non_img_accuracy, accuracy_gap, p_value, significant
```

A positive `accuracy_gap` means the model is less accurate on IMG-relevant questions — the finding we hypothesize will hold for models trained primarily on US-centric medical content.

## Blessie's Validation Role

The medical co-author reviews a random subsample of model answers and records:

- **IMG bias detected** (yes/no): Did the model's reasoning reflect US-specific assumptions that would mislead a non-US clinician?
- **Expert score** (1–5): Quality of the model's clinical reasoning overall.

This qualitative layer supplements the keyword-based accuracy gap analysis with human judgment about whether the model's reasoning — not just its final answer — encodes US-centric biases.

## Implications for IMG Students

Regardless of the specific numerical findings, IMG students should be aware:

1. LLMs are trained largely on English-language internet text, which skews toward US medical content.
2. Model accuracy on questions involving US healthcare system knowledge has not been independently validated for the IMG context.
3. For Step 2 CK specifically, supplementing AI-based review with US-specific resources (First Aid for Step 2 CK, UWorld, Amboss) remains important.
4. When a model explains US insurance or referral concepts, cross-check against official USMLE resources — do not assume the model's framing of "what a US physician would do" is accurate.
