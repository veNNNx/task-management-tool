from fastapi import FastAPI, status

from backend.project import (
    ProjectAlreadyCompletedException,
    ProjectNotFoundException,
    TaskNotLinkedToProjectException,
)

from ..utils import register_exception_handler

EXCEPTION_STATUS_CODES = {
    ProjectNotFoundException: status.HTTP_404_NOT_FOUND,
    TaskNotLinkedToProjectException: status.HTTP_409_CONFLICT,
    ProjectAlreadyCompletedException: status.HTTP_409_CONFLICT,
}


def add_project_exception_handlers(app: FastAPI) -> None:
    for exc_class, status_code in EXCEPTION_STATUS_CODES.items():
        register_exception_handler(app, exc_class, status_code)
