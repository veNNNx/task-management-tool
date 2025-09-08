from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from backend.ioc_container import ApplicationContainer
from backend.task import Task, TaskService

from .schema import TaskIn, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# POST
@router.post(
    "/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task.",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Deadline cannot be earlier than now."
        },
    },
)
@inject
def create(
    payload: TaskIn,
    task_service: Annotated[
        TaskService,
        Depends(Provide[ApplicationContainer.tasks.container.task_service]),
    ],
) -> Task:
    return task_service.create(
        title=payload.title,
        deadline=payload.deadline,
        description=payload.description,
        project_id=payload.project_id,
    )


# GET
@router.get(
    "/",
    response_model=list[TaskOut],
    status_code=status.HTTP_200_OK,
    summary="Retrieve a list of all tasks.",
)
@inject
def get_all(
    task_service: Annotated[
        TaskService,
        Depends(Provide[ApplicationContainer.tasks.container.task_service]),
    ],
) -> list[Task]:
    return task_service.get_all()


@router.get(
    "/{id}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single task by ID.",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Requested task does not exist."},
    },
)
@inject
def get_by_id(
    id: UUID,
    task_service: Annotated[
        TaskService,
        Depends(Provide[ApplicationContainer.tasks.container.task_service]),
    ],
) -> Task:
    return task_service.get_by_id(id)


# PUT
@router.put(
    "/{id}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
    summary="Update an existing task.",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Requested task does not exist."},
    },
)
@inject
def update_by_id(
    id: UUID,
    payload: TaskUpdate,
    task_service: Annotated[
        TaskService,
        Depends(Provide[ApplicationContainer.tasks.container.task_service]),
    ],
) -> Task:
    return task_service.update_by_id(
        id=id,
        title=payload.title,
        deadline=payload.deadline,
        description=payload.description,
    )


# PATCH
@router.patch(
    "/{id}/complete",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
    summary="Mark a task as completed.",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Requested task does not exist."},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Requested task is already completed."
        },
    },
)
@inject
def mark_as_completed(
    id: UUID,
    task_service: Annotated[
        TaskService,
        Depends(Provide[ApplicationContainer.tasks.container.task_service]),
    ],
) -> Task:
    return task_service.change_task_state(id=id, completed=True)


@router.patch(
    "/{id}/uncomplete",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
    summary="Mark a task as uncompleted.",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Requested task does not exist."},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Requested task is already uncompleted."
        },
    },
)
@inject
def mark_as_uncompleted(
    id: UUID,
    task_service: Annotated[
        TaskService,
        Depends(Provide[ApplicationContainer.tasks.container.task_service]),
    ],
) -> Task:
    return task_service.change_task_state(id=id, completed=False)


# DELETE
@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task.",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Requested task does not exist."},
    },
)
@inject
def delete_by_id(
    id: UUID,
    task_service: Annotated[
        TaskService,
        Depends(Provide[ApplicationContainer.tasks.container.task_service]),
    ],
) -> None:
    task_service.delete_by_id(id)
