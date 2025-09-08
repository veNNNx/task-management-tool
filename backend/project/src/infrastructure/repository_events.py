from datetime import timezone

from sqlalchemy import event

from backend.task import TaskDeadlineExceededException

from .models import ProjectModel


@event.listens_for(ProjectModel, "before_update")
def project_deadline_update(mapper, connection, target: ProjectModel):
    target_deadline_utc = target.deadline
    if target_deadline_utc.tzinfo is None:
        target_deadline_utc = target_deadline_utc.replace(tzinfo=timezone.utc)

    for task in target.tasks:
        task_deadline_utc = task.deadline
        if task_deadline_utc.tzinfo is None:
            task_deadline_utc = task_deadline_utc.replace(tzinfo=timezone.utc)

        if task_deadline_utc > target_deadline_utc:
            raise TaskDeadlineExceededException(
                task_title=task.title,
                task_deadline=task.deadline,
                project_deadline=target.deadline,  # type: ignore[arg-type]
            )
