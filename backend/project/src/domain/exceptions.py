from uuid import UUID


class TaskNotLinkedToProjectException(Exception):
    def __init__(
        self, task_project_id: UUID | None, project_title: str, project_id: UUID
    ):
        message = f"Task with id='{task_project_id}' is not linked to project with title='{project_title}' and id='{project_id}'."

        super().__init__(message)


class ProjectAlreadyCompletedException(Exception):
    def __init__(self, project_title: str, project_id: UUID):
        message = f"Project with id='{project_id}' and title='{project_title}' is already completed."

        super().__init__(message)
