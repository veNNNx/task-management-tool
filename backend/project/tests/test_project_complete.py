from assertpy import assert_that

from .steps import Steps


class TestProjectComplete:
    def test_complete_project(self, steps: Steps) -> None:
        project, task = steps.create_project_with_linked_task()
        steps.change_task_state(task_id=task.id)

        project_linked = steps.get_project_by_id(project.id)

        assert_that(project_linked.updated_at).is_greater_than(project.updated_at)
        assert_that(project_linked.completed).is_true()

    def test_complete_project_after_deleting_uncompleted_tasks(
        self, steps: Steps
    ) -> None:
        project, task = steps.create_project_with_linked_task()
        task_1 = steps.create_task()
        steps.link_task_to_project(project_id=project.id, task_id=task_1.id)
        steps.change_task_state(task_id=task.id)

        project_linked = steps.get_project_by_id(project.id)
        assert_that(project_linked.completed).is_false()

        steps.delete_task_by_id(task_1.id)
        project_linked = steps.get_project_by_id(project.id)

        assert_that(project_linked.completed).is_true()
        assert_that(project_linked.updated_at).is_greater_than(project.updated_at)

    def test_uncomplete_project_after_opening_task(self, steps: Steps) -> None:
        project, task = steps.create_project_with_linked_task()
        steps.change_task_state(task_id=task.id)
        project_linked = steps.get_project_by_id(project.id)

        assert_that(project_linked.completed).is_true()

        steps.change_task_state(task_id=task.id, completed=False)

        project_linked = steps.get_project_by_id(project.id)
        assert_that(project_linked.completed).is_false()
        assert_that(project_linked.updated_at).is_greater_than(project.updated_at)
