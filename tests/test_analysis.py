import pytest
import numpy as np
from pipeline.analysis.statistics import compare_models, subgroup_chi_square, effect_size_cohens_h
from pipeline.analysis.img_perspective import img_accuracy_gap_analysis


def _make_results(model_name: str, question_ids: list, correct_mask: list,
                  img_mask: list = None) -> list[dict]:
    if img_mask is None:
        img_mask = [False] * len(question_ids)
    return [
        {
            "question_id": qid,
            "model_name": model_name,
            "selected_answer": "A" if c else "B",
            "correct_answer": "A",
            "is_correct": c,
            "subject": "Anatomy",
            "step": "step1",
            "difficulty": "medium",
            "question_type": "single_best_answer",
            "img_relevant": img,
            "latency_ms": 500.0,
            "input_tokens": 100,
            "output_tokens": 50,
            "cost_usd": 0.001,
        }
        for qid, c, img in zip(question_ids, correct_mask, img_mask)
    ]


# ---------------------------------------------------------------------------
# img_accuracy_gap_analysis
# ---------------------------------------------------------------------------

def test_img_accuracy_gap_analysis_detects_gap():
    # IMG questions: 2/5 correct; non-IMG: 5/5 correct
    qids = [f"q{i}" for i in range(10)]
    img_mask = [True] * 5 + [False] * 5
    correct_mask = [True, True, False, False, False, True, True, True, True, True]
    results = _make_results("gpt-4o", qids, correct_mask, img_mask)
    df = img_accuracy_gap_analysis(results)
    assert len(df) == 1
    row = df.iloc[0]
    assert row["model"] == "gpt-4o"
    assert row["img_accuracy"] < row["non_img_accuracy"]
    assert row["accuracy_gap"] > 0


def test_img_accuracy_gap_analysis_skips_models_missing_img():
    # All questions are non-IMG — model should be skipped
    qids = [f"q{i}" for i in range(5)]
    results = _make_results("model-x", qids, [True] * 5, [False] * 5)
    df = img_accuracy_gap_analysis(results)
    assert len(df) == 0


def test_img_accuracy_gap_analysis_multi_model():
    qids = [f"q{i}" for i in range(10)]
    img_mask = [True] * 5 + [False] * 5
    r1 = _make_results("model-a", qids, [True, False, True, False, True, True, True, True, True, True], img_mask)
    r2 = _make_results("model-b", qids, [False, False, False, False, True, True, True, False, True, True], img_mask)
    df = img_accuracy_gap_analysis(r1 + r2)
    assert len(df) == 2
    assert set(df["model"]) == {"model-a", "model-b"}


# ---------------------------------------------------------------------------
# compare_models (McNemar)
# ---------------------------------------------------------------------------

def test_compare_models_returns_correct_columns():
    qids = [f"q{i}" for i in range(20)]
    correct_a = [True] * 15 + [False] * 5
    correct_b = [True] * 10 + [False] * 10
    results = {
        "model-a": _make_results("model-a", qids, correct_a),
        "model-b": _make_results("model-b", qids, correct_b),
    }
    df = compare_models(results)
    assert "model_a" in df.columns
    assert "model_b" in df.columns
    assert "p_value" in df.columns
    assert "p_adjusted" in df.columns
    assert "significant" in df.columns


def test_compare_models_three_models_six_pairs():
    qids = [f"q{i}" for i in range(20)]
    results = {
        "m1": _make_results("m1", qids, [True] * 20),
        "m2": _make_results("m2", qids, [True] * 15 + [False] * 5),
        "m3": _make_results("m3", qids, [True] * 10 + [False] * 10),
    }
    df = compare_models(results)
    # C(3,2) = 3 pairs
    assert len(df) == 3


# ---------------------------------------------------------------------------
# effect_size_cohens_h
# ---------------------------------------------------------------------------

def test_effect_size_cohens_h_zero_for_equal_proportions():
    h = effect_size_cohens_h(0.5, 0.5)
    assert abs(h) < 1e-9


def test_effect_size_cohens_h_positive_when_p1_greater():
    h = effect_size_cohens_h(0.8, 0.5)
    assert h > 0


def test_effect_size_cohens_h_known_value():
    # Cohen's h for p1=1.0, p2=0.0: 2*arcsin(1) - 2*arcsin(0) = 2*(pi/2) - 0 = pi
    h = effect_size_cohens_h(1.0, 0.0)
    assert abs(h - np.pi) < 1e-6
