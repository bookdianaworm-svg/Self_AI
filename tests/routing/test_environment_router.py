"""
Tests for EnvironmentRouter component.

This module tests EnvironmentRouter class which handles:
- YAML configuration loading
- Environment rule matching based on task descriptors
- Security constraint checking
- Capability-based routing
"""

from pathlib import Path

import pytest

from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
from rlm.routing.backend_router import TaskDescriptor


class TestEnvironmentRouterInitialization:
    """
    Tests for EnvironmentRouter initialization and configuration loading.
    """

    def test_init_with_default_config(self):
        """
        Test that EnvironmentRouter initializes with default config.

        Expected behavior:
        - Router should initialize successfully
        - Should have default configuration structure
        """
        router = EnvironmentRouter()
        assert router.config is not None
        assert "version" in router.config
        assert "environments" in router.config
        assert "defaults" in router.config

    def test_init_with_config_path(self, temp_dir: Path):
        """
        Test that EnvironmentRouter loads config from specified path.

        Args:
            temp_dir: Temporary directory fixture

        Expected behavior:
        - Router should load configuration from file
        - Configuration should match file contents
        """
        config_path = temp_dir / "test-env-config.yaml"
        config_content = """
version: "0.1"
environments:
  test_env:
    kind: localrepl
    description: Test environment
defaults:
  fallback_environment: test_env
"""
        config_path.write_text(config_content)

        router = EnvironmentRouter(config_path=str(config_path))
        assert router.config["version"] == "0.1"
        assert "test_env" in router.config["environments"]
        assert router.config["defaults"]["fallback_environment"] == "test_env"

    def test_init_with_missing_config_file(self, temp_dir: Path):
        """
        Test that EnvironmentRouter falls back to default config when file not found.

        Args:
            temp_dir: Temporary directory fixture

        Expected behavior:
        - Router should not raise exception
        - Should use default configuration
        """
        config_path = temp_dir / "nonexistent.yaml"
        router = EnvironmentRouter(config_path=str(config_path))
        assert router.config is not None
        assert "environments" in router.config

    def test_init_with_invalid_yaml(self, temp_dir: Path):
        """
        Test that EnvironmentRouter handles invalid YAML gracefully.

        Args:
            temp_dir: Temporary directory fixture

        Expected behavior:
        - Router should not raise exception
        - Should use default configuration
        """
        config_path = temp_dir / "invalid.yaml"
        config_path.write_text("invalid: yaml: content: [unclosed")

        router = EnvironmentRouter(config_path=str(config_path))
        assert router.config is not None


