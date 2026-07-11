# Human Review Workflow

## Overview

Phase 9 adds human-in-the-loop review for risky or low-confidence AI outputs.

The review workflow allows reviewers to inspect AI-generated answers, guardrail decisions, citations, and metadata before approving, rejecting, or editing the final answer.

## Review Routing

A review item is created when:

- guardrail action is `warn`
- guardrail action is `fallback`
- guardrail action is `block`
- groundedness is weak
- citations are missing
- investment-advice risk is detected
- PII risk is detected

## Review Statuses

```text
pending
approved
rejected
edited_approved