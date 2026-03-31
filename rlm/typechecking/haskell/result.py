"""
Haskell-specific type checking result types.

This module provides data classes for representing Haskell type checking results.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Sequence

from rlm.typechecking.result import TypeCheckSuccess, TypeCheckFailure, TypeErrorInfo


@dataclass
class HaskellTypeResult:
    """
    Result of a Haskell type checking operation.

    Attributes:
        success: Whether type checking passed.
        code: The code that was checked.
        errors: List of type errors found.
        checked_at: Timestamp of the check.
        execution_time_ms: Time taken to perform the check.
        stdout: Standard output from GHC.
        stderr: Standard error from GHC.
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
            return f"HaskellTypeResult: OK ({self.execution_time_ms:.2f}ms)"
        return f"HaskellTypeResult: {self.error_count} errors ({self.execution_time_ms:.2f}ms)"

    def to_base_result(self) -> TypeCheckSuccess | TypeCheckFailure:
        """Convert to base TypeCheckerResult type."""
        if self.success:
            return TypeCheckSuccess(
                checker="haskell",
                code=self.code,
                checked_at=self.checked_at,
                execution_time_ms=self.execution_time_ms,
                output=self.stdout,
                metadata=self.metadata,
            )
        return TypeCheckFailure(
            checker="haskell",
            code=self.code,
            errors=list(self.errors),
            checked_at=self.checked_at,
            execution_time_ms=self.execution_time_ms,
            stdout=self.stdout,
            stderr=self.stderr,
            metadata=self.metadata,
        )


@dataclass
class HaskellErrorInfo(TypeErrorInfo):
    """
    Haskell-specific type error information.

    Additional attributes:
        suggested_fix: Optional suggested fix for the error.
    """

    suggested_fix: Optional[str] = None
    ghc_code: Optional[str] = (
        None  # GHC's error code (e.g., "Couldn't match expected type")
    )

    def __str__(self) -> str:
        base = super().__str__()
        if self.suggested_fix:
            base += f"\n  Suggestion: {self.suggested_fix}"
        return base
