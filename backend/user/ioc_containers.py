from dependency_injector import containers, providers
from sqlalchemy.orm import sessionmaker

from .src.application.user_service import UserService
from .src.infrastructure.user_repository import UserTable


class UsersContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency(instance_of=sessionmaker)
    user_table = providers.Factory(UserTable, session=session_factory)

    user_service = providers.Factory(
        UserService,
        user_table=user_table,
    )
