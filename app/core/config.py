from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FinSight AI Platform"
    APP_ENV: str = "local"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+psycopg2://finsight:finsight@localhost:5432/finsight"
    REDIS_URL: str = "redis://localhost:6379/0"

    # Storage
    STORAGE_PROVIDER: str = "local"
    LOCAL_STORAGE_PATH: str = "./storage"

    S3_BUCKET_NAME: str = "finsight-documents"
    S3_REGION: str = "ap-south-1"
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    S3_ENDPOINT_URL: str | None = None

    # Vector DB
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "finsight_documents"

    # LLM
    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str | None = None
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Chunking
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 150
    MIN_CHUNK_SIZE: int = 100

    # Embeddings
    EMBEDDING_PROVIDER: str = "mock"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSION: int = 1536
    EMBEDDING_BATCH_SIZE: int = 32

    # Vector DB
    VECTOR_DB_PROVIDER: str = "qdrant"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "finsight_documents"
    
    # # For local mock embeddings, set:
    # EMBEDDING_DIMENSION: int = 384

    # RAG
    RAG_TOP_K: int = 5
    RAG_MIN_SCORE: float = 0.20
    RAG_MAX_CONTEXT_CHARS: int = 8000

    # LLM
    LLM_PROVIDER: str = "mock"
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 1000

    LOG_LEVEL: str = "INFO"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    CELERY_TASK_ALWAYS_EAGER: bool = False
    CELERY_TASK_TIME_LIMIT: int = 1800
    CELERY_TASK_SOFT_TIME_LIMIT: int = 1500

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()