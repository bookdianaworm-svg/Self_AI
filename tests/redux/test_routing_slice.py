"""
Tests for RoutingSlice Redux component.

This module tests routing slice state management which handles:
- Routing state updates
- Backend metrics tracking
- Routing decisions
- Active routing state
"""

import pytest
from unittest.mock import MagicMock

from rlm.redux.slices.routing_slice import (
    RoutingState,
    RoutingDecision,
    BackendMetrics,
    RoutingDecisionType,
    RoutingActions,
    routing_reducer
)


class TestRoutingState:
    """
    Tests for RoutingState dataclass.
    """

    def test_routing_state_initialization(self):
        """
        Test RoutingState initialization with defaults.

        Expected behavior:
        - Should initialize with empty collections
        - Should set active_routing to None
        """
        state = RoutingState()
        assert state.decisions == {}
        assert state.backend_metrics == {}
        assert state.environment_metrics == {}
        assert state.active_routing is None

    def test_routing_state_with_values(self):
        """
        Test RoutingState initialization with values.

        Expected behavior:
        - Should store provided values
        - Should maintain all fields
        """
        decision = RoutingDecision(
            decision_id="decision-1",
            decision_type=RoutingDecisionType.BACKEND,
            subtask_id="task-1",
            selected="backend1",
            rule_name="test_rule",
            overrides=[],
            reasoning="Test reasoning",
            timestamp=1234567890.0
        )
        metrics = BackendMetrics(
            backend_id="backend1",
            total_calls=10,
            successful_calls=9,
            total_cost=0.15,
            avg_latency_ms=250.0,
            lean_pass_rate=0.8
        )

        state = RoutingState(
            decisions={"decision-1": decision},
            backend_metrics={"backend1": metrics},
            environment_metrics={},
            active_routing="task-2"
        )

        assert "decision-1" in state.decisions
        assert state.decisions["decision-1"].decision_id == "decision-1"
        assert "backend1" in state.backend_metrics
        assert state.backend_metrics["backend1"].total_calls == 10
        assert state.active_routing == "task-2"

    def test_routing_state_post_init(self):
        """
        Test RoutingState __post_init__ method.

        Expected behavior:
        - Should initialize None collections to empty dicts
        - Should handle None values gracefully
        """
        state = RoutingState(
            decisions=None,
            backend_metrics=None,
            environment_metrics=None
        )
        assert state.decisions == {}
        assert state.backend_metrics == {}
        assert state.environment_metrics == {}


class TestRoutingDecision:
    """
    Tests for RoutingDecision dataclass.
    """

    def test_routing_decision_creation(self):
        """
        Test creating a RoutingDecision instance.

        Expected behavior:
        - Should create valid instance with all fields
        - Should store all provided values
        """
        decision = RoutingDecision(
            decision_id="decision-1",
            decision_type=RoutingDecisionType.BACKEND,
            subtask_id="task-1",
            selected="backend1",
            rule_name="test_rule",
            overrides=["temp: 0.1"],
            reasoning="Test reasoning",
            timestamp=1234567890.0
        )

        assert decision.decision_id == "decision-1"
        assert decision.decision_type == RoutingDecisionType.BACKEND
        assert decision.subtask_id == "task-1"
        assert decision.selected == "backend1"
        assert decision.rule_name == "test_rule"
        assert decision.overrides == ["temp: 0.1"]
        assert decision.reasoning == "Test reasoning"
        assert decision.timestamp == 1234567890.0

    def test_routing_decision_type_enum(self):
        """
        Test RoutingDecisionType enum values.

        Expected behavior:
        - Should have BACKEND value
        - Should have ENVIRONMENT value
        """
        assert RoutingDecisionType.BACKEND.value == "backend"
        assert RoutingDecisionType.ENVIRONMENT.value == "environment"


class TestBackendMetrics:
    """
    Tests for BackendMetrics dataclass.
    """

    def test_backend_metrics_creation(self):
        """
        Test creating a BackendMetrics instance.

        Expected behavior:
        - Should create valid instance with all fields
        - Should store all provided values
        """
        metrics = BackendMetrics(
            backend_id="backend1",
            total_calls=100,
            successful_calls=95,
            total_cost=1.5,
            avg_latency_ms=200.0,
            lean_pass_rate=0.85
        )

        assert metrics.backend_id == "backend1"
        assert metrics.total_calls == 100
        assert metrics.successful_calls == 95
        assert metrics.total_cost == 1.5
        assert metrics.avg_latency_ms == 200.0
        assert metrics.lean_pass_rate == 0.85

    def test_backend_metrics_calculations(self):
        """
        Test that metrics can be calculated from raw data.

        Expected behavior:
        - Total cost should sum individual costs
        - Average latency should be calculated correctly
        - Pass rate should be calculated correctly
        """
        # Simulate calculating metrics from raw data
        total_calls = 10
        successful_calls = 8
        latencies = [100, 150, 200, 250, 300, 100, 150, 200, 250, 300]
        costs = [0.01, 0.015, 0.02, 0.025, 0.03, 0.01, 0.015, 0.02, 0.025, 0.03]

        avg_latency = sum(latencies) / len(latencies)
        total_cost = sum(costs)
        pass_rate = successful_calls / total_calls

        assert avg_latency == 200.0
        assert total_cost == 0.2
        assert pass_rate == 0.8


