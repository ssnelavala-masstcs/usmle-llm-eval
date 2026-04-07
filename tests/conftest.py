import pytest
from pipeline.dataset.schema import Question, EvalResult


@pytest.fixture
def sample_question():
    return {
        "id": "test_001",
        "question": "A 45-year-old man presents with crushing chest pain radiating to the left arm. ECG shows ST elevation in leads II, III, aVF. What is the most appropriate next step?",
        "options": {
            "A": "Administer aspirin 325mg and activate cath lab",
            "B": "Obtain troponin levels and wait for results",
            "C": "Administer nitroglycerin and observe",
            "D": "Perform echocardiogram",
        },
        "answer": "A",
        "subject": "Cardiology",
        "step": "step2ck",
        "difficulty": "medium",
        "question_type": "clinical_vignette",
        "img_relevant": False,
        "source": "MedQA-test",
    }


@pytest.fixture
def sample_eval_result():
    return EvalResult(
        question_id="test_001",
        model_name="gpt-4o",
        selected_answer="A",
        correct_answer="A",
        is_correct=True,
        subject="Cardiology",
        step="step2ck",
        difficulty="medium",
        question_type="clinical_vignette",
        img_relevant=False,
        latency_ms=1200.5,
        input_tokens=300,
        output_tokens=150,
        cost_usd=0.003,
    )


@pytest.fixture
def sample_results_list():
    """10 EvalResult objects: 7 correct, 3 incorrect, across subjects and difficulties."""
    base = dict(
        model_name="gpt-4o",
        step="step1",
        question_type="single_best_answer",
        img_relevant=False,
        latency_ms=500.0,
        input_tokens=200,
        output_tokens=100,
        cost_usd=0.001,
    )
    entries = [
        {"question_id": f"q{i:03d}", "selected_answer": ans, "correct_answer": "A",
         "is_correct": ans == "A", "subject": subj, "difficulty": diff}
        for i, (ans, subj, diff) in enumerate([
            ("A", "Anatomy", "easy"),
            ("A", "Physiology", "easy"),
            ("A", "Biochemistry", "medium"),
            ("A", "Pharmacology", "medium"),
            ("A", "Pathology", "hard"),
            ("A", "Microbiology", "hard"),
            ("A", "Immunology", "easy"),
            ("B", "Anatomy", "medium"),
            ("B", "Physiology", "hard"),
            ("B", "Biochemistry", "easy"),
        ])
    ]
    return [EvalResult(**{**base, **e}) for e in entries]
