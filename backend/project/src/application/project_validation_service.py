from datetime import datetime
from uuid import UUID

from attrs import define

from backend.common import CommonValidationService
from backend.task import Task, TaskAlreadyCompletedException

from ..domain.exceptions import TaskNotLinkedToProjectException
from ..domain.project import Project


@define
class ProjectValidationService:
    def validate_deadline(self, deadline: datetime) -> None:
        CommonValidationService.validate_deadline(deadline)

    def validate_task_linked_to_project(
        self, task_project_id: UUID | None, project: Project
    ) -> None:
        if not task_project_id or task_project_id != project.id:
            raise TaskNotLinkedToProjectException(
                task_project_id=task_project_id,
                project_title=project.title,
                project_id=project.id,
            )

    def validate_task_completed(self, task: Task) -> None:
        if task.completed:
            raise TaskAlreadyCompletedException(
                task_title=task.title,
                task_id=task.id,
            )
