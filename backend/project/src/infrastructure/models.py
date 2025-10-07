from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from backend.common.infrastructure.base import Base
from backend.common.infrastructure.db_tables import Tables


class ProjectModel(Base):
    __tablename__ = Tables.PROJECTS

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
        unique=True,
        index=True,
    )
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    tasks = relationship("TaskModel", back_populates="project")
