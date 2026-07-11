from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.human_review import HumanReview
from app.db.repositories.base_repository import BaseRepository


class HumanReviewRepository(BaseRepository[HumanReview]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, HumanReview)

    def list_pending(
        self,
        organization_id: UUID,
        limit: int = 50,
    ) -> list[HumanReview]:
        return (
            self.db.query(HumanReview)
            .filter(
                HumanReview.organization_id == organization_id,
                HumanReview.status == "pending",
            )
            .order_by(HumanReview.created_at.asc())
            .limit(limit)
            .all()
        )

    def list_by_document(
        self,
        document_id: UUID,
        organization_id: UUID,
    ) -> list[HumanReview]:
        return (
            self.db.query(HumanReview)
            .filter(
                HumanReview.document_id == document_id,
                HumanReview.organization_id == organization_id,
            )
            .order_by(HumanReview.created_at.desc())
            .all()
        )

    def list_by_status(
        self,
        organization_id: UUID,
        status: str,
        limit: int = 50,
    ) -> list[HumanReview]:
        return (
            self.db.query(HumanReview)
            .filter(
                HumanReview.organization_id == organization_id,
                HumanReview.status == status,
            )
            .order_by(HumanReview.created_at.desc())
            .limit(limit)
            .all()
        )