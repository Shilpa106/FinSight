# Architecture

FinSight follows a modular, layered architecture designed for production AI systems.

## High-Level Architecture

```text
Client
  ↓
FastAPI Backend
  ↓
Service Layer
  ↓
Agent and Workflow Layer
  ↓
Storage, Database, Vector DB, Queue, LLM Provider