"""
Database connection and session management.
Creates connection to PostgreSQL database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine
# This connects to PostgreSQL using the URL from .env file
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Print SQL queries if DEBUG=True
    pool_pre_ping=True,   # Check connection before using
)

# Create session factory
# Sessions are used to interact with the database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all database models
Base = declarative_base()

def get_db():
    """
    Dependency function to get database session.
    Used in FastAPI endpoints to access database.
    Automatically closes connection after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database tables.
    Creates all tables defined in models.py
    """
    from app.models import Quiz  # Import models
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")