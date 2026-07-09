# Document Upload and Storage

## Overview

The document upload pipeline accepts financial documents from users, validates the file, stores it in object storage, persists document metadata in PostgreSQL, and writes an audit log.

## Upload Flow

```text
User Uploads File
  ↓
API Receives Multipart Request
  ↓
Validate File Type and Size
  ↓
Read File Content
  ↓
Generate SHA-256 Checksum
  ↓
Generate Document ID
  ↓
Build Storage Key
  ↓
Upload Raw File to Storage
  ↓
Insert Document Metadata in PostgreSQL
  ↓
Create Audit Log
  ↓
Return Document ID and Status