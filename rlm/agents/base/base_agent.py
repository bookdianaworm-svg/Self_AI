"""
Base Agent class for RLM swarm system.

This module provides the base class for all agents in the swarm system,
including configuration and lifecycle management.
"""

import asyncio
import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from rlm.core.rlm import RLM


class AgentStatus(Enum):
    """Status of an agent."""

    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    TERMINATED = "terminated"


@dataclass
class AgentConfig:
    """Configuration for an agent."""

    backend: str = "openai"
    backend_kwargs: Optional[Dict[str, Any]] = None
    environment: str = "local"
    environment_kwargs: Optional[Dict[str, Any]] = None
    max_depth: int = 1
    max_iterations: int = 30
    max_budget: Optional[float] = None
    max_timeout: Optional[float] = None
    max_tokens: Optional[int] = None
    max_errors: Optional[int] = None
    custom_system_prompt: Optional[str] = None
    custom_tools: Optional[Dict[str, Any]] = None
    custom_sub_tools: Optional[Dict[str, Any]] = None
    compaction: bool = False
    compaction_threshold_pct: float = 0.85
    can_spawn: bool = False
    max_child_agents: int = 5


@dataclass
class AgentMetrics:
    """Metrics for an agent's execution."""

    iterations: int = 0
    total_tokens: int = 0
    total_time_ms: float = 0.0
    api_calls: int = 0
    errors: int = 0
    spawns: int = 0


