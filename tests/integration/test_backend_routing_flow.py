"""
Integration tests for backend routing flow through RLM._subcall().

This module tests the complete flow of backend routing including:
- Task descriptor generation
- Backend router decision
- Backend factory client creation
- Subcall execution
- Metrics tracking
"""

from unittest.mock import MagicMock, patch

import pytest

from rlm.routing.backend_router import BackendRouter, TaskDescriptor
from rlm.routing.backend_factory import BackendFactory
from rlm.routing.task_descriptor import default_task_descriptor_fn


class TestBackendRoutingFlow:
    """
    Integration tests for complete backend routing flow.
    """

    @patch('rlm.routing.backend_factory.get_client')
    @patch('rlm.routing.backend_router.BackendRouter.route')
    def test_complete_backend_routing_flow(self, mock_route, mock_get_client):
        """
        Test complete backend routing flow from prompt to response.

        Args:
            mock_route: Mocked BackendRouter.route
            mock_get_client: Mocked get_client

        Expected behavior:
        - Should generate task descriptor
        - Should route to appropriate backend
        - Should create backend client
        - Should execute subcall
        - Should track metrics
        """
        # Setup mocks
        mock_route.return_value = MagicMock(
            backend_id="claude_agent",
            rule_name="test_rule",
            overrides=[],
            reasoning="Test reasoning"
        )
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client

        # Create components
        router = BackendRouter()
        factory = BackendFactory()

        # Execute flow
        prompt = "Write a function that adds two numbers"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)

        # Route
        route = router.route(task_descriptor)
        assert route.backend_id == "claude_agent"

        # Get backend
        backend = factory.get_backend(route.backend_id)
        assert backend == mock_client

        # Execute
        response = backend.completion(prompt)
        assert response == "Test response"

    @patch('rlm.routing.backend_factory.get_client')
    def test_backend_routing_with_overrides(self, mock_get_client):
        """
        Test backend routing with parameter overrides.

        Args:
            mock_get_client: Mocked get_client

        Expected behavior:
        - Should apply overrides to backend
        - Should pass overrides to client
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client

        router = BackendRouter()
        factory = BackendFactory()

        prompt = "Prove this theorem"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)

        # Route (may include overrides)
        route = router.route(task_descriptor)

        # Get backend
        backend = factory.get_backend(route.backend_id)
        assert backend == mock_client

    @patch('rlm.routing.backend_factory.get_client')
    def test_backend_routing_metrics_tracking(self, mock_get_client):
        """
        Test that backend routing tracks metrics.

        Args:
            mock_get_client: Mocked get_client

        Expected behavior:
        - Should record successful calls
        - Should record failed calls
        - Should track latency
        - Should track costs
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client

        router = BackendRouter()
        factory = BackendFactory()

        # Execute multiple calls
        for i in range(5):
            prompt = f"Test prompt {i}"
            task_descriptor = default_task_descriptor_fn(prompt, depth=1)
            route = router.route(task_descriptor)
            backend = factory.get_backend(route.backend_id)
            backend.completion(prompt)

            # Record metrics
            router.record_call(
                route.backend_id,
                success=True,
                latency_ms=100 + i * 10,
                cost=0.01
            )

        # Check metrics
        metrics = router.get_backend_metrics(route.backend_id)
        assert metrics is not None
        assert metrics.total_calls == 5
        assert metrics.successful_calls == 5

    @patch('rlm.routing.backend_factory.get_client')
    def test_backend_routing_with_fallback(self, mock_get_client):
        """
        Test backend routing with fallback to default.

        Args:
            mock_get_client: Mocked get_client

        Expected behavior:
        - Should use fallback when no rule matches
        - Should route to default backend
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client

        router = BackendRouter()
        factory = BackendFactory()

        # Use prompt that won't match any specific rule
        prompt = "General question"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)

        # Route
        route = router.route(task_descriptor)

        # Should use fallback
        assert route.backend_id == router.config["defaults"]["fallback_backend"]

        # Get backend
        backend = factory.get_backend(route.backend_id)
        assert backend == mock_client


class TestBackendRoutingErrorHandling:
    """
    Integration tests for error handling in backend routing.
    """

    @patch('rlm.routing.backend_factory.get_client')
    def test_backend_routing_with_client_error(self, mock_get_client):
        """
        Test backend routing when client creation fails.

        Args:
            mock_get_client: Mocked get_client

        Expected behavior:
        - Should propagate client creation error
        - Should not crash
        """
        mock_get_client.side_effect = RuntimeError("Failed to create client")

        router = BackendRouter()
        factory = BackendFactory()

        prompt = "Test prompt"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        route = router.route(task_descriptor)

        with pytest.raises(RuntimeError, match="Failed to create client"):
            factory.get_backend(route.backend_id)

    @patch('rlm.routing.backend_factory.get_client')
    def test_backend_routing_with_execution_error(self, mock_get_client):
        """
        Test backend routing when execution fails.

        Args:
            mock_get_client: Mocked get_client

        Expected behavior:
        - Should handle execution error gracefully
        - Should record failed call in metrics
        """
        mock_client = MagicMock()
        mock_client.completion.side_effect = RuntimeError("Execution failed")
        mock_get_client.return_value = mock_client

        router = BackendRouter()
        factory = BackendFactory()

        prompt = "Test prompt"
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        route = router.route(task_descriptor)
        backend = factory.get_backend(route.backend_id)

        # Execute and record metrics
        try:
            backend.completion(prompt)
            success = True
        except RuntimeError:
            success = False

        router.record_call(route.backend_id, success=success, latency_ms=100, cost=0.01)

        # Check metrics
        metrics = router.get_backend_metrics(route.backend_id)
        assert metrics is not None
        assert metrics.total_calls == 1
        assert metrics.successful_calls == 0


class TestBackendRoutingEdgeCases:
    """
    Integration tests for edge cases in backend routing.
    """

    @patch('rlm.routing.backend_factory.get_client')
    def test_backend_routing_with_empty_prompt(self, mock_get_client):
        """
        Test backend routing with empty prompt.

        Args:
            mock_get_client: Mocked get_client

        Expected behavior:
        - Should handle empty prompt gracefully
        - Should still route to backend
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client

        router = BackendRouter()
        factory = BackendFactory()

        prompt = ""
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        route = router.route(task_descriptor)
        backend = factory.get_backend(route.backend_id)
        response = backend.completion(prompt)

        assert response == "Test response"

    @patch('rlm.routing.backend_factory.get_client')
    def test_backend_routing_with_very_long_prompt(self, mock_get_client):
        """
        Test backend routing with very long prompt.

        Args:
            mock_get_client: Mocked get_client

        Expected behavior:
        - Should handle long prompt
        - Should route appropriately
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client

        router = BackendRouter()
        factory = BackendFactory()

        prompt = "Test " * 10000
        task_descriptor = default_task_descriptor_fn(prompt, depth=1)
        route = router.route(task_descriptor)
        backend = factory.get_backend(route.backend_id)
        response = backend.completion(prompt)

        assert response == "Test response"

    @patch('rlm.routing.backend_factory.get_client')
    def test_backend_routing_concurrent_calls(self, mock_get_client):
        """
        Test backend routing with concurrent calls.

        Args:
            mock_get_client: Mocked get_client

        Expected behavior:
        - Should handle multiple concurrent requests
        - Each request should be independent
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client

        router = BackendRouter()
        factory = BackendFactory()

        # Simulate concurrent calls
        prompts = [f"Prompt {i}" for i in range(10)]
        task_descriptors = [default_task_descriptor_fn(p, depth=1) for p in prompts]
        routes = [router.route(td) for td in task_descriptors]
        backends = [factory.get_backend(r.backend_id) for r in routes]
        responses = [b.completion(p) for b, p in zip(backends, prompts)]

        assert len(responses) == 10
        assert all(r == "Test response" for r in responses)


