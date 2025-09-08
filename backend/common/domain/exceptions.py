from datetime import datetime, timezone


class InvalidDeadlineException(Exception):
    def __init__(self):
        now = datetime.now(timezone.utc)
        message = f"Deadline cannot be earlier than now ({now.isoformat()})"

        super().__init__(message)
