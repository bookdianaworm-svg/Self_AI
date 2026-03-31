"""
Agent Manager for lifecycle management of agents.

This module provides the AgentManager class that manages
the complete lifecycle of agents including creation, tracking,
and cleanup.
"""

import asyncio
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from rlm.agents.base.base_agent import AgentConfig, AgentStatus, BaseAgent
from rlm.agents.executor import ExecutionResult, RLMExecutor


class ManagerStatus(Enum):
    """Status of the agent manager."""

    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    SHUTDOWN = "shutdown"


@dataclass
class AgentStats:
    """Statistics for agent management."""

    total_agents: int = 0
    active_agents: int = 0
    completed_agents: int = 0
    failed_agents: int = 0
    terminated_agents: int = 0


class AgentManager:
    """
    Manager for agent lifecycle management.

    This class provides centralized management of agents including:
    - Agent creation and registration
    - Lifecycle tracking
    - Resource management
    - Cleanup and termination
    """

    def __init__(
        self,
        max_agents: int = 100,
        max_workers: int = 10,
        cleanup_interval_seconds: float = 60.0,
    ):
        """
        Initialize the agent manager.

        Args:
            max_agents: Maximum number of agents to manage.
            max_workers: Maximum worker threads for execution.
            cleanup_interval_seconds: Interval for cleaning up completed agents.
        """
        self.max_agents = max_agents
        self.cleanup_interval = cleanup_interval_seconds

        # Agent tracking
        self._agents: Dict[str, BaseAgent] = {}
        self._tasks: Dict[str, str] = {}  # agent_id -> task mapping
        self._callbacks: Dict[str, List[Callable]] = {}  # agent_id -> callbacks
        self._lock = threading.Lock()

        # Executor for running agents
        self._executor = RLMExecutor(max_workers=max_workers)

        # Status
        self._status = ManagerStatus.IDLE
        self._stats = AgentStats()

        # Cleanup thread
        self._cleanup_thread: Optional[threading.Thread] = None
        self._should_cleanup = False

    @property
    def status(self) -> ManagerStatus:
        """Get the current status of the manager."""
        return self._status

    @property
    def stats(self) -> AgentStats:
        """Get current agent statistics."""
        return self._stats

    def start(self) -> None:
        """Start the agent manager."""
        if self._status == ManagerStatus.SHUTDOWN:
            raise RuntimeError("Cannot restart a shutdown manager")

        self._status = ManagerStatus.RUNNING
        self._should_cleanup = True

        # Start cleanup thread
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()

    def stop(self) -> None:
        """Stop the agent manager."""
        self._status = ManagerStatus.PAUSED
        self._should_cleanup = False

        if self._cleanup_thread:
            self._cleanup_thread.join(timeout=5.0)

    def shutdown(self) -> None:
        """Shutdown the agent manager and all agents."""
        self._status = ManagerStatus.SHUTDOWN
        self._should_cleanup = False

        # Terminate all agents
        self.terminate_all_agents()

        # Shutdown executor
        self._executor.shutdown(wait=True)

        if self._cleanup_thread:
            self._cleanup_thread.join(timeout=5.0)

    def create_agent(
        self,
        task: str,
        config: Optional[AgentConfig] = None,
        agent_id: Optional[str] = None,
        callback: Optional[Callable] = None,
    ) -> str:
        """
        Create and start a new agent.

        Args:
            task: Task description for the agent.
            config: Optional agent configuration.
            agent_id: Optional pre-assigned ID.
            callback: Optional callback when agent completes.

        Returns:
            The agent ID.

        Raises:
            RuntimeError: If max agents reached or manager not running.
        """
        if self._status != ManagerStatus.RUNNING:
            raise RuntimeError("Manager is not running")

        if len(self._agents) >= self.max_agents:
            raise RuntimeError(f"Maximum agents ({self.max_agents}) reached")

        # Create agent ID
        if agent_id is None:
            agent_id = str(uuid.uuid4())

        # Create agent
        if config is None:
            config = AgentConfig()

        agent = BaseAgent(
            id=agent_id,
            config=config,
        )

        # Register agent
        with self._lock:
            self._agents[agent_id] = agent
            self._tasks[agent_id] = task
            if callback:
                self._callbacks[agent_id] = [callback]
            else:
                self._callbacks[agent_id] = []

            self._stats.total_agents += 1
            self._stats.active_agents += 1

        # Submit to executor
        self._executor.submit(agent, task)

        return agent_id

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """
        Get an agent by ID.

        Args:
            agent_id: ID of the agent.

        Returns:
            The agent if found, None otherwise.
        """
        return self._agents.get(agent_id)

    def get_agent_status(self, agent_id: str) -> Optional[AgentStatus]:
        """
        Get the status of an agent.

        Args:
            agent_id: ID of the agent.

        Returns:
            AgentStatus if found, None otherwise.
        """
        agent = self._agents.get(agent_id)
        return agent.status if agent else None

    def get_agent_result(self, agent_id: str) -> Optional[Any]:
        """
        Get the result of an agent.

        Args:
            agent_id: ID of the agent.

        Returns:
            The agent's result if available, None otherwise.
        """
        agent = self._agents.get(agent_id)
        return agent.result if agent else None

    def get_all_agents(self) -> Dict[str, BaseAgent]:
        """
        Get all managed agents.

        Returns:
            Dictionary of agent_id -> BaseAgent.
        """
        return dict(self._agents)

    def get_active_agents(self) -> List[str]:
        """
        Get IDs of all active agents.

        Returns:
            List of active agent IDs.
        """
        return [
            agent_id
            for agent_id, agent in self._agents.items()
            if agent.status == AgentStatus.EXECUTING
        ]

    def get_completed_agents(self) -> List[str]:
        """
        Get IDs of all completed agents.

        Returns:
            List of completed agent IDs.
        """
        return [
            agent_id
            for agent_id, agent in self._agents.items()
            if agent.status == AgentStatus.COMPLETED
        ]

    def get_failed_agents(self) -> List[str]:
        """
        Get IDs of all failed agents.

        Returns:
            List of failed agent IDs.
        """
        return [
            agent_id
            for agent_id, agent in self._agents.items()
            if agent.status == AgentStatus.FAILED
        ]

    def terminate_agent(self, agent_id: str) -> bool:
        """
        Terminate a specific agent.

        Args:
            agent_id: ID of the agent to terminate.

        Returns:
            True if terminated, False if not found.
        """
        agent = self._agents.get(agent_id)
        if not agent:
            return False

        # Cancel if running
        if self._executor.is_running(agent_id):
            self._executor.cancel(agent_id)

        # Update status
        with self._lock:
            agent.update_status(AgentStatus.TERMINATED)
            self._stats.terminated_agents += 1
            if agent.status == AgentStatus.EXECUTING:
                self._stats.active_agents -= 1

        return True

    def terminate_all_agents(self) -> int:
        """
        Terminate all managed agents.

        Returns:
            Number of agents terminated.
        """
        count = 0
        for agent_id in list(self._agents.keys()):
            if self.terminate_agent(agent_id):
                count += 1
        return count

    def wait_for_agent(
        self, agent_id: str, timeout: Optional[float] = None
    ) -> Optional[Any]:
        """
        Wait for an agent to complete.

        Args:
            agent_id: ID of the agent.
            timeout: Optional timeout in seconds.

        Returns:
            The agent's result if completed, None if timeout.
        """
        result = self._executor.wait_for(agent_id, timeout=timeout)
        if result:
            return result.result
        return None

    def add_callback(self, agent_id: str, callback: Callable) -> bool:
        """
        Add a callback for an agent's completion.

        Args:
            agent_id: ID of the agent.
            callback: Callback function.

        Returns:
            True if added, False if agent not found.
        """
        if agent_id not in self._agents:
            return False

        with self._lock:
            if agent_id not in self._callbacks:
                self._callbacks[agent_id] = []
            self._callbacks[agent_id].append(callback)

        return True

    def remove_agent(self, agent_id: str) -> bool:
        """
        Remove an agent from management.

        Args:
            agent_id: ID of the agent to remove.

        Returns:
            True if removed, False if not found.
        """
        with self._lock:
            if agent_id not in self._agents:
                return False

            agent = self._agents[agent_id]

            # Update stats
            if agent.status == AgentStatus.EXECUTING:
                self._stats.active_agents -= 1
            elif agent.status == AgentStatus.COMPLETED:
                self._stats.completed_agents -= 1
            elif agent.status == AgentStatus.FAILED:
                self._stats.failed_agents -= 1

            # Remove
            del self._agents[agent_id]
            self._tasks.pop(agent_id, None)
            self._callbacks.pop(agent_id, None)

            return True

    def cleanup_completed(self) -> int:
        """
        Clean up completed and failed agents.

        Returns:
            Number of agents cleaned up.
        """
        to_remove = []

        with self._lock:
            for agent_id, agent in self._agents.items():
                if agent.status in (
                    AgentStatus.COMPLETED,
                    AgentStatus.FAILED,
                    AgentStatus.TERMINATED,
                ):
                    to_remove.append(agent_id)

        count = 0
        for agent_id in to_remove:
            if self.remove_agent(agent_id):
                count += 1

        return count

    def _cleanup_loop(self) -> None:
        """Background loop for cleaning up completed agents."""
        while self._should_cleanup:
            time.sleep(self.cleanup_interval)

            if self._should_cleanup:
                self.cleanup_completed()

    def _update_stats(self) -> None:
        """Update agent statistics."""
        with self._lock:
            self._stats.active_agents = sum(
                1
                for agent in self._agents.values()
                if agent.status == AgentStatus.EXECUTING
            )
            self._stats.completed_agents = sum(
                1
                for agent in self._agents.values()
                if agent.status == AgentStatus.COMPLETED
            )
            self._stats.failed_agents = sum(
                1
                for agent in self._agents.values()
                if agent.status == AgentStatus.FAILED
            )

    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the manager.

        Returns:
            Dictionary containing manager information.
        """
        self._update_stats()

        return {
            "status": self._status.value,
            "max_agents": self.max_agents,
            "stats": {
                "total": self._stats.total_agents,
                "active": self._stats.active_agents,
                "completed": self._stats.completed_agents,
                "failed": self._stats.failed_agents,
                "terminated": self._stats.terminated_agents,
            },
            "managed_agents": len(self._agents),
            "executor": {
                "active_count": self._executor.get_active_count(),
                "completed_count": self._executor.get_completed_count(),
                "pending_count": self._executor.get_pending_count(),
            },
        }

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
        return False
