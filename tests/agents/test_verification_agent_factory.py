"""
Tests for VerificationAgentFactory component.

This module tests VerificationAgentFactory class which handles:
- Autoformalization agent creation
- Verifier agent creation
- Physicist agent creation
- Cross-check agent creation
"""

from unittest.mock import MagicMock, patch

import pytest

from rlm.agents.verification_agent_factory import VerificationAgentFactory
from rlm.agents.prompts.verification_prompts import (
    AUTOFORMALIZATION_SYSTEM_PROMPT,
    VERIFIER_SYSTEM_PROMPT,
    PHYSICIST_SYSTEM_PROMPT,
    CROSS_CHECK_SYSTEM_PROMPT
)


class TestVerificationAgentFactoryInitialization:
    """
    Tests for VerificationAgentFactory initialization.
    """

    def test_init_with_parent_rlm(self, mock_parent_rlm: MagicMock):
        """
        Test that VerificationAgentFactory initializes with parent RLM.

        Args:
            mock_parent_rlm: Mock parent RLM fixture

        Expected behavior:
        - Should store parent RLM reference
        - Should initialize successfully
        """
        factory = VerificationAgentFactory(parent_rlm=mock_parent_rlm)
        assert factory.parent_rlm == mock_parent_rlm

    def test_init_without_parent_rlm(self):
        """
        Test that VerificationAgentFactory handles missing parent RLM.

        Expected behavior:
        - Should handle None gracefully
        - May raise exception or handle gracefully
        """
        try:
            factory = VerificationAgentFactory(parent_rlm=None)
            assert factory is not None
        except (TypeError, AttributeError):
            # Also acceptable to raise exception
            pass


class TestAutoformalizationAgentCreation:
    """
    Tests for Autoformalization agent creation.
    """

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_create_autoformalization_agent(self, mock_rlm_class):
        """
        Test creating an Autoformalization agent.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should create RLM instance with correct configuration
        - Should set environment to local
        - Should enable Layer1 tools
        - Should use AUTOFORMALIZATION_SYSTEM_PROMPT
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {"model": "gpt-4"}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        research_output = {"findings": "Mathematical pattern discovered"}
        agent = factory.create_autoformalization_agent(research_output)

        assert agent == mock_agent
        mock_rlm_class.assert_called_once()

        # Verify RLM was called with correct parameters
        call_kwargs = mock_rlm_class.call_args[1]
        assert call_kwargs["environment"] == "local"
        assert "enable_layer1" in call_kwargs.get("environment_kwargs", {})
        assert call_kwargs["custom_system_prompt"] == AUTOFORMALIZATION_SYSTEM_PROMPT
        assert call_kwargs["depth"] == 1
        assert call_kwargs["max_depth"] == 5

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_autoformalization_agent_tools(self, mock_rlm_class):
        """
        Test that Autoformalization agent has correct tools.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should include verify_lean tool
        - Should include get_layer1_axioms tool
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_autoformalization_agent({})

        # Check environment_kwargs
        call_kwargs = mock_rlm_class.call_args[1]
        env_kwargs = call_kwargs.get("environment_kwargs", {})
        assert "custom_tools" in env_kwargs
        tools = env_kwargs["custom_tools"]
        assert "verify_lean" in tools
        assert "get_layer1_axioms" in tools


