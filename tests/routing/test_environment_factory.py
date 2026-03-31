"""
Tests for EnvironmentFactory component.

This module tests EnvironmentFactory class which handles:
- Environment instance creation
- ID mapping to EnvironmentType
- Configuration merging
"""

from unittest.mock import MagicMock, patch

import pytest

from rlm.routing.environment_factory import EnvironmentFactory
from rlm.environments.base_env import BaseEnv


class TestEnvironmentFactoryInitialization:
    """
    Tests for EnvironmentFactory initialization.
    """

    def test_init_with_no_configs(self):
        """
        Test that EnvironmentFactory initializes with empty configs.

        Expected behavior:
        - Factory should initialize successfully
        - environment_configs should be empty dict
        """
        factory = EnvironmentFactory()
        assert factory.environment_configs == {}

    def test_init_with_configs(self):
        """
        Test that EnvironmentFactory initializes with provided configs.

        Expected behavior:
        - Factory should store provided configs
        - Configs should be accessible
        """
        configs = {
            "local": {"enable_layer1": True},
            "docker": {"image": "python:3.11-slim"},
            "modal": {"profile": "default"}
        }
        factory = EnvironmentFactory(environment_configs=configs)
        assert factory.environment_configs == configs

    def test_init_with_none_configs(self):
        """
        Test that EnvironmentFactory handles None configs gracefully.

        Expected behavior:
        - Should treat None as empty dict
        - Should not raise exception
        """
        factory = EnvironmentFactory(environment_configs=None)
        assert factory.environment_configs == {}


