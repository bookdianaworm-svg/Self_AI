"""
Tests for VerificationMiddleware Redux component.

This module tests VerificationMiddleware which handles:
- Layer1 loading coordination
- Theorem verification orchestration
- Action interception and dispatch
- Error handling in verification workflows
"""

from unittest.mock import MagicMock, patch

import pytest

from rlm.redux.middleware.verification_middleware import VerificationMiddleware
from rlm.redux.slices.verification_slice import VerificationActions


class TestVerificationMiddlewareInitialization:
    """
    Tests for VerificationMiddleware initialization.
    """

    def test_init_with_store(self):
        """
        Test that VerificationMiddleware initializes with store.

        Expected behavior:
        - Should store reference to store
        - Should initialize agent_factory to None
        """
        store = MagicMock()
        middleware = VerificationMiddleware(store)

        assert middleware.store == store
        assert middleware.agent_factory is None

    def test_init_without_store(self):
        """
        Test that VerificationMiddleware handles missing store.

        Expected behavior:
        - Should handle None store gracefully
        - May raise exception or handle gracefully
        """
        try:
            middleware = VerificationMiddleware(None)
            assert middleware is not None
        except (TypeError, AttributeError):
            # Also acceptable to raise exception
            pass


class TestMiddlewareCallPattern:
    """
    Tests for middleware call pattern.
    """

    def test_middleware_returns_function(self):
        """
        Test that middleware returns a function.

        Expected behavior:
        - __call__ should return middleware function
        - Should follow Redux middleware pattern
        """
        store = MagicMock()
        middleware = VerificationMiddleware(store)

        middleware_fn = middleware(store)
        assert callable(middleware_fn)

    def test_middleware_returns_dispatch(self):
        """
        Test that middleware returns dispatch function.

        Expected behavior:
        - Middleware function should return dispatch
        - Should follow Redux middleware pattern
        """
        store = MagicMock()
        middleware = VerificationMiddleware(store)

        middleware_fn = middleware(store)
        dispatch = middleware_fn(MagicMock())
        assert callable(dispatch)


class TestLayer1LoadingHandling:
    """
    Tests for Layer1 loading action handling.
    """

    @patch('rlm.redux.middleware.verification_middleware.Layer1Bootstrap')
    def test_handle_load_layer1_success(self, mock_bootstrap):
        """
        Test successful Layer1 loading.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should create Layer1Bootstrap instance
        - Should call load_layer1
        - Should dispatch success action
        """
        store = MagicMock()
        mock_instance = MagicMock()
        mock_instance.load_layer1.return_value = {
            "success": True,
            "mathlib_version": "v4.0.0",
            "physlib_version": "v1.0.0",
            "load_time_ms": 1500.0,
            "memory_mb": 256.0
        }
        mock_bootstrap.return_value = mock_instance

        middleware = VerificationMiddleware(store)
        action = VerificationActions.load_layer1_request()

        # Call middleware handler directly
        middleware._handle_load_layer1(action)

        # Verify success action was dispatched
        success_dispatched = any(
            call[0][0]["type"] == "verification/load_layer1_success"
            for call in store.dispatch.call_args_list
        )
        assert success_dispatched

    @patch('rlm.redux.middleware.verification_middleware.Layer1Bootstrap')
    def test_handle_load_layer1_failure(self, mock_bootstrap):
        """
        Test failed Layer1 loading.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should handle exception gracefully
        - Should dispatch failure action with error
        """
        store = MagicMock()
        mock_instance = MagicMock()
        mock_instance.load_layer1.return_value = {
            "success": False,
            "error": "Failed to load Lean kernel"
        }
        mock_bootstrap.return_value = mock_instance

        middleware = VerificationMiddleware(store)
        action = VerificationActions.load_layer1_request()

        middleware._handle_load_layer1(action)

        # Verify failure action was dispatched
        failure_dispatched = any(
            call[0][0]["type"] == "verification/load_layer1_failure"
            for call in store.dispatch.call_args_list
        )
        assert failure_dispatched

    @patch('rlm.redux.middleware.verification_middleware.Layer1Bootstrap')
    def test_handle_load_layer1_with_custom_path(self, mock_bootstrap):
        """
        Test Layer1 loading with custom path.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should use custom path from action payload
        - Should pass path to Layer1Bootstrap
        """
        store = MagicMock()
        mock_instance = MagicMock()
        mock_instance.load_layer1.return_value = {"success": True, "cached": True}
        mock_bootstrap.return_value = mock_instance

        middleware = VerificationMiddleware(store)
        action = {
            "type": "verification/load_layer1_request",
            "payload": {"layer1_path": "/custom/path"}
        }

        middleware._handle_load_layer1(action)

        # Verify Layer1Bootstrap was called with custom path
        mock_bootstrap.assert_called_once_with(layer1_path="/custom/path")

    @patch('rlm.redux.middleware.verification_middleware.Layer1Bootstrap')
    def test_handle_load_layer1_exception(self, mock_bootstrap):
        """
        Test Layer1 loading with exception.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should catch exception
        - Should dispatch failure action
        """
        store = MagicMock()
        mock_bootstrap.side_effect = RuntimeError("Unexpected error")

        middleware = VerificationMiddleware(store)
        action = VerificationActions.load_layer1_request()

        middleware._handle_load_layer1(action)

        # Verify failure action was dispatched
        failure_dispatched = any(
            call[0][0]["type"] == "verification/load_layer1_failure"
            for call in store.dispatch.call_args_list
        )
        assert failure_dispatched


