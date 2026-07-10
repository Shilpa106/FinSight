from app.core.config import settings
from app.llm.llm_client import LLMClient
from app.llm.mock_llm_client import MockLLMClient
from app.llm.openai_client import OpenAILLMClient


def get_llm_client() -> LLMClient:
    if settings.LLM_PROVIDER == "mock":
        return MockLLMClient()

    if settings.LLM_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI LLM provider.")

        return OpenAILLMClient(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_CHAT_MODEL,
        )

    raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")