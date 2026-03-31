"""
Pytest configuration and shared fixtures for the test suite.

This module provides common fixtures and configuration used across
all test modules in the test suite.
"""

import os
import tempfile
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

from rlm.routing.backend_router import BackendRouter, TaskDescriptor
from rlm.routing.backend_factory import BackendFactory
from rlm.routing.environment_router import EnvironmentRouter
from rlm.routing.environment_factory import EnvironmentFactory
from rlm.routing.task_descriptor import default_task_descriptor_fn
from rlm.redux.slices.routing_slice import RoutingState, BackendMetrics
from rlm.redux.slices.verification_slice import VerificationState, Layer1State, TheoremVerification
from rlm.environments.layer1_bootstrap import Layer1Bootstrap
from rlm.agents.verification_agent_factory import VerificationAgentFactory
from tests.mock_lm import MockLM, MockLMWithResponse


# =============================================================================
# Pytest Configuration
# =============================================================================

def pytest_configure(config):
    """
    Configure pytest with custom markers and settings.

    Args:
        config: Pytest config object
    """
    config.addinivalue_line(
        "markers",
        "unit: Unit tests for individual components"
    )
    config.addinivalue_line(
        "markers",
        "integration: Integration tests for component interactions"
    )
    config.addinivalue_line(
        "markers",
        "slow: Tests that take longer to run"
    )
    config.addinivalue_line(
        "markers",
        "layer1: Tests that require Layer1 setup"
    )


# =============================================================================
# Path Fixtures
# =============================================================================

