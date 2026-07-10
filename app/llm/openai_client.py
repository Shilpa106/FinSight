import time

from openai import OpenAI

from app.core.config import settings
from app.llm.llm_client import LLMClient


class OpenAILLMClient(LLMClient):
    def __init__(
        self,
        api_key: str,
        model: str,
    ) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_answer(
        self,
        question: str,
        context: str,
    ) -> dict:
        start_time = time.time()

        system_prompt = self._build_system_prompt()

        user_prompt = self._build_user_prompt(
            question=question,
            context=context,
        )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        latency_ms = int((time.time() - start_time) * 1000)

        answer = response.choices[0].message.content or ""

        usage = response.usage

        return {
            "answer": answer,
            "provider": "openai",
            "model": self.model,
            "input_tokens": usage.prompt_tokens if usage else None,
            "output_tokens": usage.completion_tokens if usage else None,
            "total_tokens": usage.total_tokens if usage else None,
            "latency_ms": latency_ms,
            "raw_response": {
                "id": response.id,
                "model": response.model,
            },
        }

    def _build_system_prompt(self) -> str:
        return """
You are FinSight, an AI assistant for financial document analysis.

Rules:
1. Answer only using the provided context.
2. If the context does not contain the answer, say you could not find it in the document.
3. Do not make unsupported assumptions.
4. Do not provide investment advice.
5. Include source references when possible.
6. Keep the answer clear, professional, and concise.
""".strip()

    def _build_user_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        return f"""
Context:
{context}

Question:
{question}

Answer:
""".strip()