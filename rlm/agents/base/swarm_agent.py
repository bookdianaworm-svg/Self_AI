"""
Swarm Agent and SwarmRLM for continuous spawning during recursion.

This module provides enhanced agent classes that support spawning
child agents during the recursive loop.
"""

import asyncio
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from rlm.agents.base.base_agent import AgentConfig, AgentMetrics, AgentStatus, BaseAgent
from rlm.core.rlm import RLM


@dataclass
class SwarmAgent:
    """
    A swarm agent that can spawn child agents during execution.

    This extends BaseAgent with swarm-specific capabilities like
    spawning, child tracking, and result aggregation.
    """

    id: str
    parent_id: Optional[str] = None
    task: str = ""
    status: AgentStatus = AgentStatus.IDLE
    created_at: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    metrics: AgentMetrics = field(default_factory=AgentMetrics)
    child_agent_ids: List[str] = field(default_factory=list)
    rlm_instance: Optional[RLM] = None
    should_spawn_agents: bool = True

    def spawn_child(
        self,
        task: str,
        backend: Optional[str] = None,
        environment: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> "SwarmAgent":
        """
        Spawn a new child swarm agent.

        Args:
            task: Task description for the child agent.
            backend: Optional backend override for the child.
            environment: Optional environment override for the child.
            agent_id: Optional pre-assigned ID.

        Returns:
            The spawned child SwarmAgent.
        """
        child_id = agent_id or str(uuid.uuid4())

        child = SwarmAgent(
            id=child_id,
            parent_id=self.id,
            task=task,
            status=AgentStatus.IDLE,
            created_at=datetime.now(),
            last_update=datetime.now(),
        )

        # Create RLM instance for child
        child.rlm_instance = RLM(
            backend=backend
            or (self.rlm_instance.backend if self.rlm_instance else "openai"),
            backend_kwargs=self.rlm_instance.backend_kwargs
            if self.rlm_instance
            else None,
            environment=environment
            or (self.rlm_instance.environment_type if self.rlm_instance else "local"),
            environment_kwargs=self.rlm_instance.environment_kwargs
            if self.rlm_instance
            else None,
            depth=0,
            max_depth=1,
            max_iterations=30,
            logger=None,
            verbose=False,
        )

        self.child_agent_ids.append(child_id)
        self.metrics.spawns += 1
        self.last_update = datetime.now()

        return child

    def get_completed_children(self) -> List[tuple[str, Any]]:
        """
        Get results from child agents that have completed.

        Returns:
            List of (agent_id, result) tuples.
        """
        completed = []
        # In a real implementation, this would track child completion
        return completed

    def get_all_descendants(self) -> List[str]:
        """
        Get all descendant agent IDs recursively.

        Returns:
            List of all descendant agent IDs.
        """
        descendants = []
        for child_id in self.child_agent_ids:
            descendants.append(child_id)
            # Recursively get descendants (would need child objects for this)
        return descendants

    def aggregate_results(self) -> Dict[str, Any]:
        """
        Aggregate results from this agent and all children.

        Returns:
            Dictionary containing aggregated results.
        """
        return {
            "agent_id": self.id,
            "task": self.task,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "metrics": {
                "iterations": self.metrics.iterations,
                "total_tokens": self.metrics.total_tokens,
                "errors": self.metrics.errors,
                "spawns": self.metrics.spawns,
            },
            "child_count": len(self.child_agent_ids),
            "children": self.child_agent_ids,
        }

    def __repr__(self) -> str:
        return f"SwarmAgent(id={self.id}, status={self.status.value}, children={len(self.child_agent_ids)})"


class SwarmRLM(RLM):
    """
    Enhanced RLM that supports continuous spawning of agents during its recursive loop.

    This class extends the base RLM with swarm capabilities:
    - Spawning child agents during execution
    - Tracking child agent lifecycle
    - Aggregating results from spawned agents
    - Redux store integration for observability
    """

    def __init__(self, *args, store=None, agent_id=None, agent_name=None, **kwargs):
        """Initialize SwarmRLM with agent tracking.

        Args:
            store: Optional Redux store for observability.
            agent_id: Optional agent ID for this instance.
            agent_name: Optional agent name for display.
        """
        super().__init__(*args, **kwargs)
        self.agents: Dict[str, SwarmAgent] = {}
        self.agent_lock = threading.Lock()
        self.should_spawn_agents = True
        self.store = store
        self.agent_id = agent_id or str(uuid.uuid4())
        self.agent_name = agent_name or f"SwarmAgent-{self.agent_id[:8]}"

    def _dispatch_spawn_event(
        self, parent_id: str, child_id: str, task: str, reason: str
    ):
        """Dispatch spawn event to Redux store if available."""
        if self.store is not None:
            try:
                from rlm.redux.slices.agent_loop_slice import AgentLoopActions

                self.store.dispatch(
                    AgentLoopActions.agent_spawned(
                        parent_agent_id=parent_id,
                        child_agent_id=child_id,
                        child_task=task,
                        reason=reason,
                    )
                )
            except Exception:
                pass

    def spawn_agent(
        self,
        task: str,
        backend: Optional[str] = None,
        environment: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> str:
        """
        Spawn a new agent to work on a specific task.

        Args:
            task: Task description for the new agent.
            backend: Optional backend to use.
            environment: Optional environment to use.
            agent_id: Optional pre-assigned ID.

        Returns:
            The ID of the spawned agent.
        """
        with self.agent_lock:
            agent_id = agent_id or str(uuid.uuid4())

            # Create RLM instance for the agent
            agent_rlm = RLM(
                backend=backend or self.backend,
                backend_kwargs=self.backend_kwargs,
                environment=environment or self.environment_type,
                environment_kwargs=self.environment_kwargs,
                depth=self.depth + 1,
                max_depth=self.max_depth,
                max_iterations=self.max_iterations,
                max_budget=self.max_budget,
                max_timeout=self.max_timeout,
                max_tokens=self.max_tokens,
                max_errors=self.max_errors,
                custom_system_prompt=self.system_prompt,
                logger=self.logger,
                verbose=False,
                persistent=False,
                custom_tools=self.custom_tools,
                custom_sub_tools=self.custom_sub_tools,
                compaction=self.compaction,
                compaction_threshold_pct=self.compaction_threshold_pct,
            )

            # Create swarm agent
            agent = SwarmAgent(
                id=agent_id,
                parent_id=getattr(self, "id", None),
                task=task,
                status=AgentStatus.IDLE,
                created_at=datetime.now(),
                last_update=datetime.now(),
                rlm_instance=agent_rlm,
            )

            self.agents[agent_id] = agent

            # Register child agent with Redux store if available
            if self.store is not None:
                try:
                    from rlm.redux.slices.agent_loop_slice import AgentLoopActions

                    self.store.dispatch(
                        AgentLoopActions.register_agent(
                            agent_id=agent_id,
                            agent_name=f"Child of {self.agent_name}",
                            depth=self.depth + 1,
                            task=task,
                            parent_id=self.agent_id,
                        )
                    )
                except Exception:
                    pass

            # Dispatch spawn event for observability
            self._dispatch_spawn_event(
                parent_id=self.agent_id,
                child_id=agent_id,
                task=task,
                reason="Task delegation to child agent",
            )

            # Start the agent in a separate thread
            agent_thread = threading.Thread(
                target=self._run_agent, args=(agent_id,), daemon=True
            )
            agent_thread.start()

            return agent_id

    def _run_agent(self, agent_id: str) -> None:
        """
        Run an agent's recursive loop in a separate thread.

        Args:
            agent_id: ID of the agent to run.
        """
        agent = self.agents.get(agent_id)
        if not agent:
            return

        agent.status = AgentStatus.EXECUTING
        agent.start_time = datetime.now()
        agent.last_update = datetime.now()

        try:
            if agent.rlm_instance:
                completion_result = agent.rlm_instance.completion(agent.task)
                agent.result = completion_result.response if completion_result else None
            agent.status = AgentStatus.COMPLETED
        except Exception as e:
            agent.error = str(e)
            agent.status = AgentStatus.FAILED
        finally:
            agent.end_time = datetime.now()
            agent.last_update = datetime.now()

    def _check_if_should_spawn_agent(
        self, current_iteration: int, message_history: List[Dict]
    ) -> Optional[str]:
        """
        Determine if a new agent should be spawned based on current state.

        Args:
            current_iteration: Current iteration number.
            message_history: Recent message history.

        Returns:
            Task description for new agent, or None if no spawn needed.
        """
        if not self.should_spawn_agents:
            return None

        # Simple heuristic: if message history is long, consider spawning
        if len(message_history) > 10:
            return "Continue processing the task with the available context."

        return None

    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific agent.

        Args:
            agent_id: ID of the agent.

        Returns:
            Agent information dict, or None if not found.
        """
        agent = self.agents.get(agent_id)
        if not agent:
            return None
        return agent.aggregate_results()

    def get_all_agents(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all agents.

        Returns:
            Dictionary mapping agent IDs to their info.
        """
        return {
            agent_id: agent.aggregate_results()
            for agent_id, agent in self.agents.items()
        }

    def get_active_agents(self) -> List[str]:
        """
        Get IDs of all agents that are currently executing.

        Returns:
            List of active agent IDs.
        """
        return [
            agent_id
            for agent_id, agent in self.agents.items()
            if agent.status == AgentStatus.EXECUTING
        ]

    def terminate_agent(self, agent_id: str) -> bool:
        """
        Terminate a specific agent.

        Args:
            agent_id: ID of the agent to terminate.

        Returns:
            True if terminated, False if not found.
        """
        agent = self.agents.get(agent_id)
        if not agent:
            return False

        agent.status = AgentStatus.TERMINATED
        agent.last_update = datetime.now()
        return True

    def terminate_all_agents(self) -> int:
        """
        Terminate all spawned agents.

        Returns:
            Number of agents terminated.
        """
        count = 0
        for agent in self.agents.values():
            if agent.status == AgentStatus.EXECUTING:
                agent.status = AgentStatus.TERMINATED
                agent.last_update = datetime.now()
                count += 1
        return count
