"""
Edge Domains Module - Advanced Edge Cases and User Overrides.

This module handles advanced edge domains including CYBER_SEC, REVERSE_ENGINEERING,
hardware protocol discovery, and user-defined axiom overrides (Layer 1.5).
"""

from rlm.edge.edge_domains import (
    EdgeDomainManager,
    EdgeDomainType,
    SandboxSecurityLevel,
    OverrideSource,
    UserAxiomOverride,
    Layer1_5Override,
    HardwareProtocol,
    SandboxConfig,
)

__all__ = [
    "EdgeDomainManager",
    "EdgeDomainType",
    "SandboxSecurityLevel",
    "OverrideSource",
    "UserAxiomOverride",
    "Layer1_5Override",
    "HardwareProtocol",
    "SandboxConfig",
]
