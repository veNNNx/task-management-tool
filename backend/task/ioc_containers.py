from dependency_injector import containers, providers
from sqlalchemy.orm import sessionmaker

from backend.common import EventBus

from .src.application.task_deadline_checker_service import TaskDeadlineCheckerService
from .src.application.task_service import TaskService
from .src.application.task_validation_service import TaskValidationService
from .src.infrastructure.task_repository import TaskTable


class TasksContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency(instance_of=sessionmaker)
    task_table = providers.Factory(TaskTable, session=session_factory)
    task_validation_service = providers.Factory(TaskValidationService)
    event_bus = providers.Dependency(instance_of=EventBus)

    task_service = providers.Factory(
        TaskService,
        task_table=task_table,
        task_validation_service=task_validation_service,
    )

    task_deadline_checker_service = providers.Factory(
        TaskDeadlineCheckerService,
        task_table=task_table,
        event_bus=event_bus,
    )
