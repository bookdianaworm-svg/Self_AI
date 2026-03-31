"""
Backend and environment routing for RLM sub-calls.

This module provides dynamic routing capabilities for selecting appropriate
backends and environments based on task descriptors.
"""

from rlm.routing.backend_router import (
    BackendRouter,
    BackendRoute,
    TaskDescriptor,
    MetricsStore,
)
from rlm.routing.backend_factory import BackendFactory
from rlm.routing.environment_router import EnvironmentRouter, EnvironmentRoute
from rlm.routing.environment_factory import EnvironmentFactory
from rlm.routing.domain_classifier import (
    DomainClassifier,
    DomainType,
    ClassificationConfidence,
    ClassificationResult,
    DomainScore,
)

__all__ = [
    "BackendRouter",
    "BackendRoute",
    "TaskDescriptor",
    "MetricsStore",
    "BackendFactory",
    "EnvironmentRouter",
    "EnvironmentRoute",
    "EnvironmentFactory",
    "DomainClassifier",
    "DomainType",
    "ClassificationConfidence",
    "ClassificationResult",
    "DomainScore",
]
