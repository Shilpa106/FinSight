from app.evals.metrics.citation_metrics import CitationMetrics


def test_citation_metrics_valid_citations() -> None:
    metric = CitationMetrics()

    score, metadata = metric.score(
        citations=[
            {
                "chunk_id": "chunk-1",
                "document_id": "doc-1",
            }
        ],
        retrieved_chunk_count=1,
    )

    assert score == 1.0
    assert metadata["valid_citation_count"] == 1


def test_citation_metrics_no_citations() -> None:
    metric = CitationMetrics()

    score, metadata = metric.score(
        citations=[],
        retrieved_chunk_count=1,
    )

    assert score == 0.0
    assert metadata["citation_count"] == 0