import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient
from sqlalchemy.orm import close_all_sessions, sessionmaker

from api.api.app_factory import create_app
from api.api.auth import router as auth_router
from backend.common.infrastructure.base import Base
from backend.common.infrastructure.db_test import test_engine
from backend.ioc_container import ApplicationContainer


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()

    TestSessionMaker = sessionmaker(
        autocommit=False,
        autoflush=False,
    )

    TestSessionMaker.configure(bind=connection)

    session = TestSessionMaker()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
        close_all_sessions()


@pytest.fixture
def test_app_container(db_session):
    container = ApplicationContainer()
    container.init_resources()
    container.wire(packages=["api", "backend", auth_router])

    TestSessionMaker = sessionmaker(autocommit=False, autoflush=False)
    TestSessionMaker.configure(bind=db_session.bind)

    container.session_factory.override(providers.Object(TestSessionMaker))

    try:
        yield container
    finally:
        container.shutdown_resources()
        container.session_factory.reset_override()


@pytest.fixture
def client(test_app_container: ApplicationContainer) -> TestClient:
    test_app = create_app(test_app_container)
    return TestClient(test_app)
