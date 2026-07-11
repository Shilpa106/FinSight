from app.schemas.guardrails import GuardrailCheckResult


class CitationValidator:
    def check(
        self,
        answer: str,
        citations: list[dict],
        retrieved_chunk_count: int,
    ) -> GuardrailCheckResult:
        if retrieved_chunk_count == 0:
            return GuardrailCheckResult(
                name="citation_validation",
                passed=False,
                severity="high",
                message="No retrieved chunks were available for citation.",
                metadata={
                    "citation_count": len(citations),
                    "retrieved_chunk_count": retrieved_chunk_count,
                },
            )

        if not citations:
            return GuardrailCheckResult(
                name="citation_validation",
                passed=False,
                severity="high",
                message="Answer has no citations.",
                metadata={
                    "citation_count": 0,
                    "retrieved_chunk_count": retrieved_chunk_count,
                },
            )

        valid_citations = [
            citation
            for citation in citations
            if citation.get("chunk_id") and citation.get("document_id")
        ]

        if not valid_citations:
            return GuardrailCheckResult(
                name="citation_validation",
                passed=False,
                severity="high",
                message="Citations are missing required chunk or document references.",
                metadata={
                    "citation_count": len(citations),
                    "valid_citation_count": 0,
                },
            )

        return GuardrailCheckResult(
            name="citation_validation",
            passed=True,
            severity="low",
            message="Citations are present and structurally valid.",
            metadata={
                "citation_count": len(citations),
                "valid_citation_count": len(valid_citations),
            },
        )