from app.core.config import settings
from app.rag.retrieval.retrieval_models import RetrievedChunk


class ContextBuilder:
    def build_context(self, chunks: list[RetrievedChunk]) -> str:
        context_parts: list[str] = []
        current_length = 0

        for chunk in chunks:
            source_label = self._build_source_label(chunk)

            chunk_text = (
                f"{source_label}\n"
                f"{chunk.content.strip()}\n"
            )

            if current_length + len(chunk_text) > settings.RAG_MAX_CONTEXT_CHARS:
                break

            context_parts.append(chunk_text)
            current_length += len(chunk_text)

        return "\n\n".join(context_parts).strip()

    def _build_source_label(self, chunk: RetrievedChunk) -> str:
        if chunk.page_number is not None:
            return (
                f"[Source: chunk_id={chunk.chunk_id}, "
                f"page={chunk.page_number}, "
                f"score={chunk.score}]"
            )

        return (
            f"[Source: chunk_id={chunk.chunk_id}, "
            f"score={chunk.score}]"
        )