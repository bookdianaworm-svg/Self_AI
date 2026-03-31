"""
Redux slice for empirical fuzzing loop state management.

This module provides state management for the Empirical Fuzzing Loop (Black-Box Discovery),
handling automata learning and finite state machine synthesis.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum
import time


class FuzzingStatus(Enum):
    """Status of a fuzzing task."""

    IDLE = "idle"
    INITIALIZING = "initializing"
    LEARNING = "learning"
    HYPOTHESIZING = "hypothesizing"
    EQUIVALENCE_TESTING = "equivalence_testing"
    REFINING = "refining"
    COMPLETED = "completed"
    TIMEOUT = "timeout"
    ERROR = "error"


class SandboxEnvironment(Enum):
    """Type of sandbox environment."""

    DOCKER = "docker"
    MODAL = "modal"
    LOCAL = "local"
    AIR_GAPPED = "air_gapped"


class SandboxResponse(Enum):
    """Response type from sandbox."""

    VALID_TRANSITION = "valid_transition"
    REJECTED = "rejected"
    TIMEOUT = "timeout"
    CRASH = "crash"
    UNKNOWN = "unknown"


@dataclass
class InputSpace:
    """Definition of the input space for fuzzing."""

    input_type: str
    lower_bound: int
    upper_bound: int
    valid_inputs: List[str] = field(default_factory=list)


@dataclass
class MembershipQuery:
    """A membership query to the sandbox."""

    id: str
    input_sequence: List[str]
    response: SandboxResponse
    new_state_discovered: bool
    timestamp: float = field(default_factory=time.time)


@dataclass
class FSMState:
    """A state in the discovered finite state machine."""

    name: str
    is_accepting: bool = False
    is_initial: bool = False


@dataclass
class FSMTransition:
    """A transition in the discovered finite state machine."""

    from_state: str
    to_state: str
    input_symbol: str
    is_learned: bool = False


@dataclass
class DiscoveredFSM:
    """A discovered finite state machine."""

    id: str
    name: str
    states: List[FSMState] = field(default_factory=list)
    transitions: List[FSMTransition] = field(default_factory=list)
    alphabet: List[str] = field(default_factory=list)
    equivalence_verified: bool = False
    counterexample: Optional[str] = None
    discovered_at: float = field(default_factory=time.time)


@dataclass
class FuzzingTask:
    """A fuzzing/automata learning task."""

    id: str
    target_description: str
    sandbox_type: SandboxEnvironment
    input_space: InputSpace
    status: FuzzingStatus = FuzzingStatus.IDLE
    membership_queries: List[MembershipQuery] = field(default_factory=list)
    fsm_id: Optional[str] = None
    equivalence_test_count: int = 0
    refinement_count: int = 0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    error_message: Optional[str] = None


@dataclass
class SandboxState:
    """State of a sandbox environment."""

    sandbox_id: str
    environment: SandboxEnvironment
    is_active: bool = False
    is_air_gapped: bool = False
    timeout_seconds: int = 300
    created_at: float = field(default_factory=time.time)


@dataclass
class FuzzingState:
    """Redux slice for fuzzing loop state."""

    active_tasks: Dict[str, FuzzingTask] = field(default_factory=dict)
    discovered_fsms: Dict[str, DiscoveredFSM] = field(default_factory=dict)
    active_sandboxes: Dict[str, SandboxState] = field(default_factory=dict)
    membership_query_history: List[MembershipQuery] = field(default_factory=list)
    total_queries: int = 0
    total_refinements: int = 0


class FuzzingActions:
    """Action creators for fuzzing state updates."""

    @staticmethod
    def start_fuzzing_task(task: FuzzingTask) -> dict:
        """Create action to start a fuzzing task."""
        return {
            "type": "fuzzing/start_task",
            "payload": {
                "id": task.id,
                "target_description": task.target_description,
                "sandbox_type": task.sandbox_type.value,
                "input_space": {
                    "input_type": task.input_space.input_type,
                    "lower_bound": task.input_space.lower_bound,
                    "upper_bound": task.input_space.upper_bound,
                    "valid_inputs": task.input_space.valid_inputs,
                },
            },
        }

    @staticmethod
    def update_fuzzing_status(task_id: str, status: FuzzingStatus) -> dict:
        """Create action to update fuzzing status."""
        return {
            "type": "fuzzing/update_status",
            "payload": {
                "task_id": task_id,
                "status": status.value,
            },
        }

    @staticmethod
    def record_membership_query(query: MembershipQuery) -> dict:
        """Create action to record a membership query result."""
        return {
            "type": "fuzzing/record_membership_query",
            "payload": {
                "id": query.id,
                "input_sequence": query.input_sequence,
                "response": query.response.value,
                "new_state_discovered": query.new_state_discovered,
            },
        }

    @staticmethod
    def create_fsm(fsm: DiscoveredFSM) -> dict:
        """Create action to create a discovered FSM."""
        return {
            "type": "fuzzing/create_fsm",
            "payload": {
                "id": fsm.id,
                "name": fsm.name,
                "states": [
                    {
                        "name": s.name,
                        "is_accepting": s.is_accepting,
                        "is_initial": s.is_initial,
                    }
                    for s in fsm.states
                ],
                "transitions": [
                    {
                        "from_state": t.from_state,
                        "to_state": t.to_state,
                        "input_symbol": t.input_symbol,
                    }
                    for t in fsm.transitions
                ],
                "alphabet": fsm.alphabet,
            },
        }

    @staticmethod
    def update_fsm(
        fsm_id: str, states: List[FSMState], transitions: List[FSMTransition]
    ) -> dict:
        """Create action to update a FSM."""
        return {
            "type": "fuzzing/update_fsm",
            "payload": {
                "fsm_id": fsm_id,
                "states": [
                    {
                        "name": s.name,
                        "is_accepting": s.is_accepting,
                        "is_initial": s.is_initial,
                    }
                    for s in states
                ],
                "transitions": [
                    {
                        "from_state": t.from_state,
                        "to_state": t.to_state,
                        "input_symbol": t.input_symbol,
                    }
                    for t in transitions
                ],
            },
        }

    @staticmethod
    def verify_equivalence(
        task_id: str, fsm_id: str, verified: bool, counterexample: Optional[str] = None
    ) -> dict:
        """Create action to record equivalence test result."""
        return {
            "type": "fuzzing/verify_equivalence",
            "payload": {
                "task_id": task_id,
                "fsm_id": fsm_id,
                "verified": verified,
                "counterexample": counterexample,
            },
        }

    @staticmethod
    def refine_fsm(task_id: str, fsm_id: str) -> dict:
        """Create action to refine the FSM with counterexample."""
        return {
            "type": "fuzzing/refine_fsm",
            "payload": {
                "task_id": task_id,
                "fsm_id": fsm_id,
            },
        }

    @staticmethod
    def complete_fuzzing_task(task_id: str) -> dict:
        """Create action to complete a fuzzing task."""
        return {
            "type": "fuzzing/complete_task",
            "payload": {"task_id": task_id},
        }

    @staticmethod
    def fail_fuzzing_task(task_id: str, error: str) -> dict:
        """Create action to mark a fuzzing task as failed."""
        return {
            "type": "fuzzing/fail_task",
            "payload": {
                "task_id": task_id,
                "error": error,
            },
        }

    @staticmethod
    def create_sandbox(sandbox: SandboxState) -> dict:
        """Create action to create a sandbox environment."""
        return {
            "type": "fuzzing/create_sandbox",
            "payload": {
                "sandbox_id": sandbox.sandbox_id,
                "environment": sandbox.environment.value,
                "is_air_gapped": sandbox.is_air_gapped,
                "timeout_seconds": sandbox.timeout_seconds,
            },
        }

    @staticmethod
    def activate_sandbox(sandbox_id: str) -> dict:
        """Create action to activate a sandbox."""
        return {
            "type": "fuzzing/activate_sandbox",
            "payload": {"sandbox_id": sandbox_id},
        }

    @staticmethod
    def deactivate_sandbox(sandbox_id: str) -> dict:
        """Create action to deactivate a sandbox."""
        return {
            "type": "fuzzing/deactivate_sandbox",
            "payload": {"sandbox_id": sandbox_id},
        }


def fuzzing_reducer(state: FuzzingState, action: dict) -> FuzzingState:
    """
    Reducer function for fuzzing state.

    Args:
        state: Current fuzzing state.
        action: Action to apply to the state.

    Returns:
        New fuzzing state.
    """
    action_type = action.get("type")

    if action_type == "fuzzing/start_task":
        payload = action.get("payload", {})
        input_space = InputSpace(
            input_type=payload.get("input_space", {}).get("input_type"),
            lower_bound=payload.get("input_space", {}).get("lower_bound", 0),
            upper_bound=payload.get("input_space", {}).get("upper_bound", 255),
            valid_inputs=payload.get("input_space", {}).get("valid_inputs", []),
        )
        task = FuzzingTask(
            id=payload.get("id"),
            target_description=payload.get("target_description"),
            sandbox_type=SandboxEnvironment(payload.get("sandbox_type")),
            input_space=input_space,
            status=FuzzingStatus.INITIALIZING,
            started_at=time.time(),
        )
        new_active = state.active_tasks.copy()
        new_active[task.id] = task
        return FuzzingState(
            active_tasks=new_active,
            discovered_fsms=state.discovered_fsms,
            active_sandboxes=state.active_sandboxes,
            membership_query_history=state.membership_query_history,
            total_queries=state.total_queries,
            total_refinements=state.total_refinements,
        )

    elif action_type == "fuzzing/update_status":
        payload = action.get("payload", {})
        task_id = payload.get("task_id")
        task = state.active_tasks.get(task_id)
        if task:
            task.status = FuzzingStatus(payload.get("status"))
            new_active = state.active_tasks.copy()
            new_active[task_id] = task
            return FuzzingState(
                active_tasks=new_active,
                discovered_fsms=state.discovered_fsms,
                active_sandboxes=state.active_sandboxes,
                membership_query_history=state.membership_query_history,
                total_queries=state.total_queries,
                total_refinements=state.total_refinements,
            )
        return state

    elif action_type == "fuzzing/record_membership_query":
        payload = action.get("payload", {})
        query = MembershipQuery(
            id=payload.get("id"),
            input_sequence=payload.get("input_sequence", []),
            response=SandboxResponse(payload.get("response", "unknown")),
            new_state_discovered=payload.get("new_state_discovered", False),
        )
        task_id = None
        for tid, t in state.active_tasks.items():
            if (
                t.status == FuzzingStatus.LEARNING
                or t.status == FuzzingStatus.HYPOTHESIZING
            ):
                task_id = tid
                break
        if task_id:
            task = state.active_tasks[task_id]
            task.membership_queries.append(query)
            new_active = state.active_tasks.copy()
            new_active[task_id] = task
        else:
            new_active = state.active_tasks
        new_history = (state.membership_query_history + [query])[-1000:]
        return FuzzingState(
            active_tasks=new_active,
            discovered_fsms=state.discovered_fsms,
            active_sandboxes=state.active_sandboxes,
            membership_query_history=new_history,
            total_queries=state.total_queries + 1,
            total_refinements=state.total_refinements,
        )

    elif action_type == "fuzzing/create_fsm":
        payload = action.get("payload", {})
        states = [FSMState(**s) for s in payload.get("states", [])]
        transitions = [FSMTransition(**t) for t in payload.get("transitions", [])]
        fsm = DiscoveredFSM(
            id=payload.get("id"),
            name=payload.get("name"),
            states=states,
            transitions=transitions,
            alphabet=payload.get("alphabet", []),
        )
        new_fsms = state.discovered_fsms.copy()
        new_fsms[fsm.id] = fsm
        return FuzzingState(
            active_tasks=state.active_tasks,
            discovered_fsms=new_fsms,
            active_sandboxes=state.active_sandboxes,
            membership_query_history=state.membership_query_history,
            total_queries=state.total_queries,
            total_refinements=state.total_refinements,
        )

    elif action_type == "fuzzing/update_fsm":
        payload = action.get("payload", {})
        fsm_id = payload.get("fsm_id")
        fsm = state.discovered_fsms.get(fsm_id)
        if fsm:
            fsm.states = [FSMState(**s) for s in payload.get("states", [])]
            fsm.transitions = [
                FSMTransition(**t) for t in payload.get("transitions", [])
            ]
            new_fsms = state.discovered_fsms.copy()
            new_fsms[fsm_id] = fsm
            return FuzzingState(
                active_tasks=state.active_tasks,
                discovered_fsms=new_fsms,
                active_sandboxes=state.active_sandboxes,
                membership_query_history=state.membership_query_history,
                total_queries=state.total_queries,
                total_refinements=state.total_refinements,
            )
        return state

    elif action_type == "fuzzing/verify_equivalence":
        payload = action.get("payload", {})
        task_id = payload.get("task_id")
        fsm_id = payload.get("fsm_id")
        task = state.active_tasks.get(task_id)
        if task:
            task.equivalence_test_count += 1
            new_active = state.active_tasks.copy()
            new_active[task_id] = task
        else:
            new_active = state.active_tasks
        fsm = state.discovered_fsms.get(fsm_id)
        if fsm:
            fsm.equivalence_verified = payload.get("verified", False)
            fsm.counterexample = payload.get("counterexample")
            new_fsms = state.discovered_fsms.copy()
            new_fsms[fsm_id] = fsm
        else:
            new_fsms = state.discovered_fsms
        return FuzzingState(
            active_tasks=new_active,
            discovered_fsms=new_fsms,
            active_sandboxes=state.active_sandboxes,
            membership_query_history=state.membership_query_history,
            total_queries=state.total_queries,
            total_refinements=state.total_refinements,
        )

    elif action_type == "fuzzing/refine_fsm":
        payload = action.get("payload", {})
        task_id = payload.get("task_id")
        task = state.active_tasks.get(task_id)
        if task:
            task.refinement_count += 1
            task.status = FuzzingStatus.REFINING
            new_active = state.active_tasks.copy()
            new_active[task_id] = task
        else:
            new_active = state.active_tasks
        return FuzzingState(
            active_tasks=new_active,
            discovered_fsms=state.discovered_fsms,
            active_sandboxes=state.active_sandboxes,
            membership_query_history=state.membership_query_history,
            total_queries=state.total_queries,
            total_refinements=state.total_refinements + 1,
        )

    elif action_type == "fuzzing/complete_task":
        payload = action.get("payload", {})
        task_id = payload.get("task_id")
        task = state.active_tasks.get(task_id)
        if task:
            task.status = FuzzingStatus.COMPLETED
            task.completed_at = time.time()
            new_active = state.active_tasks.copy()
            new_active[task_id] = task
            return FuzzingState(
                active_tasks=new_active,
                discovered_fsms=state.discovered_fsms,
                active_sandboxes=state.active_sandboxes,
                membership_query_history=state.membership_query_history,
                total_queries=state.total_queries,
                total_refinements=state.total_refinements,
            )
        return state

    elif action_type == "fuzzing/fail_task":
        payload = action.get("payload", {})
        task_id = payload.get("task_id")
        task = state.active_tasks.get(task_id)
        if task:
            task.status = FuzzingStatus.ERROR
            task.error_message = payload.get("error")
            task.completed_at = time.time()
            new_active = state.active_tasks.copy()
            new_active[task_id] = task
            return FuzzingState(
                active_tasks=new_active,
                discovered_fsms=state.discovered_fsms,
                active_sandboxes=state.active_sandboxes,
                membership_query_history=state.membership_query_history,
                total_queries=state.total_queries,
                total_refinements=state.total_refinements,
            )
        return state

    elif action_type == "fuzzing/create_sandbox":
        payload = action.get("payload", {})
        sandbox = SandboxState(
            sandbox_id=payload.get("sandbox_id"),
            environment=SandboxEnvironment(payload.get("environment")),
            is_air_gapped=payload.get("is_air_gapped", False),
            timeout_seconds=payload.get("timeout_seconds", 300),
        )
        new_sandboxes = state.active_sandboxes.copy()
        new_sandboxes[sandbox.sandbox_id] = sandbox
        return FuzzingState(
            active_tasks=state.active_tasks,
            discovered_fsms=state.discovered_fsms,
            active_sandboxes=new_sandboxes,
            membership_query_history=state.membership_query_history,
            total_queries=state.total_queries,
            total_refinements=state.total_refinements,
        )

    elif action_type == "fuzzing/activate_sandbox":
        payload = action.get("payload", {})
        sandbox_id = payload.get("sandbox_id")
        sandbox = state.active_sandboxes.get(sandbox_id)
        if sandbox:
            sandbox.is_active = True
            new_sandboxes = state.active_sandboxes.copy()
            new_sandboxes[sandbox_id] = sandbox
            return FuzzingState(
                active_tasks=state.active_tasks,
                discovered_fsms=state.discovered_fsms,
                active_sandboxes=new_sandboxes,
                membership_query_history=state.membership_query_history,
                total_queries=state.total_queries,
                total_refinements=state.total_refinements,
            )
        return state

    elif action_type == "fuzzing/deactivate_sandbox":
        payload = action.get("payload", {})
        sandbox_id = payload.get("sandbox_id")
        sandbox = state.active_sandboxes.get(sandbox_id)
        if sandbox:
            sandbox.is_active = False
            new_sandboxes = state.active_sandboxes.copy()
            new_sandboxes[sandbox_id] = sandbox
            return FuzzingState(
                active_tasks=state.active_tasks,
                discovered_fsms=state.discovered_fsms,
                active_sandboxes=new_sandboxes,
                membership_query_history=state.membership_query_history,
                total_queries=state.total_queries,
                total_refinements=state.total_refinements,
            )
        return state

    return state
