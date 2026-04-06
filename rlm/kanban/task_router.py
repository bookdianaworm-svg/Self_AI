"""Task routing logic for selecting the best runner for a given task."""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from rlm.storage.task_fingerprint import compute as compute_fingerprint
from rlm.storage.task_knowledge_storage import TaskKnowledgeStorage


_TASK_TYPE_KEYWORDS: Dict[str, List[str]] = {
    "bugfix": ["fix", "bug", "error", "crash"],
    "feature": ["add", "create", "implement", "build"],
    "refactor": ["update", "modify", "refactor"],
    "testing": ["test", "spec"],
    "infrastructure": ["deploy", "setup", "config"],
}


@dataclass
class RoutingDecision:
    """Result of task routing containing runner assignment and context."""

    runner_id: str
    task_type: str
    similar_tasks: List[Dict[str, Any]]
    fingerprint: str
    task_description: str


class TaskRouter:
    """Routes tasks to the appropriate runner based on task type and history."""

    def __init__(
        self,
        kb_storage: TaskKnowledgeStorage,
        available_runners: List[Dict[str, str]],
    ) -> None:
        """Initialize the task router.

        Args:
            kb_storage: TaskKnowledgeStorage instance for finding similar tasks.
            available_runners: List of runner spec dicts with keys: runner_id,
                specialization.
        """
        self.kb_storage = kb_storage
        self.available_runners = available_runners

    def classify_task_type(self, description: str) -> str:
        """Classify task type via keyword matching.

        Args:
            description: The task description.

        Returns:
            Task type string: bugfix, feature, refactor, testing,
            infrastructure, or investigation.
        """
        lower = description.lower()
        for task_type, keywords in _TASK_TYPE_KEYWORDS.items():
            if any(kw in lower for kw in keywords):
                return task_type
        return "investigation"

    def _select_runner(self, task_type: str) -> str:
        """Select the first runner whose specialization matches the task type.

        Args:
            task_type: The task type to match against runner specializations.

        Returns:
            The runner_id of the selected runner, or empty string if none match.
        """
        for runner in self.available_runners:
            specialization = runner.get("specialization", "").lower()
            if specialization == task_type:
                return runner.get("runner_id", "")
        # Fallback: return first runner if no specialization matches
        if self.available_runners:
            return self.available_runners[0].get("runner_id", "")
        return ""

    def route_task(
        self,
        description: str,
        priority: str = "NORMAL",
    ) -> RoutingDecision:
        """Route a task to the appropriate runner.

        Args:
            description: The task description.
            priority: Task priority (default 'NORMAL').

        Returns:
            RoutingDecision with runner_id, task_type, similar_tasks,
            fingerprint, and task_description.
        """
        fingerprint = compute_fingerprint(description)
        similar_tasks = self.kb_storage.find_similar(fingerprint)
        task_type = self.classify_task_type(description)
        runner_id = self._select_runner(task_type)

        return RoutingDecision(
            runner_id=runner_id,
            task_type=task_type,
            similar_tasks=similar_tasks,
            fingerprint=fingerprint,
            task_description=description,
        )
