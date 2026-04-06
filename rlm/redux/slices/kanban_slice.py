"""
Redux slice for Kanban board state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time


class KanbanActionType(Enum):
    MOVE_TASK = "kanban/move_task"
    SUBMIT_TASK = "kanban/submit_task"
    ASSIGN_TASK = "kanban/assign_task"
    COMPLETE_TASK = "kanban/complete_task"
    FAIL_TASK = "kanban/fail_task"
    LOAD_STATE = "kanban/load_state"


# Column constants matching KanbanTask
BACKLOG = "BACKLOG"
READY = "READY"
IN_PROGRESS = "IN_PROGRESS"
DONE = "DONE"
FAILED = "FAILED"


@dataclass
class KanbanTask:
    """Kanban task representation matching rlm.kanban.KanbanTask."""
    id: str
    description: str
    task_type: str
    column: str
    runner_id: Optional[str] = None
    priority: str = 'NORMAL'
    created_at: float = 0.0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    knowledge_id: Optional[str] = None
    similar_knowledge: List[Any] = field(default_factory=list)


@dataclass
class KanbanState:
    """State shape for Kanban board."""
    columns: Dict[str, List[str]] = field(default_factory=lambda: {
        BACKLOG: [],
        READY: [],
        IN_PROGRESS: [],
        DONE: [],
        FAILED: [],
    })
    tasks: Dict[str, KanbanTask] = field(default_factory=dict)
    column_assignments: Dict[str, str] = field(default_factory=dict)  # task_id -> runner_id
    runner_status: Dict[str, str] = field(default_factory=dict)  # runner_id -> 'idle'|'busy'


class KanbanActions:
    """Action creators for Kanban slice."""

    @staticmethod
    def move_task(task_id: str, to_column: str) -> dict:
        """Move a task to a different column."""
        return {"type": KanbanActionType.MOVE_TASK.value, "payload": {"task_id": task_id, "to_column": to_column}}

    @staticmethod
    def submit_task(task: KanbanTask) -> dict:
        """Submit a new task to the backlog."""
        return {"type": KanbanActionType.SUBMIT_TASK.value, "payload": task}

    @staticmethod
    def assign_task(task_id: str, runner_id: str) -> dict:
        """Assign a task to a runner."""
        return {"type": KanbanActionType.ASSIGN_TASK.value, "payload": {"task_id": task_id, "runner_id": runner_id}}

    @staticmethod
    def complete_task(task_id: str) -> dict:
        """Mark a task as completed."""
        return {"type": KanbanActionType.COMPLETE_TASK.value, "payload": {"task_id": task_id}}

    @staticmethod
    def fail_task(task_id: str) -> dict:
        """Mark a task as failed."""
        return {"type": KanbanActionType.FAIL_TASK.value, "payload": {"task_id": task_id}}

    @staticmethod
    def load_state(state: KanbanState) -> dict:
        """Load a full Kanban state."""
        return {"type": KanbanActionType.LOAD_STATE.value, "payload": state}


def kanban_reducer(state: KanbanState, action: dict) -> KanbanState:
    """Reducer for Kanban board actions."""
    action_type = action.get("type", "")
    payload = action.get("payload", {})

    if action_type == KanbanActionType.MOVE_TASK.value:
        task_id = payload.get("task_id")
        to_column = payload.get("to_column")

        if task_id not in state.tasks:
            return state

        task = state.tasks[task_id]
        from_column = task.column

        if from_column == to_column:
            return state

        # Update column lists
        new_columns = {k: list(v) for k, v in state.columns.items()}
        if task_id in new_columns.get(from_column, []):
            new_columns[from_column].remove(task_id)
        if task_id not in new_columns.get(to_column, []):
            new_columns.setdefault(to_column, []).append(task_id)

        # Update task's column
        new_tasks = dict(state.tasks)
        new_tasks[task_id] = KanbanTask(
            id=task.id,
            description=task.description,
            task_type=task.task_type,
            column=to_column,
            runner_id=task.runner_id,
            priority=task.priority,
            created_at=task.created_at,
            started_at=task.started_at,
            completed_at=task.completed_at,
            knowledge_id=task.knowledge_id,
            similar_knowledge=task.similar_knowledge,
        )

        return KanbanState(
            columns=new_columns,
            tasks=new_tasks,
            column_assignments=dict(state.column_assignments),
            runner_status=dict(state.runner_status),
        )

    elif action_type == KanbanActionType.SUBMIT_TASK.value:
        task_data = payload
        if isinstance(task_data, dict):
            task = KanbanTask(**task_data)
        elif isinstance(task_data, KanbanTask):
            task = task_data
        else:
            return state

        # Force column to BACKLOG
        task.column = BACKLOG

        new_tasks = dict(state.tasks)
        new_tasks[task.id] = task

        new_columns = {k: list(v) for k, v in state.columns.items()}
        if task.id not in new_columns[BACKLOG]:
            new_columns[BACKLOG].append(task.id)

        return KanbanState(
            columns=new_columns,
            tasks=new_tasks,
            column_assignments=dict(state.column_assignments),
            runner_status=dict(state.runner_status),
        )

    elif action_type == KanbanActionType.ASSIGN_TASK.value:
        task_id = payload.get("task_id")
        runner_id = payload.get("runner_id")

        if task_id not in state.tasks:
            return state

        task = state.tasks[task_id]

        new_column_assignments = dict(state.column_assignments)
        new_column_assignments[task_id] = runner_id

        new_runner_status = dict(state.runner_status)
        new_runner_status[runner_id] = 'busy'

        # Update task's runner_id
        new_tasks = dict(state.tasks)
        new_tasks[task_id] = KanbanTask(
            id=task.id,
            description=task.description,
            task_type=task.task_type,
            column=task.column,
            runner_id=runner_id,
            priority=task.priority,
            created_at=task.created_at,
            started_at=task.started_at,
            completed_at=task.completed_at,
            knowledge_id=task.knowledge_id,
            similar_knowledge=task.similar_knowledge,
        )

        return KanbanState(
            columns={k: list(v) for k, v in state.columns.items()},
            tasks=new_tasks,
            column_assignments=new_column_assignments,
            runner_status=new_runner_status,
        )

    elif action_type == KanbanActionType.COMPLETE_TASK.value:
        task_id = payload.get("task_id")

        if task_id not in state.tasks:
            return state

        task = state.tasks[task_id]
        runner_id = state.column_assignments.get(task_id)

        new_columns = {k: list(v) for k, v in state.columns.items()}
        if task_id in new_columns.get(task.column, []):
            new_columns[task.column].remove(task_id)
        if task_id not in new_columns[DONE]:
            new_columns[DONE].append(task_id)

        new_tasks = dict(state.tasks)
        new_tasks[task_id] = KanbanTask(
            id=task.id,
            description=task.description,
            task_type=task.task_type,
            column=DONE,
            runner_id=None,
            priority=task.priority,
            created_at=task.created_at,
            started_at=task.started_at,
            completed_at=time.time(),
            knowledge_id=task.knowledge_id,
            similar_knowledge=task.similar_knowledge,
        )

        new_column_assignments = dict(state.column_assignments)
        if task_id in new_column_assignments:
            del new_column_assignments[task_id]

        new_runner_status = dict(state.runner_status)
        if runner_id and runner_id in new_runner_status:
            # Check if runner has other assigned tasks
            still_busy = any(
                new_column_assignments.get(tid) == runner_id
                for tid in new_tasks
                if tid != task_id
            )
            new_runner_status[runner_id] = 'busy' if still_busy else 'idle'

        return KanbanState(
            columns=new_columns,
            tasks=new_tasks,
            column_assignments=new_column_assignments,
            runner_status=new_runner_status,
        )

    elif action_type == KanbanActionType.FAIL_TASK.value:
        task_id = payload.get("task_id")

        if task_id not in state.tasks:
            return state

        task = state.tasks[task_id]
        runner_id = state.column_assignments.get(task_id)

        new_columns = {k: list(v) for k, v in state.columns.items()}
        if task_id in new_columns.get(task.column, []):
            new_columns[task.column].remove(task_id)
        if task_id not in new_columns[FAILED]:
            new_columns[FAILED].append(task_id)

        new_tasks = dict(state.tasks)
        new_tasks[task_id] = KanbanTask(
            id=task.id,
            description=task.description,
            task_type=task.task_type,
            column=FAILED,
            runner_id=None,
            priority=task.priority,
            created_at=task.created_at,
            started_at=task.started_at,
            completed_at=time.time(),
            knowledge_id=task.knowledge_id,
            similar_knowledge=task.similar_knowledge,
        )

        new_column_assignments = dict(state.column_assignments)
        if task_id in new_column_assignments:
            del new_column_assignments[task_id]

        new_runner_status = dict(state.runner_status)
        if runner_id and runner_id in new_runner_status:
            still_busy = any(
                new_column_assignments.get(tid) == runner_id
                for tid in new_tasks
                if tid != task_id
            )
            new_runner_status[runner_id] = 'busy' if still_busy else 'idle'

        return KanbanState(
            columns=new_columns,
            tasks=new_tasks,
            column_assignments=new_column_assignments,
            runner_status=new_runner_status,
        )

    elif action_type == KanbanActionType.LOAD_STATE.value:
        new_state = payload
        if isinstance(new_state, KanbanState):
            return new_state
        elif isinstance(new_state, dict):
            # Reconstruct columns from tasks
            columns: Dict[str, List[str]] = {
                BACKLOG: [],
                READY: [],
                IN_PROGRESS: [],
                DONE: [],
                FAILED: [],
            }
            tasks: Dict[str, KanbanTask] = {}
            column_assignments: Dict[str, str] = {}
            runner_status: Dict[str, str] = {}

            tasks_data = new_state.get('tasks', {})
            if isinstance(tasks_data, list):
                for task_dict in tasks_data:
                    task = KanbanTask(**task_dict) if isinstance(task_dict, dict) else task_dict
                    tasks[task.id] = task
                    columns.setdefault(task.column, []).append(task.id)
                    if task.runner_id:
                        column_assignments[task.id] = task.runner_id
            elif isinstance(tasks_data, dict):
                for task_id, task_dict in tasks_data.items():
                    task = KanbanTask(**task_dict) if isinstance(task_dict, dict) else task_dict
                    tasks[task_id] = task
                    columns.setdefault(task.column, []).append(task_id)
                    if task.runner_id:
                        column_assignments[task_id] = task.runner_id

            runner_status = new_state.get('runner_status', {})

            return KanbanState(
                columns=columns,
                tasks=tasks,
                column_assignments=column_assignments,
                runner_status=runner_status,
            )

    return state
