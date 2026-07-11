from app.evals.metrics.answer_metrics import AnswerMetrics


def test_answer_metrics_matches_keywords() -> None:
    metric = AnswerMetrics()

    score, metadata = metric.score(
        actual_answer="Revenue increased and risk declined.",
        expected_keywords=["revenue", "risk"],
    )

    assert score == 1.0
    assert metadata["matched_keywords"] == ["revenue", "risk"]


def test_answer_metrics_partial_match() -> None:
    metric = AnswerMetrics()

    score, metadata = metric.score(
        actual_answer="Revenue increased.",
        expected_keywords=["revenue", "risk"],
    )

    assert score == 0.5
    assert metadata["matched_keywords"] == ["revenue"]