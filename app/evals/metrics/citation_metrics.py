class CitationMetrics:
    def score(
        self,
        citations: list[dict],
        retrieved_chunk_count: int,
    ) -> tuple[float, dict]:
        if retrieved_chunk_count == 0:
            return 0.0, {
                "citation_count": len(citations),
                "retrieved_chunk_count": retrieved_chunk_count,
            }

        if not citations:
            return 0.0, {
                "citation_count": 0,
                "retrieved_chunk_count": retrieved_chunk_count,
            }

        valid_citations = [
            citation
            for citation in citations
            if citation.get("chunk_id") and citation.get("document_id")
        ]

        score = len(valid_citations) / len(citations)

        return score, {
            "citation_count": len(citations),
            "valid_citation_count": len(valid_citations),
            "retrieved_chunk_count": retrieved_chunk_count,
        }