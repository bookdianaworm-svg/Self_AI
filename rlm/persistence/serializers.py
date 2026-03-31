"""
Serialization helpers for complex objects.

Provides serialization and deserialization functions for
tasks, workflows, and messages.
"""

from datetime import datetime
from typing import Any, Dict

from rlm.messaging.message_types import (
    Message,
    MessageContent,
    MessagePriority,
    MessageType,
)
from rlm.tasks.task import Task, TaskPriority, TaskResult, TaskStatus
from rlm.tasks.workflow import (
    Workflow,
    WorkflowStatus,
    WorkflowStep,
    WorkflowStepResult,
    WorkflowStepStatus,
)


def serialize_task(task: Task) -> Dict[str, Any]:
    """
    Serialize a Task to dictionary.

    Args:
        task: Task to serialize.

    Returns:
        Dictionary representation of the task.
    """
    result_dict = None
    if task.result is not None:
        result_dict = {
            "task_id": task.result.task_id,
            "success": task.result.success,
            "output": task.result.output,
            "error": task.result.error,
            "execution_time_ms": task.result.execution_time_ms,
            "completed_at": task.result.completed_at.isoformat()
            if task.result.completed_at
            else None,
            "metadata": task.result.metadata,
        }

    return {
        "id": task.id,
        "description": task.description,
        "priority": task.priority.value,
        "status": task.status.value,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "started_at": task.started_at.isoformat() if task.started_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "assigned_agent_id": task.assigned_agent_id,
        "result": result_dict,
        "parent_task_id": task.parent_task_id,
        "child_task_ids": task.child_task_ids,
        "dependencies": task.dependencies,
        "metadata": task.metadata,
        "retry_count": task.retry_count,
        "max_retries": task.max_retries,
        "timeout_seconds": task.timeout_seconds,
    }


def deserialize_task(data: Dict[str, Any]) -> Task:
    """
    Deserialize a Task from dictionary.

    Args:
        data: Dictionary representation of the task.

    Returns:
        Deserialized Task object.
    """
    result = None
    if data.get("result") is not None:
        result_data = data["result"]
        result = TaskResult(
            task_id=result_data.get("task_id", ""),
            success=result_data.get("success", False),
            output=result_data.get("output"),
            error=result_data.get("error"),
            execution_time_ms=result_data.get("execution_time_ms", 0.0),
            completed_at=datetime.fromisoformat(result_data["completed_at"])
            if result_data.get("completed_at")
            else datetime.now(),
            metadata=result_data.get("metadata", {}),
        )

    task = Task(
        id=data.get("id", ""),
        description=data.get("description", ""),
        priority=TaskPriority(data.get("priority", 2)),
        status=TaskStatus(data.get("status", "pending")),
        created_at=datetime.fromisoformat(data["created_at"])
        if data.get("created_at")
        else datetime.now(),
        started_at=datetime.fromisoformat(data["started_at"])
        if data.get("started_at")
        else None,
        completed_at=datetime.fromisoformat(data["completed_at"])
        if data.get("completed_at")
        else None,
        assigned_agent_id=data.get("assigned_agent_id"),
        result=result,
        parent_task_id=data.get("parent_task_id"),
        child_task_ids=data.get("child_task_ids", []),
        dependencies=data.get("dependencies", []),
        metadata=data.get("metadata", {}),
        retry_count=data.get("retry_count", 0),
        max_retries=data.get("max_retries", 3),
        timeout_seconds=data.get("timeout_seconds"),
    )
    return task


def serialize_workflow(workflow: Workflow) -> Dict[str, Any]:
    """
    Serialize a Workflow to dictionary.

    Args:
        workflow: Workflow to serialize.

    Returns:
        Dictionary representation of the workflow.
    """
    steps = []
    for step in workflow.steps:
        step_result = None
        if step.result is not None:
            step_result = {
                "step_id": step.result.step_id,
                "success": step.result.success,
                "output": step.result.output,
                "error": step.result.error,
                "execution_time_ms": step.result.execution_time_ms,
            }
        steps.append(
            {
                "id": step.id,
                "name": step.name,
                "description": step.description,
                "task": step.task,
                "status": step.status.value,
                "dependencies": step.dependencies,
                "result": step_result,
                "agent_id": step.agent_id,
                "started_at": step.started_at.isoformat() if step.started_at else None,
                "completed_at": step.completed_at.isoformat()
                if step.completed_at
                else None,
                "on_success": step.on_success,
                "on_failure": step.on_failure,
                "skip_if": step.skip_if,
            }
        )

    return {
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "status": workflow.status.value,
        "created_at": workflow.created_at.isoformat() if workflow.created_at else None,
        "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
        "completed_at": workflow.completed_at.isoformat()
        if workflow.completed_at
        else None,
        "current_step_index": workflow.current_step_index,
        "steps": steps,
        "metadata": workflow.metadata,
    }


