"""
Redux slice for messages state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class MessagePriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MessageEntity:
    message_id: str
    sender_id: str
    recipient_id: str
    content: str
    timestamp: float
    priority: MessagePriority = MessagePriority.NORMAL
    read: bool = False
    archived: bool = False


@dataclass
class MessageThread:
    thread_id: str
    participant_ids: List[str] = field(default_factory=list)
    messages: List[MessageEntity] = field(default_factory=list)
    last_activity: float = 0.0
    archived: bool = False


@dataclass
class MessageRetention:
    max_threads: int = 50
    auto_archive_after: int = 10
    persist_all: bool = False


@dataclass
class MessagesState:
    threads: Dict[str, MessageThread] = field(default_factory=dict)
    inbox: Dict[str, List[MessageEntity]] = field(default_factory=dict)
    outbox: List[MessageEntity] = field(default_factory=list)
    unread_counts: Dict[str, int] = field(default_factory=dict)
    retention: MessageRetention = field(default_factory=MessageRetention)


class MessagesActions:
    @staticmethod
    def send_message(recipient_id: str, content: str, priority: MessagePriority = MessagePriority.NORMAL) -> dict:
        return {"type": "messages/send_message", "payload": {"recipient_id": recipient_id, "content": content, "priority": priority.value}}

    @staticmethod
    def broadcast_message(content: str, recipients: str = "all", group_id: Optional[str] = None) -> dict:
        return {"type": "messages/broadcast_message", "payload": {"content": content, "recipients": recipients, "group_id": group_id}}

    @staticmethod
    def mark_read(message_id: str) -> dict:
        return {"type": "messages/mark_read", "payload": {"message_id": message_id}}

    @staticmethod
    def archive_thread(thread_id: str) -> dict:
        return {"type": "messages/archive_thread", "payload": {"thread_id": thread_id}}

    @staticmethod
    def receive_message(message: MessageEntity) -> dict:
        return {"type": "messages/receive_message", "payload": message}

    @staticmethod
    def set_retention(max_threads: Optional[int] = None, auto_archive_after: Optional[int] = None, persist_all: Optional[bool] = None) -> dict:
        return {"type": "messages/set_retention", "payload": {"max_threads": max_threads, "auto_archive_after": auto_archive_after, "persist_all": persist_all}}


def messages_reducer(state: MessagesState, action: dict) -> MessagesState:
    action_type = action.get("type")

    if action_type == "messages/send_message":
        payload = action.get("payload", {})
        recipient_id = payload.get("recipient_id")
        content = payload.get("content")
        priority_str = payload.get("priority", "normal")
        new_outbox = state.outbox.copy()
        new_outbox.append(MessageEntity(
            message_id=f"msg-{len(new_outbox)}",
            sender_id="user",
            recipient_id=recipient_id,
            content=content,
            timestamp=payload.get("timestamp", 0.0),
            priority=MessagePriority(priority_str)
        ))
        return MessagesState(
            threads=state.threads,
            inbox=state.inbox,
            outbox=new_outbox,
            unread_counts=state.unread_counts,
            retention=state.retention
        )

    elif action_type == "messages/broadcast_message":
        payload = action.get("payload", {})
        content = payload.get("content")
        return state

    elif action_type == "messages/mark_read":
        payload = action.get("payload", {})
        message_id = payload.get("message_id")
        new_inbox = state.inbox.copy()
        new_unread = state.unread_counts.copy()
        for recipient, messages in new_inbox.items():
            for msg in messages:
                if msg.message_id == message_id:
                    msg.read = True
                    if recipient in new_unread and new_unread[recipient] > 0:
                        new_unread[recipient] -= 1
                    break
        return MessagesState(
            threads=state.threads,
            inbox=new_inbox,
            outbox=state.outbox,
            unread_counts=new_unread,
            retention=state.retention
        )

    elif action_type == "messages/archive_thread":
        payload = action.get("payload", {})
        thread_id = payload.get("thread_id")
        new_threads = state.threads.copy()
        if thread_id in new_threads:
            new_threads[thread_id].archived = True
        return MessagesState(
            threads=new_threads,
            inbox=state.inbox,
            outbox=state.outbox,
            unread_counts=state.unread_counts,
            retention=state.retention
        )

    elif action_type == "messages/receive_message":
        message: Any = action.get("payload")
        if message is None:
            return state
        new_inbox = state.inbox.copy()
        recipient = message.recipient_id
        if recipient not in new_inbox:
            new_inbox[recipient] = []
        new_inbox[recipient].append(message)
        new_unread = state.unread_counts.copy()
        new_unread[recipient] = new_unread.get(recipient, 0) + 1
        return MessagesState(
            threads=state.threads,
            inbox=new_inbox,
            outbox=state.outbox,
            unread_counts=new_unread,
            retention=state.retention
        )

    elif action_type == "messages/set_retention":
        payload = action.get("payload", {})
        new_retention = MessageRetention(
            max_threads=payload.get("max_threads", state.retention.max_threads),
            auto_archive_after=payload.get("auto_archive_after", state.retention.auto_archive_after),
            persist_all=payload.get("persist_all", state.retention.persist_all)
        )
        return MessagesState(
            threads=state.threads,
            inbox=state.inbox,
            outbox=state.outbox,
            unread_counts=state.unread_counts,
            retention=new_retention
        )

    return state
