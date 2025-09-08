from typing import TypeAlias

from sqlalchemy.orm import declarative_base

Base: TypeAlias = declarative_base()  # type: ignore[valid-type]