class TestRoutingActions:
    """
    Tests for RoutingActions action creators.
    """

    def test_routing_decision_made_action(self):
        """
        Test creating routing_decision_made action.

        Expected behavior:
        - Should create action with correct type
        - Should include decision in payload
        """
        decision = RoutingDecision(
            decision_id="decision-1",
            decision_type=RoutingDecisionType.BACKEND,
            subtask_id="task-1",
            selected="backend1",
            rule_name="test_rule",
            overrides=[],
            reasoning="Test",
            timestamp=1234567890.0
        )

        action = RoutingActions.routing_decision_made(decision)

        assert action["type"] == "routing/decision_made"
        assert action["payload"] == decision

    def test_routing_started_action(self):
        """
        Test creating routing_started action.

        Expected behavior:
        - Should create action with correct type
        - Should include subtask_id in payload
        """
        action = RoutingActions.routing_started("task-1")

        assert action["type"] == "routing/started"
        assert action["payload"]["subtask_id"] == "task-1"

    def test_routing_completed_action(self):
        """
        Test creating routing_completed action.

        Expected behavior:
        - Should create action with correct type
        - Should include subtask_id and result in payload
        """
        result = {"backend": "backend1", "status": "success"}
        action = RoutingActions.routing_completed("task-1", result)

        assert action["type"] == "routing/completed"
        assert action["payload"]["subtask_id"] == "task-1"
        assert action["payload"]["result"] == result

    def test_backend_metrics_updated_action(self):
        """
        Test creating backend_metrics_updated action.

        Expected behavior:
        - Should create action with correct type
        - Should include backend_id and metrics in payload
        """
        metrics = {"total_calls": 10, "successful_calls": 9}
        action = RoutingActions.backend_metrics_updated("backend1", metrics)

        assert action["type"] == "routing/backend_metrics_updated"
        assert action["payload"]["backend_id"] == "backend1"
        assert action["payload"]["metrics"] == metrics


