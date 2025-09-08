from uuid import uuid4

import pytest
from assertpy import assert_that

from ..src.application.project_servcie import ProjectService
from ..src.infrastructure.exceptions import ProjectNotFoundException
from .steps import Steps


class TestProjectDelete:
    def test_delete_project_by_id(
        self, project_service: ProjectService, steps: Steps
    ) -> None:
        project = steps.create_project()

        project_service.delete_by_id(project.id)
        with pytest.raises(ProjectNotFoundException, match=str(project.id)):
            project_service.get_by_id(project.id)

    def test_delete_project_by_id_fails_on_invalid_id(
        self, project_service: ProjectService
    ) -> None:
        invalid_uuid = uuid4()

        with pytest.raises(ProjectNotFoundException, match=str(invalid_uuid)):
            project_service.delete_by_id(invalid_uuid)

    def test_delete_project_by_id_unlinks_its_tasks(
        self, project_service: ProjectService, steps: Steps
    ) -> None:
        project, task = steps.create_project_with_linked_task()

        project_service.delete_by_id(project.id)

        task_unlinked = steps.get_task_by_id(task.id)
        assert_that(task_unlinked.project_id).is_none()
