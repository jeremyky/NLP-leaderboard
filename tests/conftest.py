"""
Shared pytest fixtures for all tests
"""
import pytest
from database import SessionLocal, init_db
from models import Base, Dataset, Submission
from sqlalchemy import create_engine
import os

# Use test database for isolation
TEST_DB_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test_leaderboard.db")
test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DB_URL else {},
)

@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """Clean database before each test"""
    # Ensure tables exist
    Base.metadata.create_all(bind=test_engine)
    
    # Clean up any existing data
    db = SessionLocal()
    try:
        db.query(Submission).delete()
        db.query(Dataset).delete()
        db.commit()
    finally:
        db.close()
    
    yield
    
    # Cleanup after test
    db = SessionLocal()
    try:
        db.query(Submission).delete()
        db.query(Dataset).delete()
        db.commit()
    finally:
        db.close()

