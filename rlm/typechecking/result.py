"""
Result types for type checking operations.

This module provides data classes for representing type checking results,
including success/failure status and detailed error information.
"""

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Sequence


@dataclass
class TypeErrorInfo:
    """
    Represents a single type error.

    Attributes:
        line: Line number where the error occurred (1-indexed).
        column: Column number where the error started (1-indexed).
        end_column: Column number where the error ended.
        message: Human-readable error message.
        severity: Error severity (error, warning, info).
        code: Error code (e.g., 'HC002' for Haskell type errors).
    """

    line: int
    column: int
    end_column: Optional[int] = None
    message: str = ""
    severity: str = "error"
    code: str = ""

    def __str__(self) -> str:
        if self.end_column:
            return f"Line {self.line}, Col {self.column}-{self.end_column}: [{self.code}] {self.message}"
        return f"Line {self.line}, Col {self.column}: [{self.code}] {self.message}"


class TypeCheckResultBase(ABC):
    """Abstract base class for type checking results."""

    @property
    def success(self) -> bool:
        raise NotImplementedError

    @property
    def error_count(self) -> int:
        raise NotImplementedError


@dataclass
class TypeCheckSuccess(TypeCheckResultBase):
    """
    Result of a successful type check operation.

    Attributes:
        checker: Name of the checker that produced this result.
        code: The code that was checked.
        checked_at: Timestamp when the check was performed.
        execution_time_ms: Time taken to perform the check.
        output: Optional output from the checker (e.g., warnings).
        metadata: Additional metadata about the check.
    """

    checker: str
    code: str
    checked_at: datetime = field(default_factory=datetime.now)
    execution_time_ms: float = 0.0
    output: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return True

    @property
    def error_count(self) -> int:
        return 0

    def __str__(self) -> str:
        return f"TypeCheckSuccess({self.checker}, {self.execution_time_ms:.2f}ms)"


@dataclass
class TypeCheckFailure(TypeCheckResultBase):
    """
    Result of a failed type check operation.

    Attributes:
        checker: Name of the checker that produced this result.
        code: The code that was checked.
        errors: List of TypeErrorInfo objects describing the errors.
        checked_at: Timestamp when the check was performed.
        execution_time_ms: Time taken to perform the check.
        stdout: Standard output from the checker.
        stderr: Standard error from the checker.
        metadata: Additional metadata about the check.
    """

    checker: str
    code: str
    errors: Sequence[TypeErrorInfo] = field(default_factory=list)
    checked_at: datetime = field(default_factory=datetime.now)
    execution_time_ms: float = 0.0
    stdout: str = ""
    stderr: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return False

    @property
    def error_count(self) -> int:
        return len(self.errors)

    def __str__(self) -> str:
        return f"TypeCheckFailure({self.checker}, {self.error_count} errors)"


# Type alias for results
TypeCheckerResult = TypeCheckSuccess | TypeCheckFailure


def create_success_result(
    checker: str,
    code: str,
    execution_time_ms: float = 0.0,
    output: str = "",
    metadata: Optional[dict[str, Any]] = None,
) -> TypeCheckSuccess:
    """
    Factory function to create a successful type check result.

    Args:
        checker: Name of the checker.
        code: The code that was checked.
        execution_time_ms: Time taken in milliseconds.
        output: Optional output from the checker.
        metadata: Optional metadata dictionary.

    Returns:
        TypeCheckSuccess result.
    """
    return TypeCheckSuccess(
        checker=checker,
        code=code,
        execution_time_ms=execution_time_ms,
        output=output,
        metadata=metadata or {},
    )


def create_failure_result(
    checker: str,
    code: str,
    errors: list[TypeErrorInfo],
    execution_time_ms: float = 0.0,
    stdout: str = "",
    stderr: str = "",
    metadata: Optional[dict[str, Any]] = None,
) -> TypeCheckFailure:
    """
    Factory function to create a failed type check result.

    Args:
        checker: Name of the checker.
        code: The code that was checked.
        errors: List of TypeErrorInfo objects.
        execution_time_ms: Time taken in milliseconds.
        stdout: Standard output from the checker.
        stderr: Standard error from the checker.
        metadata: Optional metadata dictionary.

    Returns:
        TypeCheckFailure result.
    """
    return TypeCheckFailure(
        checker=checker,
        code=code,
        errors=errors,
        execution_time_ms=execution_time_ms,
        stdout=stdout,
        stderr=stderr,
        metadata=metadata or {},
    )
