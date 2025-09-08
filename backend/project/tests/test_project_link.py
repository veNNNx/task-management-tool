from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from assertpy import assert_that

from backend.task import TaskAlreadyCompletedException, TaskNotFoundException

from ..src.application.project_servcie import ProjectService
from ..src.domain.exceptions import (
    ProjectAlreadyCompletedException,
    TaskNotLinkedToProjectException,
)
from ..src.infrastructure.exceptions import ProjectNotFoundException
from .steps import Steps


class TestProjectLink:
    def test_link_task_to_project(self, steps: Steps) -> None:
        project = steps.create_project()
        task = steps.create_task()

        steps.link_task_to_project(project_id=project.id, task_id=task.id)

        task_linked = steps.get_task_by_id(task.id)
        project_linked = steps.get_project_by_id(project.id)

        assert_that(task_linked.project_id).is_equal_to(project.id)
        assert_that(task_linked.updated_at).is_greater_than(project.updated_at)
        assert_that(project_linked.updated_at).is_greater_than(project.updated_at)

    def test_link_task_with_longer_deadline_to_project(self, steps: Steps) -> None:
        project = steps.create_project()
        deadline = datetime.now(timezone.utc) + timedelta(days=10)
        task = steps.create_task(deadline=deadline)

        steps.link_task_to_project(project_id=project.id, task_id=task.id)

        task_linked = steps.get_task_by_id(task.id)

        assert_that(task_linked.project_id).is_equal_to(project.id)
        assert_that(task_linked.deadline).is_equal_to(project.deadline)

    def test_link_task_to_project_fails_on_invalid_task_id(self, steps: Steps) -> None:
        project = steps.create_project()
        invalid_uuid = uuid4()
        with pytest.raises(TaskNotFoundException):
            steps.link_task_to_project(project_id=project.id, task_id=invalid_uuid)

    def test_link_task_to_project_fails_on_invalid_project_id(
        self, steps: Steps
    ) -> None:
        task = steps.create_task()
        invalid_uuid = uuid4()
        with pytest.raises(ProjectNotFoundException):
            steps.link_task_to_project(project_id=invalid_uuid, task_id=task.id)

    def test_link_completed_task_to_project_fails(self, steps: Steps) -> None:
        project, _ = steps.create_project_with_linked_task()
        task = steps.create_task()
        steps.change_task_state(task.id)

        with pytest.raises(TaskAlreadyCompletedException):
            steps.link_task_to_project(project_id=project.id, task_id=task.id)

    def test_link_task_to_completed_project_fails(self, steps: Steps) -> None:
        project_linked, task_linked = steps.create_project_with_linked_task()
        task = steps.create_task()
        steps.change_task_state(task_id=task_linked.id)

        with pytest.raises(ProjectAlreadyCompletedException):
            steps.link_task_to_project(project_id=project_linked.id, task_id=task.id)


class TestProjectUnlink:
    def test_unink_task_from_project(
        self, steps: Steps, project_service: ProjectService
    ) -> None:
        project, task = steps.create_project_with_linked_task()
        project_service.unlink_task_from_project(project_id=project.id, task_id=task.id)

        task_unlinked = steps.get_task_by_id(task.id)
        linked_tasks = project_service.get_all_tasks_by_project_id(project.id)

        assert_that(task_unlinked.project_id).is_none()
        assert_that(linked_tasks).is_empty()

    def test_unlink_task_from_project_fails_on_invalid_task_id(
        self, steps: Steps, project_service: ProjectService
    ) -> None:
        project, _ = steps.create_project_with_linked_task()
        invalid_uuid = uuid4()

        with pytest.raises(TaskNotFoundException):
            project_service.unlink_task_from_project(
                project_id=project.id, task_id=invalid_uuid
            )

    def test_unlink_task_from_project_fails_on_invalid_project_id(
        self, project_service: ProjectService
    ) -> None:
        invalid_uuid = uuid4()

        with pytest.raises(ProjectNotFoundException):
            project_service.unlink_task_from_project(
                project_id=invalid_uuid, task_id=invalid_uuid
            )

    def test_unlink_task_from_project_fails_on_not_linked_task(
        self, steps: Steps, project_service: ProjectService
    ) -> None:
        task = steps.create_task()
        project, _ = steps.create_project_with_linked_task()

        with pytest.raises(TaskNotLinkedToProjectException):
            project_service.unlink_task_from_project(
                project_id=project.id, task_id=task.id
            )

    def test_unlink_task_from_project_fails_on_task_linked_to_other_project(
        self, steps: Steps, project_service: ProjectService
    ) -> None:
        project = steps.create_project()
        _, task = steps.create_project_with_linked_task()

        with pytest.raises(TaskNotLinkedToProjectException):
            project_service.unlink_task_from_project(
                project_id=project.id, task_id=task.id
            )

    def test_unlink_completed_task_from_project_fails(
        self, steps: Steps, project_service: ProjectService
    ) -> None:
        project, task_1 = steps.create_project_with_linked_task()
        task_2 = steps.create_task()
        steps.link_task_to_project(project_id=project.id, task_id=task_2.id)
        steps.change_task_state(task_id=task_1.id)

        with pytest.raises(TaskAlreadyCompletedException):
            project_service.unlink_task_from_project(
                project_id=project.id, task_id=task_1.id
            )
