"""
Edge Domains Module - Advanced Edge Cases and User Overrides.

This module handles advanced edge domains including CYBER_SEC, REVERSE_ENGINEERING,
hardware protocol discovery, and user-defined axiom overrides (Layer 1.5).
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
from enum import Enum
import threading
import time
import uuid

from rlm.routing.domain_classifier import DomainType


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
    name: str
    source: OverrideSource
    lean_axiom: str
    description: str
    human_readable: str
    created_at: float = field(default_factory=time.time)
    verified: bool = False


@dataclass
class Layer1_5Override:
    """Layer 1.5 axiom override file."""

    id: str
    task_id: str
    overrides: List[UserAxiomOverride] = field(default_factory=list)
    compiled_content: Optional[str] = None
    is_active: bool = False
    created_at: float = field(default_factory=time.time)


@dataclass
class HardwareProtocol:
    """A discovered hardware protocol."""

    id: str
    name: str
    description: str
    discovered_transitions: int = 0
    fsm_description: Optional[str] = None
    verified_theorems: List[str] = field(default_factory=list)
    discovered_at: float = field(default_factory=time.time)


@dataclass
class SandboxConfig:
    """Configuration for a sandbox environment."""

    sandbox_id: str
    security_level: SandboxSecurityLevel
    is_isolated: bool = True
    network_access: bool = False
    timeout_seconds: int = 300


class EdgeDomainManager:
    """
    Manager for edge domains and user overrides.

    Responsibilities:
    1. Manage CYBER_SEC and REVERSE_ENGINEERING domains
    2. Handle user-defined axiom overrides (Layer 1.5)
    3. Manage sandbox configurations for hardware discovery
    4. Track discovered hardware protocols
    """

    def __init__(self):
        """Initialize the edge domain manager."""
        self._user_overrides: Dict[str, Layer1_5Override] = {}
        self._active_overrides: List[UserAxiomOverride] = []
        self._hardware_protocols: Dict[str, HardwareProtocol] = {}
        self._sandbox_configs: Dict[str, SandboxConfig] = {}
        self._lock = threading.Lock()
        self._callbacks: Dict[str, List[Callable]] = {
            "override_added": [],
            "override_activated": [],
            "protocol_discovered": [],
            "sandbox_created": [],
        }

    # ============ User Override Management ============

    def create_layer1_5_override(
        self,
        task_id: str,
        overrides: List[Dict[str, str]],
    ) -> Layer1_5Override:
        """
        Create a Layer 1.5 override file from user axioms.

        Args:
            task_id: ID of the task
            overrides: List of axiom definitions

        Returns:
            The created Layer 1.5 override
        """
        override_list = [
            UserAxiomOverride(
                id=str(uuid.uuid4()),
                name=o.get("name", f"axiom_{i}"),
                source=OverrideSource(o.get("source", "user")),
                lean_axiom=o.get("lean_axiom", o.get("expression", "")),
                description=o.get("description", ""),
                human_readable=o.get("human_readable", ""),
            )
            for i, o in enumerate(overrides)
        ]

        override = Layer1_5Override(
            id=str(uuid.uuid4()),
            task_id=task_id,
            overrides=override_list,
        )

        # Generate compiled content
        override.compiled_content = self._generate_override_file(override)

        with self._lock:
            self._user_overrides[override.id] = override
            self._emit("override_added", {"override": override})

        return override

    def activate_override(self, override_id: str) -> bool:
        """
        Activate a Layer 1.5 override.

        Args:
            override_id: ID of the override to activate

        Returns:
            True if activated successfully
        """
        with self._lock:
            override = self._user_overrides.get(override_id)
            if not override:
                return False

            override.is_active = True
            self._active_overrides.extend(override.overrides)

            self._emit("override_activated", {"override": override})
            return True

    def deactivate_override(self, override_id: str) -> bool:
        """
        Deactivate a Layer 1.5 override.

        Args:
            override_id: ID of the override to deactivate

        Returns:
            True if deactivated successfully
        """
        with self._lock:
            override = self._user_overrides.get(override_id)
            if not override:
                return False

            override.is_active = False
            self._active_overrides = [
                o
                for o in self._active_overrides
                if o.id not in [ao.id for ao in override.overrides]
            ]
            return True

    def get_override(self, override_id: str) -> Optional[Layer1_5Override]:
        """Get a override by ID."""
        with self._lock:
            return self._user_overrides.get(override_id)

    def get_active_overrides(self) -> List[UserAxiomOverride]:
        """Get all active user axiom overrides."""
        with self._lock:
            return self._active_overrides.copy()

    # ============ Hardware Protocol Management ============

    def register_hardware_protocol(
        self,
        name: str,
        description: str,
    ) -> HardwareProtocol:
        """
        Register a new hardware protocol for tracking.

        Args:
            name: Protocol name
            description: Protocol description

        Returns:
            The created protocol
        """
        protocol = HardwareProtocol(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
        )

        with self._lock:
            self._hardware_protocols[protocol.id] = protocol
            self._emit("protocol_discovered", {"protocol": protocol})

        return protocol

    def update_hardware_protocol(
        self,
        protocol_id: str,
        fsm_description: Optional[str] = None,
        transitions: Optional[int] = None,
    ) -> bool:
        """
        Update a hardware protocol with discovered information.

        Args:
            protocol_id: ID of the protocol
            fsm_description: Description of the discovered FSM
            transitions: Number of discovered transitions

        Returns:
            True if updated successfully
        """
        with self._lock:
            protocol = self._hardware_protocols.get(protocol_id)
            if not protocol:
                return False

            if fsm_description is not None:
                protocol.fsm_description = fsm_description
            if transitions is not None:
                protocol.discovered_transitions = transitions

            return True

    def add_verified_theorem(self, protocol_id: str, theorem: str) -> bool:
        """
        Add a verified theorem to a hardware protocol.

        Args:
            protocol_id: ID of the protocol
            theorem: Theorem description

        Returns:
            True if added successfully
        """
        with self._lock:
            protocol = self._hardware_protocols.get(protocol_id)
            if not protocol:
                return False

            protocol.verified_theorems.append(theorem)
            return True

    def get_hardware_protocol(self, protocol_id: str) -> Optional[HardwareProtocol]:
        """Get a hardware protocol by ID."""
        with self._lock:
            return self._hardware_protocols.get(protocol_id)

    def get_all_protocols(self) -> List[HardwareProtocol]:
        """Get all registered hardware protocols."""
        with self._lock:
            return list(self._hardware_protocols.values())

    # ============ Sandbox Management ============

    def create_sandbox(
        self,
        security_level: SandboxSecurityLevel = SandboxSecurityLevel.ENHANCED,
        is_isolated: bool = True,
        network_access: bool = False,
        timeout_seconds: int = 300,
    ) -> SandboxConfig:
        """
        Create a sandbox configuration.

        Args:
            security_level: Security level
            is_isolated: Whether sandbox is isolated
            network_access: Whether network access is allowed
            timeout_seconds: Timeout for operations

        Returns:
            The created sandbox config
        """
        sandbox = SandboxConfig(
            sandbox_id=str(uuid.uuid4()),
            security_level=security_level,
            is_isolated=is_isolated,
            network_access=network_access,
            timeout_seconds=timeout_seconds,
        )

        with self._lock:
            self._sandbox_configs[sandbox.sandbox_id] = sandbox
            self._emit("sandbox_created", {"sandbox": sandbox})

        return sandbox

    def get_sandbox(self, sandbox_id: str) -> Optional[SandboxConfig]:
        """Get a sandbox config by ID."""
        with self._lock:
            return self._sandbox_configs.get(sandbox_id)

    # ============ Helpers ============

    def _generate_override_file(self, override: Layer1_5Override) -> str:
        """Generate the Lean file content for an override."""
        lines = [
            "-- USER AXIOM OVERRIDES (LAYER 1.5)",
            f"-- Task: {override.task_id}",
            f"-- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "-- WARNING: User-defined axioms bypass Lean kernel safety!",
            "",
            "namespace Layer1_5",
            "",
        ]

        for axiom in override.overrides:
            lines.append(f"/- {axiom.description} -/")
            lines.append(f"axiom {axiom.name} : {axiom.lean_axiom}")
            lines.append("")

        lines.append("end Layer1_5")
        return "\n".join(lines)

    def generate_layer1_5_for_task(
        self,
        task_description: str,
    ) -> Optional[str]:
        """
        Parse task description for <axioms> block and generate Layer 1.5.

        Args:
            task_description: Task description with optional <axioms> block

        Returns:
            Generated Layer 1.5 file content, or None if no axioms found
        """
        import re

        # Look for <axioms>...</axioms> block
        match = re.search(r"<axioms>(.*?)</axioms>", task_description, re.DOTALL)
        if not match:
            return None

        axioms_text = match.group(1)

        # Parse individual axioms (numbered lines)
        overrides = []
        for line in axioms_text.strip().split("\n"):
            line = line.strip()
            if not line:
                continue

            # Match "1. All traffic..." style
            m = re.match(r"^\d+\.\s+(.*)$", line)
            if m:
                description = m.group(1)
            else:
                description = line

            # Generate a simple axiom name
            axiom_name = f"user_axiom_{len(overrides) + 1}"

            overrides.append(
                {
                    "name": axiom_name,
                    "description": description,
                    "lean_axiom": f"/- User override: {description} -/",
                    "source": "user",
                }
            )

        if not overrides:
            return None

        # Create override and generate content
        override = self.create_layer1_5_override(
            task_id=f"task_{hash(task_description) % 10000}",
            overrides=overrides,
        )

        return override.compiled_content

    def register_callback(self, event: str, callback: Callable) -> None:
        """
        Register a callback for manager events.

        Args:
            event: Event type
            callback: Function to call
        """
        if event in self._callbacks and callback not in self._callbacks[event]:
            self._callbacks[event].append(callback)

    def _emit(self, event: str, data: Dict[str, Any]) -> None:
        """Emit an event to callbacks."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(data)
            except Exception:
                pass
