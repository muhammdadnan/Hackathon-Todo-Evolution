"""Task routes.

Handles task CRUD operations with user authentication and isolation.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.middleware.auth import verify_user_access
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=list[TaskResponse])
async def list_tasks(
    user_id: str = Depends(verify_user_access),
    completed: Optional[bool] = Query(default=None, description="Filter by completion status"),
    session: AsyncSession = Depends(get_session),
) -> list[TaskResponse]:
    """List all tasks for authenticated user.

    Args:
        user_id: User ID from JWT token (verified by dependency)
        completed: Optional filter for completion status (true/false)
        session: Database session

    Returns:
        list[TaskResponse]: List of tasks belonging to the user

    Raises:
        HTTPException: 401 if not authenticated, 403 if user_id mismatch
    """
    # Build query to get user's tasks
    query = select(Task).where(Task.user_id == user_id)

    # Apply completion filter if provided
    if completed is not None:
        query = query.where(Task.completed == completed)

    # Order by created_at descending (newest first)
    query = query.order_by(Task.created_at.desc())

    # Execute query
    result = await session.execute(query)
    tasks = result.scalars().all()

    # Convert to response models
    return [
        TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat() + "Z",
            updated_at=task.updated_at.isoformat() + "Z",
        )
        for task in tasks
    ]


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Create a new task for authenticated user.

    Args:
        task_data: Task creation data (title, description)
        user_id: User ID from JWT token (verified by dependency)
        session: Database session

    Returns:
        TaskResponse: Created task

    Raises:
        HTTPException: 401 if not authenticated, 403 if user_id mismatch, 422 if validation fails
    """
    # Create new task
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    # Return response
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat() + "Z",
        updated_at=task.updated_at.isoformat() + "Z",
    )


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: int,
    user_id: str = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Toggle task completion status.

    Args:
        task_id: Task ID to toggle
        user_id: User ID from JWT token (verified by dependency)
        session: Database session

    Returns:
        TaskResponse: Updated task with toggled completion status

    Raises:
        HTTPException: 401 if not authenticated, 403 if user_id mismatch or task doesn't belong to user, 404 if task not found
    """
    # Find task by id
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Verify task belongs to authenticated user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: task does not belong to user",
        )

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    # Return response
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat() + "Z",
        updated_at=task.updated_at.isoformat() + "Z",
    )


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Update task details (title and/or description).

    Args:
        task_id: Task ID to update
        task_data: Task update data (title and/or description)
        user_id: User ID from JWT token (verified by dependency)
        session: Database session

    Returns:
        TaskResponse: Updated task

    Raises:
        HTTPException: 401 if not authenticated, 403 if user_id mismatch or task doesn't belong to user, 404 if task not found, 422 if validation fails
    """
    # Find task by id
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Verify task belongs to authenticated user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: task does not belong to user",
        )

    # Update task fields
    task.title = task_data.title
    task.description = task_data.description
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    # Return response
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat() + "Z",
        updated_at=task.updated_at.isoformat() + "Z",
    )


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: str = Depends(verify_user_access),
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a task.

    Args:
        task_id: Task ID to delete
        user_id: User ID from JWT token (verified by dependency)
        session: Database session

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 401 if not authenticated, 403 if user_id mismatch or task doesn't belong to user, 404 if task not found
    """
    # Find task by id
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Verify task belongs to authenticated user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: task does not belong to user",
        )

    # Delete task
    await session.delete(task)
    await session.commit()

    # Return 204 No Content (no response body)
