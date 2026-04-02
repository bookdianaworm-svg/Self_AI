"""
Sidebar Inbox Writer

Utility for sidebar agents to write messages to the inbox.
This is the writer-side of the sidebar → task agent communication.

Usage (from sidebar agent):
    from sidebar.writer import InboxWriter

    writer = InboxWriter()
    writer.send_task_request(
        task_id="task-123",
        title="Fix login bug",
        description="Users cannot login on mobile",
    )
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from .inbox_schema import (
    InboxMessage,
    InboxMessageType,
    InboxPriority,
    TaskStatus,
    make_task_request,
    make_self_awareness_prompt,
    make_user_input_required,
    make_status_update,
)


INBOX_DIR = Path(__file__).parent / "inbox"


class InboxWriter:
    """
    Writer-side API for sidebar agents to send messages to task agents.

    Sidebar agents use this to:
    - Queue tasks for task agents
    - Trigger self-awareness reflections
    - Signal user input requirements
    - Update task statuses
    """

    def __init__(self, inbox_dir: Path = INBOX_DIR):
        self.inbox_dir = inbox_dir
        self.inbox_dir.mkdir(parents=True, exist_ok=True)

    def _write(self, message: InboxMessage) -> str:
        """
        Write message to inbox file.

        Returns the message ID.
        """
        file_path = self.inbox_dir / f"{message.id}.json"
        with open(file_path, "w") as f:
            json.dump(message.to_dict(), f, indent=2)
        return message.id

    # -------------------------------------------------------------------------
    # Task operations
    # -------------------------------------------------------------------------

    def send_task(
        self,
        task_id: str,
        title: str,
        description: str,
        payload: Optional[Dict[str, Any]] = None,
        priority: InboxPriority = InboxPriority.NORMAL,
        self_awareness: bool = False,
        expires_in_seconds: Optional[float] = None,
    ) -> str:
        """Send a task request to the inbox."""
        msg = make_task_request(
            task_id=task_id,
            title=title,
            description=description,
            payload=payload,
            priority=priority,
            self_awareness=self_awareness,
        )

        if expires_in_seconds:
            expires_at = datetime.now() + timedelta(seconds=expires_in_seconds)
            msg.expires_at = expires_at.isoformat()

        return self._write(msg)

    def send_task_with_reflection(
        self,
        task_id: str,
        title: str,
        description: str,
        reflection_prompt: str,
        check_state: Optional[Dict[str, Any]] = None,
        priority: InboxPriority = InboxPriority.NORMAL,
    ) -> str:
        """Send a task that includes self-awareness reflection."""
        msg = make_self_awareness_prompt(
            task_id=task_id,
            reflection_prompt=reflection_prompt,
            check_state=check_state,
            priority=priority,
        )
        msg.description = description
        msg.title = title
        return self._write(msg)

    def request_user_input(
        self,
        task_id: str,
        prompt: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Request user input (blocks task agent)."""
        msg = make_user_input_required(
            task_id=task_id,
            prompt=prompt,
            payload=payload,
        )
        return self._write(msg)

    def update_status(
        self,
        task_id: str,
        status: str,
        details: Optional[str] = None,
    ) -> str:
        """Send a status update notification."""
        msg = make_status_update(
            task_id=task_id,
            status=status,
            details=details,
        )
        return self._write(msg)

    def cancel_task(self, task_id: str, reason: str = "") -> str:
        """Cancel a pending task."""
        msg = InboxMessage(
            task_id=task_id,
            type=InboxMessageType.TASK_CANCEL,
            title="Task Cancelled",
            description=reason or "Task has been cancelled.",
            priority=InboxPriority.HIGH,
        )
        return self._write(msg)

    def revise_task(
        self,
        task_id: str,
        revisions: Dict[str, Any],
        reason: str = "",
    ) -> str:
        """Send revised task parameters."""
        msg = InboxMessage(
            task_id=task_id,
            type=InboxMessageType.TASK_REVISION,
            title="Task Revised",
            description=reason or "Task parameters have been revised.",
            payload=revisions,
            priority=InboxPriority.HIGH,
        )
        return self._write(msg)

    # -------------------------------------------------------------------------
    # Context sharing
    # -------------------------------------------------------------------------

    def share_context(
        self,
        context_data: Dict[str, Any],
        task_id: Optional[str] = None,
        title: str = "Context Share",
    ) -> str:
        """Share context data with task agent."""
        msg = InboxMessage(
            task_id=task_id or "",
            type=InboxMessageType.CONTEXT_SHARE,
            title=title,
            description="Context data shared from sidebar.",
            payload=context_data,
            priority=InboxPriority.NORMAL,
        )
        return self._write(msg)

    def notify_file_change(
        self,
        file_path: str,
        change_type: str,  # "created", "modified", "deleted"
        task_id: Optional[str] = None,
    ) -> str:
        """Notify task agent of external file change."""
        msg = InboxMessage(
            task_id=task_id or "",
            type=InboxMessageType.FILE_CHANGE,
            title=f"File {change_type}: {file_path}",
            description=f"File {change_type} externally.",
            payload={
                "file_path": file_path,
                "change_type": change_type,
            },
            priority=InboxPriority.NORMAL,
        )
        return self._write(msg)

    # -------------------------------------------------------------------------
    # Self-awareness triggers
    # -------------------------------------------------------------------------

    def trigger_self_reflection(
        self,
        task_id: str,
        reflection_prompt: str,
        check_state: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Trigger self-awareness reflection without a new task."""
        msg = make_self_awareness_prompt(
            task_id=task_id,
            reflection_prompt=reflection_prompt,
            check_state=check_state,
            priority=InboxPriority.NORMAL,
        )
        return self._write(msg)

    def metacognitive_check(
        self,
        task_id: str,
        state_keys: List[str],
        prompt: str = "Verify internal state consistency.",
    ) -> str:
        """Request metacognitive state check."""
        msg = InboxMessage(
            task_id=task_id,
            type=InboxMessageType.METACOGNITIVE_CHECK,
            title="Metacognitive Check",
            description=prompt,
            check_internal_state={k: None for k in state_keys},  # None = just verify exists
            priority=InboxPriority.HIGH,
            self_awareness=True,
        )
        return self._write(msg)

    # -------------------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------------------

    def get_sent_messages(self) -> List[str]:
        """Get IDs of messages this writer has sent (by file count)."""
        if not self.inbox_dir.exists():
            return []
        return [f.stem for f in self.inbox_dir.glob("*.json")]


# =============================================================================
# CLI for testing
# =============================================================================

if __name__ == "__main__":
    writer = InboxWriter()

    # Demo: send a task
    msg_id = writer.send_task(
        task_id="demo-task-1",
        title="Process user request",
        description="Handle the incoming user query with care.",
        priority=InboxPriority.NORMAL,
    )
    print(f"[writer] Sent message: {msg_id}")

    # Demo: send with self-awareness
    msg_id = writer.send_task_with_reflection(
        task_id="demo-task-2",
        title="Analyze architecture",
        description="Review the current architecture and suggest improvements.",
        reflection_prompt="What assumptions am I making about the architecture?",
        check_state={"current_phase": "analysis"},
    )
    print(f"[writer] Sent self-awareness message: {msg_id}")

    # Demo: request user input
    msg_id = writer.request_user_input(
        task_id="demo-task-3",
        prompt="Please confirm the deployment target: production or staging?",
        payload={"options": ["production", "staging"]},
    )
    print(f"[writer] Sent user input request: {msg_id}")
