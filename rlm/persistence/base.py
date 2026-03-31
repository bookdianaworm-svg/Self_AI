"""
Base storage backend abstract class.

Defines the interface for persistence backends.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    def save(self, key: str, data: Dict[str, Any]) -> None:
        """
        Save data for a given key.

        Args:
            key: Unique identifier for the data.
            data: Dictionary of data to save.

        Raises:
            Exception: If save fails.
        """
        pass

    @abstractmethod
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Load data for a given key.

        Args:
            key: Unique identifier for the data.

        Returns:
            Dictionary of data if found, None otherwise.
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        Delete data for a given key.

        Args:
            key: Unique identifier for the data.

        Returns:
            True if deleted, False if not found.
        """
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        Check if data exists for a given key.

        Args:
            key: Unique identifier for the data.

        Returns:
            True if exists, False otherwise.
        """
        pass

    @abstractmethod
    def list_keys(self, prefix: Optional[str] = None) -> List[str]:
        """
        List all keys, optionally filtered by prefix.

        Args:
            prefix: Optional prefix to filter keys.

        Returns:
            List of keys matching the filter.
        """
        pass
