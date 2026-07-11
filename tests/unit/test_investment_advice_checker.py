from app.guardrails.output.investment_advice_checker import InvestmentAdviceChecker


def test_investment_advice_checker_blocks_direct_advice() -> None:
    checker = InvestmentAdviceChecker()

    result = checker.check("You should buy this stock because it will go up.")

    assert result.passed is False
    assert result.severity == "critical"


def test_investment_advice_checker_allows_summary() -> None:
    checker = InvestmentAdviceChecker()

    result = checker.check("The document reports revenue growth and higher expenses.")

    assert result.passed is True