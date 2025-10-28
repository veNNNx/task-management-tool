from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from assertpy import assert_that

from backend.common import InvalidDeadlineException

from ..src.application.task_facade import TaskFacade
from ..src.infrastructure.exceptions import InvalidProjectIdException


class TestTaskCreate:
    def test_task_create(self, task_facade: TaskFacade) -> None:
        title = "title"
        deadline = datetime.now(timezone.utc) + timedelta(days=1)

        task = task_facade.create(title=title, deadline=deadline)

        assert_that(task.title).is_equal_to(title)
        assert_that(task.deadline).is_equal_to(deadline)

    def test_task_create_fails_on_invalid_deadline(
        self, task_facade: TaskFacade
    ) -> None:
        title = "title"
        deadline = datetime.now(timezone.utc) + timedelta(days=-1)

        with pytest.raises(InvalidDeadlineException):
            task_facade.create(title=title, deadline=deadline)

    def test_task_create_fails_on_invalid_project_id(
        self, task_facade: TaskFacade
    ) -> None:
        deadline = datetime.now(timezone.utc) + timedelta(days=1)
        invalid_uuid = uuid4()

        with pytest.raises(InvalidProjectIdException):
            task_facade.create(
                title="title", deadline=deadline, project_id=invalid_uuid
            )
