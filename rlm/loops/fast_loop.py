"""
Fast Loop (Skunkworks) Implementation.

The Fast Loop handles creative discovery, rapid iteration, and user interaction.
It operates like a standard autonomous AI - writing draft code, querying the web,
running local scripts, and iterating rapidly. All logs and thoughts stream to the
user interface in real-time.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
from enum import Enum
import threading
import time
import uuid

from rlm.loops.message_queue import (
    AsyncMessageQueue,
    QueueMessage,
    MessageType,
    MessagePriority,
)
from rlm.loops.interrupt_protocol import (
    InterruptProtocol,
    Interrupt,
    InterruptType,
    InterruptSeverity,
)


class FastLoopStatus(Enum):
    """Status of the Fast Loop."""

    IDLE = "idle"
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    WAITING_FOR_INTERRUPT = "waiting_for_interrupt"
    STOPPING = "stopping"
    STOPPED = "stopped"


class TaskDescriptor:
    """Descriptor for a task to be processed by the Fast Loop."""

    def __init__(
        self,
        task_id: str,
        description: str,
        domain: str,
        constraints: Optional[Dict[str, Any]] = None,
    ):
        self.task_id = task_id
        self.description = description
        self.domain = domain
        self.constraints = constraints or {}
        self.created_at = time.time()


@dataclass
class FastLoopMetrics:
    """Metrics for Fast Loop performance."""

    iterations_completed: int = 0
    tasks_processed: int = 0
    release_candidates_submitted: int = 0
    interrupts_received: int = 0
    interrupts_acknowledged: int = 0
    avg_iteration_time_ms: float = 0.0
    total_processing_time_ms: float = 0.0


@dataclass
class ReleaseCandidate:
    """
    A release candidate produced by the Fast Loop for Slow Loop verification.

    This is the output of the Fast Loop that gets packaged and sent to the
    Async Message Queue for the Slow Loop to verify.
    """

    id: str
    task_id: str
    description: str
    formal_structure: str
    code: str
    domain: str
    iteration: int
    created_at: float = field(default_factory=time.time)
    certified: bool = False
    certified_at: Optional[float] = None


class FastLoop:
    """
    Fast Loop (Skunkworks) processor.

    Responsibilities:
    1. Process tasks through rapid iteration
    2. Generate release candidates for verification
    3. Stream progress to user interface
    4. Handle interrupts from Slow Loop
    5. Integrate certified candidates as frozen foundation
    """

    def __init__(
        self,
        message_queue: AsyncMessageQueue,
        interrupt_protocol: InterruptProtocol,
    ):
        """
        Initialize the Fast Loop.

        Args:
            message_queue: Queue for sending/receiving messages to/from Slow Loop
            interrupt_protocol: Protocol for handling interrupts
        """
        self._message_queue = message_queue
        self._interrupt_protocol = interrupt_protocol
        self._status = FastLoopStatus.IDLE
        self._current_task: Optional[TaskDescriptor] = None
        self._current_iteration: int = 0
        self._metrics = FastLoopMetrics()
        self._lock = threading.Lock()
        self._running = False
        self._paused = False
        self._callbacks: Dict[str, List[Callable]] = {
            "iteration": [],
            "candidate": [],
            "interrupt": [],
            "status_change": [],
        }

        # Register interrupt handler
        self._interrupt_protocol.register_callback(
            InterruptType.VERIFICATION_FAILED, self._handle_verification_failed
        )
        self._interrupt_protocol.register_callback(
            InterruptType.EMERGENCY_STOP, self._handle_emergency_stop
        )

    def start(self) -> None:
        """Start the Fast Loop."""
        with self._lock:
            if self._status in (FastLoopStatus.RUNNING, FastLoopStatus.PAUSED):
                return

            self._status = FastLoopStatus.INITIALIZING
            self._running = True
            self._emit_status_change()

            # Register message handler for interrupts
            self._message_queue.register_handler(
                MessageType.INTERRUPT, self._handle_interrupt_message
            )

            self._status = FastLoopStatus.RUNNING
            self._emit_status_change()

    def stop(self) -> None:
        """Stop the Fast Loop."""
        with self._lock:
            self._status = FastLoopStatus.STOPPING
            self._emit_status_change()
            self._running = False
            self._message_queue.unregister_handler(
                MessageType.INTERRUPT, self._handle_interrupt_message
            )
            self._status = FastLoopStatus.STOPPED
            self._emit_status_change()

    def pause(self) -> None:
        """Pause the Fast Loop."""
        with self._lock:
            if self._status == FastLoopStatus.RUNNING:
                self._status = FastLoopStatus.PAUSED
                self._paused = True
                self._emit_status_change()

    def resume(self) -> None:
        """Resume the Fast Loop."""
        with self._lock:
            if self._status == FastLoopStatus.PAUSED:
                self._status = FastLoopStatus.RUNNING
                self._paused = False
                self._emit_status_change()

    def process_task(self, task: TaskDescriptor) -> None:
        """
        Process a task through the Fast Loop.

        Args:
            task: The task to process
        """
        with self._lock:
            if self._status != FastLoopStatus.RUNNING:
                return
            self._current_task = task
            self._current_iteration = 0

        self._run_iteration()

    def _run_iteration(self) -> None:
        """Run a single iteration of the Fast Loop."""
        start_time = time.time()

        with self._lock:
            if not self._running or self._current_task is None:
                return
            self._current_iteration += 1
            iteration = self._current_iteration

        # Emit iteration callback (for streaming to UI)
        self._emit(
            "iteration",
            {
                "task_id": self._current_task.task_id,
                "iteration": iteration,
                "status": "in_progress",
            },
        )

        # Simulate work being done (in real implementation, this would be
        # actual agent work: code generation, web queries, etc.)
        # For now, we just update metrics

        iteration_time = (time.time() - start_time) * 1000

        with self._lock:
            self._metrics.iterations_completed += 1
            self._metrics.total_processing_time_ms += iteration_time
            self._metrics.avg_iteration_time_ms = (
                self._metrics.total_processing_time_ms
                / self._metrics.iterations_completed
            )

        # Emit iteration complete
        self._emit(
            "iteration",
            {
                "task_id": self._current_task.task_id,
                "iteration": iteration,
                "status": "complete",
                "duration_ms": iteration_time,
            },
        )

    def submit_candidate(
        self,
        description: str,
        formal_structure: str,
        code: str,
    ) -> ReleaseCandidate:
        """
        Submit a release candidate for Slow Loop verification.

        Args:
            description: Human-readable description of the candidate
            formal_structure: Lean/Haskell formal structure
            code: The actual code/implementation

        Returns:
            The created release candidate
        """
        with self._lock:
            if self._current_task is None:
                raise ValueError("No current task")

            candidate = ReleaseCandidate(
                id=str(uuid.uuid4()),
                task_id=self._current_task.task_id,
                description=description,
                formal_structure=formal_structure,
                code=code,
                domain=self._current_task.domain,
                iteration=self._current_iteration,
            )

        # Enqueue for Slow Loop processing
        message = QueueMessage(
            id=candidate.id,
            message_type=MessageType.RELEASE_CANDIDATE,
            payload=candidate,
            priority=MessagePriority.NORMAL,
            correlation_id=self._current_task.task_id,
        )
        self._message_queue.enqueue(message)

        with self._lock:
            self._metrics.release_candidates_submitted += 1

        # Emit candidate submitted
        self._emit(
            "candidate",
            {
                "candidate_id": candidate.id,
                "task_id": candidate.task_id,
                "status": "submitted",
            },
        )

        return candidate

    def acknowledge_interrupt(
        self, interrupt_id: str, response: str, will_comply: bool
    ) -> bool:
        """
        Acknowledge an interrupt from the Slow Loop.

        Args:
            interrupt_id: ID of the interrupt to acknowledge
            response: Response message
            will_comply: Whether the Fast Loop will comply

        Returns:
            True if acknowledged successfully
        """
        result = self._interrupt_protocol.acknowledge_interrupt(
            interrupt_id, response, will_comply
        )

        if result:
            with self._lock:
                self._metrics.interrupts_acknowledged += 1
                if will_comply:
                    self._status = FastLoopStatus.WAITING_FOR_INTERRUPT

            # Emit interrupt acknowledged
            self._emit(
                "interrupt",
                {
                    "interrupt_id": interrupt_id,
                    "acknowledged": True,
                    "will_comply": will_comply,
                },
            )

        return result

    def get_status(self) -> FastLoopStatus:
        """Get the current status of the Fast Loop."""
        return self._status

    def get_metrics(self) -> FastLoopMetrics:
        """Get Fast Loop metrics."""
        with self._lock:
            return FastLoopMetrics(
                iterations_completed=self._metrics.iterations_completed,
                tasks_processed=self._metrics.tasks_processed,
                release_candidates_submitted=self._metrics.release_candidates_submitted,
                interrupts_received=self._metrics.interrupts_received,
                interrupts_acknowledged=self._metrics.interrupts_acknowledged,
                avg_iteration_time_ms=self._metrics.avg_iteration_time_ms,
                total_processing_time_ms=self._metrics.total_processing_time_ms,
            )

    def get_pending_interrupts(self) -> List[Interrupt]:
        """Get all pending interrupts."""
        return self._interrupt_protocol.get_pending_interrupts()

    def register_callback(self, event: str, callback: Callable) -> None:
        """
        Register a callback for Fast Loop events.

        Args:
            event: Event type ('iteration', 'candidate', 'interrupt', 'status_change')
            callback: Function to call when event occurs
        """
        if event in self._callbacks and callback not in self._callbacks[event]:
            self._callbacks[event].append(callback)

    def unregister_callback(self, event: str, callback: Callable) -> None:
        """
        Unregister a callback.

        Args:
            event: Event type
            callback: Callback to remove
        """
        if event in self._callbacks and callback in self._callbacks[event]:
            self._callbacks[event].remove(callback)

    def _handle_interrupt_message(self, message: QueueMessage) -> None:
        """Handle an interrupt message from the queue."""
        interrupt = message.payload
        with self._lock:
            self._metrics.interrupts_received += 1

        # Emit interrupt received
        self._emit(
            "interrupt",
            {
                "interrupt_id": interrupt.id,
                "type": interrupt.interrupt_type.value,
                "message": interrupt.message,
            },
        )

    def _handle_verification_failed(self, interrupt: Interrupt) -> None:
        """Handle a verification failed interrupt."""
        with self._lock:
            self._status = FastLoopStatus.WAITING_FOR_INTERRUPT

        self._emit(
            "interrupt",
            {
                "interrupt_id": interrupt.id,
                "type": "verification_failed",
                "message": interrupt.message,
                "constraint": interrupt.mathematical_constraint,
                "suggested_fix": interrupt.suggested_fix,
            },
        )

    def _handle_emergency_stop(self, interrupt: Interrupt) -> None:
        """Handle an emergency stop interrupt."""
        self._running = False
        with self._lock:
            self._status = FastLoopStatus.STOPPED

        self._emit(
            "interrupt",
            {
                "interrupt_id": interrupt.id,
                "type": "emergency_stop",
                "message": interrupt.message,
            },
        )

    def _emit(self, event: str, data: Dict[str, Any]) -> None:
        """Emit an event to all registered callbacks."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(data)
            except Exception:
                pass

    def _emit_status_change(self) -> None:
        """Emit a status change event."""
        self._emit(
            "status_change",
            {
                "status": self._status.value,
                "task_id": self._current_task.task_id if self._current_task else None,
            },
        )
