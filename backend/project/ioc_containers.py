from dependency_injector import containers, providers
from sqlalchemy.orm import sessionmaker

from backend.task import TaskService

from .src.application.project_servcie import ProjectService
from .src.application.project_validation_service import ProjectValidationService
from .src.infrastructure.project_repository import ProjectTable


class ProjectsContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency(instance_of=sessionmaker)

    task_service = providers.Dependency(instance_of=TaskService)

    project_table = providers.Factory(ProjectTable, session=session_factory)
    project_validation_service = providers.Factory(ProjectValidationService)

    project_service = providers.Factory(
        ProjectService,
        project_table=project_table,
        project_validation_service=project_validation_service,
        task_service=task_service,
    )
