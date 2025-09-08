from datetime import datetime
from uuid import UUID

from attrs import define


@define(frozen=True)
class TaskDeadlineApproachingEvent:
    task_id: UUID
    task_title: str
    task_deadline: datetime
