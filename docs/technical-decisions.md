
---

## 6. Write `docs/technical-decisions.md`

This is very important for interviews.

```md
# Technical Decisions

## Decision 1: FastAPI for Backend APIs

FastAPI is used because it provides high performance, async support, automatic OpenAPI generation, and strong Pydantic integration.

Alternatives considered:

- Django REST Framework
- Flask

Reason:

FastAPI is better suited for AI-native APIs where request validation, async execution, and typed schemas are important.

## Decision 2: PostgreSQL as Primary Database

PostgreSQL is used for transactional data such as users, documents, chat messages, evaluations, workflow runs, and audit logs.

Alternatives considered:

- MySQL
- MongoDB

Reason:

The platform needs relational consistency, joins, transactions, migrations, and strong support for structured data.

## Decision 3: Qdrant as Vector Database

Qdrant is used for vector search and document retrieval.

Alternatives considered:

- Pinecone
- Weaviate
- pgvector

Reason:

Qdrant is open-source, easy to run locally, supports metadata filtering, and works well for tenant-aware retrieval.

## Decision 4: LangGraph for Workflow Orchestration

LangGraph is used for deterministic multi-agent workflow orchestration.

Alternatives considered:

- CrewAI
- AutoGen
- Custom orchestration

Reason:

LangGraph gives better control over state, routing, retries, and deterministic workflow execution.

## Decision 5: Celery and Redis for Async Jobs

Celery and Redis are used for background document processing.

Alternatives considered:

- FastAPI background tasks
- Kafka
- AWS SQS

Reason:

Celery is simple, mature, and sufficient for MVP asynchronous processing. Kafka or SQS can be introduced later for larger event-driven workflows.

## Decision 6: Pydantic for Structured LLM Output

Pydantic schemas are used to validate extracted fields and LLM-generated structured responses.

Reason:

LLM outputs are unreliable by default. Schema validation ensures only valid, typed, expected data enters the system.

## Decision 7: Guardrails as Services, Not Only Prompts

Guardrails are implemented as code-level services.

Reason:

Prompt-only guardrails are not enough for production. The system needs validation, policy checks, citation checks, tenant filters, and human escalation.

## Decision 8: Evaluation Pipeline from the Beginning

Evaluation is included early instead of after production.

Reason:

AI systems can regress when prompts, models, embeddings, or retrievers change. Evaluation datasets and metrics help detect quality regressions before deployment.

## Decision 9: Object Storage for Documents

Documents are stored in S3 or MinIO instead of directly in PostgreSQL.

Reason:

Files can be large. Object storage is cheaper, scalable, and better suited for raw document storage.

## Decision 10: Observability Is a First-Class Requirement

The system tracks API latency, worker failures, LLM latency, token usage, cost, retrieved chunks, evaluation scores, and hallucination rate.

Reason:

Production AI systems require visibility into both infrastructure behavior and model behavior.