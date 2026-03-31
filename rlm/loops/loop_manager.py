"""
Loop Manager - Coordinates the Dual-Loop Architecture.

This module manages the Fast Loop and Slow Loop, providing a unified interface
for starting, stopping, and monitoring both loops. It handles the coordination
between creative discovery (Fast Loop) and formal verification (Slow Loop).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
import threading
import time

from rlm.loops.message_queue import AsyncMessageQueue, MessageType
from rlm.loops.interrupt_protocol import InterruptProtocol
from rlm.loops.fast_loop import (
    FastLoop,
    FastLoopStatus,
    TaskDescriptor,
    ReleaseCandidate,
)
from rlm.loops.slow_loop import SlowLoop, SlowLoopStatus, CertifiedCandidate


@dataclass
class DualLoopMetrics:
    """Combined metrics for both loops."""

    fast_loop: Dict[str, Any]
    slow_loop: Dict[str, Any]
    queue_stats: Dict[str, Any]
    interrupt_stats: Dict[str, Any]


class LoopManager:
    """
    Manager for the Dual-Loop Architecture.

    Responsibilities:
    1. Initialize and coordinate Fast Loop and Slow Loop
    2. Provide unified status and metrics
    3. Handle task submission and result retrieval
    4. Manage loop lifecycle (start, stop, pause, resume)
    """

    def __init__(self, type_checker_registry=None):
        """
        Initialize the Loop Manager.

        Args:
            type_checker_registry: Optional registry for type checkers
        """
        # Create shared components
        self._message_queue = AsyncMessageQueue()
        self._interrupt_protocol = InterruptProtocol()

        # Create loops
        self._fast_loop = FastLoop(self._message_queue, self._interrupt_protocol)
        self._slow_loop = SlowLoop(
            self._message_queue, self._interrupt_protocol, type_checker_registry
        )

        self._lock = threading.Lock()
        self._running = False
        self._callbacks: Dict[str, List[Callable]] = {
            "task_complete": [],
            "candidate_certified": [],
            "verification_failed": [],
            "loop_status": [],
        }

        # Register for loop events
        self._fast_loop.register_callback("status_change", self._on_fast_loop_status)
        self._slow_loop.register_callback("status_change", self._on_slow_loop_status)
        self._slow_loop.register_callback("certification", self._on_candidate_certified)
        self._slow_loop.register_callback("verification", self._on_verification_failed)

    def start(self) -> None:
        """Start both loops."""
        with self._lock:
            if self._running:
                return

            self._running = True
            self._fast_loop.start()
            self._slow_loop.start()
            self._emit("loop_status", self.get_status())

    def stop(self) -> None:
        """Stop both loops."""
        with self._lock:
            if not self._running:
                return

            self._running = False
            self._fast_loop.stop()
            self._slow_loop.stop()
            self._emit("loop_status", self.get_status())

    def pause(self) -> None:
        """Pause both loops."""
        self._fast_loop.pause()
        self._slow_loop.pause()

    def resume(self) -> None:
        """Resume both loops."""
        self._fast_loop.resume()
        self._slow_loop.resume()

    def submit_task(
        self,
        task_id: str,
        description: str,
        domain: str,
        constraints: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Submit a task for processing.

        Args:
            task_id: Unique identifier for the task
            description: Human-readable description
            domain: Domain classification
            constraints: Optional task constraints
        """
        task = TaskDescriptor(
            task_id=task_id,
            description=description,
            domain=domain,
            constraints=constraints,
        )
        self._fast_loop.process_task(task)

    def submit_candidate(
        self,
        description: str,
        formal_structure: str,
        code: str,
    ) -> ReleaseCandidate:
        """
        Submit a release candidate for verification.

        Args:
            description: Description of the candidate
            formal_structure: Lean/Haskell formal structure
            code: Implementation code

        Returns:
            The submitted release candidate
        """
        return self._fast_loop.submit_candidate(description, formal_structure, code)

    def acknowledge_interrupt(
        self, interrupt_id: str, response: str, will_comply: bool
    ) -> bool:
        """
        Acknowledge an interrupt.

        Args:
            interrupt_id: ID of the interrupt
            response: Response message
            will_comply: Whether the Fast Loop will comply

        Returns:
            True if acknowledged successfully
        """
        return self._fast_loop.acknowledge_interrupt(
            interrupt_id, response, will_comply
        )

    def get_fast_loop_status(self) -> FastLoopStatus:
        """Get Fast Loop status."""
        return self._fast_loop.get_status()

    def get_slow_loop_status(self) -> SlowLoopStatus:
        """Get Slow Loop status."""
        return self._slow_loop.get_status()

    def get_fast_loop_metrics(self) -> Dict[str, Any]:
        """Get Fast Loop metrics."""
        return self._fast_loop.get_metrics().__dict__

    def get_slow_loop_metrics(self) -> Dict[str, Any]:
        """Get Slow Loop metrics."""
        return self._slow_loop.get_metrics().__dict__

    def get_queue_stats(self) -> Dict[str, Any]:
        """Get message queue statistics."""
        return self._message_queue.get_stats()

    def get_interrupt_stats(self) -> Dict[str, Any]:
        """Get interrupt protocol statistics."""
        return self._interrupt_protocol.get_stats()

    def get_metrics(self) -> DualLoopMetrics:
        """Get combined metrics for both loops."""
        return DualLoopMetrics(
            fast_loop=self.get_fast_loop_metrics(),
            slow_loop=self.get_slow_loop_metrics(),
            queue_stats=self.get_queue_stats(),
            interrupt_stats=self.get_interrupt_stats(),
        )

    def get_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        return {
            "running": self._running,
            "fast_loop": self._fast_loop.get_status().value,
            "slow_loop": self._slow_loop.get_status().value,
            "queue_size": self._message_queue.size(),
            "pending_interrupts": len(
                self._interrupt_protocol.get_pending_interrupts()
            ),
        }

    def get_pending_interrupts(self) -> List:
        """Get all pending interrupts."""
        return self._interrupt_protocol.get_pending_interrupts()

    def get_certified_candidates(self) -> List[CertifiedCandidate]:
        """Get all certified candidates."""
        return self._slow_loop.get_all_certified_candidates()

    def get_certified_candidate(
        self, candidate_id: str
    ) -> Optional[CertifiedCandidate]:
        """Get a specific certified candidate."""
        return self._slow_loop.get_certified_candidate(candidate_id)

    def register_callback(self, event: str, callback: Callable) -> None:
        """
        Register a callback for loop events.

        Args:
            event: Event type
            callback: Function to call
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

    def _on_fast_loop_status(self, data: Dict[str, Any]) -> None:
        """Handle Fast Loop status change."""
        self._emit("loop_status", self.get_status())

    def _on_slow_loop_status(self, data: Dict[str, Any]) -> None:
        """Handle Slow Loop status change."""
        self._emit("loop_status", self.get_status())

    def _on_candidate_certified(self, data: Dict[str, Any]) -> None:
        """Handle candidate certification."""
        self._emit("candidate_certified", data)

        # Also emit task_complete if this completes a task
        candidate_id = data.get("candidate_id")
        if candidate_id:
            certified = self._slow_loop.get_certified_candidate(candidate_id)
            if certified:
                self._emit(
                    "task_complete",
                    {
                        "task_id": certified.task_id,
                        "candidate_id": candidate_id,
                        "status": "certified",
                    },
                )

    def _on_verification_failed(self, data: Dict[str, Any]) -> None:
        """Handle verification failure."""
        self._emit("verification_failed", data)

    def _emit(self, event: str, data: Dict[str, Any]) -> None:
        """Emit an event to all registered callbacks."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(data)
            except Exception:
                pass