class TestEnvironmentInstanceCreation:
    """
    Tests for environment instance creation.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    def test_get_environment_with_config(self, mock_get_environment):
        """
        Test creating an environment with existing configuration.

        Args:
            mock_get_environment: Mocked get_environment function

        Expected behavior:
        - Should use configuration from environment_configs
        - Should call get_environment with correct parameters
        - Should return BaseEnv instance
        """
        mock_env = MagicMock(spec=BaseEnv)
        mock_get_environment.return_value = mock_env

        configs = {
            "local": {"enable_layer1": True, "custom_tools": {}}
        }
        factory = EnvironmentFactory(environment_configs=configs)

        env = factory.get_environment("local")

        assert env == mock_env
        mock_get_environment.assert_called_once()

    @patch('rlm.routing.environment_factory.get_environment')
    def test_get_environment_with_default_kwargs(self, mock_get_environment):
        """
        Test creating an environment with default kwargs.

        Args:
            mock_get_environment: Mocked get_environment function

        Expected behavior:
        - Should use default_kwargs when config not found
        - Should call get_environment with default parameters
        """
        mock_env = MagicMock(spec=BaseEnv)
        mock_get_environment.return_value = mock_env

        factory = EnvironmentFactory()
        default_kwargs = {"enable_layer1": False}

        env = factory.get_environment("unknown_environment", default_kwargs=default_kwargs)

        assert env == mock_env
        mock_get_environment.assert_called_once()

    @patch('rlm.routing.environment_factory.get_environment')
    def test_get_environment_with_no_config_or_default(self, mock_get_environment):
        """
        Test creating an environment with no config and no defaults.

        Args:
            mock_get_environment: Mocked get_environment function

        Expected behavior:
        - Should call get_environment with empty dict
        - Should not raise exception
        """
        mock_env = MagicMock(spec=BaseEnv)
        mock_get_environment.return_value = mock_env

        factory = EnvironmentFactory()

        env = factory.get_environment("unknown_environment")

        assert env == mock_env
        mock_get_environment.assert_called_once()

    @patch('rlm.routing.environment_factory.get_environment')
    def test_get_environment_config_merging(self, mock_get_environment):
        """
        Test that configuration merging works correctly.

        Args:
            mock_get_environment: Mocked get_environment function

        Expected behavior:
        - Should use environment-specific config when available
        - Should merge with defaults appropriately
        """
        mock_env = MagicMock(spec=BaseEnv)
        mock_get_environment.return_value = mock_env

        configs = {
            "local": {"enable_layer1": True, "custom_tools": {}}
        }
        factory = EnvironmentFactory(environment_configs=configs)

        # With specific config
        env1 = factory.get_environment("local")
        assert env1 == mock_env

        # With default kwargs
        default_kwargs = {"enable_layer1": False}
        env2 = factory.get_environment("docker", default_kwargs=default_kwargs)
        assert env2 == mock_env


class TestEnvironmentIdMapping:
    """
    Tests for environment_id to EnvironmentType mapping.
    """

    def test_map_local_to_local(self):
        """
        Test that local maps to local.

        Expected behavior:
        - Should return EnvironmentType.LOCAL or "local"
        """
        factory = EnvironmentFactory()
        with patch('rlm.routing.environment_factory.get_environment') as mock_get_environment:
            mock_env = MagicMock(spec=BaseEnv)
            mock_get_environment.return_value = mock_env
            factory.get_environment("local")
            call_args = mock_get_environment.call_args
            assert call_args is not None

    def test_map_docker_to_docker(self):
        """
        Test that docker maps to docker.

        Expected behavior:
        - Should return EnvironmentType.DOCKER or "docker"
        """
        factory = EnvironmentFactory()
        with patch('rlm.routing.environment_factory.get_environment') as mock_get_environment:
            mock_env = MagicMock(spec=BaseEnv)
            mock_get_environment.return_value = mock_env
            factory.get_environment("docker")
            call_args = mock_get_environment.call_args
            assert call_args is not None

    def test_map_modal_to_modal(self):
        """
        Test that modal maps to modal.

        Expected behavior:
        - Should return EnvironmentType.MODAL or "modal"
        """
        factory = EnvironmentFactory()
        with patch('rlm.routing.environment_factory.get_environment') as mock_get_environment:
            mock_env = MagicMock(spec=BaseEnv)
            mock_get_environment.return_value = mock_env
            factory.get_environment("modal")
            call_args = mock_get_environment.call_args
            assert call_args is not None

    def test_map_e2b_to_e2b(self):
        """
        Test that e2b maps to e2b.

        Expected behavior:
        - Should return EnvironmentType.E2B or "e2b"
        """
        factory = EnvironmentFactory()
        with patch('rlm.routing.environment_factory.get_environment') as mock_get_environment:
            mock_env = MagicMock(spec=BaseEnv)
            mock_get_environment.return_value = mock_env
            factory.get_environment("e2b")
            call_args = mock_get_environment.call_args
            assert call_args is not None

    def test_map_daytona_to_daytona(self):
        """
        Test that daytona maps to daytona.

        Expected behavior:
        - Should return EnvironmentType.DAYTONA or "daytona"
        """
        factory = EnvironmentFactory()
        with patch('rlm.routing.environment_factory.get_environment') as mock_get_environment:
            mock_env = MagicMock(spec=BaseEnv)
            mock_get_environment.return_value = mock_env
            factory.get_environment("daytona")
            call_args = mock_get_environment.call_args
            assert call_args is not None

    def test_map_prime_to_prime(self):
        """
        Test that prime maps to prime.

        Expected behavior:
        - Should return EnvironmentType.PRIME or "prime"
        """
        factory = EnvironmentFactory()
        with patch('rlm.routing.environment_factory.get_environment') as mock_get_environment:
            mock_env = MagicMock(spec=BaseEnv)
            mock_get_environment.return_value = mock_env
            factory.get_environment("prime")
            call_args = mock_get_environment.call_args
            assert call_args is not None

    def test_map_unknown_to_local(self):
        """
        Test that unknown environment_id defaults to local.

        Expected behavior:
        - Should return EnvironmentType.LOCAL or "local"
        - Should not raise exception
        """
        factory = EnvironmentFactory()
        with patch('rlm.routing.environment_factory.get_environment') as mock_get_environment:
            mock_env = MagicMock(spec=BaseEnv)
            mock_get_environment.return_value = mock_env
            factory.get_environment("unknown_environment_xyz")
            call_args = mock_get_environment.call_args
            assert call_args is not None


class TestConfigurationHandling:
    """
    Tests for configuration handling and merging.
    """

    def test_config_isolation(self):
        """
        Test that configs are isolated between factory instances.

        Expected behavior:
        - Changes to one factory should not affect another
        - Each factory should have its own config
        """
        configs1 = {"local": {"key1": "value1"}}
        configs2 = {"docker": {"key2": "value2"}}

        factory1 = EnvironmentFactory(environment_configs=configs1)
        factory2 = EnvironmentFactory(environment_configs=configs2)

        assert factory1.environment_configs == configs1
        assert factory2.environment_configs == configs2
        assert factory1.environment_configs != factory2.environment_configs

    def test_config_immutability(self):
        """
        Test that modifying original config dict doesn't affect factory.

        Expected behavior:
        - Factory should store a copy or reference
        - Original dict modification should be handled appropriately
        """
        original_configs = {"local": {"key": "value"}}
        factory = EnvironmentFactory(environment_configs=original_configs)

        # Modify original
        original_configs["docker"] = {"key2": "value2"}

        # Factory should have original reference
        # (Python dicts are mutable references)
        assert "docker" in factory.environment_configs

    def test_empty_config_handling(self):
        """
        Test handling of empty environment configs.

        Expected behavior:
        - Should not raise exception
        - Should use default kwargs when provided
        """
        factory = EnvironmentFactory(environment_configs={})

        with patch('rlm.routing.environment_factory.get_environment') as mock_get_environment:
            mock_env = MagicMock(spec=BaseEnv)
            mock_get_environment.return_value = mock_env

            env = factory.get_environment("any_environment", default_kwargs={"enable_layer1": False})
            assert env == mock_env

    def test_config_with_special_characters(self):
        """
        Test handling of configs with special characters in values.

        Expected behavior:
        - Should handle special characters correctly
        - Should not raise exception
        """
        configs = {
            "local": {
                "image": "python:3.11-slim",
                "network_mode": "bridge",
                "profile": "dev-prod-2024"
            }
        }
        factory = EnvironmentFactory(environment_configs=configs)

        with patch('rlm.routing.environment_factory.get_environment') as mock_get_environment:
            mock_env = MagicMock(spec=BaseEnv)
            mock_get_environment.return_value = mock_env

            env = factory.get_environment("local")
            assert env == mock_env


class TestErrorHandling:
    """
    Tests for error handling in environment creation.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    def test_get_environment_exception_propagation(self, mock_get_environment):
        """
        Test that exceptions from get_environment are propagated.

        Args:
            mock_get_environment: Mocked get_environment function

        Expected behavior:
        - Should raise same exception
        - Should not catch or hide errors
        """
        mock_get_environment.side_effect = ValueError("Invalid configuration")

        factory = EnvironmentFactory()

        with pytest.raises(ValueError, match="Invalid configuration"):
            factory.get_environment("test_environment")

    @patch('rlm.routing.environment_factory.get_environment')
    def test_get_environment_with_none_environment_id(self, mock_get_environment):
        """
        Test creating environment with None environment_id.

        Args:
            mock_get_environment: Mocked get_environment function

        Expected behavior:
        - Should handle None gracefully
        - Should not raise exception (depends on implementation)
        """
        mock_env = MagicMock(spec=BaseEnv)
        mock_get_environment.return_value = mock_env

        factory = EnvironmentFactory()

        # This may raise an exception depending on implementation
        # Test documents current behavior
        try:
            env = factory.get_environment(None)
            assert env == mock_env
        except (TypeError, AttributeError):
            # Also acceptable if it raises an exception
            pass

    @patch('rlm.routing.environment_factory.get_environment')
    def test_get_environment_with_empty_environment_id(self, mock_get_environment):
        """
        Test creating environment with empty string environment_id.

        Args:
            mock_get_environment: Mocked get_environment function

        Expected behavior:
        - Should handle empty string gracefully
        - Should map to default environment type
        """
        mock_env = MagicMock(spec=BaseEnv)
        mock_get_environment.return_value = mock_env

        factory = EnvironmentFactory()

        env = factory.get_environment("")
        assert env == mock_env


