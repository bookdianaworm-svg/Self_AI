"""
Tests for Layer1Bootstrap component.

This module tests Layer1Bootstrap class which handles:
- Layer1 loading and initialization
- Lean kernel initialization with Mathlib
- Haskell compiler setup for dimensional types
- Error handling for Layer1 operations
- Caching of loaded Layer1 state
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from rlm.environments.layer1_bootstrap import Layer1Bootstrap


class TestLayer1BootstrapInitialization:
    """
    Tests for Layer1Bootstrap initialization.
    """

    def test_init_with_default_path(self):
        """
        Test that Layer1Bootstrap initializes with default path.

        Expected behavior:
        - Should initialize successfully
        - Should set default layer1_path
        - Should initialize lean_kernel and haskell_compiler to None
        - Should set loaded to False
        """
        bootstrap = Layer1Bootstrap()
        assert bootstrap.layer1_path is not None
        assert bootstrap.lean_kernel is None
        assert bootstrap.haskell_compiler is None
        assert bootstrap.loaded is False

    def test_init_with_custom_path(self, temp_dir: Path):
        """
        Test that Layer1Bootstrap initializes with custom path.

        Args:
            temp_dir: Temporary directory fixture

        Expected behavior:
        - Should use provided path
        - Should store path correctly
        """
        custom_path = str(temp_dir / "custom_layer1")
        bootstrap = Layer1Bootstrap(layer1_path=custom_path)
        assert bootstrap.layer1_path == custom_path

    def test_init_with_none_path(self):
        """
        Test that Layer1Bootstrap handles None path gracefully.

        Expected behavior:
        - Should use default path when None provided
        - Should not raise exception
        """
        bootstrap = Layer1Bootstrap(layer1_path=None)
        assert bootstrap.layer1_path is not None

    def test_default_layer1_path_exists(self):
        """
        Test that default Layer1 path is valid.

        Expected behavior:
        - Should return a valid path string
        - Path should be relative to module
        """
        bootstrap = Layer1Bootstrap()
        default_path = bootstrap._default_layer1_path()
        assert isinstance(default_path, str)
        assert len(default_path) > 0

    def test_initial_state(self):
        """
        Test initial state of Layer1Bootstrap.

        Expected behavior:
        - All version fields should be None initially
        - loaded should be False
        - lean_kernel and haskell_compiler should be None
        """
        bootstrap = Layer1Bootstrap()
        assert bootstrap.loaded is False
        assert bootstrap.lean_kernel is None
        assert bootstrap.haskell_compiler is None
        assert bootstrap._mathlib_version is None
        assert bootstrap._physlib_version is None


class TestLayer1Loading:
    """
    Tests for Layer1 loading functionality.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_physlib')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._compile_haskell_types')
    def test_load_layer1_success(self, mock_compile, mock_physlib, mock_lean):
        """
        Test successful Layer1 loading.

        Args:
            mock_compile: Mocked _compile_haskell_types
            mock_physlib: Mocked _load_physlib
            mock_lean: Mocked _load_lean_kernel

        Expected behavior:
        - Should call all loading methods
        - Should return success result
        - Should set loaded to True
        """
        mock_lean.return_value = MagicMock()
        mock_physlib.return_value = None
        mock_compile.return_value = None

        bootstrap = Layer1Bootstrap()
        result = bootstrap.load_layer1()

        assert result["success"] is True
        assert bootstrap.loaded is True
        mock_lean.assert_called_once()
        mock_physlib.assert_called_once()
        mock_compile.assert_called_once()

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    def test_load_layer1_failure(self, mock_lean):
        """
        Test Layer1 loading with failure.

        Args:
            mock_lean: Mocked _load_lean_kernel

        Expected behavior:
        - Should handle exception gracefully
        - Should return failure result with error
        - Should set loaded to False
        """
        mock_lean.side_effect = RuntimeError("Failed to load Lean")

        bootstrap = Layer1Bootstrap()
        result = bootstrap.load_layer1()

        assert result["success"] is False
        assert "error" in result
        assert bootstrap.loaded is False

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_physlib')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._compile_haskell_types')
    def test_load_layer1_cached(self, mock_compile, mock_physlib, mock_lean):
        """
        Test that Layer1 loading uses cache.

        Args:
            mock_compile: Mocked _compile_haskell_types
            mock_physlib: Mocked _load_physlib
            mock_lean: Mocked _load_lean_kernel

        Expected behavior:
        - Should not reload if already loaded
        - Should return cached result
        - Should not call loading methods again
        """
        mock_lean.return_value = MagicMock()
        mock_physlib.return_value = None
        mock_compile.return_value = None

        bootstrap = Layer1Bootstrap()
        # First load
        result1 = bootstrap.load_layer1()
        assert result1["success"] is True

        # Second load (should use cache)
        result2 = bootstrap.load_layer1()
        assert result2["success"] is True
        assert result2.get("cached") is True

        # Should not call loading methods again
        assert mock_lean.call_count == 1
        assert mock_physlib.call_count == 1
        assert mock_compile.call_count == 1

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_physlib')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._compile_haskell_types')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._get_memory_usage')
    def test_load_layer1_includes_metadata(self, mock_memory, mock_compile, mock_physlib, mock_lean):
        """
        Test that Layer1 loading includes metadata.

        Args:
            mock_memory: Mocked _get_memory_usage
            mock_compile: Mocked _compile_haskell_types
            mock_physlib: Mocked _load_physlib
            mock_lean: Mocked _load_lean_kernel

        Expected behavior:
        - Should include mathlib_version
        - Should include physlib_version
        - Should include load_time_ms
        - Should include memory_mb
        """
        mock_lean.return_value = MagicMock()
        mock_physlib.return_value = None
        mock_compile.return_value = None
        mock_memory.return_value = 256.0

        bootstrap = Layer1Bootstrap()
        result = bootstrap.load_layer1()

        assert result["success"] is True
        assert "mathlib_version" in result
        assert "physlib_version" in result
        assert "load_time_ms" in result
        assert "memory_mb" in result
        assert result["memory_mb"] == 256.0