class TestEnvironmentRuleMatching:
    """
    Tests for environment rule matching logic.
    """

    def test_route_lean_task_to_local(self, environment_router_with_config):
        """
        Test routing a task requiring Lean access.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should route to local environment
        - Should match lean_and_haskell rule
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-001",
            parent_task_id="main",
            intent="proof_synthesis",
            complexity_score=0.7,
            latency_budget_ms=10000,
            cost_sensitivity="low"
        )
        task.metrics = {"needs_lean": True}

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        assert route.environment_id == "local"
        assert "lean" in route.rule_name.lower()

    def test_route_internet_task_to_modal(self, environment_router_with_config):
        """
        Test routing a task requiring internet access.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should route to modal environment
        - Should match internet rule
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-002",
            parent_task_id="main",
            intent="web_research",
            complexity_score=0.5,
            latency_budget_ms=8000,
            cost_sensitivity="medium"
        )
        task.metrics = {"needs_internet": True}

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        assert route.environment_id == "modal"

    def test_route_sensitive_data_to_local(self, environment_router_with_config):
        """
        Test routing a task with sensitive data.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should route to local environment
        - Should enforce security constraints
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-003",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.4,
            latency_budget_ms=5000,
            cost_sensitivity="medium",
            safety_level="high"
        )
        task.metrics = {"data_sensitivity": "confidential"}

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        assert route.environment_id == "local"

    def test_route_with_no_matching_rule(self, environment_router_with_config):
        """
        Test routing when no rule matches.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should fall back to default environment
        - Should use default rule
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-004",
            parent_task_id="main",
            intent="general",
            complexity_score=0.3,
            latency_budget_ms=5000,
            cost_sensitivity="medium"
        )

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        assert route.environment_id == router.config["defaults"]["fallback_environment"]

    def test_route_high_cpu_task_to_modal(self, environment_router_with_config):
        """
        Test routing a task with high CPU requirements.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should route to modal environment
        - Should match high_cpu rule
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-005",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.6,
            latency_budget_ms=30000,
            cost_sensitivity="low"
        )
        task.metrics = {"estimated_cpu_seconds": 30}

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        assert route.environment_id == "modal"


class TestSecurityConstraintChecking:
    """
    Tests for security constraint enforcement.
    """

    def test_confidential_data_always_local(self, environment_router_with_config):
        """
        Test that confidential data always routes to local.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should enforce local-only for confidential data
        - Should override other routing decisions
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-006",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.5,
            latency_budget_ms=10000,
            cost_sensitivity="low"
        )
        task.metrics = {
            "data_sensitivity": "confidential",
            "needs_internet": True  # Would normally route to modal
        }

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        # Confidential data should override to local
        assert route.environment_id == "local"

    def test_public_data_can_use_remote(self, environment_router_with_config):
        """
        Test that public data can use remote environments.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should allow remote environments for public data
        - Should not restrict routing
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-007",
            parent_task_id="main",
            intent="web_research",
            complexity_score=0.4,
            latency_budget_ms=8000,
            cost_sensitivity="medium"
        )
        task.metrics = {
            "data_sensitivity": "public",
            "needs_internet": True
        }

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        # Public data can use modal
        assert route.environment_id == "modal"

    def test_internal_data_restricted_in_dev(self, environment_router_with_config):
        """
        Test that internal data may be restricted in dev mode.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should respect allow_remote_compute_in_dev setting
        - May restrict remote environments
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-008",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.5,
            latency_budget_ms=5000,
            cost_sensitivity="medium"
        )
        task.metrics = {"data_sensitivity": "internal"}

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        # Internal data behavior depends on config


class TestCapabilityBasedRouting:
    """
    Tests for capability-based routing decisions.
    """

    def test_lean_access_requires_local(self, environment_router_with_config):
        """
        Test that Lean access requires local environment.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should route to local for Lean access
        - Should not route to remote environments
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-009",
            parent_task_id="main",
            intent="proof_synthesis",
            complexity_score=0.8,
            latency_budget_ms=15000,
            cost_sensitivity="low"
        )
        task.metrics = {"needs_lean": True}

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        assert route.environment_id == "local"

    def test_haskell_access_requires_local(self, environment_router_with_config):
        """
        Test that Haskell access requires local environment.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should route to local for Haskell access
        - Should not route to remote environments
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-010",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.6,
            latency_budget_ms=10000,
            cost_sensitivity="medium"
        )
        task.metrics = {"needs_haskell": True}

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        assert route.environment_id == "local"

    def test_filesystem_access_allows_docker(self, environment_router_with_config):
        """
        Test that filesystem access can use Docker.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should route to Docker for filesystem access
        - When appropriate for security level
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-011",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.4,
            latency_budget_ms=5000,
            cost_sensitivity="medium"
        )
        task.metrics = {
            "needs_filesystem": True,
            "data_sensitivity": "public"
        }

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        # May route to docker for isolation

    def test_multiple_capabilities_priority(self, environment_router_with_config):
        """
        Test routing when multiple capabilities are required.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should prioritize based on rule order
        - Should satisfy all critical requirements
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-012",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.7,
            latency_budget_ms=20000,
            cost_sensitivity="low"
        )
        task.metrics = {
            "needs_lean": True,
            "needs_internet": True,
            "data_sensitivity": "internal"
        }

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)
        # Lean access should take priority (requires local)


