"""
Redux slice for UI state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class PanelId(Enum):
    TASK_SUBMISSION = "task-submission"
    PERMISSION_QUEUE = "permission-queue"
    TOOL_REVIEW = "tool-review"
    IMPROVEMENT_REVIEW = "improvement-review"
    ROUTING_CONTROL = "routing-control"
    VERIFICATION_CONTROL = "verification-control"
    AGENT_COMMUNICATION = "agent-communication"
    INTERVENTION = "intervention"
    SYSTEM_CONFIG = "system-config"


@dataclass
class Notification:
    notification_id: str
    message: str
    severity: str = "info"
    timestamp: float = 0.0
    dismissed: bool = False


@dataclass
class UIState:
    active_panel: PanelId = PanelId.TASK_SUBMISSION
    command_bar_open: bool = False
    command_input: str = ""
    active_panel_id: Optional[str] = None
    notifications: List[Notification] = field(default_factory=list)
    modal_open: Optional[str] = None
    modal_data: Optional[Dict[str, Any]] = None
    split_view: bool = False
    left_panel: Optional[PanelId] = None
    right_panel: Optional[PanelId] = None
    search_query: str = ""
    search_results: List[Dict[str, Any]] = field(default_factory=list)
    keyboard_shortcut_handlers: Dict[str, Any] = field(default_factory=dict)


class UIActions:
    @staticmethod
    def set_active_panel(panel_id: PanelId) -> dict:
        return {"type": "ui/set_active_panel", "payload": {"panel_id": panel_id.value}}

    @staticmethod
    def open_command_bar() -> dict:
        return {"type": "ui/open_command_bar"}

    @staticmethod
    def close_command_bar() -> dict:
        return {"type": "ui/close_command_bar"}

    @staticmethod
    def set_command_input(input_text: str) -> dict:
        return {"type": "ui/set_command_input", "payload": {"input": input_text}}

    @staticmethod
    def add_notification(message: str, severity: str = "info") -> dict:
        return {"type": "ui/add_notification", "payload": {"message": message, "severity": severity}}

    @staticmethod
    def dismiss_notification(notification_id: str) -> dict:
        return {"type": "ui/dismiss_notification", "payload": {"notification_id": notification_id}}

    @staticmethod
    def open_modal(modal_id: str, data: Optional[Dict[str, Any]] = None) -> dict:
        return {"type": "ui/open_modal", "payload": {"modal_id": modal_id, "data": data}}

    @staticmethod
    def close_modal() -> dict:
        return {"type": "ui/close_modal"}

    @staticmethod
    def set_split_view(enabled: bool, left: Optional[PanelId] = None, right: Optional[PanelId] = None) -> dict:
        return {"type": "ui/set_split_view", "payload": {"enabled": enabled, "left": left.value if left else None, "right": right.value if right else None}}

    @staticmethod
    def set_search_query(query: str) -> dict:
        return {"type": "ui/set_search_query", "payload": {"query": query}}

    @staticmethod
    def set_search_results(results: List[Dict[str, Any]]) -> dict:
        return {"type": "ui/set_search_results", "payload": {"results": results}}


def ui_reducer(state: UIState, action: dict) -> UIState:
    action_type = action.get("type")

    if action_type == "ui/set_active_panel":
        payload = action.get("payload", {})
        panel_id_str = payload.get("panel_id")
        try:
            panel_id = PanelId(panel_id_str)
        except (ValueError, TypeError):
            panel_id = PanelId.TASK_SUBMISSION
        return UIState(
            active_panel=panel_id,
            command_bar_open=state.command_bar_open,
            command_input=state.command_input,
            active_panel_id=payload.get("panel_id"),
            notifications=state.notifications,
            modal_open=state.modal_open,
            modal_data=state.modal_data,
            split_view=state.split_view,
            left_panel=state.left_panel,
            right_panel=state.right_panel,
            search_query=state.search_query,
            search_results=state.search_results,
            keyboard_shortcut_handlers=state.keyboard_shortcut_handlers
        )

    elif action_type == "ui/open_command_bar":
        return UIState(
            active_panel=state.active_panel,
            command_bar_open=True,
            command_input="",
            active_panel_id=state.active_panel_id,
            notifications=state.notifications,
            modal_open=state.modal_open,
            modal_data=state.modal_data,
            split_view=state.split_view,
            left_panel=state.left_panel,
            right_panel=state.right_panel,
            search_query=state.search_query,
            search_results=state.search_results,
            keyboard_shortcut_handlers=state.keyboard_shortcut_handlers
        )

    elif action_type == "ui/close_command_bar":
        return UIState(
            active_panel=state.active_panel,
            command_bar_open=False,
            command_input="",
            active_panel_id=state.active_panel_id,
            notifications=state.notifications,
            modal_open=state.modal_open,
            modal_data=state.modal_data,
            split_view=state.split_view,
            left_panel=state.left_panel,
            right_panel=state.right_panel,
            search_query=state.search_query,
            search_results=state.search_results,
            keyboard_shortcut_handlers=state.keyboard_shortcut_handlers
        )

    elif action_type == "ui/set_command_input":
        payload = action.get("payload", {})
        return UIState(
            active_panel=state.active_panel,
            command_bar_open=state.command_bar_open,
            command_input=payload.get("input", ""),
            active_panel_id=state.active_panel_id,
            notifications=state.notifications,
            modal_open=state.modal_open,
            modal_data=state.modal_data,
            split_view=state.split_view,
            left_panel=state.left_panel,
            right_panel=state.right_panel,
            search_query=state.search_query,
            search_results=state.search_results,
            keyboard_shortcut_handlers=state.keyboard_shortcut_handlers
        )

    elif action_type == "ui/add_notification":
        payload = action.get("payload", {})
        new_notifications = state.notifications.copy()
        new_notifications.append(Notification(
            notification_id=f"notif-{len(new_notifications)}",
            message=payload.get("message", ""),
            severity=payload.get("severity", "info"),
            timestamp=payload.get("timestamp", 0.0)
        ))
        return UIState(
            active_panel=state.active_panel,
            command_bar_open=state.command_bar_open,
            command_input=state.command_input,
            active_panel_id=state.active_panel_id,
            notifications=new_notifications,
            modal_open=state.modal_open,
            modal_data=state.modal_data,
            split_view=state.split_view,
            left_panel=state.left_panel,
            right_panel=state.right_panel,
            search_query=state.search_query,
            search_results=state.search_results,
            keyboard_shortcut_handlers=state.keyboard_shortcut_handlers
        )

    elif action_type == "ui/dismiss_notification":
        payload = action.get("payload", {})
        notification_id = payload.get("notification_id")
        new_notifications = state.notifications.copy()
        for notif in new_notifications:
            if notif.notification_id == notification_id:
                notif.dismissed = True
                break
        return UIState(
            active_panel=state.active_panel,
            command_bar_open=state.command_bar_open,
            command_input=state.command_input,
            active_panel_id=state.active_panel_id,
            notifications=new_notifications,
            modal_open=state.modal_open,
            modal_data=state.modal_data,
            split_view=state.split_view,
            left_panel=state.left_panel,
            right_panel=state.right_panel,
            search_query=state.search_query,
            search_results=state.search_results,
            keyboard_shortcut_handlers=state.keyboard_shortcut_handlers
        )

    elif action_type == "ui/open_modal":
        payload = action.get("payload", {})
        return UIState(
            active_panel=state.active_panel,
            command_bar_open=state.command_bar_open,
            command_input=state.command_input,
            active_panel_id=state.active_panel_id,
            notifications=state.notifications,
            modal_open=payload.get("modal_id"),
            modal_data=payload.get("data"),
            split_view=state.split_view,
            left_panel=state.left_panel,
            right_panel=state.right_panel,
            search_query=state.search_query,
            search_results=state.search_results,
            keyboard_shortcut_handlers=state.keyboard_shortcut_handlers
        )

    elif action_type == "ui/close_modal":
        return UIState(
            active_panel=state.active_panel,
            command_bar_open=state.command_bar_open,
            command_input=state.command_input,
            active_panel_id=state.active_panel_id,
            notifications=state.notifications,
            modal_open=None,
            modal_data=None,
            split_view=state.split_view,
            left_panel=state.left_panel,
            right_panel=state.right_panel,
            search_query=state.search_query,
            search_results=state.search_results,
            keyboard_shortcut_handlers=state.keyboard_shortcut_handlers
        )

    elif action_type == "ui/set_split_view":
        payload = action.get("payload", {})
        left_str = payload.get("left")
        right_str = payload.get("right")
        try:
            left = PanelId(left_str) if left_str else None
        except (ValueError, TypeError):
            left = None
        try:
            right = PanelId(right_str) if right_str else None
        except (ValueError, TypeError):
            right = None
        return UIState(
            active_panel=state.active_panel,
            command_bar_open=state.command_bar_open,
            command_input=state.command_input,
            active_panel_id=state.active_panel_id,
            notifications=state.notifications,
            modal_open=state.modal_open,
            modal_data=state.modal_data,
            split_view=payload.get("enabled", False),
            left_panel=left,
            right_panel=right,
            search_query=state.search_query,
            search_results=state.search_results,
            keyboard_shortcut_handlers=state.keyboard_shortcut_handlers
        )

    elif action_type == "ui/set_search_query":
        payload = action.get("payload", {})
        return UIState(
            active_panel=state.active_panel,
            command_bar_open=state.command_bar_open,
            command_input=state.command_input,
            active_panel_id=state.active_panel_id,
            notifications=state.notifications,
            modal_open=state.modal_open,
            modal_data=state.modal_data,
            split_view=state.split_view,
            left_panel=state.left_panel,
            right_panel=state.right_panel,
            search_query=payload.get("query", ""),
            search_results=state.search_results,
            keyboard_shortcut_handlers=state.keyboard_shortcut_handlers
        )

    elif action_type == "ui/set_search_results":
        payload = action.get("payload", {})
        return UIState(
            active_panel=state.active_panel,
            command_bar_open=state.command_bar_open,
            command_input=state.command_input,
            active_panel_id=state.active_panel_id,
            notifications=state.notifications,
            modal_open=state.modal_open,
            modal_data=state.modal_data,
            split_view=state.split_view,
            left_panel=state.left_panel,
            right_panel=state.right_panel,
            search_query=state.search_query,
            search_results=payload.get("results", []),
            keyboard_shortcut_handlers=state.keyboard_shortcut_handlers
        )

    return state
