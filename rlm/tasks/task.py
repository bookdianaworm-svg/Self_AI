"""
Task definition for the swarm system.

This module defines the Task class and related types
for task submission and tracking.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class TaskStatus(Enum):
    """Status of a task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class TaskPriority(Enum):
    """Priority of a task."""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class TaskResult:
    """Result of a task execution."""

    task_id: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    completed_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """
    A task to be executed by an agent.

    Tasks are the primary unit of work in the swarm system.
    They can be submitted to the task queue and executed by agents.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    assigned_agent_id: Optional[str] = None
    result: Optional[TaskResult] = None
    parent_task_id: Optional[str] = None
    child_task_ids: List[str] = field(default_factory=list)
    dependencies: List[str] = field(
        default_factory=list
    )  # Task IDs that must complete first
    metadata: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat()
            if self.completed_at
            else None,
            "assigned_agent_id": self.assigned_agent_id,
            "result": {
                "success": self.result.success if self.result else None,
                "output": self.result.output if self.result else None,
                "error": self.result.error if self.result else None,
                "execution_time_ms": self.result.execution_time_ms
                if self.result
                else None,
            }
            if self.result
            else None,
            "parent_task_id": self.parent_task_id,
            "child_task_ids": self.child_task_ids,
            "dependencies": self.dependencies,
            "metadata": self.metadata,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "timeout_seconds": self.timeout_seconds,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create task from dictionary."""
        task = cls(
            id=data.get("id", str(uuid.uuid4())),
            description=data.get("description", ""),
            priority=TaskPriority(data.get("priority", 2)),
            status=TaskStatus(data.get("status", "pending")),
            parent_task_id=data.get("parent_task_id"),
            dependencies=data.get("dependencies", []),
            metadata=data.get("metadata", {}),
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            timeout_seconds=data.get("timeout_seconds"),
        )

        if "created_at" in data:
            if isinstance(data["created_at"], str):
                task.created_at = datetime.fromisoformat(data["created_at"])

        return task

    def is_ready(self, completed_tasks: List[str]) -> bool:
        """
        Check if task is ready to be executed.

        Args:
            completed_tasks: List of completed task IDs.

        Returns:
            True if all dependencies are met.
        """
        return all(dep_id in completed_tasks for dep_id in self.dependencies)

    def can_retry(self) -> bool:
        """Check if task can be retried."""
        return self.retry_count < self.max_retries

    def mark_started(self, agent_id: str) -> None:
        """Mark task as started."""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now()
        self.assigned_agent_id = agent_id

    def mark_completed(self, result: Any) -> None:
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = TaskResult(
            task_id=self.id,
            success=True,
            output=result,
        )

    def mark_failed(self, error: str) -> None:
        """Mark task as failed."""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now()
        self.result = TaskResult(
            task_id=self.id,
            success=False,
            error=error,
        )

    def mark_cancelled(self) -> None:
        """Mark task as cancelled."""
        self.status = TaskStatus.CANCELLED
        self.completed_at = datetime.now()

    def add_child(self, child_task_id: str) -> None:
        """Add a child task."""
        self.child_task_ids.append(child_task_id)

    def increment_retry(self) -> None:
        """Increment retry count."""
        self.retry_count += 1
