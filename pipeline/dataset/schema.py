from pydantic import BaseModel
from typing import Optional, Literal


class Question(BaseModel):
    id: str
    question: str
    options: dict[str, str]        # {"A": "...", "B": "...", "C": "...", "D": "..."}
    answer: str                    # "A", "B", "C", or "D"
    subject: str
    step: Literal["step1", "step2ck"]
    difficulty: Literal["easy", "medium", "hard"]
    question_type: str
    img_relevant: bool = False     # Tagged if question has US-centric bias
    source: str = "MedQA-USMLE"


class EvalResult(BaseModel):
    question_id: str
    model_name: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    subject: str
    step: str
    difficulty: str
    question_type: str
    img_relevant: bool
    latency_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    expert_score: Optional[int] = None    # 1–5 from Blessie
    expert_notes: Optional[str] = None
    error: Optional[str] = None
