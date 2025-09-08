from fastapi import FastAPI, status

from backend.task import (
    InvalidProjectIdException,
    TaskAlreadyCompletedException,
    TaskDeadlineExceededException,
    TaskNotFoundException,
    TaskWrongStateException,
)

from ..utils import register_exception_handler

EXCEPTION_STATUS_CODES = {
    TaskNotFoundException: status.HTTP_404_NOT_FOUND,
    TaskWrongStateException: status.HTTP_400_BAD_REQUEST,
    TaskDeadlineExceededException: status.HTTP_422_UNPROCESSABLE_ENTITY,
    TaskAlreadyCompletedException: status.HTTP_409_CONFLICT,
    InvalidProjectIdException: status.HTTP_404_NOT_FOUND,
}


def add_task_exception_handlers(app: FastAPI) -> None:
    for exc_class, status_code in EXCEPTION_STATUS_CODES.items():
        register_exception_handler(app, exc_class, status_code)
