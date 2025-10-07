from uuid import UUID

from attrs import define
from bcrypt import checkpw, gensalt, hashpw

from backend.common import Entity

from .exceptions import UnauthenticatedUserException


@define(kw_only=True)
class User(Entity):
    id: UUID
    email: str
    name: str
    hashed_password: str

    @staticmethod
    def hash_password(password: str) -> str:
        return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

    def check_password(self, plain_password: str) -> bool:
        try:
            return checkpw(
                plain_password.encode("utf-8"), self.hashed_password.encode("utf-8")
            )
        except ValueError:
            raise UnauthenticatedUserException
