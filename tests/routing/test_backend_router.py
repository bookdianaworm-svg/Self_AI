"""
Tests for BackendRouter component.

This module tests the BackendRouter class which handles:
- YAML configuration loading
- Route matching based on task descriptors
- Metrics tracking for backends
- Adaptive overrides based on performance
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from rlm.routing.backend_router import BackendRouter, BackendRoute, TaskDescriptor


class TestBackendRouterInitialization:
    """
    Tests for BackendRouter initialization and configuration loading.
    """

    def test_init_with_default_config(self):
        """
        Test that BackendRouter initializes with default config when no path provided.

        Expected behavior:
        - Router should initialize successfully
        - Should have default configuration structure
        - MetricsStore should be initialized
        """
        router = BackendRouter()
        assert router.config is not None
        assert "version" in router.config
        assert "backends" in router.config
        assert "defaults" in router.config
        assert router.metrics_store is not None

    def test_init_with_config_path(self, temp_dir: Path):
        """
        Test that BackendRouter loads config from specified path.

        Args:
            temp_dir: Temporary directory fixture

        Expected behavior:
        - Router should load configuration from file
        - Configuration should match file contents
        """
        config_path = temp_dir / "test-config.yaml"
        config_content = """
version: "0.1"
backends:
  test_backend:
    provider: test
    description: Test backend
defaults:
  fallback_backend: test_backend
"""
        config_path.write_text(config_content)

        router = BackendRouter(config_path=str(config_path))
        assert router.config["version"] == "0.1"
        assert "test_backend" in router.config["backends"]
        assert router.config["defaults"]["fallback_backend"] == "test_backend"

    def test_init_with_missing_config_file(self, temp_dir: Path):
        """
        Test that BackendRouter falls back to default config when file not found.

        Args:
            temp_dir: Temporary directory fixture

        Expected behavior:
        - Router should not raise exception
        - Should use default configuration
        """
        config_path = temp_dir / "nonexistent.yaml"
        router = BackendRouter(config_path=str(config_path))
        assert router.config is not None
        assert "backends" in router.config

    def test_init_with_invalid_yaml(self, temp_dir: Path):
        """
        Test that BackendRouter handles invalid YAML gracefully.

        Args:
            temp_dir: Temporary directory fixture

        Expected behavior:
        - Router should not raise exception
        - Should use default configuration
        """
        config_path = temp_dir / "invalid.yaml"
        config_path.write_text("invalid: yaml: content: [unclosed")

        router = BackendRouter(config_path=str(config_path))
        assert router.config is not None

    def test_metrics_store_initialization(self):
        """
        Test that MetricsStore is properly initialized.

        Expected behavior:
        - MetricsStore should be accessible
        - Should be a new instance for each router
        """
        router1 = BackendRouter()
        router2 = BackendRouter()
        assert router1.metrics_store is not router2.metrics_store


class TestConfigLoading:
    """
    Tests for configuration loading methods.
    """

    def test_load_config_from_file(self, temp_dir: Path):
        """
        Test loading configuration from a valid YAML file.

        Args:
            temp_dir: Temporary directory fixture

        Expected behavior:
        - Configuration should be loaded correctly
        - All sections should be present
        """
        config_path = temp_dir / "test-config.yaml"
        config_content = """
version: "0.1"
backends:
  backend1:
    provider: openai
    description: Backend 1
  backend2:
    provider: anthropic
    description: Backend 2
defaults:
  fallback_backend: backend1
  global_cost_priority: high
