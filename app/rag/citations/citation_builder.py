from app.rag.retrieval.retrieval_models import RetrievedChunk


class CitationBuilder:
    def build_citations(self, chunks: list[RetrievedChunk]) -> list[dict]:
        citations: list[dict] = []

        for chunk in chunks:
            citations.append(
                {
                    "chunk_id": chunk.chunk_id,
                    "document_id": chunk.document_id,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                    "score": chunk.score,
                    "preview": self._preview(chunk.content),
                }
            )

        return citations

    def _preview(self, text: str, max_chars: int = 240) -> str:
        cleaned = " ".join(text.split())

        if len(cleaned) <= max_chars:
            return cleaned

        return cleaned[:max_chars] + "..."