"""
Type Checker Registry for managing available type checkers.

This module provides a registry for type checkers that allows
registering, retrieving, and managing multiple type checker instances.
"""

from typing import Dict, Optional

from rlm.typechecking.base import TypeChecker
from rlm.typechecking.config import TypeCheckerConfig, load_type_checker_config
from rlm.typechecking.exceptions import TypeCheckerNotAvailableError


class TypeCheckerRegistry:
    """
    Registry for managing type checker instances.

    This class provides a centralized registry for type checkers,
    allowing easy access to Haskell and Lean type checkers throughout
    the application.

    Example:
        >>> registry = TypeCheckerRegistry()
        >>> registry.initialize()
        >>> haskell_checker = registry.get_checker("haskell")
        >>> lean_checker = registry.get_checker("lean")
    """

    def __init__(self, config: Optional[TypeCheckerConfig] = None):
        """
        Initialize the registry.

        Args:
            config: Optional TypeCheckerConfig. If not provided,
                   loads from default config file.
        """
        self._checkers: Dict[str, TypeChecker] = {}
        self._config = config or load_type_checker_config()
        self._initialized = False

    @property
    def config(self) -> TypeCheckerConfig:
        """Return the registry configuration."""
        return self._config

    @property
    def is_initialized(self) -> bool:
        """Return whether the registry has been initialized."""
        return self._initialized

    def initialize(self) -> None:
        """
        Initialize all enabled type checkers based on configuration.

        This method creates and registers type checker instances
        for all checkers that are enabled in the configuration.

        Raises:
            TypeCheckerNotAvailableError: If a configured checker is not available.
        """
        from rlm.typechecking.haskell import GHCChecker
        from rlm.typechecking.lean import LakeChecker

        self._checkers.clear()

        # Initialize Haskell checker if enabled
        if self._config.haskell.enabled:
            try:
                haskell_checker = GHCChecker(
                    timeout_seconds=self._config.haskell.timeout_seconds,
                    ghc_path=self._config.haskell.ghc_path,
                    ghc_options=self._config.haskell.ghc_options,
                )
                self._checkers["haskell"] = haskell_checker
            except TypeCheckerNotAvailableError as e:
                # Log warning but don't fail if GHC is not available
                import warnings

                warnings.warn(f"Haskell checker not available: {e}")

        # Initialize Lean checker if enabled
        if self._config.lean.enabled:
            try:
                lean_checker = LakeChecker(
                    timeout_seconds=self._config.lean.timeout_seconds,
                    lake_path=self._config.lean.lake_path,
                    lean_path=self._config.lean.lean_path,
                    lean_options=self._config.lean.lean_options,
                )
                self._checkers["lean"] = lean_checker
            except TypeCheckerNotAvailableError as e:
                # Log warning but don't fail if Lake is not available
                import warnings

                warnings.warn(f"Lean checker not available: {e}")

        self._initialized = True

    def register_checker(self, name: str, checker: TypeChecker) -> None:
        """
        Register a type checker with a given name.

        Args:
            name: Name to register the checker under (e.g., 'haskell', 'lean').
            checker: TypeChecker instance to register.

        Raises:
            TypeError: If checker is not a TypeChecker instance.
        """
        if not isinstance(checker, TypeChecker):
            raise TypeError(f"Expected TypeChecker instance, got {type(checker)}")

        self._checkers[name] = checker

    def get_checker(self, name: str) -> TypeChecker:
        """
        Get a registered type checker by name.

        Args:
            name: Name of the checker to retrieve.

        Returns:
            The TypeChecker instance.

        Raises:
            KeyError: If no checker is registered under the given name.
        """
        if name not in self._checkers:
            raise KeyError(f"No type checker registered under '{name}'")

        return self._checkers[name]

    def get_checker_or_none(self, name: str) -> Optional[TypeChecker]:
        """
        Get a registered type checker by name, or None if not found.

        Args:
            name: Name of the checker to retrieve.

        Returns:
            The TypeChecker instance, or None if not registered.
        """
        return self._checkers.get(name)

    def unregister_checker(self, name: str) -> bool:
        """
        Unregister a type checker.

        Args:
            name: Name of the checker to unregister.

        Returns:
            True if the checker was unregistered, False if it wasn't registered.
        """
        if name in self._checkers:
            del self._checkers[name]
            return True
        return False

    def list_checkers(self) -> list[str]:
        """
        Get a list of all registered checker names.

        Returns:
            List of registered checker names.
        """
        return list(self._checkers.keys())

    def get_available_checkers(self) -> Dict[str, TypeChecker]:
        """
        Get all registered checkers that are currently available.

        Returns:
            Dictionary mapping checker names to available TypeChecker instances.
        """
        return {
            name: checker
            for name, checker in self._checkers.items()
            if checker.is_available()
        }

    def is_checker_available(self, name: str) -> bool:
        """
        Check if a checker is registered and available.

        Args:
            name: Name of the checker to check.

        Returns:
            True if the checker is registered and available.
        """
        if name not in self._checkers:
            return False
        return self._checkers[name].is_available()

    def health_check_all(self) -> Dict[str, Dict]:
        """
        Perform health check on all registered checkers.

        Returns:
            Dictionary mapping checker names to health status dicts.
        """
        results = {}
        for name, checker in self._checkers.items():
            health = checker.health_check()
            results[name] = {
                "status": health.status.value,
                "version": health.version,
                "error": health.error,
            }
        return results

    def reload_config(self, config: Optional[TypeCheckerConfig] = None) -> None:
        """
        Reload configuration and reinitialize checkers.

        Args:
            config: Optional new configuration. If not provided,
                   reloads from default config file.
        """
        self._config = config or load_type_checker_config()
        self._initialized = False
        self.initialize()


# Global registry instance for convenience
_global_registry: Optional[TypeCheckerRegistry] = None


def get_registry() -> TypeCheckerRegistry:
    """
    Get the global type checker registry instance.

    If no registry exists, creates one with default configuration
    and initializes it.

    Returns:
        The global TypeCheckerRegistry instance.
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = TypeCheckerRegistry()
        _global_registry.initialize()
    return _global_registry


def reset_registry() -> None:
    """Reset the global registry to None."""
    global _global_registry
    _global_registry = None
