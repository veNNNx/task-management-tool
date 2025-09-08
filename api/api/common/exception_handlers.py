from fastapi import FastAPI, status

from backend.common import InvalidDeadlineException

from ..utils import register_exception_handler

EXCEPTION_STATUS_CODES = {
    InvalidDeadlineException: status.HTTP_409_CONFLICT,
}


def add_common_exception_handlers(app: FastAPI) -> None:
    for exc_class, status_code in EXCEPTION_STATUS_CODES.items():
        register_exception_handler(app, exc_class, status_code)
