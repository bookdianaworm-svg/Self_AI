"""
Sidebar Response Manager

Polls `sidebar/responses/` for agent responses.
Sidebar agent uses this to receive task results and reflections.

Poll Interval: 5 seconds (configurable)
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .response_schema import ResponseMessage, ResponseType, Outcome


DEFAULT_POLL_INTERVAL_SECONDS = 5.0
RESPONSES_DIR = Path(__file__).parent / "responses"


class ResponseManager:
    """
    Manages agent-to-sidebar response communication.

    Polls for responses and routes them to handlers.
    """

    def __init__(
        self,
        responses_dir: Path = RESPONSES_DIR,
        poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS,
    ):
        self.responses_dir = responses_dir
        self.poll_interval = poll_interval
        self._read_ids: set = set()  # Track already-seen responses
        self._running = False
        self._poll_task: Optional[asyncio.Task] = None
        self._handlers: Dict[ResponseType, Callable] = {}

        self.responses_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # File I/O
    # -------------------------------------------------------------------------

    def _list_response_files(self) -> List[Path]:
        """List all .json files in responses directory."""
        if not self.responses_dir.exists():
            return []
        return sorted(self.responses_dir.glob("*.json"))

    def _read_response(self, path: Path) -> Optional[ResponseMessage]:
        """Read and parse a response file."""
        try:
            with open(path, "r") as f:
                data = json.load(f)
            return ResponseMessage.from_dict(data)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"[response] Error reading {path}: {e}")
            return None

    def _write_response(self, response: ResponseMessage, path: Path) -> None:
        """Write a response to file."""
        with open(path, "w") as f:
            json.dump(response.to_dict(), f, indent=2)

    # -------------------------------------------------------------------------
    # Fetching
    # -------------------------------------------------------------------------

    def fetch_new_responses(self) -> List[ResponseMessage]:
        """Fetch all new responses not yet processed."""
        responses: List[ResponseMessage] = []

        for file_path in self._list_response_files():
            resp = self._read_response(file_path)
            if resp is None:
                continue
            if resp.id in self._read_ids:
                continue
            responses.append(resp)

        responses.sort(key=lambda r: r.created_at)
        return responses

    def fetch_by_task(self, task_id: str) -> List[ResponseMessage]:
        """Fetch all responses for a specific task."""
        all_responses = []
        for file_path in self._list_response_files():
            resp = self._read_response(file_path)
            if resp and resp.task_id == task_id:
                all_responses.append(resp)
        return sorted(all_responses, key=lambda r: r.created_at)

    def fetch_by_type(self, response_type: ResponseType) -> List[ResponseMessage]:
        """Fetch all responses of a specific type."""
        responses = []
        for file_path in self._list_response_files():
            resp = self._read_response(file_path)
            if resp and resp.type == response_type:
                responses.append(resp)
        return sorted(responses, key=lambda r: r.created_at)

    # -------------------------------------------------------------------------
    # Surfacing
    # -------------------------------------------------------------------------

    def surface_as_prompt(self, response: ResponseMessage) -> str:
        """Convert a response into a prompt/notification for sidebar."""
        lines = [
            f"[RESPONSE] {response.type.value.upper()}",
            f"ID: {response.id} | Task: {response.task_id}",
            f"From: {response.agent_id}",
            f"Outcome: {response.outcome.value}",
            "",
        ]

        if response.title:
            lines.append(f"# {response.title}")
        if response.description:
            lines.append(response.description)
        if response.output:
            lines.append("")
            lines.append("[OUTPUT]")
            lines.append(response.output)

        if response.type == ResponseType.REFLECTION_RESULT and response.reflection_result:
            lines.append("")
            lines.append("[REFLECTION RESULT]")
            rr = response.reflection_result
            lines.append(f"Confidence: {rr.get('confidence', 'unknown')}")
            lines.append(f"What went well: {rr.get('what_went_well', 'N/A')}")
            lines.append(f"Could improve: {rr.get('what_could_improve', 'N/A')}")
            lines.append(f"Adjustments: {rr.get('adjustments_planned', 'N/A')}")

        if response.state_verified:
            lines.append("")
            lines.append("[STATE VERIFICATION]")
            for key, passed in response.state_verified.items():
                status = "✓" if passed else "✗"
                lines.append(f"  {status} {key}")

        if response.error:
            lines.append("")
            lines.append(f"[ERROR] {response.error}")

        lines.append("")
        lines.append(f"Created: {response.created_at}")

        return "\n".join(lines)

    # -------------------------------------------------------------------------
    # Polling loop
    # -------------------------------------------------------------------------

    async def _poll_loop(self) -> None:
        """Internal polling loop."""
        while self._running:
            try:
                responses = self.fetch_new_responses()
                for resp in responses:
                    self._read_ids.add(resp.id)

                    # Route to type-specific handler if registered
                    handler = self._handlers.get(resp.type)
                    if handler:
                        await handler(resp)
            except Exception as e:
                print(f"[response] Poll error: {e}")

            await asyncio.sleep(self.poll_interval)

    def start_polling(self) -> None:
        """Start background polling."""
        if self._running:
            return
        self._running = True
        self._poll_task = asyncio.create_task(self._poll_loop())

    async def stop_polling(self) -> None:
        """Stop the polling loop."""
        self._running = False
        if self._poll_task:
            self._poll_task.cancel()
            try:
                await self._poll_task
            except asyncio.CancelledError:
                pass

    def on_response(self, response_type: ResponseType, handler: Callable) -> None:
        """Register a handler for a specific response type."""
        self._handlers[response_type] = handler

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    def mark_read(self, response: ResponseMessage) -> None:
        """Mark a response as read."""
        self._read_ids.add(response.id)

    def clear_read(self, response_id: Optional[str] = None) -> None:
        """Clear read tracking. If ID provided, clear just that one."""
        if response_id:
            self._read_ids.discard(response_id)
        else:
            self._read_ids.clear()

    def cleanup_processed(self) -> int:
        """Remove responses that have been read."""
        removed = 0
        for file_path in self._list_response_files():
            resp = self._read_response(file_path)
            if resp and resp.id in self._read_ids:
                file_path.unlink()
                removed += 1
        return removed

    # -------------------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        """Get current status summary."""
        files = self._list_response_files()
        new = self.fetch_new_responses()

        by_type: Dict[str, int] = {}
        for file_path in files:
            resp = self._read_response(file_path)
            if resp:
                by_type[resp.type.value] = by_type.get(resp.type.value, 0) + 1

        return {
            "polling": self._running,
            "poll_interval_seconds": self.poll_interval,
            "total_files": len(files),
            "unread_count": len(new),
            "read_count": len(self._read_ids),
            "by_type": by_type,
        }
