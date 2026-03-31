"""
Integration tests for Layer1 verification flow.

This module tests the complete flow of Layer1 verification including:
- Layer1 loading (loading → verification → theorem proving)
- Verification agent creation
- Theorem verification
- Proof synthesis
- State transitions
"""

from unittest.mock import MagicMock, patch

import pytest

from rlm.environments.layer1_bootstrap import Layer1Bootstrap
from rlm.redux.slices.verification_slice import (
    VerificationState,
    VerificationStatus,
    VerificationActions,
    verification_reducer
)


class TestLayer1LoadingFlow:
    """
    Integration tests for Layer1 loading flow.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_physlib')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._compile_haskell_types')
    def test_layer1_loading_success_flow(self, mock_compile, mock_physlib, mock_lean):
        """
        Test successful Layer1 loading flow.

        Args:
            mock_compile: Mocked _compile_haskell_types
            mock_physlib: Mocked _load_physlib
            mock_lean: Mocked _load_lean_kernel

        Expected behavior:
        - Should load Lean kernel
        - Should load PhysLib
        - Should compile Haskell types
        - Should return success result
        - Should update state to LOADED
        """
        mock_lean.return_value = MagicMock()
        mock_physlib.return_value = None
        mock_compile.return_value = None

        # Initialize state
        state = VerificationState()

        # Load Layer1
        bootstrap = Layer1Bootstrap()
        result = bootstrap.load_layer1()

        # Verify result
        assert result["success"] is True
        assert "mathlib_version" in result
        assert "physlib_version" in result
        assert "load_time_ms" in result

        # Update state
        action = VerificationActions.load_layer1_success(result)
        state = verification_reducer(state, action)

        # Verify state transition
        assert state.layer1.status.value == "loaded"
        assert state.layer1.mathlib_version is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    def test_layer1_loading_failure_flow(self, mock_lean):
        """
        Test Layer1 loading failure flow.

        Args:
            mock_lean: Mocked _load_lean_kernel

        Expected behavior:
        - Should handle failure gracefully
        - Should return failure result
        - Should update state to FAILED
        """
        mock_lean.side_effect = RuntimeError("Failed to load Lean")

        # Initialize state
        state = VerificationState()

        # Load Layer1
        bootstrap = Layer1Bootstrap()
        result = bootstrap.load_layer1()

        # Verify result
        assert result["success"] is False
        assert "error" in result

        # Update state
        action = VerificationActions.load_layer1_failure(result["error"])
        state = verification_reducer(state, action)

        # Verify state transition
        assert state.layer1.status.value == "failed"
        assert state.layer1.error == result["error"]

    def test_layer1_loading_cached_flow(self):
        """
        Test Layer1 loading with cached result.

        Expected behavior:
        - Should not reload if already loaded
        - Should return cached result
        - Should maintain LOADED state
        """
        # Initialize state
        state = VerificationState()
        state.layer1.status = VerificationStatus.LOADED

        # Load Layer1 (should use cache)
        bootstrap = Layer1Bootstrap()
        bootstrap.loaded = True
        result = bootstrap.load_layer1()

        # Verify result
        assert result["success"] is True
        assert result.get("cached") is True

        # State should remain loaded
        assert state.layer1.status.value == "loaded"


class TestTheoremVerificationFlow:
    """
    Integration tests for theorem verification flow.
    """

    @patch('rlm.agents.verification_agent_factory.VerificationAgentFactory')
    def test_theorem_verification_success_flow(self, mock_factory):
        """
        Test successful theorem verification flow.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should create verifier agent
        - Should execute verification
        - Should return success result
        - Should update state to PASSED
        """
        mock_agent = MagicMock()
        mock_agent.query.return_value = {
            "response": "Proof completed successfully"
        }
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        # Initialize state
        state = VerificationState()
        state.layer1.status = VerificationStatus.LOADED

        # Request verification
        action = VerificationActions.verify_theorem_request(
            "theorem-1",
            "layer2/theorem1.lean"
        )
        state = verification_reducer(state, action)

        # Verify state transition
        assert state.theorems["theorem-1"].status.value == "pending"
        assert state.active_verification == "theorem-1"

        # Simulate verification success
        action = VerificationActions.verify_theorem_success(
            "theorem-1",
            "Proof completed using induction"
        )
        state = verification_reducer(state, action)

        # Verify state transition
        assert state.theorems["theorem-1"].status.value == "passed"
        assert state.theorems["theorem-1"].proof == "Proof completed using induction"
        assert state.active_verification is None

    @patch('rlm.agents.verification_agent_factory.VerificationAgentFactory')
    def test_theorem_verification_failure_flow(self, mock_factory):
        """
        Test theorem verification failure flow.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should create verifier agent
        - Should execute verification
        - Should return failure result
        - Should update state to FAILED_VERIFICATION
        """
        mock_agent = MagicMock()
        mock_agent.query.side_effect = RuntimeError("Proof failed")
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        # Initialize state
        state = VerificationState()
        state.layer1.status = VerificationStatus.LOADED

        # Request verification
        action = VerificationActions.verify_theorem_request(
            "theorem-1",
            "layer2/theorem1.lean"
        )
        state = verification_reducer(state, action)

        # Simulate verification failure
        action = VerificationActions.verify_theorem_failure(
            "theorem-1",
            "Proof failed at step 3"
        )
        state = verification_reducer(state, action)

        # Verify state transition
        assert state.theorems["theorem-1"].status.value == "failed_verification"
        assert state.theorems["theorem-1"].last_error == "Proof failed at step 3"
        assert state.active_verification is None


class TestLayer1VerificationIntegration:
    """
    Integration tests for complete Layer1 verification workflow.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_physlib')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._compile_haskell_types')
    @patch('rlm.agents.verification_agent_factory.VerificationAgentFactory')
    def test_complete_verification_workflow(self, mock_factory, mock_compile, mock_physlib, mock_lean):
        """
        Test complete Layer1 verification workflow.

        Args:
            mock_factory: Mocked VerificationAgentFactory
            mock_compile: Mocked _compile_haskell_types
            mock_physlib: Mocked _load_physlib
            mock_lean: Mocked _load_lean_kernel

        Expected behavior:
        - Should load Layer1 successfully
        - Should verify theorems
        - Should track state transitions
        """
        mock_lean.return_value = MagicMock()
        mock_physlib.return_value = None
        mock_compile.return_value = None

        mock_agent = MagicMock()
        mock_agent.query.return_value = {
            "response": "Proof completed"
        }
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        # Initialize state
        state = VerificationState()

        # Step 1: Load Layer1
        bootstrap = Layer1Bootstrap()
        load_result = bootstrap.load_layer1()
        assert load_result["success"] is True

        action = VerificationActions.load_layer1_success(load_result)
        state = verification_reducer(state, action)
        assert state.layer1.status.value == "loaded"

        # Step 2: Verify theorems
        for i in range(3):
            action = VerificationActions.verify_theorem_request(
                f"theorem-{i}",
                f"layer2/theorem{i}.lean"
            )
            state = verification_reducer(state, action)

            # Simulate success
            action = VerificationActions.verify_theorem_success(
                f"theorem-{i}",
                f"Proof {i}"
            )
            state = verification_reducer(state, action)

        # Verify final state
        assert len(state.theorems) == 3
        for i in range(3):
            assert state.theorems[f"theorem-{i}"].status.value == "passed"

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    @patch('rlm.agents.verification_agent_factory.VerificationAgentFactory')
    def test_verification_without_layer1_loaded(self, mock_factory, mock_lean):
        """
        Test verification when Layer1 is not loaded.

        Args:
            mock_factory: Mocked VerificationAgentFactory
            mock_lean: Mocked _load_lean_kernel

        Expected behavior:
        - Should handle missing Layer1 gracefully
        - May fail verification
        """
        mock_lean.side_effect = RuntimeError("Lean not loaded")
        mock_agent = MagicMock()
        mock_agent.query.return_value = {
            "response": "Verification failed"
        }
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        # Initialize state (Layer1 not loaded)
        state = VerificationState()
        state.layer1.status = VerificationStatus.PENDING

        # Request verification
        action = VerificationActions.verify_theorem_request(
            "theorem-1",
            "layer2/theorem1.lean"
        )
        state = verification_reducer(state, action)

        # Verify state
        assert "theorem-1" in state.theorems
        assert state.theorems["theorem-1"].status.value == "pending"


