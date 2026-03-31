"""
Integration helpers for persistence.

Provides classes for saving and loading task queues,
workflows, improvements, and agent states.
"""

from typing import Any, Dict, List, Optional

from rlm.improvements.improvement_registry import (
    ImprovementEntity,
    ImprovementRegistry,
)
from rlm.agents.base.base_agent import AgentConfig, AgentMetrics, AgentStatus
from rlm.agents.base.swarm_agent import SwarmAgent
from rlm.persistence.manager import PersistenceManager
from rlm.persistence.serializers import (
    deserialize_task,
    deserialize_workflow,
    deserialize_message,
    serialize_task,
    serialize_workflow,
    serialize_message,
)
from rlm.tasks.task import Task, TaskResult, TaskPriority, TaskStatus
from rlm.tasks.task_queue import TaskQueue
from rlm.tasks.workflow import Workflow, WorkflowStatus, WorkflowStep
from rlm.messaging.message_types import (
    Message,
    MessageContent,
    MessagePriority,
    MessageType,
)


class TaskQueuePersistence:
    """Save and load task queue state."""

    @staticmethod
    def save(manager: PersistenceManager, queue: TaskQueue) -> None:
        """
        Save task queue state.

        Args:
            manager: PersistenceManager instance.
            queue: TaskQueue to save.
        """
        stats = queue.get_stats()
        manager.save_state("tasks", "_queue_stats", stats)

        for task_id, task in vars(queue).get("_tasks", {}).items():
            task_data = serialize_task(task)
            manager.save_state("tasks", task_id, task_data)

        pending_ids = [t.id for t in queue.get_pending()]
        manager.save_state("tasks", "_pending_ids", {"ids": pending_ids})

    @staticmethod
    def load(manager: PersistenceManager, queue: TaskQueue) -> None:
        """
        Load task queue state.

        Args:
            manager: PersistenceManager instance.
            queue: TaskQueue to load into.
        """
        keys = manager.list_state_keys("tasks")
        for key in keys:
            if key.startswith("_"):
                continue
            data = manager.load_state("tasks", key)
            if data:
                task = deserialize_task(data)
                queue._tasks[task.id] = task


class WorkflowPersistence:
    """Save and load workflow state."""

    @staticmethod
    def save(manager: PersistenceManager, workflows: Dict[str, Workflow]) -> None:
        """
        Save workflows state.

        Args:
            manager: PersistenceManager instance.
            workflows: Dictionary of workflows to save.
        """
        for workflow_id, workflow in workflows.items():
            workflow_data = serialize_workflow(workflow)
            manager.save_state("workflows", workflow_id, workflow_data)

        manager.save_state(
            "workflows", "_workflow_ids", {"ids": list(workflows.keys())}
        )

    @staticmethod
    def load(manager: PersistenceManager) -> Dict[str, Workflow]:
        """
        Load workflows state.

        Args:
            manager: PersistenceManager instance.

        Returns:
            Dictionary of loaded workflows.
        """
        workflows: Dict[str, Workflow] = {}
        keys = manager.list_state_keys("workflows")

        for key in keys:
            if key.startswith("_"):
                continue
            data = manager.load_state("workflows", key)
            if data:
                workflow = deserialize_workflow(data)
                workflows[workflow.id] = workflow

        return workflows


