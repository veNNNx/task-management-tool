import logging
from datetime import datetime
from uuid import UUID

from attrs import define, field

from backend.task import Task, TaskService

from ..domain.project import Project
from ..infrastructure.project_repository import ProjectTable
from .project_validation_service import ProjectValidationService


@define
class ProjectService:
    logger: logging.Logger = field(init=False)
    _project_tabel: ProjectTable
    _project_validation_service: ProjectValidationService
    _task_service: TaskService

    def __attrs_post_init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    def create(
        self,
        title: str,
        deadline: datetime,
        description: str | None = None,
    ) -> Project:
        self._project_validation_service.validate_deadline(deadline)
        project = Project(
            id=Project.new_uuid(),
            title=title,
            description=description,
            deadline=deadline,
        )
        self.logger.debug("Adding new project with title: %s", title)

        return self._project_tabel.create_and_save(project)

    def link_task_to_project(self, project_id: UUID, task_id: UUID) -> None:
        task = self._task_service.get_by_id(task_id)
        project = self.get_by_id(project_id)
        project.validate_project_completed()
        self._project_validation_service.validate_task_completed(task)

        self.logger.debug(
            "Linking task with id: %s to project with id: %s",
            task_id,
            project_id,
        )
        self._task_service.link_task_to_project(
            project_id=project_id, project_deadline=project.deadline, task_id=task_id
        )
        project = self._project_tabel.update_at(project_id)

    def unlink_task_from_project(self, project_id: UUID, task_id: UUID) -> None:
        project = self.get_by_id(project_id)
        task = self._task_service.get_by_id(task_id)
        self._project_validation_service.validate_task_linked_to_project(
            task_project_id=task.project_id, project=project
        )
        self._project_validation_service.validate_task_completed(task)
        self.logger.debug(
            "Unlinking task with id: %s from project with id: %s",
            task_id,
            project_id,
        )

        self._task_service.unlink_task_from_project(task_id=task_id)
        self._project_tabel.update_at(project_id)

    def get_all(self) -> list[Project]:
        return self._project_tabel.get_all()

    def get_by_id(self, id: UUID) -> Project:
        return self._project_tabel.get_by_id(id)

    def get_all_tasks_by_project_id(self, id: UUID) -> list[Task]:
        self._project_tabel.get_by_id(id)
        return self._task_service.get_all_tasks_by_project_id(id=id)

    def update_by_id(
        self,
        id: UUID,
        title: str,
        deadline: datetime,
        description: str | None = None,
    ) -> Project:
        project = self._project_tabel.get_by_id(id)
        if project.deadline != deadline:
            self._project_validation_service.validate_deadline(deadline)

        self.logger.debug("Updating project with title: %s", title)
        return self._project_tabel.update(
            id=id,
            title=title,
            deadline=deadline,
            description=description,
        )

    def delete_by_id(self, id: UUID) -> None:
        project = self._project_tabel.get_by_id(id)
        self.logger.debug("Delete the project with title: %s", project.title)
        self._project_tabel.delete_by_id(id)
