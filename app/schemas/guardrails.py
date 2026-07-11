from pydantic import BaseModel


class GuardrailCheckResult(BaseModel):
    name: str
    passed: bool
    severity: str
    message: str
    metadata: dict | None = None


class GuardrailDecision(BaseModel):
    allowed: bool
    action: str
    reason: str
    checks: list[GuardrailCheckResult]
    safe_response: str | None = None
    