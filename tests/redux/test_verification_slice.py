"""
Tests for VerificationSlice Redux component.

This module tests verification slice state management which handles:
- Layer1 state (loading status, versions, metrics)
- Theorem verification tracking
- Verification queue management
- Active verification state
"""

import pytest
from unittest.mock import MagicMock

from rlm.redux.slices.verification_slice import (
    VerificationState,
    VerificationStatus,
    Layer1State,
    TheoremVerification,
    VerificationActions,
    verification_reducer
)


class TestVerificationStatus:
    """
    Tests for VerificationStatus enum.
    """

    def test_verification_status_values(self):
        """
        Test VerificationStatus enum values.

        Expected behavior:
        - Should have PENDING value
        - Should have LOADING value
        - Should have LOADED value
        - Should have FAILED value
        - Should have VERIFYING value
        - Should have PASSED value
        - Should have FAILED_VERIFICATION value
        """
        assert VerificationStatus.PENDING.value == "pending"
        assert VerificationStatus.LOADING.value == "loading"
        assert VerificationStatus.LOADED.value == "loaded"
        assert VerificationStatus.FAILED.value == "failed"
        assert VerificationStatus.VERIFYING.value == "verifying"
        assert VerificationStatus.PASSED.value == "passed"
        assert VerificationStatus.FAILED_VERIFICATION.value == "failed_verification"


class TestLayer1State:
    """
    Tests for Layer1State dataclass.
    """

    def test_layer1_state_initialization(self):
        """
        Test Layer1State initialization with defaults.

        Expected behavior:
        - Should initialize with PENDING status
        - Should set all optional fields to None
        """
        state = Layer1State()
        assert state.status == VerificationStatus.PENDING
        assert state.mathlib_version is None
        assert state.physlib_version is None
        assert state.load_time_ms is None
        assert state.memory_mb is None
        assert state.error is None

    def test_layer1_state_with_values(self):
        """
        Test Layer1State initialization with values.

        Expected behavior:
        - Should store all provided values
        - Should maintain all fields
        """
        state = Layer1State(
            status=VerificationStatus.LOADED,
            mathlib_version="v4.0.0",
            physlib_version="v1.0.0",
            load_time_ms=1500.0,
            memory_mb=256.0,
            error=None
        )

        assert state.status == VerificationStatus.LOADED
        assert state.mathlib_version == "v4.0.0"
        assert state.physlib_version == "v1.0.0"
        assert state.load_time_ms == 1500.0
        assert state.memory_mb == 256.0
        assert state.error is None

    def test_layer1_state_with_error(self):
        """
        Test Layer1State with error information.

        Expected behavior:
        - Should store error message
        - Should set status to FAILED
        """
        state = Layer1State(
            status=VerificationStatus.FAILED,
            error="Failed to load Lean kernel"
        )

        assert state.status == VerificationStatus.FAILED
        assert state.error == "Failed to load Lean kernel"


class TestTheoremVerification:
    """
    Tests for TheoremVerification dataclass.
    """

    def test_theorem_verification_initialization(self):
        """
        Test TheoremVerification initialization with defaults.

        Expected behavior:
        - Should initialize with PENDING status
        - Should set proof_attempts to 0
        - Should set optional fields to None
        """
        theorem = TheoremVerification(
            theorem_id="theorem-1"
        )

        assert theorem.theorem_id == "theorem-1"
        assert theorem.status == VerificationStatus.PENDING
        assert theorem.layer2_file is None
        assert theorem.proof_attempts == 0
        assert theorem.last_error is None
        assert theorem.proof is None

    def test_theorem_verification_with_values(self):
        """
        Test TheoremVerification initialization with values.

        Expected behavior:
        - Should store all provided values
        - Should maintain all fields
        """
        theorem = TheoremVerification(
            theorem_id="theorem-1",
            status=VerificationStatus.PASSED,
            layer2_file="layer2/theorem1.lean",
            proof_attempts=3,
            last_error=None,
            proof="Proof completed using induction"
        )

        assert theorem.theorem_id == "theorem-1"
        assert theorem.status == VerificationStatus.PASSED
        assert theorem.layer2_file == "layer2/theorem1.lean"
        assert theorem.proof_attempts == 3
        assert theorem.last_error is None
        assert theorem.proof == "Proof completed using induction"

    def test_theorem_verification_with_error(self):
        """
        Test TheoremVerification with error information.

        Expected behavior:
        - Should store error message
        - Should set status to FAILED_VERIFICATION
        """
        theorem = TheoremVerification(
            theorem_id="theorem-1",
            status=VerificationStatus.FAILED_VERIFICATION,
            proof_attempts=5,
            last_error="Proof failed at step 3"
        )

        assert theorem.status == VerificationStatus.FAILED_VERIFICATION
        assert theorem.last_error == "Proof failed at step 3"
        assert theorem.proof_attempts == 5


