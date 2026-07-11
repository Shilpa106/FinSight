from app.guardrails.input.prompt_injection_detector import PromptInjectionDetector
from app.schemas.guardrails import GuardrailCheckResult, GuardrailDecision


class InputGuardrailService:
    def __init__(self) -> None:
        self.prompt_injection_detector = PromptInjectionDetector()

    def validate_question(self, question: str) -> GuardrailDecision:
        checks: list[GuardrailCheckResult] = [
            self.prompt_injection_detector.check(question)
        ]

        failed_checks = [check for check in checks if not check.passed]

        if failed_checks:
            return GuardrailDecision(
                allowed=False,
                action="block",
                reason="Input failed guardrail validation.",
                checks=checks,
                safe_response=(
                    "I cannot process this request because it appears to contain "
                    "instructions intended to bypass system safeguards."
                ),
            )

        return GuardrailDecision(
            allowed=True,
            action="allow",
            reason="Input passed guardrail validation.",
            checks=checks,
            safe_response=None,
        )