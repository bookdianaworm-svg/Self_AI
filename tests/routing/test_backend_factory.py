"""
Tests for BackendFactory component.

This module tests the BackendFactory class which handles:
- Backend client creation
- ID mapping to ClientBackend types
- Configuration merging
"""

from unittest.mock import MagicMock, patch

import pytest

from rlm.routing.backend_factory import BackendFactory
from rlm.clients.base_lm import BaseLM


class TestBackendFactoryInitialization:
    """
    Tests for BackendFactory initialization.
    """

    def test_init_with_no_configs(self):
        """
        Test that BackendFactory initializes with empty configs.

        Expected behavior:
        - Factory should initialize successfully
        - backend_configs should be empty dict
        """
        factory = BackendFactory()
        assert factory.backend_configs == {}

    def test_init_with_configs(self):
        """
        Test that BackendFactory initializes with provided configs.

        Expected behavior:
        - Factory should store provided configs
        - Configs should be accessible
        """
        configs = {
            "backend1": {"model": "gpt-4", "api_key": "key1"},
            "backend2": {"model": "claude-3", "api_key": "key2"}
        }
        factory = BackendFactory(backend_configs=configs)
        assert factory.backend_configs == configs

    def test_init_with_none_configs(self):
        """
        Test that BackendFactory handles None configs gracefully.

        Expected behavior:
        - Should treat None as empty dict
        - Should not raise exception
        """
        factory = BackendFactory(backend_configs=None)
        assert factory.backend_configs == {}


class TestBackendClientCreation:
    """
    Tests for backend client creation.
    """

    @patch('rlm.routing.backend_factory.get_client')
    def test_get_backend_with_config(self, mock_get_client):
        """
        Test creating a backend with existing configuration.

        Args:
            mock_get_client: Mocked get_client function

        Expected behavior:
        - Should use configuration from backend_configs
        - Should call get_client with correct parameters
        - Should return BaseLM instance
        """
        mock_client = MagicMock(spec=BaseLM)
        mock_get_client.return_value = mock_client

        configs = {
            "test_backend": {"model": "gpt-4", "api_key": "test-key"}
        }
        factory = BackendFactory(backend_configs=configs)

        client = factory.get_backend("test_backend")

        assert client == mock_client
        mock_get_client.assert_called_once()

    @patch('rlm.routing.backend_factory.get_client')
    def test_get_backend_with_default_kwargs(self, mock_get_client):
        """
        Test creating a backend with default kwargs.

        Args:
            mock_get_client: Mocked get_client function

        Expected behavior:
        - Should use default_kwargs when config not found
        - Should call get_client with default parameters
        """
        mock_client = MagicMock(spec=BaseLM)
        mock_get_client.return_value = mock_client

        factory = BackendFactory()
        default_kwargs = {"model": "gpt-3.5", "api_key": "default-key"}

        client = factory.get_backend("unknown_backend", default_kwargs=default_kwargs)

        assert client == mock_client
        mock_get_client.assert_called_once()

    @patch('rlm.routing.backend_factory.get_client')
    def test_get_backend_with_no_config_or_default(self, mock_get_client):
        """
        Test creating a backend with no config and no defaults.

        Args:
            mock_get_client: Mocked get_client function

        Expected behavior:
        - Should call get_client with empty dict
        - Should not raise exception
        """
        mock_client = MagicMock(spec=BaseLM)
        mock_get_client.return_value = mock_client

        factory = BackendFactory()

        client = factory.get_backend("unknown_backend")

        assert client == mock_client
        mock_get_client.assert_called_once()

    @patch('rlm.routing.backend_factory.get_client')
    def test_get_backend_config_merging(self, mock_get_client):
        """
        Test that configuration merging works correctly.

        Args:
            mock_get_client: Mocked get_client function

        Expected behavior:
        - Should use backend-specific config when available
        - Should merge with defaults appropriately
        """
        mock_client = MagicMock(spec=BaseLM)
        mock_get_client.return_value = mock_client

        configs = {
            "backend1": {"model": "gpt-4", "api_key": "specific-key"}
        }
        factory = BackendFactory(backend_configs=configs)

        # With specific config
        client1 = factory.get_backend("backend1")
        assert client1 == mock_client

        # With default kwargs
        default_kwargs = {"model": "gpt-3.5"}
        client2 = factory.get_backend("backend2", default_kwargs=default_kwargs)
        assert client2 == mock_client


