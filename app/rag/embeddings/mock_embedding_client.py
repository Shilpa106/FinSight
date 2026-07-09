import hashlib
import random


class MockEmbeddingClient:
    def __init__(self, embedding_dimension: int) -> None:
        self.embedding_dimension = embedding_dimension

    def embed_text(self, text: str) -> list[float]:
        return self._deterministic_vector(text)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]

    def dimension(self) -> int:
        return self.embedding_dimension

    def _deterministic_vector(self, text: str) -> list[float]:
        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        seed = int(text_hash[:16], 16)

        rng = random.Random(seed)

        return [rng.uniform(-1.0, 1.0) for _ in range(self.embedding_dimension)]