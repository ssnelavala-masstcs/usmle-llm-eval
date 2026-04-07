import json
import pytest
from pathlib import Path
from pipeline.utils.cost_tracker import CostTracker


def test_record_accumulates_cost():
    tracker = CostTracker()
    tracker.record("gpt-4o", 0.01, 100, 50)
    tracker.record("gpt-4o", 0.02, 200, 80)
    assert abs(tracker.records["gpt-4o"]["cost_usd"] - 0.03) < 1e-9


def test_record_accumulates_tokens():
    tracker = CostTracker()
    tracker.record("gpt-4o", 0.01, 100, 50)
    tracker.record("gpt-4o", 0.01, 200, 80)
    assert tracker.records["gpt-4o"]["input_tokens"] == 300
    assert tracker.records["gpt-4o"]["output_tokens"] == 130


def test_record_counts_calls():
    tracker = CostTracker()
    for _ in range(5):
        tracker.record("gpt-4o", 0.001, 10, 5)
    assert tracker.records["gpt-4o"]["calls"] == 5


def test_record_multiple_models():
    tracker = CostTracker()
    tracker.record("gpt-4o", 0.05, 100, 50)
    tracker.record("claude-3-5-sonnet", 0.03, 80, 40)
    summary = tracker.summary()
    assert abs(summary["total_cost_usd"] - 0.08) < 1e-9
    assert "gpt-4o" in summary["by_model"]
    assert "claude-3-5-sonnet" in summary["by_model"]


def test_summary_returns_correct_structure():
    tracker = CostTracker()
    tracker.record("model-a", 0.1, 500, 200)
    summary = tracker.summary()
    assert "total_cost_usd" in summary
    assert "by_model" in summary
    assert isinstance(summary["total_cost_usd"], float)
    assert isinstance(summary["by_model"], dict)


def test_save_writes_valid_json(tmp_path):
    tracker = CostTracker()
    tracker.record("gpt-4o", 0.05, 100, 50)
    out = tmp_path / "cost_log.json"
    tracker.save(out)
    assert out.exists()
    data = json.loads(out.read_text())
    assert "total_cost_usd" in data
    assert "by_model" in data
    assert data["by_model"]["gpt-4o"]["calls"] == 1


def test_summary_total_cost_rounded():
    tracker = CostTracker()
    tracker.record("m", 0.123456789, 100, 50)
    summary = tracker.summary()
    # Should be rounded to 4 decimal places
    assert summary["total_cost_usd"] == round(0.123456789, 4)


def test_empty_tracker_has_zero_cost():
    tracker = CostTracker()
    summary = tracker.summary()
    assert summary["total_cost_usd"] == 0.0
    assert summary["by_model"] == {}
