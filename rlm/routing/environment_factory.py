"""
Environment factory for dynamic environment creation.
"""

from typing import Any, Dict

from rlm.environments import BaseEnv, get_environment
from rlm.core.types import EnvironmentType


class EnvironmentFactory:
    """
    Factory for creating environment instances dynamically based on routing decisions.
    """

    def __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None):
        """
        Initialize environment factory with environment configurations.

        Args:
            environment_configs: Mapping of environment_id to configuration kwargs
        """
        self.environment_configs = environment_configs or {}

    def get_environment(
        self,
        environment_id: str,
        default_kwargs: Dict[str, Any] | None = None
    ) -> BaseEnv:
        """
        Get an environment instance.

        Args:
            environment_id: Identifier of the environment to create
            default_kwargs: Default kwargs to use if not in config

        Returns:
            BaseEnv instance configured for the specified environment
        """
        # Get configuration for this environment
        config = self.environment_configs.get(environment_id, default_kwargs or {})

        # Map environment_id to EnvironmentType
        env_type = self._map_to_environment_type(environment_id)

        # Create environment
        return get_environment(env_type, **config)

    def _map_to_environment_type(self, environment_id: str) -> EnvironmentType:
        """Map environment_id string to EnvironmentType."""
        mapping = {
            "local": "local",
            "docker": "docker",
            "modal": "modal",
            "e2b": "e2b",
            "daytona": "daytona",
            "prime": "prime"
        }
        return mapping.get(environment_id, "local")
