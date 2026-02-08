"""Task model for todo items.

Defines the Task SQLModel for database operations and task management.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Task model for todo items.

    Attributes:
        id: Unique task identifier (auto-increment)
        user_id: Foreign key to users table
        title: Task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)
        completed: Task completion status (default: False)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        max_length=255,
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        nullable=False,
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )
    completed: bool = Field(default=False, nullable=False, index=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user_123abc",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2026-02-08T10:00:00Z",
                "updated_at": "2026-02-08T10:00:00Z",
            }
        }
