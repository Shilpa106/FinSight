from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.repositories.workflow_repository import WorkflowRunRepository
from app.db.session import get_db
from app.schemas.task import TaskStatusResponse, WorkflowStatusResponse
from app.services.tasks.task_status_service import TaskStatusService

router = APIRouter()


@router.get("/{task_id}", response_model=TaskStatusResponse)
def get_task_status(task_id: str) -> TaskStatusResponse:
    service = TaskStatusService()
    result = service.get_task_status(task_id)

    return TaskStatusResponse(**result)


@router.get("/workflows/{workflow_run_id}", response_model=WorkflowStatusResponse)
def get_workflow_status(
    workflow_run_id: UUID,
    db: Session = Depends(get_db),
) -> WorkflowStatusResponse:
    repository = WorkflowRunRepository(db)
    workflow = repository.get_by_id(workflow_run_id)

    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow run not found.")

    return WorkflowStatusResponse(
        workflow_run_id=workflow.id,
        document_id=workflow.document_id,
        workflow_name=workflow.workflow_name,
        status=workflow.status,
        error_message=workflow.error_message,
    )