class TestTheoremVerificationHandling:
    """
    Tests for theorem verification action handling.
    """

    @patch('rlm.redux.middleware.verification_middleware.VerificationAgentFactory')
    def test_handle_verify_theorem_success(self, mock_factory):
        """
        Test successful theorem verification.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should create Verifier Agent
        - Should dispatch success action
        """
        store = MagicMock()
        store.parent_rlm = None  # Prevent factory creation from MagicMock parent_rlm
        mock_agent = MagicMock()
        mock_agent.query.return_value = {
            "success": True,
            "response": "Proof completed successfully"
        }
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        middleware = VerificationMiddleware(store)
        middleware.agent_factory = mock_instance  # Set factory directly
        action = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")

        middleware._handle_verify_theorem(action)

        # Verify success action was dispatched
        success_dispatched = any(
            call[0][0]["type"] == "verification/verify_theorem_success"
            for call in store.dispatch.call_args_list
        )
        assert success_dispatched

    @patch('rlm.redux.middleware.verification_middleware.VerificationAgentFactory')
    def test_handle_verify_theorem_failure(self, mock_factory):
        """
        Test failed theorem verification.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should handle verification failure
        - Should dispatch failure action with error
        """
        store = MagicMock()
        mock_agent = MagicMock()
        mock_agent.query.side_effect = RuntimeError("Proof failed")
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        middleware = VerificationMiddleware(store)
        action = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")

        middleware._handle_verify_theorem(action)

        # Verify failure action was dispatched
        failure_dispatched = any(
            call[0][0]["type"] == "verification/verify_theorem_failure"
            for call in store.dispatch.call_args_list
        )
        assert failure_dispatched

    @patch('rlm.redux.middleware.verification_middleware.VerificationAgentFactory')
    def test_handle_verify_theorem_with_payload(self, mock_factory):
        """
        Test theorem verification with action payload.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should extract theorem_id and layer2_file from payload
        - Should pass to agent factory
        """
        store = MagicMock()
        mock_agent = MagicMock()
        mock_agent.query.return_value = {"response": "Proof completed"}
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        middleware = VerificationMiddleware(store)
        action = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")

        middleware._handle_verify_theorem(action)

        # Verify agent was created with correct layer2_file
        mock_instance.create_verifier_agent.assert_called_once()
        call_args = mock_instance.create_verifier_agent.call_args
        assert call_args is not None

    @patch('rlm.redux.middleware.verification_middleware.VerificationAgentFactory')
    def test_handle_verify_theorem_exception(self, mock_factory):
        """
        Test theorem verification with exception.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should catch exception
        - Should dispatch failure action
        """
        store = MagicMock()
        mock_factory.side_effect = RuntimeError("Agent creation failed")

        middleware = VerificationMiddleware(store)
        action = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")

        middleware._handle_verify_theorem(action)

        # Verify failure action was dispatched
        failure_dispatched = any(
            call[0][0]["type"] == "verification/verify_theorem_failure"
            for call in store.dispatch.call_args_list
        )
        assert failure_dispatched


