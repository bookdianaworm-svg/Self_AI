"""
Tests for serializers module.
"""

import pytest
from datetime import datetime

from rlm.persistence.serializers import (
    serialize_task,
    deserialize_task,
    serialize_workflow,
    deserialize_workflow,
)
from rlm.tasks.task import Task, TaskStatus, TaskPriority, TaskResult
from rlm.tasks.workflow import (
    Workflow,
    WorkflowStep,
    WorkflowStatus,
    WorkflowStepStatus,
)


class TestSerializers:
    """Test suite for serialization functions."""

    def test_task_roundtrip(self):
        """Create a task, serialize, deserialize, and verify they're equal."""
        original = Task(
            description="Test task description",
            priority=TaskPriority.HIGH,
            metadata={"key": "value"},
        )

        serialized = serialize_task(original)
        restored = deserialize_task(serialized)

        assert restored.id == original.id
        assert restored.description == original.description
        assert restored.priority == original.priority
        assert restored.status == original.status
        assert restored.metadata == original.metadata

    def test_workflow_roundtrip(self):
        """Create a workflow with steps, serialize, deserialize, verify equal."""
        step1 = WorkflowStep(
            name="Step 1",
            description="First step",
            task="Do something",
        )
        step2 = WorkflowStep(
            name="Step 2",
            description="Second step",
            task="Do something else",
            dependencies=[step1.id],
        )

        original = Workflow(
            name="Test Workflow",
            description="A test workflow",
            steps=[step1, step2],
        )

        serialized = serialize_workflow(original)
        restored = deserialize_workflow(serialized)

        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.description == original.description
        assert restored.status == original.status
        assert len(restored.steps) == 2
        assert restored.steps[0].name == "Step 1"
        assert restored.steps[1].name == "Step 2"
        assert restored.steps[1].dependencies[0] == step1.id

    def test_task_with_result(self):
        """Task with TaskResult should serialize and deserialize correctly."""
        original = Task(
            description="Task with result",
            priority=TaskPriority.NORMAL,
        )
        original.mark_completed("Task output data")

        serialized = serialize_task(original)
        restored = deserialize_task(serialized)

        assert restored.status == TaskStatus.COMPLETED
        assert restored.result is not None
        assert restored.result.success is True
        assert restored.result.output == "Task output data"

    def test_task_with_failed_status(self):
        """Task marked as failed should serialize correctly."""
        original = Task(description="Failed task")
        original.mark_failed("Something went wrong")

        serialized = serialize_task(original)
        restored = deserialize_task(serialized)

        assert restored.status == TaskStatus.FAILED
        assert restored.result is not None
        assert restored.result.success is False
        assert restored.result.error == "Something went wrong"

    def test_workflow_with_completed_steps(self):
        """Workflow with completed steps should roundtrip correctly."""
        step = WorkflowStep(
            name="Completed Step",
            task="Do it",
        )

        workflow = Workflow(name="Workflow with results", steps=[step])
        workflow.mark_started()
        workflow.mark_step_completed(step.id, "step output", 100.0)

        serialized = serialize_workflow(workflow)
        restored = deserialize_workflow(serialized)

        assert restored.status == WorkflowStatus.RUNNING
        assert len(restored.steps) == 1
        assert restored.steps[0].status == WorkflowStepStatus.COMPLETED
        assert restored.steps[0].result is not None
        assert restored.steps[0].result.success is True
        assert restored.steps[0].result.output == "step output"

    def test_task_without_optional_fields(self):
        """Task with default/optional fields should serialize correctly."""
        original = Task(description="Minimal task")

        serialized = serialize_task(original)
        restored = deserialize_task(serialized)

        assert restored.description == "Minimal task"
        assert restored.parent_task_id is None
        assert restored.child_task_ids == []
        assert restored.dependencies == []
        assert restored.metadata == {}
        assert restored.retry_count == 0
        assert restored.max_retries == 3

    def test_workflow_without_steps(self):
        """Empty workflow should roundtrip correctly."""
        original = Workflow(name="Empty Workflow")

        serialized = serialize_workflow(original)
        restored = deserialize_workflow(serialized)

        assert restored.name == "Empty Workflow"
        assert restored.steps == []

    def test_task_priority_preserved(self):
        """Task priority should be preserved through roundtrip."""
        for priority in [
            TaskPriority.LOW,
            TaskPriority.NORMAL,
            TaskPriority.HIGH,
            TaskPriority.CRITICAL,
        ]:
            task = Task(description="Priority test", priority=priority)
            serialized = serialize_task(task)
            restored = deserialize_task(serialized)
            assert restored.priority == priority
