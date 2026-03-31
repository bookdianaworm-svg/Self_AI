"""
Interactive Operations Console for Self-Improving Swarm System.

This module provides the main console interface for controlling and monitoring
the autonomous agent swarm system.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import time
import sys

from rlm.redux.store import ReduxStore, RootState, create_store, SessionPersistence
from rlm.redux.slices import (
    PanelId, UIState, UIActions,
    TaskStatus, TaskPriority, TaskEntity, TaskSubmissionDraft, TasksState, TasksActions,
    PermissionAction, PermissionType, PermissionRequest, PermissionsState, PermissionsActions,
    ToolStatus, ToolDefinition, ToolsState, ToolsActions,
    ImprovementStatus, ImprovementEntity, ImprovementsState, ImprovementsActions,
    AgentStatus, AgentEntity, AgentsState, AgentsActions,
    MessagePriority, MessageEntity, MessagesState, MessagesActions,
    SystemConfiguration, SystemState, SystemActions,
    VerificationState, VerificationActions,
    RoutingState, RoutingActions,
)
from rlm.routing.backend_router import BackendRouter, BackendMetrics
from rlm.routing.environment_router import EnvironmentRouter
from rlm.routing.task_descriptor import default_task_descriptor_fn, classify_intent, estimate_complexity


class ConsoleMode:
    TASK = "[task]"
    PERM = "[perm]"
    TOOL = "[tool]"
    IMPROVE = "[improve]"
    ROUTE = "[route]"
    VERIFY = "[verify]"
    MSG = "[msg]"
    CTRL = "[ctrl]"
    CONFIG = "[config]"
    GLOBAL = ">"


@dataclass
class CommandResult:
    success: bool
    output: str
    data: Optional[Any] = None


class InteractiveOperationsConsole:
    def __init__(self, store: Optional[ReduxStore] = None):
        self.store = store or create_store()
        self.persistence = SessionPersistence()
        self.backend_router = BackendRouter()
        self.environment_router = EnvironmentRouter()
        self.current_mode = ConsoleMode.TASK
        self.command_history: List[Tuple[ConsoleMode, str]] = []
        self._running = False
        self._auto_save_interval = 30
        self._last_save_time = time.time()

    def run(self):
        self._running = True
        print("=" * 60)
        print("Interactive Operations Console v2.0")
        print("Self-Improving Swarm System Control Panel")
        print("=" * 60)
        print("\nType 'help' for available commands, 'mode <mode>' to switch modes")
        print("Panels: task, perm, tool, improve, route, verify, msg, ctrl, config")
        print()
        self._print_prompt()

        while self._running:
            try:
                user_input = input().strip()
                if not user_input:
                    continue
                self._process_command(user_input)
                self._check_auto_save()
            except KeyboardInterrupt:
                print("\nUse 'exit' or 'quit' to stop the console.")
            except EOFError:
                break

    def _print_prompt(self):
        print(f"{self.current_mode.value} ", end="", flush=True)

    def _process_command(self, user_input: str):
        parts = user_input.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        if cmd in ("exit", "quit", "q"):
            self._running = False
            print("Shutting down console...")
            self._save_session()
            return

        if cmd == "help" or cmd == "?":
            self._print_help()
        elif cmd == "mode" and args:
            self._switch_mode(args)
        elif cmd == "save":
            self._save_session()
        elif cmd == "status":
            self._print_status()
        else:
            result = self._execute_mode_command(cmd, args)
            print(result.output)

        self._print_prompt()

    def _print_help(self):
        help_text = """
Available Commands:
  help, ?           Show this help message
  mode <mode>       Switch to mode: task, perm, tool, improve, route, verify, msg, ctrl, config
  save              Save current session
  status            Show system status
  exit, quit        Exit the console

