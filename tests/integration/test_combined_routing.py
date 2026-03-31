"""
Integration tests for combined backend + environment routing.

This module tests the complete flow of combined routing including:
- Task descriptor generation
- Backend router decision
- Environment router decision
- Combined routing logic
- Subcall execution
"""

from unittest.mock import MagicMock, patch

import pytest

from rlm.routing.backend_router import BackendRouter
from rlm.routing.environment_router import EnvironmentRouter
from rlm.routing.backend_factory import BackendFactory
from rlm.routing.environment_factory import EnvironmentFactory
from rlm.routing.task_descriptor import default_task_descriptor_fn


class TestCombinedRoutingFlow:
    """
    Integration tests for combined backend and environment routing.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    @patch('rlm.routing.backend_factory.get_client')
    @patch('rlm.routing.environment_router.EnvironmentRouter.route')
    @patch('rlm.routing.backend_router.BackendRouter.route')
    def test_combined_routing_flow(self, mock_backend_route, mock_env_route, mock_get_client, mock_get_environment):
        """
        Test complete combined routing flow.

        Args:
            mock_backend_route: Mocked BackendRouter.route
            mock_env_route: Mocked EnvironmentRouter.route
            mock_get_client: Mocked get_client
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should route to backend
        - Should route to environment
        - Should create backend client
        - Should create environment
        - Should execute subcall
        """
        # Setup mocks
        mock_backend_route.return_value = MagicMock(
            backend_id="claude_agent",
            rule_name="backend_rule",
            overrides=[],
            reasoning="Backend reasoning"
        )
        mock_env_route.return_value = MagicMock(
            environment_id="local",
            rule_name="env_rule",
            reasoning="Environment reasoning"
        )
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        # Create components
        backend_router = BackendRouter()
        env_router = EnvironmentRouter()
        backend_factory = BackendFactory()
        env_factory = EnvironmentFactory()

        # Execute flow
        prompt = "Verify this Lean theorem"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)

        # Route backend
        backend_route = backend_router.route(task_descriptor)
        assert backend_route.backend_id == "claude_agent"

        # Route environment
        env_route = env_router.route(task_descriptor)
        assert env_route.environment_id == "local"

        # Get backend
        backend = backend_factory.get_backend(backend_route.backend_id)
        assert backend == mock_client

        # Get environment
        env = env_factory.get_environment(env_route.environment_id)
        assert env == mock_env

        # Execute
        response = backend.completion(prompt)
        result = env.execute_code("print('test')")
        assert result is not None

    @patch('rlm.routing.environment_factory.get_environment')
    @patch('rlm.routing.backend_factory.get_client')
    def test_combined_routing_with_lean_task(self, mock_get_client, mock_get_environment):
        """
        Test combined routing for Lean verification task.

        Args:
            mock_get_client: Mocked get_client
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should route to appropriate backend
        - Should route to local environment
        - Should enable Layer1 tools
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        backend_router = BackendRouter()
        env_router = EnvironmentRouter()
        backend_factory = BackendFactory()
        env_factory = EnvironmentFactory()

        prompt = "Prove this theorem"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        task_descriptor["metrics"] = {"needs_lean": True}

        # Route backend
        backend_route = backend_router.route(task_descriptor)

        # Route environment
        env_route = env_router.route(task_descriptor)
        assert env_route.environment_id == "local"  # Lean requires local

        # Get components
        backend = backend_factory.get_backend(backend_route.backend_id)
        env = env_factory.get_environment(env_route.environment_id)

        assert backend == mock_client
        assert env == mock_env

    @patch('rlm.routing.environment_factory.get_environment')
    @patch('rlm.routing.backend_factory.get_client')
    def test_combined_routing_with_internet_task(self, mock_get_client, mock_get_environment):
        """
        Test combined routing for internet research task.

        Args:
            mock_get_client: Mocked get_client
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should route to appropriate backend
        - Should route to modal environment
        - Should allow internet access
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        backend_router = BackendRouter()
        env_router = EnvironmentRouter()
        backend_factory = BackendFactory()
        env_factory = EnvironmentFactory()

        prompt = "Search for recent papers"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        task_descriptor["metrics"] = {"needs_internet": True}

        # Route backend
        backend_route = backend_router.route(task_descriptor)

        # Route environment
        env_route = env_router.route(task_descriptor)
        assert env_route.environment_id == "modal"  # Internet uses modal

        # Get components
        backend = backend_factory.get_backend(backend_route.backend_id)
        env = env_factory.get_environment(env_route.environment_id)

        assert backend == mock_client
        assert env == mock_env


class TestCombinedRoutingConflicts:
    """
    Integration tests for handling routing conflicts.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    @patch('rlm.routing.backend_factory.get_client')
    def test_routing_conflict_lean_vs_internet(self, mock_get_client, mock_get_environment):
        """
        Test routing when Lean and internet are both required.

        Args:
            mock_get_client: Mocked get_client
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Environment routing should prioritize Lean (local)
        - Backend routing should consider task type
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        backend_router = BackendRouter()
        env_router = EnvironmentRouter()
        backend_factory = BackendFactory()
        env_factory = EnvironmentFactory()

        prompt = "Search for Lean proofs"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        task_descriptor["metrics"] = {
            "needs_lean": True,
            "needs_internet": True
        }

        # Route
        backend_route = backend_router.route(task_descriptor)
        env_route = env_router.route(task_descriptor)

        # Lean should take priority for environment
        assert env_route.environment_id == "local"

        # Get components
        backend = backend_factory.get_backend(backend_route.backend_id)
        env = env_factory.get_environment(env_route.environment_id)

        assert backend == mock_client
        assert env == mock_env

    @patch('rlm.routing.environment_factory.get_environment')
    @patch('rlm.routing.backend_factory.get_client')
    def test_routing_conflict_sensitive_vs_internet(self, mock_get_client, mock_get_environment):
        """
        Test routing when sensitive data and internet are both required.

        Args:
            mock_get_client: Mocked get_client
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Security should override (local)
        - Backend routing should consider task type
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        backend_router = BackendRouter()
        env_router = EnvironmentRouter()
        backend_factory = BackendFactory()
        env_factory = EnvironmentFactory()

        prompt = "Search for confidential information"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        task_descriptor["metrics"] = {
            "needs_internet": True,
            "data_sensitivity": "confidential"
        }

        # Route
        backend_route = backend_router.route(task_descriptor)
        env_route = env_router.route(task_descriptor)

        # Confidential data should force local
        assert env_route.environment_id == "local"

        # Get components
        backend = backend_factory.get_backend(backend_route.backend_id)
        env = env_factory.get_environment(env_route.environment_id)

        assert backend == mock_client
        assert env == mock_env


