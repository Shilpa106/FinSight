class TextChunker:
    def __init__(
        self,
        chunk_size: int,
        chunk_overlap: int,
        min_chunk_size: int,
    ) -> None:
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size

    def split_text(self, text: str) -> list[str]:
        text = text.strip()

        if not text:
            return []

        if len(text) <= self.chunk_size:
            return [text]

        chunks: list[str] = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end].strip()

            if len(chunk) >= self.min_chunk_size:
                chunks.append(chunk)

            if end >= len(text):
                break

            start = end - self.chunk_overlap

        return chunks