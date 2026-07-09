from app.core.config import settings
from app.rag.chunking.chunk_models import ChunkingResult
from app.rag.chunking.page_aware_chunker import PageAwareChunker


class ChunkingService:
    def __init__(self) -> None:
        self.chunker = PageAwareChunker(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            min_chunk_size=settings.MIN_CHUNK_SIZE,
        )

    def chunk_text(self, full_text: str) -> ChunkingResult:
        return self.chunker.chunk_document(full_text)