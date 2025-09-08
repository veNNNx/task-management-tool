from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def register_exception_handler(
    app: FastAPI, exc_class: type[Exception], status_code: int
) -> None:
    @app.exception_handler(exc_class)
    async def handle_exception(_request: Request, exc: type[Exception]) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={"message": exc.args[0]},
        )
