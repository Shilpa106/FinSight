# Database Design

FinSight uses PostgreSQL as the primary transactional database.

The database is designed around tenant-aware financial document processing. Every major business entity is associated with an organization to support future multi-tenant isolation.

## Core Tables

### organizations

Stores tenant organizations.

### users

Stores platform users. Each user belongs to one organization and has a role.

### documents

Stores metadata for uploaded financial documents.

The actual document file is stored in object storage such as S3 or MinIO. PostgreSQL stores only metadata and the storage key.

### document_chunks

Stores text chunks extracted from documents.

Each chunk contains page information, chunk index, token count, metadata, and a vector ID that maps to the vector database.

### chat_sessions

Stores user chat sessions for a specific document.

### chat_messages

Stores user and assistant messages, including citations and metadata.

### workflow_runs

Tracks execution of long-running workflows such as document processing, RAG queries, extraction, and risk analysis.

### workflow_steps

Tracks individual workflow steps for debugging, retry, and observability.

### llm_traces

Stores metadata about LLM calls including provider, model, token usage, latency, prompt version, cost, and success or failure.

### audit_logs

Stores user and system actions for compliance and traceability.

## Design Principles

- Store raw files in object storage, not PostgreSQL
- Store metadata and structured results in PostgreSQL
- Use UUID primary keys
- Add organization_id to tenant-owned records
- Track workflow execution explicitly
- Store LLM traces for observability
- Store audit logs for compliance
- Keep vector embeddings in Qdrant, not PostgreSQL
- Store vector IDs in PostgreSQL for traceability

## Tenant Isolation

Most tables include organization_id.

This ensures that all queries can be filtered by organization and prevents users from accessing documents from another tenant.

## Workflow Observability

Workflow runs and workflow steps allow the system to answer:

- Which workflow processed this document?
- Which step failed?
- How long did each step take?
- Can the workflow be retried?
- Which LLM calls were made during the workflow?

## LLM Observability

The llm_traces table stores:

- provider
- model name
- prompt version
- token usage
- latency
- estimated cost
- success or failure
- request metadata
- response metadata

This helps debug AI behavior and monitor production cost.