def deserialize_workflow(data: Dict[str, Any]) -> Workflow:
    """
    Deserialize a Workflow from dictionary.

    Args:
        data: Dictionary representation of the workflow.

    Returns:
        Deserialized Workflow object.
    """
    steps = []
    for step_data in data.get("steps", []):
        step_result = None
        if step_data.get("result") is not None:
            result_data = step_data["result"]
            step_result = WorkflowStepResult(
                step_id=result_data.get("step_id", ""),
                success=result_data.get("success", False),
                output=result_data.get("output"),
                error=result_data.get("error"),
                execution_time_ms=result_data.get("execution_time_ms", 0.0),
            )
        step = WorkflowStep(
            id=step_data.get("id", ""),
            name=step_data.get("name", ""),
            description=step_data.get("description", ""),
            task=step_data.get("task", ""),
            status=WorkflowStepStatus(step_data.get("status", "pending")),
            dependencies=step_data.get("dependencies", []),
            result=step_result,
            agent_id=step_data.get("agent_id"),
            started_at=datetime.fromisoformat(step_data["started_at"])
            if step_data.get("started_at")
            else None,
            completed_at=datetime.fromisoformat(step_data["completed_at"])
            if step_data.get("completed_at")
            else None,
            on_success=step_data.get("on_success"),
            on_failure=step_data.get("on_failure"),
            skip_if=step_data.get("skip_if"),
        )
        steps.append(step)

    workflow = Workflow(
        id=data.get("id", ""),
        name=data.get("name", ""),
        description=data.get("description", ""),
        steps=steps,
        status=WorkflowStatus(data.get("status", "pending")),
        created_at=datetime.fromisoformat(data["created_at"])
        if data.get("created_at")
        else datetime.now(),
        started_at=datetime.fromisoformat(data["started_at"])
        if data.get("started_at")
        else None,
        completed_at=datetime.fromisoformat(data["completed_at"])
        if data.get("completed_at")
        else None,
        current_step_index=data.get("current_step_index", 0),
        metadata=data.get("metadata", {}),
    )
    return workflow


def serialize_message(message: Message) -> Dict[str, Any]:
    """
    Serialize a Message to dictionary.

    Args:
        message: Message to serialize.

    Returns:
        Dictionary representation of the message.
    """
    return {
        "id": message.id,
        "sender": message.sender,
        "recipients": message.recipients,
        "type": message.type.value
        if isinstance(message.type, MessageType)
        else message.type,
        "subtype": message.subtype,
        "content": {
            "title": message.content.title,
            "body": message.content.body,
            "attachments": message.content.attachments,
            "metadata": message.content.metadata,
        },
        "timestamp": message.timestamp,
        "priority": message.priority.value
        if isinstance(message.priority, MessagePriority)
        else message.priority,
        "read_by": message.read_by,
        "response_to": message.response_to,
        "status": message.status,
    }


def deserialize_message(data: Dict[str, Any]) -> Message:
    """
    Deserialize a Message from dictionary.

    Args:
        data: Dictionary representation of the message.

    Returns:
        Deserialized Message object.
    """
    content_data = data.get("content", {})
    content = MessageContent(
        title=content_data.get("title", ""),
        body=content_data.get("body", ""),
        attachments=content_data.get("attachments"),
        metadata=content_data.get("metadata"),
    )

    msg_type = data.get("type", "query")
    if isinstance(msg_type, str):
        try:
            msg_type = MessageType(msg_type)
        except ValueError:
            msg_type = MessageType.QUERY

    priority = data.get("priority", "normal")
    if isinstance(priority, str):
        try:
            priority = MessagePriority[priority.upper()]
        except KeyError:
            priority = MessagePriority.NORMAL

    message = Message(
        id=data.get("id", ""),
        sender=data.get("sender", ""),
        recipients=data.get("recipients", []),
        type=msg_type,
        subtype=data.get("subtype"),
        content=content,
        timestamp=data.get("timestamp"),
        priority=priority,
        read_by=data.get("read_by", []),
        response_to=data.get("response_to"),
        status=data.get("status", "sent"),
    )
    return message
