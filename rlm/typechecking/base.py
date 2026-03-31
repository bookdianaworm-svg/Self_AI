"""
Abstract TypeChecker base class for type checking systems.

This module provides the base interface for all type checkers (Haskell, Lean, etc.)
that can be used for verification in the RLM stack.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class CheckerStatus(Enum):
    """Status of a type checker."""

    UNKNOWN = "unknown"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


@dataclass
class TypeCheckerHealth:
    """Health status of a type checker."""

    status: CheckerStatus = CheckerStatus.UNKNOWN
    version: Optional[str] = None
    last_check: Optional[datetime] = None
    error: Optional[str] = None


class TypeChecker(ABC):
    """
    Abstract base class for type checkers.

    All type checkers (Haskell GHC, Lean Lake, etc.) must inherit from this class
    and implement the abstract methods.

    Attributes:
        name: Human-readable name of the checker
        version: Version string of the underlying tool
        timeout_seconds: Default timeout for type checking operations
    """

    def __init__(
        self,
        timeout_seconds: float = 30.0,
        ghc_path: Optional[str] = None,
        ghc_options: Optional[list[str]] = None,
    ):
        """
        Initialize the type checker.

        Args:
            timeout_seconds: Default timeout for type checking operations.
            ghc_path: Path to the GHC executable (for Haskell checker).
            ghc_options: Additional options to pass to GHC.
        """
        self.timeout_seconds = timeout_seconds
        self.ghc_path = ghc_path
        self.ghc_options = ghc_options or []
        self._health: TypeCheckerHealth = TypeCheckerHealth()

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the human-readable name of the checker."""
        pass

    @property
    @abstractmethod
    def checker_type(self) -> str:
        """Return the type of checker (e.g., 'haskell', 'lean')."""
        pass

    @property
    def health(self) -> TypeCheckerHealth:
        """Return the current health status of the checker."""
        return self._health

    @abstractmethod
    def check(self, code: str, timeout_seconds: Optional[float] = None) -> Any:
        """
        Check the given code for type errors.

        Args:
            code: The code to type check.
            timeout_seconds: Optional override of the default timeout.

        Returns:
            Any result type with `success` and `error_count` properties.
        """
        pass

    @abstractmethod
    def health_check(self) -> TypeCheckerHealth:
        """
        Perform a health check on the type checker.

        Returns:
            TypeCheckerHealth with current status.
        """
        pass

    def is_available(self) -> bool:
        """
        Check if the type checker is available and ready to use.

        Returns:
            True if the checker is available, False otherwise.
        """
        health = self.health_check()
        return health.status == CheckerStatus.AVAILABLE

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, timeout={self.timeout_seconds})"


# Result type imported from result module to avoid circular imports
from rlm.typechecking.result import TypeCheckerResult
