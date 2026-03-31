"""
Skunkworks Module - Context of Discovery.

This module implements the Skunkworks Protocol for handling open-ended tasks
where the starting point is unknown. It decouples creative discovery from
formal verification.
"""

from rlm.skunkworks.protocol import (
    SkunkworksProtocol,
    SkunkworksStatus,
    HypothesisConfidence,
    Hypothesis,
    ExplorationStep,
    UserCollaborationRequest,
    SkunkworksSession,
)

__all__ = [
    "SkunkworksProtocol",
    "SkunkworksStatus",
    "HypothesisConfidence",
    "Hypothesis",
    "ExplorationStep",
    "UserCollaborationRequest",
    "SkunkworksSession",
]
