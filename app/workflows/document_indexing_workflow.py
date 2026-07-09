from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.document_chunk import DocumentChunk
from app.rag.embeddings.embedding_client import EmbeddingClient
from app.rag.vectorstores.vectorstore_client import VectorStoreClient
from app.services.documents.document_indexing_service import DocumentIndexingService


class DocumentIndexingWorkflow:
    def __init__(
        self,
        db: Session,
        embedding_client: EmbeddingClient,
        vectorstore_client: VectorStoreClient,
    ) -> None:
        self.indexing_service = DocumentIndexingService(
            db=db,
            embedding_client=embedding_client,
            vectorstore_client=vectorstore_client,
        )

    def run(
        self,
        document_id: UUID,
        organization_id: UUID,
        user_id: UUID | None = None,
    ) -> list[DocumentChunk]:
        return self.indexing_service.index_document(
            document_id=document_id,
            organization_id=organization_id,
            user_id=user_id,
        )