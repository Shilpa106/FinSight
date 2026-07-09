# Product Scope

## Product Name

FinSight AI Platform

## Target Users

The initial users are financial analysts, credit analysts, risk teams, compliance reviewers, and operations teams working with institutional financial documents.

## Primary Use Cases

### 1. Document Upload

Users can upload financial documents such as annual reports, loan agreements, and fund reports.

### 2. Document Processing

The system extracts text, chunks the document, generates embeddings, and stores searchable document chunks.

### 3. Document Q&A

Users can ask questions about uploaded documents and receive grounded answers with citations.

### 4. Structured Extraction

The system extracts important fields such as borrower name, revenue, EBITDA, interest rate, maturity date, covenants, and risk factors.

### 5. Risk Analysis

The system identifies financial and compliance risks from the document.

### 6. Guardrail Validation

The system validates whether answers are grounded in retrieved context and blocks unsupported financial claims.

### 7. Evaluation

The system evaluates answer quality, citation accuracy, faithfulness, and extraction correctness.

### 8. Human Review

Low-confidence or high-risk outputs are sent to a review queue.

## MVP Scope

The first MVP includes:

- PDF upload
- Text extraction
- Chunking
- Embedding generation
- Vector search
- RAG Q&A
- Citations
- Basic guardrails
- Basic evaluation logging

## Out of Scope for MVP

The following are not part of the first MVP:

- Full frontend
- Production AWS deployment
- Advanced OCR
- Multi-document comparison
- Fine-tuning
- Real-time streaming
- Complex approval workflows
- Full regulatory compliance certification

## Future Scope

- Multi-tenant RBAC
- Human review dashboard
- Financial risk scoring
- Loan covenant extraction
- Evaluation regression suite
- Kubernetes deployment
- Terraform AWS infrastructure
- Advanced observability dashboards