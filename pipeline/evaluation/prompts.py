SYSTEM_PROMPT = """You are an expert physician taking the USMLE examination.
Answer all questions based on current medical knowledge and standard clinical guidelines.
Be precise and evidence-based."""


def build_question_prompt(question: dict) -> str:
    options_text = "\n".join(
        f"{k}. {v}" for k, v in question["options"].items()
    )
    step_label = (
        question.get("step", "step1")
        .replace("step1", "Step 1")
        .replace("step2ck", "Step 2 CK")
    )
    return f"""You are taking the USMLE {step_label} examination.

Question:
{question['question']}

Options:
{options_text}

Instructions:
- Think through this carefully, step by step.
- Consider all options before deciding.
- State your final answer as: ANSWER: [A/B/C/D]
- The ANSWER line must be the last thing you write.
"""


EXPERT_ANNOTATION_PROMPT = """You are a medical educator reviewing an AI model's answer to a USMLE question.

Question: {question}
Correct Answer: {correct_answer}
Model's Answer: {model_answer}
Model's Reasoning: {reasoning}

Rate the model's reasoning quality on a scale of 1–5:
1 = Completely wrong reasoning, dangerous if applied clinically
2 = Mostly wrong, shows fundamental misunderstanding
3 = Partially correct, some valid reasoning but key errors
4 = Mostly correct reasoning, minor gaps
5 = Excellent reasoning, appropriate for clinical practice

Also note:
- Any US-centric assumptions that would disadvantage IMG students
- Any clinically dangerous reasoning patterns

Respond with JSON: {{"score": int, "notes": str, "img_bias_detected": bool}}
"""
