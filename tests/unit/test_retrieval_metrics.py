from app.evals.metrics.retrieval_metrics import RetrievalMetrics


def test_retrieval_metric_matches_expected_pages() -> None:
    metric = RetrievalMetrics()

    score, metadata = metric.score(
        retrieved_chunk_count=2,
        citations=[
            {
                "page_number": 1,
            },
            {
                "page_number": 2,
            },
        ],
        expected_pages=[1],
    )

    assert score == 1.0
    assert metadata["matched_expected_pages"] == [1]


def test_retrieval_metric_no_retrieved_chunks() -> None:
    metric = RetrievalMetrics()

    score, metadata = metric.score(
        retrieved_chunk_count=0,
        citations=[],
        expected_pages=[1],
    )

    assert score == 0.0