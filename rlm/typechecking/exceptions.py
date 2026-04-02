"""
Custom exceptions for the type checking system.

This module provides exception classes for handling errors that can occur
during type checking operations.
"""

from typing import Optional


class TypeCheckerError(Exception):
    """Base exception for type checking errors."""

    pass


class TypeCheckerNotAvailableError(TypeCheckerError):
    """
    Raised when a type checker is not available.

    This can occur when:
    - The required tool (GHC, Lake) is not installed
    - The executable path is incorrect
    - The tool fails to initialize
    """

    def __init__(self, checker: str, message: Optional[str] = None):
        self.checker = checker
        self.message = message or f"{checker} type checker is not available"
        super().__init__(self.message)


class TypeCheckTimeoutError(TypeCheckerError):
    """
    Raised when a type checking operation times out.

    Attributes:
        timeout_seconds: The timeout value that was exceeded.
        code: The code that was being checked when the timeout occurred.
    """

    def __init__(
        self, timeout_seconds: float, code: str = "", message: Optional[str] = None
    ):
        self.timeout_seconds = timeout_seconds
        self.code = code
        self.message = (
            message or f"Type checking timed out after {timeout_seconds} seconds"
        )
        super().__init__(self.message)


class TypeCheckExecutionError(TypeCheckerError):
    """
    Raised when a type checking operation fails to execute.

    This can occur when:
    - The subprocess fails to start
    - The subprocess is killed
    - An unexpected error occurs during execution
    """

    def __init__(
        self,
        checker: str,
        message: str,
        stderr: str = "",
        return_code: Optional[int] = None,
    ):
        self.checker = checker
        self.message = message
        self.stderr = stderr
        self.return_code = return_code
        super().__init__(self.message)


class TypeCheckConfigurationError(TypeCheckerError):
    """
    Raised when there is a configuration error for a type checker.

    This can occur when:
    - Required configuration options are missing
    - Configuration values are invalid
    - Configuration file cannot be parsed
    """

    pass
