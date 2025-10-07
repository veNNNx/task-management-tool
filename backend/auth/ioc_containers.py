from dependency_injector import containers, providers
from sqlalchemy.orm import sessionmaker

from backend.user import UserService

from .src.application.auth_service import AuthService


class AuthContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency(instance_of=sessionmaker)
    user_service = providers.Dependency(instance_of=UserService)

    auth_service = providers.Factory(
        AuthService,
        user_service=user_service,
    )
