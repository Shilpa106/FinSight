from app.db.models.document_chunk import DocumentChunk
from app.rag.vectorstores.vectorstore_client import VectorStoreClient
from app.services.ingestion.embedding_service import EmbeddingService


class IndexingService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vectorstore_client: VectorStoreClient,
    ) -> None:
        self.embedding_service = embedding_service
        self.vectorstore_client = vectorstore_client

    def index_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> list[tuple[DocumentChunk, str]]:
        if not chunks:
            return []

        self.vectorstore_client.ensure_collection()

        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedding_service.generate_embeddings(texts)

        vectors: list[dict] = []
        indexed_chunks: list[tuple[DocumentChunk, str]] = []

        for chunk, embedding in zip(chunks, embeddings, strict=True):
            vector_id = str(chunk.id)

            vectors.append(
                {
                    "id": vector_id,
                    "embedding": embedding,
                    "payload": {
                        "chunk_id": str(chunk.id),
                        "document_id": str(chunk.document_id),
                        "organization_id": str(chunk.organization_id),
                        "chunk_index": chunk.chunk_index,
                        "page_number": chunk.page_number,
                        "content": chunk.content,
                        "token_count": chunk.token_count,
                    },
                }
            )

            indexed_chunks.append((chunk, vector_id))

        self.vectorstore_client.upsert_vectors(vectors)

        return indexed_chunks