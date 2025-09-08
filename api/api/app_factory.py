from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from backend.common.infrastructure.base import Base
from backend.common.infrastructure.db import database, engine
from backend.ioc_container import ApplicationContainer

from .common.exception_handlers import add_common_exception_handlers
from .project.exception_handlers import add_project_exception_handlers
from .project.router import router as router_projects
from .task.exception_handlers import add_task_exception_handlers
from .task.router import router as router_tasks


@asynccontextmanager
async def lifespan(_fast_api_app: FastAPI) -> AsyncIterator[None]:
    await database.connect()
    yield
    await database.disconnect()


def create_app(container: ApplicationContainer) -> FastAPI:
    app = FastAPI(
        version="0.0.1",
        title="WebAPI",
        lifespan=lifespan,
    )
    app.state.container = container

    Base.metadata.create_all(engine)

    app.include_router(router_tasks)
    app.include_router(router_projects)
    add_common_exception_handlers(app)
    add_task_exception_handlers(app)
    add_project_exception_handlers(app)

    return app