class TestVerifierAgentCreation:
    """
    Tests for Verifier agent creation.
    """

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_create_verifier_agent(self, mock_rlm_class):
        """
        Test creating a Verifier agent.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should create RLM instance with correct configuration
        - Should set environment to local
        - Should enable Layer1 tools
        - Should use VERIFIER_SYSTEM_PROMPT
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {"model": "gpt-4"}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_verifier_agent("layer2/theorem1.lean")

        assert agent == mock_agent
        mock_rlm_class.assert_called_once()

        # Verify RLM was called with correct parameters
        call_kwargs = mock_rlm_class.call_args[1]
        assert call_kwargs["environment"] == "local"
        assert "enable_layer1" in call_kwargs.get("environment_kwargs", {})
        assert call_kwargs["custom_system_prompt"] == VERIFIER_SYSTEM_PROMPT

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_verifier_agent_tools(self, mock_rlm_class):
        """
        Test that Verifier agent has correct tools.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should include verify_lean tool
        - Should include prove_theorem tool
        - Should include get_layer1_axioms tool
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_verifier_agent("layer2/theorem1.lean")

        # Check environment_kwargs
        call_kwargs = mock_rlm_class.call_args[1]
        env_kwargs = call_kwargs.get("environment_kwargs", {})
        assert "custom_tools" in env_kwargs
        tools = env_kwargs["custom_tools"]
        assert "verify_lean" in tools
        assert "prove_theorem" in tools
        assert "get_layer1_axioms" in tools


class TestPhysicistAgentCreation:
    """
    Tests for Physicist agent creation.
    """

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_create_physicist_agent(self, mock_rlm_class):
        """
        Test creating a Physicist agent.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should create RLM instance with correct configuration
        - Should set environment to local
        - Should enable Layer1 tools
        - Should use PHYSICIST_SYSTEM_PROMPT
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {"model": "gpt-4"}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_physicist_agent(design_draft={}, layer2={})

        assert agent == mock_agent
        mock_rlm_class.assert_called_once()

        # Verify RLM was called with correct parameters
        call_kwargs = mock_rlm_class.call_args[1]
        assert call_kwargs["environment"] == "local"
        assert "enable_layer1" in call_kwargs.get("environment_kwargs", {})
        assert call_kwargs["custom_system_prompt"] == PHYSICIST_SYSTEM_PROMPT

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_physicist_agent_tools(self, mock_rlm_class):
        """
        Test that Physicist agent has correct tools.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should include verify_lean tool
        - Should include prove_theorem tool
        - Should include get_layer1_axioms tool
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_physicist_agent(design_draft={}, layer2={})

        # Check environment_kwargs
        call_kwargs = mock_rlm_class.call_args[1]
        env_kwargs = call_kwargs.get("environment_kwargs", {})
        assert "custom_tools" in env_kwargs
        tools = env_kwargs["custom_tools"]
        assert "verify_lean" in tools
        assert "prove_theorem" in tools
        assert "get_layer1_axioms" in tools


class TestCrossCheckAgentCreation:
    """
    Tests for Cross-check agent creation.
    """

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_create_cross_check_agent(self, mock_rlm_class):
        """
        Test creating a Cross-check agent.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should create RLM instance with correct configuration
        - Should set environment to local
        - Should enable Layer1 tools
        - Should use CROSS_CHECK_SYSTEM_PROMPT
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {"model": "gpt-4"}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_cross_check_agent(layer2_files=[])

        assert agent == mock_agent
        mock_rlm_class.assert_called_once()

        # Verify RLM was called with correct parameters
        call_kwargs = mock_rlm_class.call_args[1]
        assert call_kwargs["environment"] == "local"
        assert "enable_layer1" in call_kwargs.get("environment_kwargs", {})
        assert call_kwargs["custom_system_prompt"] == CROSS_CHECK_SYSTEM_PROMPT

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_cross_check_agent_tools(self, mock_rlm_class):
        """
        Test that Cross-check agent has correct tools.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should include verify_lean tool
        - Should include prove_theorem tool
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_cross_check_agent(layer2_files=[])

        # Check environment_kwargs
        call_kwargs = mock_rlm_class.call_args[1]
        env_kwargs = call_kwargs.get("environment_kwargs", {})
        assert "custom_tools" in env_kwargs
        tools = env_kwargs["custom_tools"]
        assert "verify_lean" in tools
        assert "prove_theorem" in tools


