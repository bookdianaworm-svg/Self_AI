"""PostgREST client for task_knowledge table."""

import os
import threading
from typing import Any, Dict, List, Optional

import requests


class TaskKnowledgeStorage:
    """Supabase-backed task knowledge storage via PostgREST API."""

    def __init__(
        self,
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None,
    ):
        self.supabase_url = supabase_url or os.environ.get("SUPABASE_URL")
        anon_key = supabase_key or os.environ.get("SUPABASE_ANON_KEY")
        self.enabled = bool(self.supabase_url) and bool(anon_key)
        self._headers: Dict[str, str] = {
            "apikey": anon_key or "",
            "Authorization": f"Bearer {anon_key}" if anon_key else "",
            "Content-Type": "application/json",
        }
        self._lock = threading.Lock()

    def _post(self, table: str, data: Dict[str, Any]) -> requests.Response:
        """Execute a POST request to PostgREST."""
        url = f"{self.supabase_url}/rest/v1/{table}"
        return requests.post(
            url,
            headers={**self._headers, "Prefer": "resolution=merge-duplicates"},
            json=data,
            timeout=30,
        )

    def _get(
        self,
        table: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Execute a GET request to PostgREST."""
        url = f"{self.supabase_url}/rest/v1/{table}"
        resp = requests.get(
            url,
            headers=self._headers,
            params=params,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json() or []

    def save(self, knowledge: Dict[str, Any]) -> str:
        """Upsert a knowledge entry and return its knowledge_id.

        Args:
            knowledge: Dict containing task knowledge fields.
                Required: fingerprint
                Optional: task_type, content, embedding, success_pattern,
                          failure_pattern, metadata

        Returns:
            The knowledge_id of the saved entry.
        """
        if not self.enabled:
            return ""

        with self._lock:
            resp = self._post(
                "task_knowledge",
                {
                    "fingerprint": knowledge.get("fingerprint"),
                    "task_type": knowledge.get("task_type"),
                    "content": knowledge.get("content"),
                    "embedding": knowledge.get("embedding"),
                    "success_pattern": knowledge.get("success_pattern"),
                    "failure_pattern": knowledge.get("failure_pattern"),
                    "metadata": knowledge.get("metadata"),
                },
            )
            resp.raise_for_status()
            # PostgREST returns Location header with the primary key
            location = resp.headers.get("Location", "")
            # Extract knowledge_id from Location header (e.g., /task_knowledge?knowledge_id=eq.123)
            if location:
                for part in location.split("&"):
                    if "knowledge_id" in part:
                        return part.split("eq.")[-1]
            return ""

    def find_similar(
        self,
        fingerprint: str,
        threshold: float = 0.7,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Find similar knowledge entries by fingerprint.

        Args:
            fingerprint: The fingerprint to search for.
            threshold: Similarity threshold (0.0-1.0).
            limit: Maximum number of results.

        Returns:
            List of matching knowledge entries.
        """
        if not self.enabled:
            return []

        params: Dict[str, Any] = {
            "fingerprint": f"eq.{fingerprint}",
            "limit": str(limit),
            "order": "created_at.desc",
        }
        with self._lock:
            return self._get("task_knowledge", params)

    def get_for_task_type(self, task_type: str) -> List[Dict[str, Any]]:
        """Get all knowledge entries for a specific task type.

        Args:
            task_type: The task type to filter by.

        Returns:
            List of knowledge entries for the task type.
        """
        if not self.enabled:
            return []

        params: Dict[str, Any] = {
            "task_type": f"eq.{task_type}",
            "order": "created_at.desc",
        }
        with self._lock:
            return self._get("task_knowledge", params)

    def get_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent knowledge entries.

        Args:
            limit: Maximum number of results (default 50).

        Returns:
            List of recent knowledge entries.
        """
        if not self.enabled:
            return []

        params: Dict[str, Any] = {
            "limit": str(limit),
            "order": "created_at.desc",
        }
        with self._lock:
            return self._get("task_knowledge", params)
