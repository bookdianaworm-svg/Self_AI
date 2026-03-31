"""
Type Checking System for RLM verification stack.

This module provides formal type verification for Haskell and Lean 4 code,
enabling compile-time unit/dimension checking (Haskell) and theorem
verification against Layer 1 axioms (Lean).

Modules:
    base: Abstract TypeChecker base class
    result: Result types (TypeCheckResult, TypeError)
    exceptions: Custom exceptions
    config: Type checker configuration
    registry: Type checker registry
    haskell: Haskell type checking via GHC
    lean: Lean verification via Lake

Example:
    >>> from rlm.typechecking import TypeCheckerRegistry
    >>> registry = TypeCheckerRegistry()
    >>> registry.initialize()
    >>> haskell_checker = registry.get_checker("haskell")
    >>> result = haskell_checker.check("x :: Int; x = 42")
    >>> result.success
    True
"""

from rlm.typechecking.base import TypeChecker, TypeCheckerResult
from rlm.typechecking.result import TypeCheckSuccess, TypeCheckFailure, TypeErrorInfo
from rlm.typechecking.exceptions import (
    TypeCheckerError,
    TypeCheckerNotAvailableError,
    TypeCheckTimeoutError,
    TypeCheckExecutionError,
)
from rlm.typechecking.config import TypeCheckerConfig, HaskellConfig, LeanConfig
from rlm.typechecking.registry import TypeCheckerRegistry

__all__ = [
    # Base classes
    "TypeChecker",
    "TypeCheckerResult",
    # Result types
    "TypeCheckSuccess",
    "TypeCheckFailure",
    "TypeErrorInfo",
    # Exceptions
    "TypeCheckerError",
    "TypeCheckerNotAvailableError",
    "TypeCheckTimeoutError",
    "TypeCheckExecutionError",
    # Config
    "TypeCheckerConfig",
    "HaskellConfig",
    "LeanConfig",
    # Registry
    "TypeCheckerRegistry",
]

__version__ = "1.0.0"
