from uuid import uuid4

import pytest
from assertpy import assert_that

from ..src.application.task_service import TaskService
from ..src.infrastructure.exceptions import TaskNotFoundException
from .steps import Steps


class TestTaskGet:
    def test_task_get_all(self, task_service: TaskService) -> None:
        tasks = task_service.get_all()
        assert_that(tasks).is_empty()

    def test_get_task_by_id(self, steps: Steps) -> None:
        title = "title test"
        task_created = steps.create_task(title=title)

        task = steps.get_by_id(id=task_created.id)

        assert_that(task.title).is_equal_to(task_created.title)
        assert_that(task.project_id).is_none()

    def test_get_task_by_id_fails_on_invalid_id(
        self, task_service: TaskService
    ) -> None:
        task_id = uuid4()
        with pytest.raises(TaskNotFoundException, match=str(task_id)):
            task_service.get_by_id(task_id)
