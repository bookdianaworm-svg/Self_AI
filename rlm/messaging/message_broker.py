"""
Message Broker for inter-agent communication.

This module provides the central message broker that routes
messages between agents, the main instance, and the user.
"""

import asyncio
import json
import threading
import time
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from rlm.messaging.message_types import (
    Message,
    MessageType,
    MessagePriority,
    MessageContent,
    QueuedMessage,
)


class MessageBroker:
    """
    Central hub for routing messages between agents, the main instance, and the user.

    The message broker handles:
    - Agent registration/unregistration
    - Message routing (direct, broadcast, topic-based)
    - Callback management for user/system notifications
    - Message queuing and delivery
    """

    def __init__(self):
        """Initialize the message broker."""
        # Agent tracking
        self._agents: Dict[str, Any] = {}  # agent_id -> agent object
        self._agent_queues: Dict[str, asyncio.Queue] = {}  # agent_id -> message queue

        # Subscription tracking
        self._broadcast_subscribers: List[str] = []  # agents subscribed to broadcasts
        self._topic_subscribers: Dict[str, List[str]] = defaultdict(
            list
        )  # topic -> agent_ids

        # Callback tracking
        self._user_callbacks: List[Callable] = []
        self._system_callbacks: List[Callable] = []

        # Message history
        self._message_history: List[Message] = []
        self._max_history: int = 1000

        # Lock for thread safety
        self._lock = threading.Lock()

        # Processing state
        self._running = True
        self._processing_thread: Optional[threading.Thread] = None

        # Statistics
        self._stats = {
            "messages_sent": 0,
            "messages_delivered": 0,
            "messages_failed": 0,
            "broadcasts_sent": 0,
        }

    def start(self) -> None:
        """Start the message broker processing thread."""
        self._running = True
        self._processing_thread = threading.Thread(
            target=self._process_loop, daemon=True
        )
        self._processing_thread.start()

    def stop(self) -> None:
        """Stop the message broker."""
        self._running = False
        if self._processing_thread:
            self._processing_thread.join(timeout=5.0)

    def register_agent(self, agent_id: str, agent: Any) -> None:
        """
        Register an agent with the message broker.

        Args:
            agent_id: Unique identifier for the agent.
            agent: The agent object to receive messages.
        """
        with self._lock:
            self._agents[agent_id] = agent
            self._agent_queues[agent_id] = asyncio.Queue()

    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregister an agent from the message broker.

        Args:
            agent_id: ID of the agent to unregister.
        """
        with self._lock:
            self._agents.pop(agent_id, None)
            self._agent_queues.pop(agent_id, None)
            self._broadcast_subscribers = [
                sid for sid in self._broadcast_subscribers if sid != agent_id
            ]
            for topic in self._topic_subscribers:
                self._topic_subscribers[topic] = [
                    sid for sid in self._topic_subscribers[topic] if sid != agent_id
                ]

    def subscribe_to_broadcasts(self, agent_id: str) -> None:
        """
        Subscribe an agent to broadcast messages.

        Args:
            agent_id: ID of the agent to subscribe.
        """
        with self._lock:
            if agent_id not in self._broadcast_subscribers:
                self._broadcast_subscribers.append(agent_id)

    def unsubscribe_from_broadcasts(self, agent_id: str) -> None:
        """
        Unsubscribe an agent from broadcast messages.

        Args:
            agent_id: ID of the agent to unsubscribe.
        """
        with self._lock:
            self._broadcast_subscribers = [
                sid for sid in self._broadcast_subscribers if sid != agent_id
            ]

    def subscribe_to_topic(self, agent_id: str, topic: str) -> None:
        """
        Subscribe an agent to a specific topic.

        Args:
            agent_id: ID of the agent to subscribe.
            topic: The topic to subscribe to.
        """
        with self._lock:
            if agent_id not in self._topic_subscribers[topic]:
                self._topic_subscribers[topic].append(agent_id)

    def unsubscribe_from_topic(self, agent_id: str, topic: str) -> None:
        """
        Unsubscribe an agent from a specific topic.

        Args:
            agent_id: ID of the agent to unsubscribe.
            topic: The topic to unsubscribe from.
        """
        with self._lock:
            if topic in self._topic_subscribers:
                self._topic_subscribers[topic] = [
                    sid for sid in self._topic_subscribers[topic] if sid != agent_id
                ]

    def send_message(self, message: Message) -> bool:
        """
        Send a message to appropriate recipients.

        Args:
            message: The message to send.

        Returns:
            True if message was sent successfully, False otherwise.
        """
        # Validate message
        if not self._validate_message(message):
            return False

        # Route message based on recipients
        if "all" in message.recipients:
            self._route_to_all(message)
        elif "user" in message.recipients:
            self._route_to_user(message)
        elif "system" in message.recipients:
            self._route_to_system(message)
        else:
            # Send to specific agents
            for recipient_id in message.recipients:
                self._route_to_agent(recipient_id, message)

        # Record in history
        self._add_to_history(message)
        self._stats["messages_sent"] += 1

        return True

    def send_to_agent(self, recipient_id: str, message: Message) -> bool:
        """
        Send a message to a specific agent.

        Args:
            recipient_id: ID of the recipient agent.
            message: The message to send.

        Returns:
            True if delivered, False otherwise.
        """
        message.recipients = [recipient_id]
        return self.send_message(message)

    def broadcast(
        self,
        sender_id: str,
        content: MessageContent,
        priority: MessagePriority = MessagePriority.NORMAL,
    ) -> bool:
        """
        Broadcast a message to all subscribers.

        Args:
            sender_id: ID of the sending agent.
            content: Content of the broadcast.
            priority: Message priority.

        Returns:
            True if broadcast was sent.
        """
        message = Message(
            sender=sender_id,
            recipients=["all"],
            type=MessageType.BROADCAST,
            content=content,
            priority=priority,
        )

        with self._lock:
            for subscriber_id in self._broadcast_subscribers:
                self._route_to_agent(subscriber_id, message)

        self._stats["broadcasts_sent"] += 1
        return True

    def publish_to_topic(
        self, sender_id: str, topic: str, content: MessageContent
    ) -> bool:
        """
        Publish a message to a topic.

        Args:
            sender_id: ID of the sending agent.
            topic: Topic to publish to.
            content: Content of the message.

        Returns:
            True if published.
        """
        message = Message(
            sender=sender_id,
            recipients=self._topic_subscribers.get(topic, []),
            type=MessageType.BROADCAST,
            content=content,
            metadata={"topic": topic},
        )

        with self._lock:
            for subscriber_id in self._topic_subscribers.get(topic, []):
                self._route_to_agent(subscriber_id, message)

        return True

    def add_user_callback(self, callback: Callable) -> None:
        """
        Add a callback for user-bound messages.

        Args:
            callback: Function to call with messages.
        """
        with self._lock:
            self._user_callbacks.append(callback)

    def remove_user_callback(self, callback: Callable) -> None:
        """
        Remove a user callback.

        Args:
            callback: Function to remove.
        """
        with self._lock:
            self._user_callbacks = [cb for cb in self._user_callbacks if cb != callback]

    def add_system_callback(self, callback: Callable) -> None:
        """
        Add a callback for system-bound messages.

        Args:
            callback: Function to call with messages.
        """
        with self._lock:
            self._system_callbacks.append(callback)

    def remove_system_callback(self, callback: Callable) -> None:
        """
        Remove a system callback.

        Args:
            callback: Function to remove.
        """
        with self._lock:
            self._system_callbacks = [
                cb for cb in self._system_callbacks if cb != callback
            ]

    def get_message_history(
        self,
        agent_id: Optional[str] = None,
        message_type: Optional[MessageType] = None,
        limit: int = 100,
    ) -> List[Message]:
        """
        Get message history.

        Args:
            agent_id: Filter by recipient/sender.
            message_type: Filter by message type.
            limit: Maximum number of messages to return.

        Returns:
            List of matching messages.
        """
        messages = self._message_history[-limit:]

        if agent_id:
            messages = [
                m for m in messages if m.sender == agent_id or agent_id in m.recipients
            ]

        if message_type:
            messages = [m for m in messages if m.type == message_type]

        return messages

    def get_stats(self) -> Dict[str, Any]:
        """
        Get broker statistics.

        Returns:
            Dictionary of statistics.
        """
        return dict(self._stats)

    def _validate_message(self, message: Message) -> bool:
        """Validate a message before sending."""
        if not message.sender:
            return False
        if not message.recipients:
            return False
        if not message.content:
            return False
        return True

    def _route_to_agent(self, agent_id: str, message: Message) -> None:
        """Route a message to a specific agent."""
        if agent_id in self._agent_queues:
            try:
                self._agent_queues[agent_id].put_nowait(message)
                self._stats["messages_delivered"] += 1
            except asyncio.QueueFull:
                self._stats["messages_failed"] += 1
        else:
            self._stats["messages_failed"] += 1

    def _route_to_all(self, message: Message) -> None:
        """Route a message to all registered agents and user."""
        # Send to all agents
        for agent_id in list(self._agents.keys()):
            self._route_to_agent(agent_id, message)

        # Send to user
        self._route_to_user(message)

    def _route_to_user(self, message: Message) -> None:
        """Route a message to user callbacks."""
        for callback in self._user_callbacks:
            try:
                callback(message)
            except Exception:
                pass  # Don't let callback errors break message routing

    def _route_to_system(self, message: Message) -> None:
        """Route a message to system callbacks."""
        for callback in self._system_callbacks:
            try:
                callback(message)
            except Exception:
                pass

    def _add_to_history(self, message: Message) -> None:
        """Add a message to history."""
        with self._lock:
            self._message_history.append(message)
            if len(self._message_history) > self._max_history:
                self._message_history = self._message_history[-self._max_history :]

    def _process_loop(self) -> None:
        """Background loop for processing messages."""
        while self._running:
            # Process agent queues
            for agent_id, queue in list(self._agent_queues.items()):
                try:
                    while not queue.empty():
                        message = queue.get_nowait()
                        if agent_id in self._agents:
                            agent = self._agents[agent_id]
                            if hasattr(agent, "receive_message"):
                                agent.receive_message(message)
                except asyncio.QueueEmpty:
                    continue
                except Exception:
                    pass

            time.sleep(0.01)  # Prevent busy waiting

    def get_agent_count(self) -> int:
        """Get the number of registered agents."""
        return len(self._agents)

    def get_subscriber_count(self, topic: Optional[str] = None) -> int:
        """
        Get subscriber count.

        Args:
            topic: Optional topic to get count for.

        Returns:
            Number of subscribers.
        """
        if topic:
            return len(self._topic_subscribers.get(topic, []))
        return len(self._broadcast_subscribers)
