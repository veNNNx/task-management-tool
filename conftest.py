import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient
from sqlalchemy import text

from api.api.app_factory import create_app
from api.api.auth import router as auth_router
from backend.common import Tables
from backend.common.infrastructure.base import Base
from backend.common.infrastructure.db_test import TestingSessionLocal, test_engine
from backend.ioc_container import ApplicationContainer


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)

    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="session")
def test_app_container():
    container = ApplicationContainer()
    container.init_resources()
    container.wire(packages=["api", "backend", auth_router])

    container.session_factory.override(providers.Singleton(lambda: TestingSessionLocal))

    yield container

    container.shutdown_resources()
    container.session_factory.reset_override()


@pytest.fixture(scope="session")
def client(test_app_container: ApplicationContainer) -> TestClient:
    test_app = create_app(test_app_container)
    return TestClient(test_app)


@pytest.fixture(autouse=True)
def clean_db_after_test():
    yield
    with test_engine.connect() as conn:
        for table in Tables:
            conn.execute(text(f"DELETE FROM {table.value}"))
        conn.commit()
