"""
WebSocket server for real-time console updates.
"""

import asyncio
import json
import os
import threading
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import time

from rlm.utils.key_encryption import EncryptedKeyStore, ConfigurationError


class ConnectionState(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"


@dataclass
class WebSocketConnection:
    connection_id: str
    client_id: str
    panels: List[str] = field(default_factory=list)
    state: ConnectionState = ConnectionState.DISCONNECTED
    last_ping: float = 0.0
    master_key: Optional[str] = None
    key_store: Optional[EncryptedKeyStore] = None


class WebSocketServer:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.connections: Dict[str, WebSocketConnection] = {}
        self._lock = threading.Lock()
        self._subscribers: Dict[str, List[Callable[[str, Dict[str, Any]], None]]] = {}
        self._running = False
        self._server = None
        self._poll_interval_ms = 1000

    async def start(self):
        self._running = True
        self._server = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port
        )
        addr = self._server.sockets[0].getsockname()
        print(f"WebSocket server started on {addr}")
        async with self._server:
            await self._server.serve_forever()

    async def stop(self):
        self._running = False
        if self._server:
            self._server.close()
            await self._server.wait_closed()

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client_id = f"{id(writer)}"
        connection = WebSocketConnection(
            connection_id=client_id,
            client_id=client_id,
            state=ConnectionState.CONNECTED
        )
        with self._lock:
            self.connections[client_id] = connection

        addr = writer.get_extra_info('peername')
        print(f"Client connected: {addr}")

        try:
            while self._running:
                try:
                    data = await asyncio.wait_for(
                        reader.read(4096),
                        timeout=self._poll_interval_ms / 1000.0
                    )
                    if not data:
                        break
                    message = json.loads(data.decode())
                    await self._handle_message(client_id, message, writer)
                except asyncio.TimeoutError:
                    await self._send_ping(writer)
        except Exception as e:
            print(f"Error handling client {client_id}: {e}")
        finally:
            with self._lock:
                if client_id in self.connections:
                    self.connections[client_id].state = ConnectionState.DISCONNECTED
                    del self.connections[client_id]
            writer.close()
            await writer.wait_closed()
            print(f"Client disconnected: {addr}")

    async def _handle_message(self, client_id: str, message: Dict[str, Any], writer: asyncio.StreamWriter):
        msg_type = message.get("type")
        payload = message.get("payload", {})

        if msg_type == "subscribe":
            panels = payload.get("panels", [])
            with self._lock:
                if client_id in self.connections:
                    self.connections[client_id].panels = panels
            response = {"type": "subscribed", "payload": {"panels": panels}}
            await self._send(writer, response)

        elif msg_type == "unsubscribe":
            with self._lock:
                if client_id in self.connections:
                    self.connections[client_id].panels = []
            response = {"type": "unsubscribed"}
            await self._send(writer, response)

        elif msg_type == "pong":
            with self._lock:
                if client_id in self.connections:
                    self.connections[client_id].last_ping = time.time()

        elif msg_type == "dispatch":
            action = payload.get("action", {})
            self._notify_subscribers("dispatch", action)
            response = {"type": "dispatch_ack", "payload": {"action": action}}
            await self._send(writer, response)

        elif msg_type == "api_keys/unlock":
            master_key = payload.get("masterKey")
            with self._lock:
                if client_id in self.connections:
                    try:
                        key_store = EncryptedKeyStore(master_key=master_key)
                        self.connections[client_id].master_key = master_key
                        self.connections[client_id].key_store = key_store
                        response = {
                            "type": "api_keys/unlock_ack",
                            "payload": {"success": True, "providers": key_store.list_keys()}
                        }
                    except ConfigurationError:
                        response = {
                            "type": "api_keys/unlock_ack",
                            "payload": {"success": False, "error": "Invalid master key"}
                        }
            await self._send(writer, response)

        elif msg_type == "api_keys/lock":
            with self._lock:
                if client_id in self.connections:
                    self.connections[client_id].master_key = None
                    self.connections[client_id].key_store = None
            response = {"type": "api_keys/lock_ack", "payload": {"success": True}}
            await self._send(writer, response)

        elif msg_type == "api_keys/set":
            provider = payload.get("provider")
            api_key = payload.get("apiKey")
            master_key = payload.get("masterKey")
            with self._lock:
                if client_id in self.connections:
                    conn = self.connections[client_id]
                    if master_key:
                        try:
                            conn.key_store = EncryptedKeyStore(master_key=master_key)
                            conn.master_key = master_key
                        except ConfigurationError:
                            response = {"type": "api_keys/set_ack", "payload": {"success": False, "error": "Invalid master key"}}
                            await self._send(writer, response)
                            return
                    if conn.key_store and provider and api_key:
                        conn.key_store.set_key(provider, api_key)
                        response = {"type": "api_keys/set_ack", "payload": {"success": True, "provider": provider}}
                    else:
                        response = {"type": "api_keys/set_ack", "payload": {"success": False, "error": "Not unlocked or missing data"}}
            await self._send(writer, response)

        elif msg_type == "api_keys/list":
            providers = []
            with self._lock:
                if client_id in self.connections:
                    conn = self.connections[client_id]
                    if conn.key_store:
                        providers = conn.key_store.list_keys()
            response = {"type": "api_keys/list_ack", "payload": {"providers": providers}}
            await self._send(writer, response)

        elif msg_type == "api_keys/delete":
            provider = payload.get("provider")
            master_key = payload.get("masterKey")
            with self._lock:
                if client_id in self.connections:
                    conn = self.connections[client_id]
                    if master_key and not conn.key_store:
                        try:
                            conn.key_store = EncryptedKeyStore(master_key=master_key)
                            conn.master_key = master_key
                        except ConfigurationError:
                            response = {"type": "api_keys/delete_ack", "payload": {"success": False, "error": "Invalid master key"}}
                            await self._send(writer, response)
                            return
                    if conn.key_store:
                        success = conn.key_store.delete_key(provider)
                        response = {"type": "api_keys/delete_ack", "payload": {"success": success, "provider": provider}}
                    else:
                        response = {"type": "api_keys/delete_ack", "payload": {"success": False, "error": "Not unlocked"}}
            await self._send(writer, response)

        elif msg_type == "api_keys/status":
            is_unlocked = False
            providers = []
            with self._lock:
                if client_id in self.connections:
                    conn = self.connections[client_id]
                    is_unlocked = conn.key_store is not None
                    if conn.key_store:
                        providers = conn.key_store.list_keys()
            response = {"type": "api_keys/status_ack", "payload": {"isUnlocked": is_unlocked, "providers": providers}}
            await self._send(writer, response)

    async def _send_ping(self, writer: asyncio.StreamWriter):
        message = {"type": "ping", "payload": {"timestamp": time.time()}}
        try:
            writer.write(json.dumps(message).encode())
            await writer.drain()
        except Exception:
            pass

    async def _send(self, writer: asyncio.StreamWriter, message: Dict[str, Any]):
        try:
            writer.write(json.dumps(message).encode())
            await writer.drain()
        except Exception as e:
            print(f"Error sending message: {e}")

    def broadcast(self, panel: str, state: Dict[str, Any]):
        message = {
            "type": "state_update",
            "payload": {"panel": panel, "state": state}
        }
        self._broadcast(message)

    def _broadcast(self, message: Dict[str, Any]):
        encoded = json.dumps(message).encode()
        with self._lock:
            disconnected = []
            for conn_id, conn in self.connections.items():
                if conn.state == ConnectionState.CONNECTED:
                    try:
                        conn.writer.write(encoded)
                    except Exception:
                        disconnected.append(conn_id)
            for conn_id in disconnected:
                if conn_id in self.connections:
                    self.connections[conn_id].state = ConnectionState.DISCONNECTED

    def subscribe(self, event_type: str, callback: Callable[[str, Dict[str, Any]], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[[str, Dict[str, Any]], None]):
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)

    def _notify_subscribers(self, event_type: str, data: Dict[str, Any]):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(event_type, data)
                except Exception as e:
                    print(f"Error in subscriber callback: {e}")

    def get_connection_count(self) -> int:
        with self._lock:
            return sum(1 for c in self.connections.values() if c.state == ConnectionState.CONNECTED)


