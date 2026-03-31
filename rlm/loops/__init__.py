"""
Dual-Loop Architecture Module.

This module implements the Universal Dual-Loop Architecture for decoupling
creative discovery (Fast Loop/Skunkworks) from formal verification
(Slow Loop/The Crucible).

Main Components:
- message_queue: Async queue for communication between loops
- interrupt_protocol: Protocol for handling verification failures
- fast_loop: Creative discovery and rapid iteration
- slow_loop: Formal verification using Lean/Haskell
- loop_manager: Coordinator for both loops
"""

from rlm.loops.message_queue import (
    AsyncMessageQueue,
    MessagePriority,
    MessageType,
    QueueMessage,
)

from rlm.loops.interrupt_protocol import (
    InterruptProtocol,
    InterruptType,
    InterruptSeverity,
    Interrupt,
    InterruptAcknowledgment,
)

from rlm.loops.fast_loop import (
    FastLoop,
    FastLoopStatus,
    TaskDescriptor,
    FastLoopMetrics,
    ReleaseCandidate,
)

from rlm.loops.slow_loop import (
    SlowLoop,
    SlowLoopStatus,
    VerificationResult,
    CertifiedCandidate,
    SlowLoopMetrics,
)

from rlm.loops.loop_manager import (
    LoopManager,
    DualLoopMetrics,
)

__all__ = [
    # Message Queue
    "AsyncMessageQueue",
    "MessagePriority",
    "MessageType",
    "QueueMessage",
    # Interrupt Protocol
    "InterruptProtocol",
    "InterruptType",
    "InterruptSeverity",
    "Interrupt",
    "InterruptAcknowledgment",
    # Fast Loop
    "FastLoop",
    "FastLoopStatus",
    "TaskDescriptor",
    "FastLoopMetrics",
    "ReleaseCandidate",
    # Slow Loop
    "SlowLoop",
    "SlowLoopStatus",
    "VerificationResult",
    "CertifiedCandidate",
    "SlowLoopMetrics",
    # Loop Manager
    "LoopManager",
    "DualLoopMetrics",
]