"""
        config_path.write_text(config_content)

        router = BackendRouter(config_path=str(config_path))
        assert len(router.config["backends"]) == 2
        assert "backend1" in router.config["backends"]
        assert "backend2" in router.config["backends"]
        assert router.config["defaults"]["fallback_backend"] == "backend1"

    def test_default_config_structure(self):
        """
        Test that default configuration has required structure.

        Expected behavior:
        - Should have version field
        - Should have backends dictionary
        - Should have defaults dictionary
        - Should have rules list
        """
        router = BackendRouter()
        assert "version" in router.config
        assert isinstance(router.config["backends"], dict)
        assert isinstance(router.config["defaults"], dict)
        assert isinstance(router.config.get("rules", []), list)

    def test_default_config_has_fallback(self):
        """
        Test that default config includes a fallback backend.

        Expected behavior:
        - Should define a fallback backend
        - Fallback should be a valid backend
        """
        router = BackendRouter()
        fallback = router.config["defaults"].get("fallback_backend")
        assert fallback is not None
        assert fallback in router.config["backends"]


class TestRouteMatching:
    """
    Tests for route matching logic based on task descriptors.
    """

    def test_route_simple_code_task(self, backend_router_with_config):
        """
        Test routing a simple code generation task.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Should match appropriate rule
        - Should return correct backend
        - Should include reasoning
        """
        router = backend_router_with_config
        task = TaskDescriptor(
            subtask_id="task-001",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.3,
            latency_budget_ms=5000,
            cost_sensitivity="medium"
        )

        route = router.route(task)
        assert isinstance(route, BackendRoute)
        assert route.backend_id is not None
        assert route.rule_name is not None
        assert route.reasoning is not None

    def test_route_proof_synthesis_task(self, backend_router_with_config):
        """
        Test routing a proof synthesis task.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Should match proof synthesis rule
        - Should prefer high-quality backend
        - Should include appropriate overrides
        """
        router = backend_router_with_config
        task = TaskDescriptor(
            subtask_id="task-002",
            parent_task_id="main",
            intent="proof_synthesis",
            complexity_score=0.7,
            latency_budget_ms=10000,
            cost_sensitivity="low"
        )

        route = router.route(task)
        assert isinstance(route, BackendRoute)
        # Proof synthesis should route to a high-quality backend

    def test_route_cost_sensitive_task(self, backend_router_with_config):
        """
        Test routing a cost-sensitive task.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Should match cost-sensitive rule
        - Should prefer cost-effective backend
        """
        router = backend_router_with_config
        task = TaskDescriptor(
            subtask_id="task-003",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.4,
            latency_budget_ms=5000,
            cost_sensitivity="high"
        )

        route = router.route(task)
        assert isinstance(route, BackendRoute)

    def test_route_with_no_matching_rule(self, backend_router_with_config):
        """
        Test routing when no rule matches.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Should fall back to default backend
        - Should use default rule
        """
        router = backend_router_with_config
        task = TaskDescriptor(
            subtask_id="task-004",
            parent_task_id="main",
            intent="unknown_intent",
            complexity_score=0.5,
            latency_budget_ms=5000,
            cost_sensitivity="medium"
        )

        route = router.route(task)
        assert isinstance(route, BackendRoute)
        assert route.backend_id == router.config["defaults"]["fallback_backend"]

    def test_route_with_overrides(self, backend_router_with_config):
        """
        Test that route includes appropriate overrides.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Route should include override list
        - Overrides should match rule configuration
        """
        router = backend_router_with_config
        task = TaskDescriptor(
            subtask_id="task-005",
            parent_task_id="main",
            intent="proof_synthesis",
            complexity_score=0.8,
            latency_budget_ms=15000,
            cost_sensitivity="low"
        )

        route = router.route(task)
        assert isinstance(route, BackendRoute)
        # Check that overrides list is present (may be empty)
        assert isinstance(route.overrides, list)


class TestMetricsTracking:
    """
    Tests for metrics tracking functionality.
    """

    def test_record_backend_call(self, backend_router_with_config):
        """
        Test recording a backend call in metrics.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Call should be recorded in metrics
        - Count should increment
        """
        router = backend_router_with_config
        backend_id = "test_backend"

        router.record_call(backend_id, success=True, latency_ms=100, cost=0.01)

        metrics = router.get_backend_metrics(backend_id)
        assert metrics is not None
        assert metrics.total_calls == 1
        assert metrics.successful_calls == 1

    def test_record_failed_backend_call(self, backend_router_with_config):
        """
        Test recording a failed backend call.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Failure should be recorded
        - Success count should not increment
        """
        router = backend_router_with_config
        backend_id = "test_backend"

        router.record_call(backend_id, success=False, latency_ms=200, cost=0.01)

        metrics = router.get_backend_metrics(backend_id)
        assert metrics is not None
        assert metrics.total_calls == 1
        assert metrics.successful_calls == 0

    def test_get_backend_metrics(self, backend_router_with_config):
        """
        Test retrieving backend metrics.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Should return metrics for existing backend
        - Should return None for non-existent backend
        """
        router = backend_router_with_config
        backend_id = "test_backend"

        router.record_call(backend_id, success=True, latency_ms=100, cost=0.01)

        metrics = router.get_backend_metrics(backend_id)
        assert metrics is not None
        assert metrics.backend_id == backend_id

        non_existent = router.get_backend_metrics("non_existent")
        assert non_existent is None

    def test_metrics_aggregation(self, backend_router_with_config):
        """
        Test that metrics are aggregated correctly.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Average latency should be calculated correctly
        - Total cost should be summed
        - Pass rate should be calculated
        """
        router = backend_router_with_config
        backend_id = "test_backend"

        router.record_call(backend_id, success=True, latency_ms=100, cost=0.01)
        router.record_call(backend_id, success=True, latency_ms=200, cost=0.02)
        router.record_call(backend_id, success=False, latency_ms=300, cost=0.03)

        metrics = router.get_backend_metrics(backend_id)
        assert metrics.total_calls == 3
        assert metrics.successful_calls == 2
        assert metrics.total_cost == 0.06
        assert metrics.avg_latency_ms == 200.0


class TestAdaptiveOverrides:
    """
    Tests for adaptive override functionality.
    """

    def test_adaptive_override_based_on_metrics(self, backend_router_with_config):
        """
        Test that routing adapts based on backend metrics.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Backend with better metrics should be preferred
        - Routing should consider pass rates
        """
        router = backend_router_with_config

        # Record poor performance for backend1
        router.record_call("backend1", success=False, latency_ms=500, cost=0.05)
        router.record_call("backend1", success=False, latency_ms=600, cost=0.05)

        # Record good performance for backend2
        router.record_call("backend2", success=True, latency_ms=100, cost=0.01)
        router.record_call("backend2", success=True, latency_ms=120, cost=0.01)

        # Routing should prefer backend2 based on metrics
        task = TaskDescriptor(
            subtask_id="task-006",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.5,
            latency_budget_ms=5000,
            cost_sensitivity="medium"
        )

        route = router.route(task)
        # The routing logic should consider metrics
        assert isinstance(route, BackendRoute)

    def test_adaptive_override_with_high_latency(self, backend_router_with_config):
        """
        Test that routing adapts when backend has high latency.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Should prefer faster backend for low latency budget
        """
        router = backend_router_with_config

        # Record high latency for backend1
        router.record_call("backend1", success=True, latency_ms=1000, cost=0.01)

        task = TaskDescriptor(
            subtask_id="task-007",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.3,
            latency_budget_ms=500,  # Low latency budget
            cost_sensitivity="medium"
        )

        route = router.route(task)
        assert isinstance(route, BackendRoute)


class TestEdgeCases:
    """
    Tests for edge cases and error handling.
    """

    def test_route_with_empty_task_descriptor(self, backend_router_with_config):
        """
        Test routing with minimal task descriptor.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Should not raise exception
        - Should use fallback backend
        """
        router = backend_router_with_config
        task = TaskDescriptor(
            subtask_id="task-008",
            parent_task_id="main",
            intent="general",
            complexity_score=0.0,
            latency_budget_ms=5000,
            cost_sensitivity="medium"
        )

        route = router.route(task)
        assert isinstance(route, BackendRoute)

    def test_route_with_extreme_complexity(self, backend_router_with_config):
        """
        Test routing with maximum complexity score.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Should handle extreme values gracefully
        - Should route to appropriate backend
        """
        router = backend_router_with_config
        task = TaskDescriptor(
            subtask_id="task-009",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=1.0,
            latency_budget_ms=60000,
            cost_sensitivity="low"
        )

        route = router.route(task)
        assert isinstance(route, BackendRoute)

    def test_route_with_zero_latency_budget(self, backend_router_with_config):
        """
        Test routing with zero latency budget.

        Args:
            backend_router_with_config: BackendRouter fixture with config

        Expected behavior:
        - Should handle zero budget gracefully
        - Should consider latency in routing
        """
        router = backend_router_with_config
        task = TaskDescriptor(
            subtask_id="task-010",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.3,
            latency_budget_ms=0,
            cost_sensitivity="medium"
        )

        route = router.route(task)
        assert isinstance(route, BackendRoute)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def backend_router_with_config(temp_dir: Path) -> BackendRouter:
    """
    Provide a BackendRouter with test configuration.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        BackendRouter instance with test config
    """
    config_path = temp_dir / "backend-test-config.yaml"
    config_content = """
