"""
Sidebar Inbox Manager

Handles polling and processing of sidebar inbox messages.

Poll Interval: 5 seconds (configurable)
Surfaces messages by generating agent prompts from message content.

Usage:
    manager = InboxManager()
    await manager.start_polling(agent_instance)

    # Or manually:
    messages = manager.fetch_pending_messages()
    for msg in messages:
        prompt = manager.surface_as_prompt(msg)
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .inbox_schema import (
    InboxMessage,
    InboxMessageType,
    InboxPriority,
    TaskStatus,
)


# Configuration
DEFAULT_POLL_INTERVAL_SECONDS = 5.0
INBOX_DIR = Path(__file__).parent / "inbox"


class InboxManager:
    """
    Manages sidebar-to-agent inbox communication.

    Responsibilities:
    - Poll .sidebar/inbox/ for new messages
    - Track processed messages (avoid duplicates)
    - Surface messages as agent prompts
    - Handle self-awareness messages specially
    - Mark messages as processed/completed/failed
    """

    def __init__(
        self,
        inbox_dir: Path = INBOX_DIR,
        poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS,
    ):
        self.inbox_dir = inbox_dir
        self.poll_interval = poll_interval
        self._processed_ids: set = set()  # Track already-seen messages
        self._running = False
        self._poll_task: Optional[asyncio.Task] = None
        self._agent_callback: Optional[Callable] = None

        # Ensure inbox directory exists
        self.inbox_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # File I/O
    # -------------------------------------------------------------------------

    def _list_pending_files(self) -> List[Path]:
        """List all .json files in inbox directory."""
        if not self.inbox_dir.exists():
            return []
        return sorted(self.inbox_dir.glob("*.json"))

    def _read_message(self, path: Path) -> Optional[InboxMessage]:
        """Read and parse a message file."""
        try:
            with open(path, "r") as f:
                data = json.load(f)
            return InboxMessage.from_dict(data)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"[inbox] Error reading {path}: {e}")
            return None

    def _write_message(self, message: InboxMessage, path: Path) -> None:
        """Write a message to file."""
        with open(path, "w") as f:
            json.dump(message.to_dict(), f, indent=2)

    def _mark_processed(self, message: InboxMessage, status: TaskStatus) -> None:
        """Update message status to mark it processed."""
        message.status = status
        message_path = self.inbox_dir / f"{message.id}.json"
        self._write_message(message, message_path)

    # -------------------------------------------------------------------------
    # Fetching
    # -------------------------------------------------------------------------

    def fetch_pending_messages(self) -> List[InboxMessage]:
        """
        Fetch all pending messages from inbox.

        Returns messages sorted by priority (high → low).
        Skips already-processed IDs and expired messages.
        """
        messages: List[InboxMessage] = []

        for file_path in self._list_pending_files():
            msg = self._read_message(file_path)
            if msg is None:
                continue

            # Skip already processed
            if msg.id in self._processed_ids:
                continue

            # Skip expired messages
            if msg.is_expired():
                self._mark_processed(msg, TaskStatus.FAILED)
                continue

            # Skip completed/cancelled/failed
            if msg.status in (
                TaskStatus.COMPLETED,
                TaskStatus.CANCELLED,
                TaskStatus.FAILED,
            ):
                self._processed_ids.add(msg.id)
                continue

            messages.append(msg)

        # Sort by priority (critical first)
        messages.sort(key=lambda m: m.priority.value)
        return messages

    def fetch_critical_messages(self) -> List[InboxMessage]:
        """Fetch only critical priority messages (immediate surfacing)."""
        all_pending = self.fetch_pending_messages()
        return [m for m in all_pending if m.priority == InboxPriority.CRITICAL]

    # -------------------------------------------------------------------------
    # Surfacing (message → agent prompt)
    # -------------------------------------------------------------------------

    def surface_as_prompt(self, message: InboxMessage) -> str:
        """
        Convert an inbox message into an agent prompt string.

        This generates the actual text that will be presented to the agent,
        formatted for immediate action/comprehension.
        """
        lines = [
            f"[INBOX MESSAGE] {'[CRITICAL] ' if message.priority == InboxPriority.CRITICAL else ''}{message.type.value.upper()}",
            f"ID: {message.id} | Task: {message.task_id or 'none'}",
            f"From: {message.source_agent}",
            "",
        ]

        # Title and description
        if message.title:
            lines.append(f"# {message.title}")
        if message.description:
            lines.append(message.description)

        # Self-awareness handling
        if message.self_awareness:
            lines.append("")
            lines.append("[SELF-AWARENESS]")
            if message.reflection_prompt:
                lines.append(f"Reflection: {message.reflection_prompt}")
            if message.check_internal_state:
                lines.append(
                    f"State check: {json.dumps(message.check_internal_state, indent=2)}"
                )

        # Payload details
        if message.payload:
            lines.append("")
            lines.append("[PAYLOAD]")
            lines.append(json.dumps(message.payload, indent=2))

        # User input required
        if message.type == InboxMessageType.USER_INPUT_REQUIRED:
            lines.append("")
            lines.append("[AWAITING USER INPUT - PAUSE EXECUTION]")

        # Revision handling
        if message.type == InboxMessageType.TASK_REVISION:
            lines.append("")
            lines.append("[TASK PARAMETERS REVISED - RECALCULATE APPROACH]")

        lines.append("")
        lines.append(f"Created: {message.created_at}")

        return "\n".join(lines)

    def generate_self_awareness_prompt(
        self, message: InboxMessage
    ) -> Dict[str, Any]:
        """
        Generate structured self-awareness reflection prompt.

        Returns a dict with keys for the agent to fill:
        - reflection: What to reflect on
        - state_checks: Internal state to verify
        - confidence: Self-rated confidence level
        """
        return {
            "type": "self_awareness",
            "trigger": message.type.value,
            "task_id": message.task_id,
            "reflection_prompt": message.reflection_prompt
            or "Reflect on your current approach and state.",
            "state_checks": message.check_internal_state or {},
            "suggested_format": {
                "what_went_well": "...",
                "what_could_improve": "...",
                "confidence_level": "high/medium/low",
                "adjustments_planned": "...",
            },
        }

    # -------------------------------------------------------------------------
    # Polling loop
    # -------------------------------------------------------------------------

    async def _poll_loop(self, agent_callback: Callable) -> None:
        """
        Internal polling loop.

        Args:
            agent_callback: Async function to call with surfaced prompts
        """
        while self._running:
            try:
                # Check for critical messages first (immediate)
                critical = self.fetch_critical_messages()
                for msg in critical:
                    prompt = self.surface_as_prompt(msg)
                    await agent_callback(prompt, msg)
                    self._processed_ids.add(msg.id)
                    self._mark_processed(msg, TaskStatus.IN_PROGRESS)

                # Check for normal priority messages
                pending = self.fetch_pending_messages()
                for msg in pending:
                    if msg.priority == InboxPriority.CRITICAL:
                        continue  # Already handled
                    prompt = self.surface_as_prompt(msg)
                    await agent_callback(prompt, msg)
                    self._processed_ids.add(msg.id)

            except Exception as e:
                print(f"[inbox] Poll error: {e}")

            await asyncio.sleep(self.poll_interval)

    def start_polling(self, agent_callback: Callable) -> None:
        """
        Start background polling.

        Args:
            agent_callback: Async function(message_prompt, inbox_message)
        """
        if self._running:
            return

        self._running = True
        self._agent_callback = agent_callback
        self._poll_task = asyncio.create_task(
            self._poll_loop(agent_callback)
        )

    async def stop_polling(self) -> None:
        """Stop the polling loop."""
        self._running = False
        if self._poll_task:
            self._poll_task.cancel()
            try:
                await self._poll_task
            except asyncio.CancelledError:
                pass

    # -------------------------------------------------------------------------
    # Message lifecycle
    # -------------------------------------------------------------------------

    def mark_completed(self, message: InboxMessage) -> None:
        """Mark a message as completed."""
        self._processed_ids.add(message.id)
        self._mark_processed(message, TaskStatus.COMPLETED)

    def mark_failed(self, message: InboxMessage, error: Optional[str] = None) -> None:
        """Mark a message as failed."""
        self._processed_ids.add(message.id)
        if error:
            message.payload["error"] = error
        self._mark_processed(message, TaskStatus.FAILED)

    def retry_message(self, message: InboxMessage) -> bool:
        """Retry a failed message if allowed."""
        if not message.can_retry():
            return False
        message.retry_count += 1
        message.status = TaskStatus.PENDING
        message_path = self.inbox_dir / f"{message.id}.json"
        self._write_message(message, message_path)
        return True

    # -------------------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------------------

    def get_inbox_status(self) -> Dict[str, Any]:
        """Get current inbox status summary."""
        all_files = self._list_pending_files()
        pending = self.fetch_pending_messages()

        by_status: Dict[str, int] = {}
        by_priority: Dict[str, int] = {}

        for file_path in all_files:
            msg = self._read_message(file_path)
            if msg:
                by_status[msg.status.value] = by_status.get(msg.status.value, 0) + 1
                by_priority[msg.priority.value] = by_priority.get(
                    msg.priority.value, 0
                ) + 1

        return {
            "polling": self._running,
            "poll_interval_seconds": self.poll_interval,
            "total_files": len(all_files),
            "pending_count": len(pending),
            "processed_count": len(self._processed_ids),
            "by_status": by_status,
            "by_priority": by_priority,
        }

    def clear_processed(self) -> int:
        """Remove completed/failed message files from inbox."""
        removed = 0
        for file_path in self._list_pending_files():
            msg = self._read_message(file_path)
            if msg and msg.status in (
                TaskStatus.COMPLETED,
                TaskStatus.CANCELLED,
                TaskStatus.FAILED,
            ):
                file_path.unlink()
                removed += 1
        return removed


# =============================================================================
# CLI utility for testing
# =============================================================================

async def demo_poll():
    """Demo: poll inbox and print messages."""
    manager = InboxManager()

    async def handle_message(prompt: str, msg: InboxMessage):
        print("\n" + "=" * 60)
        print(prompt)
        print("=" * 60)

    print(f"[demo] Polling {manager.inbox_dir} every {manager.poll_interval}s")
    print("[demo] Press Ctrl+C to stop")

    manager.start_polling(handle_message)

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n[demo] Stopping...")
        await manager.stop_polling()


if __name__ == "__main__":
    asyncio.run(demo_poll())
