"""
Agent Response Writer

Task agents use this to send responses back to the sidebar.
Responses are written to `sidebar/responses/<response_id>.json`.

Usage (from task agent):
    from sidebar.response_writer import ResponseWriter

    writer = ResponseWriter()
    writer.complete(
        task_id="task-123",
        inbox_message_id="msg-456",
        output="Task completed successfully"
    )
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .response_schema import (
    ResponseMessage,
    ResponseType,
    Outcome,
    make_completed,
    make_failed,
    make_reflection,
    make_approval,
    make_user_input_response,
)


RESPONSES_DIR = Path(__file__).parent / "responses"


class ResponseWriter:
    """
    Writer-side API for task agents to send responses to sidebar.

    Task agents use this to:
    - Report task completion/failure
    - Send self-reflection results
    - Respond to approval requests
    - Provide user input results
    """

    def __init__(self, responses_dir: Path = RESPONSES_DIR):
        self.responses_dir = responses_dir
        self.responses_dir.mkdir(parents=True, exist_ok=True)

    def _write(self, response: ResponseMessage) -> str:
        """Write response to file. Returns the response ID."""
        file_path = self.responses_dir / f"{response.id}.json"
        with open(file_path, "w") as f:
            json.dump(response.to_dict(), f, indent=2)
        return response.id

    # -------------------------------------------------------------------------
    # Task responses
    # -------------------------------------------------------------------------

    def complete(
        self,
        task_id: str,
        inbox_message_id: str,
        output: str,
        result: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Report task completion."""
        resp = make_completed(
            task_id=task_id,
            inbox_message_id=inbox_message_id,
            output=output,
            result=result,
        )
        return self._write(resp)

    def fail(
        self,
        task_id: str,
        inbox_message_id: str,
        error: str,
        output: str = "",
    ) -> str:
        """Report task failure."""
        resp = make_failed(
            task_id=task_id,
            inbox_message_id=inbox_message_id,
            error=error,
            output=output,
        )
        return self._write(resp)

    # -------------------------------------------------------------------------
    # Self-awareness responses
    # -------------------------------------------------------------------------

    def reflect(
        self,
        task_id: str,
        inbox_message_id: str,
        what_went_well: str,
        what_could_improve: str,
        confidence: str,
        adjustments_planned: str,
        state_verified: Optional[Dict[str, bool]] = None,
    ) -> str:
        """Send self-reflection result."""
        resp = make_reflection(
            task_id=task_id,
            inbox_message_id=inbox_message_id,
            what_went_well=what_went_well,
            what_could_improve=what_could_improve,
            confidence=confidence,
            adjustments_planned=adjustments_planned,
            state_verified=state_verified,
        )
        return self._write(resp)

    def verify_state(
        self,
        task_id: str,
        inbox_message_id: str,
        state_verified: Dict[str, bool],
    ) -> str:
        """Report state verification results."""
        resp = ResponseMessage(
            task_id=task_id,
            inbox_message_id=inbox_message_id,
            type=ResponseType.STATE_VERIFICATION,
            outcome=Outcome.SUCCESS,
            title="State verification complete",
            state_verified=state_verified,
        )
        return self._write(resp)

    # -------------------------------------------------------------------------
    # Approval responses
    # -------------------------------------------------------------------------

    def approve(
        self,
        task_id: str,
        inbox_message_id: str,
        reason: str = "",
    ) -> str:
        """Grant approval."""
        resp = make_approval(
            task_id=task_id,
            inbox_message_id=inbox_message_id,
            granted=True,
            reason=reason,
        )
        return self._write(resp)

    def deny(
        self,
        task_id: str,
        inbox_message_id: str,
        reason: str = "",
    ) -> str:
        """Deny approval."""
        resp = make_approval(
            task_id=task_id,
            inbox_message_id=inbox_message_id,
            granted=False,
            reason=reason,
        )
        return self._write(resp)

    # -------------------------------------------------------------------------
    # User input responses
    # -------------------------------------------------------------------------

    def respond_to_user_input(
        self,
        task_id: str,
        inbox_message_id: str,
        input_value: Any,
    ) -> str:
        """Provide user input response."""
        resp = make_user_input_response(
            task_id=task_id,
            inbox_message_id=inbox_message_id,
            input_value=input_value,
        )
        return self._write(resp)

    # -------------------------------------------------------------------------
    # Status updates
    # -------------------------------------------------------------------------

    def status_update(
        self,
        task_id: str,
        inbox_message_id: str,
        status: str,
        details: str = "",
    ) -> str:
        """Send a status update."""
        resp = ResponseMessage(
            task_id=task_id,
            inbox_message_id=inbox_message_id,
            type=ResponseType.STATUS_UPDATE,
            outcome=Outcome.SUCCESS,
            title=f"Status: {status}",
            output=details,
        )
        return self._write(resp)
