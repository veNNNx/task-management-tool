import logging

from ..domain.events import TaskDeadlineApproachingEvent

logger = logging.getLogger(__name__)


def log_deadline_warning(event: TaskDeadlineApproachingEvent):
    logger.warning(
        f"Task '{event.task_title}' (ID: {event.task_id}) "
        f"deadline approaching at {event.task_deadline}"
    )
