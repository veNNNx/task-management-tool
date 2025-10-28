from datetime import datetime, timedelta, timezone
from uuid import UUID

from attrs import define

from backend.task import Task, TaskFacade

from ..src.application.project_servcie import ProjectService
from ..src.domain.project import Project


@define
class Steps:
    _task_facade: TaskFacade
    _project_service: ProjectService

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

    def get_task_by_id(self, id: UUID) -> Task:
        return self._task_facade.get_by_id(id)

    def update_task_by_id(self, id: UUID, title: str, deadline: datetime) -> Task:
        return self._task_facade.update_by_id(id=id, title=title, deadline=deadline)

    def change_task_state(self, task_id: UUID, completed: bool = True) -> None:
        self._task_facade.change_task_state(id=task_id, completed=completed)

    def delete_task_by_id(self, task_id: UUID) -> None:
        self._task_facade.delete_by_id(task_id)

    # project
    def create_project(
        self, title: str = "title", deadline: datetime | None = None
    ) -> Project:
        if not deadline:
            deadline = datetime.now(timezone.utc) + timedelta(days=3)
        return self._project_service.create(title=title, deadline=deadline)

    def get_project_by_id(self, id: UUID) -> Project:
        return self._project_service.get_by_id(id)

    def update_project_by_id(self, id: UUID, title: str, deadline: datetime) -> Project:
        return self._project_service.update_by_id(id=id, title=title, deadline=deadline)

    def link_task_to_project(self, project_id: UUID, task_id: UUID) -> None:
        self._project_service.link_task_to_project(
            project_id=project_id, task_id=task_id
        )

    def create_project_with_linked_task(self) -> tuple[Project, Task]:
        task = self.create_task()
        project = self.create_project()
        self.link_task_to_project(project_id=project.id, task_id=task.id)
        task_linked = self.get_task_by_id(task.id)
        project_linked = self.get_project_by_id(project.id)
        return project_linked, task_linked
