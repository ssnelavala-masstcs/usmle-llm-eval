from pipeline.config import EXAM_STEPS, SUBJECTS, DIFFICULTY_LEVELS, QUESTION_TYPES


def filter_by_step(questions: list[dict], step: str) -> list[dict]:
    if step not in EXAM_STEPS:
        raise ValueError(f"Invalid step: {step}. Must be one of {EXAM_STEPS}")
    return [q for q in questions if q["step"] == step]


def filter_by_subject(questions: list[dict], subject: str) -> list[dict]:
    return [q for q in questions if q["subject"] == subject]


def filter_by_difficulty(questions: list[dict], difficulty: str) -> list[dict]:
    if difficulty not in DIFFICULTY_LEVELS:
        raise ValueError(f"Invalid difficulty: {difficulty}. Must be one of {DIFFICULTY_LEVELS}")
    return [q for q in questions if q["difficulty"] == difficulty]


def filter_by_question_type(questions: list[dict], question_type: str) -> list[dict]:
    if question_type not in QUESTION_TYPES:
        raise ValueError(f"Invalid question_type: {question_type}. Must be one of {QUESTION_TYPES}")
    return [q for q in questions if q["question_type"] == question_type]


def filter_img_relevant(questions: list[dict], img_relevant: bool = True) -> list[dict]:
    return [q for q in questions if q.get("img_relevant") == img_relevant]
