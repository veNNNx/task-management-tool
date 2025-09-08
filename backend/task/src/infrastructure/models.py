from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from backend.common import Tables
from backend.common.infrastructure.base import Base


class TaskModel(Base):
    __tablename__ = Tables.TASKS

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
        unique=True,
        index=True,
    )
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    project_id = Column(String(36), ForeignKey(f"{Tables.PROJECTS}.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    project = relationship("ProjectModel", back_populates="tasks", lazy="joined")
