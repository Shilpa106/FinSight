from app.llm.mock_llm_client import MockLLMClient


def test_mock_llm_client_generates_answer() -> None:
    client = MockLLMClient()

    response = client.generate_answer(
        question="What is revenue?",
        context="Revenue increased year over year.",
    )

    assert response["provider"] == "mock"
    assert response["model"] == "mock-llm"
    assert response["answer"]
    assert response["latency_ms"] >= 0