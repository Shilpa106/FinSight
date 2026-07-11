# FinSight AI Platform

FinSight is a production-grade AI-native multi-agent platform for financial document intelligence.

The platform helps institutional financial teams process large volumes of financial documents such as annual reports, loan agreements, fund reports, compliance documents, and KYC files.

It supports document ingestion, classification, structured financial extraction, RAG-based question answering, financial risk analysis, guardrail validation, LLM evaluation workflows, and human-in-the-loop review.

## Problem

Institutional financial teams spend significant manual effort reviewing financial documents. These documents often contain important information such as financial metrics, covenants, liquidity risks, compliance issues, and regulatory disclosures.

Manual review is slow, expensive, inconsistent, and difficult to scale.

## Solution

FinSight automates financial document analysis using a multi-agent AI architecture.

The system uses specialized agents for:

- Document ingestion
- Document classification
- Structured extraction
- RAG-based question answering
- Risk analysis
- Guardrail validation
- Evaluation
- Human review
- Notifications

## Core Capabilities

- Upload financial documents
- Extract text from PDFs and other files
- Chunk documents and generate embeddings
- Store document vectors in a vector database
- Ask grounded questions using RAG
- Extract structured financial fields
- Detect risk factors
- Validate answers with guardrails
- Evaluate LLM output quality
- Escalate low-confidence results to human reviewers
- Track latency, cost, quality, and failures

## Tech Stack

Backend:

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Celery

AI:

- LangGraph
- OpenAI / Anthropic / Local LLM
- Qdrant
- RAGAS / custom evaluations
- Pydantic structured output

Infrastructure:

- Docker
- Kubernetes
- AWS S3
- AWS RDS
- AWS EKS
- Terraform

Observability:

- OpenTelemetry
- Prometheus
- Grafana
- Loki

## MVP Scope

The MVP will support:

1. User uploads a PDF document
2. System extracts text from the PDF
3. System chunks the document
4. System generates embeddings
5. System stores chunks in Qdrant
6. User asks questions about the document
7. RAG agent answers with citations
8. Guardrail agent validates the answer
9. Evaluation agent scores the response
10. Results are stored for audit and observability

---

# Step 26: Update README MVP Progress

Add this section to your `README.md`:

```md
## Current Progress

### Completed

- Project foundation
- FastAPI skeleton
- Database foundation
- SQLAlchemy models
- Alembic migrations
- Seed data
- Health checks
- Document upload API
- Local/S3-compatible storage abstraction
- File validation
- Checksum generation
- Document metadata persistence
- Audit logging

### In Progress

- PDF text extraction

### Next

- Document processing pipeline
- Text extraction service
- Page-level PDF extraction
- Document status transition from uploaded to text_extracted

## Long-Term Scope

Future phases include:

- Structured financial extraction
- Loan covenant extraction
- Risk scoring
- Human review queue
- Prompt/version management
- Evaluation regression pipeline
- Multi-tenant RBAC
- Kubernetes deployment
- AWS production deployment

## Architecture

The system follows a layered architecture:

```text
API Layer
  ↓
Service Layer
  ↓
Agent Layer
  ↓
Workflow Layer
  ↓
Database / Vector DB / Storage / Queue



---

# Step 22: Update README Progress

Add:

```md
## Current Progress

### Completed

- Project foundation
- FastAPI skeleton
- Database foundation
- SQLAlchemy models
- Alembic migrations
- Document upload API
- Local/S3 storage abstraction
- File validation
- Checksum generation
- Audit logging
- PDF text extraction
- Document processing workflow tracking
- Extracted text persistence
- Document status transitions

### In Progress

- Chunking and embeddings

### Next

- Chunk extracted text
- Store document chunks
- Generate embeddings
- Index chunks in Qdrant


---

# Step 31: Update README Progress

Add:

```md
## Current Progress

### Completed

- Project foundation
- FastAPI skeleton
- Database foundation
- SQLAlchemy models
- Alembic migrations
- Document upload API
- Local/S3 storage abstraction
- File validation
- Checksum generation
- Audit logging
- PDF text extraction
- Extracted text persistence
- Document status transitions
- Workflow tracking
- Page-aware chunking
- Mock/OpenAI embedding abstraction
- Qdrant vector indexing
- Document chunks API

### In Progress

- RAG retrieval and Q&A

### Next

- Semantic retrieval from Qdrant
- Chat query API
- RAG answer generation
- Citations
- Guardrails



---

# Step 31: Update README Progress

Add:

```md
## Current Progress

### Completed

- Project foundation
- Database foundation
- Document upload and storage
- PDF text extraction
- Extracted text persistence
- Page-aware chunking
- Embedding generation
- Qdrant vector indexing
- RAG retrieval
- Chat query API
- LLM answer generation
- Citations
- Chat history
- LLM trace logging
- RAG workflow tracking

### In Progress

- Guardrails and hallucination checks

### Next

- Citation validation
- Groundedness checks
- No investment advice guardrail
- Prompt injection detection
- RAG evaluation metrics


---

# Step 18: README Update

Add to progress:

```md
### Completed

- RAG retrieval and Q&A
- Chat session persistence
- Citation generation
- LLM trace logging
- Input guardrails
- Prompt injection detection
- Citation validation
- Groundedness checks
- Investment advice checks
- PII checks
- Guardrail audit logging

### In Progress

- Evaluation and quality metrics

### Next

- RAG evaluation
- Extraction evaluation
- Guardrail evaluation
- Regression datasets
- Quality dashboards