class TestVerificationState:
    """
    Tests for VerificationState dataclass.
    """

    def test_verification_state_initialization(self):
        """
        Test VerificationState initialization with defaults.

        Expected behavior:
        - Should initialize with default Layer1State
        - Should initialize empty theorems dict
        - Should initialize empty verification_queue
        - Should set active_verification to None
        """
        state = VerificationState()

        assert state.layer1.status == VerificationStatus.PENDING
        assert state.theorems == {}
        assert state.verification_queue == []
        assert state.active_verification is None

    def test_verification_state_with_values(self):
        """
        Test VerificationState initialization with values.

        Expected behavior:
        - Should store all provided values
        - Should maintain all fields
        """
        layer1 = Layer1State(
            status=VerificationStatus.LOADED,
            mathlib_version="v4.0.0",
            physlib_version="v1.0.0"
        )
        theorems = {
            "theorem-1": TheoremVerification(
                theorem_id="theorem-1",
                status=VerificationStatus.PASSED
            )
        }

        state = VerificationState(
            layer1=layer1,
            theorems=theorems,
            active_verification="theorem-2",
            verification_queue=["theorem-3", "theorem-4"]
        )

        assert state.layer1.status == VerificationStatus.LOADED
        assert "theorem-1" in state.theorems
        assert state.active_verification == "theorem-2"
        assert len(state.verification_queue) == 2


class TestVerificationActions:
    """
    Tests for VerificationActions action creators.
    """

    def test_load_layer1_request_action(self):
        """
        Test creating load_layer1_request action.

        Expected behavior:
        - Should create action with correct type
        - Should have no payload or empty payload
        """
        action = VerificationActions.load_layer1_request()
        assert action["type"] == "verification/load_layer1_request"

    def test_load_layer1_success_action(self):
        """
        Test creating load_layer1_success action.

        Expected behavior:
        - Should create action with correct type
        - Should include data in payload
        """
        data = {
            "mathlib_version": "v4.0.0",
            "physlib_version": "v1.0.0",
            "load_time_ms": 1500.0,
            "memory_mb": 256.0
        }
        action = VerificationActions.load_layer1_success(data)

        assert action["type"] == "verification/load_layer1_success"
        assert action["payload"] == data

    def test_load_layer1_failure_action(self):
        """
        Test creating load_layer1_failure action.

        Expected behavior:
        - Should create action with correct type
        - Should include error in payload
        """
        error = "Failed to load Lean kernel"
        action = VerificationActions.load_layer1_failure(error)

        assert action["type"] == "verification/load_layer1_failure"
        assert action["payload"] == error

    def test_verify_theorem_request_action(self):
        """
        Test creating verify_theorem_request action.

        Expected behavior:
        - Should create action with correct type
        - Should include theorem_id and layer2_file in payload
        """
        action = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")

        assert action["type"] == "verification/verify_theorem_request"
        assert action["payload"]["theorem_id"] == "theorem-1"
        assert action["payload"]["layer2_file"] == "layer2/theorem1.lean"

    def test_verify_theorem_success_action(self):
        """
        Test creating verify_theorem_success action.

        Expected behavior:
        - Should create action with correct type
        - Should include theorem_id and proof in payload
        """
        proof = "Proof completed using induction"
        action = VerificationActions.verify_theorem_success("theorem-1", proof)

        assert action["type"] == "verification/verify_theorem_success"
        assert action["payload"]["theorem_id"] == "theorem-1"
        assert action["payload"]["proof"] == proof

    def test_verify_theorem_failure_action(self):
        """
        Test creating verify_theorem_failure action.

        Expected behavior:
        - Should create action with correct type
        - Should include theorem_id and error in payload
        """
        error = "Proof failed at step 3"
        action = VerificationActions.verify_theorem_failure("theorem-1", error)

        assert action["type"] == "verification/verify_theorem_failure"
        assert action["payload"]["theorem_id"] == "theorem-1"
        assert action["payload"]["error"] == error


