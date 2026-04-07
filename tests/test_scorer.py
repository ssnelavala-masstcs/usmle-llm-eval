import pytest
from pipeline.evaluation.scorer import compute_accuracy


def test_compute_accuracy_overall(sample_results_list):
    df = compute_accuracy(sample_results_list)
    assert len(df) == 1
    assert df.iloc[0]["group"] == "overall"
    assert df.iloc[0]["n"] == 10
    assert df.iloc[0]["correct"] == 7
    assert abs(df.iloc[0]["accuracy"] - 0.7) < 0.001


def test_compute_accuracy_ci_within_bounds(sample_results_list):
    df = compute_accuracy(sample_results_list)
    assert 0 <= df.iloc[0]["ci_lower"] <= df.iloc[0]["accuracy"]
    assert df.iloc[0]["accuracy"] <= df.iloc[0]["ci_upper"] <= 1.0


def test_compute_accuracy_group_by_subject(sample_results_list):
    df = compute_accuracy(sample_results_list, group_by="subject")
    # Should have one row per unique subject in the fixture
    subjects = {r.subject for r in sample_results_list}
    assert len(df) == len(subjects)


def test_compute_accuracy_group_by_difficulty(sample_results_list):
    df = compute_accuracy(sample_results_list, group_by="difficulty")
    difficulties = {r.difficulty for r in sample_results_list}
    assert len(df) == len(difficulties)


def test_compute_accuracy_all_ci_within_bounds_grouped(sample_results_list):
    df = compute_accuracy(sample_results_list, group_by="subject")
    assert (df["ci_lower"] >= 0).all()
    assert (df["ci_upper"] <= 1).all()
    assert (df["ci_lower"] <= df["accuracy"]).all()
    assert (df["accuracy"] <= df["ci_upper"]).all()


def test_compute_accuracy_sorted_descending(sample_results_list):
    df = compute_accuracy(sample_results_list, group_by="difficulty")
    accuracies = df["accuracy"].tolist()
    assert accuracies == sorted(accuracies, reverse=True)


def test_compute_accuracy_zero_correct():
    from pipeline.dataset.schema import EvalResult
    all_wrong = [
        EvalResult(
            question_id=f"q{i}", model_name="gpt-4o",
            selected_answer="B", correct_answer="A", is_correct=False,
            subject="Anatomy", step="step1", difficulty="easy",
            question_type="single_best_answer", img_relevant=False,
            latency_ms=100.0, input_tokens=100, output_tokens=50, cost_usd=0.001,
        )
        for i in range(5)
    ]
    df = compute_accuracy(all_wrong)
    assert df.iloc[0]["accuracy"] == 0.0
