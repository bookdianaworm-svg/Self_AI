"""
Skunkworks Module - Context of Discovery.

This module implements the Skunkworks Protocol for handling open-ended tasks
where the starting point is unknown. It decouples creative discovery from
formal verification, allowing unbounded exploration while maintaining safety.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
from enum import Enum
import threading
import time
import uuid

from rlm.loops.message_queue import AsyncMessageQueue, QueueMessage, MessagePriority


class SkunkworksStatus(Enum):
    """Status of skunkworks session."""

    IDLE = "idle"
    EXPLORING = "exploring"
    HYPOTHESIZING = "hypothesizing"
    ITERATING = "iterating"
    USER_COLLABORATION = "user_collaboration"
    TRANSITIONING = "transitioning"
    COMPLETED = "completed"


class HypothesisConfidence(Enum):
    """Confidence level of a hypothesis."""

    SPECULATIVE = "speculative"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class Hypothesis:
    """A hypothesis generated during skunkworks exploration."""

    id: str
    description: str
    confidence: HypothesisConfidence
    supporting_evidence: List[str] = field(default_factory=list)
    refined_count: int = 0
    created_at: float = field(default_factory=time.time)
    certified: bool = False


@dataclass
class ExplorationStep:
    """A single step in the exploration process."""

    id: str
    iteration: int
    action_type: str  # "web_search", "code_test", "user_query", "hypothesis_refine"
    action_description: str
    result: str
    duration_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class UserCollaborationRequest:
    """Request for user input during exploration."""

    id: str
    question: str
    context: str
    asked_at: float = field(default_factory=time.time)
    responded: bool = False
    response: Optional[str] = None
    responded_at: Optional[float] = None


@dataclass
class SkunkworksSession:
    """A complete skunkworks exploration session."""

    id: str
    task_description: str
    status: SkunkworksStatus = SkunkworksStatus.IDLE
    exploration_log: List[ExplorationStep] = field(default_factory=list)
    current_hypothesis: Optional[Hypothesis] = None
    collaboration_requests: List[UserCollaborationRequest] = field(default_factory=list)
    iteration_count: int = 0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None


class SkunkworksProtocol:
    """
    Protocol for managing skunkworks exploration sessions.

    Responsibilities:
    1. Manage exploration sessions
    2. Generate and refine hypotheses
    3. Handle user collaboration requests
    4. Transition hypotheses to formal verification
    """

    def __init__(self, message_queue: Optional[AsyncMessageQueue] = None):
        """
        Initialize the skunkworks protocol.

        Args:
            message_queue: Optional message queue for integration with loops
        """
        self._message_queue = message_queue
        self._active_session: Optional[SkunkworksSession] = None
        self._hypothesis_history: List[Hypothesis] = []
        self._lock = threading.Lock()
        self._callbacks: Dict[str, List[Callable]] = {
            "hypothesis_generated": [],
            "hypothesis_certified": [],
            "user_collaboration": [],
            "exploration_step": [],
            "session_complete": [],
        }

    def start_session(self, task_description: str) -> SkunkworksSession:
        """
        Start a new skunkworks exploration session.

        Args:
            task_description: The task to explore

        Returns:
            The created session
        """
        with self._lock:
            session = SkunkworksSession(
                id=str(uuid.uuid4()),
                task_description=task_description,
                status=SkunkworksStatus.EXPLORING,
                started_at=time.time(),
            )
            self._active_session = session
            return session

    def log_exploration_step(
        self,
        action_type: str,
        action_description: str,
        result: str,
        duration_ms: float = 0.0,
    ) -> ExplorationStep:
        """
        Log an exploration step.

        Args:
            action_type: Type of action taken
            action_description: Description of the action
            result: Result of the action
            duration_ms: Duration in milliseconds

        Returns:
            The created exploration step
        """
        with self._lock:
            if not self._active_session:
                raise ValueError("No active session")

            step = ExplorationStep(
                id=str(uuid.uuid4()),
                iteration=self._active_session.iteration_count,
                action_type=action_type,
                action_description=action_description,
                result=result,
                duration_ms=duration_ms,
            )

            self._active_session.exploration_log.append(step)
            self._emit("exploration_step", {"step": step})

            return step

    def generate_hypothesis(
        self,
        description: str,
        confidence: HypothesisConfidence,
        evidence: Optional[List[str]] = None,
    ) -> Hypothesis:
        """
        Generate a new hypothesis.

        Args:
            description: Description of the hypothesis
            confidence: Confidence level
            evidence: Supporting evidence

        Returns:
            The generated hypothesis
        """
        with self._lock:
            if not self._active_session:
                raise ValueError("No active session")

            self._active_session.status = SkunkworksStatus.HYPOTHESIZING

            hypothesis = Hypothesis(
                id=str(uuid.uuid4()),
                description=description,
                confidence=confidence,
                supporting_evidence=evidence or [],
            )

            self._active_session.current_hypothesis = hypothesis
            self._hypothesis_history.append(hypothesis)

            self._emit("hypothesis_generated", {"hypothesis": hypothesis})

            return hypothesis

    def refine_hypothesis(
        self,
        new_evidence: List[str],
        new_confidence: Optional[HypothesisConfidence] = None,
    ) -> Hypothesis:
        """
        Refine the current hypothesis with new evidence.

        Args:
            new_evidence: New evidence to add
            new_confidence: Optional new confidence level

        Returns:
            The refined hypothesis
        """
        with self._lock:
            if not self._active_session or not self._active_session.current_hypothesis:
                raise ValueError("No active hypothesis")

            hypothesis = self._active_session.current_hypothesis
            hypothesis.supporting_evidence.extend(new_evidence)
            hypothesis.refined_count += 1

            if new_confidence:
                hypothesis.confidence = new_confidence

            self._active_session.status = SkunkworksStatus.ITERATING
            self._active_session.iteration_count += 1

            return hypothesis

    def request_user_collaboration(
        self,
        question: str,
        context: str,
    ) -> UserCollaborationRequest:
        """
        Request collaboration from the user.

        Args:
            question: Question to ask the user
            context: Context for the question

        Returns:
            The created collaboration request
        """
        with self._lock:
            if not self._active_session:
                raise ValueError("No active session")

            request = UserCollaborationRequest(
                id=str(uuid.uuid4()),
                question=question,
                context=context,
            )

            self._active_session.collaboration_requests.append(request)
            self._active_session.status = SkunkworksStatus.USER_COLLABORATION

            self._emit("user_collaboration", {"request": request})

            return request

    def receive_user_response(self, request_id: str, response: str) -> bool:
        """
        Record a user's response to a collaboration request.

        Args:
            request_id: ID of the request
            response: User's response

        Returns:
            True if response was recorded
        """
        with self._lock:
            if not self._active_session:
                return False

            for req in self._active_session.collaboration_requests:
                if req.id == request_id:
                    req.responded = True
                    req.response = response
                    req.responded_at = time.time()

                    self._active_session.status = SkunkworksStatus.ITERATING
                    return True

            return False

    def certify_hypothesis(self) -> Optional[Hypothesis]:
        """
        Certify the current hypothesis as high-confidence.

        Returns:
            The certified hypothesis, or None if no hypothesis
        """
        with self._lock:
            if not self._active_session or not self._active_session.current_hypothesis:
                return None

            hypothesis = self._active_session.current_hypothesis

            # Check if hypothesis meets certification criteria
            if len(hypothesis.supporting_evidence) < 3:
                return None

            if hypothesis.confidence not in (
                HypothesisConfidence.HIGH,
                HypothesisConfidence.VERY_HIGH,
            ):
                return None

            hypothesis.certified = True
            self._active_session.status = SkunkworksStatus.TRANSITIONING

            self._emit("hypothesis_certified", {"hypothesis": hypothesis})

            return hypothesis

    def transition_to_verification(self) -> Dict[str, Any]:
        """
        Transition the certified hypothesis to formal verification.

        Returns:
            Dictionary with hypothesis data for verification
        """
        with self._lock:
            if not self._active_session:
                raise ValueError("No active session")

            if not self._active_session.current_hypothesis:
                raise ValueError("No hypothesis to transition")

            hypothesis = self._active_session.current_hypothesis

            if not hypothesis.certified:
                raise ValueError("Hypothesis must be certified before transition")

            transition_data = {
                "hypothesis_id": hypothesis.id,
                "description": hypothesis.description,
                "evidence": hypothesis.supporting_evidence,
                "confidence": hypothesis.confidence.value,
                "session_id": self._active_session.id,
                "exploration_log": [
                    {
                        "id": step.id,
                        "action_type": step.action_type,
                        "result": step.result,
                    }
                    for step in self._active_session.exploration_log
                ],
            }

            # Send to message queue if available
            if self._message_queue:
                message = QueueMessage(
                    id=str(uuid.uuid4()),
                    message_type=MessagePriority.HIGH,
                    payload=transition_data,
                )
                self._message_queue.enqueue(message)

            self._active_session.status = SkunkworksStatus.COMPLETED
            self._active_session.completed_at = time.time()

            self._emit(
                "session_complete",
                {
                    "session": self._active_session,
                    "transition_data": transition_data,
                },
            )

            return transition_data

    def complete_session(self) -> SkunkworksSession:
        """
        Complete the current session without transitioning.

        Returns:
            The completed session
        """
        with self._lock:
            if not self._active_session:
                raise ValueError("No active session")

            self._active_session.status = SkunkworksStatus.COMPLETED
            self._active_session.completed_at = time.time()

            return self._active_session

    def get_active_session(self) -> Optional[SkunkworksSession]:
        """Get the currently active session."""
        with self._lock:
            return self._active_session

    def get_hypothesis_history(self) -> List[Hypothesis]:
        """Get all hypotheses generated in this protocol."""
        with self._lock:
            return self._hypothesis_history.copy()

    def register_callback(self, event: str, callback: Callable) -> None:
        """
        Register a callback for protocol events.

        Args:
            event: Event type
            callback: Function to call
        """
        if event in self._callbacks and callback not in self._callbacks[event]:
            self._callbacks[event].append(callback)

    def _emit(self, event: str, data: Dict[str, Any]) -> None:
        """Emit an event to callbacks."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(data)
            except Exception:
                pass
