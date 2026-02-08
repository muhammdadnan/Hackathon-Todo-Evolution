"""Authentication middleware and JWT utilities.

Provides JWT token verification, password hashing, and authentication
dependencies for FastAPI endpoints.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()

# Get settings
settings = get_settings()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password

    Example:
        hashed = hash_password("my_secure_password")
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise

    Example:
        is_valid = verify_password("my_password", hashed_password)
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token.

    Args:
        data: Data to encode in the token (typically {"sub": user_id})
        expires_delta: Optional expiration time delta

    Returns:
        str: Encoded JWT token

    Example:
        token = create_access_token({"sub": "user_123"})
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.better_auth_secret,
        algorithm=settings.jwt_algorithm,
    )

    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify and decode a JWT token.

    Args:
        token: JWT token string

    Returns:
        dict: Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Get current user ID from JWT token.

    This is a FastAPI dependency that extracts and validates the JWT token
    from the Authorization header and returns the user ID.

    Args:
        credentials: HTTP Bearer credentials from request header

    Returns:
        str: User ID from token

    Raises:
        HTTPException: If token is invalid or user_id not found

    Example:
        @app.get("/protected")
        async def protected_route(user_id: str = Depends(get_current_user_id)):
            return {"user_id": user_id}
    """
    token = credentials.credentials
    payload = verify_token(token)

    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


def verify_user_access(
    path_user_id: str,
    token_user_id: str = Depends(get_current_user_id),
) -> str:
    """Verify that the authenticated user matches the path user_id.

    This dependency ensures user isolation by checking that the user_id
    in the JWT token matches the user_id in the URL path.

    Args:
        path_user_id: User ID from URL path parameter
        token_user_id: User ID from JWT token (injected by dependency)

    Returns:
        str: Verified user ID

    Raises:
        HTTPException: If user IDs don't match (403 Forbidden)

    Example:
        @app.get("/api/{user_id}/tasks")
        async def get_tasks(
            user_id: str = Depends(verify_user_access)
        ):
            # user_id is verified to match JWT token
            return await fetch_tasks(user_id)
    """
    if path_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    return token_user_id
