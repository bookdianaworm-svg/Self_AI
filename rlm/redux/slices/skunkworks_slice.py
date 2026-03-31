"""
Redux slice for skunkworks state management.

This module provides state management for the Skunkworks Protocol,
decoupling creative discovery (Fast Loop) from formal verification (Slow Loop).
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum
import time


class SkunkworksStatus(Enum):
    """Status of a skunkworks session."""

    IDLE = "idle"
    EXPLORING = "exploring"
    HYPOTHESIZING = "hypothesizing"
    ITERATING = "iterating"
    USER_COLLABORATION = "user_collaboration"
    COMPLETED = "completed"
    TRANSITIONING_TO_CRITICAL = "transitioning_to_crucible"


class HypothesisConfidence(Enum):
    """Confidence level of a hypothesis."""

    SPECULATIVE = "speculative"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class HypothesisStatus(Enum):
    """Status of a hypothesis."""

    GENERATED = "generated"
    TESTING = "testing"
    REFINED = "refined"
    CERTIFIED = "certified"
    REJECTED = "rejected"


@dataclass
class Hypothesis:
    """A high-confidence hypothesis from skunkworks exploration."""

    id: str
    description: str
    confidence: HypothesisConfidence
    evidence: List[str] = field(default_factory=list)
    supporting_queries: List[str] = field(default_factory=list)
    status: HypothesisStatus = HypothesisStatus.GENERATED
    refinement_count: int = 0
    generated_at: float = field(default_factory=time.time)
    certified_at: Optional[float] = None


@dataclass
class ExplorationLog:
    """Log entry for skunkworks exploration."""

    id: str
    iteration: int
    action_type: str
    description: str
    result: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class UserCollaborationRequest:
    """Request for user collaboration during skunkworks."""

    id: str
    question: str
    context: str
    asked_at: float = field(default_factory=time.time)
    responded: bool = False
    response: Optional[str] = None
    responded_at: Optional[float] = None


@dataclass
class SkunkworksSession:
    """A skunkworks exploration session."""

    id: str
    task_description: str
    status: SkunkworksStatus = SkunkworksStatus.IDLE
    active_hypothesis_id: Optional[str] = None
    exploration_logs: List[ExplorationLog] = field(default_factory=list)
    collaboration_requests: List[UserCollaborationRequest] = field(default_factory=list)
    iteration_count: int = 0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None


@dataclass
class SkunkworksState:
    """Redux slice for skunkworks state."""

    active_session: Optional[SkunkworksSession] = None
    hypotheses: Dict[str, Hypothesis] = field(default_factory=dict)
    exploration_history: List[ExplorationLog] = field(default_factory=list)
    certified_hypotheses: List[str] = field(default_factory=list)
    rejected_hypotheses: List[str] = field(default_factory=list)
    pending_collaboration: List[UserCollaborationRequest] = field(default_factory=list)


class SkunkworksActions:
    """Action creators for skunkworks state updates."""

    @staticmethod
    def start_session(session: SkunkworksSession) -> dict:
        """Create action to start a skunkworks session."""
        return {
            "type": "skunkworks/start_session",
            "payload": {
                "id": session.id,
                "task_description": session.task_description,
            },
        }

    @staticmethod
    def update_session_status(status: SkunkworksStatus) -> dict:
        """Create action to update session status."""
        return {
            "type": "skunkworks/update_status",
            "payload": {"status": status.value},
        }

    @staticmethod
    def generate_hypothesis(hypothesis: Hypothesis) -> dict:
        """Create action to generate a new hypothesis."""
        return {
            "type": "skunkworks/generate_hypothesis",
            "payload": {
                "id": hypothesis.id,
                "description": hypothesis.description,
                "confidence": hypothesis.confidence.value,
                "evidence": hypothesis.evidence,
                "supporting_queries": hypothesis.supporting_queries,
            },
        }

    @staticmethod
    def set_active_hypothesis(hypothesis_id: str) -> dict:
        """Create action to set the active hypothesis."""
        return {
            "type": "skunkworks/set_active_hypothesis",
            "payload": {"hypothesis_id": hypothesis_id},
        }

    @staticmethod
    def refine_hypothesis(hypothesis_id: str, new_evidence: List[str]) -> dict:
        """Create action to refine a hypothesis."""
        return {
            "type": "skunkworks/refine_hypothesis",
            "payload": {
                "hypothesis_id": hypothesis_id,
                "new_evidence": new_evidence,
            },
        }

    @staticmethod
    def certify_hypothesis(hypothesis_id: str) -> dict:
        """Create action to certify a hypothesis as high-confidence."""
        return {
            "type": "skunkworks/certify_hypothesis",
            "payload": {"hypothesis_id": hypothesis_id},
        }

    @staticmethod
    def reject_hypothesis(hypothesis_id: str, reason: str) -> dict:
        """Create action to reject a hypothesis."""
        return {
            "type": "skunkworks/reject_hypothesis",
            "payload": {
                "hypothesis_id": hypothesis_id,
                "reason": reason,
            },
        }

    @staticmethod
    def log_exploration(log: ExplorationLog) -> dict:
        """Create action to log an exploration action."""
        return {
            "type": "skunkworks/log_exploration",
            "payload": {
                "id": log.id,
                "iteration": log.iteration,
                "action_type": log.action_type,
                "description": log.description,
                "result": log.result,
            },
        }

    @staticmethod
    def request_user_collaboration(request: UserCollaborationRequest) -> dict:
        """Create action to request user collaboration."""
        return {
            "type": "skunkworks/request_collaboration",
            "payload": {
                "id": request.id,
                "question": request.question,
                "context": request.context,
            },
        }

    @staticmethod
    def respond_to_collaboration(request_id: str, response: str) -> dict:
        """Create action to respond to a collaboration request."""
        return {
            "type": "skunkworks/respond_to_collaboration",
            "payload": {
                "request_id": request_id,
                "response": response,
            },
        }

    @staticmethod
    def complete_session() -> dict:
        """Create action to complete the skunkworks session."""
        return {"type": "skunkworks/complete_session"}

    @staticmethod
    def transition_to_crucible(hypothesis_id: str) -> dict:
        """Create action to transition to formal verification."""
        return {
            "type": "skunkworks/transition_to_crucible",
            "payload": {"hypothesis_id": hypothesis_id},
        }


def skunkworks_reducer(state: SkunkworksState, action: dict) -> SkunkworksState:
    """
    Reducer function for skunkworks state.

    Args:
        state: Current skunkworks state.
        action: Action to apply to the state.

    Returns:
        New skunkworks state.
    """
    action_type = action.get("type")

    if action_type == "skunkworks/start_session":
        payload = action.get("payload", {})
        session = SkunkworksSession(
            id=payload.get("id"),
            task_description=payload.get("task_description"),
            status=SkunkworksStatus.EXPLORING,
            started_at=time.time(),
        )
        return SkunkworksState(
            active_session=session,
            hypotheses=state.hypotheses,
            exploration_history=state.exploration_history,
            certified_hypotheses=state.certified_hypotheses,
            rejected_hypotheses=state.rejected_hypotheses,
            pending_collaboration=state.pending_collaboration,
        )

    elif action_type == "skunkworks/update_status":
        payload = action.get("payload", {})
        if state.active_session:
            state.active_session.status = SkunkworksStatus(payload.get("status"))
        return SkunkworksState(
            active_session=state.active_session,
            hypotheses=state.hypotheses,
            exploration_history=state.exploration_history,
            certified_hypotheses=state.certified_hypotheses,
            rejected_hypotheses=state.rejected_hypotheses,
            pending_collaboration=state.pending_collaboration,
        )

    elif action_type == "skunkworks/generate_hypothesis":
        payload = action.get("payload", {})
        hypothesis = Hypothesis(
            id=payload.get("id"),
            description=payload.get("description"),
            confidence=HypothesisConfidence(payload.get("confidence")),
            evidence=payload.get("evidence", []),
            supporting_queries=payload.get("supporting_queries", []),
        )
        new_hypotheses = state.hypotheses.copy()
        new_hypotheses[hypothesis.id] = hypothesis
        if state.active_session:
            state.active_session.active_hypothesis_id = hypothesis.id
            state.active_session.status = SkunkworksStatus.HYPOTHESIZING
        return SkunkworksState(
            active_session=state.active_session,
            hypotheses=new_hypotheses,
            exploration_history=state.exploration_history,
            certified_hypotheses=state.certified_hypotheses,
            rejected_hypotheses=state.rejected_hypotheses,
            pending_collaboration=state.pending_collaboration,
        )

    elif action_type == "skunkworks/set_active_hypothesis":
        payload = action.get("payload", {})
        if state.active_session:
            state.active_session.active_hypothesis_id = payload.get("hypothesis_id")
        return SkunkworksState(
            active_session=state.active_session,
            hypotheses=state.hypotheses,
            exploration_history=state.exploration_history,
            certified_hypotheses=state.certified_hypotheses,
            rejected_hypotheses=state.rejected_hypotheses,
            pending_collaboration=state.pending_collaboration,
        )

    elif action_type == "skunkworks/refine_hypothesis":
        payload = action.get("payload", {})
        hypothesis_id = payload.get("hypothesis_id")
        hypothesis = state.hypotheses.get(hypothesis_id)
        if hypothesis:
            hypothesis.evidence.extend(payload.get("new_evidence", []))
            hypothesis.refinement_count += 1
            hypothesis.status = HypothesisStatus.REFINED
            new_hypotheses = state.hypotheses.copy()
            new_hypotheses[hypothesis_id] = hypothesis
            return SkunkworksState(
                active_session=state.active_session,
                hypotheses=new_hypotheses,
                exploration_history=state.exploration_history,
                certified_hypotheses=state.certified_hypotheses,
                rejected_hypotheses=state.rejected_hypotheses,
                pending_collaboration=state.pending_collaboration,
            )
        return state

    elif action_type == "skunkworks/certify_hypothesis":
        payload = action.get("payload", {})
        hypothesis_id = payload.get("hypothesis_id")
        hypothesis = state.hypotheses.get(hypothesis_id)
        if hypothesis:
            hypothesis.status = HypothesisStatus.CERTIFIED
            hypothesis.certified_at = time.time()
            new_hypotheses = state.hypotheses.copy()
            new_hypotheses[hypothesis_id] = hypothesis
            new_certified = state.certified_hypotheses + [hypothesis_id]
            return SkunkworksState(
                active_session=state.active_session,
                hypotheses=new_hypotheses,
                exploration_history=state.exploration_history,
                certified_hypotheses=new_certified,
                rejected_hypotheses=state.rejected_hypotheses,
                pending_collaboration=state.pending_collaboration,
            )
        return state

    elif action_type == "skunkworks/reject_hypothesis":
        payload = action.get("payload", {})
        hypothesis_id = payload.get("hypothesis_id")
        hypothesis = state.hypotheses.get(hypothesis_id)
        if hypothesis:
            hypothesis.status = HypothesisStatus.REJECTED
            new_hypotheses = state.hypotheses.copy()
            new_hypotheses[hypothesis_id] = hypothesis
            new_rejected = state.rejected_hypotheses + [hypothesis_id]
            return SkunkworksState(
                active_session=state.active_session,
                hypotheses=new_hypotheses,
                exploration_history=state.exploration_history,
                certified_hypotheses=state.certified_hypotheses,
                rejected_hypotheses=new_rejected,
                pending_collaboration=state.pending_collaboration,
            )
        return state

    elif action_type == "skunkworks/log_exploration":
        payload = action.get("payload", {})
        log = ExplorationLog(
            id=payload.get("id"),
            iteration=payload.get("iteration"),
            action_type=payload.get("action_type"),
            description=payload.get("description"),
            result=payload.get("result"),
        )
        new_history = (state.exploration_history + [log])[-500:]
        if state.active_session:
            state.active_session.exploration_logs.append(log)
            state.active_session.iteration_count = payload.get("iteration", 0)
        return SkunkworksState(
            active_session=state.active_session,
            hypotheses=state.hypotheses,
            exploration_history=new_history,
            certified_hypotheses=state.certified_hypotheses,
            rejected_hypotheses=state.rejected_hypotheses,
            pending_collaboration=state.pending_collaboration,
        )

    elif action_type == "skunkworks/request_collaboration":
        payload = action.get("payload", {})
        request = UserCollaborationRequest(
            id=payload.get("id"),
            question=payload.get("question"),
            context=payload.get("context"),
        )
        new_pending = state.pending_collaboration + [request]
        if state.active_session:
            state.active_session.collaboration_requests.append(request)
            state.active_session.status = SkunkworksStatus.USER_COLLABORATION
        return SkunkworksState(
            active_session=state.active_session,
            hypotheses=state.hypotheses,
            exploration_history=state.exploration_history,
            certified_hypotheses=state.certified_hypotheses,
            rejected_hypotheses=state.rejected_hypotheses,
            pending_collaboration=new_pending,
        )

    elif action_type == "skunkworks/respond_to_collaboration":
        payload = action.get("payload", {})
        request_id = payload.get("request_id")
        response = payload.get("response")
        new_pending = []
        for req in state.pending_collaboration:
            if req.id == request_id:
                req.responded = True
                req.response = response
                req.responded_at = time.time()
            else:
                new_pending.append(req)
        for req in (
            state.active_session.collaboration_requests if state.active_session else []
        ):
            if req.id == request_id:
                req.responded = True
                req.response = response
                req.responded_at = time.time()
        return SkunkworksState(
            active_session=state.active_session,
            hypotheses=state.hypotheses,
            exploration_history=state.exploration_history,
            certified_hypotheses=state.certified_hypotheses,
            rejected_hypotheses=state.rejected_hypotheses,
            pending_collaboration=new_pending,
        )

    elif action_type == "skunkworks/complete_session":
        if state.active_session:
            state.active_session.status = SkunkworksStatus.COMPLETED
            state.active_session.completed_at = time.time()
        return SkunkworksState(
            active_session=state.active_session,
            hypotheses=state.hypotheses,
            exploration_history=state.exploration_history,
            certified_hypotheses=state.certified_hypotheses,
            rejected_hypotheses=state.rejected_hypotheses,
            pending_collaboration=state.pending_collaboration,
        )

    elif action_type == "skunkworks/transition_to_crucible":
        payload = action.get("payload", {})
        if state.active_session:
            state.active_session.active_hypothesis_id = payload.get("hypothesis_id")
            state.active_session.status = SkunkworksStatus.TRANSITIONING_TO_CRITICAL
        return SkunkworksState(
            active_session=state.active_session,
            hypotheses=state.hypotheses,
            exploration_history=state.exploration_history,
            certified_hypotheses=state.certified_hypotheses,
            rejected_hypotheses=state.rejected_hypotheses,
            pending_collaboration=state.pending_collaboration,
        )

    return state
