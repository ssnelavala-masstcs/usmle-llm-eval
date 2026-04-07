# Models

## Evaluated Models

All eight models are evaluated under identical conditions: the same prompt template, `temperature=0`, `max_tokens=512`, and no system prompt.

| Model Key | Display Name | Provider | ~Parameters | Input $/1K | Output $/1K |
|-----------|-------------|----------|-------------|------------|-------------|
| `gpt-4o` | GPT-4o | OpenAI | Not disclosed | $0.005 | $0.015 |
| `gpt-4o-mini` | GPT-4o-mini | OpenAI | Not disclosed | $0.00015 | $0.0006 |
| `claude-3-5-sonnet` | Claude 3.5 Sonnet | Anthropic | Not disclosed | $0.003 | $0.015 |
| `claude-3-haiku` | Claude 3 Haiku | Anthropic | Not disclosed | $0.00025 | $0.00125 |
| `gemini-1.5-pro` | Gemini 1.5 Pro | Google | Not disclosed | $0.00125 | $0.005 |
| `gemini-1.5-flash` | Gemini 1.5 Flash | Google | Not disclosed | $0.000075 | $0.0003 |
| `llama-3.3-70b` | Llama 3.3 70B | Meta (via Groq) | 70B | Free | Free |
| `deepseek-r1-70b` | DeepSeek R1 Distill 70B | DeepSeek (via Groq) | 70B | Free | Free |

Prices reflect approximate rates at the time of study design. Check current provider pricing before running at scale.

## Selecting Models for a Run

Use the `--models` flag in `scripts/03_run_evaluation.py`:

```bash
# Run all 8 models
python scripts/03_run_evaluation.py --models all --questions data/sampled/step1_sample.json

# Run a specific subset
python scripts/03_run_evaluation.py \
  --models gpt-4o,claude-3-5-sonnet,llama-3.3-70b \
  --questions data/sampled/step1_sample.json

# Run only free models (Groq-hosted)
python scripts/03_run_evaluation.py \
  --models llama-3.3-70b,deepseek-r1-70b \
  --questions data/sampled/step1_sample.json
```

## Adding a New Model

To add a model not in the current registry:

**Step 1** — Add an entry to `MODELS` in `pipeline/config.py`:

```python
MODELS["my-new-model"] = {
    "provider": "openai",       # or "anthropic", "google", "groq"
    "model_id": "gpt-4-turbo",  # exact API model identifier
    "cost_per_1k_input": 0.01,
    "cost_per_1k_output": 0.03,
}
```

**Step 2** — If the provider is new, create a file `pipeline/models/my_provider_model.py` extending `LLMModel` from `pipeline/models/base.py`, implementing the `answer_question()` method.

**Step 3** — Register it in `pipeline/models/registry.py`:

```python
from .my_provider_model import MyProviderModel
# Add to the provider dispatch dict:
"myprovider": MyProviderModel,
```

The new model will automatically be included in `--models all` runs and cost tracking.

## Model Architecture Notes

- **GPT-4o / GPT-4o-mini**: OpenAI's latest generation multimodal models. Both support the standard chat completions API.
- **Claude 3.5 Sonnet / Haiku**: Anthropic's messages API. Sonnet is the most capable; Haiku is optimized for speed and cost.
- **Gemini 1.5 Pro / Flash**: Google's `google-generativeai` SDK. Pro supports a 1M-token context window; Flash is optimized for latency.
- **Llama 3.3 70B**: Meta's open-weight model, served via Groq's LPU inference hardware. Uses the same chat completions API interface as OpenAI.
- **DeepSeek R1 Distill Llama 70B**: A reasoning-focused model distilled from DeepSeek R1 into the Llama 70B architecture. Also served via Groq. Expected to produce longer, more deliberate reasoning chains.
