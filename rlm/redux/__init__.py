"""
Redux state management for RLM system.

This module provides Redux-style state management for tracking
system state including verification, routing, and other concerns.
"""

from rlm.redux.slices.verification_slice import (
    VerificationStatus,
    Layer1State,
    TheoremVerification,
    VerificationState,
    VerificationActions,
    verification_reducer,
)

from rlm.redux.slices.routing_slice import (
    RoutingDecisionType,
    RoutingDecision,
    BackendMetrics,
    RoutingState,
    RoutingActions,
    routing_reducer,
)

from rlm.redux.store import (
    RootState,
    ReduxStore,
    SessionPersistence,
    create_store,
)

__all__ = [
    "VerificationStatus",
    "Layer1State",
    "TheoremVerification",
    "VerificationState",
    "VerificationActions",
    "verification_reducer",
    "RoutingDecisionType",
    "RoutingDecision",
    "BackendMetrics",
    "RoutingState",
    "RoutingActions",
    "routing_reducer",
    "RootState",
    "ReduxStore",
    "SessionPersistence",
    "create_store",
]
