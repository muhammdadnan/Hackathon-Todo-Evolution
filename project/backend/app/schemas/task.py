"""Pydantic schemas for task request/response validation.

Defines request and response models for task API endpoints.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Schema for creating a new task.

    Attributes:
        title: Task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)
    """

    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title",
        examples=["Buy groceries"],
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description",
        examples=["Milk, eggs, bread"],
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task.

    Attributes:
        title: Task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)
    """

    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title",
        examples=["Buy groceries and fruits"],
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description",
        examples=["Milk, eggs, bread, apples, bananas"],
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "title": "Buy groceries and fruits",
                "description": "Milk, eggs, bread, apples, bananas",
            }
        }


class TaskResponse(BaseModel):
    """Schema for task response.

    Attributes:
        id: Task ID
        user_id: User ID who owns the task
        title: Task title
        description: Optional task description
        completed: Task completion status
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """

    id: int = Field(description="Task ID", examples=[1])
    user_id: str = Field(description="User ID", examples=["user_123abc"])
    title: str = Field(description="Task title", examples=["Buy groceries"])
    description: Optional[str] = Field(
        default=None,
        description="Task description",
        examples=["Milk, eggs, bread"],
    )
    completed: bool = Field(description="Completion status", examples=[False])
    created_at: datetime = Field(
        description="Creation timestamp",
        examples=["2026-02-08T10:00:00Z"],
    )
    updated_at: datetime = Field(
        description="Last update timestamp",
        examples=["2026-02-08T10:00:00Z"],
    )

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Enable ORM mode for SQLModel compatibility

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
