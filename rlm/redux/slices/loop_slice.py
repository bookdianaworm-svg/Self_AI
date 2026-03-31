"""
Redux slice for dual-loop (Fast/Slow) state management.

This module provides state management for the Universal Dual-Loop Architecture,
decoupling creative discovery (Fast Loop/Skunkworks) from formal verification
(Slow Loop/The Crucible).
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum
import time


class LoopStatus(Enum):
    """Status of a loop."""

    INACTIVE = "inactive"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPING = "stopping"
    ERROR = "error"


class CandidateStatus(Enum):
    """Status of a release candidate."""

    PENDING = "pending"
    IN_REVIEW = "in_review"
    CERTIFIED = "certified"
    REJECTED = "rejected"
    INTEGRATED = "integrated"


class InterruptPriority(Enum):
    """Priority of an interrupt."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class LoopMetrics:
    """Metrics for loop performance."""

    iterations: int = 0
    candidates_submitted: int = 0
    candidates_certified: int = 0
    candidates_rejected: int = 0
    interrupts_sent: int = 0
    interrupts_received: int = 0
    avg_iteration_time_ms: float = 0.0
    total_processing_time_ms: float = 0.0


@dataclass
class ReleaseCandidate:
    """A release candidate from the Fast Loop for Slow Loop verification."""

    id: str
    task_id: str
    description: str
    formal_structure: str
    code: str
    domain: str
    status: CandidateStatus = CandidateStatus.PENDING
    submitted_at: float = field(default_factory=time.time)
    certified_at: Optional[float] = None
    rejected_at: Optional[float] = None
    rejection_reason: Optional[str] = None
    proof: Optional[str] = None
    error_trace: Optional[str] = None


@dataclass
class CertifiedCandidate:
    """A release candidate that has passed Slow Loop verification."""

    id: str
    task_id: str
    domain: str
    formal_structure: str
    proof: str
    certified_at: float
    invariants: List[str] = field(default_factory=list)


@dataclass
class Interrupt:
    """An interrupt from Slow Loop to Fast Loop."""

    id: str
    candidate_id: str
    priority: InterruptPriority
    message: str
    error_type: str
    mathematical_constraint: str
    created_at: float = field(default_factory=time.time)
    acknowledged: bool = False
    acknowledged_at: Optional[float] = None


@dataclass
class LoopState:
    """Redux slice for dual-loop state."""

    fast_loop_status: LoopStatus = LoopStatus.INACTIVE
    slow_loop_status: LoopStatus = LoopStatus.INACTIVE
    fast_loop_active: bool = False
    slow_loop_active: bool = False
    active_candidates: Dict[str, ReleaseCandidate] = field(default_factory=dict)
    certified_candidates: Dict[str, CertifiedCandidate] = field(default_factory=dict)
    pending_interrupts: List[Interrupt] = field(default_factory=list)
    acknowledged_interrupts: List[Interrupt] = field(default_factory=list)
    loop_metrics: LoopMetrics = field(default_factory=LoopMetrics)
    last_fast_loop_iteration: Optional[float] = None
    last_slow_loop_iteration: Optional[float] = None


