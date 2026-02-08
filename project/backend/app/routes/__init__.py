"""Routes package.

Exports all API routers.
"""

from app.routes.auth import router as auth_router

__all__ = ["auth_router"]
