from uuid import uuid4

import pytest
from assertpy import assert_that

from backend.user import UserByIdNotFoundException

from ..src.application.task_facade import TaskFacade
from ..src.infrastructure.exceptions import TaskNotFoundException
from .steps import Steps


class TestTaskGet:
    def test_task_get_all(self, task_facade: TaskFacade) -> None:
        tasks = task_facade.get_all()
        assert_that(tasks).is_empty()

    def test_get_task_by_id(self, steps: Steps) -> None:
        title = "title test"
        task_created = steps.create_task(title=title)

        task = steps.get_by_id(id=task_created.id)

        assert_that(task.title).is_equal_to(task_created.title)
        assert_that(task.project_id).is_none()

    def test_get_task_by_id_fails_on_invalid_id(self, task_facade: TaskFacade) -> None:
        task_id = uuid4()
        with pytest.raises(TaskNotFoundException, match=str(task_id)):
            task_facade.get_by_id(task_id)

    def test_get_tasks_by_user_id(self, steps: Steps, task_facade: TaskFacade) -> None:
        user_id = steps.create_user()
        task1 = steps.create_task(title="Task 1")
        task2 = steps.create_task(title="Task 2")
        steps.create_task()
        task_facade.assign_task_to_user(task_id=task1.id, user_id=user_id)
        task_facade.assign_task_to_user(task_id=task2.id, user_id=user_id)

        tasks = task_facade.get_tasks_by_user_id(user_id=user_id)

        assert_that(tasks).is_length(2)
        task_ids = [task.id for task in tasks]
        assert_that(task_ids).contains(task1.id, task2.id)

    def test_get_tasks_by_user_id_fails_on_invalid_user_id(
        self, task_facade: TaskFacade
    ) -> None:
        invalid_user_id = uuid4()

        with pytest.raises(UserByIdNotFoundException, match=str(invalid_user_id)):
            task_facade.get_tasks_by_user_id(user_id=invalid_user_id)
