"""Task endpoint tests.

Tests for task CRUD operations including listing, creating, updating, and deleting tasks.
Following TDD RED phase - these tests should FAIL until implementation is complete.
"""

import pytest
from httpx import AsyncClient

from app.models.task import Task
from app.models.user import User


class TestListTasks:
    """Test listing tasks for a user (User Story 2)."""

    @pytest.mark.asyncio
    async def test_list_tasks_success(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test listing all tasks for authenticated user."""
        response = await client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        # Verify task structure
        task = data[0]
        assert "id" in task
        assert "user_id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "created_at" in task
        assert "updated_at" in task

        # Verify task belongs to user
        assert task["user_id"] == test_user.id

    @pytest.mark.asyncio
    async def test_list_tasks_empty(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
    ):
        """Test listing tasks when user has no tasks."""
        response = await client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_list_tasks_multiple(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_session,
    ):
        """Test listing multiple tasks."""
        # Create multiple tasks
        tasks = [
            Task(
                user_id=test_user.id,
                title=f"Task {i}",
                description=f"Description {i}",
                completed=i % 2 == 0,  # Alternate completed status
            )
            for i in range(5)
        ]

        for task in tasks:
            test_session.add(task)
        await test_session.commit()

        response = await client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

    @pytest.mark.asyncio
    async def test_list_tasks_without_token(
        self,
        client: AsyncClient,
        test_user: User,
    ):
        """Test listing tasks without authentication fails."""
        response = await client.get(f"/api/{test_user.id}/tasks")

        assert response.status_code == 403  # Forbidden

    @pytest.mark.asyncio
    async def test_list_tasks_invalid_token(
        self,
        client: AsyncClient,
        test_user: User,
    ):
        """Test listing tasks with invalid token fails."""
        response = await client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": "Bearer invalid.token.here"},
        )

        assert response.status_code == 401  # Unauthorized


class TestUserIsolation:
    """Test user isolation for task operations (User Story 2)."""

    @pytest.mark.asyncio
    async def test_user_cannot_list_other_users_tasks(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        another_test_user: User,
        test_session,
    ):
        """Test that users can only see their own tasks."""
        # Create task for another user
        other_task = Task(
            user_id=another_test_user.id,
            title="Other user's task",
            description="Should not be visible",
            completed=False,
        )
        test_session.add(other_task)
        await test_session.commit()

        # Try to access another user's tasks with test_user's token
        response = await client.get(
            f"/api/{another_test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 403  # Forbidden
        data = response.json()
        assert "detail" in data
        assert "mismatch" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_user_only_sees_own_tasks(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        another_test_user: User,
        test_session,
    ):
        """Test that user only sees their own tasks, not others'."""
        # Create tasks for test_user
        user_task = Task(
            user_id=test_user.id,
            title="My task",
            description="My description",
            completed=False,
        )
        test_session.add(user_task)

        # Create tasks for another_test_user
        other_task = Task(
            user_id=another_test_user.id,
            title="Other user's task",
            description="Should not be visible",
            completed=False,
        )
        test_session.add(other_task)
        await test_session.commit()

        # Get test_user's tasks
        response = await client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 200
        data = response.json()

        # Should only see own task
        assert len(data) == 1
        assert data[0]["user_id"] == test_user.id
        assert data[0]["title"] == "My task"


class TestTaskOrdering:
    """Test task ordering and sorting."""

    @pytest.mark.asyncio
    async def test_tasks_ordered_by_created_at_desc(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_session,
    ):
        """Test that tasks are ordered by creation date (newest first)."""
        import asyncio
        from datetime import datetime, timedelta

        # Create tasks with different timestamps
        base_time = datetime.utcnow()
        tasks = []
        for i in range(3):
            task = Task(
                user_id=test_user.id,
                title=f"Task {i}",
                description=f"Description {i}",
                completed=False,
            )
            # Manually set created_at to ensure ordering
            task.created_at = base_time - timedelta(hours=i)
            tasks.append(task)
            test_session.add(task)

        await test_session.commit()

        response = await client.get(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 200
        data = response.json()

        # Verify tasks are ordered by created_at descending (newest first)
        assert len(data) == 3
        # Task 0 has the most recent timestamp
        assert data[0]["title"] == "Task 0"
        assert data[1]["title"] == "Task 1"
        assert data[2]["title"] == "Task 2"


class TestTaskFiltering:
    """Test filtering tasks by completion status."""

    @pytest.mark.asyncio
    async def test_filter_completed_tasks(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_session,
    ):
        """Test filtering to show only completed tasks."""
        # Create mix of completed and pending tasks
        tasks = [
            Task(user_id=test_user.id, title="Task 1", completed=True),
            Task(user_id=test_user.id, title="Task 2", completed=False),
            Task(user_id=test_user.id, title="Task 3", completed=True),
        ]
        for task in tasks:
            test_session.add(task)
        await test_session.commit()

        # Filter for completed tasks
        response = await client.get(
            f"/api/{test_user.id}/tasks?completed=true",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(task["completed"] is True for task in data)

    @pytest.mark.asyncio
    async def test_filter_pending_tasks(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_session,
    ):
        """Test filtering to show only pending tasks."""
        # Create mix of completed and pending tasks
        tasks = [
            Task(user_id=test_user.id, title="Task 1", completed=True),
            Task(user_id=test_user.id, title="Task 2", completed=False),
            Task(user_id=test_user.id, title="Task 3", completed=False),
        ]
        for task in tasks:
            test_session.add(task)
        await test_session.commit()

        # Filter for pending tasks
        response = await client.get(
            f"/api/{test_user.id}/tasks?completed=false",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(task["completed"] is False for task in data)


class TestCreateTask:
    """Test creating tasks (User Story 3)."""

    @pytest.mark.asyncio
    async def test_create_task_success(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
    ):
        """Test creating a task with title and description."""
        task_data = {
            "title": "New Task",
            "description": "Task description",
        }

        response = await client.post(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=task_data,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["description"] == "Task description"
        assert data["user_id"] == test_user.id
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    @pytest.mark.asyncio
    async def test_create_task_without_description(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
    ):
        """Test creating a task with only title (description optional)."""
        task_data = {
            "title": "Task without description",
        }

        response = await client.post(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=task_data,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Task without description"
        assert data["description"] is None
        assert data["user_id"] == test_user.id

    @pytest.mark.asyncio
    async def test_create_task_missing_title(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
    ):
        """Test creating a task without title fails."""
        task_data = {
            "description": "Description without title",
        }

        response = await client.post(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=task_data,
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_task_empty_title(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
    ):
        """Test creating a task with empty title fails."""
        task_data = {
            "title": "",
            "description": "Description",
        }

        response = await client.post(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=task_data,
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_task_title_too_long(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
    ):
        """Test creating a task with title > 200 characters fails."""
        task_data = {
            "title": "x" * 201,  # Exceeds max length
            "description": "Description",
        }

        response = await client.post(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=task_data,
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_task_description_too_long(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
    ):
        """Test creating a task with description > 1000 characters fails."""
        task_data = {
            "title": "Valid title",
            "description": "x" * 1001,  # Exceeds max length
        }

        response = await client.post(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=task_data,
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_task_without_token(
        self,
        client: AsyncClient,
        test_user: User,
    ):
        """Test creating a task without authentication fails."""
        task_data = {
            "title": "New Task",
            "description": "Description",
        }

        response = await client.post(
            f"/api/{test_user.id}/tasks",
            json=task_data,
        )

        assert response.status_code == 403  # Forbidden

    @pytest.mark.asyncio
    async def test_create_task_user_id_mismatch(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        another_test_user: User,
    ):
        """Test creating a task for another user fails."""
        task_data = {
            "title": "New Task",
            "description": "Description",
        }

        # Try to create task for another_test_user with test_user's token
        response = await client.post(
            f"/api/{another_test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=task_data,
        )

        assert response.status_code == 403  # Forbidden
        data = response.json()
        assert "mismatch" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_create_task_sets_correct_user_id(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_session,
    ):
        """Test that created task has correct user_id."""
        task_data = {
            "title": "New Task",
            "description": "Description",
        }

        response = await client.post(
            f"/api/{test_user.id}/tasks",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=task_data,
        )

        assert response.status_code == 201
        data = response.json()

        # Verify task in database has correct user_id
        from sqlmodel import select
        result = await test_session.execute(
            select(Task).where(Task.id == data["id"])
        )
        task = result.scalar_one()
        assert task.user_id == test_user.id


class TestToggleTaskCompletion:
    """Test toggling task completion status (User Story 4)."""

    @pytest.mark.asyncio
    async def test_toggle_task_to_completed(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test marking a pending task as completed."""
        # Ensure task starts as pending
        assert test_task.completed is False

        response = await client.patch(
            f"/api/{test_user.id}/tasks/{test_task.id}/complete",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_task.id
        assert data["completed"] is True
        assert data["title"] == test_task.title

    @pytest.mark.asyncio
    async def test_toggle_task_to_pending(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_session,
    ):
        """Test marking a completed task as pending."""
        # Create a completed task
        completed_task = Task(
            user_id=test_user.id,
            title="Completed Task",
            description="Already done",
            completed=True,
        )
        test_session.add(completed_task)
        await test_session.commit()
        await test_session.refresh(completed_task)

        response = await client.patch(
            f"/api/{test_user.id}/tasks/{completed_task.id}/complete",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == completed_task.id
        assert data["completed"] is False

    @pytest.mark.asyncio
    async def test_toggle_completion_persists(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
        test_session,
    ):
        """Test that completion status persists in database."""
        # Toggle to completed
        response = await client.patch(
            f"/api/{test_user.id}/tasks/{test_task.id}/complete",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        assert response.status_code == 200

        # Verify in database
        from sqlmodel import select
        result = await test_session.execute(
            select(Task).where(Task.id == test_task.id)
        )
        task = result.scalar_one()
        assert task.completed is True

    @pytest.mark.asyncio
    async def test_toggle_completion_without_token(
        self,
        client: AsyncClient,
        test_user: User,
        test_task: Task,
    ):
        """Test toggling completion without authentication fails."""
        response = await client.patch(
            f"/api/{test_user.id}/tasks/{test_task.id}/complete"
        )

        assert response.status_code == 403  # Forbidden

    @pytest.mark.asyncio
    async def test_toggle_completion_user_id_mismatch(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        another_test_user: User,
        test_session,
    ):
        """Test cannot toggle another user's task."""
        # Create task for another user
        other_task = Task(
            user_id=another_test_user.id,
            title="Other user's task",
            completed=False,
        )
        test_session.add(other_task)
        await test_session.commit()
        await test_session.refresh(other_task)

        # Try to toggle with test_user's token
        response = await client.patch(
            f"/api/{another_test_user.id}/tasks/{other_task.id}/complete",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 403  # Forbidden

    @pytest.mark.asyncio
    async def test_toggle_completion_task_not_found(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
    ):
        """Test toggling non-existent task returns 404."""
        response = await client.patch(
            f"/api/{test_user.id}/tasks/99999/complete",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_toggle_completion_updates_timestamp(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test that toggling completion updates updated_at timestamp."""
        original_updated_at = test_task.updated_at

        # Small delay to ensure timestamp difference
        import asyncio
        await asyncio.sleep(0.1)

        response = await client.patch(
            f"/api/{test_user.id}/tasks/{test_task.id}/complete",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 200
        data = response.json()

        # Parse timestamps and compare
        from datetime import datetime
        new_updated_at = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
        assert new_updated_at > original_updated_at


class TestUpdateTask:
    """Test updating task details (User Story 5)."""

    @pytest.mark.asyncio
    async def test_update_task_title_only(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test updating only the task title."""
        update_data = {
            "title": "Updated Task Title",
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_task.id
        assert data["title"] == "Updated Task Title"
        assert data["description"] == test_task.description  # Unchanged

    @pytest.mark.asyncio
    async def test_update_task_description_only(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test updating only the task description."""
        update_data = {
            "description": "Updated task description",
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_task.id
        assert data["title"] == test_task.title  # Unchanged
        assert data["description"] == "Updated task description"

    @pytest.mark.asyncio
    async def test_update_task_both_fields(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test updating both title and description."""
        update_data = {
            "title": "New Title",
            "description": "New Description",
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_task.id
        assert data["title"] == "New Title"
        assert data["description"] == "New Description"

    @pytest.mark.asyncio
    async def test_update_task_persists(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
        test_session,
    ):
        """Test that task updates persist in database."""
        update_data = {
            "title": "Persisted Title",
            "description": "Persisted Description",
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )
        assert response.status_code == 200

        # Verify in database
        from sqlmodel import select
        result = await test_session.execute(
            select(Task).where(Task.id == test_task.id)
        )
        task = result.scalar_one()
        assert task.title == "Persisted Title"
        assert task.description == "Persisted Description"

    @pytest.mark.asyncio
    async def test_update_task_empty_title(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test updating task with empty title fails."""
        update_data = {
            "title": "",
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_update_task_title_too_long(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test updating task with title > 200 characters fails."""
        update_data = {
            "title": "x" * 201,
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_update_task_description_too_long(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test updating task with description > 1000 characters fails."""
        update_data = {
            "description": "x" * 1001,
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_update_task_without_token(
        self,
        client: AsyncClient,
        test_user: User,
        test_task: Task,
    ):
        """Test updating task without authentication fails."""
        update_data = {
            "title": "New Title",
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            json=update_data,
        )

        assert response.status_code == 403  # Forbidden

    @pytest.mark.asyncio
    async def test_update_task_user_id_mismatch(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        another_test_user: User,
        test_session,
    ):
        """Test cannot update another user's task."""
        # Create task for another user
        other_task = Task(
            user_id=another_test_user.id,
            title="Other user's task",
            completed=False,
        )
        test_session.add(other_task)
        await test_session.commit()
        await test_session.refresh(other_task)

        update_data = {
            "title": "Trying to update",
        }

        # Try to update with test_user's token
        response = await client.put(
            f"/api/{another_test_user.id}/tasks/{other_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )

        assert response.status_code == 403  # Forbidden

    @pytest.mark.asyncio
    async def test_update_task_not_found(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
    ):
        """Test updating non-existent task returns 404."""
        update_data = {
            "title": "New Title",
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/99999",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_task_updates_timestamp(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test that updating task updates updated_at timestamp."""
        original_updated_at = test_task.updated_at

        # Small delay to ensure timestamp difference
        import asyncio
        await asyncio.sleep(0.1)

        update_data = {
            "title": "Updated Title",
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )

        assert response.status_code == 200
        data = response.json()

        # Parse timestamps and compare
        from datetime import datetime
        new_updated_at = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
        assert new_updated_at > original_updated_at

    @pytest.mark.asyncio
    async def test_update_task_clear_description(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test clearing task description by setting to null."""
        update_data = {
            "description": None,
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["description"] is None

    @pytest.mark.asyncio
    async def test_update_task_does_not_change_completion(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_session,
    ):
        """Test that updating task does not change completion status."""
        # Create a completed task
        completed_task = Task(
            user_id=test_user.id,
            title="Completed Task",
            description="Done",
            completed=True,
        )
        test_session.add(completed_task)
        await test_session.commit()
        await test_session.refresh(completed_task)

        update_data = {
            "title": "Updated Completed Task",
        }

        response = await client.put(
            f"/api/{test_user.id}/tasks/{completed_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
            json=update_data,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True  # Should remain completed


class TestDeleteTask:
    """Test deleting tasks (User Story 6)."""

    @pytest.mark.asyncio
    async def test_delete_task_success(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
    ):
        """Test successfully deleting a task."""
        response = await client.delete(
            f"/api/{test_user.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 204  # No Content

    @pytest.mark.asyncio
    async def test_delete_task_removes_from_database(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_task: Task,
        test_session,
    ):
        """Test that deleted task is removed from database."""
        task_id = test_task.id

        # Delete task
        response = await client.delete(
            f"/api/{test_user.id}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        assert response.status_code == 204

        # Verify task no longer exists in database
        from sqlmodel import select
        result = await test_session.execute(
            select(Task).where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()
        assert task is None

    @pytest.mark.asyncio
    async def test_delete_task_without_token(
        self,
        client: AsyncClient,
        test_user: User,
        test_task: Task,
    ):
        """Test deleting task without authentication fails."""
        response = await client.delete(
            f"/api/{test_user.id}/tasks/{test_task.id}"
        )

        assert response.status_code == 403  # Forbidden

    @pytest.mark.asyncio
    async def test_delete_task_user_id_mismatch(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        another_test_user: User,
        test_session,
    ):
        """Test cannot delete another user's task."""
        # Create task for another user
        other_task = Task(
            user_id=another_test_user.id,
            title="Other user's task",
            completed=False,
        )
        test_session.add(other_task)
        await test_session.commit()
        await test_session.refresh(other_task)

        # Try to delete with test_user's token
        response = await client.delete(
            f"/api/{another_test_user.id}/tasks/{other_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 403  # Forbidden

    @pytest.mark.asyncio
    async def test_delete_task_not_found(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
    ):
        """Test deleting non-existent task returns 404."""
        response = await client.delete(
            f"/api/{test_user.id}/tasks/99999",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_completed_task(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_session,
    ):
        """Test deleting a completed task works."""
        # Create a completed task
        completed_task = Task(
            user_id=test_user.id,
            title="Completed Task",
            description="Done",
            completed=True,
        )
        test_session.add(completed_task)
        await test_session.commit()
        await test_session.refresh(completed_task)

        response = await client.delete(
            f"/api/{test_user.id}/tasks/{completed_task.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_task_does_not_affect_other_tasks(
        self,
        client: AsyncClient,
        test_user: User,
        test_user_token: str,
        test_session,
    ):
        """Test that deleting one task doesn't affect other tasks."""
        # Create multiple tasks
        task1 = Task(user_id=test_user.id, title="Task 1", completed=False)
        task2 = Task(user_id=test_user.id, title="Task 2", completed=False)
        task3 = Task(user_id=test_user.id, title="Task 3", completed=False)

        test_session.add(task1)
        test_session.add(task2)
        test_session.add(task3)
        await test_session.commit()
        await test_session.refresh(task1)
        await test_session.refresh(task2)
        await test_session.refresh(task3)

        # Delete task2
        response = await client.delete(
            f"/api/{test_user.id}/tasks/{task2.id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        assert response.status_code == 204

        # Verify task1 and task3 still exist
        from sqlmodel import select
        result = await test_session.execute(
            select(Task).where(Task.user_id == test_user.id)
        )
        remaining_tasks = result.scalars().all()
        assert len(remaining_tasks) == 2
        remaining_ids = [t.id for t in remaining_tasks]
        assert task1.id in remaining_ids
        assert task3.id in remaining_ids
        assert task2.id not in remaining_ids
