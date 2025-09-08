from datetime import datetime, timedelta, timezone

import pytest
from assertpy import assert_that

from backend.common import InvalidDeadlineException

from .steps import Steps


class TestProjectCreate:
    def test_project_create(self, steps: Steps) -> None:
        title = "title"
        deadline = datetime.now(timezone.utc) + timedelta(days=1)

        project = steps.create_project(title=title, deadline=deadline)

        assert_that(project.title).is_equal_to(title)
        assert_that(project.deadline).is_equal_to(deadline)

    def test_project_create_fails_on_invalid_deadline(self, steps: Steps) -> None:
        deadline = datetime.now(timezone.utc) + timedelta(days=-1)

        with pytest.raises(InvalidDeadlineException):
            steps.create_project(deadline=deadline)