class TestAgentConfiguration:
    """
    Tests for agent configuration inheritance.
    """

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_backend_inheritance(self, mock_rlm_class):
        """
        Test that agents inherit backend from parent.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should use parent's backend
        - Should use parent's backend_kwargs
        """
        mock_parent = MagicMock()
        mock_parent.backend = "anthropic"
        mock_parent.backend_kwargs = {"model": "claude-3-opus", "api_key": "test-key"}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_verifier_agent("layer2/theorem1.lean")

        call_kwargs = mock_rlm_class.call_args[1]
        assert call_kwargs["backend"] == "anthropic"
        assert call_kwargs["backend_kwargs"] == {"model": "claude-3-opus", "api_key": "test-key"}

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_depth_inheritance(self, mock_rlm_class):
        """
        Test that agents increment depth from parent.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should use parent's depth + 1
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {}
        mock_parent.depth = 2
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_verifier_agent("layer2/theorem1.lean")

        call_kwargs = mock_rlm_class.call_args[1]
        assert call_kwargs["depth"] == 3  # parent depth + 1

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_max_depth_inheritance(self, mock_rlm_class):
        """
        Test that agents inherit max_depth from parent.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should use parent's max_depth
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {}
        mock_parent.depth = 0
        mock_parent.max_depth = 10
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_verifier_agent("layer2/theorem1.lean")

        call_kwargs = mock_rlm_class.call_args[1]
        assert call_kwargs["max_depth"] == 10

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_logger_inheritance(self, mock_rlm_class):
        """
        Test that agents inherit logger from parent.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should use parent's logger
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_verifier_agent("layer2/theorem1.lean")

        call_kwargs = mock_rlm_class.call_args[1]
        assert call_kwargs["logger"] == mock_parent.logger

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_verbose_disabled(self, mock_rlm_class):
        """
        Test that agents have verbose disabled.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should set verbose to False
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_verifier_agent("layer2/theorem1.lean")

        call_kwargs = mock_rlm_class.call_args[1]
        assert call_kwargs["verbose"] is False


class TestMultipleAgentCreation:
    """
    Tests for creating multiple agents from same factory.
    """

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_create_multiple_agents(self, mock_rlm_class):
        """
        Test creating multiple agents from same factory.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should create each agent correctly
        - Each agent should be independent
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)

        # Create multiple agents
        agent1 = factory.create_autoformalization_agent({})
        agent2 = factory.create_verifier_agent("layer2/theorem1.lean")
        agent3 = factory.create_physicist_agent(design_draft={}, layer2={})
        agent4 = factory.create_cross_check_agent(layer2_files=[])

        assert mock_rlm_class.call_count == 4


class TestErrorHandling:
    """
    Tests for error handling in agent creation.
    """

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_rlm_creation_exception(self, mock_rlm_class):
        """
        Test handling RLM creation exception.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should propagate exception
        - Should not catch or hide errors
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_rlm_class.side_effect = ValueError("Invalid configuration")

        factory = VerificationAgentFactory(parent_rlm=mock_parent)

        with pytest.raises(ValueError, match="Invalid configuration"):
            factory.create_verifier_agent("layer2/theorem1.lean")

    @patch('rlm.agents.verification_agent_factory.RLM')
    def test_create_agent_with_none_research_output(self, mock_rlm_class):
        """
        Test creating Autoformalization agent with None research output.

        Args:
            mock_rlm_class: Mocked RLM class

        Expected behavior:
        - Should handle None gracefully
        - Should still create agent
        """
        mock_parent = MagicMock()
        mock_parent.backend = "openai"
        mock_parent.backend_kwargs = {}
        mock_parent.depth = 0
        mock_parent.max_depth = 5
        mock_parent.logger = MagicMock()

        mock_agent = MagicMock()
        mock_rlm_class.return_value = mock_agent

        factory = VerificationAgentFactory(parent_rlm=mock_parent)
        agent = factory.create_autoformalization_agent(None)

        assert agent == mock_agent


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def mock_parent_rlm() -> MagicMock:
    """
    Provide a mock parent RLM instance.

    Returns:
        MagicMock configured as parent RLM
    """
    rlm = MagicMock()
    rlm.backend = "openai"
    rlm.backend_kwargs = {"model": "gpt-4", "api_key": "test-key"}
    rlm.depth = 0
    rlm.max_depth = 5
    rlm.logger = MagicMock()
    return rlm
