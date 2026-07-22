"""Database engine and session management for MediNexus AI."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite for hackathon — swap URL for PostgreSQL in production:
# "postgresql://user:pass@localhost/medinexus"
SQLALCHEMY_DATABASE_URL = "sqlite:///./medinexus.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite-only flag
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
