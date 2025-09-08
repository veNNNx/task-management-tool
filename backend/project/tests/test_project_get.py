from uuid import uuid4

import pytest
from assertpy import assert_that

from ..src.application.project_servcie import ProjectService
from ..src.infrastructure.exceptions import ProjectNotFoundException
from .steps import Steps


class TestProjectGet:
    def test_project_get_all(self, project_service: ProjectService) -> None:
        projects = project_service.get_all()
        assert_that(projects).is_empty()

    def test_get_project_by_id(self, steps: Steps) -> None:
        title = "title test"
        project_created = steps.create_project(title=title)

        project = steps.get_project_by_id(id=project_created.id)

        assert_that(project.title).is_equal_to(project_created.title)

    def test_get_project_by_id_fails_on_invalid_id(
        self, project_service: ProjectService
    ) -> None:
        project_id = uuid4()
        with pytest.raises(ProjectNotFoundException, match=str(project_id)):
            project_service.get_by_id(project_id)


class TestProjectGetTasks:
    def test_project_get_all_linked_tasks(
        self, project_service: ProjectService, steps: Steps
    ) -> None:
        project = steps.create_project()
        task_1 = steps.create_task(title="task_1")
        steps.link_task_to_project(project_id=project.id, task_id=task_1.id)
        task_2 = steps.create_task(title="task_2")
        steps.link_task_to_project(project_id=project.id, task_id=task_2.id)

        linked_tasks = project_service.get_all_tasks_by_project_id(project.id)

        assert_that(linked_tasks).is_length(2)
        assert_that(linked_tasks[0].id).is_equal_to(task_1.id)
        assert_that(linked_tasks[0].title).is_equal_to(task_1.title)
        assert_that(linked_tasks[1].id).is_equal_to(task_2.id)
        assert_that(linked_tasks[1].title).is_equal_to(task_2.title)

    def test_project_get_all_linked_tasks_fails_on_invalid_project_id(
        self, project_service: ProjectService
    ) -> None:
        project_id = uuid4()
        with pytest.raises(ProjectNotFoundException, match=str(project_id)):
            project_service.get_by_id(project_id)
