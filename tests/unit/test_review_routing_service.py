from app.enums.review_reason import ReviewReason
from app.services.reviews.reviews_routing_service import ReviewRoutingService


def test_review_routing_for_block_action() -> None:
    service = ReviewRoutingService.__new__(ReviewRoutingService)

    reason = service._determine_review_reason(
        guardrail_action="block",
        guardrail_checks=[],
        retrieved_chunk_count=0,
    )

    assert reason == ReviewReason.GUARDRAIL_BLOCKED.value


def test_review_routing_for_warn_action() -> None:
    service = ReviewRoutingService.__new__(ReviewRoutingService)

    reason = service._determine_review_reason(
        guardrail_action="warn",
        guardrail_checks=[],
        retrieved_chunk_count=2,
    )

    assert reason == ReviewReason.GUARDRAIL_WARNING.value


def test_review_routing_for_allow_action() -> None:
    service = ReviewRoutingService.__new__(ReviewRoutingService)

    reason = service._determine_review_reason(
        guardrail_action="allow",
        guardrail_checks=[],
        retrieved_chunk_count=2,
    )

    assert reason is None


def test_review_routing_for_low_groundedness() -> None:
    service = ReviewRoutingService.__new__(ReviewRoutingService)

    reason = service._determine_review_reason(
        guardrail_action="allow",
        retrieved_chunk_count=2,
        guardrail_checks=[
            {
                "name": "groundedness",
                "severity": "medium",
                "passed": True,
            }
        ],
    )

    assert reason == ReviewReason.LOW_GROUNDEDNESS.value