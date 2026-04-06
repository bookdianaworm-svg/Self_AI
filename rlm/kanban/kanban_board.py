from typing import Optional

from .kanban_task import KanbanTask


class KanbanBoard:
    VALID_TRANSITIONS: dict = {
        KanbanTask.BACKLOG: [KanbanTask.READY],
        KanbanTask.READY: [KanbanTask.BACKLOG, KanbanTask.IN_PROGRESS],
        KanbanTask.IN_PROGRESS: [KanbanTask.READY, KanbanTask.DONE, KanbanTask.FAILED],
        KanbanTask.DONE: [KanbanTask.BACKLOG],
        KanbanTask.FAILED: [KanbanTask.BACKLOG, KanbanTask.READY],
    }

    def __init__(self, initial_state: Optional[dict] = None) -> None:
        self._tasks: dict[str, KanbanTask] = {}
        if initial_state:
            for task_data in initial_state.get('tasks', []):
                task = KanbanTask(**task_data)
                self._tasks[task.id] = task

    def get_task(self, task_id: str) -> Optional[KanbanTask]:
        return self._tasks.get(task_id)

    def get_column_tasks(self, column: str) -> list[KanbanTask]:
        return [task for task in self._tasks.values() if task.column == column]

    def add_task(self, task: KanbanTask) -> None:
        self._tasks[task.id] = task

    def move_task(self, task_id: str, to_column: str) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        valid = self.get_valid_transitions(task.column)
        if to_column not in valid:
            return False
        task.column = to_column
        return True

    def get_valid_transitions(self, from_column: str) -> list[str]:
        return list(self.VALID_TRANSITIONS.get(from_column, []))

    def assign_runner(self, task_id: str, runner_id: str) -> None:
        task = self.get_task(task_id)
        if task:
            task.runner_id = runner_id

    def get_runner_tasks(self, runner_id: str) -> list[KanbanTask]:
        return [task for task in self._tasks.values() if task.runner_id == runner_id]

    def to_dict(self) -> dict:
        return {
            'tasks': [
                {
                    'id': t.id,
                    'description': t.description,
                    'task_type': t.task_type,
                    'column': t.column,
                    'runner_id': t.runner_id,
                    'priority': t.priority,
                    'created_at': t.created_at,
                    'started_at': t.started_at,
                    'completed_at': t.completed_at,
                    'knowledge_id': t.knowledge_id,
                    'similar_knowledge': t.similar_knowledge,
                }
                for t in self._tasks.values()
            ]
        }
