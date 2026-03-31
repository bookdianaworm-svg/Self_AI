"""
Redux slice for verification state management.

This module provides state management for Layer 1 Axiomatic Foundation
verification, including Layer 1 loading status, theorem verification tracking,
and type checker status.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum


class VerificationStatus(Enum):
    """Status of verification operations."""

    PENDING = "pending"
    LOADING = "loading"
    LOADED = "loaded"
    FAILED = "failed"
    VERIFYING = "verifying"
    PASSED = "passed"
    FAILED_VERIFICATION = "failed_verification"


class TypeCheckerAvailabilityStatus(Enum):
    """Status of type checker availability."""

    UNKNOWN = "unknown"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


@dataclass
class Layer1State:
    """State of Layer 1 Axiomatic Foundation."""

    status: VerificationStatus = VerificationStatus.PENDING
    mathlib_version: Optional[str] = None
    physlib_version: Optional[str] = None
    load_time_ms: Optional[float] = None
    memory_mb: Optional[float] = None
    error: Optional[str] = None


@dataclass
class TheoremVerification:
    """State of a single theorem verification."""

    theorem_id: str
    status: VerificationStatus = VerificationStatus.PENDING
    layer2_file: Optional[str] = None
    proof_attempts: int = 0
    last_error: Optional[str] = None
    proof: Optional[str] = None


@dataclass
class TypeCheckerStatus:
    """State of a type checker (Haskell or Lean)."""

    checker_type: str  # 'haskell' or 'lean'
    availability: TypeCheckerAvailabilityStatus = TypeCheckerAvailabilityStatus.UNKNOWN
    version: Optional[str] = None
    last_check: Optional[float] = None
    error: Optional[str] = None


@dataclass
class TypeCheckRecord:
    """Record of a type checking operation."""

    code_type: str  # 'haskell' or 'lean'
    success: bool
    error_count: int = 0
    execution_time_ms: float = 0.0
    timestamp: float = 0.0
    errors: List[str] = field(default_factory=list)


@dataclass
class VerificationState:
    """Redux slice for verification state."""

    layer1: Layer1State = field(default_factory=Layer1State)
    theorems: Dict[str, TheoremVerification] = field(default_factory=dict)
    active_verification: Optional[str] = None
    verification_queue: List[str] = field(default_factory=list)
    # Type checker state
    haskell_status: TypeCheckerStatus = field(
        default_factory=lambda: TypeCheckerStatus(checker_type="haskell")
    )
    lean_status: TypeCheckerStatus = field(
        default_factory=lambda: TypeCheckerStatus(checker_type="lean")
    )
    type_check_history: List[TypeCheckRecord] = field(default_factory=list)


class VerificationActions:
    """Action creators for verification state updates."""

    @staticmethod
    def load_layer1_request() -> dict:
        """Create action to request Layer 1 loading."""
        return {"type": "verification/load_layer1_request"}

    @staticmethod
    def load_layer1_success(data: dict) -> dict:
        """
        Create action for successful Layer 1 loading.

        Args:
            data: Dictionary containing mathlib_version, physlib_version,
                  load_time_ms, and memory_mb.
        """
        return {"type": "verification/load_layer1_success", "payload": data}

    @staticmethod
    def load_layer1_failure(error: str) -> dict:
        """
        Create action for failed Layer 1 loading.

        Args:
            error: Error message describing the failure.
        """
        return {"type": "verification/load_layer1_failure", "payload": error}

    @staticmethod
    def verify_theorem_request(theorem_id: str, layer2_file: str) -> dict:
        """
        Create action to request theorem verification.

        Args:
            theorem_id: Unique identifier for the theorem.
            layer2_file: Path to the Layer 2 file containing the theorem.
        """
        return {
            "type": "verification/verify_theorem_request",
            "payload": {"theorem_id": theorem_id, "layer2_file": layer2_file},
        }

    @staticmethod
    def verify_theorem_success(theorem_id: str, proof: str) -> dict:
        """
        Create action for successful theorem verification.

        Args:
            theorem_id: Unique identifier for the theorem.
            proof: The verified proof.
        """
        return {
            "type": "verification/verify_theorem_success",
            "payload": {"theorem_id": theorem_id, "proof": proof},
        }

    @staticmethod
    def verify_theorem_failure(theorem_id: str, error: str) -> dict:
        """
        Create action for failed theorem verification.

        Args:
            theorem_id: Unique identifier for the theorem.
            error: Error message describing the failure.
        """
        return {
            "type": "verification/verify_theorem_failure",
            "payload": {"theorem_id": theorem_id, "error": error},
        }

    @staticmethod
    def update_haskell_checker_status(
        availability: TypeCheckerAvailabilityStatus,
        version: Optional[str] = None,
        error: Optional[str] = None,
    ) -> dict:
        """
        Create action to update Haskell checker status.

        Args:
            availability: Availability status of the checker.
            version: Optional version string of GHC.
            error: Optional error message.
        """
        return {
            "type": "verification/update_haskell_checker_status",
            "payload": {
                "availability": availability.value,
                "version": version,
                "error": error,
            },
        }

    @staticmethod
    def update_lean_checker_status(
        availability: TypeCheckerAvailabilityStatus,
        version: Optional[str] = None,
        error: Optional[str] = None,
    ) -> dict:
        """
        Create action to update Lean checker status.

        Args:
            availability: Availability status of the checker.
            version: Optional version string of Lean.
            error: Optional error message.
        """
        return {
            "type": "verification/update_lean_checker_status",
            "payload": {
                "availability": availability.value,
                "version": version,
                "error": error,
            },
        }

    @staticmethod
    def record_haskell_type_check(
        success: bool,
        error_count: int,
        execution_time_ms: float,
        errors: Optional[List[str]] = None,
    ) -> dict:
        """
        Create action to record a Haskell type check operation.

        Args:
            success: Whether the type check passed.
            error_count: Number of errors found.
            execution_time_ms: Time taken for the check.
            errors: List of error messages.
        """
        return {
            "type": "verification/record_haskell_type_check",
            "payload": {
                "success": success,
                "error_count": error_count,
                "execution_time_ms": execution_time_ms,
                "errors": errors or [],
            },
        }

    @staticmethod
    def record_lean_type_check(
        success: bool,
        error_count: int,
        execution_time_ms: float,
        errors: Optional[List[str]] = None,
    ) -> dict:
        """
        Create action to record a Lean type check operation.

        Args:
            success: Whether the type check passed.
            error_count: Number of errors found.
            execution_time_ms: Time taken for the check.
            errors: List of error messages.
        """
        return {
            "type": "verification/record_lean_type_check",
            "payload": {
                "success": success,
                "error_count": error_count,
                "execution_time_ms": execution_time_ms,
                "errors": errors or [],
            },
        }


def verification_reducer(state: VerificationState, action: dict) -> VerificationState:
    """
    Reducer function for verification state.

    Args:
        state: Current verification state.
        action: Action to apply to the state.

    Returns:
        New verification state.
    """
    action_type = action.get("type")

    if action_type == "verification/load_layer1_request":
        return VerificationState(
            layer1=Layer1State(status=VerificationStatus.LOADING),
            theorems=state.theorems,
            active_verification=state.active_verification,
            verification_queue=state.verification_queue,
        )

    elif action_type == "verification/load_layer1_success":
        payload = action.get("payload", {})
        return VerificationState(
            layer1=Layer1State(
                status=VerificationStatus.LOADED,
                mathlib_version=payload.get("mathlib_version"),
                physlib_version=payload.get("physlib_version"),
                load_time_ms=payload.get("load_time_ms"),
                memory_mb=payload.get("memory_mb"),
            ),
            theorems=state.theorems,
            active_verification=state.active_verification,
            verification_queue=state.verification_queue,
        )

    elif action_type == "verification/load_layer1_failure":
        return VerificationState(
            layer1=Layer1State(
                status=VerificationStatus.FAILED, error=action.get("payload")
            ),
            theorems=state.theorems,
            active_verification=state.active_verification,
            verification_queue=state.verification_queue,
        )

    elif action_type == "verification/verify_theorem_request":
        payload = action.get("payload", {})
        theorem_id = payload.get("theorem_id")
        new_theorems = state.theorems.copy()
        new_theorems[theorem_id] = TheoremVerification(
            theorem_id=theorem_id,
            status=VerificationStatus.PENDING,
            layer2_file=payload.get("layer2_file"),
        )
        new_queue = state.verification_queue.copy()
        if theorem_id not in new_queue:
            new_queue.append(theorem_id)
        return VerificationState(
            layer1=state.layer1,
            theorems=new_theorems,
            active_verification=theorem_id,
            verification_queue=new_queue,
        )

    elif action_type == "verification/verify_theorem_success":
        payload = action.get("payload", {})
        theorem_id = payload.get("theorem_id")
        new_theorems = state.theorems.copy()
        if theorem_id in new_theorems:
            new_theorems[theorem_id].status = VerificationStatus.PASSED
            new_theorems[theorem_id].proof = payload.get("proof")
        new_queue = state.verification_queue.copy()
        if theorem_id in new_queue:
            new_queue.remove(theorem_id)
        return VerificationState(
            layer1=state.layer1,
            theorems=new_theorems,
            active_verification=None,
            verification_queue=new_queue,
        )

    elif action_type == "verification/verify_theorem_failure":
        payload = action.get("payload", {})
        theorem_id = payload.get("theorem_id")
        new_theorems = state.theorems.copy()
        if theorem_id in new_theorems:
            new_theorems[theorem_id].status = VerificationStatus.FAILED_VERIFICATION
            new_theorems[theorem_id].last_error = payload.get("error")
            new_theorems[theorem_id].proof_attempts += 1
        new_queue = state.verification_queue.copy()
        if theorem_id in new_queue:
            new_queue.remove(theorem_id)
        return VerificationState(
            layer1=state.layer1,
            theorems=new_theorems,
            active_verification=None,
            verification_queue=new_queue,
            haskell_status=state.haskell_status,
            lean_status=state.lean_status,
            type_check_history=state.type_check_history,
        )

    elif action_type == "verification/update_haskell_checker_status":
        payload = action.get("payload", {})
        import time

        return VerificationState(
            layer1=state.layer1,
            theorems=state.theorems,
            active_verification=state.active_verification,
            verification_queue=state.verification_queue,
            haskell_status=TypeCheckerStatus(
                checker_type="haskell",
                availability=TypeCheckerAvailabilityStatus(
                    payload.get("availability", "unknown")
                ),
                version=payload.get("version"),
                last_check=time.time(),
                error=payload.get("error"),
            ),
            lean_status=state.lean_status,
            type_check_history=state.type_check_history,
        )

    elif action_type == "verification/update_lean_checker_status":
        payload = action.get("payload", {})
        import time

        return VerificationState(
            layer1=state.layer1,
            theorems=state.theorems,
            active_verification=state.active_verification,
            verification_queue=state.verification_queue,
            haskell_status=state.haskell_status,
            lean_status=TypeCheckerStatus(
                checker_type="lean",
                availability=TypeCheckerAvailabilityStatus(
                    payload.get("availability", "unknown")
                ),
                version=payload.get("version"),
                last_check=time.time(),
                error=payload.get("error"),
            ),
            type_check_history=state.type_check_history,
        )

    elif action_type == "verification/record_haskell_type_check":
        payload = action.get("payload", {})
        import time

        new_record = TypeCheckRecord(
            code_type="haskell",
            success=payload.get("success", False),
            error_count=payload.get("error_count", 0),
            execution_time_ms=payload.get("execution_time_ms", 0.0),
            timestamp=time.time(),
            errors=payload.get("errors", []),
        )
        # Keep last 100 records
        new_history = (state.type_check_history + [new_record])[-100:]
        return VerificationState(
            layer1=state.layer1,
            theorems=state.theorems,
            active_verification=state.active_verification,
            verification_queue=state.verification_queue,
            haskell_status=state.haskell_status,
            lean_status=state.lean_status,
            type_check_history=new_history,
        )

    elif action_type == "verification/record_lean_type_check":
        payload = action.get("payload", {})
        import time

        new_record = TypeCheckRecord(
            code_type="lean",
            success=payload.get("success", False),
            error_count=payload.get("error_count", 0),
            execution_time_ms=payload.get("execution_time_ms", 0.0),
            timestamp=time.time(),
            errors=payload.get("errors", []),
        )
        # Keep last 100 records
        new_history = (state.type_check_history + [new_record])[-100:]
        return VerificationState(
            layer1=state.layer1,
            theorems=state.theorems,
            active_verification=state.active_verification,
            verification_queue=state.verification_queue,
            haskell_status=state.haskell_status,
            lean_status=state.lean_status,
            type_check_history=new_history,
        )

    # Return unchanged state for unknown actions
    return state
