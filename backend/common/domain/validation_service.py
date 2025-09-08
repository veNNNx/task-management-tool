from datetime import datetime, timezone

from attrs import define

from .exceptions import InvalidDeadlineException


@define
class CommonValidationService:
    @staticmethod
    def validate_deadline(deadline: datetime) -> None:
        now = datetime.now(timezone.utc)
        if deadline < now:
            raise InvalidDeadlineException()
