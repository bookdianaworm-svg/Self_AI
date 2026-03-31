"""
Persistence manager for multiple namespaces.

Manages storage across different namespaces like tasks,
workflows, improvements, and agents.
"""

from typing import Any, Dict, List, Optional

from rlm.persistence.base import StorageBackend
from rlm.persistence.json_storage import JSONFileStorage


class PersistenceManager:
    """
    Manages multiple storage namespaces.

    Each namespace corresponds to a separate storage directory,
    allowing logical separation of different data types.
    """

    DEFAULT_NAMESPACES = ["tasks", "workflows", "improvements", "agents"]

    def __init__(self, storage_dir: str):
        """
        Initialize persistence manager.

        Args:
            storage_dir: Base directory for all storage.
        """
        self._base_dir = storage_dir
        self._storages: Dict[str, StorageBackend] = {}
        self._init_default_namespaces()

    def _init_default_namespaces(self) -> None:
        """Initialize default namespace storages."""
        for namespace in self.DEFAULT_NAMESPACES:
            self.get_storage(namespace)

    def get_storage(self, namespace: str) -> StorageBackend:
        """
        Get or create storage for a namespace.

        Args:
            namespace: Name of the namespace.

        Returns:
            StorageBackend for the namespace.
        """
        if namespace not in self._storages:
            namespace_dir = f"{self._base_dir}/{namespace}"
            self._storages[namespace] = JSONFileStorage(namespace_dir)
        return self._storages[namespace]

    def save_state(self, namespace: str, key: str, data: Dict[str, Any]) -> None:
        """
        Save state to a namespace.

        Args:
            namespace: Namespace to save to.
            key: Unique identifier for the data.
            data: Dictionary of data to save.

        Raises:
            Exception: If save fails.
        """
        storage = self.get_storage(namespace)
        storage.save(key, data)

    def load_state(self, namespace: str, key: str) -> Optional[Dict[str, Any]]:
        """
        Load state from a namespace.

        Args:
            namespace: Namespace to load from.
            key: Unique identifier for the data.

        Returns:
            Dictionary of data if found, None otherwise.
        """
        storage = self.get_storage(namespace)
        return storage.load(key)

    def list_state_keys(
        self, namespace: str, prefix: Optional[str] = None
    ) -> List[str]:
        """
        List keys in a namespace.

        Args:
            namespace: Namespace to list from.
            prefix: Optional prefix to filter keys.

        Returns:
            List of keys matching the filter.
        """
        storage = self.get_storage(namespace)
        return storage.list_keys(prefix)

    def delete_state(self, namespace: str, key: str) -> bool:
        """
        Delete state from a namespace.

        Args:
            namespace: Namespace to delete from.
            key: Unique identifier for the data.

        Returns:
            True if deleted, False if not found.
        """
        storage = self.get_storage(namespace)
        return storage.delete(key)

    def namespace_exists(self, namespace: str) -> bool:
        """
        Check if a namespace has any data.

        Args:
            namespace: Namespace to check.

        Returns:
            True if namespace has data, False otherwise.
        """
        if namespace not in self._storages:
            return False
        return len(self._storages[namespace].list_keys()) > 0
