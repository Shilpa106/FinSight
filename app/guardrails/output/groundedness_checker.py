import re

from app.rag.retrieval.retrieval_models import RetrievedChunk
from app.schemas.guardrails import GuardrailCheckResult


class GroundednessChecker:
    def check(
        self,
        answer: str,
        retrieved_chunks: list[RetrievedChunk],
    ) -> GuardrailCheckResult:
        if not retrieved_chunks:
            return GuardrailCheckResult(
                name="groundedness",
                passed=False,
                severity="high",
                message="No retrieved context available to ground the answer.",
                metadata=None,
            )

        answer_terms = self._important_terms(answer)

        context_text = " ".join(chunk.content for chunk in retrieved_chunks).lower()
        supported_terms = [
            term for term in answer_terms if term.lower() in context_text
        ]

        if not answer_terms:
            return GuardrailCheckResult(
                name="groundedness",
                passed=True,
                severity="low",
                message="Answer is too short for detailed groundedness analysis.",
                metadata={
                    "support_ratio": 1.0,
                },
            )

        support_ratio = len(supported_terms) / len(answer_terms)

        if support_ratio < 0.35:
            return GuardrailCheckResult(
                name="groundedness",
                passed=False,
                severity="high",
                message="Answer appears weakly grounded in retrieved context.",
                metadata={
                    "support_ratio": support_ratio,
                    "answer_term_count": len(answer_terms),
                    "supported_term_count": len(supported_terms),
                },
            )

        if support_ratio < 0.55:
            return GuardrailCheckResult(
                name="groundedness",
                passed=True,
                severity="medium",
                message="Answer is partially grounded, but should be reviewed.",
                metadata={
                    "support_ratio": support_ratio,
                    "answer_term_count": len(answer_terms),
                    "supported_term_count": len(supported_terms),
                },
            )

        return GuardrailCheckResult(
            name="groundedness",
            passed=True,
            severity="low",
            message="Answer appears grounded in retrieved context.",
            metadata={
                "support_ratio": support_ratio,
                "answer_term_count": len(answer_terms),
                "supported_term_count": len(supported_terms),
            },
        )

    def _important_terms(self, text: str) -> list[str]:
        words = re.findall(r"[A-Za-z][A-Za-z0-9\-]{3,}", text.lower())

        stop_words = {
            "this",
            "that",
            "with",
            "from",
            "there",
            "their",
            "about",
            "document",
            "context",
            "based",
            "retrieved",
            "question",
            "answer",
            "information",
            "could",
            "would",
            "should",
        }

        terms = []

        for word in words:
            if word not in stop_words and word not in terms:
                terms.append(word)

        return terms[:50]