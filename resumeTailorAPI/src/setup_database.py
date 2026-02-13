"""
Setup script to initialize the database and create tables.
Run this script once to create the database schema.
"""
from src.database import engine, Base
from src.models import User, Resume


def setup_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")
    print(f"✓ Table 'user' with columns: userId, firstName, lastName, createdAt")
    print(f"✓ Table 'resume' with columns: resumeId, userId, fileName, resumeText, createdAt")


if __name__ == "__main__":
    setup_database()
