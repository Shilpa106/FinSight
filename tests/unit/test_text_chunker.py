from app.rag.chunking.text_chunker import TextChunker


def test_text_chunker_splits_text() -> None:
    chunker = TextChunker(
        chunk_size=10,
        chunk_overlap=2,
        min_chunk_size=3,
    )

    chunks = chunker.split_text("abcdefghijklmnopqrstuvwxyz")

    assert len(chunks) > 1
    assert chunks[0] == "abcdefghij"
    assert chunks[1].startswith("ij")


def test_text_chunker_returns_single_chunk_for_short_text() -> None:
    chunker = TextChunker(
        chunk_size=100,
        chunk_overlap=10,
        min_chunk_size=3,
    )

    chunks = chunker.split_text("short text")

    assert chunks == ["short text"]