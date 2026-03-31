"""
Backend factory for dynamic backend client creation.
"""

from typing import Any, Dict

from rlm.clients import BaseLM, get_client
from rlm.core.types import ClientBackend


class BackendFactory:
    """
    Factory for creating backend clients dynamically based on routing decisions.
    """

    def __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None):
        """
        Initialize backend factory with backend configurations.

        Args:
            backend_configs: Mapping of backend_id to configuration kwargs
        """
        self.backend_configs = backend_configs or {}

    def get_backend(
        self,
        backend_id: str,
        default_kwargs: Dict[str, Any] | None = None
    ) -> BaseLM:
        """
        Get a backend client instance.

        Args:
            backend_id: Identifier of the backend to create
            default_kwargs: Default kwargs to use if not in config

        Returns:
            BaseLM instance configured for the specified backend
        """
        # Get configuration for this backend
        config = self.backend_configs.get(backend_id, default_kwargs or {})

        # Map backend_id to ClientBackend type
        client_backend = self._map_to_client_backend(backend_id)

        # Create client
        return get_client(client_backend, **config)

    def _map_to_client_backend(self, backend_id: str) -> ClientBackend:
        """Map backend_id string to ClientBackend enum."""
        # This mapping should be configurable
        mapping = {
            "rlm_internal": "openai",
            "claude_agent": "anthropic",
            "openai_gpt": "openai",
            "gemini": "gemini",
            "portkey": "portkey",
            "litellm": "litellm",
            "minimax": "minimax"
        }
        return mapping.get(backend_id, "openai")
