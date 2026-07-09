from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.document_chunk import DocumentChunk
from app.db.repositories.base_repository import BaseRepository


class DocumentChunkRepository(BaseRepository[DocumentChunk]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, DocumentChunk)

    def list_by_document(self, document_id: UUID) -> list[DocumentChunk]:
        return (
            self.db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index.asc())
            .all()
        )

    def bulk_create(self, chunks: list[DocumentChunk]) -> list[DocumentChunk]:
        self.db.add_all(chunks)
        self.db.flush()

        for chunk in chunks:
            self.db.refresh(chunk)

        return chunks