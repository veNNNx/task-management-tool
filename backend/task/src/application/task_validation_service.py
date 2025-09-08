from datetime import datetime

from attrs import define

from backend.common import CommonValidationService

from ..domain.exceptions import TaskWrongStateException
from ..domain.task import Task


@define
class TaskValidationService:
    def validate_deadline(self, deadline: datetime) -> None:
        CommonValidationService.validate_deadline(deadline)

    def validate_task_state(self, task: Task, completed: bool) -> None:
        if task.completed == completed:
            raise TaskWrongStateException(
                title=task.title, current_state=task.completed
            )
