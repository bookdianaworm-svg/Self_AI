"""
Redux slice for agent loop observability.

Captures full LLM I/O, REPL executions, chain-of-thought, and agent spawning
events for real-time monitoring and historical analysis.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time
import uuid


class AgentLoopStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class LLMCallType(Enum):
    COMPLETION = "completion"
    SUBCALL = "subcall"
    LLM_QUERY = "llm_query"
    RLM_QUERY = "rlm_query"


@dataclass
class LLMCallRecord:
    """Single LLM call (prompt -> response)."""

    call_id: str
    agent_id: str
    parent_call_id: Optional[str]
    depth: int
    model: str
    prompt: str
    response: str
    input_tokens: int
    output_tokens: int
    cost: Optional[float]
    execution_time: float
    call_type: str
    success: bool
    error: Optional[str]
    timestamp: float


@dataclass
class REPLExecutionRecord:
    """Single REPL code block execution."""

    execution_id: str
    agent_id: str
    parent_call_id: Optional[str]
    code: str
    stdout: str
    stderr: str
    execution_time: float
    success: bool
    error: Optional[str]
    return_value_preview: Optional[str]
    llm_calls_made: List[str]
    timestamp: float


@dataclass
class IterationRecord:
    """Single RLM iteration."""

    iteration_id: str
    agent_id: str
    iteration_number: int
    depth: int
    prompt: str
    response: str
    code_blocks: List[Dict[str, Any]]
    final_answer: Optional[str]
    execution_time: float
    timestamp: float


@dataclass
class SpawningEvent:
    """Agent spawned another agent."""

    event_id: str
    parent_agent_id: str
    child_agent_id: str
    child_task: str
    reason: str
    timestamp: float


@dataclass
class ChainThoughtStep:
    """Chain-of-thought reasoning step."""

    step_id: str
    agent_id: str
    iteration: int
    thought: str
    action: str
    context: Dict[str, Any]
    timestamp: float


@dataclass
class AgentLoopState:
    """Full loop state for an agent."""

    agent_id: str
    agent_name: str
    status: AgentLoopStatus
    depth: int
    current_task: str
    started_at: float
    parent_id: Optional[str]
    iterations: List[IterationRecord] = field(default_factory=list)
    llm_calls: List[LLMCallRecord] = field(default_factory=list)
    repl_history: List[REPLExecutionRecord] = field(default_factory=list)
    spawning_events: List[SpawningEvent] = field(default_factory=list)
    chain_of_thought: List[ChainThoughtStep] = field(default_factory=list)
    total_llm_calls: int = 0
    total_repl_executions: int = 0
    successful_repl_executions: int = 0
    failed_repl_executions: int = 0


@dataclass
class AgentLoopSlice:
    """Redux slice for agent loop observability."""

    agents: Dict[str, AgentLoopState] = field(default_factory=dict)
    active_agent_id: Optional[str] = None
    call_index: int = 0
    repl_index: int = 0
    iteration_index: int = 0
    chain_thought_index: int = 0
    streaming_mode: bool = True
    max_history_per_agent: int = 1000
    paused_agents: List[str] = field(default_factory=list)
    total_agents: int = 0


def generate_call_id(slice_state: AgentLoopSlice) -> str:
    """Generate a unique call ID."""
    call_id = f"call-{slice_state.call_index:06d}"
    slice_state.call_index += 1
    return call_id


def generate_execution_id(slice_state: AgentLoopSlice) -> str:
    """Generate a unique execution ID."""
    exec_id = f"exec-{slice_state.repl_index:06d}"
    slice_state.repl_index += 1
    return exec_id


def generate_iteration_id(slice_state: AgentLoopSlice) -> str:
    """Generate a unique iteration ID."""
    iter_id = f"iter-{slice_state.iteration_index:06d}"
    slice_state.iteration_index += 1
    return iter_id


def generate_chain_thought_id(slice_state: AgentLoopSlice) -> str:
    """Generate a unique chain thought ID."""
    cot_id = f"cot-{slice_state.chain_thought_index:06d}"
    slice_state.chain_thought_index += 1
    return cot_id


class AgentLoopActions:
    @staticmethod
    def register_agent(
        agent_id: str,
        agent_name: str,
        depth: int,
        task: str,
        parent_id: Optional[str] = None,
    ) -> dict:
        return {
            "type": "agent_loop/register_agent",
            "payload": {
                "agent_id": agent_id,
                "agent_name": agent_name,
                "depth": depth,
                "task": task,
                "parent_id": parent_id,
                "timestamp": time.time(),
            },
        }

    @staticmethod
    def unregister_agent(agent_id: str) -> dict:
        return {
            "type": "agent_loop/unregister_agent",
            "payload": {"agent_id": agent_id},
        }

    @staticmethod
    def set_active_agent(agent_id: Optional[str]) -> dict:
        return {
            "type": "agent_loop/set_active_agent",
            "payload": {"agent_id": agent_id},
        }

    @staticmethod
    def update_agent_status(agent_id: str, status: AgentLoopStatus) -> dict:
        return {
            "type": "agent_loop/update_status",
            "payload": {"agent_id": agent_id, "status": status.value},
        }

    @staticmethod
    def update_agent_task(agent_id: str, task: str) -> dict:
        return {
            "type": "agent_loop/update_task",
            "payload": {"agent_id": agent_id, "task": task},
        }

    @staticmethod
    def llm_call_started(
        agent_id: str,
        call_id: str,
        parent_call_id: Optional[str],
        depth: int,
        model: str,
        prompt: str,
        call_type: str,
    ) -> dict:
        return {
            "type": "agent_loop/llm_call_started",
            "payload": {
                "call_id": call_id,
                "agent_id": agent_id,
                "parent_call_id": parent_call_id,
                "depth": depth,
                "model": model,
                "prompt": prompt,
                "call_type": call_type,
                "timestamp": time.time(),
            },
        }

    @staticmethod
    def llm_call_completed(
        agent_id: str,
        call_id: str,
        response: str,
        input_tokens: int,
        output_tokens: int,
        cost: Optional[float],
        execution_time: float,
        success: bool,
        error: Optional[str] = None,
    ) -> dict:
        return {
            "type": "agent_loop/llm_call_completed",
            "payload": {
                "call_id": call_id,
                "agent_id": agent_id,
                "response": response,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "execution_time": execution_time,
                "success": success,
                "error": error,
                "timestamp": time.time(),
            },
        }

    @staticmethod
    def repl_execution_started(
        agent_id: str, execution_id: str, parent_call_id: Optional[str], code: str
    ) -> dict:
        return {
            "type": "agent_loop/repl_execution_started",
            "payload": {
                "execution_id": execution_id,
                "agent_id": agent_id,
                "parent_call_id": parent_call_id,
                "code": code,
                "timestamp": time.time(),
            },
        }

    @staticmethod
    def repl_execution_completed(
        agent_id: str,
        execution_id: str,
        stdout: str,
        stderr: str,
        execution_time: float,
        success: bool,
        error: Optional[str],
        return_value_preview: Optional[str],
        llm_calls_made: List[str],
    ) -> dict:
        return {
            "type": "agent_loop/repl_execution_completed",
            "payload": {
                "execution_id": execution_id,
                "agent_id": agent_id,
                "stdout": stdout,
                "stderr": stderr,
                "execution_time": execution_time,
                "success": success,
                "error": error,
                "return_value_preview": return_value_preview,
                "llm_calls_made": llm_calls_made,
                "timestamp": time.time(),
            },
        }

    @staticmethod
    def iteration_started(
        agent_id: str, iteration_id: str, iteration_number: int, depth: int, prompt: str
    ) -> dict:
        return {
            "type": "agent_loop/iteration_started",
            "payload": {
                "iteration_id": iteration_id,
                "agent_id": agent_id,
                "iteration_number": iteration_number,
                "depth": depth,
                "prompt": prompt,
                "timestamp": time.time(),
            },
        }

    @staticmethod
    def iteration_completed(
        agent_id: str,
        iteration_id: str,
        response: str,
        code_blocks: List[Dict[str, Any]],
        final_answer: Optional[str],
        execution_time: float,
    ) -> dict:
        return {
            "type": "agent_loop/iteration_completed",
            "payload": {
                "iteration_id": iteration_id,
                "agent_id": agent_id,
                "response": response,
                "code_blocks": code_blocks,
                "final_answer": final_answer,
                "execution_time": execution_time,
                "timestamp": time.time(),
            },
        }

    @staticmethod
    def agent_spawned(
        parent_agent_id: str, child_agent_id: str, child_task: str, reason: str
    ) -> dict:
        return {
            "type": "agent_loop/agent_spawned",
            "payload": {
                "event_id": str(uuid.uuid4()),
                "parent_agent_id": parent_agent_id,
                "child_agent_id": child_agent_id,
                "child_task": child_task,
                "reason": reason,
                "timestamp": time.time(),
            },
        }

    @staticmethod
    def chain_thought_added(
        agent_id: str,
        step_id: str,
        iteration: int,
        thought: str,
        action: str,
        context: Dict[str, Any],
    ) -> dict:
        return {
            "type": "agent_loop/chain_thought_added",
            "payload": {
                "step_id": step_id,
                "agent_id": agent_id,
                "iteration": iteration,
                "thought": thought,
                "action": action,
                "context": context,
                "timestamp": time.time(),
            },
        }

    @staticmethod
    def set_streaming_mode(enabled: bool) -> dict:
        return {
            "type": "agent_loop/set_streaming_mode",
            "payload": {"enabled": enabled},
        }

    @staticmethod
    def pause_agent_streaming(agent_id: str) -> dict:
        return {"type": "agent_loop/pause_streaming", "payload": {"agent_id": agent_id}}

    @staticmethod
    def resume_agent_streaming(agent_id: str) -> dict:
        return {
            "type": "agent_loop/resume_streaming",
            "payload": {"agent_id": agent_id},
        }

    @staticmethod
    def clear_agent_history(agent_id: str) -> dict:
        return {"type": "agent_loop/clear_history", "payload": {"agent_id": agent_id}}


def agent_loop_reducer(state: AgentLoopSlice, action: dict) -> AgentLoopSlice:
    """Reducer for agent loop slice."""
    action_type = action.get("type", "")
    payload = action.get("payload", {})

    if action_type == "agent_loop/register_agent":
        agent_id = payload.get("agent_id")
        if agent_id not in state.agents:
            state.agents[agent_id] = AgentLoopState(
                agent_id=agent_id,
                agent_name=payload.get("agent_name", agent_id),
                status=AgentLoopStatus.RUNNING,
                depth=payload.get("depth", 0),
                current_task=payload.get("task", ""),
                started_at=payload.get("timestamp", time.time()),
                parent_id=payload.get("parent_id"),
            )
            state.total_agents += 1
            state.active_agent_id = agent_id
        return state

    elif action_type == "agent_loop/unregister_agent":
        agent_id = payload.get("agent_id")
        if agent_id in state.agents:
            del state.agents[agent_id]
            if state.active_agent_id == agent_id:
                state.active_agent_id = next(iter(state.agents.keys()), None)
        return state

    elif action_type == "agent_loop/set_active_agent":
        state.active_agent_id = payload.get("agent_id")
        return state

    elif action_type == "agent_loop/update_status":
        agent_id = payload.get("agent_id")
        if agent_id in state.agents:
            status_str = payload.get("status")
            state.agents[agent_id].status = AgentLoopStatus(status_str)
        return state

    elif action_type == "agent_loop/update_task":
        agent_id = payload.get("agent_id")
        if agent_id in state.agents:
            state.agents[agent_id].current_task = payload.get("task", "")
        return state

    elif action_type == "agent_loop/llm_call_started":
        agent_id = payload.get("agent_id")
        if agent_id in state.agents:
            call_record = LLMCallRecord(
                call_id=payload.get("call_id"),
                agent_id=agent_id,
                parent_call_id=payload.get("parent_call_id"),
                depth=payload.get("depth", 0),
                model=payload.get("model", "unknown"),
                prompt=payload.get("prompt", ""),
                response="",
                input_tokens=0,
                output_tokens=0,
                cost=None,
                execution_time=0.0,
                call_type=payload.get("call_type", "completion"),
                success=True,
                error=None,
                timestamp=payload.get("timestamp", time.time()),
            )
            state.agents[agent_id].llm_calls.append(call_record)
            state.agents[agent_id].total_llm_calls += 1
        return state

    elif action_type == "agent_loop/llm_call_completed":
        agent_id = payload.get("agent_id")
        call_id = payload.get("call_id")
        if agent_id in state.agents:
            for call in reversed(state.agents[agent_id].llm_calls):
                if call.call_id == call_id:
                    call.response = payload.get("response", "")
                    call.input_tokens = payload.get("input_tokens", 0)
                    call.output_tokens = payload.get("output_tokens", 0)
                    call.cost = payload.get("cost")
                    call.execution_time = payload.get("execution_time", 0.0)
                    call.success = payload.get("success", True)
                    call.error = payload.get("error")
                    break
        return state

    elif action_type == "agent_loop/repl_execution_started":
        agent_id = payload.get("agent_id")
        if agent_id in state.agents:
            exec_record = REPLExecutionRecord(
                execution_id=payload.get("execution_id"),
                agent_id=agent_id,
                parent_call_id=payload.get("parent_call_id"),
                code=payload.get("code", ""),
                stdout="",
                stderr="",
                execution_time=0.0,
                success=True,
                error=None,
                return_value_preview=None,
                llm_calls_made=[],
                timestamp=payload.get("timestamp", time.time()),
            )
            state.agents[agent_id].repl_history.append(exec_record)
            state.agents[agent_id].total_repl_executions += 1
        return state

    elif action_type == "agent_loop/repl_execution_completed":
        agent_id = payload.get("agent_id")
        execution_id = payload.get("execution_id")
        if agent_id in state.agents:
            for exec_record in reversed(state.agents[agent_id].repl_history):
                if exec_record.execution_id == execution_id:
                    exec_record.stdout = payload.get("stdout", "")
                    exec_record.stderr = payload.get("stderr", "")
                    exec_record.execution_time = payload.get("execution_time", 0.0)
                    exec_record.success = payload.get("success", True)
                    exec_record.error = payload.get("error")
                    exec_record.return_value_preview = payload.get(
                        "return_value_preview"
                    )
                    exec_record.llm_calls_made = payload.get("llm_calls_made", [])
                    if exec_record.success:
                        state.agents[agent_id].successful_repl_executions += 1
                    else:
                        state.agents[agent_id].failed_repl_executions += 1
                    break
        return state

    elif action_type == "agent_loop/iteration_started":
        agent_id = payload.get("agent_id")
        if agent_id in state.agents:
            iteration = IterationRecord(
                iteration_id=payload.get("iteration_id"),
                agent_id=agent_id,
                iteration_number=payload.get("iteration_number", 0),
                depth=payload.get("depth", 0),
                prompt=payload.get("prompt", ""),
                response="",
                code_blocks=[],
                final_answer=None,
                execution_time=0.0,
                timestamp=payload.get("timestamp", time.time()),
            )
            state.agents[agent_id].iterations.append(iteration)
        return state

    elif action_type == "agent_loop/iteration_completed":
        agent_id = payload.get("agent_id")
        iteration_id = payload.get("iteration_id")
        if agent_id in state.agents:
            for iteration in reversed(state.agents[agent_id].iterations):
                if iteration.iteration_id == iteration_id:
                    iteration.response = payload.get("response", "")
                    iteration.code_blocks = payload.get("code_blocks", [])
                    iteration.final_answer = payload.get("final_answer")
                    iteration.execution_time = payload.get("execution_time", 0.0)
                    break
        return state

    elif action_type == "agent_loop/agent_spawned":
        parent_agent_id = payload.get("parent_agent_id")
        if parent_agent_id in state.agents:
            spawning_event = SpawningEvent(
                event_id=payload.get("event_id"),
                parent_agent_id=parent_agent_id,
                child_agent_id=payload.get("child_agent_id"),
                child_task=payload.get("child_task", ""),
                reason=payload.get("reason", ""),
                timestamp=payload.get("timestamp", time.time()),
            )
            state.agents[parent_agent_id].spawning_events.append(spawning_event)
        return state

    elif action_type == "agent_loop/chain_thought_added":
        agent_id = payload.get("agent_id")
        if agent_id in state.agents:
            step = ChainThoughtStep(
                step_id=payload.get("step_id"),
                agent_id=agent_id,
                iteration=payload.get("iteration", 0),
                thought=payload.get("thought", ""),
                action=payload.get("action", ""),
                context=payload.get("context", {}),
                timestamp=payload.get("timestamp", time.time()),
            )
            state.agents[agent_id].chain_of_thought.append(step)
        return state

    elif action_type == "agent_loop/set_streaming_mode":
        state.streaming_mode = payload.get("enabled", True)
        return state

    elif action_type == "agent_loop/pause_streaming":
        agent_id = payload.get("agent_id")
        if agent_id not in state.paused_agents:
            state.paused_agents.append(agent_id)
        return state

    elif action_type == "agent_loop/resume_streaming":
        agent_id = payload.get("agent_id")
        if agent_id in state.paused_agents:
            state.paused_agents.remove(agent_id)
        return state

    elif action_type == "agent_loop/clear_history":
        agent_id = payload.get("agent_id")
        if agent_id in state.agents:
            state.agents[agent_id].iterations.clear()
            state.agents[agent_id].llm_calls.clear()
            state.agents[agent_id].repl_history.clear()
            state.agents[agent_id].chain_of_thought.clear()
        return state

    return state
