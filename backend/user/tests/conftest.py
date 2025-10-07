import pytest

from backend.ioc_container import ApplicationContainer
from backend.user import UserService


@pytest.fixture
def user_service(test_app_container: ApplicationContainer) -> UserService:
    return test_app_container.users().user_service()


@pytest.fixture
def user_data() -> dict[str, str]:
    return {"email": "example@gmail.com", "name": "example", "password": "password"}
