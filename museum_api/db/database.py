from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator
from config import settings
import sqlalchemy as sa

# Create database engine
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables in the database"""
    from .models import Base
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all tables in the database"""
    from .models import Base
    Base.metadata.drop_all(bind=engine)


def update_tables():
    """Update tables by dropping and recreating them (WARNING: This will lose data)"""
    from .models import Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def add_column(table_name: str, column_name: str, column_type, **kwargs):
    """Add a column to an existing table"""
    with engine.connect() as connection:
        column_def = f"{column_name} {column_type}"
        if kwargs.get('nullable') is False:
            column_def += " NOT NULL"
        if 'default' in kwargs:
            column_def += f" DEFAULT {kwargs['default']}"

        sql = f"ALTER TABLE {table_name} ADD COLUMN {column_def}"
        connection.execute(sa.text(sql))
        connection.commit()


def drop_column(table_name: str, column_name: str):
    """Drop a column from an existing table"""
    with engine.connect() as connection:
        sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
        connection.execute(sa.text(sql))
        connection.commit()