class TestVerificationReducer:
    """
    Tests for verification_reducer function.
    """

    def test_reducer_initial_state(self):
        """
        Test reducer with initial state.

        Expected behavior:
        - Should return initial state for unknown action
        - Should handle empty state
        """
        state = VerificationState()
        action = {"type": "unknown/action"}

        new_state = verification_reducer(state, action)

        assert new_state == state

    def test_reducer_load_layer1_request(self):
        """
        Test reducer with load_layer1_request action.

        Expected behavior:
        - Should set layer1 status to LOADING
        - Should preserve other state
        """
        state = VerificationState()
        action = VerificationActions.load_layer1_request()

        new_state = verification_reducer(state, action)

        assert new_state.layer1.status == VerificationStatus.LOADING
        assert new_state.theorems == state.theorems

    def test_reducer_load_layer1_success(self):
        """
        Test reducer with load_layer1_success action.

        Expected behavior:
        - Should update layer1 status to LOADED
        - Should set version and metrics
        - Should preserve other state
        """
        state = VerificationState(
            layer1=Layer1State(status=VerificationStatus.LOADING)
        )

        data = {
            "mathlib_version": "v4.0.0",
            "physlib_version": "v1.0.0",
            "load_time_ms": 1500.0,
            "memory_mb": 256.0
        }
        action = VerificationActions.load_layer1_success(data)

        new_state = verification_reducer(state, action)

        assert new_state.layer1.status == VerificationStatus.LOADED
        assert new_state.layer1.mathlib_version == "v4.0.0"
        assert new_state.layer1.physlib_version == "v1.0.0"
        assert new_state.layer1.load_time_ms == 1500.0
        assert new_state.layer1.memory_mb == 256.0

    def test_reducer_load_layer1_failure(self):
        """
        Test reducer with load_layer1_failure action.

        Expected behavior:
        - Should set layer1 status to FAILED
        - Should store error message
        - Should preserve other state
        """
        state = VerificationState(
            layer1=Layer1State(status=VerificationStatus.LOADING)
        )

        error = "Failed to load Lean kernel"
        action = VerificationActions.load_layer1_failure(error)

        new_state = verification_reducer(state, action)

        assert new_state.layer1.status == VerificationStatus.FAILED
        assert new_state.layer1.error == error

    def test_reducer_verify_theorem_request(self):
        """
        Test reducer with verify_theorem_request action.

        Expected behavior:
        - Should create new theorem entry
        - Should set status to PENDING
        - Should add to verification_queue
        - Should set active_verification
        """
        state = VerificationState()

        action = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")

        new_state = verification_reducer(state, action)

        assert "theorem-1" in new_state.theorems
        assert new_state.theorems["theorem-1"].status == VerificationStatus.PENDING
        assert new_state.theorems["theorem-1"].layer2_file == "layer2/theorem1.lean"
        assert new_state.active_verification == "theorem-1"

    def test_reducer_verify_theorem_success(self):
        """
        Test reducer with verify_theorem_success action.

        Expected behavior:
        - Should update theorem status to PASSED
        - Should store proof
        - Should clear active_verification
        """
        state = VerificationState(
            theorems={
                "theorem-1": TheoremVerification(
                    theorem_id="theorem-1",
                    status=VerificationStatus.VERIFYING,
                    proof_attempts=2
                )
            },
            active_verification="theorem-1"
        )

        proof = "Proof completed using induction"
        action = VerificationActions.verify_theorem_success("theorem-1", proof)

        new_state = verification_reducer(state, action)

        assert new_state.theorems["theorem-1"].status == VerificationStatus.PASSED
        assert new_state.theorems["theorem-1"].proof == proof
        assert new_state.active_verification is None

    def test_reducer_verify_theorem_failure(self):
        """
        Test reducer with verify_theorem_failure action.

        Expected behavior:
        - Should update theorem status to FAILED_VERIFICATION
        - Should store error
        - Should clear active_verification
        """
        state = VerificationState(
            theorems={
                "theorem-1": TheoremVerification(
                    theorem_id="theorem-1",
                    status=VerificationStatus.VERIFYING,
                    proof_attempts=2
                )
            },
            active_verification="theorem-1"
        )

        error = "Proof failed at step 3"
        action = VerificationActions.verify_theorem_failure("theorem-1", error)

        new_state = verification_reducer(state, action)

        assert new_state.theorems["theorem-1"].status == VerificationStatus.FAILED_VERIFICATION
        assert new_state.theorems["theorem-1"].last_error == error
        assert new_state.active_verification is None

    def test_reducer_unknown_action(self):
        """
        Test reducer with unknown action type.

        Expected behavior:
        - Should return state unchanged
        - Should not modify any fields
        """
        state = VerificationState(
            layer1=Layer1State(status=VerificationStatus.LOADED),
            theorems={"theorem-1": MagicMock()},
            active_verification="theorem-1",
            verification_queue=["theorem-2"]
        )
        action = {"type": "unknown/action"}

        new_state = verification_reducer(state, action)

        assert new_state.layer1 == state.layer1
        assert new_state.theorems == state.theorems
        assert new_state.active_verification == state.active_verification
        assert new_state.verification_queue == state.verification_queue


