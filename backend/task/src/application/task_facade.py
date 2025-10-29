import logging
from datetime import datetime
from uuid import UUID

from attrs import define, field

from backend.user import UserService

from ..domain.task import Task
from .task_service import TaskService


@define
class TaskFacade:
    _task_service: TaskService
    _user_service: UserService
    logger: logging.Logger = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    def create(
        self,
        title: str,
        deadline: datetime,
        description: str | None = None,
        project_id: None | UUID = None,
    ) -> Task:
        return self._task_service.create(
            title=title,
            deadline=deadline,
            description=description,
            project_id=project_id,
        )

    def link_task_to_project(
        self, project_id: UUID, project_deadline: datetime, task_id: UUID
    ) -> None:
        self._task_service.link_task_to_project(
            project_id=project_id, project_deadline=project_deadline, task_id=task_id
        )

    def unlink_task_from_project(self, task_id: UUID) -> None:
        self._task_service.unlink_task_from_project(task_id=task_id)

    def get_tasks_by_user_id(self, user_id: UUID) -> list[Task]:
        self._user_service.get_by_id(id=user_id)
        return self._task_service.get_tasks_by_user_id(user_id=user_id)

    def assign_task_to_user(self, task_id: UUID, user_id: UUID) -> None:
        self._user_service.get_by_id(id=user_id)
        self._task_service.assign_task_to_user(task_id=task_id, user_id=user_id)

    def unassign_task(self, task_id: UUID) -> None:
        self._task_service.unassign_task(task_id=task_id)

    def get_all_tasks_by_project_id(self, id: UUID) -> list[Task]:
        return self._task_service.get_all_tasks_by_project_id(id=id)

    def get_all(self) -> list[Task]:
        return self._task_service.get_all()

    def get_by_id(self, id: UUID) -> Task:
        return self._task_service.get_by_id(id)

    def update_by_id(
        self,
        id: UUID,
        title: str,
        deadline: datetime,
        description: str | None = None,
    ) -> Task:
        return self._task_service.update_by_id(
            id=id,
            title=title,
            deadline=deadline,
            description=description,
        )

    def change_task_state(self, id: UUID, completed: bool) -> Task:
        return self._task_service.change_task_state(id=id, completed=completed)

    def delete_by_id(self, id: UUID) -> None:
        self._task_service.delete_by_id(id)
