# MVP Plan

The MVP will be built in small production-style increments.

## Phase 1: Project Foundation

Goal:

Set up the backend project structure, local development environment, configuration, and health check API.

Deliverables:

- FastAPI app
- Project structure
- Environment configuration
- Health check endpoint
- Docker Compose setup
- Basic logging
- README and documentation

## Phase 2: Database Foundation

Goal:

Add PostgreSQL database models and migrations.

Deliverables:

- User model
- Organization model
- Document model
- Document chunk model
- Chat session model
- Chat message model
- Audit log model
- Alembic migrations

## Phase 3: Document Upload

Goal:

Allow users to upload documents.

Deliverables:

- Document upload API
- File validation
- Local storage or S3-compatible storage
- Document metadata persistence
- Document processing status

## Phase 4: Text Extraction

Goal:

Extract text from uploaded PDFs.

Deliverables:

- PDF loader
- Text extraction service
- Page-level text extraction
- Text cleaning
- Extraction status updates

## Phase 5: Chunking and Embeddings

Goal:

Prepare documents for retrieval.

Deliverables:

- Chunking service
- Chunk metadata
- Embedding client
- Batch embedding generation
- Qdrant indexing

## Phase 6: RAG Q&A

Goal:

Allow users to ask questions about documents.

Deliverables:

- Chat query API
- Query rewrite service
- Retriever
- Answer generation service
- Citation builder
- Citation validation

## Phase 7: Guardrails

Goal:

Reduce unsafe or hallucinated outputs.

Deliverables:

- Grounding validation
- Citation requirement
- No investment advice policy
- Prompt injection detection
- Tenant retrieval guardrail

## Phase 8: Evaluations

Goal:

Measure LLM output quality.

Deliverables:

- RAG evaluation service
- Faithfulness metric
- Answer relevance metric
- Citation accuracy metric
- Evaluation result persistence
- Regression dataset structure

## Phase 9: Async Processing

Goal:

Move long-running document processing to background workers.

Deliverables:

- Celery setup
- Redis broker
- Ingestion task
- Embedding task
- Retry policy
- Dead-letter handling

## Phase 10: Observability

Goal:

Track system and AI behavior.

Deliverables:

- Structured logs
- Correlation IDs
- LLM trace logging
- Token usage tracking
- Latency metrics
- Prometheus metrics endpoint

## MVP Completion Criteria

The MVP is complete when:

1. A user can upload a PDF
2. The document is processed asynchronously
3. Text is extracted and chunked
4. Chunks are embedded and indexed
5. User can ask questions
6. System returns grounded answers with citations
7. Guardrails validate the answer
8. Evaluation results are stored
9. Logs and traces are available