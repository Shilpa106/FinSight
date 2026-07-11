from app.guardrails.output.citation_validator import CitationValidator
from app.guardrails.output.groundedness_checker import GroundednessChecker
from app.guardrails.output.investment_advice_checker import InvestmentAdviceChecker
from app.guardrails.output.pii_checker import PIIChecker
from app.rag.retrieval.retrieval_models import RetrievedChunk
from app.schemas.guardrails import GuardrailCheckResult, GuardrailDecision


class OutputGuardrailService:
    def __init__(self) -> None:
        self.citation_validator = CitationValidator()
        self.groundedness_checker = GroundednessChecker()
        self.investment_advice_checker = InvestmentAdviceChecker()
        self.pii_checker = PIIChecker()

    def validate_answer(
        self,
        answer: str,
        citations: list[dict],
        retrieved_chunks: list[RetrievedChunk],
    ) -> GuardrailDecision:
        checks: list[GuardrailCheckResult] = [
            self.citation_validator.check(
                answer=answer,
                citations=citations,
                retrieved_chunk_count=len(retrieved_chunks),
            ),
            self.groundedness_checker.check(
                answer=answer,
                retrieved_chunks=retrieved_chunks,
            ),
            self.investment_advice_checker.check(answer),
            self.pii_checker.check(answer),
        ]

        blocking_checks = [
            check
            for check in checks
            if not check.passed and check.severity in {"high", "critical"}
        ]

        if blocking_checks:
            return GuardrailDecision(
                allowed=False,
                action="fallback",
                reason="Output failed guardrail validation.",
                checks=checks,
                safe_response=(
                    "I could not produce a sufficiently grounded answer from the "
                    "retrieved document context. Please rephrase your question or "
                    "review the cited document sections manually."
                ),
            )

        warning_checks = [
            check
            for check in checks
            if check.severity == "medium"
        ]

        if warning_checks:
            return GuardrailDecision(
                allowed=True,
                action="warn",
                reason="Output passed with warnings.",
                checks=checks,
                safe_response=None,
            )

        return GuardrailDecision(
            allowed=True,
            action="allow",
            reason="Output passed guardrail validation.",
            checks=checks,
            safe_response=None,
        )