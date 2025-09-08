from databases import Database
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.common.infrastructure import db_events as _  # noqa: F401

DATABASE_URL = "sqlite:///./prod_db.sqlite"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
with engine.connect() as conn:
    conn.execute(text("PRAGMA foreign_keys = ON"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from .db_models import *  # noqa: F403 E402

database = Database(DATABASE_URL)
