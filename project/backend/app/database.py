"""Database connection and session management.

Provides SQLModel engine, session management, and database initialization
for the FastAPI backend.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import get_settings

# Get settings
settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.is_development,  # Log SQL queries in development
    future=True,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Max connections beyond pool_size
)

# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency for FastAPI.

    Yields:
        AsyncSession: Database session

    Example:
        @app.get("/items")
        async def get_items(session: AsyncSession = Depends(get_session)):
            result = await session.execute(select(Item))
            return result.scalars().all()
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_db_and_tables() -> None:
    """Create database tables.

    This function creates all tables defined in SQLModel models.
    Should be called on application startup.

    Note:
        In production, use Alembic migrations instead of this function.
    """
    async with engine.begin() as conn:
        # Import all models to ensure they're registered with SQLModel
        from app.models.task import Task  # noqa: F401
        from app.models.user import User  # noqa: F401

        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_db_and_tables() -> None:
    """Drop all database tables.

    WARNING: This will delete all data in the database.
    Only use for testing or development.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def close_db_connection() -> None:
    """Close database connection.

    Should be called on application shutdown.
    """
    await engine.dispose()
