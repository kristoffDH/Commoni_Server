from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.configs.config import db_config

engine = create_engine(db_config.URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
