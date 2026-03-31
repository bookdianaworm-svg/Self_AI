"""
Backend router for dynamic backend selection based on task descriptors.
"""

import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class BackendMetrics:
    """Metrics for a specific backend."""
    backend_id: str
    total_calls: int
    successful_calls: int
    total_cost: float
    avg_latency_ms: float


@dataclass
class BackendRoute:
    """Result of backend routing decision."""
    backend_id: str
    rule_name: str
    overrides: list[str]
    reasoning: str


@dataclass
class TaskDescriptor:
    """Descriptor for a sub-task used in routing decisions."""
    subtask_id: str
    parent_task_id: str
    intent: str
    complexity_score: float
    latency_budget_ms: int
    cost_sensitivity: str
    token_estimate: Optional[int] = None
    safety_level: str = "medium"
    metrics: Optional[Dict[str, Any]] = None


class BackendRouter:
    """
    Routes sub-calls to appropriate backend clients based on task descriptors.
    """

    def __init__(self, config_path: str | None = None):
        """
        Initialize backend router with configuration.

        Args:
            config_path: Path to backend-routing.yaml config file
        """
        self.config = self._load_config(config_path)
        self.metrics_store = MetricsStore()

    def _load_config(self, config_path: str | None) -> dict:
        """Load backend routing configuration from YAML file."""
        if config_path is None:
            config_path = self._default_config_path()

        if yaml is not None:
            try:
                with open(config_path, "r") as f:
                    return yaml.safe_load(f)
            except FileNotFoundError:
                # Return default configuration
                return self._default_config()
            except Exception:
                # Return default configuration for any other error
                return self._default_config()
        else:
            # yaml not available, return default configuration
            return self._default_config()

    def _default_config_path(self) -> str:
        """Return default path to backend routing config."""
        return os.path.join(
            os.path.dirname(__file__),
            "..",
            "config",
            "backend-routing.yaml"
        )

    def _default_config(self) -> dict:
        """Return default backend routing configuration."""
        return {
            "version": "0.1",
            "backends": {
                "rlm_internal": {
                    "provider": "internal",
                    "description": "Default internal RLM-backed model"
                },
                "claude_agent": {
                    "provider": "anthropic",
                    "description": "Claude Agent SDK"
                },
                "openai_gpt": {
                    "provider": "openai",
                    "description": "OpenAI GPT model"
                }
            },
            "defaults": {
                "fallback_backend": "rlm_internal",
                "global_cost_priority": "medium",
                "global_quality_priority": "high"
            },
            "rules": [
                {
                    "name": "cheap_simple_research",
                    "when": {
                        "intent": "web_research",
                        "complexity_score": "<0.4",
                        "latency_budget_ms": ">=2000"
                    },
                    "choose": {
                        "backend": "rlm_internal"
                    }
                },
                {
                    "name": "deep_research_claude",
                    "when": {
                        "intent": "web_research",
                        "complexity_score": ">=0.4"
                    },
                    "choose": {
                        "backend": "claude_agent"
                    }
                },
                {
                    "name": "proof_synthesis_strong",
                    "when": {
                        "intent": "proof_synthesis",
                        "complexity_score": ">=0.3"
                    },
                    "choose": {
                        "backend": "claude_agent"
                    }
                }
            ],
            "adaptive_overrides": [
                {
                    "name": "avoid_low_pass_backend_for_proofs",
                    "when": {
                        "intent": "proof_synthesis",
                        "metrics.lean_pass_rate_last_50": "<0.6"
                    },
                    "override": {
                        "backend": "claude_agent"
                    }
                }
            ]
        }

    def choose_backend(self, desc: TaskDescriptor) -> BackendRoute:
        """
        Choose backend for a sub-call based on task descriptor.

        Args:
            desc: Task descriptor with intent, complexity, etc.

        Returns:
            BackendRoute with selected backend and metadata
        """
        features = self._augment_with_metrics(desc)
        backend = self._match_rules(features)
        backend, overrides = self._apply_adaptive_overrides(backend, features)

        return BackendRoute(
            backend_id=backend,
            rule_name=features.get("_matched_rule", "fallback"),
            overrides=overrides,
            reasoning=self._generate_reasoning(features, backend, overrides)
        )

    def route(self, desc: TaskDescriptor) -> BackendRoute:
        """
        Route a task to appropriate backend (alias for choose_backend).

        Args:
            desc: Task descriptor with intent, complexity, etc.

        Returns:
            BackendRoute with selected backend and metadata
        """
        return self.choose_backend(desc)

    def record_call(
        self,
        backend_id: str,
        success: bool,
        latency_ms: float,
        cost: float
    ) -> None:
        """
        Record a backend call for metrics tracking.

        Args:
            backend_id: Identifier of the backend used
            success: Whether the call succeeded
            latency_ms: Latency of the call in milliseconds
            cost: Cost of the call
        """
        self.metrics_store.record_call(backend_id, success, latency_ms, cost)

    def get_backend_metrics(self, backend_id: str) -> Optional[BackendMetrics]:
        """
        Get metrics for a specific backend.

        Args:
            backend_id: Identifier of the backend

        Returns:
            BackendMetrics with aggregated call statistics, or None if backend not found
        """
        return self.metrics_store.get_backend_metrics(backend_id)

    def _augment_with_metrics(self, desc: TaskDescriptor) -> Dict[str, Any]:
        """Fetch rolling metrics and add to descriptor."""
        # Handle both dict and TaskDescriptor objects
        if isinstance(desc, dict):
            features = desc.copy()
            intent = desc.get("intent", "")
        else:
            # TaskDescriptor object
            features = desc.__dict__.copy()
            intent = desc.intent
        metrics = self.metrics_store.get_for_intent(intent)
        features["metrics"] = metrics
        return features

    def _match_rules(self, features: Dict[str, Any]) -> str:
        """Match task descriptor against routing rules."""
        for rule in self.config.get("rules", []):
            if self._matches(rule["when"], features):
                features["_matched_rule"] = rule["name"]
                return rule["choose"]["backend"]
        return self.config["defaults"]["fallback_backend"]

    def _apply_adaptive_overrides(
        self,
        backend: str,
        features: Dict[str, Any]
    ) -> tuple[str, list[str]]:
        """Apply adaptive overrides based on metrics."""
        applied = []
        for override in self.config.get("adaptive_overrides", []):
            if self._matches(override["when"], features):
                backend = override["override"]["backend"]
                applied.append(override["name"])
        return backend, applied

    def _matches(self, cond: Dict[str, Any], features: Dict[str, Any]) -> bool:
        """Check if condition matches features."""
        for key, pattern in cond.items():
            value = self._get_nested(features, key)
            if not self._match_single(value, pattern):
                return False
        return True

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

    def _match_single(self, value: Any, pattern: str) -> bool:
        """Match a single value against a pattern."""
        if value is None:
            return False

        # Numeric comparison pattern
        if isinstance(value, (int, float)) and isinstance(pattern, str):
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

    def _generate_reasoning(
        self,
        features: Dict[str, Any],
        backend: str,
        overrides: list[str]
    ) -> str:
        """Generate human-readable reasoning for routing decision."""
        rule = features.get("_matched_rule", "fallback")
        reasoning = f"Rule '{rule}' matched, selected backend '{backend}'"
        if overrides:
            reasoning += f", overrides applied: {', '.join(overrides)}"
        return reasoning


