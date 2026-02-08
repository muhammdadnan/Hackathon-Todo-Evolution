"""Pytest configuration and fixtures.

Provides test fixtures for database, test client, and test users.
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import Settings, get_settings
from app.database import get_session
from app.main import app
from app.middleware.auth import create_access_token, hash_password
from app.models.task import Task
from app.models.user import User


# Test database URL (in-memory SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# Override settings for testing
class TestSettings(Settings):
    """Test settings with in-memory database."""

    database_url: str = TEST_DATABASE_URL
    environment: str = "testing"
    better_auth_secret: str = "test-secret-key-minimum-32-characters-long-for-testing"
    cors_origins: str = "http://localhost:3000"

    class Config:
        """Pydantic configuration."""

        env_file = None  # Don't load .env file in tests


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session_maker = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with test database session."""

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield test_session

    # Override dependencies
    app.dependency_overrides[get_session] = override_get_session

    # Override settings
    def override_get_settings() -> Settings:
        return TestSettings()

    app.dependency_overrides[get_settings] = override_get_settings

    # Create test client
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as test_client:
        yield test_client

    # Clear overrides
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_session: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        id="test_user_123",
        email="test@example.com",
        password=hash_password("testpassword123"),
        name="Test User",
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest.fixture
async def test_user_token(test_user: User) -> str:
    """Create a JWT token for test user."""
    return create_access_token({"sub": test_user.id})


@pytest.fixture
async def another_test_user(test_session: AsyncSession) -> User:
    """Create another test user for isolation testing."""
    user = User(
        id="test_user_456",
        email="another@example.com",
        password=hash_password("anotherpassword123"),
        name="Another User",
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest.fixture
async def another_test_user_token(another_test_user: User) -> str:
    """Create a JWT token for another test user."""
    return create_access_token({"sub": another_test_user.id})


@pytest.fixture
async def test_task(test_session: AsyncSession, test_user: User) -> Task:
    """Create a test task."""
    task = Task(
        user_id=test_user.id,
        title="Test Task",
        description="Test task description",
        completed=False,
    )
    test_session.add(task)
    await test_session.commit()
    await test_session.refresh(task)
    return task
