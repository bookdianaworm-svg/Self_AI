"""
Tests for BaseAgent class.
"""

import pytest

from rlm.agents.base.base_agent import BaseAgent, AgentConfig, AgentStatus


class TestBaseAgent:
    """Test suite for BaseAgent class."""

    def test_agent_creation(self):
        """Test agent creation with required fields."""
        agent = BaseAgent(id="test_agent_123")

        assert agent.id == "test_agent_123"
        assert agent.status == AgentStatus.IDLE
        assert agent.parent_id is None
        assert agent.config is not None
        assert agent.created_at is not None

    def test_agent_id_unique(self):
        """Test that agent IDs are unique when provided."""
        agent1 = BaseAgent(id="unique_agent_1")
        agent2 = BaseAgent(id="unique_agent_2")

        assert agent1.id != agent2.id
        assert agent1.id == "unique_agent_1"
        assert agent2.id == "unique_agent_2"

    def test_agent_state(self):
        """Test agent initial state is correct."""
        agent = BaseAgent(id="state_test")

        assert agent.status == AgentStatus.IDLE
        assert agent.result is None
        assert agent.error is None
        assert agent.metrics is not None
        assert agent.metrics.iterations == 0
        assert agent.metrics.errors == 0
        assert agent.child_agent_ids == []
        assert agent.message_handlers == []

    def test_agent_config_defaults(self):
        """Test default agent configuration."""
        agent = BaseAgent(id="config_test")

        assert agent.config.backend == "openai"
        assert agent.config.max_depth == 1
        assert agent.config.max_iterations == 30
        assert agent.config.can_spawn is False

    def test_agent_custom_config(self):
        """Test agent with custom configuration."""
        config = AgentConfig(
            backend="anthropic",
            max_depth=5,
            max_iterations=100,
            can_spawn=True,
        )
        agent = BaseAgent(id="custom_config", config=config)

        assert agent.config.backend == "anthropic"
        assert agent.config.max_depth == 5
        assert agent.config.max_iterations == 100
        assert agent.config.can_spawn is True

    def test_update_status(self):
        """Test updating agent status."""
        agent = BaseAgent(id="status_update_test")

        agent.update_status(AgentStatus.PLANNING)
        assert agent.status == AgentStatus.PLANNING

        agent.update_status(AgentStatus.EXECUTING)
        assert agent.status == AgentStatus.EXECUTING

    def test_get_info(self):
        """Test getting agent information."""
        agent = BaseAgent(id="info_test")
        info = agent.get_info()

        assert info["id"] == "info_test"
        assert info["status"] == "idle"
        assert "created_at" in info
        assert "config" in info
        assert "metrics" in info

    def test_can_spawn_agents(self):
        """Test checking if agent can spawn child agents."""
        agent_no_spawn = BaseAgent(id="no_spawn")
        assert agent_no_spawn.can_spawn_agents() is False

        config = AgentConfig(can_spawn=True)
        agent_spawn = BaseAgent(id="can_spawn", config=config)
        assert agent_spawn.can_spawn_agents() is True

    def test_terminate(self):
        """Test terminating an agent."""
        agent = BaseAgent(id="terminate_test")

        agent.terminate()

        assert agent.status == AgentStatus.TERMINATED

    def test_send_message(self):
        """Test sending messages to other agents."""
        agent = BaseAgent(id="sender")

        agent.send_message("recipient_1", {"content": "Hello"})

        assert len(agent.outbox) == 1
        assert agent.outbox[0]["recipient"] == "recipient_1"
        assert agent.outbox[0]["content"] == {"content": "Hello"}

    def test_broadcast_message(self):
        """Test broadcasting messages to child agents."""
        agent = BaseAgent(id="parent")
        child_id = "child_1"
        agent.child_agent_ids.append(child_id)

        agent.broadcast_message({"content": "Broadcast test"})

        assert len(agent.outbox) == 1
        assert agent.outbox[0]["recipient"] == child_id

    def test_register_message_handler(self):
        """Test registering message handlers."""
        agent = BaseAgent(id="handler_test")

        def handler(msg):
            pass

        agent.register_message_handler(handler)

        assert len(agent.message_handlers) == 1
        assert agent.message_handlers[0] is handler

    def test_receive_message(self):
        """Test receiving messages."""
        agent = BaseAgent(id="receiver_test")

        agent.receive_message({"content": "Test message"})

        assert not agent.inbox.empty()

    def test_spawn_agent_permission_denied(self):
        """Test that spawning is denied when not allowed."""
        agent = BaseAgent(id="no_spawn_test")

        with pytest.raises(PermissionError):
            agent.spawn_agent("Child task")

    def test_spawn_agent_max_children(self):
        """Test max child agents limit."""
        config = AgentConfig(can_spawn=True, max_child_agents=2)
        agent = BaseAgent(id="limited_spawn", config=config)

        child1 = agent.spawn_agent("Task 1")
        child2 = agent.spawn_agent("Task 2")

        with pytest.raises(RuntimeError):
            agent.spawn_agent("Task 3")

    def test_metrics_tracking(self):
        """Test that metrics are tracked correctly."""
        agent = BaseAgent(id="metrics_test")

        assert agent.metrics.iterations == 0
        assert agent.metrics.api_calls == 0
        assert agent.metrics.errors == 0
