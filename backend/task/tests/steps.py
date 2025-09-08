from datetime import datetime, timedelta, timezone
from uuid import UUID

from attrs import define

from ..src.application.task_service import TaskService
from ..src.domain.task import Task


@define
class Steps:
    _task_service: TaskService

    def create_task(
        self,
        title: str = "title",
        deadline: datetime | None = None,
        project_id: UUID | None = None,
    ) -> Task:
        if not deadline:
            deadline = datetime.now(timezone.utc) + timedelta(days=1)
        return self._task_service.create(
            title=title, deadline=deadline, project_id=project_id
        )

    def get_by_id(self, id: UUID) -> Task:
        return self._task_service.get_by_id(id)
