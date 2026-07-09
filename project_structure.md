finsight-ai-platform/
│
├── README.md
├── Makefile
├── pyproject.toml
├── poetry.lock
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── .dockerignore
├── docker-compose.yml
├── docker-compose.observability.yml
├── docker-compose.local.yml
├── alembic.ini
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── server.py
│   ├── lifespan.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── constants.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── security.py
│   │   ├── middleware.py
│   │   ├── permissions.py
│   │   ├── tenant_context.py
│   │   ├── rate_limiter.py
│   │   ├── feature_flags.py
│   │   ├── error_codes.py
│   │   └── app_context.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   │
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       │
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── organizations.py
│   │       │   ├── documents.py
│   │       │   ├── document_status.py
│   │       │   ├── document_chunks.py
│   │       │   ├── extraction.py
│   │       │   ├── chat.py
│   │       │   ├── risk_analysis.py
│   │       │   ├── compliance.py
│   │       │   ├── evaluations.py
│   │       │   ├── reviews.py
│   │       │   ├── notifications.py
│   │       │   ├── audit_logs.py
│   │       │   ├── observability.py
│   │       │   ├── health.py
│   │       │   └── admin.py
│   │       │
│   │       ├── request_models/
│   │       │   ├── __init__.py
│   │       │   ├── auth_requests.py
│   │       │   ├── document_requests.py
│   │       │   ├── extraction_requests.py
│   │       │   ├── chat_requests.py
│   │       │   ├── risk_requests.py
│   │       │   ├── evaluation_requests.py
│   │       │   └── review_requests.py
│   │       │
│   │       └── response_models/
│   │           ├── __init__.py
│   │           ├── auth_responses.py
│   │           ├── document_responses.py
│   │           ├── extraction_responses.py
│   │           ├── chat_responses.py
│   │           ├── risk_responses.py
│   │           ├── evaluation_responses.py
│   │           ├── review_responses.py
│   │           └── common_responses.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   ├── base.py
│   │   ├── transaction.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── organization.py
│   │   │   ├── document.py
│   │   │   ├── document_chunk.py
│   │   │   ├── extracted_field.py
│   │   │   ├── risk_finding.py
│   │   │   ├── chat_session.py
│   │   │   ├── chat_message.py
│   │   │   ├── evaluation.py
│   │   │   ├── human_review.py
│   │   │   ├── notification.py
│   │   │   ├── audit_log.py
│   │   │   ├── workflow_run.py
│   │   │   ├── workflow_step.py
│   │   │   ├── prompt_version.py
│   │   │   ├── llm_trace.py
│   │   │   └── api_key.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py
│   │   │   ├── organization_repository.py
│   │   │   ├── document_repository.py
│   │   │   ├── chunk_repository.py
│   │   │   ├── extraction_repository.py
│   │   │   ├── risk_repository.py
│   │   │   ├── chat_repository.py
│   │   │   ├── evaluation_repository.py
│   │   │   ├── review_repository.py
│   │   │   ├── audit_repository.py
│   │   │   ├── workflow_repository.py
│   │   │   └── llm_trace_repository.py
│   │   │
│   │   └── migrations/
│   │       ├── README
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       └── versions/
│   │           ├── 0001_create_users_and_organizations.py
│   │           ├── 0002_create_documents.py
│   │           ├── 0003_create_chunks_and_embeddings.py
│   │           ├── 0004_create_extractions.py
│   │           ├── 0005_create_risk_findings.py
│   │           ├── 0006_create_chat_tables.py
│   │           ├── 0007_create_evaluations.py
│   │           ├── 0008_create_human_reviews.py
│   │           ├── 0009_create_audit_logs.py
│   │           ├── 0010_create_workflow_runs.py
│   │           └── 0011_create_llm_traces.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── common.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── organization.py
│   │   ├── document.py
│   │   ├── document_chunk.py
│   │   ├── extraction.py
│   │   ├── financial_fields.py
│   │   ├── loan_agreement.py
│   │   ├── annual_report.py
│   │   ├── fund_report.py
│   │   ├── risk.py
│   │   ├── chat.py
│   │   ├── citation.py
│   │   ├── evaluation.py
│   │   ├── review.py
│   │   ├── notification.py
│   │   ├── audit.py
│   │   ├── workflow.py
│   │   └── llm.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   │
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── password_service.py
│   │   │   ├── token_service.py
│   │   │   ├── api_key_service.py
│   │   │   └── rbac_service.py
│   │   │
│   │   ├── documents/
│   │   │   ├── __init__.py
│   │   │   ├── document_service.py
│   │   │   ├── upload_service.py
│   │   │   ├── document_status_service.py
│   │   │   ├── metadata_service.py
│   │   │   ├── document_access_service.py
│   │   │   └── document_version_service.py
│   │   │
│   │   ├── ingestion/
│   │   │   ├── __init__.py
│   │   │   ├── ingestion_service.py
│   │   │   ├── text_extraction_service.py
│   │   │   ├── ocr_service.py
│   │   │   ├── chunking_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── indexing_service.py
│   │   │   ├── checksum_service.py
│   │   │   └── idempotency_service.py
│   │   │
│   │   ├── classification/
│   │   │   ├── __init__.py
│   │   │   ├── document_classifier_service.py
│   │   │   ├── classification_rules.py
│   │   │   ├── classification_prompts.py
│   │   │   └── classification_confidence.py
│   │   │
│   │   ├── extraction/
│   │   │   ├── __init__.py
│   │   │   ├── extraction_service.py
│   │   │   ├── financial_extraction_service.py
│   │   │   ├── covenant_extraction_service.py
│   │   │   ├── kyc_extraction_service.py
│   │   │   ├── compliance_extraction_service.py
│   │   │   ├── schema_validation_service.py
│   │   │   ├── confidence_scoring_service.py
│   │   │   └── extraction_normalizer.py
│   │   │
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── rag_service.py
│   │   │   ├── query_rewrite_service.py
│   │   │   ├── retrieval_service.py
│   │   │   ├── hybrid_search_service.py
│   │   │   ├── reranker_service.py
│   │   │   ├── context_compression_service.py
│   │   │   ├── answer_generation_service.py
│   │   │   ├── citation_service.py
│   │   │   ├── citation_validator.py
│   │   │   └── conversation_memory_service.py
│   │   │
│   │   ├── risk/
│   │   │   ├── __init__.py
│   │   │   ├── risk_analysis_service.py
│   │   │   ├── financial_risk_rules.py
│   │   │   ├── covenant_risk_service.py
│   │   │   ├── liquidity_risk_service.py
│   │   │   ├── compliance_risk_service.py
│   │   │   ├── risk_score_service.py
│   │   │   └── risk_summary_service.py
│   │   │
│   │   ├── guardrails/
│   │   │   ├── __init__.py
│   │   │   ├── guardrail_service.py
│   │   │   ├── input_guardrail_service.py
│   │   │   ├── retrieval_guardrail_service.py
│   │   │   ├── output_guardrail_service.py
│   │   │   ├── hallucination_checker.py
│   │   │   ├── prompt_injection_detector.py
│   │   │   ├── pii_redaction_service.py
│   │   │   ├── financial_advice_policy.py
│   │   │   ├── schema_guardrail.py
│   │   │   └── tenant_guardrail.py
│   │   │
│   │   ├── evaluations/
│   │   │   ├── __init__.py
│   │   │   ├── evaluation_service.py
│   │   │   ├── rag_evaluation_service.py
│   │   │   ├── extraction_evaluation_service.py
│   │   │   ├── workflow_evaluation_service.py
│   │   │   ├── golden_dataset_service.py
│   │   │   ├── regression_test_service.py
│   │   │   ├── human_feedback_service.py
│   │   │   └── metrics_aggregator.py
│   │   │
│   │   ├── reviews/
│   │   │   ├── __init__.py
│   │   │   ├── human_review_service.py
│   │   │   ├── review_assignment_service.py
│   │   │   ├── review_decision_service.py
│   │   │   └── review_escalation_service.py
│   │   │
│   │   ├── notifications/
│   │   │   ├── __init__.py
│   │   │   ├── notification_service.py
│   │   │   ├── email_notification_service.py
│   │   │   ├── slack_notification_service.py
│   │   │   ├── webhook_notification_service.py
│   │   │   └── notification_templates.py
│   │   │
│   │   ├── observability/
│   │   │   ├── __init__.py
│   │   │   ├── tracing_service.py
│   │   │   ├── metrics_service.py
│   │   │   ├── logging_service.py
│   │   │   ├── llm_observability_service.py
│   │   │   ├── cost_tracking_service.py
│   │   │   ├── latency_tracking_service.py
│   │   │   └── failure_tracking_service.py
│   │   │
│   │   ├── audit/
│   │   │   ├── __init__.py
│   │   │   ├── audit_service.py
│   │   │   ├── audit_event_builder.py
│   │   │   └── audit_policy.py
│   │   │
│   │   └── admin/
│   │       ├── __init__.py
│   │       ├── admin_service.py
│   │       ├── usage_service.py
│   │       ├── tenant_admin_service.py
│   │       └── system_config_service.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── agent_context.py
│   │   ├── agent_state.py
│   │   ├── agent_registry.py
│   │   ├── agent_exceptions.py
│   │   │
│   │   ├── ingestion_agent.py
│   │   ├── classification_agent.py
│   │   ├── extraction_agent.py
│   │   ├── rag_agent.py
│   │   ├── query_rewrite_agent.py
│   │   ├── risk_agent.py
│   │   ├── compliance_agent.py
│   │   ├── guardrail_agent.py
│   │   ├── evaluation_agent.py
│   │   ├── human_review_agent.py
│   │   ├── notification_agent.py
│   │   └── summarization_agent.py
│   │
│   ├── workflows/
│   │   ├── __init__.py
│   │   ├── workflow_registry.py
│   │   ├── workflow_state.py
│   │   ├── workflow_events.py
│   │   ├── workflow_exceptions.py
│   │   │
│   │   ├── document_processing_workflow.py
│   │   ├── rag_query_workflow.py
│   │   ├── extraction_workflow.py
│   │   ├── risk_analysis_workflow.py
│   │   ├── evaluation_workflow.py
│   │   ├── human_review_workflow.py
│   │   └── notification_workflow.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   ├── llm_provider.py
│   │   ├── openai_client.py
│   │   ├── anthropic_client.py
│   │   ├── local_llm_client.py
│   │   ├── model_router.py
│   │   ├── fallback_strategy.py
│   │   ├── token_counter.py
│   │   ├── prompt_renderer.py
│   │   ├── structured_output.py
│   │   ├── retry_policy.py
│   │   ├── timeout_policy.py
│   │   └── llm_exceptions.py
│   │
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── prompt_registry.py
│   │   ├── prompt_versioning.py
│   │   │
│   │   ├── system/
│   │   │   ├── base_financial_assistant.md
│   │   │   ├── no_investment_advice.md
│   │   │   ├── citation_required.md
│   │   │   └── tenant_security.md
│   │   │
│   │   ├── classification/
│   │   │   ├── classify_document.md
│   │   │   └── classify_financial_document.md
│   │   │
│   │   ├── extraction/
│   │   │   ├── extract_annual_report_fields.md
│   │   │   ├── extract_loan_agreement_fields.md
│   │   │   ├── extract_fund_report_fields.md
│   │   │   ├── extract_kyc_fields.md
│   │   │   └── extract_compliance_fields.md
│   │   │
│   │   ├── rag/
│   │   │   ├── rewrite_query.md
│   │   │   ├── generate_grounded_answer.md
│   │   │   ├── compress_context.md
│   │   │   └── validate_citations.md
│   │   │
│   │   ├── risk/
│   │   │   ├── analyze_financial_risk.md
│   │   │   ├── analyze_covenant_risk.md
│   │   │   ├── analyze_liquidity_risk.md
│   │   │   └── summarize_risk_findings.md
│   │   │
│   │   ├── guardrails/
│   │   │   ├── detect_prompt_injection.md
│   │   │   ├── detect_hallucination.md
│   │   │   ├── validate_grounding.md
│   │   │   └── redact_sensitive_output.md
│   │   │
│   │   ├── evaluation/
│   │   │   ├── evaluate_faithfulness.md
│   │   │   ├── evaluate_answer_relevance.md
│   │   │   ├── evaluate_context_relevance.md
│   │   │   ├── evaluate_extraction_accuracy.md
│   │   │   └── evaluate_citation_accuracy.md
│   │   │
│   │   └── review/
│   │       ├── generate_review_summary.md
│   │       └── generate_reviewer_notes.md
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── chunking/
│   │   │   ├── __init__.py
│   │   │   ├── base_chunker.py
│   │   │   ├── recursive_chunker.py
│   │   │   ├── semantic_chunker.py
│   │   │   ├── financial_section_chunker.py
│   │   │   └── chunk_metadata_builder.py
│   │   │
│   │   ├── embeddings/
│   │   │   ├── __init__.py
│   │   │   ├── embedding_client.py
│   │   │   ├── openai_embedding_client.py
│   │   │   ├── local_embedding_client.py
│   │   │   ├── embedding_cache.py
│   │   │   └── embedding_batcher.py
│   │   │
│   │   ├── vectorstores/
│   │   │   ├── __init__.py
│   │   │   ├── vectorstore_client.py
│   │   │   ├── qdrant_client.py
│   │   │   ├── pinecone_client.py
│   │   │   ├── weaviate_client.py
│   │   │   ├── collection_manager.py
│   │   │   └── tenant_vector_policy.py
│   │   │
│   │   ├── retrieval/
│   │   │   ├── __init__.py
│   │   │   ├── retriever.py
│   │   │   ├── hybrid_retriever.py
│   │   │   ├── keyword_retriever.py
│   │   │   ├── vector_retriever.py
│   │   │   ├── metadata_filter.py
│   │   │   ├── reranker.py
│   │   │   └── retrieval_result.py
│   │   │
│   │   └── citations/
│   │       ├── __init__.py
│   │       ├── citation_builder.py
│   │       ├── citation_validator.py
│   │       ├── source_mapper.py
│   │       └── citation_formatter.py
│   │
│   ├── document_processing/
│   │   ├── __init__.py
│   │   │
│   │   ├── loaders/
│   │   │   ├── __init__.py
│   │   │   ├── base_loader.py
│   │   │   ├── pdf_loader.py
│   │   │   ├── docx_loader.py
│   │   │   ├── csv_loader.py
│   │   │   ├── xlsx_loader.py
│   │   │   ├── image_loader.py
│   │   │   └── html_loader.py
│   │   │
│   │   ├── ocr/
│   │   │   ├── __init__.py
│   │   │   ├── ocr_client.py
│   │   │   ├── tesseract_ocr.py
│   │   │   ├── aws_textract_ocr.py
│   │   │   └── ocr_quality_checker.py
│   │   │
│   │   ├── parsers/
│   │   │   ├── __init__.py
│   │   │   ├── financial_statement_parser.py
│   │   │   ├── table_parser.py
│   │   │   ├── loan_agreement_parser.py
│   │   │   ├── annual_report_parser.py
│   │   │   └── kyc_parser.py
│   │   │
│   │   ├── preprocessors/
│   │   │   ├── __init__.py
│   │   │   ├── text_cleaner.py
│   │   │   ├── page_normalizer.py
│   │   │   ├── table_normalizer.py
│   │   │   ├── language_detector.py
│   │   │   └── duplicate_page_detector.py
│   │   │
│   │   └── validators/
│   │       ├── __init__.py
│   │       ├── file_type_validator.py
│   │       ├── file_size_validator.py
│   │       ├── malware_scan_stub.py
│   │       ├── document_quality_validator.py
│   │       └── text_extraction_validator.py
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   │
│   │   ├── storage/
│   │   │   ├── __init__.py
│   │   │   ├── storage_client.py
│   │   │   ├── s3_client.py
│   │   │   ├── local_storage_client.py
│   │   │   ├── minio_client.py
│   │   │   └── signed_url_service.py
│   │   │
│   │   ├── queues/
│   │   │   ├── __init__.py
│   │   │   ├── queue_client.py
│   │   │   ├── celery_app.py
│   │   │   ├── redis_queue.py
│   │   │   ├── sqs_queue.py
│   │   │   ├── kafka_client.py
│   │   │   └── dead_letter_queue.py
│   │   │
│   │   ├── email/
│   │   │   ├── __init__.py
│   │   │   ├── email_client.py
│   │   │   ├── ses_email_client.py
│   │   │   └── smtp_email_client.py
│   │   │
│   │   ├── slack/
│   │   │   ├── __init__.py
│   │   │   ├── slack_client.py
│   │   │   └── slack_message_builder.py
│   │   │
│   │   └── webhooks/
│   │       ├── __init__.py
│   │       ├── webhook_client.py
│   │       ├── webhook_signature.py
│   │       └── webhook_retry_policy.py
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_worker.py
│   │   ├── document_tasks.py
│   │   ├── ingestion_tasks.py
│   │   ├── embedding_tasks.py
│   │   ├── extraction_tasks.py
│   │   ├── risk_tasks.py
│   │   ├── evaluation_tasks.py
│   │   ├── notification_tasks.py
│   │   ├── cleanup_tasks.py
│   │   └── scheduled_tasks.py
│   │
│   ├── policies/
│   │   ├── __init__.py
│   │   ├── financial_advice_policy.yaml
│   │   ├── document_access_policy.yaml
│   │   ├── tenant_isolation_policy.yaml
│   │   ├── pii_policy.yaml
│   │   ├── prompt_injection_policy.yaml
│   │   ├── human_review_policy.yaml
│   │   ├── risk_scoring_policy.yaml
│   │   └── retention_policy.yaml
│   │
│   ├── enums/
│   │   ├── __init__.py
│   │   ├── document_type.py
│   │   ├── document_status.py
│   │   ├── user_role.py
│   │   ├── risk_level.py
│   │   ├── review_status.py
│   │   ├── workflow_status.py
│   │   ├── evaluation_metric.py
│   │   └── llm_provider.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── datetime_utils.py
│       ├── json_utils.py
│       ├── hashing.py
│       ├── pagination.py
│       ├── file_utils.py
│       ├── retry.py
│       ├── circuit_breaker.py
│       ├── text_utils.py
│       ├── money_utils.py
│       ├── percentage_utils.py
│       ├── validation_utils.py
│       └── correlation_id.py
│
├── frontend/
│   ├── README.md
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── .env.example
│   │
│   ├── public/
│   │   ├── logo.svg
│   │   └── favicon.ico
│   │
│   └── src/
│       ├── app/
│       │   ├── layout.tsx
│       │   ├── page.tsx
│       │   ├── login/
│       │   │   └── page.tsx
│       │   ├── dashboard/
│       │   │   └── page.tsx
│       │   ├── documents/
│       │   │   ├── page.tsx
│       │   │   └── [documentId]/
│       │   │       └── page.tsx
│       │   ├── chat/
│       │   │   └── page.tsx
│       │   ├── reviews/
│       │   │   └── page.tsx
│       │   ├── evaluations/
│       │   │   └── page.tsx
│       │   └── admin/
│       │       └── page.tsx
│       │
│       ├── components/
│       │   ├── common/
│       │   │   ├── Button.tsx
│       │   │   ├── Modal.tsx
│       │   │   ├── Table.tsx
│       │   │   └── Loader.tsx
│       │   ├── documents/
│       │   │   ├── DocumentUploader.tsx
│       │   │   ├── DocumentList.tsx
│       │   │   ├── DocumentStatusCard.tsx
│       │   │   ├── DocumentPreview.tsx
│       │   │   └── ExtractedFieldsPanel.tsx
│       │   ├── chat/
│       │   │   ├── ChatWindow.tsx
│       │   │   ├── ChatMessage.tsx
│       │   │   ├── CitationPanel.tsx
│       │   │   └── SourceChunkViewer.tsx
│       │   ├── risk/
│       │   │   ├── RiskScoreCard.tsx
│       │   │   ├── RiskFindingList.tsx
│       │   │   └── RiskTrendChart.tsx
│       │   ├── reviews/
│       │   │   ├── ReviewQueue.tsx
│       │   │   ├── ReviewDecisionPanel.tsx
│       │   │   └── ReviewerNotes.tsx
│       │   └── evaluations/
│       │       ├── EvaluationMetrics.tsx
│       │       ├── RegressionRunTable.tsx
│       │       └── LLMTraceViewer.tsx
│       │
│       ├── lib/
│       │   ├── api-client.ts
│       │   ├── auth.ts
│       │   ├── constants.ts
│       │   └── utils.ts
│       │
│       ├── hooks/
│       │   ├── useAuth.ts
│       │   ├── useDocuments.ts
│       │   ├── useChat.ts
│       │   ├── useReviews.ts
│       │   └── useEvaluations.ts
│       │
│       └── types/
│           ├── auth.ts
│           ├── document.ts
│           ├── chat.ts
│           ├── risk.ts
│           ├── evaluation.ts
│           └── review.ts
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── factories.py
│   │
│   ├── unit/
│   │   ├── test_chunking_service.py
│   │   ├── test_embedding_service.py
│   │   ├── test_document_classifier.py
│   │   ├── test_extraction_service.py
│   │   ├── test_rag_service.py
│   │   ├── test_retrieval_service.py
│   │   ├── test_citation_validator.py
│   │   ├── test_guardrail_service.py
│   │   ├── test_risk_score_service.py
│   │   ├── test_evaluation_service.py
│   │   ├── test_tenant_permissions.py
│   │   └── test_prompt_injection_detector.py
│   │
│   ├── integration/
│   │   ├── test_document_upload_flow.py
│   │   ├── test_document_processing_workflow.py
│   │   ├── test_rag_query_workflow.py
│   │   ├── test_extraction_workflow.py
│   │   ├── test_risk_analysis_workflow.py
│   │   ├── test_human_review_workflow.py
│   │   ├── test_vectorstore_integration.py
│   │   ├── test_postgres_integration.py
│   │   ├── test_s3_integration.py
│   │   └── test_celery_tasks.py
│   │
│   ├── e2e/
│   │   ├── test_upload_to_answer_flow.py
│   │   ├── test_upload_to_risk_report_flow.py
│   │   ├── test_low_confidence_review_flow.py
│   │   └── test_admin_observability_flow.py
│   │
│   ├── load/
│   │   ├── locustfile.py
│   │   ├── test_document_upload_load.py
│   │   ├── test_chat_query_load.py
│   │   └── test_embedding_batch_load.py
│   │
│   ├── security/
│   │   ├── test_rbac.py
│   │   ├── test_tenant_isolation.py
│   │   ├── test_prompt_injection.py
│   │   ├── test_pii_redaction.py
│   │   └── test_document_access_control.py
│   │
│   └── fixtures/
│       ├── documents/
│       │   ├── sample_annual_report.pdf
│       │   ├── sample_loan_agreement.pdf
│       │   ├── sample_fund_report.pdf
│       │   ├── sample_kyc_document.pdf
│       │   └── prompt_injection_document.pdf
│       ├── extracted_fields/
│       │   ├── annual_report_expected.json
│       │   ├── loan_agreement_expected.json
│       │   └── fund_report_expected.json
│       ├── rag/
│       │   ├── sample_questions.json
│       │   ├── expected_answers.json
│       │   └── expected_citations.json
│       └── users/
│           ├── admin_user.json
│           ├── analyst_user.json
│           └── reviewer_user.json
│
├── evals/
│   ├── README.md
│   ├── run_rag_evals.py
│   ├── run_extraction_evals.py
│   ├── run_workflow_evals.py
│   ├── run_regression_suite.py
│   │
│   ├── datasets/
│   │   ├── golden_rag_dataset.jsonl
│   │   ├── golden_extraction_dataset.jsonl
│   │   ├── golden_risk_dataset.jsonl
│   │   ├── prompt_injection_dataset.jsonl
│   │   └── human_review_dataset.jsonl
│   │
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── faithfulness.py
│   │   ├── answer_relevance.py
│   │   ├── context_precision.py
│   │   ├── context_recall.py
│   │   ├── citation_accuracy.py
│   │   ├── extraction_accuracy.py
│   │   ├── json_validity.py
│   │   ├── hallucination_rate.py
│   │   └── human_override_rate.py
│   │
│   ├── reports/
│   │   ├── .gitkeep
│   │   └── sample_eval_report.md
│   │
│   └── notebooks/
│       ├── rag_error_analysis.ipynb
│       ├── extraction_error_analysis.ipynb
│       └── cost_latency_analysis.ipynb
│
├── infra/
│   ├── README.md
│   │
│   ├── docker/
│   │   ├── Dockerfile.api
│   │   ├── Dockerfile.worker
│   │   ├── Dockerfile.frontend
│   │   ├── Dockerfile.evals
│   │   └── entrypoint.sh
│   │
│   ├── kubernetes/
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── secrets.example.yaml
│   │   ├── api-deployment.yaml
│   │   ├── api-service.yaml
│   │   ├── worker-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── frontend-service.yaml
│   │   ├── ingress.yaml
│   │   ├── hpa-api.yaml
│   │   ├── hpa-worker.yaml
│   │   ├── cronjob-evals.yaml
│   │   ├── pdb-api.yaml
│   │   └── network-policy.yaml
│   │
│   ├── helm/
│   │   └── finsight/
│   │       ├── Chart.yaml
│   │       ├── values.yaml
│   │       ├── values-dev.yaml
│   │       ├── values-prod.yaml
│   │       └── templates/
│   │           ├── deployment-api.yaml
│   │           ├── deployment-worker.yaml
│   │           ├── service-api.yaml
│   │           ├── ingress.yaml
│   │           ├── configmap.yaml
│   │           ├── secret.yaml
│   │           ├── hpa.yaml
│   │           └── serviceaccount.yaml
│   │
│   ├── terraform/
│   │   ├── README.md
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── provider.tf
│   │   ├── backend.tf
│   │   │
│   │   ├── environments/
│   │   │   ├── dev.tfvars
│   │   │   ├── staging.tfvars
│   │   │   └── prod.tfvars
│   │   │
│   │   └── modules/
│   │       ├── vpc/
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       ├── eks/
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       ├── rds/
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       ├── s3/
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       ├── elasticache/
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       ├── sqs/
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       ├── opensearch/
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       └── monitoring/
│   │           ├── main.tf
│   │           ├── variables.tf
│   │           └── outputs.tf
│   │
│   └── local/
│       ├── init-db.sql
│       ├── init-qdrant.sh
│       ├── seed-local-data.sh
│       └── create-local-buckets.sh
│
├── observability/
│   ├── README.md
│   │
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── alert-rules.yml
│   │
│   ├── grafana/
│   │   ├── dashboards/
│   │   │   ├── api-dashboard.json
│   │   │   ├── worker-dashboard.json
│   │   │   ├── rag-quality-dashboard.json
│   │   │   ├── llm-cost-dashboard.json
│   │   │   ├── latency-dashboard.json
│   │   │   └── evaluation-dashboard.json
│   │   └── provisioning/
│   │       ├── dashboards.yml
│   │       └── datasources.yml
│   │
│   ├── loki/
│   │   └── loki-config.yml
│   │
│   ├── tempo/
│   │   └── tempo-config.yml
│   │
│   └── otel/
│       ├── collector-config.yml
│       └── semantic_conventions.md
│
├── scripts/
│   ├── dev.sh
│   ├── start-api.sh
│   ├── start-worker.sh
│   ├── run-tests.sh
│   ├── run-evals.sh
│   ├── run-migrations.sh
│   ├── create-migration.sh
│   ├── seed-db.sh
│   ├── generate-openapi.sh
│   ├── build-images.sh
│   ├── deploy-dev.sh
│   ├── deploy-staging.sh
│   ├── deploy-prod.sh
│   ├── rollback.sh
│   └── cleanup-local.sh
│
├── configs/
│   ├── app.dev.yaml
│   ├── app.staging.yaml
│   ├── app.prod.yaml
│   ├── logging.yaml
│   ├── model-routing.yaml
│   ├── embedding-config.yaml
│   ├── retrieval-config.yaml
│   ├── guardrails-config.yaml
│   ├── evaluation-config.yaml
│   └── risk-scoring-config.yaml
│
├── seed_data/
│   ├── organizations.json
│   ├── users.json
│   ├── roles.json
│   ├── sample_documents.json
│   ├── risk_rules.json
│   ├── prompt_versions.json
│   └── evaluation_questions.json
│
├── docs/
│   ├── index.md
│   ├── architecture.md
│   ├── system-design.md
│   ├── api-design.md
│   ├── database-design.md
│   ├── agent-design.md
│   ├── rag-design.md
│   ├── document-processing.md
│   ├── extraction-design.md
│   ├── risk-analysis-design.md
│   ├── guardrails.md
│   ├── evaluation-framework.md
│   ├── observability.md
│   ├── security.md
│   ├── tenant-isolation.md
│   ├── deployment.md
│   ├── ci-cd.md
│   ├── incident-response.md
│   ├── runbook.md
│   ├── local-development.md
│   ├── interview-explanation.md
│   └── tradeoffs.md
│
├── architecture/
│   ├── high-level-architecture.drawio
│   ├── document-processing-flow.drawio
│   ├── rag-query-flow.drawio
│   ├── multi-agent-workflow.drawio
│   ├── deployment-architecture.drawio
│   ├── database-erd.drawio
│   └── sequence-diagrams/
│       ├── document-upload-sequence.mmd
│       ├── rag-query-sequence.mmd
│       ├── extraction-sequence.mmd
│       ├── risk-analysis-sequence.mmd
│       └── human-review-sequence.mmd
│
├── postman/
│   ├── FinSight.postman_collection.json
│   ├── FinSight.local.postman_environment.json
│   ├── FinSight.dev.postman_environment.json
│   └── FinSight.prod.postman_environment.json
│
├── openapi/
│   ├── openapi.json
│   └── openapi.yaml
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── lint.yml
│       ├── test.yml
│       ├── security-scan.yml
│       ├── docker-build.yml
│       ├── deploy-dev.yml
│       ├── deploy-staging.yml
│       ├── deploy-prod.yml
│       └── run-evals.yml
│
└── demo/
    ├── README.md
    ├── demo_script.md
    ├── interview_talking_points.md
    ├── sample_questions.md
    ├── sample_outputs/
    │   ├── document_summary.json
    │   ├── extracted_fields.json
    │   ├── rag_answer_with_citations.json
    │   ├── risk_report.json
    │   └── evaluation_report.json
    └── screenshots/
        ├── dashboard.png
        ├── document-upload.png
        ├── rag-chat.png
        ├── risk-analysis.png
        ├── human-review.png
        └── observability-dashboard.png

        