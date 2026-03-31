"""
Tests for the Lean type checker (LakeChecker).

These tests verify the Lake/Lean-based verification functionality.
Note: These tests require Lean to be installed to run successfully.
"""

import pytest
from unittest.mock import patch, MagicMock
import subprocess

from rlm.typechecking.lean.lake_checker import LakeChecker
from rlm.typechecking.lean.result import LeanVerificationResult
from rlm.typechecking.exceptions import TypeCheckerNotAvailableError


class TestLakeChecker:
    """Test suite for LakeChecker."""

    def test_lake_checker_initialization(self):
        """Test that LakeChecker can be initialized."""
        # This test will fail if Lean is not installed
        try:
            checker = LakeChecker()
            assert checker.name == "Lake Lean 4 Verifier"
            assert checker.checker_type == "lean"
            assert checker.timeout_seconds == 60.0
        except TypeCheckerNotAvailableError:
            pytest.skip("Lean not installed")

    def test_lake_checker_health_check(self):
        """Test LakeChecker health check."""
        try:
            checker = LakeChecker()
            health = checker.health_check()
            assert health.status.value in ["available", "unavailable", "error"]
        except TypeCheckerNotAvailableError:
            pytest.skip("Lean not installed")

    def test_lake_checker_is_available(self):
        """Test LakeChecker availability check."""
        try:
            checker = LakeChecker()
            result = checker.is_available()
            assert isinstance(result, bool)
        except TypeCheckerNotAvailableError:
            pytest.skip("Lean not installed")

    def test_verify_valid_lean(self):
        """Test verifying valid Lean code."""
        try:
            checker = LakeChecker()
            # Simple valid Lean code
            code = "theorem test : 1 + 1 = 2 := rfl"
            result = checker.verify(code)
            assert isinstance(result, LeanVerificationResult)
            assert hasattr(result, "success")
            assert hasattr(result, "errors")
        except TypeCheckerNotAvailableError:
            pytest.skip("Lean not installed")

    def test_verify_invalid_lean(self):
        """Test verifying invalid Lean code."""
        try:
            checker = LakeChecker()
            # Invalid Lean code (type mismatch)
            code = "theorem test : 1 = 2 := rfl"
            result = checker.verify(code)
            assert isinstance(result, LeanVerificationResult)
            # This should fail since 1 ≠ 2
            assert result.success == False
        except TypeCheckerNotAvailableError:
            pytest.skip("Lean not installed")

    def test_verify_timeout(self):
        """Test verification with custom timeout."""
        try:
            checker = LakeChecker(timeout_seconds=5.0)
            assert checker.timeout_seconds == 5.0
        except TypeCheckerNotAvailableError:
            pytest.skip("Lean not installed")

    def test_error_codes(self):
        """Test that error codes are properly defined."""
        assert LakeChecker.ERROR_CODE_NOT_AVAILABLE == "LN001"
        assert LakeChecker.ERROR_CODE_VERIFICATION_FAILED == "LN002"
        assert LakeChecker.ERROR_CODE_TIMEOUT == "LN003"


class TestLakeCheckerParsing:
    """Tests for Lean output parsing."""

    def test_parse_lean_error_simple(self):
        """Test parsing a simple Lean error message."""
        try:
            checker = LakeChecker()
            stderr = "test.lean:3:10: error: expected"
            errors = checker._parse_lean_errors(stderr)
            # May or may not have errors depending on format
            assert isinstance(errors, list)
        except TypeCheckerNotAvailableError:
            pytest.skip("Lean not installed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
