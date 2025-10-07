from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from backend.ioc_container import ApplicationContainer
from backend.project import Project, ProjectService
from backend.task import Task

from ..auth.router import verify_user
from ..task.schema import TaskOut
from .schema import ProjectIn, ProjectOut

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Depends(verify_user)],
)


# POST
@router.post(
    "/",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project.",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Deadline cannot be earlier than now."
        },
    },
)
@inject
def create(
    payload: ProjectIn,
    project_service: Annotated[
        ProjectService,
        Depends(Provide[ApplicationContainer.projects.container.project_service]),
    ],
) -> Project:
    return project_service.create(
        title=payload.title,
        deadline=payload.deadline,
        description=payload.description,
    )


@router.post(
    "{project_id}/tasks/{task_id}/link",
    status_code=status.HTTP_200_OK,
    summary="Link a task to a project.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Requested project or task does not exist."
        },
    },
)
@inject
def link_task_to_project(
    project_id: UUID,
    task_id: UUID,
    project_service: Annotated[
        ProjectService,
        Depends(Provide[ApplicationContainer.projects.container.project_service]),
    ],
) -> None:
    project_service.link_task_to_project(project_id=project_id, task_id=task_id)


# GET
@router.get(
    "/",
    response_model=list[ProjectOut],
    status_code=status.HTTP_200_OK,
    summary="Retrieve a list of all projects",
)
@inject
def get_all(
    project_service: Annotated[
        ProjectService,
        Depends(Provide[ApplicationContainer.projects.container.project_service]),
    ],
) -> list[Project]:
    return project_service.get_all()


@router.get(
    "/{id}",
    response_model=ProjectOut,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single project by ID.",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Requested project does not exist."},
    },
)
@inject
def get_by_id(
    id: UUID,
    project_service: Annotated[
        ProjectService,
        Depends(Provide[ApplicationContainer.projects.container.project_service]),
    ],
) -> Project:
    return project_service.get_by_id(id)


@router.get(
    "/{id}/tasks",
    response_model=list[TaskOut],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all tasks associated with a project.",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Requested project does not exist."},
    },
)
@inject
def get_all_tasks_by_project_id(
    id: UUID,
    project_service: Annotated[
        ProjectService,
        Depends(Provide[ApplicationContainer.projects.container.project_service]),
    ],
) -> list[Task]:
    return project_service.get_all_tasks_by_project_id(id)


# PUT
@router.put(
    "/{id}",
    response_model=ProjectOut,
    status_code=status.HTTP_200_OK,
    summary="Update an existing project.",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Requested project does not exist."},
    },
)
@inject
def update_by_id(
    id: UUID,
    payload: ProjectIn,
    project_service: Annotated[
        ProjectService,
        Depends(Provide[ApplicationContainer.projects.container.project_service]),
    ],
) -> Project:
    return project_service.update_by_id(
        id=id,
        title=payload.title,
        deadline=payload.deadline,
        description=payload.description,
    )


# DELETE
@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete the project by id.",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Requested project does not exist."},
    },
)
@inject
def delete_by_id(
    id: UUID,
    project_service: Annotated[
        ProjectService,
        Depends(Provide[ApplicationContainer.projects.container.project_service]),
    ],
) -> None:
    project_service.delete_by_id(id)


@router.delete(
    "{project_id}/tasks/{task_id}/unlink",
    status_code=status.HTTP_200_OK,
    summary="Unlink a task from a project.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Requested project or task does not exist."
        },
        status.HTTP_409_CONFLICT: {
            "description": "Requested task is not linked to this project"
        },
    },
)
@inject
def unlink_task_from_project(
    project_id: UUID,
    task_id: UUID,
    project_service: Annotated[
        ProjectService,
        Depends(Provide[ApplicationContainer.projects.container.project_service]),
    ],
) -> None:
    project_service.unlink_task_from_project(project_id=project_id, task_id=task_id)
