from app.rag.chunking.page_aware_chunker import PageAwareChunker


def test_page_aware_chunker_preserves_page_number() -> None:
    chunker = PageAwareChunker(
        chunk_size=100,
        chunk_overlap=10,
        min_chunk_size=5,
    )

    text = """
--- Page 1 ---
Revenue increased year over year.

--- Page 2 ---
Debt obligations mature in 2028.
"""

    result = chunker.chunk_document(text)

    assert result.total_chunks == 2
    assert result.chunks[0].page_number == 1
    assert result.chunks[1].page_number == 2