class LoopActions:
    """Action creators for loop state updates."""

    @staticmethod
    def start_fast_loop() -> dict:
        """Create action to start the Fast Loop."""
        return {"type": "loop/start_fast_loop"}

    @staticmethod
    def stop_fast_loop() -> dict:
        """Create action to stop the Fast Loop."""
        return {"type": "loop/stop_fast_loop"}

    @staticmethod
    def start_slow_loop() -> dict:
        """Create action to start the Slow Loop."""
        return {"type": "loop/start_slow_loop"}

    @staticmethod
    def stop_slow_loop() -> dict:
        """Create action to stop the Slow Loop."""
        return {"type": "loop/stop_slow_loop"}

    @staticmethod
    def pause_fast_loop() -> dict:
        """Create action to pause the Fast Loop."""
        return {"type": "loop/pause_fast_loop"}

    @staticmethod
    def resume_fast_loop() -> dict:
        """Create action to resume the Fast Loop."""
        return {"type": "loop/resume_fast_loop"}

    @staticmethod
    def submit_candidate(candidate: ReleaseCandidate) -> dict:
        """Create action to submit a release candidate for verification."""
        return {
            "type": "loop/submit_candidate",
            "payload": {
                "id": candidate.id,
                "task_id": candidate.task_id,
                "description": candidate.description,
                "formal_structure": candidate.formal_structure,
                "code": candidate.code,
                "domain": candidate.domain,
            },
        }

    @staticmethod
    def certify_candidate(candidate_id: str, proof: str, invariants: List[str]) -> dict:
        """Create action to certify a release candidate."""
        return {
            "type": "loop/certify_candidate",
            "payload": {
                "candidate_id": candidate_id,
                "proof": proof,
                "invariants": invariants,
            },
        }

    @staticmethod
    def reject_candidate(candidate_id: str, reason: str, error_trace: str) -> dict:
        """Create action to reject a release candidate."""
        return {
            "type": "loop/reject_candidate",
            "payload": {
                "candidate_id": candidate_id,
                "reason": reason,
                "error_trace": error_trace,
            },
        }

    @staticmethod
    def send_interrupt(interrupt: Interrupt) -> dict:
        """Create action to send an interrupt to the Fast Loop."""
        return {
            "type": "loop/send_interrupt",
            "payload": {
                "id": interrupt.id,
                "candidate_id": interrupt.candidate_id,
                "priority": interrupt.priority.value,
                "message": interrupt.message,
                "error_type": interrupt.error_type,
                "mathematical_constraint": interrupt.mathematical_constraint,
            },
        }

    @staticmethod
    def acknowledge_interrupt(interrupt_id: str) -> dict:
        """Create action to acknowledge an interrupt."""
        return {
            "type": "loop/acknowledge_interrupt",
            "payload": {"interrupt_id": interrupt_id},
        }

    @staticmethod
    def record_fast_loop_iteration(processing_time_ms: float) -> dict:
        """Create action to record a Fast Loop iteration."""
        return {
            "type": "loop/record_fast_loop_iteration",
            "payload": {"processing_time_ms": processing_time_ms},
        }

    @staticmethod
    def record_slow_loop_iteration(processing_time_ms: float) -> dict:
        """Create action to record a Slow Loop iteration."""
        return {
            "type": "loop/record_slow_loop_iteration",
            "payload": {"processing_time_ms": processing_time_ms},
        }


