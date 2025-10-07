from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from backend.user import UnauthenticatedUserException


def add_auth_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UnauthenticatedUserException)
    async def unauthenticated_user_exception_handler(
        _request: Request, _exc: UnauthenticatedUserException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Incorrect email or password"},
            headers={"WWW-Authenticate": "Bearer"},
        )
