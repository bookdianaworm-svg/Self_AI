"""
Orchestrator for the Self_AI Application Runtime.

The Orchestrator is the central coordinator that:
- Manages the Redux store lifecycle
- Spawns and monitors agents
- Handles task routing
- Coordinates system state

This module provides the base orchestrator that will be extended
in later phases to support full multi-agent orchestration.
"""

import asyncio
import signal
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Callable

from rlm.app.logging_config import get_logger
from rlm.redux.store import ReduxStore

logger = get_logger("orchestrator")


class SystemStatus(Enum):
    """System status states."""

    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class OrchestratorConfig:
    """Configuration for the orchestrator."""

    log_level: str = "INFO"
    log_file: Optional[str] = None
    auto_save_interval: int = 30
    max_concurrent_agents: int = 10
    enable_message_bus: bool = True


class Orchestrator:
    """
    Central orchestrator for the Self_AI swarm system.

    The orchestrator manages:
    - System lifecycle (start, stop, pause, resume)
    - Redux store access
    - Agent creation and management (Phase 2+)
    - Task routing and execution (Phase 2+)
    - Message bus coordination (Phase 3+)

    Attributes:
        status: Current system status
        config: Orchestrator configuration
        store: Redux store instance

    Example:
        orchestrator = Orchestrator()
        orchestrator.start()
        # System is now running
        orchestrator.stop()
    """

    def __init__(
        self,
        store: Optional[ReduxStore] = None,
        config: Optional[OrchestratorConfig] = None,
    ):
        """
        Initialize the orchestrator.

        Args:
            store: Redux store instance. If None, creates a new one.
            config: Orchestrator configuration. If None, uses defaults.
        """
        self.config = config or OrchestratorConfig()
        self.store = store
        self._status = SystemStatus.IDLE

        self._running = False
        self._shutdown_event = asyncio.Event()
        self._subscribers: List[Callable[[SystemStatus], None]] = []

        logger.info("Orchestrator initialized")
        logger.debug(f"Configuration: {self.config}")

    @property
    def status(self) -> SystemStatus:
        """Get current system status."""
        return self._status

    def _set_status(self, status: SystemStatus) -> None:
        """Set status and notify subscribers."""
        old_status = self._status
        self._status = status
        logger.info(f"System status changed: {old_status.value} -> {status.value}")
        for callback in self._subscribers:
            try:
                callback(status)
            except Exception as e:
                logger.error(f"Error in status subscriber: {e}")

    def subscribe_status(self, callback: Callable[[SystemStatus], None]) -> None:
        """
        Subscribe to status changes.

        Args:
            callback: Function to call when status changes
        """
        self._subscribers.append(callback)

    def unsubscribe_status(self, callback: Callable[[SystemStatus], None]) -> None:
        """Unsubscribe from status changes."""
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def start(self) -> None:
        """
        Start the orchestrator and all subsystems.

        This method initializes the Redux store if not provided,
        sets up signal handlers, and transitions the system to RUNNING state.

        Raises:
            RuntimeError: If system is already running or in error state
        """
        if self._status == SystemStatus.RUNNING:
            raise RuntimeError("System is already running")
        if self._status == SystemStatus.ERROR:
            raise RuntimeError("System is in error state. Reset before starting.")

        logger.info("Starting Self-AI Swarm System...")
        self._set_status(SystemStatus.STARTING)

        try:
            if self.store is None:
                from rlm.redux.store import create_store

                self.store = create_store()
                logger.info("Redux store created")

            self._running = True
            self._set_status(SystemStatus.RUNNING)
            logger.info("Self-AI Swarm System started successfully")

        except Exception as e:
            logger.error(f"Failed to start system: {e}")
            self._set_status(SystemStatus.ERROR)
            raise

    def stop(self) -> None:
        """
        Stop the orchestrator and all subsystems gracefully.

        This method:
        1. Sets status to STOPPING
        2. Signals all subsystems to stop
        3. Waits for cleanup to complete
        4. Sets status to STOPPED

        Raises:
            RuntimeError: If system is not running
        """
        if self._status != SystemStatus.RUNNING and self._status != SystemStatus.PAUSED:
            raise RuntimeError(f"System is not running (status: {self._status.value})")

        logger.info("Stopping Self-AI Swarm System...")
        self._set_status(SystemStatus.STOPPING)

        try:
            self._running = False
            self._shutdown_event.set()

            logger.info("System shutdown complete")
            self._set_status(SystemStatus.STOPPED)

        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            self._set_status(SystemStatus.ERROR)
            raise

    def pause(self) -> None:
        """
        Pause the system, stopping all active agents and tasks.

        The system can be resumed with resume().

        Raises:
            RuntimeError: If system is not running
        """
        if self._status != SystemStatus.RUNNING:
            raise RuntimeError(f"System is not running (status: {self._status.value})")

        logger.info("Pausing Self-AI Swarm System...")
        self._set_status(SystemStatus.PAUSED)

    def resume(self) -> None:
        """
        Resume the system from a paused state.

        Raises:
            RuntimeError: If system is not paused
        """
        if self._status != SystemStatus.PAUSED:
            raise RuntimeError(f"System is not paused (status: {self._status.value})")

        logger.info("Resuming Self-AI Swarm System...")
        self._set_status(SystemStatus.RUNNING)

    async def run_async(self) -> None:
        """
        Run the orchestrator's async event loop.

        This method runs until stop() is called or a shutdown signal is received.
        It handles:
        - Graceful shutdown on SIGINT/SIGTERM
        - Periodic tasks (auto-save, health checks)
        - Event processing

        Usage:
            orchestrator = Orchestrator()
            orchestrator.start()
            await orchestrator.run_async()
        """
        loop = asyncio.get_event_loop()

        shutdown_requested = asyncio.Event()

        def signal_handler():
            logger.info("Shutdown signal received")
            shutdown_requested.set()

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, signal_handler)
            except NotImplementedError:
                pass

        logger.info("Event loop started")

        while self._running and not shutdown_requested.is_set():
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break

        logger.info("Event loop exiting")

    def get_state(self) -> Dict[str, Any]:
        """
        Get the current system state as a dictionary.

        Returns:
            Dictionary containing system status and key metrics
        """
        return {
            "status": self._status.value,
            "running": self._running,
            "store_initialized": self.store is not None,
        }

    def __repr__(self) -> str:
        return f"Orchestrator(status={self._status.value}, running={self._running})"
