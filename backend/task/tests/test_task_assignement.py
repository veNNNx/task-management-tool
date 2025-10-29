from uuid import uuid4

import pytest
from assertpy import assert_that

from backend.user import UserByIdNotFoundException

from ..src.application.task_facade import TaskFacade
from ..src.infrastructure.exceptions import TaskNotFoundException
from .steps import Steps


class TestTaskAssignement:
    def test_task_assign(self, task_facade: TaskFacade, steps: Steps) -> None:
        user_id = steps.create_user()
        task_created = steps.create_task()
        assert_that(task_created.assigned_to).is_none()

        task_facade.assign_task_to_user(task_id=task_created.id, user_id=user_id)

        task = steps.get_by_id(id=task_created.id)
        assert_that(task.assigned_to).is_equal_to(user_id)
        assert_that(task_created.updated_at).is_less_than(task.updated_at)

    def test_task_assign_fails_on_invalid_user(
        self, task_facade: TaskFacade, steps: Steps
    ) -> None:
        task_created = steps.create_task()

        with pytest.raises(UserByIdNotFoundException):
            task_facade.assign_task_to_user(task_id=task_created.id, user_id=uuid4())

    def test_task_assign_fails_on_invalid_task(
        self, task_facade: TaskFacade, steps: Steps
    ) -> None:
        user_id = steps.create_user()

        with pytest.raises(TaskNotFoundException):
            task_facade.assign_task_to_user(task_id=uuid4(), user_id=user_id)

    def test_task_unassign(self, task_facade: TaskFacade, steps: Steps) -> None:
        user_id = steps.create_user()
        task_created = steps.create_task()
        task_facade.assign_task_to_user(task_id=task_created.id, user_id=user_id)
        task_facade.unassign_task(task_id=task_created.id)
        task = steps.get_by_id(id=task_created.id)

        assert_that(task.assigned_to).is_none()
        assert_that(task_created.updated_at).is_less_than(task.updated_at)

    def test_task_unassign_fails_on_invalid_task(
        self, task_facade: TaskFacade, steps: Steps
    ) -> None:
        with pytest.raises(TaskNotFoundException):
            task_facade.unassign_task(task_id=uuid4())
