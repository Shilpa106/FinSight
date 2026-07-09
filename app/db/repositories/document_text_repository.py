from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.document_text import DocumentText
from app.db.repositories.base_repository import BaseRepository


class DocumentTextRepository(BaseRepository[DocumentText]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, DocumentText)

    def get_by_document_id(self, document_id: UUID) -> DocumentText | None:
        return (
            self.db.query(DocumentText)
            .filter(DocumentText.document_id == document_id)
            .first()
        )

    def upsert_document_text(
        self,
        document_id: UUID,
        organization_id: UUID,
        full_text: str,
        page_count: int,
        character_count: int,
        extraction_metadata: dict | None = None,
    ) -> DocumentText:
        existing_text = self.get_by_document_id(document_id)

        if existing_text is not None:
            existing_text.full_text = full_text
            existing_text.page_count = page_count
            existing_text.character_count = character_count
            existing_text.extraction_metadata = extraction_metadata
            self.db.flush()
            self.db.refresh(existing_text)
            return existing_text

        document_text = DocumentText(
            document_id=document_id,
            organization_id=organization_id,
            full_text=full_text,
            page_count=page_count,
            character_count=character_count,
            extraction_metadata=extraction_metadata,
        )

        return self.create(document_text)