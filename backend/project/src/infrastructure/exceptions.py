from uuid import UUID


class ProjectNotFoundException(Exception):
    def __init__(self, id: UUID):
        message = f"No task with {id=} exists in the store!"

        super().__init__(message)
