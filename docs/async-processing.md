# Async Processing with Celery

## Overview

Phase 10 moves long-running document workflows into background jobs using Celery and Redis.

This prevents API requests from blocking while documents are parsed, chunked, embedded, indexed, or evaluated.

## Components

- FastAPI API
- Celery worker
- Redis broker/result backend
- PostgreSQL workflow tracking
- Qdrant vector database

## Async Workflows

### Text Extraction

```text
POST /api/v1/documents/{document_id}/process-text/async