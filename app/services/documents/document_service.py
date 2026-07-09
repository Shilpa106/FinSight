from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.document import Document
from app.db.repositories.document_repository import DocumentRepository


class DocumentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.document_repository = DocumentRepository(db)

    def get_document(self, document_id: UUID) -> Document | None:
        return self.document_repository.get_by_id(document_id)

    def list_documents(self, organization_id: UUID) -> list[Document]:
        return self.document_repository.list_by_organization(organization_id)

    def update_status(
        self,
        document_id: UUID,
        status: str,
        failure_reason: str | None = None,
    ) -> Document | None:
        return self.document_repository.update_status(
            document_id=document_id,
            status=status,
            failure_reason=failure_reason,
        )