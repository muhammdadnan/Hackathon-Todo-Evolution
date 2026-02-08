"""User model for authentication.

Defines the User SQLModel for database operations and authentication.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model for authentication.

    Attributes:
        id: Unique user identifier (UUID string)
        email: User email address (unique)
        password: Hashed password (bcrypt)
        name: Optional user display name
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """

    __tablename__ = "users"

    id: str = Field(primary_key=True, index=True, max_length=255)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    password: str = Field(max_length=255, nullable=False)  # Hashed password
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": "user_123abc",
                "email": "user@example.com",
                "name": "John Doe",
                "created_at": "2026-02-08T10:00:00Z",
                "updated_at": "2026-02-08T10:00:00Z",
            }
        }
