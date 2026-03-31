"""
Self_AI Application Runtime

This module contains the application layer that orchestrates the RLM core,
Redux store, and agent management into a functioning swarm system.

Architecture:
- app.py: Application entry point with event loop
- orchestrator.py: Central coordinator for agents and tasks
- agent_manager.py: Manages agent lifecycle
- message_bus.py: Inter-agent communication
- ws_bridge.py: WebSocket bridge to UI
"""

from rlm.app.dependencies import DependencyContainer
from rlm.app.logging_config import setup_logging

__all__ = [
    "DependencyContainer",
    "setup_logging",
]
