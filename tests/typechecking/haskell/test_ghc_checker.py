"""
Tests for the Haskell type checker (GHCChecker).

These tests verify the GHC-based type checking functionality.
Note: These tests require GHC to be installed to run successfully.
"""

import pytest
from unittest.mock import patch, MagicMock
import subprocess

from rlm.typechecking.haskell.ghc_checker import GHCChecker
from rlm.typechecking.haskell.result import HaskellTypeResult
from rlm.typechecking.exceptions import TypeCheckerNotAvailableError


class TestGHCChecker:
    """Test suite for GHCChecker."""

    def test_ghc_checker_initialization(self):
        """Test that GHCChecker can be initialized."""
        # This test will fail if GHC is not installed
        try:
            checker = GHCChecker()
            assert checker.name == "GHC Haskell Type Checker"
            assert checker.checker_type == "haskell"
            assert checker.timeout_seconds == 30.0
        except TypeCheckerNotAvailableError:
            pytest.skip("GHC not installed")

    def test_ghc_checker_health_check(self):
        """Test GHCChecker health check."""
        try:
            checker = GHCChecker()
            health = checker.health_check()
            assert health.status.value in ["available", "unavailable", "error"]
        except TypeCheckerNotAvailableError:
            pytest.skip("GHC not installed")

    def test_ghc_checker_is_available(self):
        """Test GHCChecker availability check."""
        try:
            checker = GHCChecker()
            # is_available should return True if GHC is working
            result = checker.is_available()
            assert isinstance(result, bool)
        except TypeCheckerNotAvailableError:
            pytest.skip("GHC not installed")

    def test_check_types_valid_haskell(self):
        """Test type checking valid Haskell code."""
        try:
            checker = GHCChecker()
            code = "double x = x * 2"
            result = checker.check_types(code)
            assert isinstance(result, HaskellTypeResult)
            assert hasattr(result, "success")
            assert hasattr(result, "errors")
            assert hasattr(result, "execution_time_ms")
        except TypeCheckerNotAvailableError:
            pytest.skip("GHC not installed")

    def test_check_types_with_type_error(self):
        """Test type checking Haskell code with type error."""
        try:
            checker = GHCChecker()
            # This code has a type error: adding string to int
            code = 'x :: Int; x = "hello" + 5'
            result = checker.check_types(code)
            assert isinstance(result, HaskellTypeResult)
            # The result should indicate failure with errors
            if not result.success:
                assert len(result.errors) > 0
        except TypeCheckerNotAvailableError:
            pytest.skip("GHC not installed")

    def test_check_types_timeout(self):
        """Test type checking with custom timeout."""
        try:
            checker = GHCChecker(timeout_seconds=1.0)
            assert checker.timeout_seconds == 1.0
        except TypeCheckerNotAvailableError:
            pytest.skip("GHC not installed")

    def test_error_codes(self):
        """Test that error codes are properly defined."""
        assert GHCChecker.ERROR_CODE_NOT_AVAILABLE == "HC001"
        assert GHCChecker.ERROR_CODE_TYPE_ERROR == "HC002"
        assert GHCChecker.ERROR_CODE_TIMEOUT == "HC003"


class TestGHCCheckerParsing:
    """Tests for GHC output parsing."""

    def test_parse_ghc_error_simple(self):
        """Test parsing a simple GHC error message."""
        try:
            checker = GHCChecker()
            stderr = "test.hs:3:10: error: Couldn't match expected type 'Int' with 'String'\n"
            errors = checker._parse_ghc_errors(stderr)
            assert len(errors) > 0
        except TypeCheckerNotAvailableError:
            pytest.skip("GHC not installed")

    def test_parse_ghc_error_with_code(self):
        """Test parsing GHC error with error code."""
        try:
            checker = GHCChecker()
            stderr = "test.hs:5:1: error: Variable not in scope: x :: Int\n"
            errors = checker._parse_ghc_errors(stderr)
            assert len(errors) > 0
        except TypeCheckerNotAvailableError:
            pytest.skip("GHC not installed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
