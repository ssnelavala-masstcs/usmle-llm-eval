import pytest
from pipeline.dataset.loader import _infer_step, _infer_difficulty, _infer_question_type
from pipeline.dataset.sampler import stratified_sample
from pipeline.analysis.img_perspective import tag_img_relevant


# ---------------------------------------------------------------------------
# _infer_step
# ---------------------------------------------------------------------------

def test_infer_step_returns_step2ck_for_management_question():
    item = {"question": "A 30-year-old woman presents to the clinic. What is the most appropriate management?"}
    assert _infer_step(item) == "step2ck"


def test_infer_step_returns_step2ck_for_next_step():
    item = {"question": "What is the next step in the management of this patient?"}
    assert _infer_step(item) == "step2ck"


def test_infer_step_returns_step1_for_basic_science():
    item = {"question": "Which enzyme catalyzes the conversion of pyruvate to acetyl-CoA?"}
    assert _infer_step(item) == "step1"


def test_infer_step_returns_step2ck_for_hospitalized():
    item = {"question": "A patient hospitalized for pneumonia develops new fever on day 3."}
    assert _infer_step(item) == "step2ck"


# ---------------------------------------------------------------------------
# _infer_difficulty
# ---------------------------------------------------------------------------

def test_infer_difficulty_easy_short_question():
    item = {"question": " ".join(["word"] * 30)}
    assert _infer_difficulty(item) == "easy"


def test_infer_difficulty_medium():
    item = {"question": " ".join(["word"] * 80)}
    assert _infer_difficulty(item) == "medium"


def test_infer_difficulty_hard_long_question():
    item = {"question": " ".join(["word"] * 150)}
    assert _infer_difficulty(item) == "hard"


def test_infer_difficulty_returns_valid_level():
    for length in [20, 70, 130]:
        item = {"question": " ".join(["word"] * length)}
        assert _infer_difficulty(item) in ("easy", "medium", "hard")


# ---------------------------------------------------------------------------
# stratified_sample
# ---------------------------------------------------------------------------

def _make_questions(n=300):
    """Generate synthetic questions with both steps and 3 difficulties."""
    questions = []
    subjects = ["Anatomy", "Physiology", "Biochemistry", "Pharmacology", "Pathology"]
    for i in range(n):
        questions.append({
            "id": f"q{i:04d}",
            "question": f"Question text {i}",
            "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
            "answer": "A",
            "subject": subjects[i % len(subjects)],
            "step": "step1" if i % 2 == 0 else "step2ck",
            "difficulty": ["easy", "medium", "hard"][i % 3],
            "question_type": "single_best_answer",
            "img_relevant": False,
            "source": "test",
        })
    return questions


def test_stratified_sample_returns_exactly_n_per_step():
    questions = _make_questions(300)
    samples = stratified_sample(questions, n_per_step=50, seed=0)
    for step in ["step1", "step2ck"]:
        assert len(samples[step]) == 50


def test_stratified_sample_includes_all_difficulties():
    questions = _make_questions(300)
    samples = stratified_sample(questions, n_per_step=50, seed=0)
    for step, qs in samples.items():
        difficulties = {q["difficulty"] for q in qs}
        assert len(difficulties) > 1, f"{step} sample missing difficulty variation"


def test_stratified_sample_is_reproducible():
    questions = _make_questions(300)
    s1 = stratified_sample(questions, n_per_step=30, seed=42)
    s2 = stratified_sample(questions, n_per_step=30, seed=42)
    assert [q["id"] for q in s1["step1"]] == [q["id"] for q in s2["step1"]]


def test_stratified_sample_different_seeds_differ():
    questions = _make_questions(300)
    s1 = stratified_sample(questions, n_per_step=30, seed=1)
    s2 = stratified_sample(questions, n_per_step=30, seed=2)
    # Very unlikely to be identical with different seeds
    assert [q["id"] for q in s1["step1"]] != [q["id"] for q in s2["step1"]]


# ---------------------------------------------------------------------------
# tag_img_relevant
# ---------------------------------------------------------------------------

def test_tag_img_relevant_detects_us_keywords():
    questions = [
        {
            "id": "img1",
            "question": "A patient on Medicaid presents to the clinic.",
            "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
        },
        {
            "id": "non1",
            "question": "A patient presents with chest pain and dyspnea.",
            "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
        },
    ]
    tagged = tag_img_relevant(questions)
    assert tagged[0]["img_relevant"] is True
    assert tagged[1]["img_relevant"] is False


def test_tag_img_relevant_detects_brand_name_drugs():
    questions = [{
        "id": "drug1",
        "question": "A patient took Tylenol overdose.",
        "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
    }]
    tagged = tag_img_relevant(questions)
    assert tagged[0]["img_relevant"] is True


def test_tag_img_relevant_case_insensitive():
    questions = [{
        "id": "case1",
        "question": "Patient enrolled in MEDICARE.",
        "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
    }]
    tagged = tag_img_relevant(questions)
    assert tagged[0]["img_relevant"] is True
