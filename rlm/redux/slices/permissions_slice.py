"""
Redux slice for permissions state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class PermissionAction(Enum):
    APPROVE = "approve"
    DENY = "deny"
    ASK = "ask"


class PermissionType(Enum):
    TOOL_CREATION = "tool_creation"
    NETWORK_ACCESS = "network_access"
    AGENT_SPAWNING = "agent_spawning"
    FILESYSTEM_WRITE = "filesystem_write"
    CODE_EXECUTION = "code_execution"
    EXTERNAL_API = "external_api"


@dataclass
class PermissionRequest:
    request_id: str
    requesting_agent_id: str
    permission_type: PermissionType
    description: str
    risk_assessment: str
    created_at: float
    status: str = "pending"
    response_at: Optional[float] = None
    response_action: Optional[str] = None
    reason: Optional[str] = None


@dataclass
class PermissionDefaults:
    action: PermissionAction = PermissionAction.ASK
    scope: str = "global"
    scope_id: Optional[str] = None


@dataclass
class PermissionRecord:
    request_id: str
    permission_type: str
    action: str
    timestamp: float
    reason: Optional[str] = None


@dataclass
class PermissionsState:
    pending_requests: List[PermissionRequest] = field(default_factory=list)
    defaults: Dict[str, PermissionAction] = field(default_factory=dict)
    scope_defaults: Dict[str, PermissionDefaults] = field(default_factory=dict)
    history: List[PermissionRecord] = field(default_factory=list)


class PermissionsActions:
    @staticmethod
    def approve_request(request_id: str, remember: bool = False) -> dict:
        return {"type": "permissions/approve_request", "payload": {"request_id": request_id, "remember": remember}}

    @staticmethod
    def deny_request(request_id: str, reason: Optional[str] = None) -> dict:
        return {"type": "permissions/deny_request", "payload": {"request_id": request_id, "reason": reason}}

    @staticmethod
    def set_default(permission_type: str, action: PermissionAction) -> dict:
        return {"type": "permissions/set_default", "payload": {"permission_type": permission_type, "action": action.value}}

    @staticmethod
    def set_default_scope(permission_type: str, scope: str, scope_id: Optional[str] = None) -> dict:
        return {"type": "permissions/set_default_scope", "payload": {"permission_type": permission_type, "scope": scope, "scope_id": scope_id}}

    @staticmethod
    def add_request(request: PermissionRequest) -> dict:
        return {"type": "permissions/add_request", "payload": request}

    @staticmethod
    def clear_history() -> dict:
        return {"type": "permissions/clear_history"}


def permissions_reducer(state: PermissionsState, action: dict) -> PermissionsState:
    action_type = action.get("type")

    if action_type == "permissions/approve_request":
        payload = action.get("payload", {})
        request_id = payload.get("request_id")
        remember = payload.get("remember", False)
        new_pending = [r for r in state.pending_requests if r.request_id != request_id]
        new_history = state.history.copy()
        for req in state.pending_requests:
            if req.request_id == request_id:
                new_history.append(PermissionRecord(
                    request_id=request_id,
                    permission_type=req.permission_type.value,
                    action="approve",
                    timestamp=payload.get("timestamp", 0.0)
                ))
                if remember:
                    new_defaults = state.defaults.copy()
                    new_defaults[req.permission_type.value] = PermissionAction.APPROVE
                break
        return PermissionsState(
            pending_requests=new_pending,
            defaults=state.defaults,
            scope_defaults=state.scope_defaults,
            history=new_history
        )

    elif action_type == "permissions/deny_request":
        payload = action.get("payload", {})
        request_id = payload.get("request_id")
        reason = payload.get("reason")
        new_pending = [r for r in state.pending_requests if r.request_id != request_id]
        new_history = state.history.copy()
        for req in state.pending_requests:
            if req.request_id == request_id:
                new_history.append(PermissionRecord(
                    request_id=request_id,
                    permission_type=req.permission_type.value,
                    action="deny",
                    timestamp=payload.get("timestamp", 0.0),
                    reason=reason
                ))
                break
        return PermissionsState(
            pending_requests=new_pending,
            defaults=state.defaults,
            scope_defaults=state.scope_defaults,
            history=new_history
        )

    elif action_type == "permissions/set_default":
        payload = action.get("payload", {})
        permission_type = payload.get("permission_type")
        action_str = payload.get("action")
        new_defaults = state.defaults.copy()
        new_defaults[permission_type] = PermissionAction(action_str)
        return PermissionsState(
            pending_requests=state.pending_requests,
            defaults=new_defaults,
            scope_defaults=state.scope_defaults,
            history=state.history
        )

    elif action_type == "permissions/set_default_scope":
        payload = action.get("payload", {})
        permission_type = payload.get("permission_type")
        scope = payload.get("scope")
        scope_id = payload.get("scope_id")
        key = f"{permission_type}:{scope}:{scope_id or 'global'}"
        new_scope_defaults = state.scope_defaults.copy()
        new_scope_defaults[key] = PermissionDefaults(
            action=state.defaults.get(permission_type, PermissionAction.ASK),
            scope=scope,
            scope_id=scope_id
        )
        return PermissionsState(
            pending_requests=state.pending_requests,
            defaults=state.defaults,
            scope_defaults=new_scope_defaults,
            history=state.history
        )

    elif action_type == "permissions/add_request":
        new_pending = state.pending_requests.copy()
        new_request: Any = action.get("payload")
        if new_request is not None:
            new_pending.append(new_request)
        return PermissionsState(
            pending_requests=new_pending,
            defaults=state.defaults,
            scope_defaults=state.scope_defaults,
            history=state.history
        )

    elif action_type == "permissions/clear_history":
        return PermissionsState(
            pending_requests=state.pending_requests,
            defaults=state.defaults,
            scope_defaults=state.scope_defaults,
            history=[]
        )

    return state
