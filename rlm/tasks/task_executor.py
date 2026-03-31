"""
Task Executor for running tasks with agents.

This module provides the TaskExecutor class that coordinates
task execution with agents.
"""

import asyncio
import threading
import time
from typing import Any, Callable, Dict, List, Optional

from rlm.agents.base.base_agent import AgentConfig, BaseAgent
from rlm.agents.manager import AgentManager
from rlm.tasks.task import Task, TaskStatus
from rlm.tasks.task_queue import TaskQueue


class TaskExecutor:
    """
    Executor that coordinates task execution with agents.

    The task executor:
    - Pulls tasks from the queue
    - Assigns tasks to agents
    - Tracks execution state
    - Handles completion and failures
    """

    def __init__(
        self,
        agent_manager: AgentManager,
        task_queue: Optional[TaskQueue] = None,
        max_concurrent: int = 10,
    ):
        """
        Initialize the task executor.

        Args:
            agent_manager: Agent manager for running tasks.
            task_queue: Optional task queue (creates one if not provided).
            max_concurrent: Maximum concurrent task executions.
        """
        self._agent_manager = agent_manager
        self._task_queue = task_queue or TaskQueue()
        self._max_concurrent = max_concurrent
        self._running = False
        self._lock = threading.Lock()
        self._callbacks: Dict[str, List[Callable]] = {}
        self._active_tasks: Dict[str, str] = {}  # task_id -> agent_id

    def start(self) -> None:
        """Start the task executor."""
        self._running = True

    def stop(self) -> None:
        """Stop the task executor."""
        self._running = False

    def submit_task(
        self,
        description: str,
        priority: int = 2,
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Submit a new task for execution.

        Args:
            description: Task description.
            priority: Priority (1=low, 2=normal, 3=high, 4=critical).
            dependencies: List of task IDs this depends on.
            metadata: Additional task metadata.

        Returns:
            The task ID.
        """
        task = Task(
            description=description,
            priority=priority,
            dependencies=dependencies or [],
            metadata=metadata or {},
        )

        self._task_queue.add(task)
        self._notify_callbacks("submitted", task)

        return task.id

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by ID.

        Args:
            task_id: ID of the task.

        Returns:
            The task or None if not found.
        """
        return self._task_queue.get_by_id(task_id)

    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a task.

        Args:
            task_id: ID of the task to cancel.

        Returns:
            True if cancelled, False if not found.
        """
        return self._task_queue.mark_cancelled(task_id)

    def execute_next(self) -> Optional[str]:
        """
        Execute the next ready task.

        Returns:
            The task ID if executed, None if no task available.
        """
        if not self._running:
            return None

        # Check concurrent limit
        if len(self._active_tasks) >= self._max_concurrent:
            return None

        # Get next ready task
        task = self._task_queue.get()
        if not task:
            return None

        # Find available agent
        agent_id = self._find_available_agent()
        if not agent_id:
            # Put task back
            task.status = TaskStatus.PENDING
            return None

        # Execute task
        self._execute_task(task, agent_id)
        return task.id

    def _find_available_agent(self) -> Optional[str]:
        """Find an available agent."""
        active_agents = set(self._active_tasks.values())
        all_agents = self._agent_manager.get_all_agents()

        for agent_id in all_agents:
            if agent_id not in active_agents:
                return agent_id

        return None

    def _execute_task(self, task: Task, agent_id: str) -> None:
        """Execute a task with an agent."""
        with self._lock:
            self._active_tasks[task.id] = agent_id
            task.assigned_agent_id = agent_id

        task.mark_started(agent_id)
        self._notify_callbacks("started", task)

        def on_complete(result):
            self._on_task_complete(task.id, result)

        def on_error(error):
            self._on_task_error(task.id, error)

        # Submit to agent manager
        try:
            self._agent_manager.create_agent(
                task=task.description, callback=on_complete
            )
        except Exception as e:
            self._on_task_error(task.id, str(e))

    def _on_task_complete(self, task_id: str, result: Any) -> None:
        """Handle task completion."""
        task = self._task_queue.get_by_id(task_id)
        if not task:
            return

        with self._lock:
            if task_id in self._active_tasks:
                del self._active_tasks[task_id]

        self._task_queue.mark_completed(task_id, result)
        self._notify_callbacks("completed", task)

    def _on_task_error(self, task_id: str, error: str) -> None:
        """Handle task error."""
        task = self._task_queue.get_by_id(task_id)
        if not task:
            return

        with self._lock:
            if task_id in self._active_tasks:
                del self._active_tasks[task_id]

        # Check if should retry
        if task.can_retry():
            task.increment_retry()
            task.status = TaskStatus.PENDING
            self._task_queue.add(task)
            self._notify_callbacks("retry", task)
        else:
            self._task_queue.mark_failed(task_id, error)
            self._notify_callbacks("failed", task)

    def wait_for_task(
        self, task_id: str, timeout: Optional[float] = None
    ) -> Optional[Any]:
        """
        Wait for a task to complete.

        Args:
            task_id: ID of the task to wait for.
            timeout: Optional timeout in seconds.

        Returns:
            Task result if completed, None if timeout.
        """
        start = time.time()

        while self._running:
            task = self._task_queue.get_by_id(task_id)
            if not task:
                return None

            if task.status == TaskStatus.COMPLETED:
                return task.result.output if task.result else None

            if task.status in (TaskStatus.FAILED, TaskStatus.CANCELLED):
                return None

            if timeout and (time.time() - start) >= timeout:
                return None

            time.sleep(0.1)

        return None

    def get_active_tasks(self) -> Dict[str, str]:
        """
        Get currently active task executions.

        Returns:
            Dictionary mapping task IDs to agent IDs.
        """
        return dict(self._active_tasks)

    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        stats = self._task_queue.get_stats()
        stats["active"] = len(self._active_tasks)
        stats["max_concurrent"] = self._max_concurrent
        return stats

    def on_event(self, event: str, callback: Callable) -> None:
        """
        Register a callback for executor events.

        Args:
            event: Event type.
            callback: Callback function.
        """
        if event not in self._callbacks:
            self._callbacks[event] = []
        self._callbacks[event].append(callback)

    def _notify_callbacks(self, event: str, task: Task) -> None:
        """Notify registered callbacks."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(task)
            except Exception:
                pass
