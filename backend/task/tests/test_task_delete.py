from uuid import uuid4

import pytest

from ..src.application.task_service import TaskService
from ..src.infrastructure.exceptions import TaskNotFoundException
from .steps import Steps


class TestTaskDelete:
    def test_delete_task_by_id(self, task_service: TaskService, steps: Steps) -> None:
        task = steps.create_task()

        task_service.delete_by_id(task.id)
        with pytest.raises(TaskNotFoundException, match=str(task.id)):
            task_service.delete_by_id(task.id)

    def test_delete_task_by_id_fails_on_invalid_id(
        self, task_service: TaskService
    ) -> None:
        invalid_uuid = uuid4()

        with pytest.raises(TaskNotFoundException, match=str(invalid_uuid)):
            task_service.delete_by_id(invalid_uuid)
