import logging
from datetime import datetime, timezone

from sqlalchemy import event, text

from ..domain.exceptions import TaskDeadlineExceededException
from ..infrastructure.exceptions import InvalidProjectIdException
from .models import TaskModel

logger = logging.getLogger(__name__)


@event.listens_for(TaskModel, "before_insert")
@event.listens_for(TaskModel, "before_update")
def validate_task_deadline(mapper, connection, target: TaskModel):
    if target.project_id:
        project_row = connection.execute(
            text("SELECT deadline FROM projects WHERE id = :pid"),
            {"pid": str(target.project_id)},
        ).fetchone()
        if project_row is None:
            raise InvalidProjectIdException(target.project_id)  # type: ignore[arg-type]
        project_deadline = project_row[0]
    elif target.project:
        project_deadline = target.project.deadline
    else:
        return

    if isinstance(project_deadline, str):
        project_deadline_utc = datetime.fromisoformat(project_deadline)
    else:
        project_deadline_utc = project_deadline  # type: ignore[assignment]

    if project_deadline_utc.tzinfo is None:
        project_deadline_utc = project_deadline_utc.replace(tzinfo=timezone.utc)

    task_deadline_utc = target.deadline
    if task_deadline_utc.tzinfo is None:
        task_deadline_utc = task_deadline_utc.replace(tzinfo=timezone.utc)

    if task_deadline_utc > project_deadline_utc:
        raise TaskDeadlineExceededException(
            task_title=target.title,  # type: ignore[arg-type]
            task_deadline=task_deadline_utc,  # type: ignore[arg-type]
            project_deadline=project_deadline_utc,
        )


def _sync_project_completion(connection, project_id: str, project_title: str) -> None:
    row = connection.execute(
        text("SELECT COUNT(1) FROM tasks WHERE project_id = :pid AND completed = 0"),
        {"pid": str(project_id)},
    ).fetchone()
    incomplete_tasks = row[0] if row else 0

    prev_row = connection.execute(
        text("SELECT completed FROM projects WHERE id = :pid"),
        {"pid": str(project_id)},
    ).fetchone()
    previous_completed = prev_row[0] if prev_row else False

    completed = incomplete_tasks == 0

    connection.execute(
        text(
            "UPDATE projects SET completed = :completed, updated_at = :ts WHERE id = :pid"
        ),
        {"pid": project_id, "ts": datetime.now(timezone.utc), "completed": completed},
    )

    if completed != previous_completed:
        status_str = "COMPLETED" if completed else "UNCOMPLETED"
        logger.info(
            f"Project with id {project_id} and title {project_title} changed status: {status_str}"
        )


@event.listens_for(TaskModel, "after_update")
def task_after_update(mapper, connection, target: TaskModel):
    if target.project_id:
        _sync_project_completion(
            connection=connection,
            project_id=target.project_id,  # type: ignore[arg-type]
            project_title=target.title,  # type: ignore[arg-type]
        )


@event.listens_for(TaskModel, "after_delete")
def task_after_delete(mapper, connection, target: TaskModel):
    if target.project_id:
        _sync_project_completion(
            connection=connection,
            project_id=target.project_id,  # type: ignore[arg-type]
            project_title=target.title,  # type: ignore[arg-type]
        )
