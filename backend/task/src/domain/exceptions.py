from datetime import datetime
from uuid import UUID


class TaskNotFoundException(Exception):
    def __init__(self, id: UUID):
        message = f"No task with {id=} exists in the store!"

        super().__init__(message)


class TaskWrongStateException(Exception):
    def __init__(self, title: str, current_state: bool):
        message = f"Task with title='{title}' is already in state {current_state}."

        super().__init__(message)


class TaskDeadlineExceededException(Exception):
    def __init__(
        self, task_title: str, task_deadline: datetime, project_deadline: datetime
    ):
        message = f"Task {task_title} deadline {task_deadline} exceeds project deadline {project_deadline}"

        super().__init__(message)


class TaskAlreadyCompletedException(Exception):
    def __init__(self, task_title: str, task_id: UUID):
        message = (
            f"Task with id='{task_id}' and title='{task_title}' is already completed."
        )

        super().__init__(message)
