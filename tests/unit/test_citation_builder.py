from app.rag.citations.citation_builder import CitationBuilder
from app.rag.retrieval.retrieval_models import RetrievedChunk


def test_citation_builder_builds_citations() -> None:
    builder = CitationBuilder()

    chunks = [
        RetrievedChunk(
            chunk_id="chunk-1",
            document_id="doc-1",
            organization_id="org-1",
            chunk_index=0,
            content="Revenue increased significantly in 2024.",
            page_number=2,
            token_count=10,
            score=0.87,
        )
    ]

    citations = builder.build_citations(chunks)

    assert len(citations) == 1
    assert citations[0]["chunk_id"] == "chunk-1"
    assert citations[0]["page_number"] == 2
    assert citations[0]["score"] == 0.87