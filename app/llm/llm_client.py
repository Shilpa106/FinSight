from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def generate_answer(
        self,
        question: str,
        context: str,
    ) -> dict:
        pass