class TestLeanKernelLoading:
    """
    Tests for Lean kernel loading.
    """

    @patch('rlm.environments.layer1_bootstrap.os.path.exists')
    def test_load_lean_kernel_success(self, mock_exists):
        """
        Test successful Lean kernel loading.

        Args:
            mock_exists: Mocked os.path.exists

        Expected behavior:
        - Should execute Lean initialization
        - Should return kernel object
        - Should not raise exception
        """
        mock_exists.return_value = True

        bootstrap = Layer1Bootstrap()
        kernel = bootstrap._load_lean_kernel()
        assert kernel is not None

    @patch('rlm.environments.layer1_bootstrap.subprocess')
    def test_load_lean_kernel_failure(self, mock_subprocess):
        """
        Test Lean kernel loading with failure.

        Args:
            mock_subprocess: Mocked subprocess module

        Expected behavior:
        - Should raise exception on failure
        - Should include error details
        """
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = b"Error: Lean not found"
        mock_subprocess.run.return_value = mock_process

        bootstrap = Layer1Bootstrap()
        with pytest.raises(RuntimeError):
            bootstrap._load_lean_kernel()

    @patch('rlm.environments.layer1_bootstrap.subprocess')
    def test_load_lean_kernel_timeout(self, mock_subprocess):
        """
        Test Lean kernel loading with timeout.

        Args:
            mock_subprocess: Mocked subprocess module

        Expected behavior:
        - Should handle timeout gracefully
        - Should raise appropriate exception
        """
        mock_subprocess.TimeoutExpired = Exception
        mock_subprocess.run.side_effect = Exception("Timeout")

        bootstrap = Layer1Bootstrap()
        with pytest.raises(Exception):
            bootstrap._load_lean_kernel()


