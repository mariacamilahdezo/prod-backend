from app.config import get_settings, Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    settings = get_settings()
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    return engine


def get_session():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal
