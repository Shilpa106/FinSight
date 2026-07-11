# Evaluation Framework

## Overview

Phase 8 adds an evaluation framework for measuring the quality of the RAG system.

The evaluation framework runs golden question-answer cases against indexed documents and records retrieval, answer, citation, and guardrail metrics.

## Evaluation Flow

```text
Load Dataset
  ↓
Run RAG Query
  ↓
Capture Answer and Citations
  ↓
Compute Metrics
  ↓
Persist Evaluation Result
  ↓
Generate Markdown Report