class WebSocketClient:
    def __init__(self, url: str = "ws://localhost:8765"):
        self.url = url
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._running = False
        self._subscribed_panels: List[str] = []
        self._state_callbacks: Dict[str, Callable[[Dict[str, Any]], None]] = {}
        self._dispatch_callbacks: List[Callable[[Dict[str, Any]], None]] = []
        self._reconnect_delay = 1.0
        self._max_reconnect_delay = 30.0

    async def connect(self):
        self._running = True
        while self._running:
            try:
                self._reader, self._writer = await asyncio.wait_for(
                    asyncio.open_connection(*self.url.replace("ws://", "").split(":")),
                    timeout=5.0
                )
                print(f"Connected to {self.url}")
                if self._subscribed_panels:
                    await self.subscribe(self._subscribed_panels)
                await self._receive_loop()
            except Exception as e:
                print(f"Connection error: {e}")
                if self._running:
                    await asyncio.sleep(self._reconnect_delay)
                    self._reconnect_delay = min(self._reconnect_delay * 2, self._max_reconnect_delay)

    async def disconnect(self):
        self._running = False
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()

    async def subscribe(self, panels: List[str]):
        self._subscribed_panels = panels
        message = {
            "type": "subscribe",
            "payload": {"panels": panels}
        }
        await self._send(message)

    async def unsubscribe(self):
        message = {"type": "unsubscribe"}
        await self._send(message)
        self._subscribed_panels = []

    async def dispatch(self, action: Dict[str, Any]):
        message = {
            "type": "dispatch",
            "payload": {"action": action}
        }
        await self._send(message)

    async def _send(self, message: Dict[str, Any]):
        if self._writer:
            self._writer.write(json.dumps(message).encode())
            await self._writer.drain()

    async def _receive_loop(self):
        try:
            while self._running:
                try:
                    data = await asyncio.wait_for(
                        self._reader.read(4096),
                        timeout=30.0
                    )
                    if not data:
                        break
                    message = json.loads(data.decode())
                    self._handle_message(message)
                except asyncio.TimeoutError:
                    await self._send({"type": "ping", "payload": {"timestamp": time.time()}})
        except Exception as e:
            print(f"Receive error: {e}")

    def _handle_message(self, message: Dict[str, Any]):
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
        self._state_callbacks[panel] = callback

    def on_dispatch_ack(self, callback: Callable[[Dict[str, Any]], None]):
        self._dispatch_callbacks.append(callback)


def create_websocket_server(host: str = "localhost", port: int = 8765) -> WebSocketServer:
    return WebSocketServer(host, port)


def create_websocket_client(url: str = "ws://localhost:8765") -> WebSocketClient:
    return WebSocketClient(url)
