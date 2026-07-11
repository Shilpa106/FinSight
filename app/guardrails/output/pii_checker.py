import re

from app.schemas.guardrails import GuardrailCheckResult


class PIIChecker:
    def check(self, answer: str) -> GuardrailCheckResult:
        findings: list[str] = []

        if re.search(r"\b\d{3}-\d{2}-\d{4}\b", answer):
            findings.append("possible_ssn")

        if re.search(r"\b\d{12,19}\b", answer):
            findings.append("possible_card_or_account_number")

        if re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", answer):
            findings.append("email_address")

        if findings:
            return GuardrailCheckResult(
                name="pii_detection",
                passed=False,
                severity="high",
                message="Potential sensitive personal data detected in answer.",
                metadata={
                    "findings": findings,
                },
            )

        return GuardrailCheckResult(
            name="pii_detection",
            passed=True,
            severity="low",
            message="No obvious PII detected in answer.",
            metadata=None,
        )