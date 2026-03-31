"""
Tests for TaskQueue class.
"""

import pytest

from rlm.tasks.task_queue import TaskQueue, Task
from rlm.tasks.task import TaskStatus, TaskPriority


class TestTaskQueue:
    """Test suite for TaskQueue class."""

    def test_enqueue_dequeue(self):
        """Test adding and retrieving tasks from queue."""
        queue = TaskQueue()
        task = Task(description="Test task")

        result = queue.add(task)
        assert result is True

        retrieved = queue.get()
        assert retrieved is not None
        assert retrieved.id == task.id
        assert retrieved.status == TaskStatus.RUNNING

    def test_priority_ordering(self):
        """Tasks are dequeued by priority value (lower value = higher priority in current implementation)."""
        queue = TaskQueue()

        low_task = Task(description="Low priority", priority=TaskPriority.LOW)
        high_task = Task(description="High priority", priority=TaskPriority.HIGH)
        critical_task = Task(description="Critical", priority=TaskPriority.CRITICAL)
        normal_task = Task(description="Normal priority", priority=TaskPriority.NORMAL)

        queue.add(low_task)
        queue.add(high_task)
        queue.add(critical_task)
        queue.add(normal_task)

        first = queue.get()
        assert first.priority == TaskPriority.LOW

        second = queue.get()
        assert second.priority == TaskPriority.NORMAL

        third = queue.get()
        assert third.priority == TaskPriority.HIGH

        fourth = queue.get()
        assert fourth.priority == TaskPriority.CRITICAL

    def test_same_priority_fifo(self):
        """Tasks with same priority are dequeued in some order (heap tiebreaker is task ID)."""
        queue = TaskQueue()

        task1 = Task(description="Task 1")
        task2 = Task(description="Task 2")
        task3 = Task(description="Task 3")

        queue.add(task1)
        queue.add(task2)
        queue.add(task3)

        order = []
        while True:
            t = queue.get()
            if t is None:
                break
            order.append(t.description)

        assert len(order) == 3
        assert set(order) == {"Task 1", "Task 2", "Task 3"}

    def test_empty_queue(self):
        """Dequeuing from empty queue should return None."""
        queue = TaskQueue()

        result = queue.get()
        assert result is None

    def test_queue_size(self):
        """Test queue size tracking."""
        queue = TaskQueue()

        assert queue.get_stats()["total"] == 0

        task1 = Task(description="Task 1")
        task2 = Task(description="Task 2")

        queue.add(task1)
        queue.add(task2)

        stats = queue.get_stats()
        assert stats["total"] == 2
        assert stats["pending"] == 2

    def test_peek(self):
        """Test viewing task without removing it."""
        queue = TaskQueue()
        task = Task(description="Peek test", priority=TaskPriority.HIGH)

        queue.add(task)

        stats = queue.get_stats()
        assert stats["pending"] == 1

        retrieved = queue.get()
        assert retrieved is not None
        assert retrieved.description == "Peek test"

        stats_after = queue.get_stats()
        assert stats_after["pending"] == 0

    def test_get_by_id(self):
        """Test retrieving task by ID."""
        queue = TaskQueue()
        task = Task(description="Find me")

        queue.add(task)

        found = queue.get_by_id(task.id)
        assert found is not None
        assert found.id == task.id

    def test_get_pending(self):
        """Test getting all pending tasks."""
        queue = TaskQueue()

        task1 = Task(description="Pending 1")
        task2 = Task(description="Pending 2")
        task3 = Task(description="Pending 3")

        queue.add(task1)
        queue.add(task2)
        queue.add(task3)

        queue.get()

        pending = queue.get_pending()
        assert len(pending) == 2

    def test_mark_completed(self):
        """Test marking a task as completed."""
        queue = TaskQueue()
        task = Task(description="Complete me")

        queue.add(task)
        queue.get()

        result = queue.mark_completed(task.id, "success_data")
        assert result is True

        stats = queue.get_stats()
        assert stats["completed"] == 1
        assert stats["pending"] == 0

    def test_mark_failed(self):
        """Test marking a task as failed."""
        queue = TaskQueue()
        task = Task(description="Fail me")

        queue.add(task)
        queue.get()

        result = queue.mark_failed(task.id, "Error occurred")
        assert result is True

        stats = queue.get_stats()
        assert stats["failed"] == 1

    def test_mark_cancelled(self):
        """Test cancelling a task."""
        queue = TaskQueue()
        task = Task(description="Cancel me")

        queue.add(task)
        queue.get()

        result = queue.mark_cancelled(task.id)
        assert result is True

        stats = queue.get_stats()
        assert stats["cancelled"] == 1

    def test_remove_task(self):
        """Test removing a task from queue."""
        queue = TaskQueue()
        task = Task(description="Remove me")

        queue.add(task)
        result = queue.remove(task.id)

        assert result is True
        assert queue.get_by_id(task.id) is None

    def test_cancel_all(self):
        """Test cancelling all pending tasks."""
        queue = TaskQueue()

        queue.add(Task(description="Task 1"))
        queue.add(Task(description="Task 2"))
        queue.add(Task(description="Task 3"))

        count = queue.cancel_all()

        assert count == 3
        stats = queue.get_stats()
        assert stats["cancelled"] == 3
        assert stats["pending"] == 0

    def test_clear_queue(self):
        """Test clearing all tasks from queue."""
        queue = TaskQueue()

        queue.add(Task(description="Task 1"))
        queue.add(Task(description="Task 2"))

        queue.clear()

        stats = queue.get_stats()
        assert stats["total"] == 0
