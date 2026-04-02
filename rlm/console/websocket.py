"""
WebSocket server for real-time console updates.
Uses the websockets library for proper WebSocket protocol support.
"""

import asyncio
import json
import os
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import time

try:
    import websockets
except ImportError:
    websockets = None

from rlm.utils.key_encryption import EncryptedKeyStore, ConfigurationError


class ConnectionState(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"


@dataclass
class WebSocketConnection:
    connection_id: str
    panels: List[str] = field(default_factory=list)
    state: ConnectionState = ConnectionState.DISCONNECTED
    last_ping: float = 0.0
    master_key: Optional[str] = None
    key_store: Optional[EncryptedKeyStore] = None


class WebSocketServer:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.connections: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.connection_info: Dict[str, WebSocketConnection] = {}
        self._lock = asyncio.Lock()
        self._subscribers: Dict[str, List[Callable[[str, Dict[str, Any]], None]]] = {}
        self._running = False
        self._server = None

    async def start(self):
        if websockets is None:
            raise RuntimeError("websockets library not installed. Run: pip install websockets>=12.0")
        
        self._running = True
        self._server = await websockets.serve(
            self._handle_client,
            self.host,
            self.port
        )
        addr = self._server.sockets[0].getsockname()
        print(f"WebSocket server started on ws://{addr[0]}:{addr[1]}")
        async with self._server:
            await self._server.serve_forever()

    async def stop(self):
        self._running = False
        if self._server:
            self._server.close()
            await self._server.wait_closed()

    async def _handle_client(self, websocket: websockets.WebSocketServerProtocol):
        client_id = f"{id(websocket)}"
        connection_info = WebSocketConnection(
            connection_id=client_id,
            state=ConnectionState.CONNECTED
        )
        
        async with self._lock:
            self.connections[client_id] = websocket
            self.connection_info[client_id] = connection_info

        print(f"Client connected: {websocket.remote_address}")

        try:
            async for message_str in websocket:
                try:
                    message = json.loads(message_str)
                    await self._handle_message(client_id, message, websocket)
                except json.JSONDecodeError:
                    print(f"Invalid JSON from client {client_id}")
                except Exception as e:
                    print(f"Error handling message from {client_id}: {e}")
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Error with client {client_id}: {e}")
        finally:
            async with self._lock:
                if client_id in self.connections:
                    del self.connections[client_id]
                if client_id in self.connection_info:
                    del self.connection_info[client_id]
            print(f"Client disconnected: {websocket.remote_address}")

    async def _handle_message(self, client_id: str, message: Dict[str, Any], websocket: websockets.WebSocketServerProtocol):
        msg_type = message.get("type")
        payload = message.get("payload", {})

        if msg_type == "subscribe":
            panels = payload.get("panels", [])
            async with self._lock:
                if client_id in self.connection_info:
                    self.connection_info[client_id].panels = panels
            response = {"type": "subscribed", "payload": {"panels": panels}}
            await websocket.send(json.dumps(response))

        elif msg_type == "unsubscribe":
            async with self._lock:
                if client_id in self.connection_info:
                    self.connection_info[client_id].panels = []
            response = {"type": "unsubscribed"}
            await websocket.send(json.dumps(response))

        elif msg_type == "pong":
            async with self._lock:
                if client_id in self.connection_info:
                    self.connection_info[client_id].last_ping = time.time()

        elif msg_type == "dispatch":
            action = payload.get("action", {})
            self._notify_subscribers("dispatch", action)
            response = {"type": "dispatch_ack", "payload": {"action": action}}
            await websocket.send(json.dumps(response))

        elif msg_type == "api_keys/unlock":
            master_key = payload.get("masterKey")
            async with self._lock:
                if client_id in self.connection_info:
                    try:
                        key_store = EncryptedKeyStore(master_key=master_key)
                        self.connection_info[client_id].master_key = master_key
                        self.connection_info[client_id].key_store = key_store
                        response = {
                            "type": "api_keys/unlock_ack",
                            "payload": {"success": True, "providers": key_store.list_keys()}
                        }
                    except ConfigurationError:
                        response = {
                            "type": "api_keys/unlock_ack",
                            "payload": {"success": False, "error": "Invalid master key"}
                        }
            await websocket.send(json.dumps(response))

        elif msg_type == "api_keys/lock":
            async with self._lock:
                if client_id in self.connection_info:
                    self.connection_info[client_id].master_key = None
                    self.connection_info[client_id].key_store = None
            response = {"type": "api_keys/lock_ack", "payload": {"success": True}}
            await websocket.send(json.dumps(response))

        elif msg_type == "api_keys/set":
            provider = payload.get("provider")
            api_key = payload.get("apiKey")
            master_key = payload.get("masterKey")
            async with self._lock:
                if client_id in self.connection_info:
                    conn = self.connection_info[client_id]
                    if master_key:
                        try:
                            conn.key_store = EncryptedKeyStore(master_key=master_key)
                            conn.master_key = master_key
                        except ConfigurationError:
                            response = {"type": "api_keys/set_ack", "payload": {"success": False, "error": "Invalid master key"}}
                            await websocket.send(json.dumps(response))
                            return
                    if conn.key_store and provider and api_key:
                        conn.key_store.set_key(provider, api_key)
                        response = {"type": "api_keys/set_ack", "payload": {"success": True, "provider": provider}}
                    else:
                        response = {"type": "api_keys/set_ack", "payload": {"success": False, "error": "Not unlocked or missing data"}}
            await websocket.send(json.dumps(response))

        elif msg_type == "api_keys/list":
            providers = []
            async with self._lock:
                if client_id in self.connection_info:
                    conn = self.connection_info[client_id]
                    if conn.key_store:
                        providers = conn.key_store.list_keys()
            response = {"type": "api_keys/list_ack", "payload": {"providers": providers}}
            await websocket.send(json.dumps(response))

        elif msg_type == "api_keys/delete":
            provider = payload.get("provider")
            master_key = payload.get("masterKey")
            async with self._lock:
                if client_id in self.connection_info:
                    conn = self.connection_info[client_id]
                    if master_key and not conn.key_store:
                        try:
                            conn.key_store = EncryptedKeyStore(master_key=master_key)
                            conn.master_key = master_key
                        except ConfigurationError:
                            response = {"type": "api_keys/delete_ack", "payload": {"success": False, "error": "Invalid master key"}}
                            await websocket.send(json.dumps(response))
                            return
                    if conn.key_store:
                        success = conn.key_store.delete_key(provider)
                        response = {"type": "api_keys/delete_ack", "payload": {"success": success, "provider": provider}}
                    else:
                        response = {"type": "api_keys/delete_ack", "payload": {"success": False, "error": "Not unlocked"}}
            await websocket.send(json.dumps(response))

        elif msg_type == "api_keys/status":
            is_unlocked = False
            providers = []
            async with self._lock:
                if client_id in self.connection_info:
                    conn = self.connection_info[client_id]
                    is_unlocked = conn.key_store is not None
                    if conn.key_store:
                        providers = conn.key_store.list_keys()
            response = {"type": "api_keys/status_ack", "payload": {"isUnlocked": is_unlocked, "providers": providers}}
            await websocket.send(json.dumps(response))

    async def broadcast(self, panel: str, state: Dict[str, Any]):
        """Broadcast a state update to all connected clients subscribed to the given panel."""
        message = {
            "type": "state_update",
            "payload": {"panel": panel, "state": state}
        }
        await self._broadcast(message)

    async def _broadcast(self, message: Dict[str, Any]):
        """Send a message to all connected clients."""
        if not self.connections:
            return
            
        message_str = json.dumps(message)
        disconnected = []
        
        async with self._lock:
            for client_id, websocket in self.connections.items():
                try:
                    await websocket.send(message_str)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.append(client_id)
                except Exception as e:
                    print(f"Error broadcasting to {client_id}: {e}")
                    disconnected.append(client_id)
            
            # Clean up disconnected clients
            for client_id in disconnected:
                if client_id in self.connections:
                    del self.connections[client_id]
                if client_id in self.connection_info:
                    del self.connection_info[client_id]

    def subscribe(self, event_type: str, callback: Callable[[str, Dict[str, Any]], None]):
        """Subscribe to events from the WebSocket server."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[[str, Dict[str, Any]], None]):
        """Unsubscribe from events."""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)

    def _notify_subscribers(self, event_type: str, data: Dict[str, Any]):
        """Notify subscribers of an event."""
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(event_type, data)
                except Exception as e:
                    print(f"Error in subscriber callback: {e}")

    def get_connection_count(self) -> int:
        """Get the number of connected clients."""
        return len(self.connections)


class WebSocketClient:
    """WebSocket client for connecting to a WebSocket server."""
    
    def __init__(self, url: str = "ws://localhost:8765"):
        self.url = url
        self._websocket = None
        self._running = False
        self._subscribed_panels: List[str] = []
        self._state_callbacks: Dict[str, Callable[[Dict[str, Any]], None]] = {}
        self._dispatch_callbacks: List[Callable[[Dict[str, Any]], None]] = {}
        self._reconnect_delay = 1.0
        self._max_reconnect_delay = 30.0

    async def connect(self):
        """Connect to the WebSocket server."""
        if websockets is None:
            raise RuntimeError("websockets library not installed. Run: pip install websockets>=12.0")
        
        self._running = True
        while self._running:
            try:
                self._websocket = await websockets.connect(self.url)
                print(f"Connected to {self.url}")
                
                # Re-subscribe to panels if any
                if self._subscribed_panels:
                    await self.subscribe(self._subscribed_panels)
                
                await self._receive_loop()
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
            except Exception as e:
                print(f"Connection error: {e}")
                if self._running:
                    await asyncio.sleep(self._reconnect_delay)
                    self._reconnect_delay = min(self._reconnect_delay * 2, self._max_reconnect_delay)

    async def disconnect(self):
        """Disconnect from the WebSocket server."""
        self._running = False
        if self._websocket:
            await self._websocket.close()

    async def subscribe(self, panels: List[str]):
        """Subscribe to one or more panels."""
        self._subscribed_panels = panels
        message = {
            "type": "subscribe",
            "payload": {"panels": panels}
        }
        await self._send(message)

    async def unsubscribe(self):
        """Unsubscribe from all panels."""
        message = {"type": "unsubscribe"}
        await self._send(message)
        self._subscribed_panels = []

    async def dispatch(self, action: Dict[str, Any]):
        """Dispatch an action to the server."""
        message = {
            "type": "dispatch",
            "payload": {"action": action}
        }
        await self._send(message)

    async def _send(self, message: Dict[str, Any]):
        """Send a message to the server."""
        if self._websocket:
            await self._websocket.send(json.dumps(message))

    async def _receive_loop(self):
        """Receive and handle messages from the server."""
        try:
            async for message_str in self._websocket:
                try:
                    message = json.loads(message_str)
                    self._handle_message(message)
                except json.JSONDecodeError:
                    print(f"Invalid JSON received")
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Receive error: {e}")

    def _handle_message(self, message: Dict[str, Any]):
        """Handle an incoming message."""
        msg_type = message.get("type")
        payload = message.get("payload", {})

        if msg_type == "state_update":
            panel = payload.get("panel")
            state = payload.get("state", {})
            if panel in self._state_callbacks:
                self._state_callbacks[panel](state)

        elif msg_type == "dispatch_ack":
            action = payload.get("action", {})
            for callback in self._dispatch_callbacks:
                try:
                    callback(action)
                except Exception:
                    pass

        elif msg_type == "ping":
            asyncio.create_task(self._send({"type": "pong", "payload": {"timestamp": time.time()}}))

    def on_state_update(self, panel: str, callback: Callable[[Dict[str, Any]], None]):
        """Register a callback for state updates from a panel."""
        self._state_callbacks[panel] = callback

    def on_dispatch_ack(self, callback: Callable[[Dict[str, Any]], None]):
        """Register a callback for dispatch acknowledgments."""
        self._dispatch_callbacks.append(callback)


def create_websocket_server(host: str = "localhost", port: int = 8765) -> WebSocketServer:
    """Create a new WebSocket server instance."""
    return WebSocketServer(host, port)


def create_websocket_client(url: str = "ws://localhost:8765") -> WebSocketClient:
    """Create a new WebSocket client instance."""
    return WebSocketClient(url)


if __name__ == "__main__":
    # Example usage
    async def main():
        server = create_websocket_server()
        print("Starting WebSocket server on ws://localhost:8765")
        await server.start()
    
    asyncio.run(main())
