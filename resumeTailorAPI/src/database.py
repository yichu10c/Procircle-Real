import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL - using SQLite by default (no setup required)
# For PostgreSQL, set DATABASE_URL environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./resume_tailor.db"
)

# Remove asyncpg driver prefix if present (for sync SQLAlchemy)
if "+asyncpg" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")
if "?async_fallback=True" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("?async_fallback=True", "")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Create tables on startup
def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