class MetricsStore:
    """
    Stores rolling metrics for backend performance tracking.
    """

    def __init__(self):
        self.metrics: Dict[tuple[str, str], Dict[str, Any]] = {}
        self.backend_metrics: Dict[str, Dict[str, Any]] = {}
        self.window_size = 50

    def update(
        self,
        backend_id: str,
        intent: str,
        verification_result: Dict[str, Any]
    ):
        """Update metrics after a sub-call completes."""
        key = (backend_id, intent)

        if key not in self.metrics:
            self.metrics[key] = {
                "samples": 0,
                "lean_pass_count": 0,
                "total_iterations": 0,
                "total_latency_ms": 0,
                "total_cost": 0
            }

        metrics = self.metrics[key]
        metrics["samples"] += 1
        metrics["lean_pass_count"] += verification_result.get("passed", 0)
        metrics["total_iterations"] += verification_result.get("iterations", 0)
        metrics["total_latency_ms"] += verification_result.get("latency_ms", 0)
        metrics["total_cost"] += verification_result.get("cost", 0)

        # Keep only last N samples
        if metrics["samples"] > self.window_size:
            # Simple FIFO - in production, use proper rolling window
            pass

    def get_for_intent(self, intent: str) -> Dict[str, Any]:
        """Get aggregated metrics for all backends for an intent."""
        result = {}
        for (backend_id, intent_key), metrics in self.metrics.items():
            if intent_key == intent:
                samples = metrics["samples"]
                if samples > 0:
                    result[f"{backend_id}.lean_pass_rate_last_{samples}"] = (
                        metrics["lean_pass_count"] / samples
                    )
                    result[f"{backend_id}.avg_iterations_to_pass_last_{samples}"] = (
                        metrics["total_iterations"] / samples
                    )
                    result[f"{backend_id}.avg_latency_ms_last_{samples}"] = (
                        metrics["total_latency_ms"] / samples
                    )
                    result[f"{backend_id}.avg_cost_last_{samples}"] = (
                        metrics["total_cost"] / samples
                    )
        return result

    def record_call(
        self,
        backend_id: str,
        success: bool,
        latency_ms: float,
        cost: float
    ) -> None:
        """Record a backend call for metrics tracking."""
        if backend_id not in self.backend_metrics:
            self.backend_metrics[backend_id] = {
                "total_calls": 0,
                "successful_calls": 0,
                "total_latency_ms": 0.0,
                "total_cost": 0.0
            }

        metrics = self.backend_metrics[backend_id]
        metrics["total_calls"] += 1
        metrics["successful_calls"] += 1 if success else 0
        metrics["total_latency_ms"] += latency_ms
        metrics["total_cost"] += cost

    def get_backend_metrics(self, backend_id: str) -> Optional[BackendMetrics]:
        """Get metrics for a specific backend."""
        if backend_id not in self.backend_metrics:
            return None

        metrics = self.backend_metrics[backend_id]
        total_calls = metrics["total_calls"]
        avg_latency = (
            metrics["total_latency_ms"] / total_calls if total_calls > 0 else 0.0
        )

        return BackendMetrics(
            backend_id=backend_id,
            total_calls=total_calls,
            successful_calls=metrics["successful_calls"],
            total_cost=metrics["total_cost"],
            avg_latency_ms=avg_latency
        )
