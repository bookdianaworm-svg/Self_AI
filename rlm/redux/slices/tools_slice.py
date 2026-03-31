"""
Redux slice for tools state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ToolStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SANDBOX_TESTING = "sandbox_testing"


@dataclass
class ToolDefinition:
    tool_id: str
    name: str
    code: str
    language: str
    created_by: str
    created_at: float
    status: ToolStatus = ToolStatus.PENDING
    security_scan: Optional[Dict[str, Any]] = None
    compatibility: List[str] = field(default_factory=list)
    approval_scope: Optional[str] = None
    rejection_reason: Optional[str] = None


@dataclass
class ToolDefaults:
    action: str = "ask"
    scope: str = "global"
    scope_id: Optional[str] = None


@dataclass
class ToolsState:
    pending_tools: List[ToolDefinition] = field(default_factory=list)
    approved_tools: Dict[str, ToolDefinition] = field(default_factory=dict)
    rejected_tools: Dict[str, ToolDefinition] = field(default_factory=dict)
    defaults: Dict[str, ToolDefaults] = field(default_factory=dict)


class ToolsActions:
    @staticmethod
    def approve_tool(tool_id: str, scope: Optional[str] = None, scope_id: Optional[str] = None) -> dict:
        return {"type": "tools/approve_tool", "payload": {"tool_id": tool_id, "scope": scope, "scope_id": scope_id}}

    @staticmethod
    def reject_tool(tool_id: str, reason: str) -> dict:
        return {"type": "tools/reject_tool", "payload": {"tool_id": tool_id, "reason": reason}}

    @staticmethod
    def set_tool_default(tool_type: str, action: str) -> dict:
        return {"type": "tools/set_tool_default", "payload": {"tool_type": tool_type, "action": action}}

    @staticmethod
    def add_tool(tool: ToolDefinition) -> dict:
        return {"type": "tools/add_tool", "payload": tool}

    @staticmethod
    def sandbox_test_tool(tool_id: str) -> dict:
        return {"type": "tools/sandbox_test", "payload": {"tool_id": tool_id}}


def tools_reducer(state: ToolsState, action: dict) -> ToolsState:
    action_type = action.get("type")

    if action_type == "tools/approve_tool":
        payload = action.get("payload", {})
        tool_id = payload.get("tool_id")
        scope = payload.get("scope", "global")
        new_pending = [t for t in state.pending_tools if t.tool_id != tool_id]
        new_approved = state.approved_tools.copy()
        for tool in state.pending_tools:
            if tool.tool_id == tool_id:
                tool.status = ToolStatus.APPROVED
                tool.approval_scope = scope
                new_approved[tool_id] = tool
                break
        return ToolsState(
            pending_tools=new_pending,
            approved_tools=new_approved,
            rejected_tools=state.rejected_tools,
            defaults=state.defaults
        )

    elif action_type == "tools/reject_tool":
        payload = action.get("payload", {})
        tool_id = payload.get("tool_id")
        reason = payload.get("reason")
        new_pending = [t for t in state.pending_tools if t.tool_id != tool_id]
        new_rejected = state.rejected_tools.copy()
        for tool in state.pending_tools:
            if tool.tool_id == tool_id:
                tool.status = ToolStatus.REJECTED
                tool.rejection_reason = reason
                new_rejected[tool_id] = tool
                break
        return ToolsState(
            pending_tools=new_pending,
            approved_tools=state.approved_tools,
            rejected_tools=new_rejected,
            defaults=state.defaults
        )

    elif action_type == "tools/set_tool_default":
        payload = action.get("payload", {})
        tool_type = payload.get("tool_type")
        action_str = payload.get("action")
        new_defaults = state.defaults.copy()
        new_defaults[tool_type] = ToolDefaults(action=action_str)
        return ToolsState(
            pending_tools=state.pending_tools,
            approved_tools=state.approved_tools,
            rejected_tools=state.rejected_tools,
            defaults=new_defaults
        )

    elif action_type == "tools/add_tool":
        new_pending = state.pending_tools.copy()
        new_tool: Any = action.get("payload")
        if new_tool is not None:
            new_pending.append(new_tool)
        return ToolsState(
            pending_tools=new_pending,
            approved_tools=state.approved_tools,
            rejected_tools=state.rejected_tools,
            defaults=state.defaults
        )

    elif action_type == "tools/sandbox_test":
        payload = action.get("payload", {})
        tool_id = payload.get("tool_id")
        for tool in state.pending_tools:
            if tool.tool_id == tool_id:
                tool.status = ToolStatus.SANDBOX_TESTING
                break
        return state

    return state
