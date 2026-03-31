"""
RLM Agent Prompts Package.

This package contains system prompts for specialized RLM agents.
"""

from rlm.agents.prompts.verification_prompts import (
    AUTOFORMALIZATION_SYSTEM_PROMPT,
    VERIFIER_SYSTEM_PROMPT,
    PHYSICIST_SYSTEM_PROMPT,
    CROSS_CHECK_SYSTEM_PROMPT,
)

__all__ = [
    "AUTOFORMALIZATION_SYSTEM_PROMPT",
    "VERIFIER_SYSTEM_PROMPT",
    "PHYSICIST_SYSTEM_PROMPT",
    "CROSS_CHECK_SYSTEM_PROMPT",
]
