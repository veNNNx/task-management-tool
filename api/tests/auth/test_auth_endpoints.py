from assertpy import assert_that
from fastapi import status

from .steps import Steps


class TestAuthLogin:
    def test_get_projects_with_token(self, steps: Steps) -> None:
        token = steps.create_token()
        response = steps.get_projects(token=token)

        assert_that(token).is_type_of(str)
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.json()).is_empty()

    def test_get_projects_fails_on_invalid_token(self, steps: Steps) -> None:
        token = "invalid_token"
        response = steps.get_projects(token=token)

        assert_that(response.status_code).is_equal_to(status.HTTP_401_UNAUTHORIZED)
        assert_that(response.json()["detail"]).is_equal_to(
            "Incorrect email or password"
        )