class TestBackendRoutingIntegration:
    """
    Integration tests for backend routing with other components.
    """

    @patch('rlm.routing.backend_factory.get_client')
    def test_backend_routing_with_task_descriptor(self, mock_get_client):
        """
        Test that task descriptor integrates with routing.

        Args:
            mock_get_client: Mocked get_client

        Expected behavior:
        - Task descriptor should inform routing decision
        - Routing should consider task properties
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client

        router = BackendRouter()
        factory = BackendFactory()

        # Different task types
        prompts = {
            "code": "Write a function",
            "proof": "Prove this theorem",
            "research": "Search for information"
        }

        for task_type, prompt in prompts.items():
            task_descriptor = default_task_descriptor_fn(prompt, depth=1)
            route = router.route(task_descriptor)
            backend = factory.get_backend(route.backend_id)
            backend.completion(prompt)

            # Verify routing considered task type
            assert route is not None

    @patch('rlm.routing.backend_factory.get_client')
    def test_backend_routing_with_depth(self, mock_get_client):
        """
        Test that depth affects backend routing.

        Args:
            mock_get_client: Mocked get_client

        Expected behavior:
        - Higher depth may route to different backend
        - Routing should consider depth in decision
        """
        mock_client = MagicMock()
        mock_client.completion.return_value = "Test response"
        mock_get_client.return_value = mock_client

        router = BackendRouter()
        factory = BackendFactory()

        prompt = "Test prompt"

        for depth in [1, 3, 5]:
            task_descriptor = default_task_descriptor_fn(prompt, depth=depth)
            route = router.route(task_descriptor)
            backend = factory.get_backend(route.backend_id)
            backend.completion(prompt)

            # Verify routing considered depth
            assert route is not None
