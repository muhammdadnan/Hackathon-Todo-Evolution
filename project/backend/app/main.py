"""FastAPI application entry point.

Main application setup with middleware, routes, and lifecycle events.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import close_db_connection, create_db_and_tables

# Get settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    Handles startup and shutdown events for the FastAPI application.

    Args:
        app: FastAPI application instance

    Yields:
        None: Control back to FastAPI
    """
    # Startup: Create database tables
    await create_db_and_tables()
    print("✓ Database tables created")
    print(f"✓ Server running on {settings.host}:{settings.port}")
    print(f"✓ Environment: {settings.environment}")
    print(f"✓ CORS origins: {settings.cors_origins_list}")

    yield

    # Shutdown: Close database connection
    await close_db_connection()
    print("✓ Database connection closed")


# Create FastAPI application
app = FastAPI(
    title="Todo Evolution API",
    description="FastAPI backend for Todo Evolution Phase 2",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        dict: Health status

    Example:
        GET /health
        Response: {"status": "healthy"}
    """
    return {"status": "healthy"}


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """Root endpoint.

    Returns:
        dict: Welcome message with API documentation link

    Example:
        GET /
        Response: {"message": "...", "docs": "/docs"}
    """
    return {
        "message": "Todo Evolution API - Phase 2",
        "docs": "/docs",
        "health": "/health",
    }


# Import and register routes
from app.routes.auth import router as auth_router
from app.routes.tasks import router as tasks_router

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks_router, prefix="/api", tags=["Tasks"])
