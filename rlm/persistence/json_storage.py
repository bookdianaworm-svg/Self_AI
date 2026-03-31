"""
JSON file storage implementation.

Provides atomic, thread-safe JSON file storage.
"""

import json
import os
import shutil
import tempfile
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from rlm.persistence.base import StorageBackend


class JSONParseError(Exception):
    """Raised when JSON parsing fails."""

    pass


class JSONFileStorage(StorageBackend):
    """
    JSON file-based storage backend.

    Stores each key as a separate .json file with atomic writes
    and thread-safe access.
    """

    def __init__(self, storage_dir: str):
        """
        Initialize JSON file storage.

        Args:
            storage_dir: Directory to store JSON files.
        """
        self._storage_dir = Path(storage_dir)
        self._lock = threading.Lock()
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        """Create storage directory if it doesn't exist."""
        self._storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, key: str) -> Path:
        """Get the file path for a key."""
        safe_key = key.replace("/", "_").replace("\\", "_").replace(":", "_")
        return self._storage_dir / f"{safe_key}.json"

    def save(self, key: str, data: Dict[str, Any]) -> None:
        """
        Save data atomically using temp file and rename.

        Args:
            key: Unique identifier for the data.
            data: Dictionary of data to save.

        Raises:
            JSONParseError: If data cannot be serialized.
        """
        with self._lock:
            file_path = self._get_file_path(key)
            temp_fd, temp_path = tempfile.mkstemp(
                dir=str(self._storage_dir), suffix=".json"
            )
            try:
                with os.fdopen(temp_fd, "w") as f:
                    json.dump(data, f, indent=2)
                shutil.move(temp_path, file_path)
            except (TypeError, ValueError) as e:
                os.unlink(temp_path)
                raise JSONParseError(f"Failed to serialize data: {e}")
            except Exception as e:
                os.unlink(temp_path)
                raise

    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Load data from file.

        Args:
            key: Unique identifier for the data.

        Returns:
            Dictionary of data if found, None otherwise.
        """
        with self._lock:
            file_path = self._get_file_path(key)
            if not file_path.exists():
                return None
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                return None
            except Exception:
                return None

    def delete(self, key: str) -> bool:
        """
        Delete data file.

        Args:
            key: Unique identifier for the data.

        Returns:
            True if deleted, False if not found.
        """
        with self._lock:
            file_path = self._get_file_path(key)
            if file_path.exists():
                file_path.unlink()
                return True
            return False

    def exists(self, key: str) -> bool:
        """
        Check if data file exists.

        Args:
            key: Unique identifier for the data.

        Returns:
            True if exists, False otherwise.
        """
        file_path = self._get_file_path(key)
        return file_path.exists()

    def list_keys(self, prefix: Optional[str] = None) -> List[str]:
        """
        List all keys, optionally filtered by prefix.

        Args:
            prefix: Optional prefix to filter keys.

        Returns:
            List of keys matching the filter.
        """
        with self._lock:
            keys = []
            for file_path in self._storage_dir.glob("*.json"):
                key = file_path.stem
                if prefix is None or key.startswith(prefix):
                    keys.append(key)
            return sorted(keys)
