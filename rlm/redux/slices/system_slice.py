"""
Redux slice for system configuration state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class RealtimeMode(Enum):
    WEBSOCKET = "websocket"
    POLLING = "polling"


@dataclass
class ResourceLimits:
    cpu: float = 4.0
    memory_gb: float = 16.0
    tokens: int = 100000


@dataclass
class SecuritySettings:
    message_validation: bool = True
    tool_approval_required: bool = True
    agent_isolation: bool = False


@dataclass
class PerformanceSettings:
    message_batch_size: int = 10
    state_update_interval_ms: int = 1000
    cleanup_interval_ms: int = 60000


@dataclass
class RealtimeSettings:
    mode: RealtimeMode = RealtimeMode.WEBSOCKET
    poll_interval_ms: int = 1000
    per_panel_mode: Dict[str, str] = field(default_factory=lambda: {
        "permission-queue": "websocket",
        "verification": "websocket",
        "agent-communication": "websocket",
        "routing": "polling",
        "tool-review": "polling"
    })


@dataclass
class RetentionSettings:
    max_threads: int = 50
    auto_archive_after: int = 10
    persist_all: bool = False


@dataclass
class SystemConfiguration:
    resource_limits: ResourceLimits = field(default_factory=ResourceLimits)
    security: SecuritySettings = field(default_factory=SecuritySettings)
    performance: PerformanceSettings = field(default_factory=PerformanceSettings)
    realtime: RealtimeSettings = field(default_factory=RealtimeSettings)
    retention: RetentionSettings = field(default_factory=RetentionSettings)


@dataclass
class SystemState:
    config: SystemConfiguration = field(default_factory=SystemConfiguration)
    pending_changes: Dict[str, Any] = field(default_factory=dict)
    session_id: Optional[str] = None
    session_start_time: float = 0.0


class SystemActions:
    @staticmethod
    def update_configuration(path: str, value: Any) -> dict:
        return {"type": "system/update_configuration", "payload": {"path": path, "value": value}}

    @staticmethod
    def reset_configuration() -> dict:
        return {"type": "system/reset_configuration"}

    @staticmethod
    def export_configuration() -> dict:
        return {"type": "system/export_configuration"}

    @staticmethod
    def import_configuration(config: SystemConfiguration) -> dict:
        return {"type": "system/import_configuration", "payload": config}

    @staticmethod
    def set_session_id(session_id: str) -> dict:
        return {"type": "system/set_session_id", "payload": {"session_id": session_id}}

    @staticmethod
    def set_pending_change(path: str, value: Any) -> dict:
        return {"type": "system/set_pending_change", "payload": {"path": path, "value": value}}

    @staticmethod
    def clear_pending_changes() -> dict:
        return {"type": "system/clear_pending_changes"}


def system_reducer(state: SystemState, action: dict) -> SystemState:
    action_type = action.get("type")

    if action_type == "system/update_configuration":
        payload = action.get("payload", {})
        path = payload.get("path", "")
        value = payload.get("value")
        new_config = state.config
        parts = path.split(".")
        if len(parts) == 1:
            if hasattr(new_config, parts[0]):
                setattr(new_config, parts[0], value)
        elif len(parts) == 2:
            if hasattr(new_config, parts[0]):
                sub_obj = getattr(new_config, parts[0])
                if hasattr(sub_obj, parts[1]):
                    setattr(sub_obj, parts[1], value)
        return SystemState(
            config=new_config,
            pending_changes=state.pending_changes,
            session_id=state.session_id,
            session_start_time=state.session_start_time
        )

    elif action_type == "system/reset_configuration":
        return SystemState(
            config=SystemConfiguration(),
            pending_changes={},
            session_id=state.session_id,
            session_start_time=state.session_start_time
        )

    elif action_type == "system/import_configuration":
        new_config = action.get("payload", SystemConfiguration())
        return SystemState(
            config=new_config,
            pending_changes={},
            session_id=state.session_id,
            session_start_time=state.session_start_time
        )

    elif action_type == "system/set_session_id":
        payload = action.get("payload", {})
        return SystemState(
            config=state.config,
            pending_changes=state.pending_changes,
            session_id=payload.get("session_id"),
            session_start_time=state.session_start_time
        )

    elif action_type == "system/set_pending_change":
        payload = action.get("payload", {})
        new_pending = state.pending_changes.copy()
        new_pending[payload.get("path")] = payload.get("value")
        return SystemState(
            config=state.config,
            pending_changes=new_pending,
            session_id=state.session_id,
            session_start_time=state.session_start_time
        )

    elif action_type == "system/clear_pending_changes":
        return SystemState(
            config=state.config,
            pending_changes={},
            session_id=state.session_id,
            session_start_time=state.session_start_time
        )

    return state
