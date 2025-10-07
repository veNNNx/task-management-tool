import logging
from datetime import datetime, timedelta, timezone
from typing import cast

import jwt
from attrs import define, field
from jwt.exceptions import InvalidTokenError

from backend.user import UnauthenticatedUserException, User, UserService

from ..domain.auth_data import ALGORITHM, SECRET_KEY
from ..domain.token import TokenData


@define
class AuthService:
    logger: logging.Logger = field(init=False)
    _user_service: UserService

    def __attrs_post_init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    def authenticate_user(self, email: str, password: str) -> User:
        user = self._user_service.get_by_email(email)
        user.check_password(password)
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email is None:
                raise UnauthenticatedUserException
            token_data = TokenData(email=email)
        except InvalidTokenError:
            raise UnauthenticatedUserException
        user = self._user_service.get_by_email(email=cast(str, token_data.email))
        if user is None:
            raise UnauthenticatedUserException
        return user
