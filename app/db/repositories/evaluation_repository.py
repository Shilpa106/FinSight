from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.evaluation import Evaluation
from app.db.repositories.base_repository import BaseRepository


class EvaluationRepository(BaseRepository[Evaluation]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Evaluation)

    def list_by_document(
        self,
        document_id: UUID,
        organization_id: UUID,
    ) -> list[Evaluation]:
        return (
            self.db.query(Evaluation)
            .filter(
                Evaluation.document_id == document_id,
                Evaluation.organization_id == organization_id,
            )
            .order_by(Evaluation.created_at.desc())
            .all()
        )

    def list_by_run_name(
        self,
        run_name: str,
        organization_id: UUID,
    ) -> list[Evaluation]:
        return (
            self.db.query(Evaluation)
            .filter(
                Evaluation.run_name == run_name,
                Evaluation.organization_id == organization_id,
            )
            .order_by(Evaluation.created_at.asc())
            .all()
        )