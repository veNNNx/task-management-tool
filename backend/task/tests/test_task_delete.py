from uuid import uuid4

import pytest

from ..src.application.task_facade import TaskFacade
from ..src.infrastructure.exceptions import TaskNotFoundException
from .steps import Steps


class TestTaskDelete:
    def test_delete_task_by_id(self, task_facade: TaskFacade, steps: Steps) -> None:
        task = steps.create_task()

        task_facade.delete_by_id(task.id)
        with pytest.raises(TaskNotFoundException, match=str(task.id)):
            task_facade.delete_by_id(task.id)

    def test_delete_task_by_id_fails_on_invalid_id(
        self, task_facade: TaskFacade
    ) -> None:
        invalid_uuid = uuid4()

        with pytest.raises(TaskNotFoundException, match=str(invalid_uuid)):
            task_facade.delete_by_id(invalid_uuid)
