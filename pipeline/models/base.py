from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelResponse:
    model_name: str
    question_id: str
    raw_response: str
    selected_answer: str          # A, B, C, or D
    reasoning: str                # extracted chain-of-thought
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost_usd: float
    error: Optional[str] = None


class LLMModel(ABC):
    def __init__(self, model_name: str, model_id: str):
        self.model_name = model_name
        self.model_id = model_id

    @abstractmethod
    def answer_question(self, question: dict) -> ModelResponse:
        """
        Takes a MedQA-formatted question dict:
        {
          "id": str,
          "question": str,
          "options": {"A": str, "B": str, "C": str, "D": str},
          "answer": str,           # ground truth
          "subject": str,
          "step": str,
          "difficulty": str
        }
        Returns a ModelResponse.
        """
        pass

    def format_prompt(self, question: dict) -> str:
        options_text = "\n".join(
            f"{k}. {v}" for k, v in question["options"].items()
        )
        return (
            f"You are taking a USMLE {question.get('step', 'Step 1').upper()} examination.\n\n"
            f"Question:\n{question['question']}\n\n"
            f"Options:\n{options_text}\n\n"
            "Instructions:\n"
            "1. Think through this step by step.\n"
            "2. At the end, state your final answer as exactly: ANSWER: [A/B/C/D]\n"
            "3. Do not hedge — choose the single best answer.\n"
        )

    def extract_answer(self, response_text: str) -> str:
        """Extract A/B/C/D from model response. Returns 'X' if not found."""
        import re
        # Try explicit ANSWER: X format first
        match = re.search(r"ANSWER:\s*([A-D])", response_text, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        # Fallback: last standalone A/B/C/D letter
        matches = re.findall(r"\b([A-D])\b", response_text)
        if matches:
            return matches[-1].upper()
        return "X"
