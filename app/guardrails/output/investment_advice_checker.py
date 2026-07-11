from app.schemas.guardrails import GuardrailCheckResult


class InvestmentAdviceChecker:
    def __init__(self) -> None:
        self.high_risk_phrases = [
            "you should buy",
            "you should sell",
            "i recommend buying",
            "i recommend selling",
            "buy this stock",
            "sell this stock",
            "guaranteed return",
            "risk-free return",
            "this is a safe investment",
            "you will make money",
            "definitely invest",
            "strong buy",
            "strong sell",
        ]

        self.medium_risk_phrases = [
            "undervalued",
            "overvalued",
            "price target",
            "upside potential",
            "downside risk",
            "investment recommendation",
        ]

    def check(self, answer: str) -> GuardrailCheckResult:
        normalized_answer = answer.lower()

        high_risk_matches = [
            phrase
            for phrase in self.high_risk_phrases
            if phrase in normalized_answer
        ]

        if high_risk_matches:
            return GuardrailCheckResult(
                name="investment_advice",
                passed=False,
                severity="critical",
                message="Answer appears to provide direct investment advice.",
                metadata={
                    "matched_phrases": high_risk_matches,
                },
            )

        medium_risk_matches = [
            phrase
            for phrase in self.medium_risk_phrases
            if phrase in normalized_answer
        ]

        if medium_risk_matches:
            return GuardrailCheckResult(
                name="investment_advice",
                passed=True,
                severity="medium",
                message="Answer contains investment-sensitive language.",
                metadata={
                    "matched_phrases": medium_risk_matches,
                },
            )

        return GuardrailCheckResult(
            name="investment_advice",
            passed=True,
            severity="low",
            message="No direct investment advice detected.",
            metadata=None,
        )