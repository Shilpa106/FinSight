from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.workflow_run import WorkflowRun
from app.db.models.workflow_step import WorkflowStep
from app.db.repositories.base_repository import BaseRepository


class WorkflowRunRepository(BaseRepository[WorkflowRun]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, WorkflowRun)

    def list_by_document(self, document_id: UUID) -> list[WorkflowRun]:
        return (
            self.db.query(WorkflowRun)
            .filter(WorkflowRun.document_id == document_id)
            .order_by(WorkflowRun.created_at.desc())
            .all()
        )


class WorkflowStepRepository(BaseRepository[WorkflowStep]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, WorkflowStep)

    def list_by_workflow_run(self, workflow_run_id: UUID) -> list[WorkflowStep]:
        return (
            self.db.query(WorkflowStep)
            .filter(WorkflowStep.workflow_run_id == workflow_run_id)
            .order_by(WorkflowStep.step_order.asc())
            .all()
        )