import threading

from ..application.task_deadline_checker_service import TaskDeadlineCheckerService


def start_task_deadline_scheduler(
    checker: TaskDeadlineCheckerService, interval_sec: int = 3600
):
    stop_event = threading.Event()

    def run():
        while not stop_event.is_set():
            checker.check_deadlines()
            stop_event.wait(interval_sec)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread, stop_event
