"""
Improvements Package for self-improving system.

This package provides the improvement registry and contribution
workflow for agents to propose and share improvements.
"""

from rlm.improvements.improvement_registry import (
    ImprovementType,
    ImprovementCategory,
    ImprovementStatus,
    ImpactLevel,
    ImprovementEntity,
    ImprovementRegistry,
)

__all__ = [
    "ImprovementType",
    "ImprovementCategory",
    "ImprovementStatus",
    "ImpactLevel",
    "ImprovementEntity",
    "ImprovementRegistry",
]
