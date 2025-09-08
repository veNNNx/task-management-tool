import pytest

from backend.ioc_container import ApplicationContainer

from ..src.application.task_service import TaskService
from ..src.infrastructure.scheduler import start_task_deadline_scheduler
from .steps import Steps


@pytest.fixture
def task_service(test_app_container: ApplicationContainer) -> TaskService:
    return test_app_container.tasks().task_service()


@pytest.fixture
def steps(test_app_container: ApplicationContainer) -> Steps:
    return Steps(task_service=test_app_container.tasks().task_service())


@pytest.fixture
def task_deadline_scheduler(test_app_container: ApplicationContainer):
    checker = test_app_container.tasks().task_deadline_checker_service()
    thread, stop_event = start_task_deadline_scheduler(checker, interval_sec=1)
    try:
        yield thread
    finally:
        stop_event.set()
        thread.join()
