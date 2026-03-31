"""
Tests for Task, TaskStatus, and TaskPriority classes.
"""

import pytest
from datetime import datetime

from rlm.tasks.task import Task, TaskStatus, TaskPriority, TaskResult


class TestTask:
    """Test suite for Task class."""

    def test_task_creation(self):
        """Test task creation with default values."""
        task = Task(description="Test task")

        assert task.description == "Test task"
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.NORMAL
        assert task.id is not None
        assert task.created_at is not None
        assert task.started_at is None
        assert task.completed_at is None
        assert task.assigned_agent_id is None
        assert task.result is None
        assert task.parent_task_id is None
        assert task.child_task_ids == []
        assert task.dependencies == []
        assert task.metadata == {}
        assert task.retry_count == 0
        assert task.max_retries == 3

    def test_task_with_priority(self):
        """Test task creation with different priorities."""
        low_task = Task(description="Low priority", priority=TaskPriority.LOW)
        high_task = Task(description="High priority", priority=TaskPriority.HIGH)
        critical_task = Task(description="Critical", priority=TaskPriority.CRITICAL)

        assert low_task.priority == TaskPriority.LOW
        assert high_task.priority == TaskPriority.HIGH
        assert critical_task.priority == TaskPriority.CRITICAL

    def test_task_status_transitions(self):
        """Test task status transitions: pending -> running -> completed."""
        task = Task(description="Status test task")

        assert task.status == TaskStatus.PENDING

        task.mark_started("agent_123")
        assert task.status == TaskStatus.RUNNING
        assert task.started_at is not None
        assert task.assigned_agent_id == "agent_123"

        task.mark_completed("result_data")
        assert task.status == TaskStatus.COMPLETED
        assert task.completed_at is not None
        assert task.result is not None
        assert task.result.success is True
        assert task.result.output == "result_data"

    def test_task_result(self):
        """Test TaskResult object creation and properties."""
        result = TaskResult(
            task_id="task_123",
            success=True,
            output={"data": "value"},
            error=None,
            execution_time_ms=150.5,
        )

        assert result.task_id == "task_123"
        assert result.success is True
        assert result.output == {"data": "value"}
        assert result.error is None
        assert result.execution_time_ms == 150.5

    def test_task_from_dict(self):
        """Test creating a task from a dictionary."""
        data = {
            "id": "custom_id",
            "description": "From dict",
            "priority": 3,
            "status": "running",
            "parent_task_id": "parent_123",
            "dependencies": ["dep_1", "dep_2"],
            "metadata": {"custom": "meta"},
            "retry_count": 1,
            "max_retries": 5,
        }

        task = Task.from_dict(data)

        assert task.id == "custom_id"
        assert task.description == "From dict"
        assert task.priority == TaskPriority.HIGH
        assert task.status == TaskStatus.RUNNING
        assert task.parent_task_id == "parent_123"
        assert task.dependencies == ["dep_1", "dep_2"]
        assert task.metadata == {"custom": "meta"}
        assert task.retry_count == 1
        assert task.max_retries == 5

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            id="test_id",
            description="To dict test",
            priority=TaskPriority.CRITICAL,
        )

        task_dict = task.to_dict()

        assert task_dict["id"] == "test_id"
        assert task_dict["description"] == "To dict test"
        assert task_dict["priority"] == 4
        assert task_dict["status"] == "pending"
        assert task_dict["created_at"] is not None

    def test_task_mark_failed(self):
        """Test marking a task as failed."""
        task = Task(description="Fail test")
        task.mark_started("agent_1")

        task.mark_failed("Connection timeout")

        assert task.status == TaskStatus.FAILED
        assert task.result is not None
        assert task.result.success is False
        assert task.result.error == "Connection timeout"

    def test_task_mark_cancelled(self):
        """Test marking a task as cancelled."""
        task = Task(description="Cancel test")

        task.mark_cancelled()

        assert task.status == TaskStatus.CANCELLED
        assert task.completed_at is not None

    def test_task_is_ready(self):
        """Test is_ready method with dependencies."""
        task = Task(description="Ready test", dependencies=["dep_1", "dep_2"])

        assert task.is_ready([]) is False
        assert task.is_ready(["dep_1"]) is False
        assert task.is_ready(["dep_1", "dep_2"]) is True

    def test_task_can_retry(self):
        """Test can_retry method."""
        task = Task(description="Retry test", max_retries=3)

        assert task.can_retry() is True

        task.retry_count = 2
        assert task.can_retry() is True

        task.retry_count = 3
        assert task.can_retry() is False

    def test_task_add_child(self):
        """Test adding child task IDs."""
        parent = Task(description="Parent")
        child_id = "child_123"

        parent.add_child(child_id)

        assert child_id in parent.child_task_ids
        assert len(parent.child_task_ids) == 1

    def test_task_increment_retry(self):
        """Test incrementing retry count."""
        task = Task(description="Retry count test")
        initial_count = task.retry_count

        task.increment_retry()

        assert task.retry_count == initial_count + 1

    def test_task_with_timeout(self):
        """Test task with timeout set."""
        task = Task(description="Timeout test", timeout_seconds=30.0)

        assert task.timeout_seconds == 30.0
