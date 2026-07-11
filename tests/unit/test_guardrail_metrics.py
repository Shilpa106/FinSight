from app.evals.metrics.guardrail_metrics import GuardrailMetrics


def test_guardrail_metric_passes_expected_action() -> None:
    metric = GuardrailMetrics()

    score, metadata = metric.score(
        should_trigger_guardrail=True,
        expected_guardrail_action="block",
        actual_guardrail_action="block",
    )

    assert score == 1.0
    assert metadata["passed"] is True


def test_guardrail_metric_fails_wrong_action() -> None:
    metric = GuardrailMetrics()

    score, metadata = metric.score(
        should_trigger_guardrail=True,
        expected_guardrail_action="block",
        actual_guardrail_action="allow",
    )

    assert score == 0.0
    assert metadata["passed"] is False