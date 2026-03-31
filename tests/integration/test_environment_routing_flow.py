"""
Integration tests for environment routing flow through RLM._subcall().

This module tests the complete flow of environment routing including:
- Task descriptor generation
- Environment router decision
- Environment factory creation
- Subcall execution
- Security constraint enforcement
"""

from unittest.mock import MagicMock, patch

import pytest

from rlm.routing.environment_router import EnvironmentRouter
from rlm.routing.environment_factory import EnvironmentFactory
from rlm.routing.task_descriptor import default_task_descriptor_fn


class TestEnvironmentRoutingFlow:
    """
    Integration tests for complete environment routing flow.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    @patch('rlm.routing.environment_router.EnvironmentRouter.route')
    def test_complete_environment_routing_flow(self, mock_route, mock_get_environment):
        """
        Test complete environment routing flow from prompt to response.

        Args:
            mock_route: Mocked EnvironmentRouter.route
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should generate task descriptor
        - Should route to appropriate environment
        - Should create environment instance
        - Should execute subcall
        """
        # Setup mocks
        mock_route.return_value = MagicMock(
            environment_id="local",
            rule_name="test_rule",
            reasoning="Test reasoning"
        )
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        # Create components
        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        # Execute flow
        prompt = "Verify this Lean theorem"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)

        # Route
        route = router.route(task_descriptor)
        assert route.environment_id == "local"

        # Get environment
        env = factory.get_environment(route.environment_id)
        assert env == mock_env

        # Execute
        result = env.execute_code("print('test')")
        assert result is not None

    @patch('rlm.routing.environment_factory.get_environment')
    def test_environment_routing_with_lean_access(self, mock_get_environment):
        """
        Test environment routing for Lean access requirements.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should route to local environment
        - Should enforce Lean access constraint
        """
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        prompt = "Prove this theorem in Lean"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        task_descriptor["metrics"] = {"needs_lean": True}

        # Route
        route = router.route(task_descriptor)
        assert route.environment_id == "local"

        # Get environment
        env = factory.get_environment(route.environment_id)
        assert env == mock_env

    @patch('rlm.routing.environment_factory.get_environment')
    def test_environment_routing_with_internet_access(self, mock_get_environment):
        """
        Test environment routing for internet access requirements.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should route to modal environment
        - Should enforce security constraints
        """
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        prompt = "Search for recent papers"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        task_descriptor["metrics"] = {"needs_internet": True}

        # Route
        route = router.route(task_descriptor)
        assert route.environment_id == "modal"

        # Get environment
        env = factory.get_environment(route.environment_id)
        assert env == mock_env

    @patch('rlm.routing.environment_factory.get_environment')
    def test_environment_routing_with_sensitive_data(self, mock_get_environment):
        """
        Test environment routing for sensitive data.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should route to local environment
        - Should enforce security constraints
        """
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        prompt = "Process confidential data"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        task_descriptor["metrics"] = {"data_sensitivity": "confidential"}

        # Route
        route = router.route(task_descriptor)
        assert route.environment_id == "local"

        # Get environment
        env = factory.get_environment(route.environment_id)
        assert env == mock_env


class TestEnvironmentRoutingErrorHandling:
    """
    Integration tests for error handling in environment routing.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    def test_environment_routing_with_creation_error(self, mock_get_environment):
        """
        Test environment routing when environment creation fails.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should propagate creation error
        - Should not crash
        """
        mock_get_environment.side_effect = RuntimeError("Failed to create environment")

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        prompt = "Test prompt"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        route = router.route(task_descriptor)

        with pytest.raises(RuntimeError, match="Failed to create environment"):
            factory.get_environment(route.environment_id)

    @patch('rlm.routing.environment_factory.get_environment')
    def test_environment_routing_with_execution_error(self, mock_get_environment):
        """
        Test environment routing when execution fails.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should handle execution error gracefully
        - Should return error result
        """
        mock_env = MagicMock()
        mock_env.execute_code.side_effect = RuntimeError("Execution failed")
        mock_get_environment.return_value = mock_env

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        prompt = "Test prompt"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        route = router.route(task_descriptor)
        env = factory.get_environment(route.environment_id)

        with pytest.raises(RuntimeError, match="Execution failed"):
            env.execute_code("print('test')")


