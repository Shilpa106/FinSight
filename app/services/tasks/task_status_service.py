from celery.result import AsyncResult

from app.celery_app import celery_app


class TaskStatusService:
    def get_task_status(self, task_id: str) -> dict:
        result = AsyncResult(task_id, app=celery_app)

        response = {
            "task_id": task_id,
            "status": result.status,
            "result": None,
            "error": None,
        }

        if result.successful():
            response["result"] = result.result

        if result.failed():
            response["error"] = str(result.result)

        return response