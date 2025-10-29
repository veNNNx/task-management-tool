from datetime import datetime, timedelta, timezone
from uuid import UUID

from attrs import define

from ..src.application.task_facade import TaskFacade
from ..src.domain.task import Task


@define
class Steps:
    _task_facade: TaskFacade

    def create_task(
        self,
        title: str = "title",
        deadline: datetime | None = None,
        project_id: UUID | None = None,
    ) -> Task:
        if not deadline:
            deadline = datetime.now(timezone.utc) + timedelta(days=1)
        return self._task_facade.create(
            title=title, deadline=deadline, project_id=project_id
        )

    def get_by_id(self, id: UUID) -> Task:
        return self._task_facade.get_by_id(id)

    def create_user(self, name: str = "user") -> UUID:
        email = f"{name}@example.com"
        user = self._task_facade._user_service.create(
            email=email, name=name, password=name
        )
        return user.id
