# FAQ

**Q: How much will this cost to run?**

Running all 8 models on 200 questions (100 Step 1 + 100 Step 2 CK) costs approximately $50–$200 depending on current API pricing. The main cost drivers are GPT-4o (~$0.005/1K input tokens) and Claude 3.5 Sonnet (~$0.003/1K input tokens). Llama 3.3 70B and DeepSeek R1 70B via Groq are completely free. The disk cache ensures you never re-pay for a cached response.

---

**Q: Why use Groq for Llama and DeepSeek instead of running them locally?**

Groq's LPU (Language Processing Unit) hardware provides extremely fast inference — far faster than a typical GPU setup — and the free tier covers our usage volume. Running these models locally would require significant GPU memory (at least 80GB for a 70B model at float16) and introduce hardware-dependent variability. Groq provides a consistent, reproducible inference environment that mirrors how most users would access these models in practice.

---

**Q: How does the disk cache work?**

Every API response is stored in `.cache/` using `diskcache`, keyed by `<model_name>:<question_id>`. On subsequent runs, if a key exists in the cache, the stored response is used instead of making an API call. This means:

- If you run the same model on the same questions twice, you only pay once.
- If you add a new model or new questions, only the new combinations incur API costs.
- To force a re-run: use `--no-cache` flag or call `ResponseCache().clear()`.

---

**Q: How do I cite this work?**

<!-- TODO: Replace with actual citation when paper is published -->
```
Nelavala, S. S., & [Last Name], B. (2025). Large language model performance on
USMLE-style questions: A systematic evaluation with implications for international
medical graduates. [Journal TBD]. [DOI TBD]
```

---

**Q: Are there any IRB considerations?**

This study uses only publicly available, de-identified question-and-answer data from the MedQA dataset, which is derived from released USMLE practice materials. No human subjects data is collected or analyzed. Expert annotations are contributed by a co-author in their professional capacity. Standard IRB review for human subjects research is not required for this study design, but researchers adapting this work to include patient data or human subject experiments should seek appropriate ethical review.

---

**Q: Why MedQA and not actual retired USMLE questions?**

Retired official USMLE items are not publicly available for research use without a licensing agreement with the NBME. MedQA is the closest publicly available proxy and is widely used in published LLM evaluation research. We acknowledge this as a limitation: MedQA may not fully reflect current USMLE difficulty distribution or item formats.

---

**Q: How do I reproduce the exact results from the paper?**

1. Use `--seed 42` (the default) when running `scripts/02_sample_questions.py`. This produces the exact same 200-question sample.
2. Use `temperature=0` (already hardcoded in all model implementations).
3. Do not clear the cache between runs of the same model.
4. Use the same model API versions specified in `pipeline/config.py` (e.g., `claude-3-5-sonnet-20241022`). Model providers may silently update models behind the same API name; check the model card at time of reproduction.

---

**Q: What does `temperature=0` mean and why does it matter?**

`temperature=0` tells the model to always select the highest-probability token at each step, making the output deterministic (or near-deterministic, depending on the provider's implementation). This is essential for reproducibility: running the same model on the same question twice should produce the same answer. Without `temperature=0`, stochastic sampling would introduce variance that makes it harder to attribute accuracy differences to the model rather than to random noise.

---

**Q: Can I run only a subset of models to save money?**

Yes. Use the `--models` flag:

```bash
python scripts/03_run_evaluation.py \
  --models llama-3.3-70b,deepseek-r1-70b \
  --questions data/sampled/step1_sample.json
```

All subsequent analysis scripts will process whatever result files exist in `evaluation/results/`, so partial runs are fully supported.

---

**Q: How do I add more questions (e.g., 200 per step instead of 100)?**

```bash
python scripts/02_sample_questions.py --n 200 --seed 42
```

This overwrites the existing sample files. Re-run script 03 afterward. Note that doubling the question count will approximately double the API cost.

---

**Q: Why do some models return `selected_answer = "X"`?**

`"X"` is the sentinel value returned when `extract_answer()` cannot find a clear A/B/C/D selection in the model's response. This happens rarely — primarily when a model produces a very short, non-standard response or when an API error occurs. These responses are counted as incorrect. Check `error` field in the result JSON for API errors.

---

**Q: How is the expert annotation integrated into the statistical analysis?**

Expert scores are stored in the `expert_score` and `expert_notes` fields of `EvalResult`. After the medical co-author completes the annotation sheet (generated by `pipeline/evaluation/annotator.py`), the filled CSV is merged back using `merge_annotations()`. The merged results can then be used for correlation analysis between expert score and model accuracy, and for reporting inter-rater reliability if a second annotator reviews a subsample.
