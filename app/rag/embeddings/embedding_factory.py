from app.core.config import settings
from app.rag.embeddings.embedding_client import EmbeddingClient
from app.rag.embeddings.mock_embedding_client import MockEmbeddingClient
from app.rag.embeddings.openai_embedding_client import OpenAIEmbeddingClient


def get_embedding_client() -> EmbeddingClient:
    if settings.EMBEDDING_PROVIDER == "mock":
        return MockEmbeddingClient(
            embedding_dimension=settings.EMBEDDING_DIMENSION,
        )

    if settings.EMBEDDING_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI embeddings.")

        return OpenAIEmbeddingClient(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_EMBEDDING_MODEL,
            embedding_dimension=settings.EMBEDDING_DIMENSION,
        )

    raise ValueError(f"Unsupported embedding provider: {settings.EMBEDDING_PROVIDER}")