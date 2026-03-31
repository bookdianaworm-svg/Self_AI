"""
Tests for PersistenceManager class.
"""

import pytest

from rlm.persistence.manager import PersistenceManager


class TestPersistenceManager:
    """Test suite for PersistenceManager class."""

    def test_get_storage_creates_namespace(self, tmp_path):
        """Getting storage for a namespace creates it if it doesn't exist."""
        manager = PersistenceManager(str(tmp_path))

        storage1 = manager.get_storage("new_namespace")
        storage2 = manager.get_storage("new_namespace")

        assert storage1 is storage2

    def test_save_and_load_state(self, tmp_path):
        """Test saving and loading state through the manager."""
        manager = PersistenceManager(str(tmp_path))

        task_data = {
            "id": "task_1",
            "description": "Test task",
            "priority": 2,
        }

        manager.save_state("tasks", "task_1", task_data)
        loaded = manager.load_state("tasks", "task_1")

        assert loaded == task_data
        assert loaded["id"] == "task_1"

    def test_list_state_keys(self, tmp_path):
        """Test listing state keys in a namespace."""
        manager = PersistenceManager(str(tmp_path))

        manager.save_state("tasks", "task_1", {"id": "1"})
        manager.save_state("tasks", "task_2", {"id": "2"})
        manager.save_state("workflows", "wf_1", {"id": "w1"})

        task_keys = manager.list_state_keys("tasks")
        assert len(task_keys) == 2
        assert "task_1" in task_keys
        assert "task_2" in task_keys

        workflow_keys = manager.list_state_keys("workflows")
        assert len(workflow_keys) == 1
        assert "wf_1" in workflow_keys

    def test_list_state_keys_with_prefix(self, tmp_path):
        """Test listing state keys with prefix filter."""
        manager = PersistenceManager(str(tmp_path))

        manager.save_state("tasks", "task_high_1", {"priority": 3})
        manager.save_state("tasks", "task_high_2", {"priority": 3})
        manager.save_state("tasks", "task_low_1", {"priority": 1})

        high_priority = manager.list_state_keys("tasks", prefix="task_high_")
        assert len(high_priority) == 2
        assert "task_high_1" in high_priority
        assert "task_high_2" in high_priority

    def test_isolated_namespaces(self, tmp_path):
        """Different namespaces should not interfere with each other."""
        manager = PersistenceManager(str(tmp_path))

        manager.save_state("namespace_a", "key_1", {"value": "a"})
        manager.save_state("namespace_b", "key_1", {"value": "b"})

        loaded_a = manager.load_state("namespace_a", "key_1")
        loaded_b = manager.load_state("namespace_b", "key_1")

        assert loaded_a["value"] == "a"
        assert loaded_b["value"] == "b"

        keys_a = manager.list_state_keys("namespace_a")
        keys_b = manager.list_state_keys("namespace_b")

        assert len(keys_a) == 1
        assert len(keys_b) == 1
        assert "key_1" in keys_a
        assert "key_1" in keys_b

    def test_delete_state(self, tmp_path):
        """Test deleting state from a namespace."""
        manager = PersistenceManager(str(tmp_path))

        manager.save_state("tasks", "to_delete", {"id": "delete_me"})
        assert manager.load_state("tasks", "to_delete") is not None

        result = manager.delete_state("tasks", "to_delete")
        assert result is True
        assert manager.load_state("tasks", "to_delete") is None

    def test_delete_state_nonexistent(self, tmp_path):
        """Deleting nonexistent state should return False."""
        manager = PersistenceManager(str(tmp_path))

        result = manager.delete_state("tasks", "nonexistent")
        assert result is False

    def test_load_nonexistent_returns_none(self, tmp_path):
        """Loading nonexistent key should return None."""
        manager = PersistenceManager(str(tmp_path))

        result = manager.load_state("tasks", "nonexistent")
        assert result is None

    def test_default_namespaces_initialized(self, tmp_path):
        """Default namespaces should be initialized."""
        manager = PersistenceManager(str(tmp_path))

        for namespace in ["tasks", "workflows", "improvements", "agents"]:
            storage = manager.get_storage(namespace)
            assert storage is not None

    def test_namespace_exists(self, tmp_path):
        """Test namespace_exists method."""
        manager = PersistenceManager(str(tmp_path))

        assert manager.namespace_exists("tasks") is False

        manager.save_state("tasks", "task_1", {"id": "1"})

        assert manager.namespace_exists("tasks") is True
