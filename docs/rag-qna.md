# RAG Retrieval and Q&A

## Overview

Phase 6 adds retrieval-augmented question answering over indexed financial documents.

Users can ask natural-language questions about a document. The system retrieves relevant chunks from Qdrant, builds a context window, generates a grounded answer using an LLM, and returns citations.

## Flow

```text
User Question
  ↓
Validate Document Access
  ↓
Create or Reuse Chat Session
  ↓
Embed Question
  ↓
Search Qdrant with Tenant and Document Filters
  ↓
Build Context
  ↓
Generate Answer
  ↓
Build Citations
  ↓
Persist Messages
  ↓
Store LLM Trace
  ↓
Return Answer