from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.human_review import HumanReview
from app.db.repositories.human_review_repository import HumanReviewRepository
from app.enums.review_status import ReviewStatus
from app.services.audit.audit_service import AuditService


class ReviewService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = HumanReviewRepository(db)
        self.audit_service = AuditService(db)

    def create_review_item(
        self,
        organization_id: UUID,
        document_id: UUID,
        reason: str,
        question: str,
        original_answer: str | None,
        session_id: UUID | None = None,
        assistant_message_id: UUID | None = None,
        workflow_run_id: UUID | None = None,
        citations: list | None = None,
        guardrail_metadata: dict | None = None,
        review_metadata: dict | None = None,
    ) -> HumanReview:
        review = HumanReview(
            organization_id=organization_id,
            document_id=document_id,
            session_id=session_id,
            assistant_message_id=assistant_message_id,
            workflow_run_id=workflow_run_id,
            status=ReviewStatus.PENDING.value,
            reason=reason,
            question=question,
            original_answer=original_answer,
            final_answer=None,
            citations=citations,
            guardrail_metadata=guardrail_metadata,
            review_metadata=review_metadata,
        )

        created_review = self.repository.create(review)

        self.audit_service.log_event(
            organization_id=organization_id,
            user_id=None,
            action="human_review.created",
            resource_type="human_review",
            resource_id=str(created_review.id),
            metadata={
                "document_id": str(document_id),
                "reason": reason,
                "workflow_run_id": str(workflow_run_id) if workflow_run_id else None,
            },
        )

        return created_review

    def get_review(
        self,
        review_id: UUID,
        organization_id: UUID,
    ) -> HumanReview:
        review = self.repository.get_by_id(review_id)

        if review is None:
            raise ValueError("Review item not found.")

        if review.organization_id != organization_id:
            raise PermissionError("Access denied.")

        return review

    def list_pending_reviews(
        self,
        organization_id: UUID,
        limit: int = 50,
    ) -> list[HumanReview]:
        return self.repository.list_pending(
            organization_id=organization_id,
            limit=limit,
        )

    def list_reviews_by_document(
        self,
        document_id: UUID,
        organization_id: UUID,
    ) -> list[HumanReview]:
        return self.repository.list_by_document(
            document_id=document_id,
            organization_id=organization_id,
        )

    def approve_review(
        self,
        review_id: UUID,
        organization_id: UUID,
        reviewer_id: UUID,
        reviewer_notes: str | None = None,
    ) -> HumanReview:
        review = self.get_review(review_id, organization_id)

        self._ensure_pending(review)

        review.status = ReviewStatus.APPROVED.value
        review.final_answer = review.original_answer
        review.reviewer_id = reviewer_id
        review.reviewer_notes = reviewer_notes
        review.reviewed_at = datetime.utcnow()

        self.db.flush()
        self.db.refresh(review)

        self.audit_service.log_event(
            organization_id=organization_id,
            user_id=reviewer_id,
            action="human_review.approved",
            resource_type="human_review",
            resource_id=str(review.id),
            metadata={
                "document_id": str(review.document_id),
                "session_id": str(review.session_id) if review.session_id else None,
            },
        )

        return review

    def reject_review(
        self,
        review_id: UUID,
        organization_id: UUID,
        reviewer_id: UUID,
        reviewer_notes: str | None = None,
    ) -> HumanReview:
        review = self.get_review(review_id, organization_id)

        self._ensure_pending(review)

        review.status = ReviewStatus.REJECTED.value
        review.final_answer = None
        review.reviewer_id = reviewer_id
        review.reviewer_notes = reviewer_notes
        review.reviewed_at = datetime.utcnow()

        self.db.flush()
        self.db.refresh(review)

        self.audit_service.log_event(
            organization_id=organization_id,
            user_id=reviewer_id,
            action="human_review.rejected",
            resource_type="human_review",
            resource_id=str(review.id),
            metadata={
                "document_id": str(review.document_id),
                "session_id": str(review.session_id) if review.session_id else None,
                "reviewer_notes": reviewer_notes,
            },
        )

        return review

    def edit_and_approve_review(
        self,
        review_id: UUID,
        organization_id: UUID,
        reviewer_id: UUID,
        final_answer: str,
        reviewer_notes: str | None = None,
    ) -> HumanReview:
        review = self.get_review(review_id, organization_id)

        self._ensure_pending(review)

        review.status = ReviewStatus.EDITED_APPROVED.value
        review.final_answer = final_answer
        review.reviewer_id = reviewer_id
        review.reviewer_notes = reviewer_notes
        review.reviewed_at = datetime.utcnow()

        self.db.flush()
        self.db.refresh(review)

        self.audit_service.log_event(
            organization_id=organization_id,
            user_id=reviewer_id,
            action="human_review.edited_approved",
            resource_type="human_review",
            resource_id=str(review.id),
            metadata={
                "document_id": str(review.document_id),
                "session_id": str(review.session_id) if review.session_id else None,
                "reviewer_notes": reviewer_notes,
            },
        )

        return review

    def _ensure_pending(self, review: HumanReview) -> None:
        if review.status != ReviewStatus.PENDING.value:
            raise ValueError(
                f"Review item is not pending. Current status: {review.status}"
            )