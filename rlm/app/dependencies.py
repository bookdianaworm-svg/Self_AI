"""
Dependency Container for the Self_AI Application Runtime.

This module provides lazy initialization and singleton management
for all shared services in the application.
"""

from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from rlm.redux.store import ReduxStore
    from rlm.app.orchestrator import Orchestrator
    from rlm.app.message_bus import MessageBus


class DependencyContainer:
    """
    Singleton dependency container for lazy initialization of services.

    Services are created on first access and cached for subsequent access.
    This avoids creating expensive resources until they are actually needed.

    Usage:
        container = DependencyContainer()

        # First access creates the instance
        store = container.store

        # Subsequent access returns cached instance
        store2 = container.store
        assert store is store2  # Same instance
    """

    _instance: Optional["DependencyContainer"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self._store: Optional["ReduxStore"] = None
        self._orchestrator: Optional["Orchestrator"] = None
        self._message_bus: Optional["MessageBus"] = None
        self._services: Dict[str, Any] = {}

    @property
    def store(self) -> "ReduxStore":
        """Get or create the Redux store instance."""
        if self._store is None:
            from rlm.redux.store import create_store

            self._store = create_store()
        return self._store

    @property
    def orchestrator(self) -> "Orchestrator":
        """Get or create the orchestrator instance."""
        if self._orchestrator is None:
            from rlm.app.orchestrator import Orchestrator

            self._orchestrator = Orchestrator(store=self.store)
        return self._orchestrator

    @property
    def message_bus(self) -> "MessageBus":
        """Get or create the message bus instance."""
        if self._message_bus is None:
            from rlm.app.message_bus import MessageBus

            self._message_bus = MessageBus()
        return self._message_bus

    def register_service(self, name: str, service: Any) -> None:
        """
        Register a custom service in the container.

        Args:
            name: Service identifier
            service: Service instance
        """
        self._services[name] = service

    def get_service(self, name: str) -> Optional[Any]:
        """
        Get a registered service by name.

        Args:
            name: Service identifier

        Returns:
            Service instance or None if not registered
        """
        return self._services.get(name)

    def has_service(self, name: str) -> bool:
        """Check if a service is registered."""
        return name in self._services

    def reset(self) -> None:
        """
        Reset the container, clearing all cached instances.

        Primarily used for testing.
        """
        self._store = None
        self._orchestrator = None
        self._message_bus = None
        self._services.clear()


def get_container() -> DependencyContainer:
    """
    Get the global dependency container instance.

    Returns:
        The singleton DependencyContainer
    """
    return DependencyContainer()


def get_store() -> "ReduxStore":
    """Convenience function to get the store."""
    return get_container().store


def get_orchestrator() -> "Orchestrator":
    """Convenience function to get the orchestrator."""
    return get_container().orchestrator


def get_message_bus() -> "MessageBus":
    """Convenience function to get the message bus."""
    return get_container().message_bus