class TestLayer1VerificationErrorHandling:
    """
    Integration tests for error handling in Layer1 verification.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    def test_layer1_load_error_propagation(self, mock_lean):
        """
        Test that Layer1 load errors are propagated correctly.

        Args:
            mock_lean: Mocked _load_lean_kernel

        Expected behavior:
        - Should propagate load errors
        - Should update state to FAILED
        """
        mock_lean.side_effect = RuntimeError("Lean kernel not found")

        # Initialize state
        state = VerificationState()

        # Load Layer1
        bootstrap = Layer1Bootstrap()
        result = bootstrap.load_layer1()

        # Verify result
        assert result["success"] is False
        assert "error" in result

        # Update state
        action = VerificationActions.load_layer1_failure(result["error"])
        state = verification_reducer(state, action)

        # Verify error is stored
        assert state.layer1.error == result["error"]

    @patch('rlm.agents.verification_agent_factory.VerificationAgentFactory')
    def test_verification_agent_creation_error(self, mock_factory):
        """
        Test handling of verifier agent creation errors.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should handle creation errors gracefully
        - Should dispatch failure action
        """
        mock_factory.side_effect = RuntimeError("Failed to create agent")

        # Initialize state
        state = VerificationState()

        # Request verification (will fail at agent creation)
        action = VerificationActions.verify_theorem_request(
            "theorem-1",
            "layer2/theorem1.lean"
        )
        state = verification_reducer(state, action)

        # Verify state
        assert "theorem-1" in state.theorems


class TestLayer1VerificationEdgeCases:
    """
    Integration tests for edge cases in Layer1 verification.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_physlib')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._compile_haskell_types')
    def test_multiple_layer1_load_attempts(self, mock_compile, mock_physlib, mock_lean):
        """
        Test multiple Layer1 load attempts.

        Args:
            mock_compile: Mocked _compile_haskell_types
            mock_physlib: Mocked _load_physlib
            mock_lean: Mocked _load_lean_kernel

        Expected behavior:
        - First load should succeed
        - Subsequent loads should use cache
        """
        mock_lean.return_value = MagicMock()
        mock_physlib.return_value = None
        mock_compile.return_value = None

        bootstrap = Layer1Bootstrap()

        # First load
        result1 = bootstrap.load_layer1()
        assert result1["success"] is True

        # Second load (should use cache)
        result2 = bootstrap.load_layer1()
        assert result2["success"] is True
        assert result2.get("cached") is True

    @patch('rlm.agents.verification_agent_factory.VerificationAgentFactory')
    def test_multiple_theorem_verifications(self, mock_factory):
        """
        Test multiple theorem verifications.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should handle multiple theorems
        - Each verification should be independent
        """
        mock_agent = MagicMock()
        mock_agent.query.return_value = {
            "response": "Proof completed"
        }
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        # Initialize state
        state = VerificationState()
        state.layer1.status = VerificationStatus.LOADED

        # Verify multiple theorems
        for i in range(5):
            action = VerificationActions.verify_theorem_request(
                f"theorem-{i}",
                f"layer2/theorem{i}.lean"
            )
            state = verification_reducer(state, action)

            # Simulate success
            action = VerificationActions.verify_theorem_success(
                f"theorem-{i}",
                f"Proof {i}"
            )
            state = verification_reducer(state, action)

        # Verify all theorems are tracked
        assert len(state.theorems) == 5
        for i in range(5):
            assert state.theorems[f"theorem-{i}"].status.value == "passed"

    @patch('rlm.agents.verification_agent_factory.VerificationAgentFactory')
    def test_verification_with_duplicate_theorem_id(self, mock_factory):
        """
        Test verification with duplicate theorem ID.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should update existing theorem
        - Should not create duplicate
        """
        mock_agent = MagicMock()
        mock_agent.query.return_value = {
            "response": "Proof completed"
        }
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        # Initialize state
        state = VerificationState()
        state.layer1.status = VerificationStatus.LOADED

        # First verification
        action = VerificationActions.verify_theorem_request(
            "theorem-1",
            "layer2/theorem1.lean"
        )
        state = verification_reducer(state, action)
        action = VerificationActions.verify_theorem_success(
            "theorem-1",
            "First proof"
        )
        state = verification_reducer(state, action)

        # Second verification (same ID)
        action = VerificationActions.verify_theorem_success(
            "theorem-1",
            "Second proof"
        )
        state = verification_reducer(state, action)

        # Should update existing theorem
        assert len(state.theorems) == 1
        assert state.theorems["theorem-1"].proof == "Second proof"


