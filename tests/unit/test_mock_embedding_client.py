from app.rag.embeddings.mock_embedding_client import MockEmbeddingClient


def test_mock_embedding_client_returns_expected_dimension() -> None:
    client = MockEmbeddingClient(embedding_dimension=8)

    vector = client.embed_text("hello world")

    assert len(vector) == 8


def test_mock_embedding_client_is_deterministic() -> None:
    client = MockEmbeddingClient(embedding_dimension=8)

    vector_1 = client.embed_text("same text")
    vector_2 = client.embed_text("same text")

    assert vector_1 == vector_2