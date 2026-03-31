"""
Redux slice for tasks state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    LOW = 1
    NORMAL = 5
    HIGH = 8
    CRITICAL = 10


@dataclass
class TaskConstraints:
    max_tokens: Optional[int] = None
    timeout_seconds: Optional[int] = None
    docker_isolation: bool = False


@dataclass
class TaskRouting:
    backend: Optional[str] = None
    environment: Optional[str] = None
    mode: Optional[str] = None


@dataclass
class TaskClassification:
    intent: str
    confidence: float
    complexity_score: float = 0.0


@dataclass
class TaskEntity:
    task_id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.NORMAL
    routing: TaskRouting = field(default_factory=TaskRouting)
    constraints: TaskConstraints = field(default_factory=TaskConstraints)
    classification: Optional[TaskClassification] = None
    parent_task_id: Optional[str] = None
    created_at: float = 0.0
    updated_at: float = 0.0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class TaskSubmissionDraft:
    description: str = ""
    priority: TaskPriority = TaskPriority.NORMAL
    routing: TaskRouting = field(default_factory=TaskRouting)
    constraints: TaskConstraints = field(default_factory=TaskConstraints)
    classification: Optional[TaskClassification] = None


@dataclass
class TasksState:
    tasks: Dict[str, TaskEntity] = field(default_factory=dict)
    current_draft: Optional[TaskSubmissionDraft] = None
    active_task_id: Optional[str] = None
    task_queue: List[str] = field(default_factory=list)


class TasksActions:
    @staticmethod
    def submit_task(task: TaskEntity) -> dict:
        return {"type": "tasks/submit_task", "payload": task}

    @staticmethod
    def update_task_status(task_id: str, status: TaskStatus) -> dict:
        return {"type": "tasks/update_status", "payload": {"task_id": task_id, "status": status.value}}

    @staticmethod
    def set_draft(draft: TaskSubmissionDraft) -> dict:
        return {"type": "tasks/set_draft", "payload": draft}

    @staticmethod
    def clear_draft() -> dict:
        return {"type": "tasks/clear_draft"}

    @staticmethod
    def set_routing_preference(routing: TaskRouting) -> dict:
        return {"type": "tasks/set_routing_preference", "payload": routing}

    @staticmethod
    def set_constraints(constraints: TaskConstraints) -> dict:
        return {"type": "tasks/set_constraints", "payload": constraints}

    @staticmethod
    def cancel_task(task_id: str) -> dict:
        return {"type": "tasks/cancel_task", "payload": {"task_id": task_id}}


def tasks_reducer(state: TasksState, action: dict) -> TasksState:
    action_type = action.get("type")

    if action_type == "tasks/submit_task":
        payload: Any = action.get("payload")
        if payload is None:
            return state
        new_tasks = state.tasks.copy()
        new_tasks[payload.task_id] = payload
        new_queue = state.task_queue.copy()
        if payload.task_id not in new_queue:
            new_queue.append(payload.task_id)
        return TasksState(
            tasks=new_tasks,
            current_draft=None,
            active_task_id=payload.task_id,
            task_queue=new_queue
        )

    elif action_type == "tasks/update_status":
        payload = action.get("payload", {})
        task_id = payload.get("task_id")
        status_str = payload.get("status")
        new_tasks = state.tasks.copy()
        if task_id in new_tasks:
            new_tasks[task_id].status = TaskStatus(status_str)
            new_tasks[task_id].updated_at = payload.get("timestamp", 0.0)
        return TasksState(
            tasks=new_tasks,
            current_draft=state.current_draft,
            active_task_id=state.active_task_id,
            task_queue=state.task_queue
        )

    elif action_type == "tasks/set_draft":
        return TasksState(
            tasks=state.tasks,
            current_draft=action.get("payload"),
            active_task_id=state.active_task_id,
            task_queue=state.task_queue
        )

    elif action_type == "tasks/clear_draft":
        return TasksState(
            tasks=state.tasks,
            current_draft=None,
            active_task_id=state.active_task_id,
            task_queue=state.task_queue
        )

    elif action_type == "tasks/set_routing_preference":
        payload = action.get("payload", {})
        draft = state.current_draft or TaskSubmissionDraft()
        draft.routing = TaskRouting(
            backend=payload.get("backend"),
            environment=payload.get("environment"),
            mode=payload.get("mode")
        )
        return TasksState(
            tasks=state.tasks,
            current_draft=draft,
            active_task_id=state.active_task_id,
            task_queue=state.task_queue
        )

    elif action_type == "tasks/set_constraints":
        payload = action.get("payload", {})
        draft = state.current_draft or TaskSubmissionDraft()
        draft.constraints = TaskConstraints(
            max_tokens=payload.get("max_tokens"),
            timeout_seconds=payload.get("timeout_seconds"),
            docker_isolation=payload.get("docker_isolation", False)
        )
        return TasksState(
            tasks=state.tasks,
            current_draft=draft,
            active_task_id=state.active_task_id,
            task_queue=state.task_queue
        )

    elif action_type == "tasks/cancel_task":
        payload = action.get("payload", {})
        task_id = payload.get("task_id")
        new_tasks = state.tasks.copy()
        if task_id in new_tasks:
            new_tasks[task_id].status = TaskStatus.CANCELLED
        new_queue = state.task_queue.copy()
        if task_id in new_queue:
            new_queue.remove(task_id)
        return TasksState(
            tasks=new_tasks,
            current_draft=state.current_draft,
            active_task_id=state.active_task_id,
            task_queue=new_queue
        )

    return state
