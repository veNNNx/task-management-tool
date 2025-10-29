from fastapi import FastAPI, status

from backend.user import (
    UserByEmailNotFoundException,
    UserByIdNotFoundException,
    UserWithEmailAlreadyExistsException,
)

from ..utils import register_exception_handler

EXCEPTION_STATUS_CODES = {
    UserWithEmailAlreadyExistsException: status.HTTP_409_CONFLICT,
    UserByEmailNotFoundException: status.HTTP_404_NOT_FOUND,
    UserByIdNotFoundException: status.HTTP_404_NOT_FOUND,
}


def add_user_exception_handlers(app: FastAPI) -> None:
    for exc_class, status_code in EXCEPTION_STATUS_CODES.items():
        register_exception_handler(app, exc_class, status_code)
