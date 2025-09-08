from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from assertpy import assert_that

from backend.common import InvalidDeadlineException

from ..src.application.task_service import TaskService
from ..src.infrastructure.exceptions import InvalidProjectIdException


class TestTaskCreate:
    def test_task_create(self, task_service: TaskService) -> None:
        title = "title"
        deadline = datetime.now(timezone.utc) + timedelta(days=1)

        task = task_service.create(title=title, deadline=deadline)

        assert_that(task.title).is_equal_to(title)
        assert_that(task.deadline).is_equal_to(deadline)

    def test_task_create_fails_on_invalid_deadline(
        self, task_service: TaskService
    ) -> None:
        title = "title"
        deadline = datetime.now(timezone.utc) + timedelta(days=-1)

        with pytest.raises(InvalidDeadlineException):
            task_service.create(title=title, deadline=deadline)

    def test_task_create_fails_on_invalid_project_id(
        self, task_service: TaskService
    ) -> None:
        deadline = datetime.now(timezone.utc) + timedelta(days=1)
        invalid_uuid = uuid4()

        with pytest.raises(InvalidProjectIdException):
            task_service.create(
                title="title", deadline=deadline, project_id=invalid_uuid
            )
