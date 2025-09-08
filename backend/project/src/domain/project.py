from datetime import datetime, timezone
from uuid import UUID

from attrs import define

from backend.common import Entity

from ..domain.exceptions import ProjectAlreadyCompletedException


@define(kw_only=True)
class Project(Entity):
    id: UUID
    title: str
    deadline: datetime
    description: str | None = None
    completed: bool = False
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    def validate_project_completed(self) -> None:
        if self.completed:
            raise ProjectAlreadyCompletedException(
                project_title=self.title,
                project_id=self.id,
            )
