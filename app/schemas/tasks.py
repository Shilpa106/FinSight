from uuid import UUID

from pydantic import BaseModel


class AsyncTaskResponse(BaseModel):
    task_id: str
    workflow_run_id: UUID | None = None
    document_id: UUID | None = None
    status: str
    message: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: dict | None = None
    error: str | None = None


class WorkflowStatusResponse(BaseModel):
    workflow_run_id: UUID
    document_id: UUID | None
    workflow_name: str
    status: str
    error_message: str | None