"""
Async Message Queue for the Dual-Loop Architecture.

This module provides the communication channel between the Fast Loop (Skunkworks)
and the Slow Loop (The Crucible) via Release Candidates.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
from enum import Enum
import threading
import queue
import time
from collections import deque


class MessagePriority(Enum):
    """Priority levels for messages in the queue."""

    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


class MessageType(Enum):
    """Types of messages in the dual-loop system."""

    RELEASE_CANDIDATE = "release_candidate"
    INTERRUPT = "interrupt"
    CERTIFICATION_RESULT = "certification_result"
    REJECTION_RESULT = "rejection_result"
    LOOP_CONTROL = "loop_control"


@dataclass
class QueueMessage:
    """A message in the async queue."""

    id: str
    message_type: MessageType
    payload: Any
    priority: MessagePriority = MessagePriority.NORMAL
    created_at: float = field(default_factory=time.time)
    correlation_id: Optional[str] = None


@dataclass
class AsyncMessageQueue:
    """
    Thread-safe async message queue for dual-loop communication.

    This queue handles:
    - Release Candidates from Fast Loop to Slow Loop
    - Interrupts from Slow Loop to Fast Loop
    - Certification/Rejection results
    """

    def __init__(self, max_size: int = 1000):
        """
        Initialize the async message queue.

        Args:
            max_size: Maximum number of messages in queue before blocking
        """
        self._queue: queue.PriorityQueue = queue.PriorityQueue(maxsize=max_size)
        self._message_index: Dict[str, QueueMessage] = {}
        self._handlers: Dict[MessageType, List[Callable]] = {}
        self._lock = threading.Lock()
        self._history: deque = deque(maxlen=1000)
        self._stats = {
            "enqueued": 0,
            "dequeued": 0,
            "handlers_called": 0,
        }

    def enqueue(self, message: QueueMessage) -> bool:
        """
        Add a message to the queue.

        Args:
            message: The message to enqueue

        Returns:
            True if enqueued successfully, False if queue is full
        """
        try:
            # Invert priority so highest priority comes first (lower number = higher priority)
            priority = -message.priority.value
            self._queue.put((priority, message), block=False)
            with self._lock:
                self._message_index[message.id] = message
                self._history.append(message)
            self._stats["enqueued"] += 1
            return True
        except queue.Full:
            return False

    def dequeue(self, timeout: Optional[float] = None) -> Optional[QueueMessage]:
        """
        Remove and return a message from the queue.

        Args:
            timeout: Maximum time to wait for a message (None = block indefinitely)

        Returns:
            The next message or None if timeout/exit
        """
        try:
            _, message = self._queue.get(block=True, timeout=timeout)
            with self._lock:
                if message.id in self._message_index:
                    del self._message_index[message.id]
            self._stats["dequeued"] += 1
            return message
        except queue.Empty:
            return None

    def peek(self) -> Optional[QueueMessage]:
        """
        View the next message without removing it.

        Returns:
            The next message or None if queue is empty
        """
        try:
            # Priority queue doesn't support peek, so we use a temporary get/put
            _, message = self._queue.get(block=False)
            self._queue.put((_, message))
            return message
        except queue.Empty:
            return None

    def register_handler(
        self, message_type: MessageType, handler: Callable[[QueueMessage], None]
    ) -> None:
        """
        Register a handler for a specific message type.

        Args:
            message_type: Type of message to handle
            handler: Callback function that takes a QueueMessage
        """
        with self._lock:
            if message_type not in self._handlers:
                self._handlers[message_type] = []
            if handler not in self._handlers[message_type]:
                self._handlers[message_type].append(handler)

    def unregister_handler(
        self, message_type: MessageType, handler: Callable[[QueueMessage], None]
    ) -> None:
        """
        Unregister a handler for a specific message type.

        Args:
            message_type: Type of message
            handler: Handler to remove
        """
        with self._lock:
            if (
                message_type in self._handlers
                and handler in self._handlers[message_type]
            ):
                self._handlers[message_type].remove(handler)

    def dispatch_message(self, message: QueueMessage) -> None:
        """
        Dispatch a message to all registered handlers.

        Args:
            message: Message to dispatch
        """
        with self._lock:
            handlers = self._handlers.get(message.message_type, []).copy()

        for handler in handlers:
            try:
                handler(message)
                self._stats["handlers_called"] += 1
            except Exception:
                pass  # Handlers should not raise exceptions

    def get_message(self, message_id: str) -> Optional[QueueMessage]:
        """
        Retrieve a message by ID.

        Args:
            message_id: ID of the message to retrieve

        Returns:
            The message or None if not found
        """
        with self._lock:
            return self._message_index.get(message_id)

    def get_messages_by_type(self, message_type: MessageType) -> List[QueueMessage]:
        """
        Get all messages of a specific type.

        Args:
            message_type: Type of messages to retrieve

        Returns:
            List of messages matching the type
        """
        with self._lock:
            return [
                msg
                for msg in self._message_index.values()
                if msg.message_type == message_type
            ]

    def get_messages_by_correlation(self, correlation_id: str) -> List[QueueMessage]:
        """
        Get all messages with a specific correlation ID.

        Args:
            correlation_id: Correlation ID to search for

        Returns:
            List of messages with matching correlation ID
        """
        with self._lock:
            return [
                msg
                for msg in self._message_index.values()
                if msg.correlation_id == correlation_id
            ]

    def get_history(self, limit: int = 100) -> List[QueueMessage]:
        """
        Get the message history.

        Args:
            limit: Maximum number of messages to return

        Returns:
            List of recent messages
        """
        with self._lock:
            return list(self._history)[-limit:]

    def get_stats(self) -> Dict[str, int]:
        """
        Get queue statistics.

        Returns:
            Dictionary of queue statistics
        """
        with self._lock:
            return {
                **self._stats,
                "pending": self._queue.qsize(),
                "total_indexed": len(self._message_index),
            }

    def clear(self) -> int:
        """
        Clear all messages from the queue.

        Returns:
            Number of messages cleared
        """
        cleared = 0
        with self._lock:
            while not self._queue.empty():
                try:
                    self._queue.get_nowait()
                    cleared += 1
                except queue.Empty:
                    break
            self._message_index.clear()
        return cleared

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return self._queue.empty()

    def size(self) -> int:
        """Get the current number of messages in the queue."""
        return self._queue.qsize()
