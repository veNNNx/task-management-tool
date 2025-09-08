import logging
from datetime import datetime
from uuid import UUID

from attrs import define, field

from ..domain.task import Task
from ..infrastructure.task_repository import TaskTable
from .task_validation_service import TaskValidationService


@define
class TaskService:
    logger: logging.Logger = field(init=False)
    _task_tabel: TaskTable
    _task_validation_service: TaskValidationService

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
        self._task_validation_service.validate_deadline(deadline)
        task = Task(
            id=Task.new_uuid(),
            title=title,
            description=description,
            deadline=deadline,
            project_id=project_id,
        )
        self.logger.debug("Adding new task with title: %s", title)

        return self._task_tabel.create_and_save(task)

    def link_task_to_project(
        self, project_id: UUID, project_deadline: datetime, task_id: UUID
    ) -> None:
        self._task_tabel.link_task_to_project(
            project_id=project_id, project_deadline=project_deadline, task_id=task_id
        )

    def unlink_task_from_project(self, task_id: UUID) -> None:
        self._task_tabel.unlink_task_from_project(task_id=task_id)

    def get_all_tasks_by_project_id(self, id: UUID) -> list[Task]:
        return self._task_tabel.get_all_tasks_by_project_id(id=id)

    def get_all(self) -> list[Task]:
        return self._task_tabel.get_all()

    def get_by_id(self, id: UUID) -> Task:
        return self._task_tabel.get_by_id(id)

    def update_by_id(
        self,
        id: UUID,
        title: str,
        deadline: datetime,
        description: str | None = None,
    ) -> Task:
        task = self._task_tabel.get_by_id(id)
        if task.deadline != deadline:
            self._task_validation_service.validate_deadline(deadline)

        self.logger.debug("Updating task with title: %s", title)
        return self._task_tabel.update(
            task_id=id,
            title=title,
            deadline=deadline,
            description=description,
        )

    def change_task_state(self, id: UUID, completed: bool) -> Task:
        task = self._task_tabel.get_by_id(id)
        self._task_validation_service.validate_task_state(task, completed)
        self.logger.debug(
            "Changing task with title: %s state to %s.", task.title, completed
        )
        return self._task_tabel.change_completed_state(task_id=id, completed=completed)

    def delete_by_id(self, id: UUID) -> None:
        task = self._task_tabel.get_by_id(id)
        self.logger.debug("Delete the task with title: %s", task.title)
        self._task_tabel.delete_by_id(id)
