"""
Persistence layer for RLM system.

This module provides file-based JSON persistence for tasks,
workflows, messages, and agent states.
"""

from rlm.persistence.base import StorageBackend
from rlm.persistence.json_storage import JSONFileStorage
from rlm.persistence.manager import PersistenceManager

__all__ = [
    "StorageBackend",
    "JSONFileStorage",
    "PersistenceManager",
]
