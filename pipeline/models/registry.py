from .openai_model import OpenAIModel
from .anthropic_model import AnthropicModel
from .google_model import GoogleModel
from .groq_model import GroqModel
from pipeline.config import MODELS


def get_model(model_name: str):
    if model_name not in MODELS:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(MODELS.keys())}")
    provider = MODELS[model_name]["provider"]
    return {
        "openai": OpenAIModel,
        "anthropic": AnthropicModel,
        "google": GoogleModel,
        "groq": GroqModel,
    }[provider](model_name)


def get_all_models():
    return [get_model(name) for name in MODELS]
