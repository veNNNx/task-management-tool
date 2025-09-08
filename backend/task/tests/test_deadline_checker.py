import time
from datetime import datetime, timedelta, timezone
from threading import Thread

from assertpy import assert_that

from .steps import Steps


def test_task_deadline_warning(
    steps: Steps,
    task_deadline_scheduler: Thread,
    caplog,
):
    steps.create_task(
        title="Urgent Task", deadline=datetime.now(timezone.utc) + timedelta(hours=1)
    )

    caplog.set_level("WARNING")

    time.sleep(2)

    warnings = [r for r in caplog.records if r.levelname == "WARNING"]
    assert_that(warnings).is_not_empty()

    log_message = warnings[0].getMessage()

    assert_that(log_message).contains("Urgent Task")
    assert_that(log_message).contains("deadline approaching")
