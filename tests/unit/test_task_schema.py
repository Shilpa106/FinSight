from uuid import uuid4

from app.schemas.task import AsyncTaskResponse


def test_async_task_response_schema() -> None:
    document_id = uuid4()

    response = AsyncTaskResponse(
        task_id="task-123",
        workflow_run_id=None,
        document_id=document_id,
        status="queued",
        message="Task queued.",
    )

    assert response.task_id == "task-123"
    assert response.document_id == document_id
    assert response.status == "queued"