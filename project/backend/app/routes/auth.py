"""Authentication routes.

Handles user signup and signin with JWT token generation.
"""

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.middleware.auth import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import AuthResponse, SigninRequest, SignupRequest, UserResponse

router = APIRouter()


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: SignupRequest,
    session: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """Create a new user account.

    Args:
        signup_data: User signup information (email, password, name)
        session: Database session

    Returns:
        AuthResponse: JWT token and user information

    Raises:
        HTTPException: 400 if email already exists
    """
    # Check if user with email already exists
    result = await session.execute(select(User).where(User.email == signup_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Create new user with hashed password
    user = User(
        id=f"user_{uuid.uuid4().hex[:12]}",  # Generate unique user ID
        email=signup_data.email,
        password=hash_password(signup_data.password),
        name=signup_data.name,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Generate JWT token
    access_token = create_access_token({"sub": user.id})

    # Return token and user info (without password)
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at.isoformat() + "Z",
            updated_at=user.updated_at.isoformat() + "Z",
        ),
    )


@router.post("/signin", response_model=AuthResponse)
async def signin(
    signin_data: SigninRequest,
    session: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """Authenticate user and return JWT token.

    Args:
        signin_data: User signin credentials (email, password)
        session: Database session

    Returns:
        AuthResponse: JWT token and user information

    Raises:
        HTTPException: 401 if credentials are incorrect
    """
    # Find user by email
    result = await session.execute(select(User).where(User.email == signin_data.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Verify password
    if not verify_password(signin_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Generate JWT token
    access_token = create_access_token({"sub": user.id})

    # Return token and user info (without password)
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at.isoformat() + "Z",
            updated_at=user.updated_at.isoformat() + "Z",
        ),
    )
