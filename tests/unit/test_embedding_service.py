from app.rag.embeddings.mock_embedding_client import MockEmbeddingClient
from app.services.ingestion.embedding_service import EmbeddingService


def test_embedding_service_generates_embeddings() -> None:
    client = MockEmbeddingClient(embedding_dimension=8)
    service = EmbeddingService(embedding_client=client)

    embeddings = service.generate_embeddings(["text one", "text two"])

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 8
    assert len(embeddings[1]) == 8