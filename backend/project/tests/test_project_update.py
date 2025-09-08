from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from assertpy import assert_that

from backend.common import InvalidDeadlineException
from backend.task import TaskDeadlineExceededException

from ..src.application.project_servcie import ProjectService
from ..src.infrastructure.exceptions import ProjectNotFoundException
from .steps import Steps


class TestProjectUpdate:
    def test_project_update(
        self, steps: Steps, project_service: ProjectService
    ) -> None:
        project = steps.create_project()
        new_title = "new title"
        new_deadline = datetime.now(timezone.utc) + timedelta(days=2)

        updated_project = project_service.update_by_id(
            id=project.id, title=new_title, deadline=new_deadline
        )
        assert_that(updated_project.title).is_equal_to(new_title)
        assert_that(updated_project.deadline).is_equal_to(new_deadline)
        assert_that(updated_project.updated_at).is_greater_than(project.updated_at)

    def test_project_update_fails_on_invalid_id(
        self, project_service: ProjectService
    ) -> None:
        invalid_uuid = uuid4()

        with pytest.raises(ProjectNotFoundException, match=str(invalid_uuid)):
            project_service.update_by_id(
                id=invalid_uuid, title="title", deadline=datetime.now(timezone.utc)
            )

    def test_project_update_fails_on_invalid_deadline(
        self, steps: Steps, project_service: ProjectService
    ) -> None:
        project = steps.create_project()
        new_deadline = datetime.now(timezone.utc) + timedelta(days=-1)

        with pytest.raises(InvalidDeadlineException):
            project_service.update_by_id(
                id=project.id, title=project.title, deadline=new_deadline
            )

    def test_project_update_deadline_fails_on_task_longer_deadline(
        self, steps: Steps
    ) -> None:
        project = steps.create_project()
        steps.create_task(project_id=project.id)
        new_deadline = datetime.now(timezone.utc) + timedelta(hours=12)

        with pytest.raises(TaskDeadlineExceededException):
            steps.update_project_by_id(
                id=project.id, title=project.title, deadline=new_deadline
            )

    def test_task_update_deadline_fails_on_project_sooner_deadline(
        self, steps: Steps
    ) -> None:
        project = steps.create_project()
        task = steps.create_task(project_id=project.id)
        new_deadline = datetime.now(timezone.utc) + timedelta(days=10)

        with pytest.raises(TaskDeadlineExceededException):
            steps.update_task_by_id(
                id=task.id, title=project.title, deadline=new_deadline
            )
