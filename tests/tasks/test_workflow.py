"""
Tests for Workflow and WorkflowStep classes.
"""

import pytest
from datetime import datetime

from rlm.tasks.workflow import (
    Workflow,
    WorkflowStep,
    WorkflowStatus,
    WorkflowStepStatus,
    WorkflowStepResult,
)


class TestWorkflow:
    """Test suite for Workflow class."""

    def test_workflow_creation(self):
        """Test workflow creation with default values."""
        workflow = Workflow(name="Test Workflow", description="A test workflow")

        assert workflow.name == "Test Workflow"
        assert workflow.description == "A test workflow"
        assert workflow.status == WorkflowStatus.PENDING
        assert workflow.id is not None
        assert workflow.steps == []
        assert workflow.current_step_index == 0
        assert workflow.created_at is not None
        assert workflow.started_at is None
        assert workflow.completed_at is None

    def test_add_step(self):
        """Test adding steps to a workflow."""
        workflow = Workflow(name="Workflow with steps")
        step = WorkflowStep(name="Step 1", task="Do something")

        workflow.steps.append(step)

        assert len(workflow.steps) == 1
        assert workflow.steps[0].name == "Step 1"

    def test_step_status_tracking(self):
        """Test tracking step status through workflow lifecycle."""
        workflow = Workflow(name="Status test")
        step1 = WorkflowStep(name="Step 1", task="Task 1")
        step2 = WorkflowStep(name="Step 2", task="Task 2", dependencies=[step1.id])

        workflow.steps = [step1, step2]

        assert step1.status == WorkflowStepStatus.PENDING
        assert step2.status == WorkflowStepStatus.PENDING

        workflow.mark_step_started(step1.id, "agent_1")
        assert step1.status == WorkflowStepStatus.RUNNING
        assert step1.agent_id == "agent_1"

        workflow.mark_step_completed(step1.id, "output 1", 100.0)
        assert step1.status == WorkflowStepStatus.COMPLETED
        assert step1.result is not None
        assert step1.result.success is True

    def test_workflow_status_from_steps(self):
        """Test workflow status reflects step statuses."""
        workflow = Workflow(name="Status from steps")
        step1 = WorkflowStep(name="Step 1", task="Task 1")
        step2 = WorkflowStep(name="Step 2", task="Task 2")

        workflow.steps = [step1, step2]

        assert workflow.status == WorkflowStatus.PENDING

        workflow.mark_started()
        assert workflow.status == WorkflowStatus.RUNNING

        workflow.mark_step_completed(step1.id, "output", 50.0)
        assert workflow.status == WorkflowStatus.RUNNING

        workflow.mark_step_completed(step2.id, "output", 50.0)
        workflow.mark_completed()
        assert workflow.status == WorkflowStatus.COMPLETED

    def test_workflow_to_dict(self):
        """Test converting workflow to dictionary."""
        workflow = Workflow(
            id="wf_123",
            name="Dict test",
            description="Testing to_dict",
        )

        workflow_dict = workflow.to_dict()

        assert workflow_dict["id"] == "wf_123"
        assert workflow_dict["name"] == "Dict test"
        assert workflow_dict["description"] == "Testing to_dict"
        assert workflow_dict["status"] == "pending"

    def test_get_step(self):
        """Test retrieving step by ID."""
        step = WorkflowStep(name="Find me")
        workflow = Workflow(name="Find step test", steps=[step])

        found = workflow.get_step(step.id)
        assert found is not None
        assert found.id == step.id

    def test_get_step_by_name(self):
        """Test retrieving step by name."""
        step = WorkflowStep(name="Unique Step Name")
        workflow = Workflow(name="Find by name test", steps=[step])

        found = workflow.get_step_by_name("Unique Step Name")
        assert found is not None
        assert found.name == "Unique Step Name"

        not_found = workflow.get_step_by_name("Nonexistent")
        assert not_found is None

    def test_get_next_step(self):
        """Test getting next step in sequence."""
        step1 = WorkflowStep(name="Step 1", task="Task 1")
        step2 = WorkflowStep(name="Step 2", task="Task 2")
        step3 = WorkflowStep(name="Step 3", task="Task 3")

        workflow = Workflow(name="Next step test", steps=[step1, step2, step3])

        next_step = workflow.get_next_step(step1)
        assert next_step is not None
        assert next_step.name == "Step 2"

        next_step2 = workflow.get_next_step(step2)
        assert next_step2 is not None
        assert next_step2.name == "Step 3"

        next_step3 = workflow.get_next_step(step3)
        assert next_step3 is None

    def test_mark_step_failed(self):
        """Test marking a step as failed."""
        step = WorkflowStep(name="Failing step", task="This will fail")
        workflow = Workflow(name="Fail test", steps=[step])

        workflow.mark_step_failed(step.id, "Connection error", 50.0)

        assert step.status == WorkflowStepStatus.FAILED
        assert step.result is not None
        assert step.result.success is False
        assert step.result.error == "Connection error"

    def test_mark_step_skipped(self):
        """Test skipping a step."""
        step = WorkflowStep(name="Skipped step", task="Skip me")
        workflow = Workflow(name="Skip test", steps=[step])

        workflow.mark_step_skipped(step.id)

        assert step.status == WorkflowStepStatus.SKIPPED

    def test_is_step_ready(self):
        """Test checking if step is ready to execute."""
        step1 = WorkflowStep(name="Step 1", task="Task 1")
        step2 = WorkflowStep(name="Step 2", task="Task 2", dependencies=[step1.id])

        workflow = Workflow(name="Ready test", steps=[step1, step2])

        assert workflow.is_step_ready(step1) is True
        assert workflow.is_step_ready(step2) is False

        workflow.mark_step_completed(step1.id, "done", 50.0)
        assert workflow.is_step_ready(step2) is True

    def test_get_ready_steps(self):
        """Test getting all ready steps."""
        step1 = WorkflowStep(name="Step 1", task="Task 1")
        step2 = WorkflowStep(name="Step 2", task="Task 2", dependencies=[step1.id])
        step3 = WorkflowStep(name="Step 3", task="Task 3")

        workflow = Workflow(name="Ready steps test", steps=[step1, step2, step3])

        ready = workflow.get_ready_steps()
        assert len(ready) == 2
        assert step1 in ready
        assert step3 in ready
        assert step2 not in ready

    def test_get_results_summary(self):
        """Test getting workflow results summary."""
        step1 = WorkflowStep(name="Step 1", task="Task 1")
        step2 = WorkflowStep(name="Step 2", task="Task 2")
        step3 = WorkflowStep(name="Step 3", task="Task 3")

        workflow = Workflow(name="Summary test", steps=[step1, step2, step3])

        workflow.mark_step_completed(step1.id, "out1", 100.0)
        workflow.mark_step_failed(step2.id, "error", 50.0)

        summary = workflow.get_results_summary()

        assert summary["total_steps"] == 3
        assert summary["completed"] == 1
        assert summary["failed"] == 1
        assert summary["skipped"] == 0
        assert summary["pending"] == 1
        assert summary["success"] is False

    def test_workflow_mark_completed(self):
        """Test marking workflow as completed."""
        workflow = Workflow(name="Complete test")
        workflow.mark_started()

        workflow.mark_completed()

        assert workflow.status == WorkflowStatus.COMPLETED
        assert workflow.completed_at is not None

    def test_workflow_mark_failed(self):
        """Test marking workflow as failed."""
        workflow = Workflow(name="Fail test")
        workflow.mark_started()

        workflow.mark_failed()

        assert workflow.status == WorkflowStatus.FAILED
        assert workflow.completed_at is not None

    def test_workflow_mark_cancelled(self):
        """Test cancelling a workflow."""
        workflow = Workflow(name="Cancel test")

        workflow.mark_cancelled()

        assert workflow.status == WorkflowStatus.CANCELLED
        assert workflow.completed_at is not None
