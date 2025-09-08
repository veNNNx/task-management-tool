from datetime import datetime, timezone
from uuid import UUID

from attrs import define
from sqlalchemy.orm import sessionmaker

from ..domain.project import Project
from .exceptions import ProjectNotFoundException
from .models import ProjectModel


@define
class ProjectTable:
    _session: sessionmaker

    def create_and_save(self, project: Project) -> Project:
        project_model = self._to_model(project)
        with self._session() as db:
            db.add(project_model)
            db.commit()
            db.refresh(project_model)

        return self._to_entity(project_model)

    def update(
        self,
        id: UUID,
        title: str,
        deadline: datetime | None,
        description: str | None,
    ) -> Project:
        with self._session() as db:
            project_model = (
                db.query(ProjectModel).filter(ProjectModel.id == str(id)).first()
            )
            if not project_model:
                raise ProjectNotFoundException(id)
            project_model.title = title
            project_model.description = description
            project_model.deadline = deadline
            project_model.updated_at = datetime.now(timezone.utc)

            db.commit()
            db.refresh(project_model)

        return self._to_entity(project_model)

    def update_at(self, id: UUID) -> Project:
        with self._session() as db:
            project_model = (
                db.query(ProjectModel).filter(ProjectModel.id == str(id)).first()
            )
            if not project_model:
                raise ProjectNotFoundException(id)
            project_model.updated_at = datetime.now(timezone.utc)

            db.commit()
            db.refresh(project_model)

        return self._to_entity(project_model)

    def get_all(self) -> list[Project]:
        with self._session() as db:
            project_models = db.query(ProjectModel).all()
            return [self._to_entity(project_model) for project_model in project_models]

    def get_by_id(self, id: UUID) -> Project:
        with self._session() as db:
            project_model = (
                db.query(ProjectModel).filter(ProjectModel.id == str(id)).first()
            )
            if not project_model:
                raise ProjectNotFoundException(id)

            return self._to_entity(project_model)

    def delete_by_id(self, id: UUID) -> None:
        with self._session() as db:
            project_model = (
                db.query(ProjectModel).filter(ProjectModel.id == str(id)).first()
            )

            if not project_model:
                raise ProjectNotFoundException(id)

            db.delete(project_model)
            db.commit()

    @staticmethod
    def _to_model(project: Project) -> ProjectModel:
        return ProjectModel(
            id=str(project.id),
            title=project.title,
            description=project.description,
            deadline=project.deadline,
            completed=project.completed,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    @staticmethod
    def _to_entity(project_model: ProjectModel) -> Project:
        return Project(
            id=UUID(project_model.id),  # type: ignore[arg-type]
            title=project_model.title,  # type: ignore[arg-type]
            description=project_model.description,  # type: ignore[arg-type]
            deadline=project_model.deadline.replace(tzinfo=timezone.utc),  # type: ignore[arg-type]
            completed=project_model.completed,  # type: ignore[arg-type]
            created_at=project_model.created_at.replace(tzinfo=timezone.utc),  # type: ignore[arg-type]
            updated_at=project_model.updated_at.replace(tzinfo=timezone.utc),  # type: ignore[arg-type]
        )
