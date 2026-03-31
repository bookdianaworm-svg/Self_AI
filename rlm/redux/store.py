"""
Redux store for the Interactive Operations Console.

This module provides a unified Redux store that combines all slices
for managing the state of the autonomous agent swarm system.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
import time
import json
import os

from rlm.redux.slices import (
    VerificationState,
    RoutingState,
    TasksState,
    PermissionsState,
    ToolsState,
    ImprovementsState,
    AgentsState,
    MessagesState,
    SystemState,
    UIState,
    verification_reducer,
    routing_reducer,
    tasks_reducer,
    permissions_reducer,
    tools_reducer,
    improvements_reducer,
    agents_reducer,
    messages_reducer,
    system_reducer,
    ui_reducer,
)
from rlm.redux.slices.agent_loop_slice import (
    AgentLoopState,
    AgentLoopSlice,
    AgentLoopActions,
    agent_loop_reducer,
)


@dataclass
class RootState:
    verification: VerificationState = field(default_factory=VerificationState)
    routing: RoutingState = field(default_factory=RoutingState)
    tasks: TasksState = field(default_factory=TasksState)
    permissions: PermissionsState = field(default_factory=PermissionsState)
    tools: ToolsState = field(default_factory=ToolsState)
    improvements: ImprovementsState = field(default_factory=ImprovementsState)
    agents: AgentsState = field(default_factory=AgentsState)
    messages: MessagesState = field(default_factory=MessagesState)
    system: SystemState = field(default_factory=SystemState)
    ui: UIState = field(default_factory=UIState)
    agent_loop: AgentLoopSlice = field(default_factory=AgentLoopSlice)


class ReduxStore:
    def __init__(self, preloaded_state: Optional[RootState] = None):
        self.state = preloaded_state or RootState()
        self._listeners: List[Callable[[RootState], None]] = []
        self._dispatch_handlers: Dict[str, Callable[..., Any]] = {
            "verification/load_layer1_request": lambda s, a: verification_reducer(
                s.verification, a
            ),
            "verification/load_layer1_success": lambda s, a: verification_reducer(
                s.verification, a
            ),
            "verification/load_layer1_failure": lambda s, a: verification_reducer(
                s.verification, a
            ),
            "verification/verify_theorem_request": lambda s, a: verification_reducer(
                s.verification, a
            ),
            "verification/verify_theorem_success": lambda s, a: verification_reducer(
                s.verification, a
            ),
            "verification/verify_theorem_failure": lambda s, a: verification_reducer(
                s.verification, a
            ),
            "routing/decision_made": lambda s, a: self._update(
                s, "routing", routing_reducer(s.routing, a)
            ),
            "routing/started": lambda s, a: self._update(
                s, "routing", routing_reducer(s.routing, a)
            ),
            "routing/completed": lambda s, a: self._update(
                s, "routing", routing_reducer(s.routing, a)
            ),
            "routing/backend_metrics_updated": lambda s, a: self._update(
                s, "routing", routing_reducer(s.routing, a)
            ),
            "tasks/submit_task": lambda s, a: self._update(
                s, "tasks", tasks_reducer(s.tasks, a)
            ),
            "tasks/update_status": lambda s, a: self._update(
                s, "tasks", tasks_reducer(s.tasks, a)
            ),
            "tasks/set_draft": lambda s, a: self._update(
                s, "tasks", tasks_reducer(s.tasks, a)
            ),
            "tasks/clear_draft": lambda s, a: self._update(
                s, "tasks", tasks_reducer(s.tasks, a)
            ),
            "tasks/set_routing_preference": lambda s, a: self._update(
                s, "tasks", tasks_reducer(s.tasks, a)
            ),
            "tasks/set_constraints": lambda s, a: self._update(
                s, "tasks", tasks_reducer(s.tasks, a)
            ),
            "tasks/cancel_task": lambda s, a: self._update(
                s, "tasks", tasks_reducer(s.tasks, a)
            ),
            "permissions/approve_request": lambda s, a: self._update(
                s, "permissions", permissions_reducer(s.permissions, a)
            ),
            "permissions/deny_request": lambda s, a: self._update(
                s, "permissions", permissions_reducer(s.permissions, a)
            ),
            "permissions/set_default": lambda s, a: self._update(
                s, "permissions", permissions_reducer(s.permissions, a)
            ),
            "permissions/set_default_scope": lambda s, a: self._update(
                s, "permissions", permissions_reducer(s.permissions, a)
            ),
            "permissions/add_request": lambda s, a: self._update(
                s, "permissions", permissions_reducer(s.permissions, a)
            ),
            "permissions/clear_history": lambda s, a: self._update(
                s, "permissions", permissions_reducer(s.permissions, a)
            ),
            "tools/approve_tool": lambda s, a: self._update(
                s, "tools", tools_reducer(s.tools, a)
            ),
            "tools/reject_tool": lambda s, a: self._update(
                s, "tools", tools_reducer(s.tools, a)
            ),
            "tools/set_tool_default": lambda s, a: self._update(
                s, "tools", tools_reducer(s.tools, a)
            ),
            "tools/add_tool": lambda s, a: self._update(
                s, "tools", tools_reducer(s.tools, a)
            ),
            "tools/sandbox_test": lambda s, a: self._update(
                s, "tools", tools_reducer(s.tools, a)
            ),
            "improvements/approve_improvement": lambda s, a: self._update(
                s, "improvements", improvements_reducer(s.improvements, a)
            ),
            "improvements/reject_improvement": lambda s, a: self._update(
                s, "improvements", improvements_reducer(s.improvements, a)
            ),
            "improvements/rollback_improvement": lambda s, a: self._update(
                s, "improvements", improvements_reducer(s.improvements, a)
            ),
            "improvements/set_default": lambda s, a: self._update(
                s, "improvements", improvements_reducer(s.improvements, a)
            ),
            "improvements/add_improvement": lambda s, a: self._update(
                s, "improvements", improvements_reducer(s.improvements, a)
            ),
            "agents/pause_agent": lambda s, a: self._update(
                s, "agents", agents_reducer(s.agents, a)
            ),
            "agents/resume_agent": lambda s, a: self._update(
                s, "agents", agents_reducer(s.agents, a)
            ),
            "agents/terminate_agent": lambda s, a: self._update(
                s, "agents", agents_reducer(s.agents, a)
            ),
            "agents/emergency_stop": lambda s, a: self._update(
                s, "agents", agents_reducer(s.agents, a)
            ),
            "agents/undo": lambda s, a: self._update(
                s, "agents", agents_reducer(s.agents, a)
            ),
            "agents/add_agent": lambda s, a: self._update(
                s, "agents", agents_reducer(s.agents, a)
            ),
            "agents/update_status": lambda s, a: self._update(
                s, "agents", agents_reducer(s.agents, a)
            ),
            "messages/send_message": lambda s, a: self._update(
                s, "messages", messages_reducer(s.messages, a)
            ),
            "messages/broadcast_message": lambda s, a: self._update(
                s, "messages", messages_reducer(s.messages, a)
            ),
            "messages/mark_read": lambda s, a: self._update(
                s, "messages", messages_reducer(s.messages, a)
            ),
            "messages/archive_thread": lambda s, a: self._update(
                s, "messages", messages_reducer(s.messages, a)
            ),
            "messages/receive_message": lambda s, a: self._update(
                s, "messages", messages_reducer(s.messages, a)
            ),
            "messages/set_retention": lambda s, a: self._update(
                s, "messages", messages_reducer(s.messages, a)
            ),
            "system/update_configuration": lambda s, a: self._update(
                s, "system", system_reducer(s.system, a)
            ),
            "system/reset_configuration": lambda s, a: self._update(
                s, "system", system_reducer(s.system, a)
            ),
            "system/export_configuration": lambda s, a: self._update(
                s, "system", system_reducer(s.system, a)
            ),
            "system/import_configuration": lambda s, a: self._update(
                s, "system", system_reducer(s.system, a)
            ),
            "system/set_session_id": lambda s, a: self._update(
                s, "system", system_reducer(s.system, a)
            ),
            "system/set_pending_change": lambda s, a: self._update(
                s, "system", system_reducer(s.system, a)
            ),
            "system/clear_pending_changes": lambda s, a: self._update(
                s, "system", system_reducer(s.system, a)
            ),
            "ui/set_active_panel": lambda s, a: self._update(
                s, "ui", ui_reducer(s.ui, a)
            ),
            "ui/open_command_bar": lambda s, a: self._update(
                s, "ui", ui_reducer(s.ui, a)
            ),
            "ui/close_command_bar": lambda s, a: self._update(
                s, "ui", ui_reducer(s.ui, a)
            ),
            "ui/set_command_input": lambda s, a: self._update(
                s, "ui", ui_reducer(s.ui, a)
            ),
            "ui/add_notification": lambda s, a: self._update(
                s, "ui", ui_reducer(s.ui, a)
            ),
            "ui/dismiss_notification": lambda s, a: self._update(
                s, "ui", ui_reducer(s.ui, a)
            ),
            "ui/open_modal": lambda s, a: self._update(s, "ui", ui_reducer(s.ui, a)),
            "ui/close_modal": lambda s, a: self._update(s, "ui", ui_reducer(s.ui, a)),
            "ui/set_split_view": lambda s, a: self._update(
                s, "ui", ui_reducer(s.ui, a)
            ),
            "ui/set_search_query": lambda s, a: self._update(
                s, "ui", ui_reducer(s.ui, a)
            ),
            "ui/set_search_results": lambda s, a: self._update(
                s, "ui", ui_reducer(s.ui, a)
            ),
            "agent_loop/register_agent": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/unregister_agent": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/set_active_agent": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/update_status": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/update_task": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/llm_call_started": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/llm_call_completed": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/repl_execution_started": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/repl_execution_completed": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/iteration_started": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/iteration_completed": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/agent_spawned": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/chain_thought_added": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/set_streaming_mode": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/pause_streaming": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/resume_streaming": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
            "agent_loop/clear_history": lambda s, a: self._update(
                s, "agent_loop", agent_loop_reducer(s.agent_loop, a)
            ),
        }

    def _update(
        self, state: RootState, slice_name: str, new_slice_state: Any
    ) -> RootState:
        setattr(state, slice_name, new_slice_state)
        return state

    def dispatch(self, action: Dict[str, Any]) -> RootState:
        action_type = action.get("type", "")
        handler = self._dispatch_handlers.get(action_type)
        if handler:
            self.state = handler(self.state, action)
        self._notify_listeners()
        return self.state

    def get_state(self) -> RootState:
        return self.state

    def subscribe(self, listener: Callable[[RootState], None]) -> Callable[[], None]:
        self._listeners.append(listener)

        def unsubscribe():
            self._listeners.remove(listener)

        return unsubscribe

    def _notify_listeners(self):
        for listener in self._listeners:
            listener(self.state)


class SessionPersistence:
    def __init__(self, session_dir: str = ".sessions"):
        self.session_dir = session_dir
        os.makedirs(session_dir, exist_ok=True)

    def _get_session_path(self, session_id: str) -> str:
        return os.path.join(self.session_dir, f"{session_id}.json")

    def save_session(self, session_id: str, state: RootState) -> None:
        path = self._get_session_path(session_id)
        state_dict = {
            "verification": vars(state.verification),
            "routing": vars(state.routing),
            "tasks": vars(state.tasks),
            "permissions": vars(state.permissions),
            "tools": vars(state.tools),
            "improvements": vars(state.improvements),
            "agents": vars(state.agents),
            "messages": vars(state.messages),
            "system": vars(state.system),
            "ui": vars(state.ui),
        }
        with open(path, "w") as f:
            json.dump(state_dict, f)

    def load_session(self, session_id: str) -> Optional[RootState]:
        path = self._get_session_path(session_id)
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            state_dict = json.load(f)
        return RootState(
            verification=VerificationState(**state_dict.get("verification", {})),
            routing=RoutingState(**state_dict.get("routing", {})),
            tasks=TasksState(**state_dict.get("tasks", {})),
            permissions=PermissionsState(**state_dict.get("permissions", {})),
            tools=ToolsState(**state_dict.get("tools", {})),
            improvements=ImprovementsState(**state_dict.get("improvements", {})),
            agents=AgentsState(**state_dict.get("agents", {})),
            messages=MessagesState(**state_dict.get("messages", {})),
            system=SystemState(**state_dict.get("system", {})),
            ui=UIState(**state_dict.get("ui", {})),
        )

    def list_sessions(self) -> List[str]:
        if not os.path.exists(self.session_dir):
            return []
        return [
            f.replace(".json", "")
            for f in os.listdir(self.session_dir)
            if f.endswith(".json")
        ]

    def delete_session(self, session_id: str) -> None:
        path = self._get_session_path(session_id)
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def generate_session_id() -> str:
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d--%H-%M-%S")


def create_store(preloaded_state: Optional[RootState] = None) -> ReduxStore:
    return ReduxStore(preloaded_state)
