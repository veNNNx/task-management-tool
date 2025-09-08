from datetime import datetime, timedelta, timezone
from uuid import uuid4

from assertpy import assert_that
from fastapi import status

from .steps import Steps


class TestTask:
    def test_get_all_tasks(self, steps: Steps) -> None:
        response = steps.get_all()
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        assert_that(response.json()).is_empty()

    def test_get_task_by_id(self, steps: Steps) -> None:
        response_create = steps.create_task()
        id = response_create.json()["id"]
        response = steps.get_by_id(id)

        data = response.json()
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(data["id"]).is_equal_to(id)
        assert_that(data["title"]).is_equal_to("title")

    def test_get_task_by_id_fails_on_invalid_id(self, steps: Steps) -> None:
        task_id = uuid4()
        response = steps.get_by_id(task_id)

        assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)
        assert_that(response.json()["message"]).is_equal_to(
            f"No task with id=UUID('{task_id}') exists in the store!"
        )

    def test_create_one_task(self, steps: Steps) -> None:
        title = "Task #1"
        deadline = datetime.now(timezone.utc) + timedelta(days=1)
        response = steps.create_task(title=title, deadline=deadline)

        data = response.json()
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(data["title"]).is_equal_to(title)

        deadline_from_api = datetime.fromisoformat(
            data["deadline"].replace("Z", "+00:00")
        )
        assert_that(deadline_from_api).is_equal_to(deadline)

    def test_create_one_task_fails_on_invalid_deadline(self, steps: Steps) -> None:
        title = "Task #1"
        deadline = datetime.now(timezone.utc) + timedelta(days=-1)
        response = steps.create_task(title=title, deadline=deadline)
        assert_that(response.status_code).is_equal_to(status.HTTP_409_CONFLICT)
        assert_that(response.json()["message"]).contains(
            "Deadline cannot be earlier than now"
        )

    def test_delete_task_by_id(self, steps: Steps) -> None:
        response_create = steps.create_task()
        id = response_create.json()["id"]
        response = steps.delete_by_id(id)

        assert_that(response.status_code).is_equal_to(status.HTTP_204_NO_CONTENT)

    def test_delete_task_by_id_fails_on_invalid_id(self, steps: Steps) -> None:
        task_id = uuid4()
        response = steps.delete_by_id(task_id)

        assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)
        assert_that(response.json()["message"]).is_equal_to(
            f"No task with id=UUID('{task_id}') exists in the store!"
        )
