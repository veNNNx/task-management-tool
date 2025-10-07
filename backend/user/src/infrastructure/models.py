from uuid import uuid4

from sqlalchemy import Column, String

from backend.common import Tables
from backend.common.infrastructure.base import Base


class UserModel(Base):
    __tablename__ = Tables.USERS

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
        unique=True,
        index=True,
    )
    email = Column(String(25), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    hashed_password = Column(String(128), nullable=False)