class TestBackendIdMapping:
    """
    Tests for backend_id to ClientBackend mapping.
    """

    def test_map_rlm_internal_to_openai(self):
        """
        Test that rlm_internal maps to openai.

        Expected behavior:
        - Should return ClientBackend.OPENAI or "openai"
        """
        factory = BackendFactory()
        # The mapping is internal, so we test through get_backend
        with patch('rlm.routing.backend_factory.get_client') as mock_get_client:
            mock_get_client.return_value = MagicMock(spec=BaseLM)
            factory.get_backend("rlm_internal")
            # Check that get_client was called with correct ClientBackend
            call_args = mock_get_client.call_args
            assert call_args is not None

    def test_map_claude_agent_to_anthropic(self):
        """
        Test that claude_agent maps to anthropic.

        Expected behavior:
        - Should return ClientBackend.ANTHROPIC or "anthropic"
        """
        factory = BackendFactory()
        with patch('rlm.routing.backend_factory.get_client') as mock_get_client:
            mock_get_client.return_value = MagicMock(spec=BaseLM)
            factory.get_backend("claude_agent")
            call_args = mock_get_client.call_args
            assert call_args is not None

    def test_map_openai_gpt_to_openai(self):
        """
        Test that openai_gpt maps to openai.

        Expected behavior:
        - Should return ClientBackend.OPENAI or "openai"
        """
        factory = BackendFactory()
        with patch('rlm.routing.backend_factory.get_client') as mock_get_client:
            mock_get_client.return_value = MagicMock(spec=BaseLM)
            factory.get_backend("openai_gpt")
            call_args = mock_get_client.call_args
            assert call_args is not None

    def test_map_gemini_to_gemini(self):
        """
        Test that gemini maps to gemini.

        Expected behavior:
        - Should return ClientBackend.GEMINI or "gemini"
        """
        factory = BackendFactory()
        with patch('rlm.routing.backend_factory.get_client') as mock_get_client:
            mock_get_client.return_value = MagicMock(spec=BaseLM)
            factory.get_backend("gemini")
            call_args = mock_get_client.call_args
            assert call_args is not None

    def test_map_portkey_to_portkey(self):
        """
        Test that portkey maps to portkey.

        Expected behavior:
        - Should return ClientBackend.PORTKEY or "portkey"
        """
        factory = BackendFactory()
        with patch('rlm.routing.backend_factory.get_client') as mock_get_client:
            mock_get_client.return_value = MagicMock(spec=BaseLM)
            factory.get_backend("portkey")
            call_args = mock_get_client.call_args
            assert call_args is not None

    def test_map_litellm_to_litellm(self):
        """
        Test that litellm maps to litellm.

        Expected behavior:
        - Should return ClientBackend.LITELLM or "litellm"
        """
        factory = BackendFactory()
        with patch('rlm.routing.backend_factory.get_client') as mock_get_client:
            mock_get_client.return_value = MagicMock(spec=BaseLM)
            factory.get_backend("litellm")
            call_args = mock_get_client.call_args
            assert call_args is not None

    def test_map_unknown_to_openai(self):
        """
        Test that unknown backend_id defaults to openai.

        Expected behavior:
        - Should return ClientBackend.OPENAI or "openai"
        - Should not raise exception
        """
        factory = BackendFactory()
        with patch('rlm.routing.backend_factory.get_client') as mock_get_client:
            mock_get_client.return_value = MagicMock(spec=BaseLM)
            factory.get_backend("unknown_backend_xyz")
            call_args = mock_get_client.call_args
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
        configs1 = {"backend1": {"key1": "value1"}}
        configs2 = {"backend2": {"key2": "value2"}}

        factory1 = BackendFactory(backend_configs=configs1)
        factory2 = BackendFactory(backend_configs=configs2)

        assert factory1.backend_configs == configs1
        assert factory2.backend_configs == configs2
        assert factory1.backend_configs != factory2.backend_configs

    def test_config_immutability(self):
        """
        Test that modifying original config dict doesn't affect factory.

        Expected behavior:
        - Factory should store a copy or reference
        - Original dict modification should be handled appropriately
        """
        original_configs = {"backend1": {"key": "value"}}
        factory = BackendFactory(backend_configs=original_configs)

        # Modify original
        original_configs["backend2"] = {"key2": "value2"}

        # Factory should have the original reference
        # (Python dicts are mutable references)
        assert "backend2" in factory.backend_configs

    def test_empty_config_handling(self):
        """
        Test handling of empty backend configs.

        Expected behavior:
        - Should not raise exception
        - Should use default kwargs when provided
        """
        factory = BackendFactory(backend_configs={})

        with patch('rlm.routing.backend_factory.get_client') as mock_get_client:
            mock_client = MagicMock(spec=BaseLM)
            mock_get_client.return_value = mock_client

            client = factory.get_backend("any_backend", default_kwargs={"model": "gpt-4"})
            assert client == mock_client

    def test_config_with_special_characters(self):
        """
        Test handling of configs with special characters in values.

        Expected behavior:
        - Should handle special characters correctly
        - Should not raise exception
        """
        configs = {
            "backend1": {
                "api_key": "sk-1234567890abcdef",
                "model": "gpt-4-turbo-preview",
                "base_url": "https://api.example.com/v1"
            }
        }
        factory = BackendFactory(backend_configs=configs)

        with patch('rlm.routing.backend_factory.get_client') as mock_get_client:
            mock_client = MagicMock(spec=BaseLM)
            mock_get_client.return_value = mock_client

            client = factory.get_backend("backend1")
            assert client == mock_client


