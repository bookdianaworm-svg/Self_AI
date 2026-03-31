"""
Abstract interface for Haskell type checkers.

This module defines the abstract base class for Haskell type checking
implementations.
"""

from abc import abstractmethod
from typing import Any, Optional

from rlm.typechecking.base import TypeChecker


class HaskellChecker(TypeChecker):
    """
    Abstract base class for Haskell type checkers.

    All Haskell type checkers must inherit from this class
    and implement the type checking logic.
    """

    @property
    def checker_type(self) -> str:
        return "haskell"

    @abstractmethod
    def check_types(self, code: str, timeout_seconds: Optional[float] = None) -> Any:
        """
        Check the given Haskell code for type errors.

        Args:
            code: Haskell code to type check.
            timeout_seconds: Optional timeout override.

        Returns:
            Any result type with `success` and `error_count` properties.
        """
        pass

    def check(self, code: str, timeout_seconds: Optional[float] = None) -> Any:
        """
        Alias for check_types to satisfy TypeChecker interface.

        Args:
            code: Haskell code to type check.
            timeout_seconds: Optional timeout override.

        Returns:
            Any result type with `success` and `error_count` properties.
        """
        return self.check_types(code, timeout_seconds)
