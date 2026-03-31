"""
Dynamic Layer 1 Bootstrap Loader.

This module dynamically generates and loads Layer 1 axioms based on
domain classification. It creates domain-specific Lean import files
and manages the verification oracle for each domain.
"""

import os
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
import threading

from rlm.routing.domain_classifier import (
    DomainType,
    DomainClassifier,
    ClassificationResult,
    DOMAIN_CONFIG,
)


@dataclass
class Layer1Context:
    """Context for a loaded Layer 1 domain."""

    domain: DomainType
    lean_bootstrap: str
    haskell_types: str
    research_sources: List[str]
    loaded_at: float = field(default_factory=time.time)
    loaded_by: Optional[str] = None


@dataclass
class DynamicLoaderConfig:
    """Configuration for the dynamic Layer 1 loader."""

    output_dir: str = ".layer1_cache"
    auto_reload: bool = True
    max_cached_domains: int = 10
    lean_path: Optional[str] = None
    haskell_path: Optional[str] = None


class DynamicLayer1Loader:
    """
    Dynamically loads and manages Layer 1 axioms based on domain.

    This class:
    1. Generates domain-specific layer1-bootstrap.lean files
    2. Manages loaded Layer 1 contexts
    3. Handles Layer 1.5 user axiom overrides
    4. Provides the verification oracle for agents
    """

    def __init__(self, config: Optional[DynamicLoaderConfig] = None):
        """
        Initialize the dynamic Layer 1 loader.

        Args:
            config: Optional configuration for the loader
        """
        self._config = config or DynamicLoaderConfig()
        self._classifier = DomainClassifier()
        self._loaded_contexts: Dict[DomainType, Layer1Context] = {}
        self._lock = threading.Lock()
        self._callbacks: Dict[str, List[Callable]] = {
            "domain_loaded": [],
            "domain_unloaded": [],
        }

        # Ensure output directory exists
        os.makedirs(self._config.output_dir, exist_ok=True)

    def load_domain(
        self, domain: DomainType, owner: Optional[str] = None
    ) -> Layer1Context:
        """
        Load Layer 1 for a specific domain.

        Args:
            domain: The domain to load
            owner: Optional identifier for what requested the load

        Returns:
            Layer1Context for the loaded domain
        """
        with self._lock:
            # Check if already loaded
            if domain in self._loaded_contexts:
                return self._loaded_contexts[domain]

            # Generate bootstrap content
            context = self._generate_context(domain, owner)

            # Write bootstrap file
            self._write_bootstrap_file(context)

            # Store context
            self._loaded_contexts[domain] = context

            # Enforce max cache size
            self._enforce_cache_size()

            # Emit callback
            self._emit(
                "domain_loaded",
                {
                    "domain": domain.value,
                    "context": context,
                },
            )

            return context

    def unload_domain(self, domain: DomainType) -> bool:
        """
        Unload Layer 1 for a specific domain.

        Args:
            domain: The domain to unload

        Returns:
            True if unloaded successfully
        """
        with self._lock:
            if domain in self._loaded_contexts:
                del self._loaded_contexts[domain]
                self._emit("domain_unloaded", {"domain": domain.value})
                return True
            return False

    def get_context(self, domain: DomainType) -> Optional[Layer1Context]:
        """
        Get the loaded context for a domain.

        Args:
            domain: The domain to get context for

        Returns:
            Layer1Context if loaded, None otherwise
        """
        with self._lock:
            return self._loaded_contexts.get(domain)

    def is_loaded(self, domain: DomainType) -> bool:
        """Check if a domain is loaded."""
        with self._lock:
            return domain in self._loaded_contexts

    def get_loaded_domains(self) -> List[DomainType]:
        """Get list of currently loaded domains."""
        with self._lock:
            return list(self._loaded_contexts.keys())

    def classify_and_load(
        self, task_description: str, owner: Optional[str] = None
    ) -> tuple[ClassificationResult, Layer1Context]:
        """
        Classify a task and load the appropriate domain.

        Args:
            task_description: The task to classify
            owner: Optional identifier for the requester

        Returns:
            Tuple of (ClassificationResult, Layer1Context)
        """
        # Classify the task
        result = self._classifier.classify(task_description)

        # Load the domain
        context = self.load_domain(result.primary_domain, owner)

        return result, context

    def generate_layer1_bootstrap(self, domain: DomainType) -> str:
        """
        Generate Layer 1 bootstrap content for a domain.

        Args:
            domain: The domain to generate for

        Returns:
            The Lean bootstrap content
        """
        config = DOMAIN_CONFIG.get(domain, DOMAIN_CONFIG[DomainType.GENERAL])
        imports = config.get("lean_imports", [])

        if not imports:
            return ""

        # Generate standard header
        content = "-- Auto-generated Layer 1 Bootstrap\n"
        content += f"-- Domain: {domain.value}\n"
        content += f"-- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Add imports
        for imp in imports:
            content += f"import {imp}\n"

        content += "\n"

        # Add standard namespace and verification oracle stub
        content += """namespace VerificationOracle

-- Type aliases for common structures
section Types
  /- Common type definitions for domain verification -/
end Types

-- Verification helpers
section Helpers
  /- Helper functions for proof verification -/
end Helpers

end VerificationOracle
"""

        return content

    def generate_layer1_5_override(
        self,
        user_axioms: List[Dict[str, str]],
        task_id: str,
    ) -> str:
        """
        Generate Layer 1.5 user axiom override file.

        Args:
            user_axioms: List of axiom definitions
            task_id: ID of the task this is for

        Returns:
            The Lean override file content
        """
        content = "-- USER AXIOM OVERRIDES (LAYER 1.5)\n"
        content += f"-- Task: {task_id}\n"
        content += f"-- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += "-- WARNING: User-defined axioms bypass Lean kernel safety!\n\n"

        content += "namespace Layer1_5\n\n"

        for i, axiom in enumerate(user_axioms):
            name = axiom.get("name", f"user_axiom_{i}")
            description = axiom.get("description", "User-defined axiom")
            expression = axiom.get("lean_axiom", axiom.get("expression", ""))

            content += f"/- {description} -/\n"
            content += f"axiom {name} : {expression}\n\n"

        content += "end Layer1_5\n"

        return content

    def generate_haskell_types(self, domain: DomainType) -> str:
        """
        Generate Haskell type definitions for a domain.

        Args:
            domain: The domain to generate for

        Returns:
            Haskell type definitions
        """
        config = DOMAIN_CONFIG.get(domain, DOMAIN_CONFIG[DomainType.GENERAL])
        imports = config.get("haskell_imports", [])

        content = "-- Auto-generated Haskell Types\n"
        content += f"-- Domain: {domain.value}\n"
        content += f"-- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        if imports:
            content += "{-# LANGUAGE ImportQualifiedPost #-}\n\n"
            for imp in imports:
                content += f"import {imp}\n"
            content += "\n"

        # Add domain-specific types based on domain
        if domain == DomainType.PHYSICS:
            content += """-- Physics dimension types
module Physics.Dimensions where

data Dimension = Dimension String
  deriving (Show, Eq)

-- Unit types for common physical quantities
data Length = Length Double deriving (Show, Eq)
data Mass = Mass Double deriving (Show, Eq)
data Time = Time Double deriving (Show, Eq)
data Force = Force Double deriving (Show, Eq)
data Energy = Energy Double deriving (Show, Eq)
"""
        elif domain == DomainType.SOFTWARE:
            content += """-- Software verification types
module Software.Types where

data ProofObligation = ProofObligation String
  deriving (Show, Eq)

data Invariant a = Invariant a
  deriving (Show, Eq)
"""
        elif domain == DomainType.FINANCE:
            content += """-- Financial types
module Finance.Types where

newtype USD = USD Double deriving (Show, Eq)
newtype EUR = EUR Double deriving (Show, Eq)
newtype GBP = GBP Double deriving (Show, Eq)

data Portfolio = Portfolio [(String, Double)]
  deriving (Show, Eq)
"""

        return content

    def get_verification_oracle(self, domain: DomainType) -> Dict[str, Any]:
        """
        Get the verification oracle for a domain.

        Args:
            domain: The domain to get oracle for

        Returns:
            Dictionary with lean_bootstrap_path and haskell_types_path

        Raises:
            RuntimeError: If domain is not loaded
        """
        context = self.get_context(domain)
        if not context:
            raise RuntimeError(
                f"Domain {domain.value} not loaded. Call load_domain() first."
            )

        return {
            "domain": domain.value,
            "lean_bootstrap": context.lean_bootstrap,
            "haskell_types": context.haskell_types,
            "research_sources": context.research_sources,
            "loaded_at": context.loaded_at,
        }

    def register_callback(self, event: str, callback: Callable) -> None:
        """
        Register a callback for loader events.

        Args:
            event: Event type ('domain_loaded', 'domain_unloaded')
            callback: Function to call
        """
        if event in self._callbacks and callback not in self._callbacks[event]:
            self._callbacks[event].append(callback)

    def unregister_callback(self, event: str, callback: Callable) -> None:
        """Unregister a callback."""
        if event in self._callbacks and callback in self._callbacks[event]:
            self._callbacks[event].remove(callback)

    def _generate_context(
        self, domain: DomainType, owner: Optional[str]
    ) -> Layer1Context:
        """Generate a Layer1Context for a domain."""
        config = DOMAIN_CONFIG.get(domain, DOMAIN_CONFIG[DomainType.GENERAL])

        lean_bootstrap = self.generate_layer1_bootstrap(domain)
        haskell_types = self.generate_haskell_types(domain)

        return Layer1Context(
            domain=domain,
            lean_bootstrap=lean_bootstrap,
            haskell_types=haskell_types,
            research_sources=config.get("research_sources", []),
            loaded_by=owner,
        )

    def _write_bootstrap_file(self, context: Layer1Context) -> str:
        """Write the bootstrap file to disk and return the path."""
        filename = f"layer1_bootstrap_{context.domain.value}.lean"
        filepath = os.path.join(self._config.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(context.lean_bootstrap)

        context.lean_bootstrap = filepath
        return filepath

    def _enforce_cache_size(self) -> None:
        """Enforce maximum cache size by unloading oldest domains."""
        if len(self._loaded_contexts) > self._config.max_cached_domains:
            # Find oldest loaded domain
            oldest = None
            oldest_time = float("inf")
            for domain, context in self._loaded_contexts.items():
                if context.loaded_at < oldest_time:
                    oldest_time = context.loaded_at
                    oldest = domain

            if oldest:
                del self._loaded_contexts[oldest]

    def _emit(self, event: str, data: Dict[str, Any]) -> None:
        """Emit an event to callbacks."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(data)
            except Exception:
                pass
