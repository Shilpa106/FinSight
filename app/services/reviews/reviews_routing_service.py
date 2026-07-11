from uuid import UUID

from sqlalchemy.orm import Session

from app.enums.review_reason import ReviewReason
from app.services.reviews.reviews_service import ReviewService


class ReviewRoutingService:
    def __init__(self, db: Session) -> None:
        self.review_service = ReviewService(db)

    def route_rag_result_if_needed(
        self,
        organization_id: UUID,
        document_id: UUID,
        question: str,
        answer: str | None,
        guardrail_action: str | None,
        guardrail_reason: str | None,
        guardrail_checks: list[dict] | None,
        session_id: UUID | None = None,
        assistant_message_id: UUID | None = None,
        workflow_run_id: UUID | None = None,
        citations: list | None = None,
        retrieved_chunk_count: int | None = None,
    ):
        reason = self._determine_review_reason(
            guardrail_action=guardrail_action,
            guardrail_checks=guardrail_checks,
            retrieved_chunk_count=retrieved_chunk_count,
        )

        if reason is None:
            return None

        return self.review_service.create_review_item(
            organization_id=organization_id,
            document_id=document_id,
            session_id=session_id,
            assistant_message_id=assistant_message_id,
            workflow_run_id=workflow_run_id,
            reason=reason,
            question=question,
            original_answer=answer,
            citations=citations,
            guardrail_metadata={
                "guardrail_action": guardrail_action,
                "guardrail_reason": guardrail_reason,
                "guardrail_checks": guardrail_checks,
            },
            review_metadata={
                "retrieved_chunk_count": retrieved_chunk_count,
            },
        )

    def _determine_review_reason(
        self,
        guardrail_action: str | None,
        guardrail_checks: list[dict] | None,
        retrieved_chunk_count: int | None,
    ) -> str | None:
        if guardrail_action in {"fallback", "block"}:
            return ReviewReason.GUARDRAIL_BLOCKED.value

        if guardrail_action == "warn":
            return ReviewReason.GUARDRAIL_WARNING.value

        if retrieved_chunk_count == 0:
            return ReviewReason.MISSING_CITATIONS.value

        checks = guardrail_checks or []

        for check in checks:
            name = check.get("name")
            severity = check.get("severity")
            passed = check.get("passed")

            if name == "groundedness" and severity in {"medium", "high"}:
                return ReviewReason.LOW_GROUNDEDNESS.value

            if name == "citation_validation" and not passed:
                return ReviewReason.MISSING_CITATIONS.value

            if name == "investment_advice" and severity in {"medium", "critical"}:
                return ReviewReason.INVESTMENT_ADVICE_RISK.value

            if name == "pii_detection" and not passed:
                return ReviewReason.PII_RISK.value

        return None