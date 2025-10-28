import logging.config

from dependency_injector import containers, providers

from backend.common import LOGGING_CONFIG, EventBus
from backend.common.infrastructure.db import SessionLocal
from backend.task import (
    TaskDeadlineApproachingEvent,
    log_deadline_warning,
    start_task_deadline_scheduler,
)

from .auth.ioc_containers import AuthContainer
from .project.ioc_containers import ProjectsContainer
from .task.ioc_containers import TasksContainer
from .user.ioc_containers import UsersContainer


class ApplicationContainer(containers.DeclarativeContainer):
    __self__ = providers.Self()
    logging = providers.Resource(logging.config.dictConfig, LOGGING_CONFIG)
    session_factory = providers.Singleton(lambda: SessionLocal)

    # Event Bus
    event_bus = providers.Singleton(EventBus)

    # containers
    users = providers.Container(
        UsersContainer,
        session_factory=session_factory,
    )
    auth = providers.Container(
        AuthContainer,
        user_service=users.user_service,
    )
    tasks = providers.Container(
        TasksContainer,
        session_factory=session_factory,
        event_bus=event_bus,
    )
    projects = providers.Container(
        ProjectsContainer,
        session_factory=session_factory,
        task_facade=tasks.task_facade,
    )

    # events
    event_subscribers = providers.Resource(
        lambda bus: bus.subscribe(TaskDeadlineApproachingEvent, log_deadline_warning),
        event_bus,
    )
    task_deadline_scheduler = providers.Resource(
        start_task_deadline_scheduler,
        checker=tasks.task_deadline_checker_service,
        interval_sec=3600,
    )
