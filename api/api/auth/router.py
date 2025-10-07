from datetime import timedelta
from typing import Annotated, Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.auth import AuthService
from backend.ioc_container import ApplicationContainer

from ..user.schema import UserOut
from .schema import Token

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/token")
@inject
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[
        AuthService,
        Depends(Provide[ApplicationContainer.auth.container.auth_service]),
    ],
) -> Token:
    user = auth_service.authenticate_user(
        email=form_data.username, password=form_data.password
    )
    access_token_expires = timedelta(minutes=1440)
    access_token = auth_service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get my user information",
    response_model=UserOut,
)
@inject
async def verify_user(
    auth_service: Annotated[
        AuthService,
        Depends(Provide[ApplicationContainer.auth.container.auth_service]),
    ],
    token: str = Depends(oauth2_scheme),
) -> Any:
    return await auth_service.get_current_user(token)
