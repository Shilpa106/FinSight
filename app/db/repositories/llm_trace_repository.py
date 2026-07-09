from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.llm_trace import LLMTrace
from app.db.repositories.base_repository import BaseRepository


class LLMTraceRepository(BaseRepository[LLMTrace]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, LLMTrace)

    def list_by_document(self, document_id: UUID) -> list[LLMTrace]:
        return (
            self.db.query(LLMTrace)
            .filter(LLMTrace.document_id == document_id)
            .order_by(LLMTrace.created_at.desc())
            .all()
        )

    def list_by_workflow_run(self, workflow_run_id: UUID) -> list[LLMTrace]:
        return (
            self.db.query(LLMTrace)
            .filter(LLMTrace.workflow_run_id == workflow_run_id)
            .order_by(LLMTrace.created_at.desc())
            .all()
        )