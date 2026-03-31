"""
Tests for MessageBroker class.
"""

import pytest

from rlm.messaging.message_broker import MessageBroker
from rlm.messaging.message_types import (
    Message,
    MessageType,
    MessagePriority,
    MessageContent,
)


class TestMessageBroker:
    """Test suite for MessageBroker class."""

    def test_publish_subscribe(self):
        """Test basic publish and subscribe functionality."""
        broker = MessageBroker()
        broker.start()
        received_messages = []

        class MockAgent:
            def __init__(self, agent_id):
                self.agent_id = agent_id
                self.inbox = []

            def receive_message(self, message):
                self.inbox.append(message)

        agent1 = MockAgent("agent_1")
        agent2 = MockAgent("agent_2")

        broker.register_agent("agent_1", agent1)
        broker.register_agent("agent_2", agent2)

        message = Message(
            sender="agent_1",
            recipients=["agent_2"],
            content=MessageContent(title="Direct", body="Hello"),
        )

        broker.send_message(message)

        import time

        time.sleep(0.1)

        assert len(agent2.inbox) == 1
        assert agent2.inbox[0].content.title == "Direct"

        broker.stop()

    def test_multiple_subscribers(self):
        """Test message delivered to multiple subscribers."""
        broker = MessageBroker()
        broker.start()

        class MockAgent:
            def __init__(self, agent_id):
                self.agent_id = agent_id
                self.inbox = []

            def receive_message(self, message):
                self.inbox.append(message)

        agent1 = MockAgent("agent_1")
        agent2 = MockAgent("agent_2")
        agent3 = MockAgent("agent_3")

        broker.register_agent("agent_1", agent1)
        broker.register_agent("agent_2", agent2)
        broker.register_agent("agent_3", agent3)

        message = Message(
            sender="system",
            recipients=["agent_1", "agent_2", "agent_3"],
            content=MessageContent(title="Multi", body="All get this"),
        )

        broker.send_message(message)

        import time

        time.sleep(0.1)

        assert len(agent1.inbox) == 1
        assert len(agent2.inbox) == 1
        assert len(agent3.inbox) == 1

        broker.stop()

    def test_unsubscribe(self):
        """Test unsubscribing from broadcasts."""
        broker = MessageBroker()
        broker.start()

        class MockAgent:
            def __init__(self, agent_id):
                self.agent_id = agent_id
                self.inbox = []

            def receive_message(self, message):
                self.inbox.append(message)

        agent = MockAgent("agent_1")
        broker.register_agent("agent_1", agent)
        broker.subscribe_to_broadcasts("agent_1")

        broker.broadcast(
            sender_id="system",
            content=MessageContent(title="Before unsub", body="Text"),
        )

        import time

        time.sleep(0.1)

        assert len(agent.inbox) == 1

        broker.unsubscribe_from_broadcasts("agent_1")

        broker.broadcast(
            sender_id="system",
            content=MessageContent(title="After unsub", body="Text"),
        )

        time.sleep(0.1)

        assert len(agent.inbox) == 1

        broker.stop()

    def test_message_priority_ordering(self):
        """Test that message priority is recorded correctly."""
        broker = MessageBroker()
        stats = broker.get_stats()

        message = Message(
            sender="agent_1",
            recipients=["agent_2"],
            content=MessageContent(title="Priority", body="Test"),
            priority=MessagePriority.CRITICAL,
        )

        broker.send_message(message)

        stats_after = broker.get_stats()
        assert stats_after["messages_sent"] == 1

    def test_broadcast(self):
        """Test broadcast to all subscribers."""
        broker = MessageBroker()
        broker.start()

        class MockAgent:
            def __init__(self, agent_id):
                self.agent_id = agent_id
                self.inbox = []

            def receive_message(self, message):
                self.inbox.append(message)

        agent1 = MockAgent("agent_1")
        agent2 = MockAgent("agent_2")

        broker.register_agent("agent_1", agent1)
        broker.register_agent("agent_2", agent2)

        broker.subscribe_to_broadcasts("agent_1")
        broker.subscribe_to_broadcasts("agent_2")

        broker.broadcast(
            sender_id="system",
            content=MessageContent(title="Broadcast", body="Hello everyone"),
            priority=MessagePriority.HIGH,
        )

        import time

        time.sleep(0.1)

        assert len(agent1.inbox) == 1
        assert len(agent2.inbox) == 1
        assert agent1.inbox[0].content.title == "Broadcast"
        assert agent2.inbox[0].content.title == "Broadcast"

        broker.stop()

    def test_send_to_agent(self):
        """Test sending message to specific agent."""
        broker = MessageBroker()
        broker.start()

        class MockAgent:
            def __init__(self, agent_id):
                self.agent_id = agent_id
                self.inbox = []

            def receive_message(self, message):
                self.inbox.append(message)

        agent1 = MockAgent("agent_1")
        agent2 = MockAgent("agent_2")

        broker.register_agent("agent_1", agent1)
        broker.register_agent("agent_2", agent2)

        message = Message(
            sender="agent_1",
            recipients=["agent_2"],
            content=MessageContent(title="Direct", body="Private"),
        )

        broker.send_to_agent("agent_2", message)

        import time

        time.sleep(0.1)

        assert len(agent1.inbox) == 0
        assert len(agent2.inbox) == 1

        broker.stop()

    def test_register_unregister_agent(self):
        """Test agent registration and unregistration."""
        broker = MessageBroker()

        class MockAgent:
            def __init__(self, agent_id):
                self.agent_id = agent_id

        agent = MockAgent("test_agent")

        broker.register_agent("test_agent", agent)
        assert broker.get_agent_count() == 1

        broker.unregister_agent("test_agent")
        assert broker.get_agent_count() == 0

    def test_message_history(self):
        """Test message history tracking."""
        broker = MessageBroker()

        message = Message(
            sender="agent_1",
            recipients=["agent_2"],
            content=MessageContent(title="History", body="Record this"),
        )

        broker.send_message(message)

        history = broker.get_message_history()
        assert len(history) == 1
        assert history[0].content.title == "History"

    def test_get_stats(self):
        """Test getting broker statistics."""
        broker = MessageBroker()

        stats = broker.get_stats()

        assert "messages_sent" in stats
        assert "messages_delivered" in stats
        assert "messages_failed" in stats
        assert "broadcasts_sent" in stats

    def test_topic_subscription(self):
        """Test subscribing to topics and checking subscriber count."""
        broker = MessageBroker()

        class MockAgent:
            def __init__(self, agent_id):
                self.agent_id = agent_id
                self.inbox = []

            def receive_message(self, message):
                self.inbox.append(message)

        agent = MockAgent("agent_1")
        broker.register_agent("agent_1", agent)
        broker.subscribe_to_topic("agent_1", "updates")

        assert broker.get_subscriber_count("updates") == 1
        assert broker.get_subscriber_count("other_topic") == 0

    def test_message_validation(self):
        """Test message validation."""
        broker = MessageBroker()

        invalid_message = Message(
            sender="",
            recipients=["agent_1"],
            content=MessageContent(title="Invalid", body="No sender"),
        )

        result = broker.send_message(invalid_message)
        assert result is False
