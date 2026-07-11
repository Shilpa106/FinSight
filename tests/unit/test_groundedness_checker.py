from app.guardrails.output.groundedness_checker import GroundednessChecker
from app.rag.retrieval.retrieval_models import RetrievedChunk


def test_groundedness_checker_passes_supported_answer() -> None:
    checker = GroundednessChecker()

    chunks = [
        RetrievedChunk(
            chunk_id="chunk-1",
            document_id="doc-1",
            organization_id="org-1",
            chunk_index=0,
            content="Revenue increased from 10 million to 15 million.",
            page_number=1,
            token_count=20,
            score=0.9,
        )
    ]

    result = checker.check(
        answer="Revenue increased from 10 million to 15 million.",
        retrieved_chunks=chunks,
    )

    assert result.passed is True


def test_groundedness_checker_fails_unsupported_answer() -> None:
    checker = GroundednessChecker()

    chunks = [
        RetrievedChunk(
            chunk_id="chunk-1",
            document_id="doc-1",
            organization_id="org-1",
            chunk_index=0,
            content="Revenue increased from 10 million to 15 million.",
            page_number=1,
            token_count=20,
            score=0.9,
        )
    ]

    result = checker.check(
        answer="The company acquired three banks in Germany.",
        retrieved_chunks=chunks,
    )

    assert result.passed is False