from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FinSight AI Platform"
    APP_ENV: str = "local"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+psycopg2://finsight:finsight@localhost:5432/finsight"
    REDIS_URL: str = "redis://localhost:6379/0"

    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "finsight_documents"

    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str | None = None
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()