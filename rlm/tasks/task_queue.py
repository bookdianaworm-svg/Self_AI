"""
Task Queue for managing task execution.

This module provides the TaskQueue class for managing
pending tasks and their prioritization.
"""

import heapq
import threading
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional

from rlm.tasks.task import Task, TaskStatus, TaskPriority


class TaskQueue:
    """
    Priority queue for tasks with dependency management.

    The task queue handles:
    - Priority-based task ordering
    - Dependency tracking
    - Task state management
    """

    def __init__(self):
        """Initialize the task queue."""
        self._tasks: Dict[str, Task] = {}
        self._heap: List[tuple[int, str]] = []  # (priority, task_id)
        self._task_index: Dict[str, int] = {}  # task_id -> heap index
        self._lock = threading.Lock()
        self._callbacks: Dict[str, List[Callable]] = defaultdict(list)

    def add(self, task: Task) -> bool:
        """
        Add a task to the queue.

        Args:
            task: Task to add.

        Returns:
            True if added successfully.
        """
        with self._lock:
            if task.id in self._tasks:
                return False

            self._tasks[task.id] = task
            self._add_to_heap(task)
            return True

    def _add_to_heap(self, task: Task) -> None:
        """Add task to heap maintaining priority order."""
        entry = (task.priority.value, task.id)
        heapq.heappush(self._heap, entry)
        self._task_index[task.id] = len(self._heap) - 1

    def get(self) -> Optional[Task]:
        """
        Get the highest priority task that's ready.

        Returns:
            The highest priority ready task, or None if queue is empty.
        """
        with self._lock:
            while self._heap:
                _, task_id = self._heap[0]

                # Check if task still exists
                if task_id not in self._tasks:
                    heapq.heappop(self._heap)
                    continue

                task = self._tasks[task_id]

                # Skip if not pending
                if task.status != TaskStatus.PENDING:
                    heapq.heappop(self._heap)
                    continue

                # Task is ready - mark as running
                task.status = TaskStatus.RUNNING
                heapq.heappop(self._heap)
                return task

            return None

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a task by ID.

        Args:
            task_id: ID of the task.

        Returns:
            The task or None if not found.
        """
        return self._tasks.get(task_id)

    def get_pending(self) -> List[Task]:
        """
        Get all pending tasks.

        Returns:
            List of pending tasks.
        """
        with self._lock:
            return [
                task
                for task in self._tasks.values()
                if task.status == TaskStatus.PENDING
            ]

    def get_ready_tasks(self) -> List[Task]:
        """
        Get tasks that are ready to execute.

        A task is ready if:
        - It is pending
        - All dependencies are completed

        Returns:
            List of ready tasks.
        """
        completed = [
            task_id
            for task_id, task in self._tasks.items()
            if task.status == TaskStatus.COMPLETED
        ]

        with self._lock:
            return [
                task
                for task in self._tasks.values()
                if task.status == TaskStatus.PENDING and task.is_ready(completed)
            ]

    def mark_completed(self, task_id: str, result: Any) -> bool:
        """
        Mark a task as completed.

        Args:
            task_id: ID of the task.
            result: Result of the task.

        Returns:
            True if marked, False if not found.
        """
        task = self._tasks.get(task_id)
        if not task:
            return False

        with self._lock:
            task.mark_completed(result)
            self._notify_callbacks("completed", task)

        return True

    def mark_failed(self, task_id: str, error: str) -> bool:
        """
        Mark a task as failed.

        Args:
            task_id: ID of the task.
            error: Error message.

        Returns:
            True if marked, False if not found.
        """
        task = self._tasks.get(task_id)
        if not task:
            return False

        with self._lock:
            task.mark_failed(error)
            self._notify_callbacks("failed", task)

        return True

    def mark_cancelled(self, task_id: str) -> bool:
        """
        Mark a task as cancelled.

        Args:
            task_id: ID of the task.

        Returns:
            True if marked, False if not found.
        """
        task = self._tasks.get(task_id)
        if not task:
            return False

        with self._lock:
            task.mark_cancelled()
            self._notify_callbacks("cancelled", task)

        return True

    def remove(self, task_id: str) -> bool:
        """
        Remove a task from the queue.

        Args:
            task_id: ID of the task to remove.

        Returns:
            True if removed, False if not found.
        """
        if task_id not in self._tasks:
            return False

        with self._lock:
            del self._tasks[task_id]
            return True

    def cancel_all(self) -> int:
        """
        Cancel all pending tasks.

        Returns:
            Number of tasks cancelled.
        """
        count = 0
        with self._lock:
            for task in self._tasks.values():
                if task.status == TaskStatus.PENDING:
                    task.mark_cancelled()
                    count += 1
        return count

    def get_stats(self) -> Dict[str, Any]:
        """
        Get queue statistics.

        Returns:
            Dictionary of statistics.
        """
        with self._lock:
            status_counts = defaultdict(int)
            for task in self._tasks.values():
                status_counts[task.status.value] += 1

            return {
                "total": len(self._tasks),
                "pending": status_counts[TaskStatus.PENDING.value],
                "running": status_counts[TaskStatus.RUNNING.value],
                "completed": status_counts[TaskStatus.COMPLETED.value],
                "failed": status_counts[TaskStatus.FAILED.value],
                "cancelled": status_counts[TaskStatus.CANCELLED.value],
            }

    def on_event(self, event: str, callback: Callable) -> None:
        """
        Register a callback for queue events.

        Args:
            event: Event type ("completed", "failed", "cancelled").
            callback: Callback function.
        """
        self._callbacks[event].append(callback)

    def _notify_callbacks(self, event: str, task: Task) -> None:
        """Notify registered callbacks of an event."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(task)
            except Exception:
                pass

    def clear(self) -> None:
        """Clear all tasks from the queue."""
        with self._lock:
            self._tasks.clear()
            self._heap.clear()
            self._task_index.clear()