Mode-Specific Commands:

  [task] - Task Submission Console
    submit <description>     Submit a new task
    list                    List all tasks
    cancel <task-id>         Cancel a task
    routing --backend=X --env=Y  Set routing preferences

  [perm] - Permission Request Queue
    list                    List pending permission requests
    approve <id> [Y]        Approve a request
    deny <id> [N]           Deny a request
    dont-ask-again <id> [D] Set default for this type
    always-ask <id> [A]     Never memorize for this type
    set-default --type=X --action=Y  Set default action

  [tool] - Tool Review Interface
    list                    List pending tools
    review <tool-id>         Review a specific tool
    approve <tool-id>        Approve a tool
    reject <tool-id> --reason=X  Reject a tool

  [improve] - Improvement Review System
    list                    List pending improvements
    review <id>             Review improvement
    approve <id>            Approve improvement
    reject <id> --reason=X  Reject improvement
    rollback <id>           Rollback an applied improvement

  [route] - Routing Control Panel
    list-backends           List all backends
    metrics <backend-id>     Show backend metrics
    override <id> --scope=X  Override routing decision
    show-history             Show routing history

  [verify] - Verification Control Panel
    list                     List verification queue
    submit "<theorem>"       Submit a theorem for verification
    status <theorem-id>      Check verification status
    cancel <theorem-id>      Cancel verification
    layer1-status            Show Layer1 bootstrap status

  [msg] - Agent Communication Console
    list-agents              List all agents
    thread <agent-id>         Open conversation thread
    send <agent-id> "<msg>"   Send message to agent
    broadcast "<msg>"         Broadcast to all agents

  [ctrl] - Intervention Controls
    pause --target=X [--id=Y] Pause agents
    resume --target=X [--id=Y]  Resume agents
    terminate --id=X         Terminate an agent
    stop-all                 Emergency stop
    undo                     Undo last action
    timeline                 Show intervention history

  [config] - System Configuration
    get [--key=X]            Get config value
    set --key=X --value=Y    Set config value
    export                   Export configuration
    reset                    Reset to defaults
