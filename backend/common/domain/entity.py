from abc import ABC, abstractmethod
from uuid import UUID, uuid4


class Entity(ABC):
    @abstractmethod
    def __init__(self, uuid: UUID) -> None:
        self._uuid = uuid

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @staticmethod
    def new_uuid() -> UUID:
        return uuid4()
