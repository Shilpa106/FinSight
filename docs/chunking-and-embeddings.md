# Chunking and Embeddings

## Overview

Phase 5 converts extracted document text into retrieval-ready chunks and indexes them in a vector database.

The output of this phase is used by the RAG pipeline in Phase 6.

## Flow

```text
Document Text Extracted
  ↓
Read full_text from document_texts
  ↓
Split text into page-aware chunks
  ↓
Persist chunks in document_chunks
  ↓
Generate embeddings
  ↓
Create Qdrant collection if needed
  ↓
Upsert vectors into Qdrant
  ↓
Persist vector IDs in PostgreSQL
  ↓
Update document status to indexed