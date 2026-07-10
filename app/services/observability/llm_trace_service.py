from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.llm_trace import LLMTrace
from app.db.repositories.llm_trace_repository import LLMTraceRepository


class LLMTraceService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = LLMTraceRepository(db)

    def record_trace(
        self,
        organization_id: UUID,
        provider: str,
        model_name: str,
        workflow_run_id: UUID | None = None,
        document_id: UUID | None = None,
        prompt_name: str | None = None,
        prompt_version: str | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        total_tokens: int | None = None,
        latency_ms: int | None = None,
        estimated_cost_usd: float | None = None,
        success: bool = True,
        error_message: str | None = None,
        request_metadata: dict | None = None,
        response_metadata: dict | None = None,
    ) -> LLMTrace:
        trace = LLMTrace(
            organization_id=organization_id,
            workflow_run_id=workflow_run_id,
            document_id=document_id,
            provider=provider,
            model_name=model_name,
            prompt_name=prompt_name,
            prompt_version=prompt_version,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            latency_ms=latency_ms,
            estimated_cost_usd=estimated_cost_usd,
            success=success,
            error_message=error_message,
            request_metadata=request_metadata,
            response_metadata=response_metadata,
        )

        return self.repository.create(trace)