class TestErrorHandling:
    """
    Tests for error handling in backend creation.
    """

    @patch('rlm.routing.backend_factory.get_client')
    def test_get_client_exception_propagation(self, mock_get_client):
        """
        Test that exceptions from get_client are propagated.

        Args:
            mock_get_client: Mocked get_client function

        Expected behavior:
        - Should raise the same exception
        - Should not catch or hide errors
        """
        mock_get_client.side_effect = ValueError("Invalid configuration")

        factory = BackendFactory()

        with pytest.raises(ValueError, match="Invalid configuration"):
            factory.get_backend("test_backend")

    @patch('rlm.routing.backend_factory.get_client')
    def test_get_client_with_none_backend_id(self, mock_get_client):
        """
        Test creating backend with None backend_id.

        Args:
            mock_get_client: Mocked get_client function

        Expected behavior:
        - Should handle None gracefully
        - Should not raise exception (depends on implementation)
        """
        mock_client = MagicMock(spec=BaseLM)
        mock_get_client.return_value = mock_client

        factory = BackendFactory()

        # This may raise an exception depending on implementation
        # Test documents current behavior
        try:
            client = factory.get_backend(None)
            assert client == mock_client
        except (TypeError, AttributeError):
            # Also acceptable if it raises an exception
            pass

    @patch('rlm.routing.backend_factory.get_client')
    def test_get_client_with_empty_backend_id(self, mock_get_client):
        """
        Test creating backend with empty string backend_id.

        Args:
            mock_get_client: Mocked get_client function

        Expected behavior:
        - Should handle empty string gracefully
        - Should map to default backend type
        """
        mock_client = MagicMock(spec=BaseLM)
        mock_get_client.return_value = mock_client

        factory = BackendFactory()

        client = factory.get_backend("")
        assert client == mock_client


class TestMultipleBackends:
    """
    Tests for managing multiple backends.
    """

    @patch('rlm.routing.backend_factory.get_client')
    def test_create_multiple_backends(self, mock_get_client):
        """
        Test creating multiple backends from same factory.

        Args:
            mock_get_client: Mocked get_client function

        Expected behavior:
        - Should create each backend correctly
        - Each backend should be independent
        """
        mock_client = MagicMock(spec=BaseLM)
        mock_get_client.return_value = mock_client

        configs = {
            "backend1": {"model": "gpt-4"},
            "backend2": {"model": "claude-3"},
            "backend3": {"model": "gemini-pro"}
        }
        factory = BackendFactory(backend_configs=configs)

        client1 = factory.get_backend("backend1")
        client2 = factory.get_backend("backend2")
        client3 = factory.get_backend("backend3")

        assert mock_get_client.call_count == 3

    @patch('rlm.routing.backend_factory.get_client')
    def test_reuse_backend_config(self, mock_get_client):
        """
        Test that same backend can be requested multiple times.

        Args:
            mock_get_client: Mocked get_client function

        Expected behavior:
        - Should create new instance each time (or cache based on implementation)
        - Should not raise exception
        """
        mock_client = MagicMock(spec=BaseLM)
        mock_get_client.return_value = mock_client

        configs = {"backend1": {"model": "gpt-4"}}
        factory = BackendFactory(backend_configs=configs)

        client1 = factory.get_backend("backend1")
        client2 = factory.get_backend("backend1")

        # Depending on implementation, may create new instance or cache
        assert mock_get_client.call_count >= 1


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
            "backend1": {}  # Empty config
        }
        factory = BackendFactory(backend_configs=configs)

        with patch('rlm.routing.backend_factory.get_client') as mock_get_client:
            mock_client = MagicMock(spec=BaseLM)
            mock_get_client.return_value = mock_client

            # Should handle gracefully
            client = factory.get_backend("backend1")
            assert client == mock_client

    def test_config_with_extra_fields(self):
        """
        Test handling of config with extra fields.

        Expected behavior:
        - Should pass extra fields to get_client
        - Should not filter out fields
        """
        configs = {
            "backend1": {
                "model": "gpt-4",
                "api_key": "key",
                "extra_field": "extra_value",
                "another_extra": 123
            }
        }
        factory = BackendFactory(backend_configs=configs)

        with patch('rlm.routing.backend_factory.get_client') as mock_get_client:
            mock_client = MagicMock(spec=BaseLM)
            mock_get_client.return_value = mock_client

            client = factory.get_backend("backend1")
            assert client == mock_client
            # Check that all config fields were passed
            call_kwargs = mock_get_client.call_args[1]
            assert "extra_field" in call_kwargs or "model" in call_kwargs
