import logging

from attrs import define, field

from ..domain.user import User
from ..infrastructure.exceptions import UserWithEmailAlreadyExistsException
from ..infrastructure.user_repository import UserTable


@define
class UserService:
    logger: logging.Logger = field(init=False)
    _user_table: UserTable

    def __attrs_post_init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    def create(
        self,
        email: str,
        name: str,
        password: str,
    ) -> User:
        if self._user_table.check_if_exist_by_email(email):
            raise UserWithEmailAlreadyExistsException(email)

        hashed_password = User.hash_password(password)
        user = User(
            id=User.new_uuid(), email=email, name=name, hashed_password=hashed_password
        )
        self.logger.debug("Adding new user with email: %s", email)

        return self._user_table.create_and_save(user)

    def get_all(self) -> list[User]:
        return self._user_table.get_all()

    def get_by_email(self, email: str) -> User:
        return self._user_table.get_by_email(email)

    def delete_by_id(self, email: str) -> None:
        user = self._user_table.get_by_email(email)
        self.logger.debug("Delete the user with email: %s", user.email)
        self._user_table.delete_by_email(email)
