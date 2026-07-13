from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session

from app.core.settings import settings
from app.core.logger import logger
from app.database.base import Base

# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Checks connection health before use
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@contextmanager
def get_db() -> Iterator[Session]:
    """Dependency that provides a database session.
    
    Yields:
        Session: SQLAlchemy database session
    
    Raises:
        SQLAlchemyError: If session creation fails
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def init_database() -> None:
    """Initialize database tables.
    
    Creates all tables defined in models inheriting from Base.
    Logs success/failure using application logger.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
    except SQLAlchemyError as e:
        logger.critical(f"Database initialization failed: {str(e)}")
        raise