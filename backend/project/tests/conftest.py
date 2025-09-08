import pytest

from backend.ioc_container import ApplicationContainer

from ..src.application.project_servcie import ProjectService
from .steps import Steps


@pytest.fixture
def project_service(test_app_container: ApplicationContainer) -> ProjectService:
    return test_app_container.projects().project_service()


@pytest.fixture
def steps(test_app_container: ApplicationContainer) -> Steps:
    return Steps(
        task_service=test_app_container.tasks().task_service(),
        project_service=test_app_container.projects().project_service(),
    )
