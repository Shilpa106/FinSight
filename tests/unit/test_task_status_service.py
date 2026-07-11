from app.services.tasks.task_status_service import TaskStatusService


def test_task_status_service_initializes() -> None:
    service = TaskStatusService()

    assert service is not None
    