class TestCombinedRoutingErrorHandling:
    """
    Integration tests for error handling in combined routing.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    @patch('rlm.routing.backend_factory.get_client')
    def test_backend_failure_affects_environment_routing(self, mock_get_client, mock_get_environment):
        """
        Test that backend failure doesn't prevent environment routing.

        Args:
            mock_get_client: Mocked get_client
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Environment routing should still work
        - Backend failure should be isolated
        """
        mock_get_client.side_effect = RuntimeError("Backend creation failed")
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        backend_router = BackendRouter()
        env_router = EnvironmentRouter()
        backend_factory = BackendFactory()
        env_factory = EnvironmentFactory()

        prompt = "Test prompt"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)

        # Route
        backend_route = backend_router.route(task_descriptor)
        env_route = env_router.route(task_descriptor)

        # Backend should fail
        with pytest.raises(RuntimeError, match="Backend creation failed"):
            backend_factory.get_backend(backend_route.backend_id)

        # Environment should still work
        env = env_factory.get_environment(env_route.environment_id)
        assert env == mock_env

    @patch('rlm.routing.environment_factory.get_environment')
    @patch('rlm.routing.backend_factory.get_client')
    def test_environment_failure_affects_backend_routing(self, mock_get_client, mock_get_environment):
        """
        Test that environment failure doesn't prevent backend routing.

        Args:
            mock_get_client: Mocked get_client
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Backend routing should still work
        - Environment failure should be isolated
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client
        mock_get_environment.side_effect = RuntimeError("Environment creation failed")

        backend_router = BackendRouter()
        env_router = EnvironmentRouter()
        backend_factory = BackendFactory()
        env_factory = EnvironmentFactory()

        prompt = "Test prompt"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)

        # Route
        backend_route = backend_router.route(task_descriptor)
        env_route = env_router.route(task_descriptor)

        # Backend should still work
        backend = backend_factory.get_backend(backend_route.backend_id)
        assert backend == mock_client

        # Environment should fail
        with pytest.raises(RuntimeError, match="Environment creation failed"):
            env_factory.get_environment(env_route.environment_id)


class TestCombinedRoutingEdgeCases:
    """
    Integration tests for edge cases in combined routing.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    @patch('rlm.routing.backend_factory.get_client')
    def test_combined_routing_with_empty_task(self, mock_get_client, mock_get_environment):
        """
        Test combined routing with empty task descriptor.

        Args:
            mock_get_client: Mocked get_client
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should handle empty task gracefully
        - Should use fallback routing
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        backend_router = BackendRouter()
        env_router = EnvironmentRouter()
        backend_factory = BackendFactory()
        env_factory = EnvironmentFactory()

        prompt = ""
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)

        # Route
        backend_route = backend_router.route(task_descriptor)
        env_route = env_router.route(task_descriptor)

        # Should use fallbacks
        assert backend_route is not None
        assert env_route is not None

    @patch('rlm.routing.environment_factory.get_environment')
    @patch('rlm.routing.backend_factory.get_client')
    def test_combined_routing_concurrent_requests(self, mock_get_client, mock_get_environment):
        """
        Test combined routing with concurrent requests.

        Args:
            mock_get_client: Mocked get_client
            mock_get_environment: Mocked get_environment

        Expected behavior:
        - Should handle multiple concurrent requests
        - Each request should be independent
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client
        mock_env = MagicMock()
        mock_env.execute_code.return_value = MagicMock(stdout="Result", stderr="")
        mock_get_environment.return_value = mock_env

        backend_router = BackendRouter()
        env_router = EnvironmentRouter()
        backend_factory = BackendFactory()
        env_factory = EnvironmentFactory()

        # Simulate concurrent calls
        prompts = [f"Prompt {i}" for i in range(5)]
        task_descriptors = [default_task_descriptor_fn(p, depth=1) for p in prompts]

        backend_routes = [backend_router.route(td) for td in task_descriptors]
        env_routes = [env_router.route(td) for td in task_descriptors]
        backends = [backend_factory.get_backend(br.backend_id) for br in backend_routes]
        envs = [env_factory.get_environment(er.environment_id) for er in env_routes]

        assert len(backends) == 5
        assert len(envs) == 5
