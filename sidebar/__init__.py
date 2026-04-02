"""
Sidebar-to-Agent Inbox System (Bidirectional)

Message flow:
    Sidebar Agent → sidebar/inbox/<uuid>.json  →  Task Agent (polls)
    Task Agent   → sidebar/responses/<uuid>.json → Sidebar Agent (polls)

Usage:
    # Task agent (reads inbox, writes responses)
    from sidebar import InboxManager, ResponseWriter

    inbox = InboxManager()
    responses = ResponseWriter()

    # Sidebar agent (reads responses, writes inbox)
    from sidebar import InboxWriter, ResponseManager
"""

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

from .inbox_manager import InboxManager
from .writer import InboxWriter
from .self_awareness import (
    SelfAwarenessLoop,
    ReflectionEntry,
    ConfidenceLevel,
    pair_inbox_with_awareness,
)

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

from .response_manager import ResponseManager
from .response_writer import ResponseWriter

__all__ = [
    # Inbox (sidebar → agent)
    "InboxMessage",
    "InboxMessageType",
    "InboxPriority",
    "TaskStatus",
    "InboxManager",
    "InboxWriter",
    # Self-awareness
    "SelfAwarenessLoop",
    "ReflectionEntry",
    "ConfidenceLevel",
    "pair_inbox_with_awareness",
    # Inbox convenience
    "make_task_request",
    "make_self_awareness_prompt",
    "make_user_input_required",
    "make_status_update",
    # Response (agent → sidebar)
    "ResponseMessage",
    "ResponseType",
    "Outcome",
    "ResponseManager",
    "ResponseWriter",
    # Response convenience
    "make_completed",
    "make_failed",
    "make_reflection",
    "make_approval",
    "make_user_input_response",
]
