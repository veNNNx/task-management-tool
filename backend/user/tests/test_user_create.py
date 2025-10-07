import pytest
from assertpy import assert_that

from backend.user import UserService, UserWithEmailAlreadyExistsException


class TestUserCreate:
    def test_create_user(
        self, user_service: UserService, user_data: dict[str, str]
    ) -> None:
        user = user_service.create(**user_data)

        assert_that(user.email).is_equal_to(user_data["email"])
        assert_that(user.name).is_equal_to(user_data["name"])
        assert_that(user.hashed_password).is_not_equal_to(user_data["password"])

    def test_create_user_fails_on_already_taken_email(
        self, user_service: UserService, user_data: dict[str, str]
    ) -> None:
        user_service.create(**user_data)
        with pytest.raises(UserWithEmailAlreadyExistsException):
            user_service.create(**user_data)
