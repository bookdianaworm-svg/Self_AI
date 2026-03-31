"""
Tests for JSONFileStorage class.
"""

import json
import os
import pytest

from rlm.persistence.json_storage import JSONFileStorage, JSONParseError


class TestJSONFileStorage:
    """Test suite for JSONFileStorage class."""

    def test_save_and_load(self, tmp_path):
        """Save a simple dictionary and load it back."""
        storage = JSONFileStorage(str(tmp_path))
        data = {"key": "value", "number": 42}

        storage.save("test_key", data)
        loaded = storage.load("test_key")

        assert loaded == data
        assert loaded["key"] == "value"
        assert loaded["number"] == 42

    def test_save_nested_data(self, tmp_path):
        """Test saving and loading nested dictionaries and lists."""
        storage = JSONFileStorage(str(tmp_path))
        data = {
            "nested": {"inner": "value"},
            "list": [1, 2, 3],
            "mixed": {"items": [{"a": 1}, {"b": 2}]},
        }

        storage.save("nested_key", data)
        loaded = storage.load("nested_key")

        assert loaded == data
        assert loaded["nested"]["inner"] == "value"
        assert loaded["list"] == [1, 2, 3]
        assert len(loaded["mixed"]["items"]) == 2

    def test_load_nonexistent_returns_none(self, tmp_path):
        """Loading a nonexistent key should return None."""
        storage = JSONFileStorage(str(tmp_path))

        result = storage.load("nonexistent_key")

        assert result is None

    def test_delete(self, tmp_path):
        """Save data, delete it, and verify it's gone."""
        storage = JSONFileStorage(str(tmp_path))
        data = {"key": "value"}

        storage.save("to_delete", data)
        assert storage.exists("to_delete") is True

        result = storage.delete("to_delete")
        assert result is True
        assert storage.exists("to_delete") is False

        loaded = storage.load("to_delete")
        assert loaded is None

    def test_delete_nonexistent(self, tmp_path):
        """Deleting a nonexistent key should return False."""
        storage = JSONFileStorage(str(tmp_path))

        result = storage.delete("nonexistent")

        assert result is False

    def test_exists(self, tmp_path):
        """Test exists() returns correct values before and after save."""
        storage = JSONFileStorage(str(tmp_path))

        assert storage.exists("test_key") is False

        storage.save("test_key", {"data": "value"})

        assert storage.exists("test_key") is True

    def test_list_keys(self, tmp_path):
        """Test listing keys with optional prefix filtering."""
        storage = JSONFileStorage(str(tmp_path))

        storage.save("task_1", {"data": 1})
        storage.save("task_2", {"data": 2})
        storage.save("workflow_1", {"data": 3})
        storage.save("other_key", {"data": 4})

        all_keys = storage.list_keys()
        assert len(all_keys) == 4
        assert "task_1" in all_keys
        assert "task_2" in all_keys
        assert "workflow_1" in all_keys
        assert "other_key" in all_keys

        task_keys = storage.list_keys(prefix="task_")
        assert len(task_keys) == 2
        assert "task_1" in task_keys
        assert "task_2" in task_keys

        workflow_keys = storage.list_keys(prefix="workflow_")
        assert len(workflow_keys) == 1
        assert "workflow_1" in workflow_keys

    def test_atomic_write(self, tmp_path):
        """Verify atomic write creates proper file after save."""
        storage = JSONFileStorage(str(tmp_path))
        data = {"atomic": "test"}

        storage.save("atomic_key", data)

        file_path = tmp_path / "atomic_key.json"
        assert file_path.exists()

        with open(file_path, "r") as f:
            loaded_data = json.load(f)

        assert loaded_data == data

    def test_corrupted_json_returns_none(self, tmp_path):
        """Handle corrupted JSON files gracefully by returning None."""
        storage = JSONFileStorage(str(tmp_path))

        file_path = tmp_path / "corrupted_key.json"
        with open(file_path, "w") as f:
            f.write("{ invalid json content }")

        result = storage.load("corrupted_key")

        assert result is None

    def test_overwrite_existing_key(self, tmp_path):
        """Overwriting an existing key should replace the data."""
        storage = JSONFileStorage(str(tmp_path))

        storage.save("same_key", {"version": 1})
        loaded_v1 = storage.load("same_key")
        assert loaded_v1["version"] == 1

        storage.save("same_key", {"version": 2})
        loaded_v2 = storage.load("same_key")
        assert loaded_v2["version"] == 2

    def test_empty_dict_save(self, tmp_path):
        """Saving an empty dictionary should work correctly."""
        storage = JSONFileStorage(str(tmp_path))

        storage.save("empty", {})
        loaded = storage.load("empty")

        assert loaded == {}

    def test_special_characters_in_key(self, tmp_path):
        """Keys with special characters should be handled."""
        storage = JSONFileStorage(str(tmp_path))

        storage.save("key/with/slashes", {"data": "value"})
        storage.save("key:with:colons", {"data": "value2"})

        keys = storage.list_keys()
        assert "key_with_slashes" in keys
        assert "key_with_colons" in keys