class ImprovementRegistryPersistence:
    """Save and load improvement registry state."""

    @staticmethod
    def save(manager: PersistenceManager, registry: ImprovementRegistry) -> None:
        """
        Save improvement registry state.

        Args:
            manager: PersistenceManager instance.
            registry: ImprovementRegistry to save.
        """
        improvements = registry.get_all()
        for improvement in improvements:
            imp_data = improvement.to_dict()
            manager.save_state("improvements", improvement.id, imp_data)

        manager.save_state(
            "improvements",
            "_improvement_ids",
            {"ids": [imp.id for imp in improvements]},
        )

        manager.save_state(
            "improvements", "_pending_approvals", {"ids": registry._pending_approvals}
        )

        manager.save_state(
            "improvements",
            "_active_improvements",
            {"ids": registry._active_improvements},
        )

        manager.save_state("improvements", "_history", {"ids": registry._history})

        manager.save_state(
            "improvements",
            "_applied_improvements",
            {"ids": registry._applied_improvements},
        )

    @staticmethod
    def load(manager: PersistenceManager, registry: ImprovementRegistry) -> None:
        """
        Load improvement registry state.

        Args:
            manager: PersistenceManager instance.
            registry: ImprovementRegistry to load into.
        """
        keys = manager.list_state_keys("improvements")
        for key in keys:
            if key.startswith("_"):
                continue
            data = manager.load_state("improvements", key)
            if data:
                registry._improvements[data["id"]] = ImprovementEntity(
                    id=data.get("id", ""),
                    title=data.get("title", ""),
                    description=data.get("description", ""),
                )

        pending_data = manager.load_state("improvements", "_pending_approvals")
        if pending_data and "ids" in pending_data:
            registry._pending_approvals = pending_data["ids"]

        active_data = manager.load_state("improvements", "_active_improvements")
        if active_data and "ids" in active_data:
            registry._active_improvements = active_data["ids"]

        history_data = manager.load_state("improvements", "_history")
        if history_data and "ids" in history_data:
            registry._history = history_data["ids"]

        applied_data = manager.load_state("improvements", "_applied_improvements")
        if applied_data and "ids" in applied_data:
            registry._applied_improvements = applied_data["ids"]


class AgentStatePersistence:
    """Save and load agent states."""

    @staticmethod
    def save(manager: PersistenceManager, agents: Dict[str, SwarmAgent]) -> None:
        """
        Save agent states.

        Args:
            manager: PersistenceManager instance.
            agents: Dictionary of agents to save.
        """
        for agent_id, agent in agents.items():
            agent_data = {
                "id": agent.id,
                "parent_id": agent.parent_id,
                "task": agent.task,
                "status": agent.status.value,
                "created_at": agent.created_at.isoformat()
                if agent.created_at
                else None,
                "last_update": agent.last_update.isoformat()
                if agent.last_update
                else None,
                "start_time": agent.start_time.isoformat()
                if agent.start_time
                else None,
                "end_time": agent.end_time.isoformat() if agent.end_time else None,
                "result": agent.result,
                "error": agent.error,
                "metrics": {
                    "iterations": agent.metrics.iterations,
                    "total_tokens": agent.metrics.total_tokens,
                    "total_time_ms": agent.metrics.total_time_ms,
                    "api_calls": agent.metrics.api_calls,
                    "errors": agent.metrics.errors,
                    "spawns": agent.metrics.spawns,
                },
                "child_agent_ids": agent.child_agent_ids,
            }
            manager.save_state("agents", agent_id, agent_data)

        manager.save_state("agents", "_agent_ids", {"ids": list(agents.keys())})

    @staticmethod
    def load(manager: PersistenceManager) -> Dict[str, SwarmAgent]:
        """
        Load agent states.

        Args:
            manager: PersistenceManager instance.

        Returns:
            Dictionary of loaded agents.
        """
        agents: Dict[str, SwarmAgent] = {}
        keys = manager.list_state_keys("agents")

        for key in keys:
            if key.startswith("_"):
                continue
            data = manager.load_state("agents", key)
            if data:
                metrics_data = data.get("metrics", {})
                metrics = AgentMetrics(
                    iterations=metrics_data.get("iterations", 0),
                    total_tokens=metrics_data.get("total_tokens", 0),
                    total_time_ms=metrics_data.get("total_time_ms", 0.0),
                    api_calls=metrics_data.get("api_calls", 0),
                    errors=metrics_data.get("errors", 0),
                    spawns=metrics_data.get("spawns", 0),
                )

                from datetime import datetime

                agent = SwarmAgent(
                    id=data.get("id", ""),
                    parent_id=data.get("parent_id"),
                    task=data.get("task", ""),
                    status=AgentStatus(data.get("status", "idle")),
                    created_at=datetime.fromisoformat(data["created_at"])
                    if data.get("created_at")
                    else datetime.now(),
                    last_update=datetime.fromisoformat(data["last_update"])
                    if data.get("last_update")
                    else datetime.now(),
                    start_time=datetime.fromisoformat(data["start_time"])
                    if data.get("start_time")
                    else None,
                    end_time=datetime.fromisoformat(data["end_time"])
                    if data.get("end_time")
                    else None,
                    result=data.get("result"),
                    error=data.get("error"),
                    metrics=metrics,
                    child_agent_ids=data.get("child_agent_ids", []),
                )
                agents[agent.id] = agent

        return agents
