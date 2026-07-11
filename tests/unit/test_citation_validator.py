from app.guardrails.output.citation_validator import CitationValidator


def test_citation_validator_fails_without_citations() -> None:
    validator = CitationValidator()

    result = validator.check(
        answer="Revenue increased.",
        citations=[],
        retrieved_chunk_count=2,
    )

    assert result.passed is False
    assert result.severity == "high"


def test_citation_validator_passes_with_valid_citations() -> None:
    validator = CitationValidator()

    result = validator.check(
        answer="Revenue increased.",
        citations=[
            {
                "chunk_id": "chunk-1",
                "document_id": "doc-1",
                "page_number": 1,
            }
        ],
        retrieved_chunk_count=1,
    )

    assert result.passed is True