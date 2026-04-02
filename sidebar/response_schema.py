"""
Sidebar-to-Agent Response Schema

Agent responses written to `sidebar/responses/<response_id>.json`.
Polled by sidebar agent for task results and reflections.

Response flow:
    Task Agent → sidebar/responses/<response_id>.json → Sidebar Agent (polling)

Schema Version: 1.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class ResponseType(Enum):
    """Types of agent responses."""

    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    REFLECTION_RESULT = "reflection_result"
    STATUS_UPDATE = "status_update"
    APPROVAL_GRANTED = "approval_granted"
    APPROVAL_DENIED = "approval_denied"
    USER_INPUT_PROVIDED = "user_input_provided"
    STATE_VERIFICATION = "state_verification"


class Outcome(Enum):
    """Outcome of the agent's work."""

    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    PENDING = "pending"


@dataclass
class ResponseMessage:
    """
    A response message from task agent back to sidebar.

    Written by: Task Agent
    Read by: Sidebar Agent (polling)
    """

    # Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""  # Correlates to inbox task
    inbox_message_id: str = ""  # Which inbox message triggered this

    # Content
    type: ResponseType = ResponseType.TASK_COMPLETED
    title: str = ""
    description: str = ""
    outcome: Outcome = Outcome.SUCCESS

    # Results
    result: Optional[Dict[str, Any]] = None  # Structured result data
    output: str = ""  # Human-readable summary
    error: Optional[str] = None

    # Self-awareness results
    reflection_result: Optional[Dict[str, Any]] = None
    confidence: Optional[str] = None  # "high", "medium", "low"
    state_verified: Optional[Dict[str, bool]] = None

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    agent_id: str = "task-agent"
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for JSON storage."""
        return {
            "schema_version": "1.0",
            "id": self.id,
            "task_id": self.task_id,
            "inbox_message_id": self.inbox_message_id,
            "type": self.type.value,
            "title": self.title,
            "description": self.description,
            "outcome": self.outcome.value,
            "result": self.result,
            "output": self.output,
            "error": self.error,
            "reflection_result": self.reflection_result,
            "confidence": self.confidence,
            "state_verified": self.state_verified,
            "created_at": self.created_at,
            "agent_id": self.agent_id,
            "correlation_id": self.correlation_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResponseMessage":
        """Deserialize from dict."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            task_id=data.get("task_id", ""),
            inbox_message_id=data.get("inbox_message_id", ""),
            type=ResponseType(data.get("type", "task_completed")),
            title=data.get("title", ""),
            description=data.get("description", ""),
            outcome=Outcome(data.get("outcome", "success")),
            result=data.get("result"),
            output=data.get("output", ""),
            error=data.get("error"),
            reflection_result=data.get("reflection_result"),
            confidence=data.get("confidence"),
            state_verified=data.get("state_verified"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            agent_id=data.get("agent_id", "task-agent"),
            correlation_id=data.get("correlation_id"),
        )


# =============================================================================
# Convenience constructors
# =============================================================================

def make_completed(
    task_id: str,
    inbox_message_id: str,
    output: str,
    result: Optional[Dict[str, Any]] = None,
) -> ResponseMessage:
    """Create a task completed response."""
    return ResponseMessage(
        task_id=task_id,
        inbox_message_id=inbox_message_id,
        type=ResponseType.TASK_COMPLETED,
        outcome=Outcome.SUCCESS,
        title=f"Task {task_id} completed",
        output=output,
        result=result,
    )


def make_failed(
    task_id: str,
    inbox_message_id: str,
    error: str,
    output: str = "",
) -> ResponseMessage:
    """Create a task failed response."""
    return ResponseMessage(
        task_id=task_id,
        inbox_message_id=inbox_message_id,
        type=ResponseType.TASK_FAILED,
        outcome=Outcome.FAILURE,
        title=f"Task {task_id} failed",
        output=output,
        error=error,
    )


def make_reflection(
    task_id: str,
    inbox_message_id: str,
    what_went_well: str,
    what_could_improve: str,
    confidence: str,
    adjustments_planned: str,
    state_verified: Optional[Dict[str, bool]] = None,
) -> ResponseMessage:
    """Create a reflection result response."""
    return ResponseMessage(
        task_id=task_id,
        inbox_message_id=inbox_message_id,
        type=ResponseType.REFLECTION_RESULT,
        outcome=Outcome.SUCCESS,
        title="Self-reflection complete",
        reflection_result={
            "what_went_well": what_went_well,
            "what_could_improve": what_could_improve,
            "confidence": confidence,
            "adjustments_planned": adjustments_planned,
        },
        confidence=confidence,
        state_verified=state_verified,
    )


def make_approval(
    task_id: str,
    inbox_message_id: str,
    granted: bool,
    reason: str = "",
) -> ResponseMessage:
    """Create an approval response."""
    return ResponseMessage(
        task_id=task_id,
        inbox_message_id=inbox_message_id,
        type=ResponseType.APPROVAL_GRANTED if granted else ResponseType.APPROVAL_DENIED,
        outcome=Outcome.SUCCESS if granted else Outcome.FAILURE,
        title="Approval " + ("granted" if granted else "denied"),
        output=reason,
    )


def make_user_input_response(
    task_id: str,
    inbox_message_id: str,
    input_value: Any,
) -> ResponseMessage:
    """Create a user input response."""
    return ResponseMessage(
        task_id=task_id,
        inbox_message_id=inbox_message_id,
        type=ResponseType.USER_INPUT_PROVIDED,
        outcome=Outcome.SUCCESS,
        title="User input provided",
        result={"input": input_value},
    )
