from datetime import datetime, timedelta, timezone

from attrs import define

from backend.common import EventBus

from ..domain.events import TaskDeadlineApproachingEvent
from ..infrastructure.task_repository import TaskTable


@define
class TaskDeadlineCheckerService:
    _task_tabel: TaskTable
    _event_bus: EventBus

    def check_deadlines(self):
        now = datetime.now(timezone.utc)
        upcoming_tasks = self._task_tabel.get_tasks_with_deadline_between(
            now, now + timedelta(hours=24)
        )
        for task in upcoming_tasks:
            self._event_bus.publish(
                TaskDeadlineApproachingEvent(
                    task_id=task.id, task_title=task.title, task_deadline=task.deadline
                )
            )
