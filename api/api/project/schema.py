from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

PROJECT_IN = {
    "title": "Create ticket",
    "deadline": "2025-09-15T17:00:00Z",
    "description": "Ticket details",
}
PROJECT_OUT = {
    **PROJECT_IN,
    "id": "3d5a9f6a-0b2e-4b9b-9f61-1d8a7c28e7b4",
    "completed": False,
    "createdAt": "2025-09-01T08:30:00Z",
    "updatedAt": "2025-09-07T10:15:00Z",
}


class ProjectIn(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": PROJECT_IN},  # type: ignore[dict-item]
    )
    title: str
    deadline: datetime
    description: str | None = Field(default=None)


class ProjectOut(ProjectIn):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={"example": PROJECT_OUT},  # type: ignore[dict-item]
    )

    id: UUID
    completed: bool
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
