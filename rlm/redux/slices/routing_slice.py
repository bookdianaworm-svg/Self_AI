"""
Redux slice for routing state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RoutingDecisionType(Enum):
    BACKEND = "backend"
    ENVIRONMENT = "environment"


@dataclass
class RoutingDecision:
    """Record of a routing decision."""
    decision_id: str
    decision_type: RoutingDecisionType
    subtask_id: str
    selected: str
    rule_name: str
    overrides: List[str]
    reasoning: str
    timestamp: float


@dataclass
class BackendMetrics:
    """Metrics for a backend."""
    backend_id: str
    total_calls: int
    successful_calls: int
    total_cost: float
    avg_latency_ms: float
    lean_pass_rate: float


@dataclass
class RoutingState:
    """Redux slice for routing state."""
    decisions: Dict[str, RoutingDecision] = field(default_factory=dict)
    backend_metrics: Dict[str, BackendMetrics] = field(default_factory=dict)
    environment_metrics: Dict[str, BackendMetrics] = field(default_factory=dict)
    active_routing: Optional[str] = None

    def __post_init__(self):
        if self.decisions is None:
            self.decisions = {}
        if self.backend_metrics is None:
            self.backend_metrics = {}
        if self.environment_metrics is None:
            self.environment_metrics = {}


# Routing actions
class RoutingActions:
    @staticmethod
    def routing_decision_made(decision: RoutingDecision):
        return {
            "type": "routing/decision_made",
            "payload": decision
        }

    @staticmethod
    def routing_started(subtask_id: str):
        return {
            "type": "routing/started",
            "payload": {"subtask_id": subtask_id}
        }

    @staticmethod
    def routing_completed(subtask_id: str, result: dict):
        return {
            "type": "routing/completed",
            "payload": {"subtask_id": subtask_id, "result": result}
        }

    @staticmethod
    def backend_metrics_updated(backend_id: str, metrics: dict):
        return {
            "type": "routing/backend_metrics_updated",
            "payload": {"backend_id": backend_id, "metrics": metrics}
        }


# Routing reducer
def routing_reducer(state: RoutingState, action: dict) -> RoutingState:
    action_type = action.get("type")

    if action_type == "routing/decision_made":
        decision = action.get("payload")
        if decision is not None:
            new_decisions = state.decisions.copy()
            new_decisions[decision.decision_id] = decision
        else:
            new_decisions = state.decisions
        return RoutingState(
            decisions=new_decisions,
            backend_metrics=state.backend_metrics,
            environment_metrics=state.environment_metrics,
            active_routing=None
        )

    elif action_type == "routing/started":
        return RoutingState(
            decisions=state.decisions,
            backend_metrics=state.backend_metrics,
            environment_metrics=state.environment_metrics,
            active_routing=action.get("payload", {}).get("subtask_id")
        )

    elif action_type == "routing/completed":
        # Update metrics based on result
        payload = action.get("payload", {})
        subtask_id = payload.get("subtask_id")
        result = payload.get("result", {})

        # Always clear active_routing on completion
        new_backend_metrics = state.backend_metrics.copy()
        new_environment_metrics = state.environment_metrics.copy()

        # Find the routing decision for this subtask
        decision = None
        for dec in state.decisions.values():
            if dec.subtask_id == subtask_id:
                decision = dec
                break

        if decision and decision.decision_type == RoutingDecisionType.BACKEND:
            backend_id = decision.selected
            if backend_id not in new_backend_metrics:
                new_backend_metrics[backend_id] = BackendMetrics(
                    backend_id=backend_id,
                    total_calls=0,
                    successful_calls=0,
                    total_cost=0.0,
                    avg_latency_ms=0.0,
                    lean_pass_rate=0.0
                )

            # Update metrics
            metrics = new_backend_metrics[backend_id]
            metrics.total_calls += 1
            if result.get("success"):
                metrics.successful_calls += 1
            metrics.total_cost += result.get("cost", 0)
            metrics.avg_latency_ms = (
                (metrics.avg_latency_ms * (metrics.total_calls - 1) + result.get("latency_ms", 0))
                / metrics.total_calls
            )
            metrics.lean_pass_rate = (
                (metrics.lean_pass_rate * (metrics.total_calls - 1) + result.get("lean_passed", 0))
                / metrics.total_calls
            )

        return RoutingState(
            decisions=state.decisions,
            backend_metrics=new_backend_metrics,
            environment_metrics=new_environment_metrics,
            active_routing=None
        )

    elif action_type == "routing/backend_metrics_updated":
        payload = action.get("payload", {})
        metrics_data = payload.get("metrics")
        
        # Handle both BackendMetrics objects and dicts
        if hasattr(metrics_data, 'backend_id'):
            # It's a BackendMetrics object
            backend_id = metrics_data.backend_id
            new_backend_metrics = state.backend_metrics.copy()
            new_backend_metrics[backend_id] = metrics_data
        elif isinstance(metrics_data, dict):
            # It's a dict
            new_backend_id: Any = metrics_data.get("backend_id")
            if new_backend_id:
                new_backend_metrics = state.backend_metrics.copy()
                new_backend_metrics[new_backend_id] = BackendMetrics(
                    backend_id=new_backend_id,
                    total_calls=metrics_data.get("total_calls", 0),
                    successful_calls=metrics_data.get("successful_calls", 0),
                    total_cost=metrics_data.get("total_cost", 0.0),
                    avg_latency_ms=metrics_data.get("avg_latency_ms", 0.0),
                    lean_pass_rate=metrics_data.get("lean_pass_rate", 0.0)
                )
            else:
                new_backend_metrics = state.backend_metrics.copy()
        else:
            new_backend_metrics = state.backend_metrics.copy()

        return RoutingState(
            decisions=state.decisions,
            backend_metrics=new_backend_metrics,
            environment_metrics=state.environment_metrics,
            active_routing=state.active_routing
        )

    return state