@pytest.fixture
def test_data_dir() -> Path:
    """
    Provide path to test data directory.

    Returns:
        Path to tests/fixtures directory
    """
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_dir() -> Path:
    """
    Provide a temporary directory for test files.

    Yields:
        Path to temporary directory that will be cleaned up after test
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config_path(temp_dir: Path) -> str:
    """
    Provide path to a mock configuration file.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path string to a mock config file
    """
    config_file = temp_dir / "mock-config.yaml"
    config_file.write_text("version: 0.1\n")
    return str(config_file)


# =============================================================================
# Task Descriptor Fixtures
# =============================================================================

@pytest.fixture
def simple_task_descriptor() -> TaskDescriptor:
    """
    Provide a simple task descriptor for testing.

    Returns:
        TaskDescriptor with basic fields populated
    """
    return TaskDescriptor(
        subtask_id="test-subtask-1",
        parent_task_id="main",
        intent="code_generation",
        complexity_score=0.3,
        latency_budget_ms=5000,
        cost_sensitivity="medium",
        token_estimate=100,
        safety_level="medium",
        metrics={}
    )


@pytest.fixture
def complex_task_descriptor() -> TaskDescriptor:
    """
    Provide a complex task descriptor for testing.

    Returns:
        TaskDescriptor with all fields populated
    """
    return TaskDescriptor(
        subtask_id="test-subtask-2",
        parent_task_id="main",
        intent="proof_synthesis",
        complexity_score=0.8,
        latency_budget_ms=10000,
        cost_sensitivity="low",
        token_estimate=500,
        safety_level="high",
        metrics={
            "needs_lean": True,
            "needs_haskell": True,
            "estimated_cpu_seconds": 30
        }
    )


@pytest.fixture
def task_descriptor_dict() -> Dict[str, Any]:
    """
    Provide a task descriptor as a dictionary.

    Returns:
        Dictionary with task descriptor fields
    """
    return {
        "subtask_id": "subtask-1-1234",
        "parent_task_id": "main",
        "intent": "code_generation",
        "complexity_score": 0.3,
        "latency_budget_ms": 5000,
        "cost_sensitivity": "medium",
        "token_estimate": 100,
        "safety_level": "medium",
        "capabilities": {
            "needs_internet": False,
            "needs_filesystem": True,
            "needs_lean_access": False,
            "needs_haskell_access": False,
            "needs_docker_isolation": False
        },
        "security": {
            "data_sensitivity": "internal"
        },
        "performance": {
            "expected_cpu_seconds": 1.0
        },
        "mode": "dev"
    }


# =============================================================================
# Routing Fixtures
# =============================================================================

@pytest.fixture
def backend_router(mock_config_path: str) -> BackendRouter:
    """
    Provide a BackendRouter instance for testing.

    Args:
        mock_config_path: Path to mock config file

    Returns:
        BackendRouter instance
    """
    return BackendRouter(config_path=mock_config_path)


@pytest.fixture
def backend_factory() -> BackendFactory:
    """
    Provide a BackendFactory instance for testing.

    Returns:
        BackendFactory instance with default configs
    """
    configs = {
        "rlm_internal": {"model": "gpt-4", "api_key": "test-key"},
        "claude_agent": {"model": "claude-3-opus", "api_key": "test-key"},
        "openai_gpt": {"model": "gpt-4", "api_key": "test-key"}
    }
    return BackendFactory(backend_configs=configs)


@pytest.fixture
def environment_router(mock_config_path: str) -> EnvironmentRouter:
    """
    Provide an EnvironmentRouter instance for testing.

    Args:
        mock_config_path: Path to mock config file

    Returns:
        EnvironmentRouter instance
    """
    return EnvironmentRouter(config_path=mock_config_path)


@pytest.fixture
def environment_factory() -> EnvironmentFactory:
    """
    Provide an EnvironmentFactory instance for testing.

    Returns:
        EnvironmentFactory instance with default configs
    """
    configs = {
        "local": {"enable_layer1": True},
        "docker": {"image": "python:3.11-slim"},
        "modal": {"profile": "default"}
    }
    return EnvironmentFactory(environment_configs=configs)


# =============================================================================
# Redux State Fixtures
# =============================================================================

@pytest.fixture
def initial_routing_state() -> RoutingState:
    """
    Provide an initial RoutingState for testing.

    Returns:
        RoutingState with empty collections
    """
    return RoutingState(
        decisions={},
        backend_metrics={},
        environment_metrics={}
    )


@pytest.fixture
def routing_state_with_metrics() -> RoutingState:
    """
    Provide a RoutingState with sample metrics for testing.

    Returns:
        RoutingState with populated metrics
    """
    return RoutingState(
        decisions={},
        backend_metrics={
            "claude_agent": BackendMetrics(
                backend_id="claude_agent",
                total_calls=10,
                successful_calls=9,
                total_cost=0.15,
                avg_latency_ms=250.0,
                lean_pass_rate=0.8
            )
        },
        environment_metrics={}
    )


@pytest.fixture
def initial_verification_state() -> VerificationState:
    """
    Provide an initial VerificationState for testing.

    Returns:
        VerificationState with default Layer1State
    """
    return VerificationState()


@pytest.fixture
def verification_state_loaded() -> VerificationState:
    """
    Provide a VerificationState with Layer1 loaded for testing.

    Returns:
        VerificationState with Layer1 in LOADED state
    """
    return VerificationState(
        layer1=Layer1State(
            status="loaded",
            mathlib_version="v4.0.0",
            physlib_version="v1.0.0",
            load_time_ms=1500.0,
            memory_mb=256.0
        )
    )


@pytest.fixture
def verification_state_with_theorems() -> VerificationState:
    """
    Provide a VerificationState with theorems for testing.

    Returns:
        VerificationState with sample theorems
    """
    return VerificationState(
        layer1=Layer1State(status="loaded"),
        theorems={
            "theorem-1": TheoremVerification(
                theorem_id="theorem-1",
                status="passed",
                proof_attempts=3,
                proof="example proof"
            ),
            "theorem-2": TheoremVerification(
                theorem_id="theorem-2",
                status="failed_verification",
                proof_attempts=5,
                last_error="Proof failed at step 3"
            )
        }
    )


# =============================================================================
# Layer1 Fixtures
# =============================================================================

@pytest.fixture
def mock_layer1_bootstrap(temp_dir: Path) -> Layer1Bootstrap:
    """
    Provide a Layer1Bootstrap instance with mocked dependencies.

    Args:
        temp_dir: Temporary directory for Layer1 files

    Returns:
        Layer1Bootstrap instance
    """
    # Create a fake Layer1 directory structure
    layer1_path = temp_dir / "layer1"
    layer1_path.mkdir()
    (layer1_path / "mathlib").mkdir()
    (layer1_path / "physlib").mkdir()
    (layer1_path / "haskell").mkdir()

    return Layer1Bootstrap(layer1_path=str(layer1_path))


# =============================================================================
# Agent Factory Fixtures
# =============================================================================

@pytest.fixture
def mock_parent_rlm():
    """
    Provide a mock parent RLM instance.

    Returns:
        MagicMock configured as parent RLM
    """
    rlm = MagicMock()
    rlm.backend = "openai"
    rlm.backend_kwargs = {"model": "gpt-4", "api_key": "test-key"}
    rlm.depth = 0
    rlm.max_depth = 5
    rlm.logger = MagicMock()
    return rlm


@pytest.fixture
def verification_agent_factory(mock_parent_rlm: MagicMock) -> VerificationAgentFactory:
    """
    Provide a VerificationAgentFactory for testing.

    Args:
        mock_parent_rlm: Mock parent RLM instance

    Returns:
        VerificationAgentFactory instance
    """
    return VerificationAgentFactory(parent_rlm=mock_parent_rlm)


# =============================================================================
# MockLM Fixtures
# =============================================================================

@pytest.fixture
def mock_lm() -> MockLM:
    """
    Provide a MockLM instance for testing.

    Returns:
        MockLM instance
    """
    return MockLM()


@pytest.fixture
def mock_lm_with_responses() -> MockLMWithResponse:
    """
    Provide a MockLMWithResponse instance for testing.

    Returns:
        MockLMWithResponse instance with predefined responses
    """
    responses = {
        "test prompt": "test response",
        "code prompt": "code response"
    }
    return MockLMWithResponse(responses)


# =============================================================================
# Environment Mocking Fixtures
# =============================================================================

@pytest.fixture
def mock_lean_kernel():
    """
    Provide a mock Lean kernel for testing.

    Returns:
        MagicMock configured as Lean kernel
    """
    kernel = MagicMock()
    kernel.execute.return_value = {"success": True, "output": "Proof verified"}
    return kernel


@pytest.fixture
def mock_haskell_compiler():
    """
    Provide a mock Haskell compiler for testing.

    Returns:
        MagicMock configured as Haskell compiler
    """
    compiler = MagicMock()
    compiler.compile.return_value = {"success": True, "output": "Compilation successful"}
    return compiler


# =============================================================================
# Logging Fixtures
# =============================================================================

@pytest.fixture
def caplog_with_level(caplog):
    """
    Provide caplog with a specific log level.

    Args:
        caplog: Pytest caplog fixture

    Yields:
        Caplog fixture with INFO level
    """
    with caplog.at_level("INFO"):
        yield caplog
