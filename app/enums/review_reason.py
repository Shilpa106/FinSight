from enum import Enum


class ReviewReason(str, Enum):
    GUARDRAIL_WARNING = "guardrail_warning"
    GUARDRAIL_BLOCKED = "guardrail_blocked"
    LOW_GROUNDEDNESS = "low_groundedness"
    MISSING_CITATIONS = "missing_citations"
    INVESTMENT_ADVICE_RISK = "investment_advice_risk"
    PII_RISK = "pii_risk"
    MANUAL_REVIEW_REQUESTED = "manual_review_requested"