from app.core.config import settings
from app.rag.embeddings.embedding_client import EmbeddingClient


class EmbeddingService:
    def __init__(self, embedding_client: EmbeddingClient) -> None:
        self.embedding_client = embedding_client

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        embeddings: list[list[float]] = []

        batch_size = settings.EMBEDDING_BATCH_SIZE

        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            batch_embeddings = self.embedding_client.embed_texts(batch)
            embeddings.extend(batch_embeddings)

        return embeddings