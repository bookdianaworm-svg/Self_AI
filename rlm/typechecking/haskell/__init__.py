"""
Haskell Type Checking Module.

This module provides Haskell type checking via GHC.
"""

from rlm.typechecking.haskell.haskell_checker import HaskellChecker
from rlm.typechecking.haskell.ghc_checker import GHCChecker
from rlm.typechecking.haskell.result import HaskellTypeResult

__all__ = [
    "HaskellChecker",
    "GHCChecker",
    "HaskellTypeResult",
]