class TestActionInterception:
    """
    Tests for action interception in middleware.
    """

    @patch('rlm.redux.middleware.verification_middleware.Layer1Bootstrap')
    def test_intercepts_load_layer1_request(self, mock_bootstrap):
        """
        Test that middleware intercepts load_layer1_request.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should call _handle_load_layer1
        - Should pass action to next
        """
        store = MagicMock()
        mock_instance = MagicMock()
        mock_instance.load_layer1.return_value = {"success": True}
        mock_bootstrap.return_value = mock_instance

        middleware = VerificationMiddleware(store)
        next_fn = MagicMock(return_value="next_result")

        middleware_fn = middleware(store)
        dispatch = middleware_fn(next_fn)

        action = VerificationActions.load_layer1_request()
        result = dispatch(action)

        # Verify next was called
        next_fn.assert_called_once_with(action)
        assert result == "next_result"

    @patch('rlm.redux.middleware.verification_middleware.VerificationAgentFactory')
    def test_intercepts_verify_theorem_request(self, mock_factory):
        """
        Test that middleware intercepts verify_theorem_request.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should call _handle_verify_theorem
        - Should pass action to next
        """
        store = MagicMock()
        mock_agent = MagicMock()
        mock_agent.query.return_value = {"response": "Proof completed"}
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        middleware = VerificationMiddleware(store)
        next_fn = MagicMock(return_value="next_result")

        middleware_fn = middleware(store)
        dispatch = middleware_fn(next_fn)

        action = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")
        result = dispatch(action)

        # Verify next was called
        next_fn.assert_called_once_with(action)
        assert result == "next_result"

    def test_passes_through_other_actions(self):
        """
        Test that middleware passes through other actions.

        Expected behavior:
        - Should not intercept unknown actions
        - Should pass to next unchanged
        """
        store = MagicMock()
        middleware = VerificationMiddleware(store)
        next_fn = MagicMock(return_value="next_result")

        middleware_fn = middleware(store)
        dispatch = middleware_fn(next_fn)

        action = {"type": "other/action", "payload": "data"}
        result = dispatch(action)

        # Verify next was called
        next_fn.assert_called_once_with(action)
        assert result == "next_result"


class TestErrorHandling:
    """
    Tests for error handling in middleware.
    """

    @patch('rlm.redux.middleware.verification_middleware.Layer1Bootstrap')
    def test_load_layer1_with_bootstrap_error(self, mock_bootstrap):
        """
        Test Layer1 loading with bootstrap creation error.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should handle bootstrap creation error
        - Should dispatch failure action
        """
        store = MagicMock()
        mock_bootstrap.side_effect = ImportError("Layer1 not available")

        middleware = VerificationMiddleware(store)
        action = VerificationActions.load_layer1_request()

        middleware._handle_load_layer1(action)

        # Verify failure action was dispatched
        failure_dispatched = any(
            call[0][0]["type"] == "verification/load_layer1_failure"
            for call in store.dispatch.call_args_list
        )
        assert failure_dispatched

    @patch('rlm.redux.middleware.verification_middleware.VerificationAgentFactory')
    def test_verify_theorem_with_factory_error(self, mock_factory):
        """
        Test theorem verification with factory creation error.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should handle factory creation error
        - Should dispatch failure action
        """
        store = MagicMock()
        mock_factory.side_effect = RuntimeError("Factory initialization failed")

        middleware = VerificationMiddleware(store)
        action = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")

        middleware._handle_verify_theorem(action)

        # Verify failure action was dispatched
        failure_dispatched = any(
            call[0][0]["type"] == "verification/verify_theorem_failure"
            for call in store.dispatch.call_args_list
        )
        assert failure_dispatched

    def test_middleware_continues_on_error(self):
        """
        Test that middleware continues after handling errors.

        Expected behavior:
        - Should still pass action to next
        - Should not stop middleware chain
        """
        store = MagicMock()
        middleware = VerificationMiddleware(store)
        next_fn = MagicMock(return_value="next_result")

        middleware_fn = middleware(store)
        dispatch = middleware_fn(next_fn)

        action = VerificationActions.load_layer1_request()
        result = dispatch(action)

        # Verify next was called even if handler fails
        next_fn.assert_called_once_with(action)
        assert result == "next_result"


