from openai import OpenAI


class OpenAIEmbeddingClient:
    def __init__(
        self,
        api_key: str,
        model: str,
        embedding_dimension: int,
    ) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.embedding_dimension = embedding_dimension

    def embed_text(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return [item.embedding for item in response.data]

    def dimension(self) -> int:
        return self.embedding_dimension