@dataclass
class BaseAgent:
    """
    Base class for all agents in the swarm system.

    Agents are specialized RLM instances that can execute tasks,
    communicate with other agents, and spawn child agents.

    Attributes:
        id: Unique identifier for the agent.
        parent_id: ID of the parent agent (None for root agent).
        config: Configuration for the agent.
        status: Current status of the agent.
        created_at: When the agent was created.
        last_update: Last time the agent was updated.
    """

    id: str
    parent_id: Optional[str] = None
    config: AgentConfig = field(default_factory=AgentConfig)
    status: AgentStatus = AgentStatus.IDLE
    created_at: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    metrics: AgentMetrics = field(default_factory=AgentMetrics)
    child_agent_ids: List[str] = field(default_factory=list)
    message_handlers: List[Callable] = field(default_factory=list)

    def __post_init__(self):
        """Initialize the agent after dataclass initialization."""
        if self.id is None:
            self.id = str(uuid.uuid4())

        # Create the underlying RLM instance
        self.rlm = self._create_rlm_instance()

        # Message queues for communication
        self.inbox: asyncio.Queue = asyncio.Queue()
        self.outbox: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def _create_rlm_instance(self) -> RLM:
        """
        Create the underlying RLM instance for this agent.

        Returns:
            RLM instance configured for this agent.
        """
        return RLM(
            backend=self.config.backend,
            backend_kwargs=self.config.backend_kwargs,
            environment=self.config.environment,
            environment_kwargs=self.config.environment_kwargs,
            depth=0,
            max_depth=self.config.max_depth,
            max_iterations=self.config.max_iterations,
            max_budget=self.config.max_budget,
            max_timeout=self.config.max_timeout,
            max_tokens=self.config.max_tokens,
            max_errors=self.config.max_errors,
            custom_system_prompt=self.config.custom_system_prompt,
            logger=None,
            verbose=False,
            persistent=False,
            custom_tools=self.config.custom_tools,
            custom_sub_tools=self.config.custom_sub_tools,
            compaction=self.config.compaction,
            compaction_threshold_pct=self.config.compaction_threshold_pct,
        )

    async def execute_task(self, task_description: str) -> Any:
        """
        Execute the assigned task. Must be implemented by subclasses.

        Args:
            task_description: Description of the task to execute.

        Returns:
            Result of the task execution.
        """
        raise NotImplementedError("Subclasses must implement execute_task")

    async def run(self, task_description: str) -> Any:
        """
        Main execution method that manages the agent lifecycle.

        Args:
            task_description: Description of the task to execute.

        Returns:
            Result of the task execution.
        """
        self.status = AgentStatus.EXECUTING
        self.start_time = datetime.now()
        self.last_update = datetime.now()

        try:
            self.result = await self.execute_task(task_description)
            self.status = AgentStatus.COMPLETED
        except Exception as e:
            self.error = str(e)
            self.status = AgentStatus.FAILED
            self.metrics.errors += 1
        finally:
            self.end_time = datetime.now()
            self.last_update = datetime.now()

        return self.result

    def run_sync(self, task_description: str) -> Any:
        """
        Synchronous version of run() for thread-based execution.

        Args:
            task_description: Description of the task to execute.

        Returns:
            Result of the task execution.
        """
        self.status = AgentStatus.EXECUTING
        self.start_time = datetime.now()
        self.last_update = datetime.now()

        try:
            # Run the async task in a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                self.result = loop.run_until_complete(
                    self.execute_task(task_description)
                )
                self.status = AgentStatus.COMPLETED
            finally:
                loop.close()
        except Exception as e:
            self.error = str(e)
            self.status = AgentStatus.FAILED
            self.metrics.errors += 1
        finally:
            self.end_time = datetime.now()
            self.last_update = datetime.now()

        return self.result

    def send_message(self, recipient_id: str, message: Dict[str, Any]) -> None:
        """
        Send a message to another agent.

        Args:
            recipient_id: ID of the recipient agent.
            message: Message content to send.
        """
        message_obj = {
            "id": str(uuid.uuid4()),
            "sender": self.id,
            "recipient": recipient_id,
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "type": "agent_message",
        }
        with self._lock:
            self.outbox.append(message_obj)

    def broadcast_message(self, message: Dict[str, Any]) -> None:
        """
        Broadcast a message to all child agents.

        Args:
            message: Message content to broadcast.
        """
        for child_id in self.child_agent_ids:
            self.send_message(child_id, message)

    def receive_message(self, message: Dict[str, Any]) -> None:
        """
        Receive a message and add it to the inbox.

        Args:
            message: Message to receive.
        """
        try:
            self.inbox.put_nowait(message)
        except asyncio.QueueFull:
            pass  # Inbox full, drop message

    def register_message_handler(self, handler: Callable) -> None:
        """
        Register a function to handle incoming messages.

        Args:
            handler: Callable that handles incoming messages.
        """
        self.message_handlers.append(handler)

    async def process_incoming_messages(self) -> None:
        """Process messages from the inbox."""
        while not self.inbox.empty():
            message = await self.inbox.get()
            for handler in self.message_handlers:
                await handler(message)

    def can_spawn_agents(self) -> bool:
        """
        Check if this agent is allowed to spawn child agents.

        Returns:
            True if spawning is allowed, False otherwise.
        """
        return self.config.can_spawn

    def spawn_agent(
        self,
        task: str,
        config: Optional[AgentConfig] = None,
        agent_id: Optional[str] = None,
    ) -> "BaseAgent":
        """
        Spawn a new child agent.

        Args:
            task: Task description for the child agent.
            config: Optional configuration for the child agent.
            agent_id: Optional pre-assigned ID for the agent.

        Returns:
            The spawned child agent.

        Raises:
            PermissionError: If spawning is not allowed.
        """
        if not self.can_spawn_agents():
            raise PermissionError(f"Agent {self.id} is not allowed to spawn agents")

        if len(self.child_agent_ids) >= self.config.max_child_agents:
            raise RuntimeError(f"Agent {self.id} has reached max child agents limit")

        if config is None:
            config = self.config  # Inherit configuration from parent

        new_id = agent_id or str(uuid.uuid4())
        child = BaseAgent(
            id=new_id,
            parent_id=self.id,
            config=config,
        )

        with self._lock:
            self.child_agent_ids.append(new_id)
            self.metrics.spawns += 1

        return child

    def get_info(self) -> Dict[str, Any]:
        """
        Get information about this agent.

        Returns:
            Dictionary containing agent information.
        """
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "last_update": self.last_update.isoformat(),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "config": {
                "backend": self.config.backend,
                "environment": self.config.environment,
                "max_depth": self.config.max_depth,
                "can_spawn": self.config.can_spawn,
            },
            "metrics": {
                "iterations": self.metrics.iterations,
                "total_tokens": self.metrics.total_tokens,
                "total_time_ms": self.metrics.total_time_ms,
                "api_calls": self.metrics.api_calls,
                "errors": self.metrics.errors,
                "spawns": self.metrics.spawns,
            },
            "child_count": len(self.child_agent_ids),
            "result": self.result,
            "error": self.error,
        }

    def update_status(self, new_status: AgentStatus) -> None:
        """
        Update the agent's status.

        Args:
            new_status: New status for the agent.
        """
        self.status = new_status
        self.last_update = datetime.now()

    def terminate(self) -> None:
        """Terminate the agent and all child agents."""
        self.status = AgentStatus.TERMINATED
        self.last_update = datetime.now()

        # Recursively terminate children
        for child_id in self.child_agent_ids:
            pass  # Child termination would be handled by AgentManager

    def __repr__(self) -> str:
        return f"BaseAgent(id={self.id}, status={self.status.value}, parent={self.parent_id})"
