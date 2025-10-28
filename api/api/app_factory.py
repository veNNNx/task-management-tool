from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from backend.common.infrastructure.base import Base
from backend.common.infrastructure.db import database, engine
from backend.ioc_container import ApplicationContainer

from .auth.exception_handlers import add_auth_exception_handlers
from .auth.router import router as router_auth
from .common.exception_handlers import add_common_exception_handlers
from .project.exception_handlers import add_project_exception_handlers
from .project.router import router as router_projects
from .task.exception_handlers import add_task_exception_handlers
from .task.router import router as router_tasks
from .user.exception_handlers import add_user_exception_handlers
from .user.router import router as router_users


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

    add_pagination(app)

    app.state.container = container

    Base.metadata.create_all(engine)

    app.include_router(router_auth)
    app.include_router(router_users)
    app.include_router(router_tasks)
    app.include_router(router_projects)
    add_auth_exception_handlers(app)
    add_user_exception_handlers(app)
    add_common_exception_handlers(app)
    add_task_exception_handlers(app)
    add_project_exception_handlers(app)

    return app
