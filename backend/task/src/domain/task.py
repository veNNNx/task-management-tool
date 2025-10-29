from datetime import datetime, timezone
from uuid import UUID

from attrs import define

from backend.common import Entity


@define(kw_only=True)
class Task(Entity):
    id: UUID
    title: str
    deadline: datetime
    description: str | None = None
    completed: bool = False
    project_id: None | UUID = None
    assigned_to: None | UUID = None
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
