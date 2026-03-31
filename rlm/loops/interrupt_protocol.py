"""
Interrupt Protocol for Dual-Loop Communication.

This module implements the handoff protocol between the Fast Loop and Slow Loop,
allowing the Slow Loop to interrupt the Fast Loop when verification fails.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
from enum import Enum
import threading
import time
import uuid


class InterruptType(Enum):
    """Types of interrupts that can be sent between loops."""

    VERIFICATION_FAILED = "verification_failed"
    CONSTRAINT_VIOLATION = "constraint_violation"
    TIMEOUT = "timeout"
    DOMAIN_MISMATCH = "domain_mismatch"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    USER_ABORT = "user_abort"
    EMERGENCY_STOP = "emergency_stop"


class InterruptSeverity(Enum):
    """Severity levels for interrupts."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class Interrupt:
    """
    Represents an interrupt from the Slow Loop to the Fast Loop.

    This is the core mechanism for the "bounce-back" when verification fails.
    """

    id: str
    interrupt_type: InterruptType
    severity: InterruptSeverity
    candidate_id: str
    message: str
    mathematical_constraint: str
    error_trace: Optional[str] = None
    suggested_fix: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    acknowledged: bool = False
    acknowledged_at: Optional[float] = None
    resolved: bool = False
    resolved_at: Optional[float] = None


@dataclass
class InterruptAcknowledgment:
    """Acknowledgment of an interrupt from the Fast Loop."""

    interrupt_id: str
    fast_loop_response: str
    will_comply: bool
    acknowledged_at: float = field(default_factory=time.time)


