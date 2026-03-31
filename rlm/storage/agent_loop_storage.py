"""
SQLite-backed storage for agent loop history.

Enabled by default for persistent storage of all agent loop data.
"""

import json
import os
import sqlite3
import threading
import time
from dataclasses import asdict
from typing import Any, Dict, List, Optional


class AgentLoopStorage:
    """SQLite-backed storage for agent loop history (enabled by default)."""

    def __init__(self, db_path: str = ".agent_loop.db", enabled: bool = True):
        self.db_path = db_path
        self.enabled = enabled
        self._lock = threading.Lock()
        if enabled:
            self._init_db()

    def _init_db(self):
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS llm_calls (
                    call_id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    parent_call_id TEXT,
                    depth INTEGER,
                    model TEXT,
                    prompt TEXT,
                    response TEXT,
                    input_tokens INTEGER,
                    output_tokens INTEGER,
                    cost REAL,
                    execution_time REAL,
                    call_type TEXT,
                    success INTEGER,
                    error TEXT,
                    timestamp REAL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS repl_executions (
                    execution_id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    parent_call_id TEXT,
                    code TEXT,
                    stdout TEXT,
                    stderr TEXT,
                    execution_time REAL,
                    success INTEGER,
                    error TEXT,
                    return_value_preview TEXT,
                    llm_calls_made TEXT,
                    timestamp REAL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS iterations (
                    iteration_id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    iteration_number INTEGER,
                    depth INTEGER,
                    prompt TEXT,
                    response TEXT,
                    code_blocks TEXT,
                    final_answer TEXT,
                    execution_time REAL,
                    timestamp REAL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS spawning_events (
                    event_id TEXT PRIMARY KEY,
                    parent_agent_id TEXT NOT NULL,
                    child_agent_id TEXT NOT NULL,
                    child_task TEXT,
                    reason TEXT,
                    timestamp REAL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS chain_thoughts (
                    step_id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    iteration INTEGER,
                    thought TEXT,
                    action TEXT,
                    context TEXT,
                    timestamp REAL
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_llm_calls_agent_id 
                ON llm_calls(agent_id, timestamp)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_repl_executions_agent_id 
                ON repl_executions(agent_id, timestamp)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_iterations_agent_id 
                ON iterations(agent_id, timestamp)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_spawning_parent_agent 
                ON spawning_events(parent_agent_id, timestamp)
            """)

    def save_llm_call(self, call_data: Dict[str, Any]):
        """Save an LLM call record."""
        if not self.enabled:
            return
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO llm_calls 
                    (call_id, agent_id, parent_call_id, depth, model, prompt, response,
                     input_tokens, output_tokens, cost, execution_time, call_type, 
                     success, error, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        call_data.get("call_id"),
                        call_data.get("agent_id"),
                        call_data.get("parent_call_id"),
                        call_data.get("depth"),
                        call_data.get("model"),
                        call_data.get("prompt"),
                        call_data.get("response"),
                        call_data.get("input_tokens"),
                        call_data.get("output_tokens"),
                        call_data.get("cost"),
                        call_data.get("execution_time"),
                        call_data.get("call_type"),
                        int(call_data.get("success", True)),
                        call_data.get("error"),
                        call_data.get("timestamp", time.time()),
                    ),
                )

    def save_repl_execution(self, exec_data: Dict[str, Any]):
        """Save a REPL execution record."""
        if not self.enabled:
            return
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO repl_executions
                    (execution_id, agent_id, parent_call_id, code, stdout, stderr,
                     execution_time, success, error, return_value_preview,
                     llm_calls_made, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        exec_data.get("execution_id"),
                        exec_data.get("agent_id"),
                        exec_data.get("parent_call_id"),
                        exec_data.get("code"),
                        exec_data.get("stdout"),
                        exec_data.get("stderr"),
                        exec_data.get("execution_time"),
                        int(exec_data.get("success", True)),
                        exec_data.get("error"),
                        exec_data.get("return_value_preview"),
                        json.dumps(exec_data.get("llm_calls_made", [])),
                        exec_data.get("timestamp", time.time()),
                    ),
                )

    def save_iteration(self, iter_data: Dict[str, Any]):
        """Save an iteration record."""
        if not self.enabled:
            return
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO iterations
                    (iteration_id, agent_id, iteration_number, depth, prompt, response,
                     code_blocks, final_answer, execution_time, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        iter_data.get("iteration_id"),
                        iter_data.get("agent_id"),
                        iter_data.get("iteration_number"),
                        iter_data.get("depth"),
                        iter_data.get("prompt"),
                        iter_data.get("response"),
                        json.dumps(iter_data.get("code_blocks", [])),
                        iter_data.get("final_answer"),
                        iter_data.get("execution_time"),
                        iter_data.get("timestamp", time.time()),
                    ),
                )

    def save_spawning_event(self, spawn_data: Dict[str, Any]):
        """Save a spawning event record."""
        if not self.enabled:
            return
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO spawning_events
                    (event_id, parent_agent_id, child_agent_id, child_task, reason, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        spawn_data.get("event_id"),
                        spawn_data.get("parent_agent_id"),
                        spawn_data.get("child_agent_id"),
                        spawn_data.get("child_task"),
                        spawn_data.get("reason"),
                        spawn_data.get("timestamp", time.time()),
                    ),
                )

    def save_chain_thought(self, cot_data: Dict[str, Any]):
        """Save a chain-of-thought step record."""
        if not self.enabled:
            return
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO chain_thoughts
                    (step_id, agent_id, iteration, thought, action, context, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        cot_data.get("step_id"),
                        cot_data.get("agent_id"),
                        cot_data.get("iteration"),
                        cot_data.get("thought"),
                        cot_data.get("action"),
                        json.dumps(cot_data.get("context", {})),
                        cot_data.get("timestamp", time.time()),
                    ),
                )

    def get_agent_history(
        self,
        agent_id: str,
        limit: int = 100,
        include_llm_calls: bool = True,
        include_repl_executions: bool = True,
        include_iterations: bool = True,
        include_spawning: bool = True,
        include_chain_thoughts: bool = True,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get full history for an agent."""
        if not self.enabled:
            return {}

        result: Dict[str, List[Dict[str, Any]]] = {}

        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row

                if include_llm_calls:
                    calls = conn.execute(
                        """SELECT * FROM llm_calls WHERE agent_id = ? 
                           ORDER BY timestamp DESC LIMIT ?""",
                        (agent_id, limit),
                    ).fetchall()
                    result["llm_calls"] = [dict(r) for r in calls]

                if include_repl_executions:
                    repls = conn.execute(
                        """SELECT * FROM repl_executions WHERE agent_id = ? 
                           ORDER BY timestamp DESC LIMIT ?""",
                        (agent_id, limit),
                    ).fetchall()
                    result["repl_executions"] = [dict(r) for r in repls]

                if include_iterations:
                    iterations = conn.execute(
                        """SELECT * FROM iterations WHERE agent_id = ? 
                           ORDER BY timestamp DESC LIMIT ?""",
                        (agent_id, limit),
                    ).fetchall()
                    result["iterations"] = [dict(r) for r in iterations]

                if include_spawning:
                    spawns = conn.execute(
                        """SELECT * FROM spawning_events 
                           WHERE parent_agent_id = ? ORDER BY timestamp DESC""",
                        (agent_id,),
                    ).fetchall()
                    result["spawning_events"] = [dict(r) for r in spawns]

                if include_chain_thoughts:
                    cots = conn.execute(
                        """SELECT * FROM chain_thoughts WHERE agent_id = ? 
                           ORDER BY iteration ASC, timestamp ASC""",
                        (agent_id,),
                    ).fetchall()
                    result["chain_thoughts"] = [dict(r) for r in cots]

        return result

    def get_llm_call(self, call_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific LLM call by ID."""
        if not self.enabled:
            return None
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                row = conn.execute(
                    "SELECT * FROM llm_calls WHERE call_id = ?", (call_id,)
                ).fetchone()
                return dict(row) if row else None

    def get_repl_execution(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific REPL execution by ID."""
        if not self.enabled:
            return None
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                row = conn.execute(
                    "SELECT * FROM repl_executions WHERE execution_id = ?",
                    (execution_id,),
                ).fetchone()
                return dict(row) if row else None

    def search_llm_calls(
        self,
        agent_id: Optional[str] = None,
        contains_prompt: Optional[str] = None,
        contains_response: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Search LLM calls by content."""
        if not self.enabled:
            return []

        query = "SELECT * FROM llm_calls WHERE 1=1"
        params: List[Any] = []

        if agent_id:
            query += " AND agent_id = ?"
            params.append(agent_id)
        if contains_prompt:
            query += " AND prompt LIKE ?"
            params.append(f"%{contains_prompt}%")
        if contains_response:
            query += " AND response LIKE ?"
            params.append(f"%{contains_response}%")

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(query, params).fetchall()
                return [dict(r) for r in rows]

    def get_agent_stats(self, agent_id: str) -> Dict[str, Any]:
        """Get aggregate statistics for an agent."""
        if not self.enabled:
            return {}

        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row

                stats = {}

                llm_stats = conn.execute(
                    """
                    SELECT 
                        COUNT(*) as total_calls,
                        SUM(input_tokens) as total_input_tokens,
                        SUM(output_tokens) as total_output_tokens,
                        SUM(cost) as total_cost,
                        SUM(execution_time) as total_time
                    FROM llm_calls WHERE agent_id = ?
                """,
                    (agent_id,),
                ).fetchone()

                if llm_stats:
                    stats["llm_calls"] = dict(llm_stats)

                repl_stats = conn.execute(
                    """
                    SELECT 
                        COUNT(*) as total_executions,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                        SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed,
                        SUM(execution_time) as total_time
                    FROM repl_executions WHERE agent_id = ?
                """,
                    (agent_id,),
                ).fetchone()

                if repl_stats:
                    stats["repl_executions"] = dict(repl_stats)

                iter_count = conn.execute(
                    "SELECT COUNT(*) as total FROM iterations WHERE agent_id = ?",
                    (agent_id,),
                ).fetchone()

                if iter_count:
                    stats["total_iterations"] = iter_count["total"]

                spawn_count = conn.execute(
                    """SELECT COUNT(*) as total FROM spawning_events 
                       WHERE parent_agent_id = ?""",
                    (agent_id,),
                ).fetchone()

                if spawn_count:
                    stats["total_spawns"] = spawn_count["total"]

                return stats

    def clear_agent_history(self, agent_id: str):
        """Clear all history for an agent."""
        if not self.enabled:
            return
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM llm_calls WHERE agent_id = ?", (agent_id,))
                conn.execute(
                    "DELETE FROM repl_executions WHERE agent_id = ?", (agent_id,)
                )
                conn.execute("DELETE FROM iterations WHERE agent_id = ?", (agent_id,))
                conn.execute(
                    "DELETE FROM chain_thoughts WHERE agent_id = ?", (agent_id,)
                )

    def get_all_agents(self) -> List[str]:
        """Get list of all agent IDs with recorded history."""
        if not self.enabled:
            return []
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT DISTINCT agent_id FROM llm_calls ORDER BY timestamp DESC"
                ).fetchall()
                return [r["agent_id"] for r in rows]

    def vacuum(self):
        """Clean up the database by removing unused space."""
        if not self.enabled:
            return
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("VACUUM")
