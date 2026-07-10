from uuid import UUID

from app.core.config import settings
from app.rag.embeddings.embedding_client import EmbeddingClient
from app.rag.retrieval.retrieval_models import RetrievalResult
from app.rag.retrieval.vector_retriever import VectorRetriever
from app.rag.vectorstores.vectorstore_client import VectorStoreClient


class RetrievalService:
    def __init__(
        self,
        embedding_client: EmbeddingClient,
        vectorstore_client: VectorStoreClient,
    ) -> None:
        self.embedding_client = embedding_client
        self.vector_retriever = VectorRetriever(vectorstore_client)

    def retrieve(
        self,
        question: str,
        organization_id: UUID,
        document_id: UUID,
    ) -> RetrievalResult:
        query_vector = self.embedding_client.embed_text(question)

        return self.vector_retriever.retrieve(
            query_vector=query_vector,
            organization_id=str(organization_id),
            document_id=str(document_id),
            top_k=settings.RAG_TOP_K,
            min_score=settings.RAG_MIN_SCORE,
        )