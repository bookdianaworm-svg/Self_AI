"""
WebSocket Bridge for connecting UI to backend systems.

This module provides the bridge between the WebSocket server
and the rest of the RLM system (agents, messaging, etc.).
"""

import asyncio
import json
import threading
from typing import Any, Callable, Dict, List, Optional

from rlm.agents.manager import AgentManager
from rlm.console.websocket import WebSocketServer, WebSocketClient
from rlm.messaging.message_broker import MessageBroker
from rlm.messaging.message_types import Message, MessageContent, MessageType


class WebSocketBridge:
    """
    Bridge connecting WebSocket server to backend systems.

    This class integrates:
    - Agent management (create, monitor agents)
    - Message broker (route messages to/from UI)
    - State synchronization
    """

    def __init__(
        self,
        ws_server: WebSocketServer,
        agent_manager: Optional[AgentManager] = None,
        message_broker: Optional[MessageBroker] = None,
    ):
        """
        Initialize the WebSocket bridge.

        Args:
            ws_server: WebSocket server instance.
            agent_manager: Optional agent manager.
            message_broker: Optional message broker.
        """
        self._ws_server = ws_server
        self._agent_manager = agent_manager
        self._message_broker = message_broker
        self._lock = threading.Lock()
        self._callbacks: Dict[str, List[Callable]] = {}

        # Subscribe to WebSocket events
        self._ws_server.subscribe("dispatch", self._handle_dispatch)
        self._ws_server.subscribe("agent/*", self._handle_agent_message)
        self._ws_server.subscribe("message/*", self._handle_message)

    def set_agent_manager(self, agent_manager: AgentManager) -> None:
        """Set the agent manager."""
        self._agent_manager = agent_manager

    def set_message_broker(self, message_broker: MessageBroker) -> None:
        """Set the message broker."""
        self._message_broker = message_broker

    def on_event(self, event_type: str, callback: Callable) -> None:
        """
        Register a callback for an event type.

        Args:
            event_type: Type of event (e.g., "agent_created", "message_sent").
            callback: Callback function.
        """
        if event_type not in self._callbacks:
            self._callbacks[event_type] = []
        self._callbacks[event_type].append(callback)

    def _notify_callbacks(self, event_type: str, data: Dict[str, Any]) -> None:
        """Notify registered callbacks of an event."""
        if event_type in self._callbacks:
            for callback in self._callbacks[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in callback for {event_type}: {e}")

    def _handle_dispatch(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle Redux dispatch from UI."""
        action = data.get("action", {})
        action_type = action.get("type", "")

        # Route based on action type
        if action_type.startswith("agent/"):
            self._handle_agent_action(action)
        elif action_type.startswith("message/"):
            self._handle_message_action(action)
        elif action_type.startswith("system/"):
            self._handle_system_action(action)

        self._notify_callbacks("dispatch", {"action": action})

    def _handle_agent_action(self, action: Dict[str, Any]) -> None:
        """Handle agent-related actions."""
        if not self._agent_manager:
            return

        action_type = action.get("type", "")
        payload = action.get("payload", {})

        if action_type == "agent/create":
            task = payload.get("task", "")
            agent_id = self._agent_manager.create_agent(task)
            self.broadcast_agent_update(agent_id)

        elif action_type == "agent/terminate":
            agent_id = payload.get("agentId")
            if agent_id:
                self._agent_manager.terminate_agent(agent_id)

        elif action_type == "agent/terminate_all":
            self._agent_manager.terminate_all_agents()

    def _handle_message_action(self, action: Dict[str, Any]) -> None:
        """Handle message-related actions."""
        if not self._message_broker:
            return

        action_type = action.get("type", "")
        payload = action.get("payload", {})

        if action_type == "message/send":
            message_data = payload.get("message", {})
            message = Message.from_dict(message_data)
            self._message_broker.send_message(message)

    def _handle_system_action(self, action: Dict[str, Any]) -> None:
        """Handle system-related actions."""
        action_type = action.get("type", "")

        if action_type == "system/broadcast":
            self.broadcast_state()

    def _handle_agent_message(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle agent-related messages from UI."""
        self._notify_callbacks(event_type, data)

    def _handle_message(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle message-related messages from UI."""
        self._notify_callbacks(event_type, data)

    def broadcast_agent_update(self, agent_id: str) -> None:
        """
        Broadcast an agent state update to all connected clients.

        Args:
            agent_id: ID of the agent to broadcast.
        """
        if not self._agent_manager:
            return

        agent = self._agent_manager.get_agent(agent_id)
        if not agent:
            return

        update = {
            "type": "agent/update",
            "payload": {"agentId": agent_id, "info": agent.get_info()},
        }
        self._ws_server.broadcast("agents", update)

    def broadcast_agents_list(self) -> None:
        """Broadcast the list of all agents."""
        if not self._agent_manager:
            return

        agents = self._agent_manager.get_all_agents()
        update = {
            "type": "agents/list",
            "payload": {
                "agents": {
                    agent_id: agent.get_info() for agent_id, agent in agents.items()
                },
                "stats": self._agent_manager.get_info(),
            },
        }
        self._ws_server.broadcast("agents", update)

    def broadcast_state(self) -> None:
        """Broadcast current system state."""
        state = self.get_state()
        update = {"type": "state/snapshot", "payload": state}
        self._ws_server.broadcast("state", update)

    def broadcast_message(self, message: Message) -> None:
        """
        Broadcast a message to UI.

        Args:
            message: Message to broadcast.
        """
        update = {"type": "message/new", "payload": {"message": message.to_dict()}}
        self._ws_server.broadcast("messages", update)

    def get_state(self) -> Dict[str, Any]:
        """
        Get current system state for UI.

        Returns:
            Dictionary containing current state.
        """
        state = {
            "agents": {},
            "messages": {},
        }

        if self._agent_manager:
            state["agents"] = {
                agent_id: agent.get_info()
                for agent_id, agent in self._agent_manager.get_all_agents().items()
            }
            state["agentStats"] = self._agent_manager.get_info()

        if self._message_broker:
            state["messageStats"] = self._message_broker.get_stats()

        return state

    def start_agent(self, task: str, callback: Optional[Callable] = None) -> str:
        """
        Start a new agent and return its ID.

        Args:
            task: Task description for the agent.
            callback: Optional callback when agent completes.

        Returns:
            The agent ID.
        """
        if not self._agent_manager:
            raise RuntimeError("Agent manager not set")

        agent_id = self._agent_manager.create_agent(task, callback=callback)
        self.broadcast_agents_list()
        return agent_id

    def send_user_message(
        self, recipient_id: str, content: str, title: str = ""
    ) -> bool:
        """
        Send a message from user to an agent.

        Args:
            recipient_id: ID of the recipient agent.
            content: Message content.
            title: Optional message title.

        Returns:
            True if sent successfully.
        """
        if not self._message_broker:
            return False

        message = Message(
            sender="user",
            recipients=[recipient_id],
            type=MessageType.QUERY,
            content=MessageContent(title=title, body=content),
        )

        return self._message_broker.send_message(message)

    def handle_user_broadcast(self, content: str, title: str = "") -> bool:
        """
        Handle a broadcast message from user.

        Args:
            content: Broadcast content.
            title: Optional broadcast title.

        Returns:
            True if broadcast sent.
        """
        if not self._message_broker:
            return False

        message = Message(
            sender="user",
            recipients=["all"],
            type=MessageType.BROADCAST,
            content=MessageContent(title=title, body=content),
        )

        return self._message_broker.send_message(message)


class WebSocketBridgeManager:
    """
    Manager for WebSocket bridges.

    This class manages multiple WebSocket bridges,
    useful for multi-tenant scenarios.
    """

    def __init__(self):
        """Initialize the bridge manager."""
        self._bridges: Dict[str, WebSocketBridge] = {}
        self._lock = threading.Lock()

    def create_bridge(
        self, bridge_id: str, ws_server: WebSocketServer
    ) -> WebSocketBridge:
        """
        Create a new bridge.

        Args:
            bridge_id: Unique identifier for the bridge.
            ws_server: WebSocket server for the bridge.

        Returns:
            The created bridge.
        """
        with self._lock:
            if bridge_id in self._bridges:
                raise ValueError(f"Bridge {bridge_id} already exists")

            bridge = WebSocketBridge(ws_server)
            self._bridges[bridge_id] = bridge
            return bridge

    def get_bridge(self, bridge_id: str) -> Optional[WebSocketBridge]:
        """
        Get a bridge by ID.

        Args:
            bridge_id: ID of the bridge.

        Returns:
            The bridge or None if not found.
        """
        return self._bridges.get(bridge_id)

    def remove_bridge(self, bridge_id: str) -> bool:
        """
        Remove a bridge.

        Args:
            bridge_id: ID of the bridge to remove.

        Returns:
            True if removed, False if not found.
        """
        with self._lock:
            if bridge_id in self._bridges:
                del self._bridges[bridge_id]
                return True
            return False

    def get_all_bridges(self) -> Dict[str, WebSocketBridge]:
        """Get all bridges."""
        return dict(self._bridges)
