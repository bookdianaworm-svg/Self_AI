"""Task runner agent that executes tasks with specialized knowledge."""

from typing import Any, List, Optional

from rlm.agents.base.base_agent import AgentConfig, BaseAgent
from rlm.kanban.kanban_board import KanbanBoard
from rlm.kanban.kanban_task import KanbanTask
from rlm.storage.knowledge_extractor import KnowledgeExtractor
from rlm.storage.task_fingerprint import compute as compute_fingerprint
from rlm.storage.task_knowledge_storage import TaskKnowledgeStorage
from rlm.utils.key_encryption import EncryptedKeyStore


SPECIALIZATIONS: dict[str, list[str]] = {
    "bugfix": ["fix", "bug", "error", "crash"],
    "feature": ["add", "create", "implement", "build"],
    "refactor": ["update", "modify", "refactor"],
    "testing": ["test", "spec"],
    "infrastructure": ["deploy", "setup", "config"],
}


class TaskRunner(BaseAgent):
    """A specialized agent that executes tasks within a kanban workflow."""

    def __init__(
        self,
        specialization: str,
        specialization_prompt: str,
        runner_id: str,
        kb_storage: TaskKnowledgeStorage,
        encrypted_store: Optional[EncryptedKeyStore] = None,
    ) -> None:
        """Initialize the task runner.

        Args:
            specialization: The task specialization (e.g., bugfix, feature).
            specialization_prompt: Custom system prompt for this runner.
            runner_id: Unique identifier for this runner instance.
            kb_storage: TaskKnowledgeStorage instance for similarity lookups.
            encrypted_store: Optional EncryptedKeyStore for API key access.
        """
        self.specialization = specialization
        self.runner_id = runner_id
        self.kb_storage = kb_storage
        self._task_description: str = ""
        self._kanban_board: Optional[KanbanBoard] = None

        # Build custom system prompt with specialization context
        config = AgentConfig(
            custom_system_prompt=specialization_prompt,
            can_spawn=False,
            encrypted_store=encrypted_store,
        )

        super().__init__(id=runner_id, config=config)

    @property
    def kanban_board(self) -> Optional[KanbanBoard]:
        """Get the kanban board instance."""
        return self._kanban_board

    @kanban_board.setter
    def kanban_board(self, board: KanbanBoard) -> None:
        """Set the kanban board instance for task state transitions."""
        self._kanban_board = board

    def compute_fingerprint(self, description: str) -> str:
        """Compute task fingerprint using TaskFingerprint.

        Args:
            description: The task description.

        Returns:
            A 64-character hexadecimal fingerprint string.
        """
        return compute_fingerprint(description)

    def find_similar_tasks(self, description: str) -> List[dict[str, Any]]:
        """Find similar past tasks using kb_storage.

        Args:
            description: The task description.

        Returns:
            List of similar task knowledge entries.
        """
        fingerprint = self.compute_fingerprint(description)
        return self.kb_storage.find_similar(fingerprint)

    async def execute_task(self, task_description: str) -> Any:
        """Execute the assigned task.

        Args:
            task_description: Description of the task to execute.

        Returns:
            Result of the task execution.
        """
        self._task_description = task_description
        return await super().execute_task(task_description)

    def run_sync(self, task_description: str) -> Any:
        """Synchronous execution that stores task description.

        Args:
            task_description: Description of the task to execute.

        Returns:
            Result of the task execution.
        """
        self._task_description = task_description
        return super().run_sync(task_description)

    def on_task_complete(self, task_id: str, success: bool) -> None:
        """Handle task completion by saving knowledge and updating kanban state.

        Args:
            task_id: The identifier of the completed task.
            success: Whether the task completed successfully.
        """
        # Extract and save knowledge from the agent run
        extractor = KnowledgeExtractor(self.kb_storage)
        final_answer = str(self.result) if self.result is not None else ""

        extractor.save(
            agent_id=self.id,
            task_id=task_id,
            runner_id=self.runner_id,
            final_answer=final_answer,
            task_description=self._task_description,
        )

        # Move task to appropriate kanban column
        if self._kanban_board is not None:
            target_column = KanbanTask.DONE if success else KanbanTask.FAILED
            self._kanban_board.move_task(task_id, target_column)
