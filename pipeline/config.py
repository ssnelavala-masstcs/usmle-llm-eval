from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "populate_by_name": True,
    }

    # API Keys
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")

    # Paths
    results_dir: Path = Field(default=Path("evaluation/results"))
    data_dir: Path = Field(default=Path("data"))
    cache_dir: Path = Field(default=Path(".cache"))

    # Evaluation
    max_questions_per_run: int = 200
    request_timeout: int = 60
    max_retries: int = 3
    enable_cache: bool = True

    # Cost tracking
    cost_log_file: Path = Field(default=Path("evaluation/results/cost_log.json"))

    def ensure_dirs(self):
        for d in [self.results_dir, self.data_dir, self.cache_dir,
                  self.data_dir / "raw", self.data_dir / "sampled",
                  self.data_dir / "annotations", Path("evaluation/figures")]:
            d.mkdir(parents=True, exist_ok=True)


settings = Settings()


# All models available for evaluation
MODELS = {
    "gpt-4o": {"provider": "openai", "model_id": "gpt-4o", "cost_per_1k_input": 0.005, "cost_per_1k_output": 0.015},
    "gpt-4o-mini": {"provider": "openai", "model_id": "gpt-4o-mini", "cost_per_1k_input": 0.00015, "cost_per_1k_output": 0.0006},
    "claude-3-5-sonnet": {"provider": "anthropic", "model_id": "claude-3-5-sonnet-20241022", "cost_per_1k_input": 0.003, "cost_per_1k_output": 0.015},
    "claude-3-haiku": {"provider": "anthropic", "model_id": "claude-3-haiku-20240307", "cost_per_1k_input": 0.00025, "cost_per_1k_output": 0.00125},
    "gemini-1.5-pro": {"provider": "google", "model_id": "gemini-1.5-pro", "cost_per_1k_input": 0.00125, "cost_per_1k_output": 0.005},
    "gemini-1.5-flash": {"provider": "google", "model_id": "gemini-1.5-flash", "cost_per_1k_input": 0.000075, "cost_per_1k_output": 0.0003},
    "llama-3.3-70b": {"provider": "groq", "model_id": "llama-3.3-70b-versatile", "cost_per_1k_input": 0.0, "cost_per_1k_output": 0.0},
    "deepseek-r1-70b": {"provider": "groq", "model_id": "deepseek-r1-distill-llama-70b", "cost_per_1k_input": 0.0, "cost_per_1k_output": 0.0},
}

SUBJECTS = [
    "Anatomy", "Physiology", "Biochemistry", "Pharmacology",
    "Pathology", "Microbiology", "Immunology", "Behavioral Science",
    "Biostatistics", "Internal Medicine", "Surgery", "Pediatrics",
    "Obstetrics & Gynecology", "Psychiatry", "Neurology"
]

DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
QUESTION_TYPES = ["single_best_answer", "clinical_vignette", "laboratory_data"]
EXAM_STEPS = ["step1", "step2ck"]