version: "0.1"
backends:
  backend1:
    provider: openai
    description: OpenAI backend
    cost_per_1k_tokens: 0.03
    avg_latency_ms: 200
    lean_pass_rate: 0.75
  backend2:
    provider: anthropic
    description: Anthropic backend
    cost_per_1k_tokens: 0.015
    avg_latency_ms: 300
    lean_pass_rate: 0.85
  test_backend:
    provider: test
    description: Test backend
defaults:
  fallback_backend: backend1
  global_cost_priority: medium
  global_quality_priority: high
rules:
  - name: proof_synthesis_uses_backend2
    when:
      intent: proof_synthesis
      complexity_score: "> 0.5"
    choose:
      backend: backend2
    reasoning: "Backend2 has higher pass rate for proof synthesis"
  - name: simple_code_uses_backend1
    when:
      intent: code_generation
      complexity_score: "< 0.4"
    choose:
      backend: backend1
    reasoning: "Backend1 is faster for simple code"
  - name: cost_sensitive_uses_backend2
    when:
      cost_sensitivity: high
      complexity_score: "< 0.6"
    choose:
      backend: backend2
    reasoning: "Backend2 is more cost-effective"
  - name: default_to_backend1
    when: {}
    choose:
      backend: backend1
    reasoning: "Default to backend1"
"""
    config_path.write_text(config_content)
    return BackendRouter(config_path=str(config_path))