class TestEdgeCases:
    """
    Tests for edge cases and error handling.
    """

    def test_route_with_empty_task_descriptor(self, environment_router_with_config):
        """
        Test routing with minimal task descriptor.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should not raise exception
        - Should use fallback environment
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-013",
            parent_task_id="main",
            intent="general",
            complexity_score=0.0,
            latency_budget_ms=5000,
            cost_sensitivity="medium"
        )

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)

    def test_route_with_extreme_cpu_requirements(self, environment_router_with_config):
        """
        Test routing with very high CPU requirements.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should handle extreme values gracefully
        - Should route to appropriate environment
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-014",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.9,
            latency_budget_ms=300000,
            cost_sensitivity="low"
        )
        task.metrics = {"estimated_cpu_seconds": 600}

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)

    def test_route_with_unknown_capability(self, environment_router_with_config):
        """
        Test routing with unknown capability flag.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should handle unknown flags gracefully
        - Should not raise exception
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-015",
            parent_task_id="main",
            intent="code_generation",
            complexity_score=0.5,
            latency_budget_ms=5000,
            cost_sensitivity="medium"
        )
        task.metrics = {"unknown_capability": True}

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)

    def test_route_with_none_metrics(self, environment_router_with_config):
        """
        Test routing when metrics is None.

        Args:
            environment_router_with_config: EnvironmentRouter fixture with config

        Expected behavior:
        - Should handle None metrics gracefully
        - Should use fallback environment
        """
        router = environment_router_with_config
        task = TaskDescriptor(
            subtask_id="task-016",
            parent_task_id="main",
            intent="general",
            complexity_score=0.5,
            latency_budget_ms=5000,
            cost_sensitivity="medium"
        )
        task.metrics = None

        route = router.route(task)
        assert isinstance(route, EnvironmentRoute)


class TestEnvironmentRouteDataclass:
    """
    Tests for EnvironmentRoute dataclass.
    """

    def test_environment_route_creation(self):
        """
        Test creating an EnvironmentRoute instance.

        Expected behavior:
        - Should create valid instance
        - All fields should be set correctly
        """
        route = EnvironmentRoute(
            environment_id="local",
            rule_name="test_rule",
            reasoning="Test reasoning"
        )
        assert route.environment_id == "local"
        assert route.rule_name == "test_rule"
        assert route.reasoning == "Test reasoning"

    def test_environment_route_with_empty_fields(self):
        """
        Test creating EnvironmentRoute with minimal fields.

        Expected behavior:
        - Should create valid instance
        - Empty strings should be allowed
        """
        route = EnvironmentRoute(
            environment_id="",
            rule_name="",
            reasoning=""
        )
        assert route.environment_id == ""
        assert route.rule_name == ""
        assert route.reasoning == ""


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def environment_router_with_config(temp_dir: Path) -> EnvironmentRouter:
    """
    Provide an EnvironmentRouter with test configuration.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        EnvironmentRouter instance with test config
    """
    config_path = temp_dir / "environment-test-config.yaml"
    config_content = """
version: "0.1"
environments:
  local:
    kind: localrepl
    description: Host Python REPL
    default: true
    capabilities:
      - lean_access
      - haskell_access
      - filesystem
  docker:
    kind: dockerrepl
    description: Docker container
    image: python:3.11-slim
    capabilities:
      - filesystem
      - python_execution
  modal:
    kind: modalrepl
    description: Modal Sandbox
    profile: default
    capabilities:
      - internet_access
      - python_execution
defaults:
  fallback_environment: local
  allow_remote_compute_in_dev: false
  strict_local_for_sensitive_data: true
rules:
  - name: lean_and_haskell_always_local
    when:
      capabilities.needs_lean_access: true
    choose:
      environment: local
    reasoning: "Lean and Haskell require local installation"
  - name: sensitive_data_always_local
    when:
      security.data_sensitivity: confidential
    choose:
      environment: local
    reasoning: "Confidential data must stay local"
  - name: internet_uses_modal
    when:
      capabilities.needs_internet: true
    choose:
      environment: modal
    reasoning: "Modal provides internet access"
  - name: docker_isolation_for_untrusted
    when:
      security.data_sensitivity: public
      capabilities.needs_filesystem: true
    choose:
      environment: docker
    reasoning: "Docker provides isolation for public data"
  - name: high_cpu_uses_modal
    when:
      performance.expected_cpu_seconds: ">10"
    choose:
      environment: modal
    reasoning: "Modal provides more CPU resources"
  - name: default_to_local
    when: {}
    choose:
      environment: local
    reasoning: "Default to local environment"
"""
    config_path.write_text(config_content)
    return EnvironmentRouter(config_path=str(config_path))
