from enum import Enum


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    TEXT_EXTRACTED = "text_extracted"
    CHUNKED = "chunked"
    EMBEDDED = "embedded"
    INDEXED = "indexed"
    READY = "ready"
    FAILED = "failed"