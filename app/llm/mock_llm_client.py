import time

from app.llm.llm_client import LLMClient


class MockLLMClient(LLMClient):
    def generate_answer(
        self,
        question: str,
        context: str,
    ) -> dict:
        start_time = time.time()

        if not context.strip():
            answer = (
                "I could not find relevant information in the indexed document "
                "to answer this question."
            )
        else:
            answer = (
                "Based on the retrieved document context, here is a grounded "
                "answer for your question. "
                "This is a mock response for local development. "
                "Please switch to OpenAI for real answer generation."
            )

        latency_ms = int((time.time() - start_time) * 1000)

        return {
            "answer": answer,
            "provider": "mock",
            "model": "mock-llm",
            "input_tokens": max(1, len(question + context) // 4),
            "output_tokens": max(1, len(answer) // 4),
            "latency_ms": latency_ms,
            "raw_response": {
                "mock": True,
            },
        }
    