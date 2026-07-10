from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.retrieval_models import RetrievedChunk


def test_context_builder_includes_source_labels() -> None:
    builder = ContextBuilder()

    chunks = [
        RetrievedChunk(
            chunk_id="chunk-1",
            document_id="doc-1",
            organization_id="org-1",
            chunk_index=0,
            content="Revenue increased.",
            page_number=1,
            token_count=10,
            score=0.9,
        )
    ]

    context = builder.build_context(chunks)

    assert "chunk_id=chunk-1" in context
    assert "page=1" in context
    assert "Revenue increased." in context