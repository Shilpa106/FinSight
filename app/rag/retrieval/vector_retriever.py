from app.rag.retrieval.retrieval_models import RetrievedChunk, RetrievalResult
from app.rag.vectorstores.vectorstore_client import VectorStoreClient


class VectorRetriever:
    def __init__(
        self,
        vectorstore_client: VectorStoreClient,
    ) -> None:
        self.vectorstore_client = vectorstore_client

    def retrieve(
        self,
        query_vector: list[float],
        organization_id: str,
        document_id: str,
        top_k: int,
        min_score: float,
    ) -> RetrievalResult:
        raw_results = self.vectorstore_client.search(
            query_vector=query_vector,
            organization_id=organization_id,
            document_id=document_id,
            top_k=top_k,
            min_score=min_score,
        )

        chunks: list[RetrievedChunk] = []

        for item in raw_results:
            payload = item["payload"]

            chunks.append(
                RetrievedChunk(
                    chunk_id=payload.get("chunk_id", item["id"]),
                    document_id=payload.get("document_id", document_id),
                    organization_id=payload.get("organization_id", organization_id),
                    chunk_index=payload.get("chunk_index", 0),
                    content=payload.get("content", ""),
                    page_number=payload.get("page_number"),
                    token_count=payload.get("token_count"),
                    score=item.get("score"),
                )
            )

        return RetrievalResult(
            chunks=chunks,
            total=len(chunks),
        )