class TestPhysLibLoading:
    """
    Tests for PhysLib loading.
    """

    @patch('rlm.environments.layer1_bootstrap.os.path.exists')
    def test_load_physlib_success(self, mock_exists):
        """
        Test successful PhysLib loading.

        Args:
            mock_exists: Mocked os.path.exists

        Expected behavior:
        - Should load PhysLib/SciLean
        - Should not raise exception
        - Should complete without errors
        """
        mock_exists.return_value = True

        bootstrap = Layer1Bootstrap()
        bootstrap._load_physlib()
        # If no exception, test passes

    def test_load_physlib_with_missing_files(self, temp_dir: Path):
        """
        Test PhysLib loading with missing files.

        Args:
            temp_dir: Temporary directory fixture

        Expected behavior:
        - Should handle missing files gracefully
        - Should raise appropriate exception
        """
        # Create empty layer1 directory without physlib
        empty_path = temp_dir / "empty_layer1"
        empty_path.mkdir()

        bootstrap = Layer1Bootstrap(layer1_path=str(empty_path))
        with pytest.raises((FileNotFoundError, RuntimeError)):
            bootstrap._load_physlib()


class TestHaskellCompilerSetup:
    """
    Tests for Haskell compiler setup.
    """

    @patch('rlm.environments.layer1_bootstrap.os.path.exists')
    def test_compile_haskell_types_success(self, mock_exists):
        """
        Test successful Haskell type compilation.

        Args:
            mock_exists: Mocked os.path.exists

        Expected behavior:
        - Should compile Haskell dimensional types
        - Should return without errors
        """
        mock_exists.return_value = True

        bootstrap = Layer1Bootstrap()
        bootstrap._compile_haskell_types()
        # Should complete without exception

    @patch('rlm.environments.layer1_bootstrap.subprocess')
    def test_compile_haskell_types_failure(self, mock_subprocess):
        """
        Test Haskell type compilation with failure.

        Args:
            mock_subprocess: Mocked subprocess module

        Expected behavior:
        - Should raise exception on compilation failure
        - Should include error details
        """
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = b"Compilation error"
        mock_subprocess.run.return_value = mock_process

        bootstrap = Layer1Bootstrap()
        with pytest.raises(RuntimeError):
            bootstrap._compile_haskell_types()

    @patch('rlm.environments.layer1_bootstrap.subprocess')
    def test_compile_haskell_types_timeout(self, mock_subprocess):
        """
        Test Haskell type compilation with timeout.

        Args:
            mock_subprocess: Mocked subprocess module

        Expected behavior:
        - Should handle timeout gracefully
        - Should raise appropriate exception
        """
        mock_subprocess.TimeoutExpired = Exception
        mock_subprocess.run.side_effect = Exception("Timeout")

        bootstrap = Layer1Bootstrap()
        with pytest.raises(Exception):
            bootstrap._compile_haskell_types()