"""
        print(help_text)

    def _switch_mode(self, mode_str: str):
        mode_map = {
            "task": ConsoleMode.TASK,
            "perm": ConsoleMode.PERM,
            "tool": ConsoleMode.TOOL,
            "improve": ConsoleMode.IMPROVE,
            "route": ConsoleMode.ROUTE,
            "verify": ConsoleMode.VERIFY,
            "msg": ConsoleMode.MSG,
            "ctrl": ConsoleMode.CTRL,
            "config": ConsoleMode.CONFIG,
        }
        mode = mode_map.get(mode_str.lower())
        if mode:
            self.current_mode = mode
            print(f"Switched to mode: {mode_str}")
        else:
            print(f"Unknown mode: {mode_str}. Available: {', '.join(mode_map.keys())}")

    def _execute_mode_command(self, cmd: str, args: str) -> CommandResult:
        if self.current_mode == ConsoleMode.TASK:
            return self._handle_task_command(cmd, args)
        elif self.current_mode == ConsoleMode.PERM:
            return self._handle_perm_command(cmd, args)
        elif self.current_mode == ConsoleMode.TOOL:
            return self._handle_tool_command(cmd, args)
        elif self.current_mode == ConsoleMode.IMPROVE:
            return self._handle_improve_command(cmd, args)
        elif self.current_mode == ConsoleMode.ROUTE:
            return self._handle_route_command(cmd, args)
        elif self.current_mode == ConsoleMode.VERIFY:
            return self._handle_verify_command(cmd, args)
        elif self.current_mode == ConsoleMode.MSG:
            return self._handle_msg_command(cmd, args)
        elif self.current_mode == ConsoleMode.CTRL:
            return self._handle_ctrl_command(cmd, args)
        elif self.current_mode == ConsoleMode.CONFIG:
            return self._handle_config_command(cmd, args)
        return CommandResult(False, "Unknown mode")

    def _handle_task_command(self, cmd: str, args: str) -> CommandResult:
        if cmd == "submit":
            return self._submit_task(args)
        elif cmd == "list":
            return self._list_tasks()
        elif cmd == "cancel":
            return self._cancel_task(args)
        elif cmd.startswith("routing"):
            return self._set_task_routing(cmd, args)
        return CommandResult(False, f"Unknown task command: {cmd}")

    def _submit_task(self, description: str) -> CommandResult:
        if not description:
            return CommandResult(False, "Task description required")
        intent = classify_intent(description)
        complexity = estimate_complexity(description, depth=1)
        routing_pref = self.store.get_state().tasks.current_draft.routing if self.store.get_state().tasks.current_draft else None
        draft = TaskSubmissionDraft(
            description=description,
            priority=TaskPriority.NORMAL,
        )
        draft.classification = type("Classification", (), {"intent": intent, "confidence": 0.8, "complexity_score": complexity})()
        self.store.dispatch(TasksActions.set_draft(draft))
        output = f"Task draft created:\n  Intent: {intent}\n  Complexity: {complexity:.2f}\n  Description: {description[:50]}..."
        return CommandResult(True, output)

    def _list_tasks(self) -> CommandResult:
        state = self.store.get_state().tasks
        if not state.tasks:
            return CommandResult(True, "No tasks found")
        lines = ["Tasks:"]
        for task_id, task in state.tasks.items():
            lines.append(f"  [{task.status.value}] {task_id}: {task.description[:40]}...")
        return CommandResult(True, "\n".join(lines))

    def _cancel_task(self, task_id: str) -> CommandResult:
        if not task_id:
            return CommandResult(False, "Task ID required")
        self.store.dispatch(TasksActions.cancel_task(task_id))
        return CommandResult(True, f"Task {task_id} cancelled")

    def _set_task_routing(self, cmd: str, args: str) -> CommandResult:
        backend = None
        env = None
        if "--backend=" in args:
            parts = args.split("--backend=")
            backend = parts[1].split()[0] if " " in parts[1] else parts[1]
        if "--env=" in args:
            env = args.split("--env=")[1].split()[0] if " " in args.split("--env=")[1] else args.split("--env=")[1]
        routing = type("Routing", (), {"backend": backend, "environment": env, "mode": None})()
        self.store.dispatch(TasksActions.set_routing_preference(routing))
        return CommandResult(True, f"Routing set: backend={backend}, env={env}")

    def _handle_perm_command(self, cmd: str, args: str) -> CommandResult:
        if cmd == "list":
            return self._list_permissions()
        elif cmd in ("approve", "y"):
            return self._approve_permission(args)
        elif cmd in ("deny", "n"):
            return self._deny_permission(args)
        elif cmd in ("dont-ask-again", "d"):
            return self._dont_ask_again(args)
        elif cmd in ("always-ask", "a"):
            return self._always_ask(args)
        elif cmd == "set-default":
            return self._set_perm_default(args)
        return CommandResult(False, f"Unknown perm command: {cmd}")

    def _list_permissions(self) -> CommandResult:
        state = self.store.get_state().permissions
        if not state.pending_requests:
            return CommandResult(True, "No pending permission requests")
        lines = ["Pending Permission Requests:"]
        for req in state.pending_requests:
            lines.append(f"  [{req.request_id}] {req.permission_type.value}: {req.description[:40]}...")
        return CommandResult(True, "\n".join(lines))

    def _approve_permission(self, request_id: str) -> CommandResult:
        self.store.dispatch(PermissionsActions.approve_request(request_id))
        return CommandResult(True, f"Request {request_id} approved")

    def _deny_permission(self, request_id: str, reason: str = None) -> CommandResult:
        self.store.dispatch(PermissionsActions.deny_request(request_id, reason))
        return CommandResult(True, f"Request {request_id} denied")

    def _dont_ask_again(self, request_id: str) -> CommandResult:
        self.store.dispatch(PermissionsActions.approve_request(request_id, remember=True))
        return CommandResult(True, f"Request {request_id} approved and type will not be asked again")

    def _always_ask(self, request_id: str) -> CommandResult:
        return CommandResult(True, f"Request {request_id}: will always ask for this type")

    def _set_perm_default(self, args: str) -> CommandResult:
        perm_type = None
        action = None
        if "--type=" in args:
            perm_type = args.split("--type=")[1].split()[0]
        if "--action=" in args:
            action = args.split("--action=")[1].split()[0]
        if perm_type and action:
            self.store.dispatch(PermissionsActions.set_default(perm_type, PermissionAction(action)))
            return CommandResult(True, f"Default for {perm_type} set to {action}")
        return CommandResult(False, "Usage: set-default --type=<type> --action=<action>")

    def _handle_tool_command(self, cmd: str, args: str) -> CommandResult:
        if cmd == "list":
            return self._list_tools()
        elif cmd == "review":
            return self._review_tool(args)
        elif cmd == "approve":
            return self._approve_tool(args)
        elif cmd == "reject":
            reason = ""
            if "--reason=" in args:
                reason = args.split("--reason=")[1]
            return self._reject_tool(args.split()[0] if args else "", reason)
        return CommandResult(False, f"Unknown tool command: {cmd}")

    def _list_tools(self) -> CommandResult:
        state = self.store.get_state().tools
        if not state.pending_tools:
            return CommandResult(True, "No pending tools")
        lines = ["Pending Tools:"]
        for tool in state.pending_tools:
            lines.append(f"  [{tool.tool_id}] {tool.name} by {tool.created_by}")
        return CommandResult(True, "\n".join(lines))

    def _review_tool(self, tool_id: str) -> CommandResult:
        return CommandResult(True, f"Tool {tool_id} review details not yet implemented")

    def _approve_tool(self, tool_id: str) -> CommandResult:
        self.store.dispatch(ToolsActions.approve_tool(tool_id))
        return CommandResult(True, f"Tool {tool_id} approved")

    def _reject_tool(self, tool_id: str, reason: str) -> CommandResult:
        self.store.dispatch(ToolsActions.reject_tool(tool_id, reason))
        return CommandResult(True, f"Tool {tool_id} rejected: {reason}")

    def _handle_improve_command(self, cmd: str, args: str) -> CommandResult:
        if cmd == "list":
            return self._list_improvements()
        elif cmd == "review":
            return CommandResult(True, f"Review for {args}")
        elif cmd == "approve":
            self.store.dispatch(ImprovementsActions.approve_improvement(args))
            return CommandResult(True, f"Improvement {args} approved")
        elif cmd == "reject":
            reason = ""
            if "--reason=" in args:
                reason = args.split("--reason=")[1]
            self.store.dispatch(ImprovementsActions.reject_improvement(args, reason))
            return CommandResult(True, f"Improvement {args} rejected")
        elif cmd == "rollback":
            self.store.dispatch(ImprovementsActions.rollback_improvement(args))
            return CommandResult(True, f"Improvement {args} rolled back")
        return CommandResult(False, f"Unknown improve command: {cmd}")

    def _list_improvements(self) -> CommandResult:
        state = self.store.get_state().improvements
        if not state.pending_approvals:
            return CommandResult(True, "No pending improvements")
        lines = ["Pending Improvements:"]
        for imp in state.pending_approvals:
            lines.append(f"  [{imp.improvement_id}] {imp.title}")
        return CommandResult(True, "\n".join(lines))

    def _handle_route_command(self, cmd: str, args: str) -> CommandResult:
        if cmd == "list-backends":
            return self._list_backends()
        elif cmd == "metrics":
            return self._show_backend_metrics(args)
        elif cmd == "override":
            return CommandResult(True, f"Override: {args}")
        elif cmd == "show-history":
            return self._show_routing_history()
        return CommandResult(False, f"Unknown route command: {cmd}")

    def _list_backends(self) -> CommandResult:
        state = self.store.get_state().routing
        lines = ["Available Backends:"]
        for backend_id in state.backend_metrics:
            lines.append(f"  {backend_id}")
        return CommandResult(True, "\n".join(lines) if len(lines) > 1 else "No backends configured")

    def _show_backend_metrics(self, backend_id: str) -> CommandResult:
        metrics = self.backend_router.get_backend_metrics(backend_id)
        if metrics:
            return CommandResult(True, f"Metrics for {backend_id}:\n  Total calls: {metrics.total_calls}\n  Successful: {metrics.successful_calls}\n  Avg latency: {metrics.avg_latency_ms:.2f}ms")
        return CommandResult(False, f"No metrics for backend: {backend_id}")

    def _show_routing_history(self) -> CommandResult:
        state = self.store.get_state().routing
        lines = ["Routing History:"]
        for decision_id, decision in list(state.decisions.items())[-10:]:
            lines.append(f"  [{decision_id}] {decision.decision_type.value}: {decision.selected}")
        return CommandResult(True, "\n".join(lines) if len(lines) > 1 else "No routing history")

    def _handle_verify_command(self, cmd: str, args: str) -> CommandResult:
        if cmd == "list":
            return self._list_verifications()
        elif cmd == "submit":
            return CommandResult(True, f"Submit theorem: {args}")
        elif cmd == "status":
            return self._verify_status(args)
        elif cmd == "cancel":
            return CommandResult(True, f"Cancelled: {args}")
        elif cmd == "layer1-status":
            return self._layer1_status()
        return CommandResult(False, f"Unknown verify command: {cmd}")

    def _list_verifications(self) -> CommandResult:
        state = self.store.get_state().verification
        lines = ["Verification Queue:"]
        for theorem_id, theorem in state.theorems.items():
            lines.append(f"  [{theorem.status.value}] {theorem_id}")
        return CommandResult(True, "\n".join(lines) if len(lines) > 1 else "Queue empty")

    def _verify_status(self, theorem_id: str) -> CommandResult:
        state = self.store.get_state().verification
        if theorem_id in state.theorems:
            t = state.theorems[theorem_id]
            return CommandResult(True, f"Status: {t.status.value}, Attempts: {t.proof_attempts}")
        return CommandResult(False, f"Theorem {theorem_id} not found")

    def _layer1_status(self) -> CommandResult:
        state = self.store.get_state().verification
        layer1 = state.layer1
        return CommandResult(True, f"Layer1 Status: {layer1.status.value}\n  Mathlib: {layer1.mathlib_version}\n  Physlib: {layer1.physlib_version}")

    def _handle_msg_command(self, cmd: str, args: str) -> CommandResult:
        if cmd == "list-agents":
            return self._list_agents()
        elif cmd == "thread":
            return CommandResult(True, f"Thread: {args}")
        elif cmd == "send":
            parts = args.split(maxsplit=1)
            agent_id = parts[0] if len(parts) > 0 else ""
            message = parts[1] if len(parts) > 1 else ""
            self.store.dispatch(MessagesActions.send_message(agent_id, message))
            return CommandResult(True, f"Message sent to {agent_id}")
        elif cmd == "broadcast":
            self.store.dispatch(MessagesActions.broadcast_message(args))
            return CommandResult(True, "Broadcast sent")
        return CommandResult(False, f"Unknown msg command: {cmd}")

    def _list_agents(self) -> CommandResult:
        state = self.store.get_state().agents
        lines = ["Active Agents:"]
        for agent_id, agent in state.agents.items():
            lines.append(f"  [{agent.status.value}] {agent_id}: {agent.name}")
        return CommandResult(True, "\n".join(lines) if len(lines) > 1 else "No agents")

    def _handle_ctrl_command(self, cmd: str, args: str) -> CommandResult:
        if cmd == "pause":
            target = "all"
            target_id = None
            if "--target=" in args:
                target = args.split("--target=")[1].split()[0]
            if "--id=" in args:
                target_id = args.split("--id=")[1].split()[0]
            self.store.dispatch(AgentsActions.pause_agent(target, target_id))
            return CommandResult(True, f"Paused: target={target}, id={target_id}")
        elif cmd == "resume":
            target = "all"
            target_id = None
            if "--target=" in args:
                target = args.split("--target=")[1].split()[0]
            if "--id=" in args:
                target_id = args.split("--id=")[1].split()[0]
            self.store.dispatch(AgentsActions.resume_agent(target, target_id))
            return CommandResult(True, f"Resumed: target={target}, id={target_id}")
        elif cmd == "terminate":
            agent_id = args.split("--id=")[1].split()[0] if "--id=" in args else args
            self.store.dispatch(AgentsActions.terminate_agent(agent_id))
            return CommandResult(True, f"Terminated: {agent_id}")
        elif cmd == "stop-all":
            self.store.dispatch(AgentsActions.emergency_stop())
            return CommandResult(True, "EMERGENCY STOP: All agents paused")
        elif cmd == "undo":
            self.store.dispatch(AgentsActions.undo_last_action())
            return CommandResult(True, "Undo performed")
        elif cmd == "timeline":
            return self._show_timeline()
        return CommandResult(False, f"Unknown ctrl command: {cmd}")

    def _show_timeline(self) -> CommandResult:
        state = self.store.get_state().agents
        lines = ["Intervention Timeline:"]
        for record in state.timeline[-10:]:
            lines.append(f"  [{record.action_type.value}] {record.target_type}: {record.target_id}")
        return CommandResult(True, "\n".join(lines) if len(lines) > 1 else "No interventions")

    def _handle_config_command(self, cmd: str, args: str) -> CommandResult:
        if cmd == "get":
            key = None
            if "--key=" in args:
                key = args.split("--key=")[1].split()[0]
            return self._get_config(key)
        elif cmd == "set":
            key = None
            value = None
            if "--key=" in args:
                key = args.split("--key=")[1].split()[0]
            if "--value=" in args:
                value = args.split("--value=")[1].split()[0]
            if key and value:
                self.store.dispatch(SystemActions.update_configuration(key, value))
                return CommandResult(True, f"Set {key} = {value}")
            return CommandResult(False, "Usage: set --key=<path> --value=<value>")
        elif cmd == "export":
            return self._export_config()
        elif cmd == "reset":
            self.store.dispatch(SystemActions.reset_configuration())
            return CommandResult(True, "Configuration reset to defaults")
        return CommandResult(False, f"Unknown config command: {cmd}")

    def _get_config(self, key: Optional[str]) -> CommandResult:
        state = self.store.get_state().system.config
        if key:
            return CommandResult(True, f"Config {key}: <value>")
        return CommandResult(True, f"Config: {state}")

    def _export_config(self) -> CommandResult:
        return CommandResult(True, "Export configuration to file")

    def _print_status(self):
        state = self.store.get_state()
        print("\n--- System Status ---")
        print(f"Active Agents: {len(state.agents.agents)}")
        print(f"Paused Agents: {len(state.agents.paused_agents)}")
        print(f"Pending Tasks: {len(state.tasks.task_queue)}")
        print(f"Pending Permissions: {len(state.permissions.pending_requests)}")
        print(f"Pending Tools: {len(state.tools.pending_tools)}")
        print(f"Verification Status: {state.verification.layer1.status.value}")

    def _save_session(self):
        session_id = SessionPersistence.generate_session_id()
        self.persistence.save_session(session_id, self.store.get_state())
        print(f"Session saved: {session_id}")

    def _check_auto_save(self):
        if time.time() - self._last_save_time > self._auto_save_interval:
            self._save_session()
            self._last_save_time = time.time()

    def dispatch(self, action: Dict[str, Any]):
        self.store.dispatch(action)


def create_console(store: Optional[ReduxStore] = None) -> InteractiveOperationsConsole:
    return InteractiveOperationsConsole(store)
