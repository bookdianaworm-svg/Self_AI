#!/usr/bin/env python3
"""
Console Server - Full Self_AI Backend with WebSocket + Redux State Management.

This server properly integrates with the existing architecture:
1. WebSocket server for UI communication
2. WebSocketBridge connecting to backend systems
3. AgentManager for task/agent management
4. MessageBroker for inter-agent messaging
5. Redux store for state synchronization

This is designed to handle complex multi-turn multi-agent recursive tasks.
"""

import asyncio
import signal
import threading
import time
from typing import Any, Dict, Optional

from rlm.console.websocket import WebSocketServer, create_websocket_server
from rlm.console.ws_bridge import WebSocketBridge
from rlm.agents.manager import AgentManager
from rlm.messaging.message_broker import MessageBroker
from rlm.app.orchestrator import Orchestrator, SystemStatus
from rlm.redux.store import create_store, ReduxStore


class ConsoleServer:
    """
    Full console server integrating all backend systems.
    
    This server connects the UI to the core RLM system through:
    - WebSocketServer: Real-time UI communication
    - WebSocketBridge: Message routing and event handling
    - AgentManager: Task execution and agent lifecycle
    - MessageBroker: Inter-agent communication
    - Orchestrator: System lifecycle and state coordination
    """
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.ws_server: Optional[WebSocketServer] = None
        self.ws_bridge: Optional[WebSocketBridge] = None
        self.agent_manager: Optional[AgentManager] = None
        self.message_broker: Optional[MessageBroker] = None
        self.orchestrator: Optional[Orchestrator] = None
        self.store: Optional[ReduxStore] = None
        self._running = False
        self._lock = threading.Lock()

    async def start(self):
        """Start the console server and all subsystems."""
        print("=" * 70)
        print("  Self_AI Console Server")
        print("  Multi-Agent Recursive Language Model System")
        print("=" * 70)
        print()
        
        # Step 1: Initialize Redux store for state management
        print("[1/5] Initializing Redux store...")
        self.store = create_store()
        print("      ✓ Redux store initialized")
        
        # Step 2: Initialize orchestrator for system lifecycle
        print("[2/5] Initializing orchestrator...")
        self.orchestrator = Orchestrator(store=self.store)
        self.orchestrator.start()
        print("      ✓ Orchestrator started")
        
        # Step 3: Initialize agent manager for task execution
        print("[3/5] Initializing agent manager...")
        self.agent_manager = AgentManager()
        self.agent_manager.start()
        print("      ✓ Agent manager initialized")
        
        # Step 4: Initialize message broker for inter-agent messaging
        print("[4/5] Initializing message broker...")
        self.message_broker = MessageBroker()
        self.message_broker.start()
        print("      ✓ Message broker initialized")
        
        # Step 5: Create WebSocket server and bridge
        print("[5/5] Starting WebSocket server...")
        self.ws_server = create_websocket_server(host=self.host, port=self.port)
        
        # Create the bridge connecting WebSocket to backend systems
        self.ws_bridge = WebSocketBridge(
            ws_server=self.ws_server,
            agent_manager=self.agent_manager,
            message_broker=self.message_broker,
        )
        
        # Register state broadcast callback on agent updates
        self.ws_bridge.on_event("agent_update", lambda data: self._broadcast_state())
        self.ws_bridge.on_event("message_sent", lambda data: self._broadcast_messages())
        
        print(f"      ✓ WebSocket server on ws://{self.host}:{self.port}")
        
        print()
        print("=" * 70)
        print(f"  Server running at ws://{self.host}:{self.port}")
        print("  Waiting for UI connections...")
        print("=" * 70)
        print()
        
        self._running = True
        
        # Start the WebSocket server
        try:
            await self.ws_server.start()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            await self.stop()

    def _broadcast_state(self):
        """Broadcast current system state to all UI clients."""
        if not self.ws_server:
            return
        
        state = self.ws_bridge.get_state() if self.ws_bridge else {}
        
        # Broadcast state for each panel
        asyncio.create_task(self.ws_server.broadcast("agents", {
            "agents": state.get("agents", {}),
            "stats": state.get("agentStats", {}),
        }))
        
        asyncio.create_task(self.ws_server.broadcast("system", {
            "status": self.orchestrator.status.value if self.orchestrator else "unknown",
            "connectedClients": self.ws_server.get_connection_count(),
        }))

    def _broadcast_messages(self):
        """Broadcast current messages to UI."""
        if not self.ws_server or not self.message_broker:
            return
        
        stats = self.message_broker.get_stats()
        asyncio.create_task(self.ws_server.broadcast("messages", {
            "stats": stats,
        }))

    async def stop(self):
        """Stop all subsystems gracefully."""
        print("\nStopping console server...")
        self._running = False
        
        # Stop WebSocket server
        if self.ws_server:
            await self.ws_server.stop()
            print("  ✓ WebSocket server stopped")
        
        # Stop message broker
        if self.message_broker:
            self.message_broker.stop()
            print("  ✓ Message broker stopped")
        
        # Stop agent manager
        if self.agent_manager:
            self.agent_manager.stop()
            print("  ✓ Agent manager stopped")
        
        # Stop orchestrator
        if self.orchestrator and self.orchestrator.status == SystemStatus.RUNNING:
            self.orchestrator.stop()
            print("  ✓ Orchestrator stopped")
        
        print("Server stopped.")

    def create_agent(self, task: str, callback=None) -> str:
        """
        Create a new agent to execute a task.
        
        This is the primary interface for submitting tasks to the RLM system.
        Tasks can be simple queries or complex multi-step recursive operations.
        
        Args:
            task: Task description (can be natural language, code, etc.)
            callback: Optional callback when agent completes
            
        Returns:
            Agent ID for tracking
        """
        if not self.agent_manager:
            raise RuntimeError("Agent manager not initialized")
        
        agent_id = self.agent_manager.create_agent(task, callback=callback)
        print(f"[AGENT] Created agent {agent_id[:8]} for task: {task[:50]}...")
        
        # Broadcast updated agent list
        if self.ws_server:
            self.ws_bridge.broadcast_agents_list()
        
        return agent_id

    def send_message(self, recipient_id: str, content: str, title: str = "") -> bool:
        """
        Send a message to an agent.
        
        Args:
            recipient_id: Target agent ID
            content: Message content
            title: Optional message title
            
        Returns:
            True if sent successfully
        """
        if not self.ws_bridge:
            return False
        
        return self.ws_bridge.send_user_message(recipient_id, content, title)

    def broadcast_to_agents(self, content: str, title: str = "") -> bool:
        """
        Broadcast a message to all agents.
        
        Args:
            content: Broadcast content
            title: Optional broadcast title
            
        Returns:
            True if broadcast sent
        """
        if not self.ws_bridge:
            return False
        
        return self.ws_bridge.handle_user_broadcast(content, title)


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Self_AI Console Server - Multi-Agent RLM System"
    )
    parser.add_argument(
        "--host", 
        default="localhost", 
        help="Host to bind to (default: localhost)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8765, 
        help="Port to bind to (default: 8765)"
    )
    
    args = parser.parse_args()
    
    server = ConsoleServer(host=args.host, port=args.port)
    
    # Handle shutdown signals
    loop = asyncio.get_event_loop()
    
    def shutdown():
        print("\nReceived shutdown signal...")
        asyncio.create_task(server.stop())
    
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, shutdown)
        except NotImplementedError:
            # Windows fallback
            signal.signal(sig, lambda s, f: shutdown())
    
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
