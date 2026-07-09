import re

from app.rag.chunking.chunk_models import ChunkingResult, TextChunk
from app.rag.chunking.text_chunker import TextChunker

"""
Implemented chunks page-aware so later RAG answers can provide page-level citations.
"""
class PageAwareChunker:
    PAGE_PATTERN = re.compile(r"--- Page (\d+) ---")

    def __init__(
        self,
        chunk_size: int,
        chunk_overlap: int,
        min_chunk_size: int,
    ) -> None:
        self.text_chunker = TextChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            min_chunk_size=min_chunk_size,
        )

    def chunk_document(self, full_text: str) -> ChunkingResult:
        pages = self._split_by_page(full_text)

        chunks: list[TextChunk] = []
        chunk_index = 0
        total_tokens = 0

        for page_number, page_text in pages:
            raw_chunks = self.text_chunker.split_text(page_text)

            for raw_chunk in raw_chunks:
                token_count = self._estimate_tokens(raw_chunk)
                total_tokens += token_count

                chunks.append(
                    TextChunk(
                        chunk_index=chunk_index,
                        content=raw_chunk,
                        page_number=page_number,
                        token_count=token_count,
                        metadata={
                            "page_number": page_number,
                            "chunking_strategy": "page_aware_character_chunking",
                        },
                    )
                )

                chunk_index += 1

        return ChunkingResult(
            chunks=chunks,
            total_chunks=len(chunks),
            total_tokens=total_tokens,
        )

    def _split_by_page(self, full_text: str) -> list[tuple[int | None, str]]:
        matches = list(self.PAGE_PATTERN.finditer(full_text))

        if not matches:
            return [(None, full_text.strip())]

        pages: list[tuple[int | None, str]] = []

        for index, match in enumerate(matches):
            page_number = int(match.group(1))
            start = match.end()

            if index + 1 < len(matches):
                end = matches[index + 1].start()
            else:
                end = len(full_text)

            page_text = full_text[start:end].strip()

            if page_text:
                pages.append((page_number, page_text))

        return pages

    def _estimate_tokens(self, text: str) -> int:
        # Approximation: 1 token ≈ 4 characters for English text.
        return max(1, len(text) // 4)