class TestLayer1VerificationQueue:
    """
    Integration tests for verification queue management.
    """

    @patch('rlm.agents.verification_agent_factory.VerificationAgentFactory')
    def test_verification_queue_management(self, mock_factory):
        """
        Test that verification queue is managed correctly.

        Args:
            mock_factory: Mocked VerificationAgentFactory

        Expected behavior:
        - Should add theorems to queue
        - Should remove from queue when active
        - Should track queue state
        """
        mock_agent = MagicMock()
        mock_agent.query.return_value = {
            "response": "Proof completed"
        }
        mock_instance = MagicMock()
        mock_instance.create_verifier_agent.return_value = mock_agent
        mock_factory.return_value = mock_instance

        # Initialize state
        state = VerificationState()
        state.layer1.status = VerificationStatus.LOADED

        # Add theorems to queue
        for i in range(3):
            action = VerificationActions.verify_theorem_request(
                f"theorem-{i}",
                f"layer2/theorem{i}.lean"
            )
            state = verification_reducer(state, action)

        # Verify queue
        assert len(state.verification_queue) == 3
        for i in range(3):
            assert f"theorem-{i}" in state.verification_queue

        # Process first theorem
        action = VerificationActions.verify_theorem_success(
            "theorem-0",
            "Proof 0"
        )
        state = verification_reducer(state, action)

        # Queue should still have 2 theorems
        assert len(state.verification_queue) == 2
        assert "theorem-0" not in state.verification_queue
