"""
Configuration loader for type checking system.

This module provides utilities for loading and validating
type checking configuration from YAML files.
"""

from pathlib import Path
from typing import Optional, Union

import yaml

from rlm.typechecking.config import TypeCheckerConfig


def load_type_checking_config(
    config_path: Optional[Union[str, Path]] = None,
    default_config_path: str = "config/type-checking.yaml",
) -> TypeCheckerConfig:
    """
    Load type checking configuration from a YAML file.

    If config_path is not provided, tries default_config_path.
    If that doesn't exist either, returns a default configuration.

    Args:
        config_path: Optional explicit path to configuration file.
        default_config_path: Default path to configuration file.

    Returns:
        TypeCheckerConfig instance.

    Example:
        >>> config = load_type_checking_config()
        >>> config.haskell.enabled
        True
    """
    if config_path:
        path = Path(config_path)
        if path.exists():
            return TypeCheckerConfig.from_yaml(path)

    default_path = Path(default_config_path)
    if default_path.exists():
        return TypeCheckerConfig.from_yaml(default_path)

    # Return default configuration if no file found
    return TypeCheckerConfig()


def validate_config(config: TypeCheckerConfig) -> list[str]:
    """
    Validate a type checking configuration.

    Args:
        config: TypeCheckerConfig to validate.

    Returns:
        List of validation error messages (empty if valid).

    Example:
        >>> config = TypeCheckerConfig()
        >>> errors = validate_config(config)
        >>> if errors:
        ...     print("Config errors:", errors)
    """
    errors = []

    # Validate Haskell config
    if config.haskell.enabled:
        if not config.haskell.ghc_path:
            errors.append("Haskell checker enabled but ghc_path is empty")
        if config.haskell.timeout_seconds <= 0:
            errors.append("Haskell timeout_seconds must be positive")

    # Validate Lean config
    if config.lean.enabled:
        if not config.lean.lake_path:
            errors.append("Lean checker enabled but lake_path is empty")
        if config.lean.timeout_seconds <= 0:
            errors.append("Lean timeout_seconds must be positive")

    # Validate general config
    if config.cache_results:
        if not config.cache_dir:
            errors.append("Cache enabled but cache_dir is empty")

    return errors


def create_default_config(
    output_path: Optional[Union[str, Path]] = None,
) -> TypeCheckerConfig:
    """
    Create a default type checking configuration.

    Args:
        output_path: Optional path to save the configuration file.

    Returns:
        TypeCheckerConfig with default values.

    Example:
        >>> config = create_default_config("config/type-checking.yaml")
        >>> config.haskell.enabled
        True
    """
    config = TypeCheckerConfig()

    if output_path:
        config.to_yaml(output_path)

    return config


def merge_configs(
    base: TypeCheckerConfig, override: TypeCheckerConfig
) -> TypeCheckerConfig:
    """
    Merge two configurations, with override values taking precedence.

    Args:
        base: Base configuration.
        override: Override configuration.

    Returns:
        Merged TypeCheckerConfig.
    """
    return TypeCheckerConfig(
        version=override.version if override.version != "0.1" else base.version,
        haskell=override.haskell if override.haskell.enabled else base.haskell,
        lean=override.lean if override.lean.enabled else base.lean,
        fail_on_error=override.fail_on_error,
        cache_results=override.cache_results,
        cache_dir=override.cache_dir
        if override.cache_dir != ".type_check_cache"
        else base.cache_dir,
    )
