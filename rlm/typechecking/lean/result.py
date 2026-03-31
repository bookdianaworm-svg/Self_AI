"""
Lean-specific verification result types.

This module provides data classes for representing Lean verification results.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Sequence

from rlm.typechecking.result import TypeCheckSuccess, TypeCheckFailure, TypeErrorInfo


@dataclass
class LeanVerificationResult:
    """
    Result of a Lean verification operation.

    Attributes:
        success: Whether verification passed.
        code: The code that was verified.
        errors: List of verification errors found.
        checked_at: Timestamp of the verification.
        execution_time_ms: Time taken to perform the verification.
        stdout: Standard output from Lake.
        stderr: Standard error from Lake.
        metadata: Additional metadata.
    """

    success: bool
    code: str
    errors: Sequence[TypeErrorInfo] = field(default_factory=list)
    checked_at: datetime = field(default_factory=datetime.now)
    execution_time_ms: float = 0.0
    stdout: str = ""
    stderr: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def error_count(self) -> int:
        """Return the number of errors found."""
        return len(self.errors)

    def get_errors_by_severity(self, severity: str) -> list[TypeErrorInfo]:
        """Get errors filtered by severity (error, warning, info)."""
        return [e for e in self.errors if e.severity == severity]

    def __str__(self) -> str:
        if self.success:
            return f"LeanVerificationResult: OK ({self.execution_time_ms:.2f}ms)"
        return f"LeanVerificationResult: {self.error_count} errors ({self.execution_time_ms:.2f}ms)"

    def to_base_result(self) -> TypeCheckSuccess | TypeCheckFailure:
        """Convert to base TypeCheckerResult type."""
        if self.success:
            return TypeCheckSuccess(
                checker="lean",
                code=self.code,
                checked_at=self.checked_at,
                execution_time_ms=self.execution_time_ms,
                output=self.stdout,
                metadata=self.metadata,
            )
        return TypeCheckFailure(
            checker="lean",
            code=self.code,
            errors=list(self.errors),
            checked_at=self.checked_at,
            execution_time_ms=self.execution_time_ms,
            stdout=self.stdout,
            stderr=self.stderr,
            metadata=self.metadata,
        )


@dataclass
class LeanErrorInfo(TypeErrorInfo):
    """
    Lean-specific verification error information.

    Additional attributes:
        tactic_state: Optional tactic state at time of error.
        stack_trace: Optional stack trace for debugging.
    """

    tactic_state: Optional[str] = None
    stack_trace: Optional[str] = None
    lean_code: Optional[str] = None  # Error code from Lean (e.g., "type mismatch")

    def __str__(self) -> str:
        base = super().__str__()
        if self.tactic_state:
            base += f"\n  Tactic state: {self.tactic_state}"
        return base
