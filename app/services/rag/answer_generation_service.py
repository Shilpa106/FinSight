from app.llm.llm_client import LLMClient


class AnswerGenerationService:
    def __init__(
        self,
        llm_client: LLMClient,
    ) -> None:
        self.llm_client = llm_client

    def generate_answer(
        self,
        question: str,
        context: str,
    ) -> dict:
        return self.llm_client.generate_answer(
            question=question,
            context=context,
        )