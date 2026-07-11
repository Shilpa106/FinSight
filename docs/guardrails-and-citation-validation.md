# Guardrails and Citation Validation

## Overview

Phase 7 adds safety and grounding checks to the RAG question-answering pipeline.

The system validates both user input and generated output before returning an answer.

## Input Guardrails

Input guardrails check user questions before retrieval.

Current checks:

- prompt injection patterns
- system prompt extraction attempts
- policy bypass attempts
- jailbreak-style requests

If input fails, the request is blocked before retrieval and LLM generation.

## Output Guardrails

Output guardrails validate the generated answer.

Current checks:

- citation validation
- groundedness check
- investment advice check
- PII detection

## Citation Validation

The citation validator ensures that answers have citations when retrieved chunks exist.

Each citation must include:

- chunk ID
- document ID
- page number when available
- chunk index
- score
- preview

## Groundedness

The MVP groundedness checker uses lightweight term-overlap heuristics between the generated answer and retrieved chunks.

This is not a full hallucination detector, but it provides a useful safety layer for the MVP.

Future versions can use:

- LLM-as-judge
- RAGAS faithfulness
- entailment models
- claim-level citation validation

## No Investment Advice

The system blocks direct investment advice such as:

- buy recommendations
- sell recommendations
- guaranteed return claims
- risk-free investment claims

The system is allowed to summarize and explain information contained in the document.

## Actions

Guardrails can return:

```text
allow
warn
block
fallback