def loop_reducer(state: LoopState, action: dict) -> LoopState:
    """
    Reducer function for loop state.

    Args:
        state: Current loop state.
        action: Action to apply to the state.

    Returns:
        New loop state.
    """
    action_type = action.get("type")

    if action_type == "loop/start_fast_loop":
        return LoopState(
            fast_loop_status=LoopStatus.ACTIVE,
            slow_loop_status=state.slow_loop_status,
            fast_loop_active=True,
            slow_loop_active=state.slow_loop_active,
            active_candidates=state.active_candidates,
            certified_candidates=state.certified_candidates,
            pending_interrupts=state.pending_interrupts,
            acknowledged_interrupts=state.acknowledged_interrupts,
            loop_metrics=state.loop_metrics,
        )

    elif action_type == "loop/stop_fast_loop":
        return LoopState(
            fast_loop_status=LoopStatus.INACTIVE,
            slow_loop_status=state.slow_loop_status,
            fast_loop_active=False,
            slow_loop_active=state.slow_loop_active,
            active_candidates=state.active_candidates,
            certified_candidates=state.certified_candidates,
            pending_interrupts=state.pending_interrupts,
            acknowledged_interrupts=state.acknowledged_interrupts,
            loop_metrics=state.loop_metrics,
        )

    elif action_type == "loop/pause_fast_loop":
        return LoopState(
            fast_loop_status=LoopStatus.PAUSED,
            slow_loop_status=state.slow_loop_status,
            fast_loop_active=False,
            slow_loop_active=state.slow_loop_active,
            active_candidates=state.active_candidates,
            certified_candidates=state.certified_candidates,
            pending_interrupts=state.pending_interrupts,
            acknowledged_interrupts=state.acknowledged_interrupts,
            loop_metrics=state.loop_metrics,
        )

    elif action_type == "loop/resume_fast_loop":
        return LoopState(
            fast_loop_status=LoopStatus.ACTIVE,
            slow_loop_status=state.slow_loop_status,
            fast_loop_active=True,
            slow_loop_active=state.slow_loop_active,
            active_candidates=state.active_candidates,
            certified_candidates=state.certified_candidates,
            pending_interrupts=state.pending_interrupts,
            acknowledged_interrupts=state.acknowledged_interrupts,
            loop_metrics=state.loop_metrics,
        )

    elif action_type == "loop/start_slow_loop":
        return LoopState(
            fast_loop_status=state.fast_loop_status,
            slow_loop_status=LoopStatus.ACTIVE,
            fast_loop_active=state.fast_loop_active,
            slow_loop_active=True,
            active_candidates=state.active_candidates,
            certified_candidates=state.certified_candidates,
            pending_interrupts=state.pending_interrupts,
            acknowledged_interrupts=state.acknowledged_interrupts,
            loop_metrics=state.loop_metrics,
        )

    elif action_type == "loop/stop_slow_loop":
        return LoopState(
            fast_loop_status=state.fast_loop_status,
            slow_loop_status=LoopStatus.INACTIVE,
            fast_loop_active=state.fast_loop_active,
            slow_loop_active=False,
            active_candidates=state.active_candidates,
            certified_candidates=state.certified_candidates,
            pending_interrupts=state.pending_interrupts,
            acknowledged_interrupts=state.acknowledged_interrupts,
            loop_metrics=state.loop_metrics,
        )

    elif action_type == "loop/submit_candidate":
        payload = action.get("payload", {})
        candidate_id = payload.get("id")
        new_candidates = state.active_candidates.copy()
        new_candidates[candidate_id] = ReleaseCandidate(
            id=candidate_id,
            task_id=payload.get("task_id"),
            description=payload.get("description"),
            formal_structure=payload.get("formal_structure"),
            code=payload.get("code"),
            domain=payload.get("domain"),
            status=CandidateStatus.PENDING,
        )
        new_metrics = LoopMetrics(
            iterations=state.loop_metrics.iterations,
            candidates_submitted=state.loop_metrics.candidates_submitted + 1,
            candidates_certified=state.loop_metrics.candidates_certified,
            candidates_rejected=state.loop_metrics.candidates_rejected,
            interrupts_sent=state.loop_metrics.interrupts_sent,
            interrupts_received=state.loop_metrics.interrupts_received,
            avg_iteration_time_ms=state.loop_metrics.avg_iteration_time_ms,
            total_processing_time_ms=state.loop_metrics.total_processing_time_ms,
        )
        return LoopState(
            fast_loop_status=state.fast_loop_status,
            slow_loop_status=state.slow_loop_status,
            fast_loop_active=state.fast_loop_active,
            slow_loop_active=state.slow_loop_active,
            active_candidates=new_candidates,
            certified_candidates=state.certified_candidates,
            pending_interrupts=state.pending_interrupts,
            acknowledged_interrupts=state.acknowledged_interrupts,
            loop_metrics=new_metrics,
            last_fast_loop_iteration=time.time(),
        )

    elif action_type == "loop/certify_candidate":
        payload = action.get("payload", {})
        candidate_id = payload.get("candidate_id")
        candidate = state.active_candidates.get(candidate_id)
        if candidate:
            certified = CertifiedCandidate(
                id=candidate.id,
                task_id=candidate.task_id,
                domain=candidate.domain,
                formal_structure=candidate.formal_structure,
                proof=payload.get("proof"),
                certified_at=time.time(),
                invariants=payload.get("invariants", []),
            )
            new_certified = state.certified_candidates.copy()
            new_certified[candidate_id] = certified
            new_active = state.active_candidates.copy()
            del new_active[candidate_id]
            new_metrics = LoopMetrics(
                iterations=state.loop_metrics.iterations,
                candidates_submitted=state.loop_metrics.candidates_submitted,
                candidates_certified=state.loop_metrics.candidates_certified + 1,
                candidates_rejected=state.loop_metrics.candidates_rejected,
                interrupts_sent=state.loop_metrics.interrupts_sent,
                interrupts_received=state.loop_metrics.interrupts_received,
                avg_iteration_time_ms=state.loop_metrics.avg_iteration_time_ms,
                total_processing_time_ms=state.loop_metrics.total_processing_time_ms,
            )
            return LoopState(
                fast_loop_status=state.fast_loop_status,
                slow_loop_status=state.slow_loop_status,
                fast_loop_active=state.fast_loop_active,
                slow_loop_active=state.slow_loop_active,
                active_candidates=new_active,
                certified_candidates=new_certified,
                pending_interrupts=state.pending_interrupts,
                acknowledged_interrupts=state.acknowledged_interrupts,
                loop_metrics=new_metrics,
                last_slow_loop_iteration=time.time(),
            )
        return state

    elif action_type == "loop/reject_candidate":
        payload = action.get("payload", {})
        candidate_id = payload.get("candidate_id")
        candidate = state.active_candidates.get(candidate_id)
        if candidate:
            candidate.status = CandidateStatus.REJECTED
            candidate.rejected_at = time.time()
            candidate.rejection_reason = payload.get("reason")
            candidate.error_trace = payload.get("error_trace")
            new_active = state.active_candidates.copy()
            new_active[candidate_id] = candidate
            new_metrics = LoopMetrics(
                iterations=state.loop_metrics.iterations,
                candidates_submitted=state.loop_metrics.candidates_submitted,
                candidates_certified=state.loop_metrics.candidates_certified,
                candidates_rejected=state.loop_metrics.candidates_rejected + 1,
                interrupts_sent=state.loop_metrics.interrupts_sent,
                interrupts_received=state.loop_metrics.interrupts_received,
                avg_iteration_time_ms=state.loop_metrics.avg_iteration_time_ms,
                total_processing_time_ms=state.loop_metrics.total_processing_time_ms,
            )
            return LoopState(
                fast_loop_status=state.fast_loop_status,
                slow_loop_status=state.slow_loop_status,
                fast_loop_active=state.fast_loop_active,
                slow_loop_active=state.slow_loop_active,
                active_candidates=new_active,
                certified_candidates=state.certified_candidates,
                pending_interrupts=state.pending_interrupts,
                acknowledged_interrupts=state.acknowledged_interrupts,
                loop_metrics=new_metrics,
                last_slow_loop_iteration=time.time(),
            )
        return state

    elif action_type == "loop/send_interrupt":
        payload = action.get("payload", {})
        interrupt = Interrupt(
            id=payload.get("id"),
            candidate_id=payload.get("candidate_id"),
            priority=InterruptPriority(payload.get("priority", "normal")),
            message=payload.get("message"),
            error_type=payload.get("error_type"),
            mathematical_constraint=payload.get("mathematical_constraint"),
        )
        new_pending = state.pending_interrupts + [interrupt]
        new_metrics = LoopMetrics(
            iterations=state.loop_metrics.iterations,
            candidates_submitted=state.loop_metrics.candidates_submitted,
            candidates_certified=state.loop_metrics.candidates_certified,
            candidates_rejected=state.loop_metrics.candidates_rejected,
            interrupts_sent=state.loop_metrics.interrupts_sent + 1,
            interrupts_received=state.loop_metrics.interrupts_received,
            avg_iteration_time_ms=state.loop_metrics.avg_iteration_time_ms,
            total_processing_time_ms=state.loop_metrics.total_processing_time_ms,
        )
        return LoopState(
            fast_loop_status=state.fast_loop_status,
            slow_loop_status=state.slow_loop_status,
            fast_loop_active=state.fast_loop_active,
            slow_loop_active=state.slow_loop_active,
            active_candidates=state.active_candidates,
            certified_candidates=state.certified_candidates,
            pending_interrupts=new_pending,
            acknowledged_interrupts=state.acknowledged_interrupts,
            loop_metrics=new_metrics,
            last_slow_loop_iteration=time.time(),
        )

    elif action_type == "loop/acknowledge_interrupt":
        payload = action.get("payload", {})
        interrupt_id = payload.get("interrupt_id")
        new_pending = []
        acknowledged = None
        for interrupt in state.pending_interrupts:
            if interrupt.id == interrupt_id:
                interrupt.acknowledged = True
                interrupt.acknowledged_at = time.time()
                acknowledged = interrupt
            else:
                new_pending.append(interrupt)
        if acknowledged:
            new_acknowledged = state.acknowledged_interrupts + [acknowledged]
            new_metrics = LoopMetrics(
                iterations=state.loop_metrics.iterations,
                candidates_submitted=state.loop_metrics.candidates_submitted,
                candidates_certified=state.loop_metrics.candidates_certified,
                candidates_rejected=state.loop_metrics.candidates_rejected,
                interrupts_sent=state.loop_metrics.interrupts_sent,
                interrupts_received=state.loop_metrics.interrupts_received + 1,
                avg_iteration_time_ms=state.loop_metrics.avg_iteration_time_ms,
                total_processing_time_ms=state.loop_metrics.total_processing_time_ms,
            )
            return LoopState(
                fast_loop_status=state.fast_loop_status,
                slow_loop_status=state.slow_loop_status,
                fast_loop_active=state.fast_loop_active,
                slow_loop_active=state.slow_loop_active,
                active_candidates=state.active_candidates,
                certified_candidates=state.certified_candidates,
                pending_interrupts=new_pending,
                acknowledged_interrupts=new_acknowledged,
                loop_metrics=new_metrics,
            )
        return state

    elif action_type == "loop/record_fast_loop_iteration":
        payload = action.get("payload", {})
        processing_time = payload.get("processing_time_ms", 0.0)
        total_time = state.loop_metrics.total_processing_time_ms + processing_time
        iterations = state.loop_metrics.iterations + 1
        avg_time = total_time / iterations if iterations > 0 else 0.0
        new_metrics = LoopMetrics(
            iterations=iterations,
            candidates_submitted=state.loop_metrics.candidates_submitted,
            candidates_certified=state.loop_metrics.candidates_certified,
            candidates_rejected=state.loop_metrics.candidates_rejected,
            interrupts_sent=state.loop_metrics.interrupts_sent,
            interrupts_received=state.loop_metrics.interrupts_received,
            avg_iteration_time_ms=avg_time,
            total_processing_time_ms=total_time,
        )
        return LoopState(
            fast_loop_status=state.fast_loop_status,
            slow_loop_status=state.slow_loop_status,
            fast_loop_active=state.fast_loop_active,
            slow_loop_active=state.slow_loop_active,
            active_candidates=state.active_candidates,
            certified_candidates=state.certified_candidates,
            pending_interrupts=state.pending_interrupts,
            acknowledged_interrupts=state.acknowledged_interrupts,
            loop_metrics=new_metrics,
            last_fast_loop_iteration=time.time(),
            last_slow_loop_iteration=state.last_slow_loop_iteration,
        )

    elif action_type == "loop/record_slow_loop_iteration":
        payload = action.get("payload", {})
        processing_time = payload.get("processing_time_ms", 0.0)
        total_time = state.loop_metrics.total_processing_time_ms + processing_time
        iterations = state.loop_metrics.iterations + 1
        avg_time = total_time / iterations if iterations > 0 else 0.0
        new_metrics = LoopMetrics(
            iterations=iterations,
            candidates_submitted=state.loop_metrics.candidates_submitted,
            candidates_certified=state.loop_metrics.candidates_certified,
            candidates_rejected=state.loop_metrics.candidates_rejected,
            interrupts_sent=state.loop_metrics.interrupts_sent,
            interrupts_received=state.loop_metrics.interrupts_received,
            avg_iteration_time_ms=avg_time,
            total_processing_time_ms=total_time,
        )
        return LoopState(
            fast_loop_status=state.fast_loop_status,
            slow_loop_status=state.slow_loop_status,
            fast_loop_active=state.fast_loop_active,
            slow_loop_active=state.slow_loop_active,
            active_candidates=state.active_candidates,
            certified_candidates=state.certified_candidates,
            pending_interrupts=state.pending_interrupts,
            acknowledged_interrupts=state.acknowledged_interrupts,
            loop_metrics=new_metrics,
            last_fast_loop_iteration=state.last_fast_loop_iteration,
            last_slow_loop_iteration=time.time(),
        )

    return state
