import logging
from uuid import UUID

from attrs import define, field
from sqlalchemy.orm import sessionmaker

from ..domain.user import User
from .exceptions import UserByEmailNotFoundException, UserByIdNotFoundException
from .models import UserModel


@define
class UserTable:
    logger: logging.Logger = field(init=False)
    _session: sessionmaker

    def __attrs_post_init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    def create_and_save(self, user: User) -> User:
        user_model = self._to_model(user)
        with self._session() as db:
            db.add(user_model)
            db.commit()
            db.refresh(user_model)

        return self._to_entity(user_model)

    def get_all(self) -> list[User]:
        with self._session() as db:
            user_models = db.query(UserModel).all()
        return [self._to_entity(user_model) for user_model in user_models]

    def get_by_email(self, user_email: str) -> User:
        with self._session() as db:
            user_model = (
                db.query(UserModel).filter(UserModel.email == user_email).first()
            )
        if not user_model:
            raise UserByEmailNotFoundException(user_email)
        return self._to_entity(user_model)

    def get_by_id(self, user_id: UUID) -> User:
        with self._session() as db:
            user_model = (
                db.query(UserModel).filter(UserModel.id == str(user_id)).first()
            )
        if not user_model:
            raise UserByIdNotFoundException(user_id)
        return self._to_entity(user_model)

    def check_if_exist_by_email(self, user_email: str) -> bool:
        with self._session() as db:
            user_model = (
                db.query(UserModel).filter(UserModel.email == user_email).first()
            )
        return bool(user_model)

    def delete_by_email(self, user_email: str) -> None:
        with self._session() as db:
            user_model = (
                db.query(UserModel).filter(UserModel.email == user_email).first()
            )
            if not user_model:
                raise UserByEmailNotFoundException(user_email)
            db.delete(user_model)
            db.commit()

    @staticmethod
    def _to_model(user: User) -> UserModel:
        return UserModel(
            id=str(user.id),
            email=user.email,
            name=user.name,
            hashed_password=user.hashed_password,
        )

    @staticmethod
    def _to_entity(user_model: UserModel) -> User:
        return User(
            id=UUID(user_model.id),  # type: ignore[arg-type]
            email=user_model.email,  # type: ignore[arg-type]
            name=user_model.name,  # type: ignore[arg-type]
            hashed_password=user_model.hashed_password,  # type: ignore[arg-type]
        )
