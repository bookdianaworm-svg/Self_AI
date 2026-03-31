"""
Abstract interface for Lean type checkers.

This module defines the abstract base class for Lean verification
implementations.
"""

from abc import abstractmethod
from typing import Any, Optional

from rlm.typechecking.base import TypeChecker


class LeanChecker(TypeChecker):
    """
    Abstract base class for Lean type checkers.

    All Lean type checkers must inherit from this class
    and implement the verification logic.
    """

    @property
    def checker_type(self) -> str:
        return "lean"

    @abstractmethod
    def verify(self, code: str, timeout_seconds: Optional[float] = None) -> Any:
        """
        Verify Lean code against Layer 1 axioms.

        Args:
            code: Lean code to verify.
            timeout_seconds: Optional timeout override.

        Returns:
            Any result type with `success` and `error_count` properties.
        """
        pass

    def check(self, code: str, timeout_seconds: Optional[float] = None) -> Any:
        """
        Alias for verify to satisfy TypeChecker interface.

        Args:
            code: Lean code to verify.
            timeout_seconds: Optional timeout override.

        Returns:
            Any result type with `success` and `error_count` properties.
        """
        return self.verify(code, timeout_seconds)