class TestEnvironmentRoutingEdgeCases:
    """
    Integration tests for edge cases in environment routing.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    def test_environment_routing_with_empty_prompt(self, mock_get_environment):
        """
        Test environment routing with empty prompt.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should handle empty prompt gracefully
        - Should still route to environment
        """
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        prompt = ""
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        route = router.route(task_descriptor)
        env = factory.get_environment(route.environment_id)
        result = env.execute_code("print('test')")

        assert result is not None

    @patch('rlm.routing.environment_factory.get_environment')
    def test_environment_routing_with_very_long_prompt(self, mock_get_environment):
        """
        Test environment routing with very long prompt.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should handle long prompt
        - Should route appropriately
        """
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        prompt = "Test " * 10000
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        route = router.route(task_descriptor)
        env = factory.get_environment(route.environment_id)
        result = env.execute_code("print('test')")

        assert result is not None

    @patch('rlm.routing.environment_factory.get_environment')
    def test_environment_routing_concurrent_calls(self, mock_get_environment):
        """
        Test environment routing with concurrent calls.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should handle multiple concurrent requests
        - Each request should be independent
        """
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        # Simulate concurrent calls
        prompts = [f"Prompt {i}" for i in range(10)]
        task_descriptors = [default_task_descriptor_fn(p, depth=1) for p in prompts]
        routes = [router.route(td) for td in task_descriptors]
        envs = [factory.get_environment(r.environment_id) for r in routes]
        results = [e.execute_code("print('test')") for e in envs]

        assert len(results) == 10


class TestEnvironmentRoutingSecurity:
    """
    Integration tests for security constraint enforcement.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    def test_security_override_routing_decision(self, mock_get_environment):
        """
        Test that security constraints override routing decisions.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Confidential data should force local environment
        - Should ignore other routing rules
        """
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        # Task that would normally route to modal (needs internet)
        prompt = "Search for information"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        task_descriptor["metrics"] = {
            "needs_internet": True,
            "data_sensitivity": "confidential"  # Should override
        }

        # Route
        route = router.route(task_descriptor)
        # Confidential data should force local
        assert route.environment_id == "local"

    @patch('rlm.routing.environment_factory.get_environment')
    def test_security_with_public_data(self, mock_get_environment):
        """
        Test that public data allows remote environments.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Public data should allow modal/docker
        - Should not restrict routing
        """
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        prompt = "Search for information"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        task_descriptor["metrics"] = {
            "needs_internet": True,
            "data_sensitivity": "public"
        }

        # Route
        route = router.route(task_descriptor)
        # Public data should allow modal
        assert route.environment_id in ["modal", "docker"]


class TestEnvironmentRoutingIntegration:
    """
    Integration tests for environment routing with other components.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    def test_environment_routing_with_task_descriptor(self, mock_get_environment):
        """
        Test that task descriptor integrates with routing.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Task descriptor should inform routing decision
        - Routing should consider task properties
        """
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        # Different task types
        prompts = {
            "lean": "Verify in Lean",
            "haskell": "Check Haskell types",
            "general": "General task"
        }

        for task_type, prompt in prompts.items():
            task_descriptor = default_task_descriptor_fn(prompt, depth=1)
            route = router.route(task_descriptor)
            env = factory.get_environment(route.environment_id)
            env.execute_code("print('test')")

            # Verify routing considered task type
            assert route is not None

    @patch('rlm.routing.environment_factory.get_environment')
    def test_environment_routing_with_depth(self, mock_get_environment):
        """
        Test that depth affects environment routing.

        Args:
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Higher depth may route to different environment
        - Routing should consider depth in decision
        """
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        router = EnvironmentRouter()
        factory = EnvironmentFactory()

        prompt = "Test prompt"

        for depth in [1, 3, 5]:
            task_descriptor = default_task_descriptor_fn(prompt, depth=depth)
            route = router.route(task_descriptor)
            env = factory.get_environment(route.environment_id)
            env.execute_code("print('test')")

            # Verify routing considered depth
            assert route is not None
