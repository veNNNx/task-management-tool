from attr import define
from fastapi.testclient import TestClient
from httpx import Response


@define
class Steps:
    _client: TestClient

    # USER
    def create_user(
        self,
        email: str = "example@gmail.com",
        name: str = "example",
        password: str = "password",
    ) -> Response:
        return self._client.post(
            "/users",
            json={
                "email": email,
                "name": name,
                "password": password,
            },
        )

    def login_user(
        self,
        email: str = "example@gmail.com",
        password: str = "password",
    ) -> Response:
        return self._client.post(
            "/auth/token",
            data={
                "username": email,
                "password": password,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    # AUTH
    def create_token(
        self,
        email: str = "example@gmail.com",
        name: str = "example",
        password: str = "password",
    ) -> str:
        """Create and login user to get token for auth routes."""
        self.create_user(email=email, name=name, password=password)
        response = self.login_user(email=email, password=password)
        return response.json()["access_token"]

    def verify_user(self, token: str) -> Response:
        return self._client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

    # PROTECTED ENDPOINTS
    def get_projects(self, token: str | None = None) -> Response:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        return self._client.get(
            "/projects",
            headers=headers,
        )
