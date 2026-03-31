"""
RLM Agents Package.

This package provides specialized agent implementations for the RLM system,
including verification agents and swarm agents that can spawn sub-agents.
"""

from rlm.agents.base.base_agent import BaseAgent, AgentConfig, AgentStatus
from rlm.agents.base.swarm_agent import SwarmAgent, SwarmRLM
from rlm.agents.executor import RLMExecutor
from rlm.agents.manager import AgentManager

__all__ = [
    # Base
    "BaseAgent",
    "AgentConfig",
    "AgentStatus",
    # Swarm
    "SwarmAgent",
    "SwarmRLM",
    # Executor & Manager
    "RLMExecutor",
    "AgentManager",
]