class TestStateTransitions:
    """
    Tests for state transitions through multiple actions.
    """

    def test_layer1_loading_flow(self):
        """
        Test state transitions through Layer1 loading flow.

        Expected behavior:
        - State should update correctly through each action
        - Final state should reflect successful load
        """
        state = VerificationState()

        # Request load
        action1 = VerificationActions.load_layer1_request()
        state = verification_reducer(state, action1)
        assert state.layer1.status == VerificationStatus.LOADING

        # Success
        data = {
            "mathlib_version": "v4.0.0",
            "physlib_version": "v1.0.0",
            "load_time_ms": 1500.0,
            "memory_mb": 256.0
        }
        action2 = VerificationActions.load_layer1_success(data)
        state = verification_reducer(state, action2)
        assert state.layer1.status == VerificationStatus.LOADED
        assert state.layer1.mathlib_version == "v4.0.0"

    def test_theorem_verification_flow(self):
        """
        Test state transitions through theorem verification flow.

        Expected behavior:
        - State should update correctly through each action
        - Final state should reflect verification result
        """
        state = VerificationState()

        # Request verification
        action1 = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")
        state = verification_reducer(state, action1)
        assert state.theorems["theorem-1"].status == VerificationStatus.PENDING
        assert state.active_verification == "theorem-1"

        # Success
        proof = "Proof completed"
        action2 = VerificationActions.verify_theorem_success("theorem-1", proof)
        state = verification_reducer(state, action2)
        assert state.theorems["theorem-1"].status == VerificationStatus.PASSED
        assert state.theorems["theorem-1"].proof == proof
        assert state.active_verification is None

    def test_multiple_theorem_verifications(self):
        """
        Test state with multiple theorem verifications.

        Expected behavior:
        - Should store all theorems
        - Each theorem should be tracked independently
        """
        state = VerificationState()

        for i in range(3):
            action = VerificationActions.verify_theorem_request(
                f"theorem-{i}",
                f"layer2/theorem{i}.lean"
            )
            state = verification_reducer(state, action)

        assert len(state.theorems) == 3
        for i in range(3):
            assert f"theorem-{i}" in state.theorems

    def test_layer1_failure_then_retry(self):
        """
        Test state transitions through Layer1 failure and retry.

        Expected behavior:
        - Should handle failure state
        - Should allow retry
        """
        state = VerificationState()

        # Request load
        action1 = VerificationActions.load_layer1_request()
        state = verification_reducer(state, action1)

        # Failure
        error = "Failed to load"
        action2 = VerificationActions.load_layer1_failure(error)
        state = verification_reducer(state, action2)
        assert state.layer1.status == VerificationStatus.FAILED
        assert state.layer1.error == error

        # Retry
        action3 = VerificationActions.load_layer1_request()
        state = verification_reducer(state, action3)
        assert state.layer1.status == VerificationStatus.LOADING


class TestEdgeCases:
    """
    Tests for edge cases in verification state management.
    """

    def test_verify_theorem_without_layer1_loaded(self):
        """
        Test theorem verification when Layer1 is not loaded.

        Expected behavior:
        - Should still create theorem entry
        - May fail verification due to missing Layer1
        """
        state = VerificationState(
            layer1=Layer1State(status=VerificationStatus.PENDING)
        )

        action = VerificationActions.verify_theorem_request("theorem-1", "layer2/theorem1.lean")
        new_state = verification_reducer(state, action)

        assert "theorem-1" in new_state.theorems

    def test_verify_theorem_with_duplicate_id(self):
        """
        Test verifying theorem with duplicate ID.

        Expected behavior:
        - Should update existing theorem
        - Should not create duplicate
        """
        state = VerificationState(
            theorems={
                "theorem-1": TheoremVerification(
                    theorem_id="theorem-1",
                    status=VerificationStatus.PENDING
                )
            }
        )

        action = VerificationActions.verify_theorem_success("theorem-1", "New proof")
        new_state = verification_reducer(state, action)

        # Should still have only one theorem
        assert len(new_state.theorems) == 1
        assert new_state.theorems["theorem-1"].proof == "New proof"
