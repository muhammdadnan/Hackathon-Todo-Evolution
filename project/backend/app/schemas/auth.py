"""Pydantic schemas for authentication request/response validation.

Defines request and response models for authentication endpoints.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Schema for user signup request."""

    email: EmailStr = Field(
        description="User email address",
        examples=["user@example.com"],
    )
    password: str = Field(
        min_length=8,
        max_length=100,
        description="User password (minimum 8 characters)",
        examples=["securepassword123"],
    )
    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="User display name",
        examples=["John Doe"],
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "name": "John Doe",
            }
        }


class SigninRequest(BaseModel):
    """Schema for user signin request."""

    email: EmailStr = Field(
        description="User email address",
        examples=["user@example.com"],
    )
    password: str = Field(
        description="User password",
        examples=["securepassword123"],
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
            }
        }


class UserResponse(BaseModel):
    """Schema for user response (without password)."""

    id: str = Field(description="User ID", examples=["user_123abc"])
    email: str = Field(description="User email", examples=["user@example.com"])
    name: Optional[str] = Field(
        default=None,
        description="User display name",
        examples=["John Doe"],
    )
    created_at: str = Field(
        description="Creation timestamp",
        examples=["2026-02-08T10:00:00Z"],
    )
    updated_at: str = Field(
        description="Last update timestamp",
        examples=["2026-02-08T10:00:00Z"],
    )

    class Config:
        """Pydantic configuration."""

        from_attributes = True

        json_schema_extra = {
            "example": {
                "id": "user_123abc",
                "email": "user@example.com",
                "name": "John Doe",
                "created_at": "2026-02-08T10:00:00Z",
                "updated_at": "2026-02-08T10:00:00Z",
            }
        }


class AuthResponse(BaseModel):
    """Schema for authentication response."""

    access_token: str = Field(
        description="JWT access token",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    token_type: str = Field(
        default="bearer",
        description="Token type",
        examples=["bearer"],
    )
    user: UserResponse = Field(description="User information")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "user_123abc",
                    "email": "user@example.com",
                    "name": "John Doe",
                    "created_at": "2026-02-08T10:00:00Z",
                    "updated_at": "2026-02-08T10:00:00Z",
                },
            }
        }