class InterruptProtocol:
    """
    Protocol handler for interrupt communication between loops.

    Responsibilities:
    1. Create and send interrupts from Slow Loop to Fast Loop
    2. Track interrupt lifecycle (pending -> acknowledged -> resolved)
    3. Translate Lean/Haskell error messages into human-readable constraints
    4. Handle emergency stops
    """

    def __init__(self):
        """Initialize the interrupt protocol handler."""
        self._interrupts: Dict[str, Interrupt] = {}
        self._pending_interrupts: List[str] = []
        self._acknowledged_interrupts: List[str] = []
        self._resolved_interrupts: List[str] = []
        self._lock = threading.Lock()
        self._callbacks: Dict[InterruptType, List[Callable]] = {
            it: [] for it in InterruptType
        }
        self._stats = {
            "total_created": 0,
            "total_acknowledged": 0,
            "total_resolved": 0,
        }

    def create_interrupt(
        self,
        interrupt_type: InterruptType,
        candidate_id: str,
        message: str,
        mathematical_constraint: str,
        severity: InterruptSeverity = InterruptSeverity.ERROR,
        error_trace: Optional[str] = None,
        suggested_fix: Optional[str] = None,
    ) -> Interrupt:
        """
        Create a new interrupt.

        Args:
            interrupt_type: Type of interrupt
            candidate_id: ID of the release candidate that triggered this
            message: Human-readable message
            mathematical_constraint: The specific constraint that was violated
            severity: Severity level
            error_trace: Optional error trace from the verifier
            suggested_fix: Optional suggested fix for the Fast Loop

        Returns:
            The created interrupt
        """
        interrupt = Interrupt(
            id=str(uuid.uuid4()),
            interrupt_type=interrupt_type,
            severity=severity,
            candidate_id=candidate_id,
            message=message,
            mathematical_constraint=mathematical_constraint,
            error_trace=error_trace,
            suggested_fix=suggested_fix,
        )

        with self._lock:
            self._interrupts[interrupt.id] = interrupt
            self._pending_interrupts.append(interrupt.id)
            self._stats["total_created"] += 1

        return interrupt

    def acknowledge_interrupt(
        self, interrupt_id: str, response: str, will_comply: bool
    ) -> bool:
        """
        Acknowledge an interrupt from the Fast Loop.

        Args:
            interrupt_id: ID of the interrupt to acknowledge
            response: Fast Loop's response message
            will_comply: Whether the Fast Loop will comply with the interrupt

        Returns:
            True if acknowledged successfully, False if interrupt not found
        """
        with self._lock:
            interrupt = self._interrupts.get(interrupt_id)
            if not interrupt:
                return False

            interrupt.acknowledged = True
            interrupt.acknowledged_at = time.time()

            # Move from pending to acknowledged
            if interrupt_id in self._pending_interrupts:
                self._pending_interrupts.remove(interrupt_id)
            if interrupt_id not in self._acknowledged_interrupts:
                self._acknowledged_interrupts.append(interrupt_id)

            self._stats["total_acknowledged"] += 1

        return True

    def resolve_interrupt(self, interrupt_id: str) -> bool:
        """
        Mark an interrupt as resolved.

        Args:
            interrupt_id: ID of the interrupt to resolve

        Returns:
            True if resolved successfully, False if interrupt not found
        """
        with self._lock:
            interrupt = self._interrupts.get(interrupt_id)
            if not interrupt:
                return False

            interrupt.resolved = True
            interrupt.resolved_at = time.time()

            # Move from acknowledged to resolved
            if interrupt_id in self._acknowledged_interrupts:
                self._acknowledged_interrupts.remove(interrupt_id)
            if interrupt_id not in self._resolved_interrupts:
                self._resolved_interrupts.append(interrupt_id)

            self._stats["total_resolved"] += 1

        return True

    def get_pending_interrupts(self) -> List[Interrupt]:
        """Get all pending (unacknowledged) interrupts."""
        with self._lock:
            return [
                self._interrupts[iid]
                for iid in self._pending_interrupts
                if iid in self._interrupts
            ]

    def get_acknowledged_interrupts(self) -> List[Interrupt]:
        """Get all acknowledged but unresolved interrupts."""
        with self._lock:
            return [
                self._interrupts[iid]
                for iid in self._acknowledged_interrupts
                if iid in self._interrupts
            ]

    def get_resolved_interrupts(self, limit: int = 100) -> List[Interrupt]:
        """Get recently resolved interrupts."""
        with self._lock:
            ids = list(self._resolved_interrupts)[-limit:]
            return [self._interrupts[iid] for iid in ids if iid in self._interrupts]

    def get_interrupt(self, interrupt_id: str) -> Optional[Interrupt]:
        """Get a specific interrupt by ID."""
        with self._lock:
            return self._interrupts.get(interrupt_id)

    def get_interrupts_by_candidate(self, candidate_id: str) -> List[Interrupt]:
        """Get all interrupts related to a specific release candidate."""
        with self._lock:
            return [
                i for i in self._interrupts.values() if i.candidate_id == candidate_id
            ]

    def get_critical_interrupts(self) -> List[Interrupt]:
        """Get all critical severity interrupts that are pending."""
        with self._lock:
            return [
                self._interrupts[iid]
                for iid in self._pending_interrupts
                if iid in self._interrupts
                and self._interrupts[iid].severity == InterruptSeverity.CRITICAL
            ]

    def register_callback(
        self, interrupt_type: InterruptType, callback: Callable[[Interrupt], None]
    ) -> None:
        """
        Register a callback to be called when an interrupt of a specific type is created.

        Args:
            interrupt_type: Type of interrupt to listen for
            callback: Function to call with the interrupt
        """
        with self._lock:
            if callback not in self._callbacks[interrupt_type]:
                self._callbacks[interrupt_type].append(callback)

    def unregister_callback(
        self, interrupt_type: InterruptType, callback: Callable[[Interrupt], None]
    ) -> None:
        """
        Unregister a callback.

        Args:
            interrupt_type: Type of interrupt
            callback: Callback to remove
        """
        with self._lock:
            if callback in self._callbacks[interrupt_type]:
                self._callbacks[interrupt_type].remove(callback)

    def dispatch_interrupt(self, interrupt: Interrupt) -> None:
        """
        Dispatch an interrupt to all registered callbacks.

        Args:
            interrupt: The interrupt to dispatch
        """
        with self._lock:
            callbacks = self._callbacks.get(interrupt.interrupt_type, []).copy()

        for callback in callbacks:
            try:
                callback(interrupt)
            except Exception:
                pass

    def translate_verification_error(
        self, error_type: str, error_message: str
    ) -> tuple[str, str]:
        """
        Translate a verification error into a human-readable message and constraint.

        Args:
            error_type: Type of verification error
            error_message: Raw error message from the verifier

        Returns:
            Tuple of (human_readable_message, mathematical_constraint)
        """
        # Common Lean error translations
        translations = {
            "type_mismatch": (
                f"Type mismatch error: {error_message}",
                "The expression must have the correct type",
            ),
            "type_error": (
                f"Type error detected: {error_message}",
                "Types must be compatible for the operation",
            ),
            " unification": (
                f"Unification failed: {error_message}",
                "Terms must be unifiable",
            ),
            "goal unsolved": (
                f"Proof goal not fully solved: {error_message}",
                "All proof goals must be closed",
            ),
        }

        for key, (msg, constraint) in translations.items():
            if key in error_message.lower():
                return msg, constraint

        # Default translation
        return (
            f"Verification failed: {error_message}",
            "The formal structure must satisfy all type and proof constraints",
        )

    def create_verification_failed_interrupt(
        self,
        candidate_id: str,
        error_type: str,
        error_message: str,
        error_trace: Optional[str] = None,
    ) -> Interrupt:
        """
        Create an interrupt for a verification failure.

        Args:
            candidate_id: ID of the release candidate
            error_type: Type of verification error
            error_message: Raw error message
            error_trace: Optional full error trace

        Returns:
            The created interrupt
        """
        message, constraint = self.translate_verification_error(
            error_type, error_message
        )

        interrupt = self.create_interrupt(
            interrupt_type=InterruptType.VERIFICATION_FAILED,
            candidate_id=candidate_id,
            message=message,
            mathematical_constraint=constraint,
            severity=InterruptSeverity.ERROR,
            error_trace=error_trace,
        )

        self.dispatch_interrupt(interrupt)
        return interrupt

    def create_emergency_stop(self, reason: str) -> Interrupt:
        """
        Create an emergency stop interrupt.

        Args:
            reason: Reason for the emergency stop

        Returns:
            The created interrupt
        """
        interrupt = self.create_interrupt(
            interrupt_type=InterruptType.EMERGENCY_STOP,
            candidate_id="",
            message=f"EMERGENCY STOP: {reason}",
            mathematical_constraint="ALL OPERATIONS MUST STOP IMMEDIATELY",
            severity=InterruptSeverity.CRITICAL,
        )

        self.dispatch_interrupt(interrupt)
        return interrupt

    def get_stats(self) -> Dict[str, Any]:
        """Get interrupt protocol statistics."""
        with self._lock:
            return {
                **self._stats,
                "pending_count": len(self._pending_interrupts),
                "acknowledged_count": len(self._acknowledged_interrupts),
                "resolved_count": len(self._resolved_interrupts),
                "total_interrupts": len(self._interrupts),
            }

    def clear_resolved(self, older_than: Optional[float] = None) -> int:
        """
        Clear resolved interrupts from memory.

        Args:
            older_than: Only clear interrupts resolved before this timestamp

        Returns:
            Number of interrupts cleared
        """
        with self._lock:
            if older_than is None:
                cleared = len(self._resolved_interrupts)
                for iid in self._resolved_interrupts:
                    if iid in self._interrupts:
                        del self._interrupts[iid]
                self._resolved_interrupts.clear()
            else:
                cleared = 0
                to_remove = []
                for iid in self._resolved_interrupts:
                    interrupt = self._interrupts.get(iid)
                    if (
                        interrupt
                        and interrupt.resolved_at
                        and interrupt.resolved_at < older_than
                    ):
                        to_remove.append(iid)
                        del self._interrupts[iid]
                        cleared += 1
                for iid in to_remove:
                    self._resolved_interrupts.remove(iid)
            return cleared
