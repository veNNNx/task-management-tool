from assertpy import assert_that
from fastapi import status

from .steps import Steps


class TestAuthLogin:
    def test_login_user(self, steps: Steps) -> None:
        steps.create_user()
        response = steps.login_user()

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.json()["token_type"]).is_equal_to("bearer")

    def test_login_user_fails_on_invalid_user(self, steps: Steps) -> None:
        response = steps.login_user()

        assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)
