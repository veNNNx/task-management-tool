from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

TASK_UPDATE_IN = {
    "title": "Create ticket",
    "deadline": "2025-09-15T17:00:00Z",
    "description": "Ticket details",
}
TASK_IN = {
    **TASK_UPDATE_IN,
    "projectId": None,
}
TASK_OUT = {
    **TASK_UPDATE_IN,
    "projectId": "8b2a9f6c-1d3f-4a7b-b8e2-2f9c6e31e9d5",
    "id": "3d5a9f6a-0b2e-4b9b-9f61-1d8a7c28e7b4",
    "completed": False,
    "createdAt": "2025-09-01T08:30:00Z",
    "updatedAt": "2025-09-07T10:15:00Z",
}


class TaskUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={"example": TASK_UPDATE_IN},  # type: ignore[dict-item]
    )
    title: str
    deadline: datetime
    description: str | None = Field(default=None)


class TaskIn(TaskUpdate):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={"example": TASK_IN},  # type: ignore[dict-item]
    )
    title: str
    deadline: datetime
    description: str | None = Field(default=None)
    project_id: None | UUID = Field(default=None)


class TaskOut(TaskIn):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={"example": TASK_OUT},  # type: ignore[dict-item]
    )

    id: UUID
    completed: bool
    project_id: None | UUID = Field(..., alias="projectId")
    assigned_to: None | UUID = Field(..., alias="assignedTo")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
