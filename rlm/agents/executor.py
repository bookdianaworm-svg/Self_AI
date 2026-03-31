"""
RLM Executor for running agents in threads.

This module provides the RLMExecutor class that manages
thread-based execution of agents.
"""

import asyncio
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from rlm.agents.base.base_agent import AgentStatus, BaseAgent
from rlm.agents.base.swarm_agent import SwarmAgent


@dataclass
class ExecutionResult:
    """Result of an agent execution."""

    agent_id: str
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    completed_at: Optional[datetime] = None


class RLMExecutor:
    """
    Executor for running RLM agents in threads.

    This class manages a pool of threads for executing agents
    and tracks their execution status.
    """

    def __init__(self, max_workers: int = 10, thread_name_prefix: str = "RLMExecutor"):
        """
        Initialize the executor.

        Args:
            max_workers: Maximum number of worker threads.
            thread_name_prefix: Prefix for thread names.
        """
        self.max_workers = max_workers
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers, thread_name_prefix=thread_name_prefix
        )
        self._futures: Dict[str, Future] = {}
        self._agents: Dict[str, BaseAgent] = {}
        self._results: Dict[str, ExecutionResult] = {}
        self._lock = threading.Lock()
        self._start_times: Dict[str, float] = {}

    def submit(
        self, agent: BaseAgent, task: str, callback: Optional[Callable] = None
    ) -> str:
        """
        Submit an agent for execution.

        Args:
            agent: The agent to execute.
            task: Task description.
            callback: Optional callback when execution completes.

        Returns:
            The agent ID.
        """
        with self._lock:
            self._agents[agent.id] = agent
            self._start_times[agent.id] = time.perf_counter()

        future = self._executor.submit(self._run_agent, agent, task)
        self._futures[agent.id] = future

        if callback:
            future.add_done_callback(lambda f: callback(f))

        return agent.id

    def _run_agent(self, agent: BaseAgent, task: str) -> ExecutionResult:
        """
        Run an agent's task in a thread.

        Args:
            agent: The agent to run.
            task: Task description.

        Returns:
            ExecutionResult containing the result.
        """
        start_time = self._start_times.get(agent.id, time.perf_counter())

        try:
            result = agent.run_sync(task)

            execution_time_ms = (time.perf_counter() - start_time) * 1000

            return ExecutionResult(
                agent_id=agent.id,
                success=True,
                result=result,
                execution_time_ms=execution_time_ms,
                completed_at=datetime.now(),
            )
        except Exception as e:
            execution_time_ms = (time.perf_counter() - start_time) * 1000

            return ExecutionResult(
                agent_id=agent.id,
                success=False,
                error=str(e),
                execution_time_ms=execution_time_ms,
                completed_at=datetime.now(),
            )
        finally:
            with self._lock:
                if agent.id in self._start_times:
                    del self._start_times[agent.id]

    def get_result(self, agent_id: str) -> Optional[ExecutionResult]:
        """
        Get the result of an agent execution.

        Args:
            agent_id: ID of the agent.

        Returns:
            ExecutionResult if available, None otherwise.
        """
        return self._results.get(agent_id)

    def get_status(self, agent_id: str) -> Optional[AgentStatus]:
        """
        Get the status of an agent.

        Args:
            agent_id: ID of the agent.

        Returns:
            AgentStatus if agent is tracked, None otherwise.
        """
        agent = self._agents.get(agent_id)
        return agent.status if agent else None

    def is_running(self, agent_id: str) -> bool:
        """
        Check if an agent is currently running.

        Args:
            agent_id: ID of the agent.

        Returns:
            True if the agent is running, False otherwise.
        """
        future = self._futures.get(agent_id)
        return future is not None and not future.done()

    def is_complete(self, agent_id: str) -> bool:
        """
        Check if an agent execution is complete.

        Args:
            agent_id: ID of the agent.

        Returns:
            True if complete, False otherwise.
        """
        future = self._futures.get(agent_id)
        return future is not None and future.done()

    def cancel(self, agent_id: str) -> bool:
        """
        Cancel an agent execution.

        Args:
            agent_id: ID of the agent.

        Returns:
            True if cancelled, False if not found or already complete.
        """
        future = self._futures.get(agent_id)
        if future and not future.done():
            cancelled = future.cancel()
            if cancelled:
                agent = self._agents.get(agent_id)
                if agent:
                    agent.update_status(AgentStatus.TERMINATED)
            return cancelled
        return False

    def get_active_count(self) -> int:
        """
        Get the number of currently running agents.

        Returns:
            Number of active agent executions.
        """
        return sum(1 for f in self._futures.values() if not f.done())

    def get_completed_count(self) -> int:
        """
        Get the number of completed agent executions.

        Returns:
            Number of completed agent executions.
        """
        return sum(1 for f in self._futures.values() if f.done())

    def get_pending_count(self) -> int:
        """
        Get the number of pending agent executions.

        Returns:
            Number of pending agent executions.
        """
        return sum(
            1 for f in self._futures.values() if not f.done() and not f.cancelled()
        )

    def wait_for(
        self, agent_id: str, timeout: Optional[float] = None
    ) -> Optional[ExecutionResult]:
        """
        Wait for an agent execution to complete.

        Args:
            agent_id: ID of the agent.
            timeout: Optional timeout in seconds.

        Returns:
            ExecutionResult if complete, None if timeout.
        """
        future = self._futures.get(agent_id)
        if not future:
            return None

        try:
            future.result(timeout=timeout)
            return self.get_result(agent_id)
        except TimeoutError:
            return None
        except Exception:
            return self.get_result(agent_id)

    def wait_all(self, timeout: Optional[float] = None) -> Dict[str, ExecutionResult]:
        """
        Wait for all agent executions to complete.

        Args:
            timeout: Optional timeout in seconds.

        Returns:
            Dictionary of all execution results.
        """
        start_time = time.perf_counter()

        for future in self._futures.values():
            remaining = None
            if timeout:
                elapsed = time.perf_counter() - start_time
                remaining = max(0.1, timeout - elapsed)

            try:
                future.result(timeout=remaining)
            except TimeoutError:
                break
            except Exception:
                pass

        return dict(self._results)

    def shutdown(self, wait: bool = True) -> None:
        """
        Shutdown the executor.

        Args:
            wait: Whether to wait for pending tasks to complete.
        """
        self._executor.shutdown(wait=wait)

        if wait:
            with self._lock:
                self._futures.clear()
                self._agents.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return False
