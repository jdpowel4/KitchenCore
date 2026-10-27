from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from kitchen_ledger.infrastructure.config import DATABASE_URL
from kitchen_ledger.models import *

def create_database_engine(database_url: str = DATABASE_URL) -> Engine:
    return create_engine(database_url)

def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=True)

engine = create_database_engine()
SessionLocal = create_session_factory(engine)