# Document Processing

## Overview

Document processing converts uploaded raw files into clean extracted text that can be used for downstream chunking, embeddings, retrieval, and AI workflows.

Phase 4 focuses only on PDF text extraction.

## Processing Flow

```text
Document Uploaded
  ↓
Fetch Document Metadata
  ↓
Download Raw File from Storage
  ↓
Validate File Type
  ↓
Extract Page-Level Text
  ↓
Clean and Normalize Text
  ↓
Validate Extracted Text
  ↓
Persist Extracted Text
  ↓
Update Document Status
  ↓
Write Audit Log