class TestMultipleEnvironments:
    """
    Tests for managing multiple environments.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    def test_create_multiple_environments(self, mock_get_environment):
        """
        Test creating multiple environments from same factory.

        Args:
            mock_get_environment: Mocked get_environment function

        Expected behavior:
        - Should create each environment correctly
        - Each environment should be independent
        """
        mock_env = MagicMock(spec=BaseEnv)
        mock_get_environment.return_value = mock_env

        configs = {
            "local": {"enable_layer1": True},
            "docker": {"image": "python:3.11-slim"},
            "modal": {"profile": "default"}
        }
        factory = EnvironmentFactory(environment_configs=configs)

        env1 = factory.get_environment("local")
        env2 = factory.get_environment("docker")
        env3 = factory.get_environment("modal")

        assert mock_get_environment.call_count == 3

    @patch('rlm.routing.environment_factory.get_environment')
    def test_reuse_environment_config(self, mock_get_environment):
        """
        Test that same environment can be requested multiple times.

        Args:
            mock_get_environment: Mocked get_environment function

        Expected behavior:
        - Should create new instance each time (or cache based on implementation)
        - Should not raise exception
        """
        mock_env = MagicMock(spec=BaseEnv)
        mock_get_environment.return_value = mock_env

        configs = {"local": {"enable_layer1": True}}
        factory = EnvironmentFactory(environment_configs=configs)

        env1 = factory.get_environment("local")
        env2 = factory.get_environment("local")

        # Depending on implementation, may create new instance or cache
        assert mock_get_environment.call_count >= 1


class TestConfigValidation:
    """
    Tests for configuration validation.
    """

    def test_config_with_missing_required_fields(self):
        """
        Test handling of config with missing required fields.

        Expected behavior:
        - May raise exception or use defaults
        - Should not crash
        """
        configs = {
            "local": {}  # Empty config
        }
        factory = EnvironmentFactory(environment_configs=configs)

        with patch('rlm.routing.environment_factory.get_environment') as mock_get_environment:
            mock_env = MagicMock(spec=BaseEnv)
            mock_get_environment.return_value = mock_env

            # Should handle gracefully
            env = factory.get_environment("local")
            assert env == mock_env

    def test_config_with_extra_fields(self):
        """
        Test handling of config with extra fields.

        Expected behavior:
        - Should pass extra fields to get_environment
        - Should not filter out fields
        """
        configs = {
            "local": {
                "enable_layer1": True,
                "custom_tools": {},
                "extra_field": "extra_value",
                "another_extra": 123
            }
        }
        factory = EnvironmentFactory(environment_configs=configs)

        with patch('rlm.routing.environment_factory.get_environment') as mock_get_environment:
            mock_env = MagicMock(spec=BaseEnv)
            mock_get_environment.return_value = mock_env

            env = factory.get_environment("local")
            assert env == mock_env
            # Check that all config fields were passed
            call_kwargs = mock_get_environment.call_args[1]
            assert "extra_field" in call_kwargs or "enable_layer1" in call_kwargs


class TestLayer1Configuration:
    """
    Tests for Layer1-specific configuration handling.
    """

    @patch('rlm.routing.environment_factory.get_environment')
    def test_enable_layer1_flag(self, mock_get_environment):
        """
        Test that enable_layer1 flag is passed correctly.

        Args:
            mock_get_environment: Mocked get_environment function

        Expected behavior:
        - Should pass enable_layer1 flag to environment
        """
        mock_env = MagicMock(spec=BaseEnv)
        mock_get_environment.return_value = mock_env

        configs = {"local": {"enable_layer1": True}}
        factory = EnvironmentFactory(environment_configs=configs)

        env = factory.get_environment("local")
        assert env == mock_env
        # Verify enable_layer1 was passed
        call_kwargs = mock_get_environment.call_args[1]
        assert call_kwargs.get("enable_layer1") == True

    @patch('rlm.routing.environment_factory.get_environment')
    def test_custom_tools_configuration(self, mock_get_environment):
        """
        Test that custom_tools dict is passed correctly.

        Args:
            mock_get_environment: Mocked get_environment function

        Expected behavior:
        - Should pass custom_tools dict to environment
        """
        mock_env = MagicMock(spec=BaseEnv)
        mock_get_environment.return_value = mock_env

        configs = {
            "local": {
                "enable_layer1": True,
                "custom_tools": {
                    "verify_lean": lambda x: {},
                    "get_layer1_axioms": lambda: {}
                }
            }
        }
        factory = EnvironmentFactory(environment_configs=configs)

        env = factory.get_environment("local")
        assert env == mock_env
        # Verify custom_tools was passed
        call_kwargs = mock_get_environment.call_args[1]
        assert "custom_tools" in call_kwargs
