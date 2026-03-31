"""
Tests for Message and related classes.
"""

import pytest
from datetime import datetime

from rlm.messaging.message_types import (
    Message,
    MessageType,
    MessagePriority,
    MessageContent,
    QueuedMessage,
)


class TestMessage:
    """Test suite for Message class."""

    def test_message_creation(self):
        """Test message creation with default values."""
        message = Message(
            sender="agent_1",
            recipients=["agent_2"],
            content=MessageContent(title="Test", body="Hello"),
        )

        assert message.sender == "agent_1"
        assert message.recipients == ["agent_2"]
        assert message.type == MessageType.QUERY
        assert message.priority == MessagePriority.NORMAL
        assert message.id is not None
        assert message.timestamp is not None
        assert message.status == "sent"

    def test_message_types(self):
        """Test different message types."""
        types_to_test = [
            MessageType.STATUS_UPDATE,
            MessageType.TASK_REQUEST,
            MessageType.TASK_COMPLETE,
            MessageType.TASK_FAILED,
            MessageType.BROADCAST,
            MessageType.QUERY,
            MessageType.RESPONSE,
        ]

        for msg_type in types_to_test:
            message = Message(
                sender="test",
                recipients=["test"],
                type=msg_type,
            )
            assert message.type == msg_type

    def test_message_priorities(self):
        """Test different message priorities."""
        priorities = [
            MessagePriority.LOW,
            MessagePriority.NORMAL,
            MessagePriority.HIGH,
            MessagePriority.CRITICAL,
        ]

        for priority in priorities:
            message = Message(
                sender="test",
                recipients=["test"],
                priority=priority,
            )
            assert message.priority == priority

    def test_message_to_dict(self):
        """Test converting message to dictionary."""
        message = Message(
            id="msg_123",
            sender="sender_1",
            recipients=["recipient_1"],
            type=MessageType.TASK_REQUEST,
            priority=MessagePriority.HIGH,
            content=MessageContent(title="Title", body="Body"),
        )

        msg_dict = message.to_dict()

        assert msg_dict["id"] == "msg_123"
        assert msg_dict["sender"] == "sender_1"
        assert msg_dict["recipients"] == ["recipient_1"]
        assert msg_dict["type"] == "task-request"
        assert msg_dict["priority"] == 3

    def test_message_from_dict(self):
        """Test creating message from dictionary."""
        data = {
            "id": "msg_456",
            "sender": "from_dict",
            "recipients": ["to_dict"],
            "type": "broadcast",
            "priority": "high",
            "content": {
                "title": "From Dict",
                "body": "Testing from_dict",
            },
        }

        message = Message.from_dict(data)

        assert message.id == "msg_456"
        assert message.sender == "from_dict"
        assert message.type == MessageType.BROADCAST
        assert message.priority == MessagePriority.HIGH
        assert message.content.title == "From Dict"

    def test_message_content_defaults(self):
        """Test MessageContent default values."""
        content = MessageContent()

        assert content.title == ""
        assert content.body == ""
        assert content.attachments == []
        assert content.metadata == {}

    def test_message_content_with_attachments(self):
        """Test MessageContent with attachments."""
        content = MessageContent(
            title="With attachments",
            body="Body text",
            attachments=["file1.txt", "file2.txt"],
            metadata={"key": "value"},
        )

        assert len(content.attachments) == 2
        assert content.metadata == {"key": "value"}


class TestQueuedMessage:
    """Test suite for QueuedMessage class."""

    def test_queued_message_creation(self):
        """Test QueuedMessage creation."""
        message = Message(
            sender="sender",
            recipients=["recipient"],
        )
        queued = QueuedMessage(
            message=message,
            priority=MessagePriority.HIGH,
        )

        assert queued.message is not None
        assert queued.priority == MessagePriority.HIGH
        assert queued.delivery_attempts == 0

    def test_queued_message_priority_ordering(self):
        """Test QueuedMessage priority comparison for queue ordering."""
        low_msg = QueuedMessage(
            message=Message(sender="a", recipients=["b"]),
            priority=MessagePriority.LOW,
        )
        high_msg = QueuedMessage(
            message=Message(sender="c", recipients=["d"]),
            priority=MessagePriority.HIGH,
        )

        assert low_msg < high_msg
