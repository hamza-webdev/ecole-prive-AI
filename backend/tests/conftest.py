import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from backend.app.main import app  # Main FastAPI application
from backend.app.database import Base, get_db  # SQLAlchemy Base and get_db dependency
from backend.app.config import settings # Application settings

# --- Test Database Setup ---
# Use an in-memory SQLite database for testing for simplicity and speed.
# If specific PostgreSQL features are used that SQLite doesn't support,
# this might need adjustment to use a test PostgreSQL database.
TEST_DATABASE_URL = "sqlite:///:memory:" 
# Alternatively, for a test PostgreSQL DB (requires setup and teardown):
# TEST_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    """
    Fixture to create all tables in the test database once per session.
    The autouse=True ensures it runs automatically.
    """
    Base.metadata.create_all(bind=engine)
    yield
    # Optional: Base.metadata.drop_all(bind=engine) # To clean up, but often not needed for in-memory

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Provides a transactional scope around a test function.
    A new session is created for each test, and any changes are rolled back.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Provides a FastAPI TestClient that uses the test database session.
    Overrides the `get_db` dependency in the app for the scope of the test.
    """
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            db_session.close() # Ensure session is closed if not already by the db_session fixture

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    del app.dependency_overrides[get_db] # Clean up override
