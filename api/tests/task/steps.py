from datetime import datetime, timedelta, timezone
from uuid import UUID

from attr import define
from fastapi.testclient import TestClient
from httpx import Response


@define
class Steps:
    _client: TestClient

    def create_task(
        self,
        title: str = "title",
        deadline: datetime = datetime.now(timezone.utc) + timedelta(days=1),
        project_id: UUID | None = None,
    ) -> Response:
        return self._client.post(
            "/tasks",
            json={
                "title": title,
                "deadline": deadline.isoformat(),
                "project_id": project_id,
            },
        )

    def get_all(self) -> Response:
        return self._client.get("/tasks?page=1&size=50")

    def get_by_id(self, id: UUID) -> Response:
        return self._client.get(f"/tasks/{id}")

    def delete_by_id(self, id: UUID) -> Response:
        return self._client.delete(f"/tasks/{id}")
