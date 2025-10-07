from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from backend.ioc_container import ApplicationContainer
from backend.user import User, UserService

from .schema import UserIn, UserOut

router = APIRouter(prefix="/users", tags=["Users"])


# POST
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user.",
    response_model=UserOut,
    responses={
        status.HTTP_409_CONFLICT: {"description": "Email is already taken."},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Email validation failed."
        },
    },
)
@inject
def register(
    payload: UserIn,
    user_service: Annotated[
        UserService,
        Depends(Provide[ApplicationContainer.users.container.user_service]),
    ],
) -> User:
    return user_service.create(
        email=payload.email,
        name=payload.name,
        password=payload.password,
    )