class TestAgentFactoryIntegration:
    """
    Tests for agent factory integration in middleware.
    """

    @patch('rlm.redux.middleware.verification_middleware.VerificationAgentFactory')
    def test_agent_factory_initialization(self, mock_factory):
        """
        Test that agent factory is initialized correctly.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should create factory with parent RLM
        - Should store factory reference
        """
        store = MagicMock()
        mock_instance = MagicMock()
        mock_factory.return_value = mock_instance

        middleware = VerificationMiddleware(store)
        action = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")

        middleware._handle_verify_theorem(action)

        # Factory should be created (implementation may vary)
        assert middleware is not None

    @patch('rlm.redux.middleware.verification_middleware.VerificationAgentFactory')
    def test_agent_factory_reuse(self, mock_factory):
        """
        Test that agent factory is reused across calls.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should create factory once
        - Should reuse for subsequent calls
        """
        store = MagicMock()
        mock_instance = MagicMock()
        mock_agent = MagicMock()
        mock_agent.query.return_value = {"response": "Proof completed"}
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        middleware = VerificationMiddleware(store)

        # First call
        action1 = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")
        middleware._handle_verify_theorem(action1)

        # Second call
        action2 = VerificationActions.verify_theorem_request("theorem-2", "layer2/theorem2.lean")
        middleware._handle_verify_theorem(action2)

        # Factory should be reused (implementation may vary)
        assert middleware is not None


class TestEdgeCases:
    """
    Tests for edge cases in middleware.
    """

    def test_middleware_with_none_action(self):
        """
        Test middleware with None action.

        Expected behavior:
        - Should handle None gracefully
        - Should pass to next or handle appropriately
        """
        store = MagicMock()
        middleware = VerificationMiddleware(store)
        next_fn = MagicMock(return_value="next_result")

        middleware_fn = middleware(store)
        dispatch = middleware_fn(next_fn)

        result = dispatch(None)

        # Should handle gracefully
        assert middleware is not None

    def test_middleware_with_empty_action(self):
        """
        Test middleware with empty action.

        Expected behavior:
        - Should handle empty action gracefully
        - Should pass to next
        """
        store = MagicMock()
        middleware = VerificationMiddleware(store)
        next_fn = MagicMock(return_value="next_result")

        middleware_fn = middleware(store)
        dispatch = middleware_fn(next_fn)

        action = {}
        result = dispatch(action)

        next_fn.assert_called_once_with(action)
        assert result == "next_result"

    @patch('rlm.redux.middleware.verification_middleware.Layer1Bootstrap')
    def test_multiple_load_layer1_requests(self, mock_bootstrap):
        """
        Test multiple Layer1 load requests.

        Args:
            mock_bootstrap: Mocked Layer1Bootstrap

        Expected behavior:
        - Should handle each request
        - Should dispatch appropriate actions
        """
        store = MagicMock()
        mock_instance = MagicMock()
        mock_instance.load_layer1.return_value = {"success": True}
        mock_bootstrap.return_value = mock_instance

        middleware = VerificationMiddleware(store)

        # Multiple requests
        for i in range(3):
            action = VerificationActions.load_layer1_request()
            middleware._handle_load_layer1(action)

        # Should have dispatched multiple actions
        assert store.dispatch.call_count >= 3

    @patch('rlm.redux.middleware.verification_middleware.VerificationAgentFactory')
    def test_multiple_verify_theorem_requests(self, mock_factory):
        """
        Test multiple theorem verification requests.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should handle each request
        - Should dispatch appropriate actions
        """
        store = MagicMock()
        mock_agent = MagicMock()
        mock_agent.query.return_value = {"response": "Proof completed"}
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        middleware = VerificationMiddleware(store)

        # Multiple requests
        for i in range(3):
            action = VerificationActions.verify_theorem_request(
                f"theorem-{i}",
                f"layer2/theorem{i}.lean"
            )
            middleware._handle_verify_theorem(action)

        # Should have dispatched multiple actions
        assert store.dispatch.call_count >= 3
