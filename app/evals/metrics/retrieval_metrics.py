class RetrievalMetrics:
    def score(
        self,
        retrieved_chunk_count: int,
        citations: list[dict],
        expected_pages: list[int],
    ) -> tuple[float, dict]:
        if retrieved_chunk_count == 0:
            return 0.0, {
                "retrieved_chunk_count": 0,
                "expected_pages": expected_pages,
                "matched_expected_pages": [],
            }

        if not expected_pages:
            return 1.0, {
                "retrieved_chunk_count": retrieved_chunk_count,
                "expected_pages": [],
                "matched_expected_pages": [],
                "note": "No expected pages provided.",
            }

        cited_pages = {
            citation.get("page_number")
            for citation in citations
            if citation.get("page_number") is not None
        }

        expected_page_set = set(expected_pages)
        matched_pages = expected_page_set.intersection(cited_pages)

        score = len(matched_pages) / len(expected_page_set)

        return score, {
            "retrieved_chunk_count": retrieved_chunk_count,
            "expected_pages": expected_pages,
            "cited_pages": sorted(cited_pages),
            "matched_expected_pages": sorted(matched_pages),
        }