class TestRoutingReducer:
    """
    Tests for routing_reducer function.
    """

    def test_reducer_initial_state(self):
        """
        Test reducer with initial state.

        Expected behavior:
        - Should return initial state for unknown action
        - Should handle empty state
        """
        state = RoutingState()
        action = {"type": "unknown/action"}

        new_state = routing_reducer(state, action)

        assert new_state == state

    def test_reducer_routing_decision_made(self):
        """
        Test reducer with routing_decision_made action.

        Expected behavior:
        - Should add decision to decisions dict
        - Should clear active_routing
        - Should preserve other state
        """
        state = RoutingState(
            decisions={},
            backend_metrics={},
            environment_metrics={},
            active_routing="task-1"
        )

        decision = RoutingDecision(
            decision_id="decision-1",
            decision_type=RoutingDecisionType.BACKEND,
            subtask_id="task-1",
            selected="backend1",
            rule_name="test_rule",
            overrides=[],
            reasoning="Test",
            timestamp=1234567890.0
        )
        action = RoutingActions.routing_decision_made(decision)

        new_state = routing_reducer(state, action)

        assert "decision-1" in new_state.decisions
        assert new_state.decisions["decision-1"] == decision
        assert new_state.active_routing is None
        assert new_state.backend_metrics == state.backend_metrics

    def test_reducer_routing_started(self):
        """
        Test reducer with routing_started action.

        Expected behavior:
        - Should set active_routing to subtask_id
        - Should preserve other state
        """
        state = RoutingState(
            decisions={},
            backend_metrics={},
            environment_metrics={},
            active_routing=None
        )
        action = RoutingActions.routing_started("task-1")

        new_state = routing_reducer(state, action)

        assert new_state.active_routing == "task-1"
        assert new_state.decisions == state.decisions

    def test_reducer_routing_completed(self):
        """
        Test reducer with routing_completed action.

        Expected behavior:
        - Should clear active_routing
        - Should preserve other state
        """
        state = RoutingState(
            decisions={},
            backend_metrics={},
            environment_metrics={},
            active_routing="task-1"
        )
        action = RoutingActions.routing_completed("task-1", {"status": "success"})

        new_state = routing_reducer(state, action)

        assert new_state.active_routing is None
        assert new_state.decisions == state.decisions

    def test_reducer_backend_metrics_updated(self):
        """
        Test reducer with backend_metrics_updated action.

        Expected behavior:
        - Should update backend metrics
        - Should preserve other state
        """
        state = RoutingState(
            decisions={},
            backend_metrics={
                "backend1": BackendMetrics(
                    backend_id="backend1",
                    total_calls=5,
                    successful_calls=4,
                    total_cost=0.1,
                    avg_latency_ms=200.0,
                    lean_pass_rate=0.8
                )
            },
            environment_metrics={},
            active_routing=None
        )

        new_metrics = BackendMetrics(
            backend_id="backend1",
            total_calls=10,
            successful_calls=9,
            total_cost=0.2,
            avg_latency_ms=190.0,
            lean_pass_rate=0.85
        )
        action = RoutingActions.backend_metrics_updated("backend1", new_metrics)

        new_state = routing_reducer(state, action)

        assert "backend1" in new_state.backend_metrics
        assert new_state.backend_metrics["backend1"].total_calls == 10
        assert new_state.backend_metrics["backend1"].successful_calls == 9

    def test_reducer_unknown_action(self):
        """
        Test reducer with unknown action type.

        Expected behavior:
        - Should return state unchanged
        - Should not modify any fields
        """
        state = RoutingState(
            decisions={"decision-1": MagicMock()},
            backend_metrics={"backend1": MagicMock()},
            environment_metrics={"local": MagicMock()},
            active_routing="task-1"
        )
        action = {"type": "unknown/action"}

        new_state = routing_reducer(state, action)

        assert new_state.decisions == state.decisions
        assert new_state.backend_metrics == state.backend_metrics
        assert new_state.environment_metrics == state.environment_metrics
        assert new_state.active_routing == state.active_routing

    def test_reducer_immutability(self):
        """
        Test that reducer doesn't mutate original state.

        Expected behavior:
        - Should return new state object
        - Should not modify original state
        """
        state = RoutingState(
            decisions={},
            backend_metrics={},
            environment_metrics={},
            active_routing=None
        )

        decision = RoutingDecision(
            decision_id="decision-1",
            decision_type=RoutingDecisionType.BACKEND,
            subtask_id="task-1",
            selected="backend1",
            rule_name="test_rule",
            overrides=[],
            reasoning="Test",
            timestamp=1234567890.0
        )
        action = RoutingActions.routing_decision_made(decision)

        new_state = routing_reducer(state, action)

        # Original state should be unchanged
        assert len(state.decisions) == 0
        assert len(new_state.decisions) == 1


class TestStateTransitions:
    """
    Tests for state transitions through multiple actions.
    """

    def test_routing_flow_state_transitions(self):
        """
        Test state transitions through a complete routing flow.

        Expected behavior:
        - State should update correctly through each action
        - Final state should reflect all operations
        """
        state = RoutingState()

        # Start routing
        action1 = RoutingActions.routing_started("task-1")
        state = routing_reducer(state, action1)
        assert state.active_routing == "task-1"

        # Make decision
        decision = RoutingDecision(
            decision_id="decision-1",
            decision_type=RoutingDecisionType.BACKEND,
            subtask_id="task-1",
            selected="backend1",
            rule_name="test_rule",
            overrides=[],
            reasoning="Test",
            timestamp=1234567890.0
        )
        action2 = RoutingActions.routing_decision_made(decision)
        state = routing_reducer(state, action2)
        assert "decision-1" in state.decisions
        assert state.active_routing is None

        # Complete routing
        action3 = RoutingActions.routing_completed("task-1", {"status": "success"})
        state = routing_reducer(state, action3)
        assert state.active_routing is None

    def test_multiple_routing_decisions(self):
        """
        Test state with multiple routing decisions.

        Expected behavior:
        - Should store all decisions
        - Each decision should be accessible
        """
        state = RoutingState()

        for i in range(5):
            decision = RoutingDecision(
                decision_id=f"decision-{i}",
                decision_type=RoutingDecisionType.BACKEND,
                subtask_id=f"task-{i}",
                selected="backend1",
                rule_name="test_rule",
                overrides=[],
                reasoning="Test",
                timestamp=1234567890.0 + i
            )
            action = RoutingActions.routing_decision_made(decision)
            state = routing_reducer(state, action)

        assert len(state.decisions) == 5
        for i in range(5):
            assert f"decision-{i}" in state.decisions
