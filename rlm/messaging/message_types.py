"""
Message types for inter-agent communication.

This module defines the message types, priorities, and content
structures used in the messaging system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class MessageType(Enum):
    """Types of messages in the system."""

    # Status messages
    STATUS_UPDATE = "status-update"

    # Task messages
    TASK_REQUEST = "task-request"
    TASK_COMPLETE = "task-complete"
    TASK_FAILED = "task-failed"

    # Resource messages
    RESOURCE_REQUEST = "resource-request"
    RESOURCE_SHARE = "resource-share"

    # Tool messages
    TOOL_REQUEST = "tool-request"
    TOOL_SHARE = "tool-share"

    # Permission messages
    PERMISSION_REQUEST = "permission-request"
    PERMISSION_GRANTED = "permission-granted"
    PERMISSION_DENIED = "permission-denied"

    # Error messages
    ERROR_REPORT = "error-report"

    # Query/Response
    QUERY = "query"
    RESPONSE = "response"

    # Broadcast
    BROADCAST = "broadcast"

    # Lifecycle
    PAUSE_REQUEST = "pause-request"
    RESUME_REQUEST = "resume-request"
    TERMINATE_REQUEST = "terminate-request"

    # Improvement
    IMPROVEMENT_SHARE = "improvement-share"

    # Collaboration
    COLLABORATION = "collaboration"

    # System
    SYSTEM_ALERT = "system-alert"
    HEARTBEAT = "heartbeat"


class MessagePriority(Enum):
    """Priority levels for messages."""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class MessageContent:
    """Content of a message."""

    title: str = ""
    body: str = ""
    attachments: Optional[List[Any]] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Message:
    """
    A message in the messaging system.

    Messages are used for communication between agents, the main instance,
    and the user interface.
    """

    id: str = ""
    sender: str = ""  # Agent ID, 'user', or 'system'
    recipients: List[str] = field(
        default_factory=list
    )  # ['all'], ['user'], or agent IDs
    type: MessageType = MessageType.QUERY
    subtype: Optional[str] = None
    content: MessageContent = field(default_factory=MessageContent)
    timestamp: Optional[str] = None
    priority: MessagePriority = MessagePriority.NORMAL
    read_by: List[str] = field(default_factory=list)
    response_to: Optional[str] = None
    status: str = "sent"  # 'sent', 'delivered', 'read', 'failed'

    def __post_init__(self):
        if not self.id:
            import uuid

            self.id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "sender": self.sender,
            "recipients": self.recipients,
            "type": self.type.value
            if isinstance(self.type, MessageType)
            else self.type,
            "subtype": self.subtype,
            "content": {
                "title": self.content.title,
                "body": self.content.body,
                "attachments": self.content.attachments,
                "metadata": self.content.metadata,
            },
            "timestamp": self.timestamp,
            "priority": self.priority.value
            if isinstance(self.priority, MessagePriority)
            else self.priority,
            "read_by": self.read_by,
            "response_to": self.response_to,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create message from dictionary."""
        content_data = data.get("content", {})
        content = MessageContent(
            title=content_data.get("title", ""),
            body=content_data.get("body", ""),
            attachments=content_data.get("attachments"),
            metadata=content_data.get("metadata"),
        )

        msg_type = data.get("type", "query")
        if isinstance(msg_type, str):
            try:
                msg_type = MessageType(msg_type)
            except ValueError:
                msg_type = MessageType.QUERY

        priority = data.get("priority", "normal")
        if isinstance(priority, str):
            try:
                priority = MessagePriority[priority.upper()]
            except KeyError:
                priority = MessagePriority.NORMAL

        return cls(
            id=data.get("id", ""),
            sender=data.get("sender", ""),
            recipients=data.get("recipients", []),
            type=msg_type,
            subtype=data.get("subtype"),
            content=content,
            timestamp=data.get("timestamp"),
            priority=priority,
            read_by=data.get("read_by", []),
            response_to=data.get("response_to"),
            status=data.get("status", "sent"),
        )


@dataclass
class QueuedMessage:
    """A message with priority queued for delivery."""

    message: Message
    priority: MessagePriority
    created_at: datetime = field(default_factory=datetime.now)
    delivery_attempts: int = 0

    def __lt__(self, other: "QueuedMessage") -> bool:
        """Compare by priority for queue ordering."""
        return self.priority.value < other.priority.value
