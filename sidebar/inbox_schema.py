"""
Sidebar-to-Agent Inbox Schema

Defines the JSON message format for sidebar agent → task agent communication.
Sidebar agent writes messages to `.sidebar/inbox/<task_id>.json`.
Task agent polls for new messages and surfaces them as prompts.

Message Flow:
    Sidebar Agent → writes → .sidebar/inbox/<task_id>.json
                                   ↓
                    Task Agent ← polls ← (poll interval: 5 seconds)

Schema Version: 1.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class InboxMessageType(Enum):
    """Types of inbox messages."""

    # Task directives
    TASK_REQUEST = "task_request"           # Sidebar requests a task be performed
    TASK_CANCEL = "task_cancel"             # Cancel an existing task
    TASK_REVISION = "task_revision"         # Revise parameters of a task

    # Status updates from sidebar
    STATUS_UPDATE = "status_update"         # UI state change notification
    USER_INPUT_REQUIRED = "user_input_required"  # Pauses for human input
    APPROVAL_REQUIRED = "approval_required"    # Needs explicit approval

    # Context sharing
    CONTEXT_SHARE = "context_share"         # Shared context/brain_state
    FILE_CHANGE = "file_change"             # File was modified externally
    EXTERNAL_EVENT = "external_event"        # Webhook, timer, etc.

    # Self-awareness pairing
    SELF_AWARENESS_PROMPT = "self_awareness_prompt"  # Self-reflection trigger
    METACOGNITIVE_CHECK = "metacognitive_check"    # Check internal state

    # Heartbeat/keepalive
    HEARTBEAT = "heartbeat"                 # Sidebar is alive


class InboxPriority(Enum):
    """Priority levels for inbox messages (lower = higher priority)."""

    LOW = 3
    NORMAL = 2
    HIGH = 1
    CRITICAL = 0  # Surfaces immediately, bypasses normal poll


class TaskStatus(Enum):
    """Status of an inbox task."""

    PENDING = "pending"       # Queued, not yet processed
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REVISED = "revised"


@dataclass
class InboxMessage:
    """
    A message in the sidebar-to-agent inbox.

    Written by: Sidebar Agent
    Read by: Task Agent (polling)

    File location: .sidebar/inbox/<message_id>.json
    """

    # Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""  # Correlates with kanban task or standalone work item
    type: InboxMessageType = InboxMessageType.TASK_REQUEST

    # Routing
    priority: InboxPriority = InboxPriority.NORMAL
    recipient: Optional[str] = None  # Specific agent ID or None for broadcast

    # Content
    title: str = ""
    description: str = ""  # Detailed description of what to do
    payload: Dict[str, Any] = field(default_factory=dict)  # Structured data

    # Self-awareness pairing
    self_awareness: bool = False  # If True, agent should do self-reflection
    reflection_prompt: Optional[str] = None  # Custom reflection question
    check_internal_state: Optional[Dict[str, Any]] = None  # State keys to verify

    # Metadata
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    expires_at: Optional[str] = None  # ISO timestamp, None = never expires
    retry_count: int = 0
    max_retries: int = 3
    status: TaskStatus = TaskStatus.PENDING

    # Source tracking
    source_agent: str = "sidebar"  # Always "sidebar" for inbox messages
    correlation_id: Optional[str] = None  # For tracing related messages

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for JSON storage."""
        return {
            "schema_version": "1.0",
            "id": self.id,
            "task_id": self.task_id,
            "type": self.type.value,
            "priority": self.priority.value,
            "recipient": self.recipient,
            "title": self.title,
            "description": self.description,
            "payload": self.payload,
            "self_awareness": self.self_awareness,
            "reflection_prompt": self.reflection_prompt,
            "check_internal_state": self.check_internal_state,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "status": self.status.value,
            "source_agent": self.source_agent,
            "correlation_id": self.correlation_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InboxMessage":
        """Deserialize from dict."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            task_id=data.get("task_id", ""),
            type=InboxMessageType(data.get("type", "task_request")),
            priority=InboxPriority(data.get("priority", 2)),
            recipient=data.get("recipient"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            payload=data.get("payload", {}),
            self_awareness=data.get("self_awareness", False),
            reflection_prompt=data.get("reflection_prompt"),
            check_internal_state=data.get("check_internal_state"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            expires_at=data.get("expires_at"),
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            status=TaskStatus(data.get("status", "pending")),
            source_agent=data.get("source_agent", "sidebar"),
            correlation_id=data.get("correlation_id"),
        )

    def is_expired(self) -> bool:
        """Check if message has expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > datetime.fromisoformat(self.expires_at)

    def can_retry(self) -> bool:
        """Check if message can be retried."""
        return self.retry_count < self.max_retries


# =============================================================================
# Convenience constructors for common message types
# =============================================================================

def make_task_request(
    task_id: str,
    title: str,
    description: str,
    payload: Optional[Dict[str, Any]] = None,
    priority: InboxPriority = InboxPriority.NORMAL,
    self_awareness: bool = False,
) -> InboxMessage:
    """Create a task request message."""
    return InboxMessage(
        task_id=task_id,
        type=InboxMessageType.TASK_REQUEST,
        title=title,
        description=description,
        payload=payload or {},
        priority=priority,
        self_awareness=self_awareness,
    )


def make_self_awareness_prompt(
    task_id: str,
    reflection_prompt: str,
    check_state: Optional[Dict[str, Any]] = None,
    priority: InboxPriority = InboxPriority.NORMAL,
) -> InboxMessage:
    """Create a self-awareness prompt message."""
    return InboxMessage(
        task_id=task_id,
        type=InboxMessageType.SELF_AWARENESS_PROMPT,
        title="Self-Awareness Check",
        description=reflection_prompt,
        self_awareness=True,
        reflection_prompt=reflection_prompt,
        check_internal_state=check_state,
        priority=priority,
    )


def make_user_input_required(
    task_id: str,
    prompt: str,
    payload: Optional[Dict[str, Any]] = None,
) -> InboxMessage:
    """Create a message requiring user input."""
    return InboxMessage(
        task_id=task_id,
        type=InboxMessageType.USER_INPUT_REQUIRED,
        title="User Input Required",
        description=prompt,
        payload=payload or {},
        priority=InboxPriority.HIGH,
    )


def make_status_update(
    task_id: str,
    status: str,
    details: Optional[str] = None,
) -> InboxMessage:
    """Create a status update message."""
    return InboxMessage(
        task_id=task_id,
        type=InboxMessageType.STATUS_UPDATE,
        title=f"Status: {status}",
        description=details or status,
        priority=InboxPriority.LOW,
    )
