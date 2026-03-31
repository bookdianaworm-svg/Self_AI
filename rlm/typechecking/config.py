"""
Configuration classes for the type checking system.

This module provides dataclasses for configuring Haskell and Lean type checkers,
as well as loading configuration from YAML files.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml


@dataclass
class HaskellConfig:
    """Configuration for Haskell type checking via GHC."""

    enabled: bool = False
    ghc_path: str = "ghc"
    timeout_seconds: float = 30.0
    ghc_options: list[str] = field(default_factory=lambda: ["-Wall", "-Werror"])
    note: str = ""


@dataclass
class LeanConfig:
    """Configuration for Lean verification via Lake."""

    enabled: bool = True
    lake_path: str = "lake"
    lean_path: str = "lean"
    mathlib: bool = True
    timeout_seconds: float = 60.0
    lean_options: list[str] = field(default_factory=list)


@dataclass
class TypeCheckerConfig:
    """
    Main configuration class for the type checking system.

    Attributes:
        version: Configuration version.
        haskell: Haskell checker configuration.
        lean: Lean checker configuration.
        fail_on_error: Whether to raise exceptions on type check failures.
        cache_results: Whether to cache type checking results.
        cache_dir: Directory for caching results.
    """

    version: str = "0.1"
    haskell: HaskellConfig = field(default_factory=HaskellConfig)
    lean: LeanConfig = field(default_factory=LeanConfig)
    fail_on_error: bool = True
    cache_results: bool = True
    cache_dir: str = ".type_check_cache"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TypeCheckerConfig":
        """
        Create a TypeCheckerConfig from a dictionary.

        Args:
            data: Dictionary containing configuration data.

        Returns:
            TypeCheckerConfig instance.
        """
        haskell_data = data.get("haskell", {})
        lean_data = data.get("lean", {})
        type_checking_data = data.get("type_checking", {})

        return cls(
            version=data.get("version", "0.1"),
            haskell=HaskellConfig(
                enabled=haskell_data.get("enabled", False),
                ghc_path=haskell_data.get("ghc_path", "ghc"),
                timeout_seconds=float(haskell_data.get("timeout_seconds", 30.0)),
                ghc_options=haskell_data.get("ghc_options", ["-Wall", "-Werror"]),
                note=haskell_data.get("note", ""),
            ),
            lean=LeanConfig(
                enabled=lean_data.get("enabled", True),
                lake_path=lean_data.get("lake_path", "lake"),
                lean_path=lean_data.get("lean_path", "lean"),
                mathlib=lean_data.get("mathlib", True),
                timeout_seconds=float(lean_data.get("timeout_seconds", 60.0)),
                lean_options=lean_data.get("lean_options", []),
            ),
            fail_on_error=type_checking_data.get("fail_on_error", True),
            cache_results=type_checking_data.get("cache_results", True),
            cache_dir=type_checking_data.get("cache_dir", ".type_check_cache"),
        )

    @classmethod
    def from_yaml(cls, path: str | Path) -> "TypeCheckerConfig":
        """
        Load configuration from a YAML file.

        Args:
            path: Path to the YAML configuration file.

        Returns:
            TypeCheckerConfig instance.

        Raises:
            FileNotFoundError: If the configuration file doesn't exist.
            yaml.YAMLError: If the file contains invalid YAML.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls.from_dict(data or {})

    def to_dict(self) -> dict[str, Any]:
        """
        Convert configuration to a dictionary.

        Returns:
            Dictionary representation of the configuration.
        """
        return {
            "version": self.version,
            "haskell": {
                "enabled": self.haskell.enabled,
                "ghc_path": self.haskell.ghc_path,
                "timeout_seconds": self.haskell.timeout_seconds,
                "ghc_options": self.haskell.ghc_options,
                "note": self.haskell.note,
            },
            "lean": {
                "enabled": self.lean.enabled,
                "lake_path": self.lean.lake_path,
                "lean_path": self.lean.lean_path,
                "mathlib": self.lean.mathlib,
                "timeout_seconds": self.lean.timeout_seconds,
                "lean_options": self.lean.lean_options,
            },
            "type_checking": {
                "fail_on_error": self.fail_on_error,
                "cache_results": self.cache_results,
                "cache_dir": self.cache_dir,
            },
        }

    def to_yaml(self, path: str | Path) -> None:
        """
        Save configuration to a YAML file.

        Args:
            path: Path where to save the configuration.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)


def load_type_checker_config(
    config_path: Optional[str | Path] = None,
    default_config_path: str = "config/type-checking.yaml",
) -> TypeCheckerConfig:
    """
    Load type checker configuration from a file.

    If config_path is not provided, tries default_config_path.
    If that doesn't exist either, returns a default configuration.

    Args:
        config_path: Optional explicit path to configuration file.
        default_config_path: Default path to configuration file.

    Returns:
        TypeCheckerConfig instance.
    """
    if config_path:
        path = Path(config_path)
        if path.exists():
            return TypeCheckerConfig.from_yaml(path)

    default_path = Path(default_config_path)
    if default_path.exists():
        return TypeCheckerConfig.from_yaml(default_path)

    return TypeCheckerConfig()