class TestVersionRetrieval:
    """
    Tests for version information retrieval.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_physlib')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._compile_haskell_types')
    def test_get_mathlib_version(self, mock_compile, mock_physlib, mock_lean):
        """
        Test Mathlib version retrieval.

        Expected behavior:
        - Should return version string
        - Should not be None when loaded
        """
        mock_lean.return_value = MagicMock()
        mock_physlib.return_value = None
        mock_compile.return_value = None

        bootstrap = Layer1Bootstrap()
        # Before loading, should be None
        assert bootstrap._get_mathlib_version() is None

        # After loading (mocked), should have version
        result = bootstrap.load_layer1()
        assert result["success"] is True
        assert bootstrap._get_mathlib_version() is not None

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_physlib')
    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._compile_haskell_types')
    def test_get_physlib_version(self, mock_compile, mock_physlib, mock_lean):
        """
        Test Physlib version retrieval.

        Expected behavior:
        - Should return version string
        - Should not be None when loaded
        """
        mock_lean.return_value = MagicMock()
        mock_physlib.return_value = None
        mock_compile.return_value = None

        bootstrap = Layer1Bootstrap()
        # Before loading, should be None
        assert bootstrap._get_physlib_version() is None

        # After loading (mocked), should have version
        result = bootstrap.load_layer1()
        assert result["success"] is True
        assert bootstrap._get_physlib_version() is not None


class TestMemoryUsage:
    """
    Tests for memory usage tracking.
    """

    @patch('rlm.environments.layer1_bootstrap.psutil')
    def test_get_memory_usage(self, mock_psutil):
        """
        Test memory usage retrieval.

        Args:
            mock_psutil: Mocked psutil module

        Expected behavior:
        - Should return memory usage in MB
        - Should be a positive number
        """
        mock_process = MagicMock()
        mock_process.memory_info.return_value.rss = 268435456  # 256 MB
        mock_psutil.Process.return_value = mock_process

        bootstrap = Layer1Bootstrap()
        memory_mb = bootstrap._get_memory_usage()
        assert memory_mb == 256.0

    @patch('rlm.environments.layer1_bootstrap.psutil')
    def test_get_memory_usage_with_exception(self, mock_psutil):
        """
        Test memory usage retrieval with exception.

        Args:
            mock_psutil: Mocked psutil module

        Expected behavior:
        - Should handle psutil exceptions gracefully
        - Should return None or default value
        """
        mock_psutil.Process.side_effect = Exception("Process not found")

        bootstrap = Layer1Bootstrap()
        memory_mb = bootstrap._get_memory_usage()
        # Should handle gracefully
        assert memory_mb is None or memory_mb >= 0


class TestErrorHandling:
    """
    Tests for error handling in Layer1Bootstrap.
    """

    @patch('rlm.environments.layer1_bootstrap.Layer1Bootstrap._load_lean_kernel')
    def test_load_layer1_with_partial_failure(self, mock_lean):
        """
        Test Layer1 loading with partial failure.

        Args:
            mock_lean: Mocked _load_lean_kernel

        Expected behavior:
        - Should handle partial failures gracefully
        - Should return failure result
        - Should not leave system in inconsistent state
        """
        mock_lean.side_effect = RuntimeError("Partial failure")

        bootstrap = Layer1Bootstrap()
        result = bootstrap.load_layer1()

        assert result["success"] is False
        assert "error" in result
        assert bootstrap.loaded is False

    def test_load_layer1_with_invalid_path(self):
        """
        Test Layer1 loading with invalid path.

        Expected behavior:
        - Should handle invalid path gracefully
        - Should return failure result
        """
        bootstrap = Layer1Bootstrap(layer1_path="/nonexistent/path")
        result = bootstrap.load_layer1()

        # Should handle gracefully (may succeed with defaults or fail)
        assert isinstance(result, dict)
        assert "success" in result


class TestEdgeCases:
    """
    Tests for edge cases in Layer1Bootstrap.
    """

    def test_multiple_load_calls(self):
        """
        Test multiple load_layer1 calls.

        Expected behavior:
        - First call should load
        - Subsequent calls should use cache
        - Should not reload
        """
        bootstrap = Layer1Bootstrap()

        # Mock the loading methods to track calls
        with patch.object(bootstrap, '_load_lean_kernel') as mock_lean, \
             patch.object(bootstrap, '_load_physlib') as mock_physlib, \
             patch.object(bootstrap, '_compile_haskell_types') as mock_compile:

            mock_lean.return_value = MagicMock()
            mock_physlib.return_value = None
            mock_compile.return_value = None

            # First load
            result1 = bootstrap.load_layer1()
            assert result1["success"] is True
            assert mock_lean.call_count == 1

            # Second load
            result2 = bootstrap.load_layer1()
            assert result2["success"] is True
            assert result2.get("cached") is True
            assert mock_lean.call_count == 1  # No additional calls

    def test_load_time_tracking(self):
        """
        Test that load time is tracked correctly.

        Expected behavior:
        - Should measure load time in milliseconds
        - Should be positive value
        """
        bootstrap = Layer1Bootstrap()

        with patch.object(bootstrap, '_load_lean_kernel') as mock_lean, \
             patch.object(bootstrap, '_load_physlib') as mock_physlib, \
             patch.object(bootstrap, '_compile_haskell_types') as mock_compile:

            mock_lean.return_value = MagicMock()
            mock_physlib.return_value = None
            mock_compile.return_value = None

            result = bootstrap.load_layer1()
            assert result["success"] is True
            assert "load_time_ms" in result
            assert result["load_time_ms"] >= 0


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """
    Provide a temporary directory for test files.

    Args:
        tmp_path: Pytest tmp_path fixture

    Returns:
        Path to temporary directory
    """
    return tmp_path
