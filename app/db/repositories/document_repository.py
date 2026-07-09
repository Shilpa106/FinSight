from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.document import Document
from app.db.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Document)

    def list_by_organization(self, organization_id: UUID) -> list[Document]:
        return (
            self.db.query(Document)
            .filter(Document.organization_id == organization_id)
            .order_by(Document.created_at.desc())
            .all()
        )

    def update_status(
        self,
        document_id: UUID,
        status: str,
        failure_reason: str | None = None,
    ) -> Document | None:
        document = self.get_by_id(document_id)

        if document is None:
            return None

        document.status = status
        document.failure_reason = failure_reason
        self.db.flush()
        self.db.refresh(document)

        return document