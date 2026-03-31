"""
Environment router for dynamic environment selection based on task descriptors.
"""

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from rlm.routing.backend_router import TaskDescriptor

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class EnvironmentRoute:
    """Result of environment routing decision."""
    environment_id: str
    rule_name: str
    reasoning: str
    config: Dict[str, Any] = field(default_factory=dict)


class EnvironmentRouter:
    """
    Routes sub-calls to appropriate execution environments based on task descriptors.
    """

    def __init__(self, config_path: str | None = None):
        """
        Initialize environment router with configuration.

        Args:
            config_path: Path to environment-routing.yaml config file
        """
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str | None) -> dict:
        """Load environment routing configuration from YAML file."""
        if config_path is None:
            config_path = self._default_config_path()

        if yaml is not None:
            try:
                with open(config_path, "r") as f:
                    return yaml.safe_load(f)
            except FileNotFoundError:
                return self._default_config()
            except yaml.YAMLError:
                return self._default_config()
            except Exception:
                return self._default_config()
        else:
            return self._default_config()

    def _default_config_path(self) -> str:
        """Return default path to environment routing config."""
        return os.path.join(
            os.path.dirname(__file__),
            "..",
            "config",
            "environment-routing.yaml"
        )

    def _default_config(self) -> dict:
        """Return default environment routing configuration."""
        return {
            "version": "0.1",
            "environments": {
                "local": {
                    "kind": "localrepl",
                    "description": "Host Python REPL (Lean/Haskell installed here)",
                    "default": True
                },
                "docker": {
                    "kind": "dockerrepl",
                    "description": "Docker container with optional internet access",
                    "image": "python:3.11-slim",
                    "network_mode": "bridge",
                    "cpu_limit": 1.0,
                    "memory_limit_gb": 2
                },
                "modal": {
                    "kind": "modalrepl",
                    "description": "Modal Sandbox for internet-facing subtasks",
                    "profile": "default",
                    "cpu_limit": 2.0,
                    "memory_limit_gb": 4
                }
            },
            "defaults": {
                "fallback_environment": "local",
                "allow_remote_compute_in_dev": False,
                "strict_local_for_sensitive_data": True
            },
            "rules": [
                {
                    "name": "lean_and_haskell_always_local",
                    "when": {
                        "capabilities.needs_lean_access": True
                    },
                    "choose": {
                        "environment": "local"
                    }
                },
                {
                    "name": "sensitive_data_force_local",
                    "when": {
                        "security.data_sensitivity": "confidential"
                    },
                    "choose": {
                        "environment": "local"
                    }
                },
                {
                    "name": "pure_filesystem_local",
                    "when": {
                        "capabilities.needs_filesystem": True,
                        "capabilities.needs_internet": False,
                        "security.data_sensitivity": "local_only"
                    },
                    "choose": {
                        "environment": "local"
                    }
                },
                {
                    "name": "untrusted_code_docker",
                    "when": {
                        "capabilities.needs_docker_isolation": True,
                        "capabilities.needs_internet": False
                    },
                    "choose": {
                        "environment": "docker"
                    }
                },
                {
                    "name": "internet_research_modal",
                    "when": {
                        "capabilities.needs_internet": True
                    },
                    "choose": {
                        "environment": "modal"
                    }
                }
            ]
        }

    def route(self, task: "TaskDescriptor") -> EnvironmentRoute:
        """
        Route a task to an appropriate environment.

        Args:
            task: TaskDescriptor with task details and metrics

        Returns:
            EnvironmentRoute with selected environment and metadata
        """
        desc = self._build_features_dict(task)
        route = self.choose_env(desc)
        route.config = self._get_environment_config(route.environment_id)
        return route

    def _build_features_dict(self, task: "TaskDescriptor") -> Dict[str, Any]:
        """Build features dict from TaskDescriptor for rule matching."""
        # Handle both dict and TaskDescriptor objects
        if isinstance(task, dict):
            subtask_id = task.get("subtask_id", "")
            intent = task.get("intent", "")
            complexity_score = task.get("complexity_score", 0.0)
            latency_budget_ms = task.get("latency_budget_ms", 5000)
            cost_sensitivity = task.get("cost_sensitivity", "medium")
            safety_level = task.get("safety_level", "medium")
            metrics = task.get("metrics")
        else:
            # TaskDescriptor object
            subtask_id = task.subtask_id
            intent = task.intent
            complexity_score = task.complexity_score
            latency_budget_ms = task.latency_budget_ms
            cost_sensitivity = task.cost_sensitivity
            safety_level = task.safety_level
            metrics = getattr(task, 'metrics', None)
        
        features = {
            "subtask_id": subtask_id,
            "intent": intent,
            "complexity_score": complexity_score,
            "latency_budget_ms": latency_budget_ms,
            "cost_sensitivity": cost_sensitivity,
            "safety_level": safety_level,
            "mode": "dev"  # Default mode
        }
        
        if metrics:
            features["capabilities"] = {}
            if "needs_lean" in metrics:
                features["capabilities"]["needs_lean_access"] = metrics["needs_lean"]
            if "needs_haskell" in metrics:
                features["capabilities"]["needs_haskell_access"] = metrics["needs_haskell"]
            if "needs_internet" in metrics:
                features["capabilities"]["needs_internet"] = metrics["needs_internet"]
            if "needs_filesystem" in metrics:
                features["capabilities"]["needs_filesystem"] = metrics["needs_filesystem"]
            if "needs_docker_isolation" in metrics:
                features["capabilities"]["needs_docker_isolation"] = metrics["needs_docker_isolation"]
            if "data_sensitivity" in metrics:
                if "security" not in features:
                    features["security"] = {}
                features["security"]["data_sensitivity"] = metrics["data_sensitivity"]
            if "estimated_cpu_seconds" in metrics:
                features["performance"] = {"expected_cpu_seconds": metrics["estimated_cpu_seconds"]}
            if "mode" in metrics:
                features["mode"] = metrics["mode"]
            for key, value in metrics.items():
                if key not in ("needs_lean", "needs_haskell", "needs_internet",
                               "needs_filesystem", "needs_docker_isolation",
                               "data_sensitivity", "estimated_cpu_seconds", "mode"):
                    if "capabilities" not in features:
                        features["capabilities"] = {}
                    features["capabilities"][key] = value
        return features

    def _get_environment_config(self, environment_id: str) -> Dict[str, Any]:
        """Get configuration for the selected environment."""
        return self.config.get("environments", {}).get(environment_id, {})

    def choose_env(self, desc: Dict[str, Any]) -> EnvironmentRoute:
        """
        Choose environment for a sub-call based on task descriptor.

        Args:
            desc: Task descriptor with capabilities, security, mode

        Returns:
            EnvironmentRoute with selected environment and metadata
        """
        env_id = self._match_rules(desc)
        rule_name = desc.get("_matched_rule", "fallback")

        return EnvironmentRoute(
            environment_id=env_id,
            rule_name=rule_name,
            reasoning=self._generate_reasoning(desc, env_id, rule_name)
        )

    def _match_rules(self, features: Dict[str, Any]) -> str:
        """Match task descriptor against routing rules."""
        for rule in self.config.get("rules", []):
            if self._matches(rule["when"], features):
                features["_matched_rule"] = rule["name"]
                return rule["choose"]["environment"]
        return self.config["defaults"]["fallback_environment"]

    def _matches(self, cond: Dict[str, Any], features: Dict[str, Any]) -> bool:
        """Check if condition matches features."""
        for key, pattern in cond.items():
            value = self._get_nested(features, key)
            if not self._match_single(value, pattern):
                return False
        return True

    def _match_single(self, value: Any, pattern: str) -> bool:
        """Match a single value against a pattern."""
        if value is None:
            return False

        # Numeric comparison pattern
        if isinstance(value, (int, float)) and isinstance(pattern, str):
            import re
            m = re.match(r"([<>]=?)([0-9.]+)", pattern)
            if m:
                op, num = m.group(1), float(m.group(2))
                if op == ">":
                    return value > num
                if op == ">=":
                    return value >= num
                if op == "<":
                    return value < num
                if op == "<=":
                    return value <= num

        # Exact match
        return value == pattern

    def _get_nested(self, obj: Dict[str, Any], key: str) -> Any:
        """Get nested value from dict using dot notation."""
        parts = key.split(".")
        cur = obj
        for p in parts:
            if not isinstance(cur, dict):
                return None
            cur = cur.get(p)
            if cur is None:
                return None
        return cur

    def _generate_reasoning(
        self,
        features: Dict[str, Any],
        env_id: str,
        rule_name: str
    ) -> str:
        """Generate human-readable reasoning for routing decision."""
        return f"Rule '{rule_name}' matched, selected environment '{env_id}'"
