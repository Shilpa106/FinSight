from app.schemas.guardrails import GuardrailCheckResult


class PromptInjectionDetector:
    def __init__(self) -> None:
        self.blocked_patterns = [
            "ignore previous instructions",
            "ignore all previous instructions",
            "disregard previous instructions",
            "forget your instructions",
            "reveal your system prompt",
            "show me your system prompt",
            "developer message",
            "system message",
            "bypass",
            "jailbreak",
            "do anything now",
            "act as dan",
            "override policy",
        ]

    def check(self, text: str) -> GuardrailCheckResult:
        normalized_text = text.lower()

        matched_patterns = [
            pattern
            for pattern in self.blocked_patterns
            if pattern in normalized_text
        ]

        if matched_patterns:
            return GuardrailCheckResult(
                name="prompt_injection",
                passed=False,
                severity="high",
                message="Potential prompt injection detected.",
                metadata={
                    "matched_patterns": matched_patterns,
                },
            )

        return GuardrailCheckResult(
            name="prompt_injection",
            passed=True,
            severity="low",
            message="No prompt injection pattern detected.",
            metadata=None,
        )