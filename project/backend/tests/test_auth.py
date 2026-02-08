"""Authentication endpoint tests.

Tests for user signup, signin, JWT token verification, and protected endpoints.
Following TDD RED phase - these tests should FAIL until implementation is complete.
"""

import pytest
from httpx import AsyncClient

from app.models.user import User


class TestUserSignup:
    """Test user signup functionality."""

    @pytest.mark.asyncio
    async def test_signup_success(self, client: AsyncClient):
        """Test successful user signup."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "newuser@example.com",
                "password": "securepassword123",
                "name": "New User",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["name"] == "New User"
        assert "password" not in data["user"]  # Password should not be returned

    @pytest.mark.asyncio
    async def test_signup_duplicate_email(self, client: AsyncClient, test_user: User):
        """Test signup with duplicate email fails."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": test_user.email,  # Already exists
                "password": "anotherpassword123",
                "name": "Duplicate User",
            },
        )

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already exists" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_signup_invalid_email(self, client: AsyncClient):
        """Test signup with invalid email format fails."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "not-an-email",
                "password": "securepassword123",
                "name": "Invalid Email User",
            },
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_signup_short_password(self, client: AsyncClient):
        """Test signup with short password fails."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "shortpass@example.com",
                "password": "123",  # Too short
                "name": "Short Password User",
            },
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_signup_missing_email(self, client: AsyncClient):
        """Test signup without email fails."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "password": "securepassword123",
                "name": "No Email User",
            },
        )

        assert response.status_code == 422  # Validation error


class TestUserSignin:
    """Test user signin functionality."""

    @pytest.mark.asyncio
    async def test_signin_success(self, client: AsyncClient, test_user: User):
        """Test successful user signin."""
        response = await client.post(
            "/api/auth/signin",
            json={
                "email": test_user.email,
                "password": "testpassword123",  # Correct password
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == test_user.email
        assert "password" not in data["user"]

    @pytest.mark.asyncio
    async def test_signin_wrong_password(self, client: AsyncClient, test_user: User):
        """Test signin with wrong password fails."""
        response = await client.post(
            "/api/auth/signin",
            json={
                "email": test_user.email,
                "password": "wrongpassword",
            },
        )

        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "incorrect" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_signin_nonexistent_user(self, client: AsyncClient):
        """Test signin with non-existent user fails."""
        response = await client.post(
            "/api/auth/signin",
            json={
                "email": "nonexistent@example.com",
                "password": "somepassword123",
            },
        )

        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_signin_missing_credentials(self, client: AsyncClient):
        """Test signin without credentials fails."""
        response = await client.post(
            "/api/auth/signin",
            json={},
        )

        assert response.status_code == 422  # Validation error


class TestJWTTokenVerification:
    """Test JWT token verification."""

    @pytest.mark.asyncio
    async def test_verify_valid_token(self, test_user_token: str):
        """Test verification of valid JWT token."""
        from app.middleware.auth import verify_token

        payload = verify_token(test_user_token)
        assert "sub" in payload
        assert payload["sub"] == "test_user_123"

    @pytest.mark.asyncio
    async def test_verify_invalid_token(self):
        """Test verification of invalid JWT token fails."""
        from fastapi import HTTPException

        from app.middleware.auth import verify_token

        with pytest.raises(HTTPException) as exc_info:
            verify_token("invalid.token.here")

        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_verify_expired_token(self):
        """Test verification of expired JWT token fails."""
        from datetime import timedelta

        from fastapi import HTTPException

        from app.middleware.auth import create_access_token, verify_token

        # Create token that expires immediately
        expired_token = create_access_token(
            {"sub": "test_user_123"},
            expires_delta=timedelta(seconds=-1),  # Already expired
        )

        with pytest.raises(HTTPException) as exc_info:
            verify_token(expired_token)

        assert exc_info.value.status_code == 401


class TestProtectedEndpoints:
    """Test protected endpoint access with JWT authentication."""

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_valid_token(
        self, client: AsyncClient, test_user: User, test_user_token: str
    ):
        """Test accessing protected endpoint with valid token succeeds."""
        response = await client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        # Should succeed (200) or return empty list if no tasks
        # Implementation will determine exact behavior
        assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_protected_endpoint_without_token(
        self, client: AsyncClient, test_user: User
    ):
        """Test accessing protected endpoint without token fails."""
        response = await client.get(f"/api/{test_user.id}/tasks")

        assert response.status_code == 403  # Forbidden (no credentials)

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_invalid_token(
        self, client: AsyncClient, test_user: User
    ):
        """Test accessing protected endpoint with invalid token fails."""
        response = await client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": "Bearer invalid.token.here"},
        )

        assert response.status_code == 401  # Unauthorized

    @pytest.mark.asyncio
    async def test_protected_endpoint_user_id_mismatch(
        self,
        client: AsyncClient,
        test_user: User,
        another_test_user: User,
        test_user_token: str,
    ):
        """Test accessing another user's resources fails (user isolation)."""
        # Try to access another user's tasks with test_user's token
        response = await client.get(
            f"/api/{another_test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 403  # Forbidden (user_id mismatch)
        data = response.json()
        assert "detail" in data
        assert "mismatch" in data["detail"].lower()
