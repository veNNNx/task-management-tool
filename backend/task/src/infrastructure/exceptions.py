from uuid import UUID


class TaskNotFoundException(Exception):
    def __init__(self, id: UUID):
        message = f"No task with {id=} exists in the store!"

        super().__init__(message)


class InvalidProjectIdException(Exception):
    def __init__(self, id: UUID):
        message = f"No preoject with {id=} exists in the store!"

        super().__init__(message)
