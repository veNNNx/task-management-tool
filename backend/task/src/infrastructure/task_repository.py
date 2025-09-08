import logging
from datetime import datetime, timezone
from uuid import UUID

from attrs import define, field
from sqlalchemy.orm import sessionmaker

from ..domain.task import Task
from .exceptions import TaskNotFoundException
from .models import TaskModel


@define
class TaskTable:
    logger: logging.Logger = field(init=False)
    _session: sessionmaker

    def __attrs_post_init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    def create_and_save(self, task: Task) -> Task:
        task_model = self._to_model(task)
        with self._session() as db:
            db.add(task_model)
            db.commit()
            db.refresh(task_model)

        return self._to_entity(task_model)

    def update(
        self,
        task_id: UUID,
        title: str,
        deadline: datetime | None,
        description: str | None,
    ) -> Task:
        with self._session() as db:
            task_model = (
                db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
            )
            if not task_model:
                raise TaskNotFoundException(task_id)

            task_model.title = title
            task_model.description = description
            task_model.deadline = deadline
            task_model.updated_at = datetime.now(timezone.utc)

            db.commit()
            db.refresh(task_model)

        return self._to_entity(task_model)

    def link_task_to_project(
        self, project_id: UUID, project_deadline: datetime, task_id: UUID
    ) -> None:
        with self._session() as db:
            task_model = (
                db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
            )
            if not task_model:
                raise TaskNotFoundException(task_id)

            task_deadline_utc = task_model.deadline
            if task_deadline_utc and task_deadline_utc.tzinfo is None:
                task_deadline_utc = task_deadline_utc.replace(tzinfo=timezone.utc)

            project_deadline_utc = project_deadline
            if project_deadline_utc.tzinfo is None:
                project_deadline_utc = project_deadline_utc.replace(tzinfo=timezone.utc)

            if task_deadline_utc and task_deadline_utc > project_deadline_utc:
                self.logger.debug(
                    "Changing task with id %s and title %s deadline from %s to assigned project deadline: %s",
                    task_model.id,
                    task_model.title,
                    task_deadline_utc,
                    project_deadline_utc,
                )
                task_model.deadline = project_deadline_utc

            task_model.project_id = str(project_id)
            task_model.updated_at = datetime.now(timezone.utc)

            db.commit()
            db.refresh(task_model)

    def unlink_task_from_project(self, task_id: UUID) -> None:
        with self._session() as db:
            task_model = (
                db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
            )
            if not task_model:
                raise TaskNotFoundException(task_id)

            task_model.project_id = None
            task_model.updated_at = datetime.now(timezone.utc)

            db.commit()
            db.refresh(task_model)

    def change_completed_state(self, task_id: UUID, completed: bool) -> Task:
        with self._session() as db:
            task_model = (
                db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
            )
            if not task_model:
                raise TaskNotFoundException(task_id)
            task_model.completed = completed
            task_model.updated_at = datetime.now(timezone.utc)

            db.commit()
            db.refresh(task_model)

        return self._to_entity(task_model)

    def get_all(self) -> list[Task]:
        with self._session() as db:
            task_models = db.query(TaskModel).all()
        return [self._to_entity(task_model) for task_model in task_models]

    def get_by_id(self, task_id: UUID) -> Task:
        with self._session() as db:
            task_model = (
                db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
            )
            if not task_model:
                raise TaskNotFoundException(task_id)

            return self._to_entity(task_model)

    def get_all_tasks_by_project_id(self, id: UUID) -> list[Task]:
        with self._session() as db:
            task_models = db.query(TaskModel).filter(TaskModel.project_id == str(id))
        return [self._to_entity(task_model) for task_model in task_models]

    def get_tasks_with_deadline_between(
        self, start: datetime, end: datetime
    ) -> list[TaskModel]:
        with self._session() as db:
            result = (
                db.query(TaskModel)
                .filter(TaskModel.deadline >= start)
                .filter(TaskModel.deadline <= end)
                .all()
            )
        return result

    def delete_by_id(self, id: UUID) -> None:
        with self._session() as db:
            task_model = db.query(TaskModel).filter(TaskModel.id == str(id)).first()

            if not task_model:
                raise TaskNotFoundException(id)

            db.delete(task_model)
            db.commit()

    @staticmethod
    def _to_model(task: Task) -> TaskModel:
        return TaskModel(
            id=str(task.id),
            title=task.title,
            description=task.description,
            deadline=task.deadline,
            completed=task.completed,
            project_id=str(task.project_id) if task.project_id else None,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    @staticmethod
    def _to_entity(task_model: TaskModel) -> Task:
        return Task(
            id=UUID(task_model.id),  # type: ignore[arg-type]
            title=task_model.title,  # type: ignore[arg-type]
            description=task_model.description,  # type: ignore[arg-type]
            deadline=task_model.deadline.replace(tzinfo=timezone.utc),  # type: ignore[arg-type]
            completed=task_model.completed,  # type: ignore[arg-type]
            project_id=UUID(task_model.project_id) if task_model.project_id else None,  # type: ignore[arg-type]
            created_at=task_model.created_at.replace(tzinfo=timezone.utc),  # type: ignore[arg-type]
            updated_at=task_model.updated_at.replace(tzinfo=timezone.utc),  # type: ignore[arg-type]
        )
