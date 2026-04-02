"""
WebSocket server for real-time agent loop updates.

Pushes agent loop state changes to connected clients in real-time.
"""

import asyncio
import json
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Set


class AgentLoopWebSocket:
    """WebSocket server for real-time agent loop updates."""

    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[Any] = set()
        self._server: Optional[Any] = None
        self._running = False
        self._store = None
        self._store_unsubscribe: Optional[Callable] = None
        self._lock = threading.Lock()

    async def handle_client(self, websocket: Any, path: str):
        """Handle a single WebSocket client connection."""
        client_id = id(websocket)
        with self._lock:
            self.clients.add(websocket)

        try:
            await websocket.send_json(self._serialize_full_state())
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._handle_client_message(websocket, data)
                except json.JSONDecodeError:
                    pass
        except Exception:
            pass
        finally:
            with self._lock:
                self.clients.discard(websocket)

    async def _handle_client_message(self, websocket: Any, data: Dict[str, Any]):
        """Handle a message from a client."""
        msg_type = data.get("type")

        if msg_type == "subscribe":
            agent_id = data.get("agent_id")
            if agent_id:
                await websocket.send_json(
                    {
                        "type": "subscribed",
                        "agent_id": agent_id,
                        "history": self._get_agent_history(agent_id),
                    }
                )

        elif msg_type == "get_history":
            agent_id = data.get("agent_id")
            limit = data.get("limit", 100)
            if agent_id:
                await websocket.send_json(
                    {
                        "type": "history",
                        "agent_id": agent_id,
                        "history": self._get_agent_history(agent_id, limit),
                    }
                )

        elif msg_type == "search":
            query = data.get("query")
            if query:
                results = self._search_calls(query)
                await websocket.send_json(
                    {"type": "search_results", "query": query, "results": results}
                )

        elif msg_type == "get_stats":
            agent_id = data.get("agent_id")
            if agent_id:
                stats = self._get_agent_stats(agent_id)
                await websocket.send_json(
                    {"type": "stats", "agent_id": agent_id, "stats": stats}
                )

    def _serialize_full_state(self) -> Dict[str, Any]:
        """Serialize the full current state for initial sync."""
        if self._store is None:
            return {"type": "full_state", "agents": {}, "active_agent_id": None}

        state = self._store.get_state()
        loop_state = state.agent_loop

        agents_data = {}
        for aid, agent in loop_state.agents.items():
            agents_data[aid] = {
                "agent_id": aid,
                "agent_name": agent.agent_name,
                "status": agent.status.value
                if hasattr(agent.status, "value")
                else str(agent.status),
                "depth": agent.depth,
                "current_task": agent.current_task[:200]
                if agent.current_task
                else None,
                "parent_id": agent.parent_id,
                "total_iterations": len(agent.iterations),
                "total_llm_calls": len(agent.llm_calls),
                "total_repl_executions": len(agent.repl_history),
                "successful_repls": agent.successful_repl_executions,
                "failed_repls": agent.failed_repl_executions,
                "total_spawns": len(agent.spawning_events),
                "started_at": agent.started_at,
            }

        return {
            "type": "full_state",
            "agents": agents_data,
            "active_agent_id": loop_state.active_agent_id,
            "streaming_mode": loop_state.streaming_mode,
            "total_agents": loop_state.total_agents,
        }

    def _serialize_update(self) -> Dict[str, Any]:
        """Serialize incremental update."""
        if self._store is None:
            return {"type": "incremental_update"}

        state = self._store.get_state()
        loop_state = state.agent_loop

        if not loop_state.active_agent_id:
            return {"type": "incremental_update", "active_agent_id": None}

        active_agent = loop_state.agents.get(loop_state.active_agent_id)
        if not active_agent:
            return {"type": "incremental_update", "active_agent_id": None}

        latest_iteration = None
        if active_agent.iterations:
            last_iter = active_agent.iterations[-1]
            latest_iteration = {
                "iteration_id": last_iter.iteration_id,
                "iteration_number": last_iter.iteration_number,
                "depth": last_iter.depth,
                "response_preview": last_iter.response[:500]
                if last_iter.response
                else None,
                "final_answer": last_iter.final_answer,
                "code_block_count": len(last_iter.code_blocks),
            }

        latest_llm_call = None
        if active_agent.llm_calls:
            last_call = active_agent.llm_calls[-1]
            latest_llm_call = {
                "call_id": last_call.call_id,
                "depth": last_call.depth,
                "model": last_call.model,
                "call_type": last_call.call_type,
                "prompt_preview": last_call.prompt[:200] if last_call.prompt else None,
                "response_preview": last_call.response[:200]
                if last_call.response
                else None,
                "success": last_call.success,
                "error": last_call.error,
            }

        latest_repl = None
        if active_agent.repl_history:
            last_repl = active_agent.repl_history[-1]
            latest_repl = {
                "execution_id": last_repl.execution_id,
                "success": last_repl.success,
                "code_preview": last_repl.code[:200] if last_repl.code else None,
                "stdout_preview": last_repl.stdout[:200] if last_repl.stdout else None,
                "stderr_preview": last_repl.stderr[:200] if last_repl.stderr else None,
            }

        latest_cot = None
        if active_agent.chain_of_thought:
            last_cot = active_agent.chain_of_thought[-1]
            latest_cot = {
                "step_id": last_cot.step_id,
                "iteration": last_cot.iteration,
                "thought": last_cot.thought[:200] if last_cot.thought else None,
                "action": last_cot.action,
            }

        return {
            "type": "incremental_update",
            "active_agent_id": loop_state.active_agent_id,
            "agent_status": active_agent.status.value
            if hasattr(active_agent.status, "value")
            else str(active_agent.status),
            "latest_iteration": latest_iteration,
            "latest_llm_call": latest_llm_call,
            "latest_repl": latest_repl,
            "latest_cot": latest_cot,
            "stats": {
                "total_iterations": len(active_agent.iterations),
                "total_llm_calls": len(active_agent.llm_calls),
                "total_repls": len(active_agent.repl_history),
                "successful_repls": active_agent.successful_repl_executions,
                "failed_repls": active_agent.failed_repl_executions,
            },
        }

    def _get_agent_history(
        self, agent_id: str, limit: int = 100
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get history for a specific agent from storage."""
        if self._store is None:
            return {}

        from rlm.storage.agent_loop_storage import AgentLoopStorage

        storage = AgentLoopStorage()

        return storage.get_agent_history(agent_id, limit)

    def _get_agent_stats(self, agent_id: str) -> Dict[str, Any]:
        """Get stats for a specific agent."""
        if self._store is None:
            return {}

        from rlm.storage.agent_loop_storage import AgentLoopStorage

        storage = AgentLoopStorage()

        return storage.get_agent_stats(agent_id)

    def _search_calls(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search LLM calls by content."""
        if self._store is None:
            return []

        from rlm.storage.agent_loop_storage import AgentLoopStorage

        storage = AgentLoopStorage()

        return storage.search_llm_calls(contains_prompt=query, limit=limit)

    def _on_store_change(self, state: Any):
        """Called when Redux store changes."""
        if not self.clients:
            return

        update = self._serialize_update()
        clients_to_remove = set()

        async def send_update():
            for client in self.clients:
                try:
                    await client.send_json(update)
                except Exception:
                    clients_to_remove.add(client)

        asyncio.create_task(send_update())

        for client in clients_to_remove:
            with self._lock:
                self.clients.discard(client)

    def start(self, store: Any):
        """Start the WebSocket server.

        Args:
            store: The Redux store to subscribe to.
        """
        self._store = store
        self._running = True
        store.subscribe(self._on_store_change)

        async def run_server():
            import websockets

            async with websockets.serve(self.handle_client, self.host, self.port):
                await asyncio.Future()

        asyncio.create_task(run_server())

    def stop(self):
        """Stop the WebSocket server."""
        self._running = False
        self._server = None


def create_websocket_server(
    host: str = "localhost", port: int = 8765
) -> AgentLoopWebSocket:
    """Factory function to create a WebSocket server.

    Args:
        host: Host to bind to.
        port: Port to bind to.

    Returns:
        Configured AgentLoopWebSocket server instance.
    """
    return AgentLoopWebSocket(host=host, port=port)
