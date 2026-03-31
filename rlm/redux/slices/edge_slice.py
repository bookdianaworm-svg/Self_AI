"""
Redux slice for advanced edge domains state management.

This module provides state management for Advanced Edge Domains including
CYBER_SEC, REVERSE_ENGINEERING, and user-defined axiomatic overrides.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum
import time


class EdgeDomainType(Enum):
    """Types of edge domains."""

    CYBER_SEC = "cyber_sec"
    REVERSE_ENGINEERING = "reverse_engineering"
    HARDWARE_DISCOVERY = "hardware_discovery"
    USER_OVERRIDE = "user_override"


class SandboxSecurityLevel(Enum):
    """Security level for sandboxed execution."""

    STANDARD = "standard"
    ENHANCED = "enhanced"
    AIR_GAPPED = "air_gapped"
    HARDENED = "hardened"


class OverrideSource(Enum):
    """Source of axiom override."""

    USER = "user"
    SYSTEM = "system"
    LAYER_1_5 = "layer_1_5"


@dataclass
class UserAxiomOverride:
    """A user-defined axiom override."""

    id: str
    source: OverrideSource
    lean_axiom: str
    description: str
    human_readable: str
    created_at: float = field(default_factory=time.time)
    verified: bool = False


@dataclass
class Layer1_5Override:
    """Layer 1.5 axiom override file content."""

    id: str
    task_id: str
    overrides: List[UserAxiomOverride] = field(default_factory=list)
    compiled_file: Optional[str] = None
    is_active: bool = False
    created_at: float = field(default_factory=time.time)


@dataclass
class HardwareProtocolState:
    """State for hardware protocol discovery."""

    protocol_id: str
    description: str
    fsm_id: Optional[str] = None
    learned_transitions: int = 0
    is_verified: bool = False
    verified_theorems: List[str] = field(default_factory=list)


@dataclass
class SandboxConfig:
    """Configuration for a sandbox environment."""

    sandbox_id: str
    security_level: SandboxSecurityLevel
    is_isolated: bool = True
    network_access: bool = False
    timeout_seconds: int = 300


@dataclass
class EdgeDomainState:
    """Redux slice for edge domains state."""

    active_edge_domain: Optional[str] = None
    user_overrides: Dict[str, Layer1_5Override] = field(default_factory=dict)
    active_overrides: List[UserAxiomOverride] = field(default_factory=list)
    hardware_protocols: Dict[str, HardwareProtocolState] = field(default_factory=dict)
    sandboxes: Dict[str, SandboxConfig] = field(default_factory=dict)
    protocol_discovery_history: List[Dict] = field(default_factory=list)


class EdgeActions:
    """Action creators for edge domain state updates."""

    @staticmethod
    def set_active_edge_domain(domain: Optional[str]) -> dict:
        """Create action to set the active edge domain."""
        return {
            "type": "edge/set_active_domain",
            "payload": {"domain": domain},
        }

    @staticmethod
    def create_layer1_5_override(layer1_5: Layer1_5Override) -> dict:
        """Create action to create a Layer 1.5 override."""
        return {
            "type": "edge/create_layer1_5_override",
            "payload": {
                "id": layer1_5.id,
                "task_id": layer1_5.task_id,
                "overrides": [
                    {
                        "id": o.id,
                        "source": o.source.value,
                        "lean_axiom": o.lean_axiom,
                        "description": o.description,
                        "human_readable": o.human_readable,
                    }
                    for o in layer1_5.overrides
                ],
            },
        }

    @staticmethod
    def add_user_axiom_override(override: UserAxiomOverride) -> dict:
        """Create action to add a user axiom override."""
        return {
            "type": "edge/add_user_axiom_override",
            "payload": {
                "id": override.id,
                "source": override.source.value,
                "lean_axiom": override.lean_axiom,
                "description": override.description,
                "human_readable": override.human_readable,
            },
        }

    @staticmethod
    def activate_overrides(layer1_5_id: str) -> dict:
        """Create action to activate layer 1.5 overrides."""
        return {
            "type": "edge/activate_overrides",
            "payload": {"layer1_5_id": layer1_5_id},
        }

    @staticmethod
    def deactivate_overrides(layer1_5_id: str) -> dict:
        """Create action to deactivate layer 1.5 overrides."""
        return {
            "type": "edge/deactivate_overrides",
            "payload": {"layer1_5_id": layer1_5_id},
        }

    @staticmethod
    def verify_override(override_id: str, verified: bool) -> dict:
        """Create action to verify a user override."""
        return {
            "type": "edge/verify_override",
            "payload": {
                "override_id": override_id,
                "verified": verified,
            },
        }

    @staticmethod
    def create_hardware_protocol(protocol: HardwareProtocolState) -> dict:
        """Create action to create a hardware protocol state."""
        return {
            "type": "edge/create_hardware_protocol",
            "payload": {
                "protocol_id": protocol.protocol_id,
                "description": protocol.description,
            },
        }

    @staticmethod
    def update_hardware_protocol(
        protocol_id: str,
        fsm_id: Optional[str] = None,
        learned_transitions: Optional[int] = None,
    ) -> dict:
        """Create action to update hardware protocol state."""
        return {
            "type": "edge/update_hardware_protocol",
            "payload": {
                "protocol_id": protocol_id,
                "fsm_id": fsm_id,
                "learned_transitions": learned_transitions,
            },
        }

    @staticmethod
    def verify_hardware_protocol(
        protocol_id: str, verified: bool, theorems: List[str]
    ) -> dict:
        """Create action to verify hardware protocol."""
        return {
            "type": "edge/verify_hardware_protocol",
            "payload": {
                "protocol_id": protocol_id,
                "verified": verified,
                "theorems": theorems,
            },
        }

    @staticmethod
    def create_sandbox(sandbox: SandboxConfig) -> dict:
        """Create action to create a sandbox configuration."""
        return {
            "type": "edge/create_sandbox",
            "payload": {
                "sandbox_id": sandbox.sandbox_id,
                "security_level": sandbox.security_level.value,
                "is_isolated": sandbox.is_isolated,
                "network_access": sandbox.network_access,
                "timeout_seconds": sandbox.timeout_seconds,
            },
        }

    @staticmethod
    def update_sandbox_security(
        sandbox_id: str, security_level: SandboxSecurityLevel
    ) -> dict:
        """Create action to update sandbox security level."""
        return {
            "type": "edge/update_sandbox_security",
            "payload": {
                "sandbox_id": sandbox_id,
                "security_level": security_level.value,
            },
        }


def edge_reducer(state: EdgeDomainState, action: dict) -> EdgeDomainState:
    """
    Reducer function for edge domain state.

    Args:
        state: Current edge domain state.
        action: Action to apply to the state.

    Returns:
        New edge domain state.
    """
    action_type = action.get("type")

    if action_type == "edge/set_active_domain":
        payload = action.get("payload", {})
        return EdgeDomainState(
            active_edge_domain=payload.get("domain"),
            user_overrides=state.user_overrides,
            active_overrides=state.active_overrides,
            hardware_protocols=state.hardware_protocols,
            sandboxes=state.sandboxes,
            protocol_discovery_history=state.protocol_discovery_history,
        )

    elif action_type == "edge/create_layer1_5_override":
        payload = action.get("payload", {})
        overrides = [
            UserAxiomOverride(
                id=o.get("id"),
                source=OverrideSource(o.get("source", "user")),
                lean_axiom=o.get("lean_axiom", ""),
                description=o.get("description", ""),
                human_readable=o.get("human_readable", ""),
            )
            for o in payload.get("overrides", [])
        ]
        layer1_5 = Layer1_5Override(
            id=payload.get("id"),
            task_id=payload.get("task_id"),
            overrides=overrides,
        )
        new_overrides = state.user_overrides.copy()
        new_overrides[layer1_5.id] = layer1_5
        return EdgeDomainState(
            active_edge_domain=state.active_edge_domain,
            user_overrides=new_overrides,
            active_overrides=state.active_overrides,
            hardware_protocols=state.hardware_protocols,
            sandboxes=state.sandboxes,
            protocol_discovery_history=state.protocol_discovery_history,
        )

    elif action_type == "edge/add_user_axiom_override":
        payload = action.get("payload", {})
        override = UserAxiomOverride(
            id=payload.get("id"),
            source=OverrideSource(payload.get("source", "user")),
            lean_axiom=payload.get("lean_axiom", ""),
            description=payload.get("description", ""),
            human_readable=payload.get("human_readable", ""),
        )
        new_active = state.active_overrides + [override]
        return EdgeDomainState(
            active_edge_domain=state.active_edge_domain,
            user_overrides=state.user_overrides,
            active_overrides=new_active,
            hardware_protocols=state.hardware_protocols,
            sandboxes=state.sandboxes,
            protocol_discovery_history=state.protocol_discovery_history,
        )

    elif action_type == "edge/activate_overrides":
        payload = action.get("payload", {})
        layer1_5_id = payload.get("layer1_5_id")
        layer1_5 = state.user_overrides.get(layer1_5_id)
        if layer1_5:
            layer1_5.is_active = True
            new_overrides = state.user_overrides.copy()
            new_overrides[layer1_5_id] = layer1_5
            new_active = state.active_overrides + layer1_5.overrides
            return EdgeDomainState(
                active_edge_domain=state.active_edge_domain,
                user_overrides=new_overrides,
                active_overrides=new_active,
                hardware_protocols=state.hardware_protocols,
                sandboxes=state.sandboxes,
                protocol_discovery_history=state.protocol_discovery_history,
            )
        return state

    elif action_type == "edge/deactivate_overrides":
        payload = action.get("payload", {})
        layer1_5_id = payload.get("layer1_5_id")
        layer1_5 = state.user_overrides.get(layer1_5_id)
        if layer1_5:
            layer1_5.is_active = False
            new_overrides = state.user_overrides.copy()
            new_overrides[layer1_5_id] = layer1_5
            new_active = [
                o
                for o in state.active_overrides
                if o.id not in [ao.id for ao in layer1_5.overrides]
            ]
            return EdgeDomainState(
                active_edge_domain=state.active_edge_domain,
                user_overrides=new_overrides,
                active_overrides=new_active,
                hardware_protocols=state.hardware_protocols,
                sandboxes=state.sandboxes,
                protocol_discovery_history=state.protocol_discovery_history,
            )
        return state

    elif action_type == "edge/verify_override":
        payload = action.get("payload", {})
        override_id = payload.get("override_id")
        verified = payload.get("verified", False)
        for override in state.active_overrides:
            if override.id == override_id:
                override.verified = verified
                break
        return EdgeDomainState(
            active_edge_domain=state.active_edge_domain,
            user_overrides=state.user_overrides,
            active_overrides=state.active_overrides,
            hardware_protocols=state.hardware_protocols,
            sandboxes=state.sandboxes,
            protocol_discovery_history=state.protocol_discovery_history,
        )

    elif action_type == "edge/create_hardware_protocol":
        payload = action.get("payload", {})
        protocol = HardwareProtocolState(
            protocol_id=payload.get("protocol_id"),
            description=payload.get("description"),
        )
        new_protocols = state.hardware_protocols.copy()
        new_protocols[protocol.protocol_id] = protocol
        return EdgeDomainState(
            active_edge_domain=state.active_edge_domain,
            user_overrides=state.user_overrides,
            active_overrides=state.active_overrides,
            hardware_protocols=new_protocols,
            sandboxes=state.sandboxes,
            protocol_discovery_history=state.protocol_discovery_history,
        )

    elif action_type == "edge/update_hardware_protocol":
        payload = action.get("payload", {})
        protocol_id = payload.get("protocol_id")
        protocol = state.hardware_protocols.get(protocol_id)
        if protocol:
            if payload.get("fsm_id") is not None:
                protocol.fsm_id = payload.get("fsm_id")
            if payload.get("learned_transitions") is not None:
                protocol.learned_transitions = payload.get("learned_transitions")
            new_protocols = state.hardware_protocols.copy()
            new_protocols[protocol_id] = protocol
            return EdgeDomainState(
                active_edge_domain=state.active_edge_domain,
                user_overrides=state.user_overrides,
                active_overrides=state.active_overrides,
                hardware_protocols=new_protocols,
                sandboxes=state.sandboxes,
                protocol_discovery_history=state.protocol_discovery_history,
            )
        return state

    elif action_type == "edge/verify_hardware_protocol":
        payload = action.get("payload", {})
        protocol_id = payload.get("protocol_id")
        protocol = state.hardware_protocols.get(protocol_id)
        if protocol:
            protocol.is_verified = payload.get("verified", False)
            protocol.verified_theorems = payload.get("theorems", [])
            new_protocols = state.hardware_protocols.copy()
            new_protocols[protocol_id] = protocol
            new_history = state.protocol_discovery_history + [
                {
                    "protocol_id": protocol_id,
                    "verified": protocol.is_verified,
                    "theorems": protocol.verified_theorems,
                    "verified_at": time.time(),
                }
            ]
            return EdgeDomainState(
                active_edge_domain=state.active_edge_domain,
                user_overrides=state.user_overrides,
                active_overrides=state.active_overrides,
                hardware_protocols=new_protocols,
                sandboxes=state.sandboxes,
                protocol_discovery_history=new_history,
            )
        return state

    elif action_type == "edge/create_sandbox":
        payload = action.get("payload", {})
        sandbox = SandboxConfig(
            sandbox_id=payload.get("sandbox_id"),
            security_level=SandboxSecurityLevel(
                payload.get("security_level", "standard")
            ),
            is_isolated=payload.get("is_isolated", True),
            network_access=payload.get("network_access", False),
            timeout_seconds=payload.get("timeout_seconds", 300),
        )
        new_sandboxes = state.sandboxes.copy()
        new_sandboxes[sandbox.sandbox_id] = sandbox
        return EdgeDomainState(
            active_edge_domain=state.active_edge_domain,
            user_overrides=state.user_overrides,
            active_overrides=state.active_overrides,
            hardware_protocols=state.hardware_protocols,
            sandboxes=new_sandboxes,
            protocol_discovery_history=state.protocol_discovery_history,
        )

    elif action_type == "edge/update_sandbox_security":
        payload = action.get("payload", {})
        sandbox_id = payload.get("sandbox_id")
        sandbox = state.sandboxes.get(sandbox_id)
        if sandbox:
            sandbox.security_level = SandboxSecurityLevel(
                payload.get("security_level", "standard")
            )
            new_sandboxes = state.sandboxes.copy()
            new_sandboxes[sandbox_id] = sandbox
            return EdgeDomainState(
                active_edge_domain=state.active_edge_domain,
                user_overrides=state.user_overrides,
                active_overrides=state.active_overrides,
                hardware_protocols=state.hardware_protocols,
                sandboxes=new_sandboxes,
                protocol_discovery_history=state.protocol_discovery_history,
            )
        return state

    return state
