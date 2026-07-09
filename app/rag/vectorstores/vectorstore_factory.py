from app.core.config import settings
from app.rag.vectorstores.qdrant_client import QdrantVectorStoreClient
from app.rag.vectorstores.vectorstore_client import VectorStoreClient


def get_vectorstore_client() -> VectorStoreClient:
    if settings.VECTOR_DB_PROVIDER == "qdrant":
        return QdrantVectorStoreClient(
            url=settings.QDRANT_URL,
            collection_name=settings.QDRANT_COLLECTION,
            vector_size=settings.EMBEDDING_DIMENSION,
        )

    raise ValueError(f"Unsupported vector DB provider: {settings.VECTOR_DB_PROVIDER}")