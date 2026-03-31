"""
Workflow module for multi-step task orchestration.

This module provides the Workflow class for defining
and executing multi-step workflows with dependencies.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import uuid

from rlm.tasks.task import Task, TaskStatus


class WorkflowStatus(Enum):
    """Status of a workflow."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class WorkflowStepStatus(Enum):
    """Status of a workflow step."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowStepResult:
    """Result of a workflow step."""

    step_id: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0


@dataclass
class WorkflowStep:
    """
    A single step in a workflow.

    Steps are executed in order, with optional branching
    and parallel execution support.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    task: str = ""  # Task description for the agent
    status: WorkflowStepStatus = WorkflowStepStatus.PENDING
    dependencies: List[str] = field(
        default_factory=list
    )  # Step IDs that must complete first
    result: Optional[WorkflowStepResult] = None
    agent_id: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    on_success: Optional[str] = None  # Next step ID on success
    on_failure: Optional[str] = None  # Next step ID on failure
    skip_if: Optional[str] = None  # Condition to skip this step

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "task": self.task,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "result": {
                "success": self.result.success if self.result else None,
                "output": self.result.output if self.result else None,
                "error": self.result.error if self.result else None,
            }
            if self.result
            else None,
            "agent_id": self.agent_id,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat()
            if self.completed_at
            else None,
            "on_success": self.on_success,
            "on_failure": self.on_failure,
            "skip_if": self.skip_if,
        }


@dataclass
class Workflow:
    """
    A multi-step workflow for complex task execution.

    Workflows consist of steps that are executed in order
    with support for branching, parallel execution, and
    conditional logic.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    steps: List[WorkflowStep] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    current_step_index: int = 0
    results: Dict[str, WorkflowStepResult] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_step(self, step_id: str) -> Optional[WorkflowStep]:
        """Get a step by ID."""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None

    def get_step_by_name(self, name: str) -> Optional[WorkflowStep]:
        """Get a step by name."""
        for step in self.steps:
            if step.name == name:
                return step
        return None

    def get_next_step(self, current_step: WorkflowStep) -> Optional[WorkflowStep]:
        """Get the next step based on current step result."""
        if current_step.result and not current_step.result.success:
            # On failure, go to on_failure step if defined
            if current_step.on_failure:
                return self.get_step(current_step.on_failure)
        else:
            # On success, go to on_success step if defined
            if current_step.on_success:
                return self.get_step(current_step.on_success)

        # Otherwise, go to next sequential step
        try:
            current_index = self.steps.index(current_step)
            if current_index + 1 < len(self.steps):
                return self.steps[current_index + 1]
        except ValueError:
            pass

        return None

    def is_step_ready(self, step: WorkflowStep) -> bool:
        """Check if a step is ready to execute."""
        if step.status != WorkflowStepStatus.PENDING:
            return False

        # Check dependencies
        for dep_id in step.dependencies:
            dep_step = self.get_step(dep_id)
            if not dep_step:
                continue
            if dep_step.status != WorkflowStepStatus.COMPLETED:
                return False

        return True

    def get_ready_steps(self) -> List[WorkflowStep]:
        """Get all steps that are ready to execute."""
        return [step for step in self.steps if self.is_step_ready(step)]

    def mark_started(self) -> None:
        """Mark workflow as started."""
        self.status = WorkflowStatus.RUNNING
        self.started_at = datetime.now()

    def mark_completed(self) -> None:
        """Mark workflow as completed."""
        self.status = WorkflowStatus.COMPLETED
        self.completed_at = datetime.now()

    def mark_failed(self) -> None:
        """Mark workflow as failed."""
        self.status = WorkflowStatus.FAILED
        self.completed_at = datetime.now()

    def mark_cancelled(self) -> None:
        """Mark workflow as cancelled."""
        self.status = WorkflowStatus.CANCELLED
        self.completed_at = datetime.now()

    def mark_step_started(self, step_id: str, agent_id: str) -> bool:
        """Mark a step as started."""
        step = self.get_step(step_id)
        if not step:
            return False
        step.status = WorkflowStepStatus.RUNNING
        step.agent_id = agent_id
        step.started_at = datetime.now()
        return True

    def mark_step_completed(
        self, step_id: str, output: Any, execution_time_ms: float
    ) -> bool:
        """Mark a step as completed."""
        step = self.get_step(step_id)
        if not step:
            return False
        step.status = WorkflowStepStatus.COMPLETED
        step.completed_at = datetime.now()
        step.result = WorkflowStepResult(
            step_id=step_id,
            success=True,
            output=output,
            execution_time_ms=execution_time_ms,
        )
        self.results[step_id] = step.result
        return True

    def mark_step_failed(
        self, step_id: str, error: str, execution_time_ms: float
    ) -> bool:
        """Mark a step as failed."""
        step = self.get_step(step_id)
        if not step:
            return False
        step.status = WorkflowStepStatus.FAILED
        step.completed_at = datetime.now()
        step.result = WorkflowStepResult(
            step_id=step_id,
            success=False,
            error=error,
            execution_time_ms=execution_time_ms,
        )
        self.results[step_id] = step.result
        return True

    def mark_step_skipped(self, step_id: str) -> bool:
        """Mark a step as skipped."""
        step = self.get_step(step_id)
        if not step:
            return False
        step.status = WorkflowStepStatus.SKIPPED
        step.completed_at = datetime.now()
        return True

    def get_results_summary(self) -> Dict[str, Any]:
        """Get a summary of all step results."""
        total_steps = len(self.steps)
        completed = sum(
            1 for s in self.steps if s.status == WorkflowStepStatus.COMPLETED
        )
        failed = sum(1 for s in self.steps if s.status == WorkflowStepStatus.FAILED)
        skipped = sum(1 for s in self.steps if s.status == WorkflowStepStatus.SKIPPED)

        total_time = sum(r.execution_time_ms for r in self.results.values())

        return {
            "total_steps": total_steps,
            "completed": completed,
            "failed": failed,
            "skipped": skipped,
            "pending": total_steps - completed - failed - skipped,
            "total_time_ms": total_time,
            "success": failed == 0 and completed == total_steps,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat()
            if self.completed_at
            else None,
            "current_step_index": self.current_step_index,
            "steps": [s.to_dict() for s in self.steps],
            "results_summary": self.get_results_summary(),
            "metadata": self.metadata,
        }
