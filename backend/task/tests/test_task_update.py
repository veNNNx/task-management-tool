from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from assertpy import assert_that

from backend.common import InvalidDeadlineException

from ..src.application.task_service import TaskService
from ..src.domain.exceptions import TaskWrongStateException
from ..src.infrastructure.exceptions import TaskNotFoundException
from .steps import Steps


class TestTaskUpdate:
    def test_task_update(self, steps: Steps, task_service: TaskService) -> None:
        task = steps.create_task()
        new_title = "new title"
        new_deadline = datetime.now(timezone.utc) + timedelta(days=2)

        updated_task = task_service.update_by_id(
            id=task.id, title=new_title, deadline=new_deadline
        )
        assert_that(updated_task.title).is_equal_to(new_title)
        assert_that(updated_task.deadline).is_equal_to(new_deadline)
        assert_that(updated_task.updated_at).is_greater_than(task.updated_at)

    def test_task_update_fails_on_invalid_id(self, task_service: TaskService) -> None:
        invalid_uuid = uuid4()

        with pytest.raises(TaskNotFoundException, match=str(invalid_uuid)):
            task_service.update_by_id(
                id=invalid_uuid, title="title", deadline=datetime.now(timezone.utc)
            )

    def test_task_update_fails_on_invalid_deadline(
        self, steps: Steps, task_service: TaskService
    ) -> None:
        task = steps.create_task()
        new_deadline = datetime.now(timezone.utc) + timedelta(days=-1)

        with pytest.raises(InvalidDeadlineException):
            task_service.update_by_id(
                id=task.id, title=task.title, deadline=new_deadline
            )


class TestTaskComplete:
    def test_task_complete(self, steps: Steps, task_service: TaskService) -> None:
        task = steps.create_task()

        updated_task = task_service.change_task_state(id=task.id, completed=True)
        assert_that(updated_task.completed).is_true()

    def test_task_complete_fails_on_already_completed(
        self, steps: Steps, task_service: TaskService
    ) -> None:
        task = steps.create_task()

        task_service.change_task_state(id=task.id, completed=True)
        with pytest.raises(TaskWrongStateException):
            task_service.change_task_state(id=task.id, completed=True)

    def test_task_uncomplete(self, steps: Steps, task_service: TaskService) -> None:
        task = steps.create_task()

        task_service.change_task_state(id=task.id, completed=True)
        updated_task = task_service.change_task_state(id=task.id, completed=False)
        assert_that(updated_task.completed).is_false()

    def test_task_uncomplete_fails_on_already_uncompleted(
        self, steps: Steps, task_service: TaskService
    ) -> None:
        task = steps.create_task()

        with pytest.raises(TaskWrongStateException):
            task_service.change_task_state(id=task.id, completed=False)

    def test_task_change_state_fails_on_invalid_id(
        self, task_service: TaskService
    ) -> None:
        invalid_uuid = uuid4()

        with pytest.raises(TaskNotFoundException, match=str(invalid_uuid)):
            task_service.change_task_state(id=invalid_uuid, completed=True)
