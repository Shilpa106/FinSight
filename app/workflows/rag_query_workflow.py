from uuid import UUID

from sqlalchemy.orm import Session

from app.llm.llm_client import LLMClient
from app.rag.embeddings.embedding_client import EmbeddingClient
from app.rag.vectorstores.vectorstore_client import VectorStoreClient
from app.services.rag.rag_service import RAGService


class RAGQueryWorkflow:
    def __init__(
        self,
        db: Session,
        embedding_client: EmbeddingClient,
        vectorstore_client: VectorStoreClient,
        llm_client: LLMClient,
    ) -> None:
        self.rag_service = RAGService(
            db=db,
            embedding_client=embedding_client,
            vectorstore_client=vectorstore_client,
            llm_client=llm_client,
        )

    def run(
        self,
        organization_id: UUID,
        user_id: UUID,
        document_id: UUID,
        question: str,
        session_id: UUID | None = None,
    ) -> dict:
        return self.rag_service.answer_question(
            organization_id=organization_id,
            user_id=user_id,
            document_id=document_id,
            question=question,
            session_id=session_id,
        )