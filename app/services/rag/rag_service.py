from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.workflow_run import WorkflowRun
from app.db.models.workflow_step import WorkflowStep
from app.db.repositories.document_repository import DocumentRepository
from app.db.repositories.workflow_repository import (
    WorkflowRunRepository,
    WorkflowStepRepository,
)
from app.enums.document_status import DocumentStatus
from app.enums.workflow_status import WorkflowStatus
from app.llm.llm_client import LLMClient
from app.rag.citations.citation_builder import CitationBuilder
from app.rag.embeddings.embedding_client import EmbeddingClient
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.vectorstores.vectorstore_client import VectorStoreClient
from app.services.audit.audit_service import AuditService
from app.services.chat.chat_service import ChatService
from app.services.observability.llm_trace_service import LLMTraceService
from app.services.rag.answer_generation_service import AnswerGenerationService
from app.services.rag.retrieval_service import RetrievalService
from app.services.guardrails.input_guardrail_service import InputGuardrailService
from app.services.guardrails.output_guardrail_service import OutputGuardrailService


class RAGService:
    def __init__(
        self,
        db: Session,
        embedding_client: EmbeddingClient,
        vectorstore_client: VectorStoreClient,
        llm_client: LLMClient,
    ) -> None:
        self.db = db
        self.document_repository = DocumentRepository(db)
        self.workflow_run_repository = WorkflowRunRepository(db)
        self.workflow_step_repository = WorkflowStepRepository(db)

        self.chat_service = ChatService(db)
        self.retrieval_service = RetrievalService(
            embedding_client=embedding_client,
            vectorstore_client=vectorstore_client,
        )
        self.context_builder = ContextBuilder()
        self.answer_generation_service = AnswerGenerationService(llm_client)
        self.citation_builder = CitationBuilder()
        self.llm_trace_service = LLMTraceService(db)
        self.audit_service = AuditService(db)
        self.input_guardrail_service = InputGuardrailService()
        self.output_guardrail_service = OutputGuardrailService()

    def answer_question(
        self,
        organization_id: UUID,
        user_id: UUID,
        document_id: UUID,
        question: str,
        session_id: UUID | None = None,
    ) -> dict:
        from uuid import uuid4
        if session_id is None:
            session_id = uuid4()
        document = self.document_repository.get_by_id(document_id)

        if document is None:
            raise ValueError("Document not found.")

        if document.organization_id != organization_id:
            raise PermissionError("Access denied.")

        if document.status not in [
            DocumentStatus.INDEXED.value,
            DocumentStatus.READY.value,
        ]:
            raise ValueError(
                f"Document must be indexed before Q&A. Current status: {document.status}"
            )
        
        input_guardrail_decision = self.input_guardrail_service.validate_question(question)

        if not input_guardrail_decision.allowed:
            self.audit_service.log_event(
                organization_id=organization_id,
                user_id=user_id,
                action="guardrail.input_blocked",
                resource_type="document",
                resource_id=str(document_id),
                metadata={
                    "reason": input_guardrail_decision.reason,
                    "action": input_guardrail_decision.action,
                    "checks": [
                        check.model_dump()
                        for check in input_guardrail_decision.checks
                    ],
                },
            )

            return {
                "session_id": session_id,
                "document_id": document_id,
                "question": question,
                "answer": input_guardrail_decision.safe_response,
                "citations": [],
                "retrieved_chunk_count": 0,
                "model_provider": "guardrail",
                "model_name": "input_guardrail",
                "guardrail_action": input_guardrail_decision.action,
                "guardrail_reason": input_guardrail_decision.reason,
                "guardrail_checks": [
                    check.model_dump()
                    for check in input_guardrail_decision.checks
                ],
            }

        workflow_run = self._create_workflow_run(
            organization_id=organization_id,
            document_id=document_id,
        )

        try:
            self._mark_workflow_running(workflow_run)

            session = self.chat_service.get_or_create_session(
                organization_id=organization_id,
                user_id=user_id,
                document_id=document_id,
                session_id=session_id,
                title=question[:80],
            )

            self.chat_service.add_message(
                session_id=session.id,
                role="user",
                content=question,
                metadata={
                    "workflow_run_id": str(workflow_run.id),
                },
            )

            retrieve_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="retrieve_relevant_chunks",
                step_order=1,
            )

            retrieval_result = self._run_step(
                retrieve_step,
                lambda: self.retrieval_service.retrieve(
                    question=question,
                    organization_id=organization_id,
                    document_id=document_id,
                ),
            )

            context_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="build_context",
                step_order=2,
            )

            context = self._run_step(
                context_step,
                lambda: self.context_builder.build_context(retrieval_result.chunks),
            )

            answer_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="generate_answer",
                step_order=3,
            )

            llm_response = self._run_step(
                answer_step,
                lambda: self.answer_generation_service.generate_answer(
                    question=question,
                    context=context,
                ),
            )

            citation_step = self._create_workflow_step(
                workflow_run_id=workflow_run.id,
                step_name="build_citations",
                step_order=4,
            )

            citations = self._run_step(
                citation_step,
                lambda: self.citation_builder.build_citations(
                    retrieval_result.chunks
                ),
            )

            guardrail_step = self._create_workflow_step(
            workflow_run_id=workflow_run.id,
            step_name="validate_answer_guardrails",
            step_order=5,
            )

            output_guardrail_decision = self._run_step(
                guardrail_step,
                lambda: self.output_guardrail_service.validate_answer(
                    answer=llm_response["answer"],
                    citations=citations,
                    retrieved_chunks=retrieval_result.chunks,
                ),
            )

            final_answer = llm_response["answer"]
            final_citations = citations

            if not output_guardrail_decision.allowed:
                final_answer = output_guardrail_decision.safe_response or (
                    "I could not produce a safe, grounded answer."
                )
                final_citations = []

            self.chat_service.add_message(
                session_id=session.id,
                role="assistant",
                content=final_answer,
                citations=final_citations,
                metadata={
                    "workflow_run_id": str(workflow_run.id),
                    "retrieved_chunk_count": retrieval_result.total,
                    "model_provider": llm_response.get("provider"),
                    "model_name": llm_response.get("model"),
                    "guardrail_action": output_guardrail_decision.action,
                    "guardrail_reason": output_guardrail_decision.reason,
                    "guardrail_checks": [
                        check.model_dump()
                        for check in output_guardrail_decision.checks
                    ],
                },
            )

            self.llm_trace_service.record_trace(
                organization_id=organization_id,
                workflow_run_id=workflow_run.id,
                document_id=document_id,
                provider=llm_response.get("provider", "unknown"),
                model_name=llm_response.get("model", "unknown"),
                prompt_name="rag_grounded_answer",
                prompt_version="v1",
                input_tokens=llm_response.get("input_tokens"),
                output_tokens=llm_response.get("output_tokens"),
                total_tokens=llm_response.get("total_tokens"),
                latency_ms=llm_response.get("latency_ms"),
                success=True,
                request_metadata={
                    "question": question,
                    "retrieved_chunk_count": retrieval_result.total,
                    "context_length": len(context),
                },
                response_metadata=llm_response.get("raw_response"),
            )

            self.audit_service.log_event(
                organization_id=organization_id,
                user_id=user_id,
                action=(
                    "guardrail.output_blocked"
                    if not output_guardrail_decision.allowed
                    else "document.question_answered"
                ),
                resource_type="document",
                resource_id=str(document_id),
                metadata={
                    "workflow_run_id": str(workflow_run.id),
                    "session_id": str(session.id),
                    "retrieved_chunk_count": retrieval_result.total,
                    "guardrail_action": output_guardrail_decision.action,
                    "guardrail_reason": output_guardrail_decision.reason,
                    "guardrail_checks": [
                        check.model_dump()
                        for check in output_guardrail_decision.checks
                    ],
                },
            )

            workflow_run.status = WorkflowStatus.COMPLETED.value
            workflow_run.completed_at = datetime.utcnow()

            return {
                "session_id": session.id,
                "document_id": document_id,
                "question": question,
                "answer": final_answer,
                "citations": final_citations,
                "retrieved_chunk_count": retrieval_result.total,
                "model_provider": llm_response.get("provider", "unknown"),
                "model_name": llm_response.get("model", "unknown"),
                "guardrail_action": output_guardrail_decision.action,
                "guardrail_reason": output_guardrail_decision.reason,
                "guardrail_checks": [
                    check.model_dump()
                    for check in output_guardrail_decision.checks
                ],
            }

        except Exception as error:
            workflow_run.status = WorkflowStatus.FAILED.value
            workflow_run.error_message = str(error)
            workflow_run.completed_at = datetime.utcnow()

            self.audit_service.log_event(
                organization_id=organization_id,
                user_id=user_id,
                action="document.question_answering_failed",
                resource_type="document",
                resource_id=str(document_id),
                metadata={
                    "workflow_run_id": str(workflow_run.id),
                    "error": str(error),
                },
            )

            raise

    def _create_workflow_run(
        self,
        organization_id: UUID,
        document_id: UUID,
    ) -> WorkflowRun:
        workflow_run = WorkflowRun(
            organization_id=organization_id,
            document_id=document_id,
            workflow_name="rag_question_answering",
            status=WorkflowStatus.PENDING.value,
        )

        return self.workflow_run_repository.create(workflow_run)

    def _mark_workflow_running(self, workflow_run: WorkflowRun) -> None:
        workflow_run.status = WorkflowStatus.RUNNING.value
        workflow_run.started_at = datetime.utcnow()
        self.db.flush()

    def _create_workflow_step(
        self,
        workflow_run_id: UUID,
        step_name: str,
        step_order: int,
    ) -> WorkflowStep:
        workflow_step = WorkflowStep(
            workflow_run_id=workflow_run_id,
            step_name=step_name,
            step_order=step_order,
            status=WorkflowStatus.PENDING.value,
        )

        return self.workflow_step_repository.create(workflow_step)

    def _run_step(self, step: WorkflowStep, fn):
        try:
            step.status = WorkflowStatus.RUNNING.value
            step.started_at = datetime.utcnow()
            self.db.flush()

            result = fn()

            step.status = WorkflowStatus.COMPLETED.value
            step.completed_at = datetime.utcnow()
            self.db.flush()

            return result

        except Exception as error:
            step.status = WorkflowStatus.FAILED.value
            step.error_message = str(error)
            step.completed_at = datetime.utcnow()
            self.db.flush()
            raise