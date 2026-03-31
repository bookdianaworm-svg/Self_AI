"""
Integration tests for the type checking system.

These tests verify that the type checking system works correctly
with the rest of the RLM stack.
"""

import pytest
from unittest.mock import patch, MagicMock

from rlm.typechecking import (
    TypeCheckerRegistry,
    TypeCheckerConfig,
    HaskellConfig,
    LeanConfig,
)
from rlm.typechecking.result import TypeCheckSuccess, TypeCheckFailure, TypeErrorInfo
from rlm.typechecking.exceptions import TypeCheckerError


class TestTypeCheckerRegistry:
    """Test suite for TypeCheckerRegistry."""

    def test_registry_initialization(self):
        """Test registry initialization with empty config."""
        config = TypeCheckerConfig()
        registry = TypeCheckerRegistry(config)
        assert registry.config == config
        assert not registry.is_initialized

    def test_registry_initialize_with_haskell_disabled(self):
        """Test registry initialization with Haskell disabled."""
        config = TypeCheckerConfig(haskell=HaskellConfig(enabled=False))
        registry = TypeCheckerRegistry(config)
        registry.initialize()
        assert registry.get_checker_or_none("haskell") is None

    def test_registry_initialize_with_lean_disabled(self):
        """Test registry initialization with Lean disabled."""
        config = TypeCheckerConfig(lean=LeanConfig(enabled=False))
        registry = TypeCheckerRegistry(config)
        registry.initialize()
        assert registry.get_checker_or_none("lean") is None

    def test_registry_register_checker(self):
        """Test manual checker registration."""
        from rlm.typechecking.base import TypeChecker

        registry = TypeCheckerRegistry()
        mock_checker = MagicMock(spec=TypeChecker)
        mock_checker.name = "Mock Checker"
        mock_checker.checker_type = "mock"
        mock_checker.is_available.return_value = True

        registry.register_checker("mock", mock_checker)
        assert registry.get_checker("mock") == mock_checker

    def test_registry_unregister_checker(self):
        """Test checker unregistration."""
        from rlm.typechecking.base import TypeChecker

        registry = TypeCheckerRegistry()
        mock_checker = MagicMock(spec=TypeChecker)
        mock_checker.name = "Mock Checker"
        mock_checker.checker_type = "mock"
        mock_checker.is_available.return_value = True

        registry.register_checker("mock", mock_checker)
        assert registry.unregister_checker("mock") is True
        assert registry.get_checker_or_none("mock") is None

    def test_registry_list_checkers(self):
        """Test listing registered checkers."""
        from rlm.typechecking.base import TypeChecker

        registry = TypeCheckerRegistry()
        mock_checker1 = MagicMock(spec=TypeChecker)
        mock_checker1.name = "Mock 1"
        mock_checker1.checker_type = "mock1"
        mock_checker1.is_available.return_value = True

        mock_checker2 = MagicMock(spec=TypeChecker)
        mock_checker2.name = "Mock 2"
        mock_checker2.checker_type = "mock2"
        mock_checker2.is_available.return_value = True

        registry.register_checker("mock1", mock_checker1)
        registry.register_checker("mock2", mock_checker2)

        checkers = registry.list_checkers()
        assert "mock1" in checkers
        assert "mock2" in checkers

    def test_registry_get_checker_or_none(self):
        """Test getting checker that doesn't exist."""
        registry = TypeCheckerRegistry()
        assert registry.get_checker_or_none("nonexistent") is None

    def test_registry_is_checker_available(self):
        """Test availability check for registered checkers."""
        from rlm.typechecking.base import TypeChecker

        registry = TypeCheckerRegistry()
        mock_checker = MagicMock(spec=TypeChecker)
        mock_checker.name = "Mock"
        mock_checker.checker_type = "mock"
        mock_checker.is_available.return_value = True

        registry.register_checker("mock", mock_checker)
        assert registry.is_checker_available("mock") is True

    def test_registry_get_unavailable_checkers(self):
        """Test getting available checkers."""
        from rlm.typechecking.base import TypeChecker

        registry = TypeCheckerRegistry()
        mock_checker1 = MagicMock(spec=TypeChecker)
        mock_checker1.name = "Mock 1"
        mock_checker1.checker_type = "mock1"
        mock_checker1.is_available.return_value = True

        mock_checker2 = MagicMock(spec=TypeChecker)
        mock_checker2.name = "Mock 2"
        mock_checker2.checker_type = "mock2"
        mock_checker2.is_available.return_value = False

        registry.register_checker("mock1", mock_checker1)
        registry.register_checker("mock2", mock_checker2)

        available = registry.get_available_checkers()
        assert "mock1" in available
        assert "mock2" not in available


class TestTypeCheckerConfig:
    """Test suite for TypeCheckerConfig."""

    def test_config_defaults(self):
        """Test configuration defaults."""
        config = TypeCheckerConfig()
        assert config.version == "0.1"
        assert config.fail_on_error is True
        assert config.cache_results is True
        assert config.cache_dir == ".type_check_cache"

    def test_config_to_dict(self):
        """Test configuration serialization."""
        config = TypeCheckerConfig()
        data = config.to_dict()
        assert isinstance(data, dict)
        assert "version" in data
        assert "haskell" in data
        assert "lean" in data


class TestResultTypes:
    """Test suite for result types."""

    def test_type_error_info_str(self):
        """Test TypeErrorInfo string representation."""
        error = TypeErrorInfo(line=10, column=5, message="Type mismatch")
        assert "10" in str(error)
        assert "5" in str(error)
        assert "Type mismatch" in str(error)

    def test_type_check_success(self):
        """Test TypeCheckSuccess creation."""
        result = TypeCheckSuccess(checker="test", code="x = 1", execution_time_ms=100.0)
        assert result.success is True
        assert result.checker == "test"
        assert result.execution_time_ms == 100.0

    def test_type_check_failure(self):
        """Test TypeCheckFailure creation."""
        errors = [
            TypeErrorInfo(line=1, column=1, message="Error 1"),
            TypeErrorInfo(line=2, column=2, message="Error 2"),
        ]
        result = TypeCheckFailure(checker="test", code="x = 'hello'", errors=errors)
        assert result.success is False
        assert result.error_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
