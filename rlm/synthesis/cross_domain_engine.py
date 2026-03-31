"""
Cross-Domain Synthesis Engine.

This module implements the Cross-Domain Synthesis & Matrix Engine for combining
multiple domain structures into unified proofs. It handles domain collision detection,
translation rules, and genesis state generation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Tuple
from enum import Enum
import time

from rlm.routing.domain_classifier import DomainType, DOMAIN_CONFIG


class CollisionStatus(Enum):
    """Status of domain collision detection."""

    NONE = "none"
    DETECTED = "detected"
    RESOLVED = "resolved"
    UNRESOLVABLE = "unresolvable"


class SynthesisStatus(Enum):
    """Status of synthesis task."""

    PENDING = "pending"
    GENERATING_STRUCTURE = "generating_structure"
    GENERATING_TRANSLATIONS = "generating_translations"
    GENERATING_GENESIS = "generating_genesis"
    VERIFYING = "verifying"
    PASSED = "passed"
    FAILED = "failed"


@dataclass
class DomainField:
    """A field from a specific domain."""

    name: str
    domain: DomainType
    lean_type: str
    description: str


@dataclass
class CrossDomainInvariant:
    """An invariant that spans multiple domains."""

    name: str
    description: str
    lean_expression: str
    involved_domains: List[DomainType]
    is_verified: bool = False
    verification_error: Optional[str] = None


@dataclass
class DomainMapping:
    """Mapping between domains for type translation."""

    source_domain: DomainType
    target_domain: DomainType
    source_type: str
    target_type: str
    translation_rule: str
    inverse_rule: Optional[str] = None


@dataclass
class UnifiedStructure:
    """A structure combining multiple domains."""

    name: str
    involved_domains: List[DomainType]
    fields: List[DomainField]
    lean_definition: str
    invariants: List[CrossDomainInvariant] = field(default_factory=list)
    genesis_state: Optional[str] = None
    genesis_proof: Optional[str] = None


@dataclass
class CollisionReport:
    """Report of a domain collision."""

    domain1: DomainType
    domain2: DomainType
    field1: str
    field2: str
    issue: str
    suggested_resolution: Optional[str] = None


# Type compatibility map - which domains can be safely combined
DOMAIN_COMPATIBILITY: Dict[DomainType, Set[DomainType]] = {
    DomainType.MATH: {
        DomainType.PHYSICS,
        DomainType.SOFTWARE,
        DomainType.FINANCE,
        DomainType.CHEMISTRY,
        DomainType.GENERAL,
    },
    DomainType.PHYSICS: {
        DomainType.MATH,
        DomainType.SOFTWARE,
        DomainType.CHEMISTRY,
        DomainType.FINANCE,
        DomainType.GENERAL,
    },
    DomainType.SOFTWARE: {
        DomainType.MATH,
        DomainType.PHYSICS,
        DomainType.FINANCE,
        DomainType.CHEMISTRY,
        DomainType.GENERAL,
    },
    DomainType.CHEMISTRY: {
        DomainType.MATH,
        DomainType.PHYSICS,
        DomainType.SOFTWARE,
        DomainType.GENERAL,
    },
    DomainType.FINANCE: {
        DomainType.MATH,
        DomainType.PHYSICS,
        DomainType.SOFTWARE,
        DomainType.GENERAL,
    },
    DomainType.CYBER_SEC: {DomainType.SOFTWARE, DomainType.GENERAL},
    DomainType.REVERSE_ENGINEERING: {
        DomainType.SOFTWARE,
        DomainType.PHYSICS,
        DomainType.GENERAL,
    },
    DomainType.DOMAIN_ZERO: set(),
    DomainType.GENERAL: set(DomainType),
}

# Cross-domain type mappings for common patterns
STANDARD_MAPPINGS: List[DomainMapping] = [
    # Finance <-> Physics (both use quantitative measures)
    DomainMapping(
        source_domain=DomainType.FINANCE,
        target_domain=DomainType.PHYSICS,
        source_type="USD",
        target_type="Quantity USD",
        translation_rule="Currency.toQuantity",
        inverse_rule="Quantity.toCurrency",
    ),
    DomainMapping(
        source_domain=DomainType.PHYSICS,
        target_domain=DomainType.FINANCE,
        source_type="Quantity Volume",
        target_type="Quantity USD_per_Volume",
        translation_rule="Volume.toUSD",
        inverse_rule="USD.toVolume",
    ),
]


class CrossDomainSynthesisEngine:
    """
    Engine for synthesizing structures across multiple domains.

    Responsibilities:
    1. Detect domain collisions when combining domains
    2. Generate unified structures from multiple domains
    3. Create cross-domain invariants
    4. Generate genesis state and proofs
    5. Verify synthesis against type system
    """

    def __init__(self):
        """Initialize the synthesis engine."""
        self._active_synthesis: Optional[UnifiedStructure] = None
        self._collision_history: List[CollisionReport] = []
        self._standard_mappings = STANDARD_MAPPINGS.copy()

    def check_domain_compatibility(
        self, domains: List[DomainType]
    ) -> Tuple[bool, List[CollisionReport]]:
        """
        Check if multiple domains can be safely combined.

        Args:
            domains: List of domains to check

        Returns:
            Tuple of (is_compatible, list of collision reports)
        """
        collisions: List[CollisionReport] = []

        # Check all pairs
        for i, d1 in enumerate(domains):
            for d2 in domains[i + 1 :]:
                compatible_domains = DOMAIN_COMPATIBILITY.get(d1, set())
                if d2 not in compatible_domains:
                    collisions.append(
                        CollisionReport(
                            domain1=d1,
                            domain2=d2,
                            field1="",
                            field2="",
                            issue=f"Domain {d1.value} and {d2.value} are not compatible",
                            suggested_resolution=f"Use a translation layer or select a different domain combination",
                        )
                    )

        return len(collisions) == 0, collisions

    def detect_collisions(
        self, structure1: UnifiedStructure, structure2: UnifiedStructure
    ) -> List[CollisionReport]:
        """
        Detect potential type collisions between two structures.

        Args:
            structure1: First structure
            structure2: Second structure

        Returns:
            List of potential collision reports
        """
        collisions: List[CollisionReport] = []

        for field1 in structure1.fields:
            for field2 in structure2.fields:
                # Check if same name but different type
                if field1.name == field2.name and field1.lean_type != field2.lean_type:
                    collisions.append(
                        CollisionReport(
                            domain1=field1.domain,
                            domain2=field2.domain,
                            field1=field1.name,
                            field2=field2.name,
                            issue=f"Field '{field1.name}' has conflicting types: {field1.lean_type} vs {field2.lean_type}",
                            suggested_resolution=f"Rename one field or create a translation mapping",
                        )
                    )

                # Check if types that shouldn't be mixed
                if self._would_cause_collision(field1.lean_type, field2.lean_type):
                    collisions.append(
                        CollisionReport(
                            domain1=field1.domain,
                            domain2=field2.domain,
                            field1=field1.name,
                            field2=field2.name,
                            issue=f"Type mismatch: {field1.lean_type} cannot be directly combined with {field2.lean_type}",
                            suggested_resolution="Create explicit type conversion",
                        )
                    )

        return collisions

    def _would_cause_collision(self, type1: str, type2: str) -> bool:
        """Check if two types would cause a collision."""
        # Incompatible type pairs
        incompatible_pairs = [
            ("USD", "Volume"),
            ("EUR", "Volume"),
            ("GBP", "Volume"),
            ("USD", "Force"),
            ("EUR", "Force"),
            ("Currency", "Dimension"),
        ]

        for inc1, inc2 in incompatible_pairs:
            if (inc1 in type1 and inc2 in type2) or (inc2 in type1 and inc1 in type2):
                return True

        return False

    def create_unified_structure(
        self,
        name: str,
        domains: List[DomainType],
        domain_fields: Dict[DomainType, List[Tuple[str, str, str]]],
    ) -> UnifiedStructure:
        """
        Create a unified structure from multiple domains.

        Args:
            name: Name of the unified structure
            domains: List of domains involved
            domain_fields: Dict mapping domain to list of (field_name, lean_type, description)

        Returns:
            The created unified structure
        """
        fields: List[DomainField] = []
        lean_lines: List[str] = []

        # Header
        lean_lines.append(f"-- Unified Structure: {name}")
        lean_lines.append(f"-- Domains: {', '.join(d.value for d in domains)}")
        lean_lines.append(f"-- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        lean_lines.append("")
        lean_lines.append(f"structure {name} where")

        # Add fields from each domain
        for domain in domains:
            domain_config = DOMAIN_CONFIG.get(domain, DOMAIN_CONFIG[DomainType.GENERAL])
            lean_imports = domain_config.get("lean_imports", [])

            # Add import comment
            if lean_imports:
                lean_lines.append(f"  /- {domain.value} domain -/")

            for field_name, lean_type, description in domain_fields.get(domain, []):
                field = DomainField(
                    name=field_name,
                    domain=domain,
                    lean_type=lean_type,
                    description=description,
                )
                fields.append(field)
                lean_lines.append(f"  {field_name} : {lean_type}")

        lean_lines.append("")

        # Add structure end marker
        lean_lines.append(f"namespace {name}")
        lean_lines.append("")
        lean_lines.append("end")

        structure = UnifiedStructure(
            name=name,
            involved_domains=domains,
            fields=fields,
            lean_definition="\n".join(lean_lines),
        )

        self._active_synthesis = structure
        return structure

    def add_cross_domain_invariant(
        self,
        name: str,
        description: str,
        lean_expression: str,
        involved_domains: List[DomainType],
    ) -> CrossDomainInvariant:
        """
        Add a cross-domain invariant to the active synthesis.

        Args:
            name: Name of the invariant
            description: Human-readable description
            lean_expression: The Lean expression for the invariant
            involved_domains: Domains involved in this invariant

        Returns:
            The created invariant
        """
        invariant = CrossDomainInvariant(
            name=name,
            description=description,
            lean_expression=lean_expression,
            involved_domains=involved_domains,
        )

        if self._active_synthesis:
            self._active_synthesis.invariants.append(invariant)

        return invariant

    def generate_genesis_state(
        self,
        field_values: Dict[str, Any],
    ) -> str:
        """
        Generate genesis state for the active synthesis.

        Args:
            field_values: Dict mapping field names to their genesis values

        Returns:
            The generated genesis state as a Lean definition
        """
        if not self._active_synthesis:
            raise ValueError(
                "No active synthesis. Call create_unified_structure first."
            )

        lines: List[str] = []
        name = self._active_synthesis.name

        lines.append(f"/- Genesis State for {name} -/")
        lines.append(f"/- Proves that the structure is mathematically consistent -/")
        lines.append("")
        lines.append(f"def Genesis{name} : {name} := {{")

        # Add field values
        for i, field in enumerate(self._active_synthesis.fields):
            value = field_values.get(
                field.name, self._get_default_value(field.lean_type)
            )
            if i > 0:
                lines.append(",")
            lines.append(f"  {field.name} := {value}")

        lines.append("}")
        lines.append("")

        # Add invariant proofs
        for invariant in self._active_synthesis.invariants:
            lines.append(f"-- {invariant.description}")
            lines.append(f"{invariant.name} := by linarith")

        genesis = "\n".join(lines)
        self._active_synthesis.genesis_state = genesis

        return genesis

    def _get_default_value(self, lean_type: str) -> str:
        """Get a default value for a Lean type."""
        if "Nat" in lean_type:
            return "0"
        elif "Int" in lean_type:
            return "0"
        elif "Float" in lean_type or "Real" in lean_type:
            return "0.0"
        elif "Bool" in lean_type:
            return "false"
        elif "String" in lean_type:
            return '""'
        elif "List" in lean_type:
            return "[]"
        elif "USD" in lean_type or "EUR" in lean_type or "GBP" in lean_type:
            return "0"
        elif "Volume" in lean_type or "Mass" in lean_type or "Length" in lean_type:
            return "0"
        else:
            return "default"

    def get_mappings_for_domains(
        self, domain1: DomainType, domain2: DomainType
    ) -> List[DomainMapping]:
        """
        Get available type mappings between two domains.

        Args:
            domain1: First domain
            domain2: Second domain

        Returns:
            List of applicable mappings
        """
        return [
            m
            for m in self._standard_mappings
            if (m.source_domain == domain1 and m.target_domain == domain2)
            or (m.source_domain == domain2 and m.target_domain == domain1)
        ]

    def add_custom_mapping(self, mapping: DomainMapping) -> None:
        """
        Add a custom domain mapping.

        Args:
            mapping: The mapping to add
        """
        self._standard_mappings.append(mapping)

    def verify_synthesis(self) -> Tuple[bool, Optional[str]]:
        """
        Verify the active synthesis.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self._active_synthesis:
            return False, "No active synthesis"

        # Check structure has fields
        if not self._active_synthesis.fields:
            return False, "Structure has no fields"

        # Check all invariants are verified
        for invariant in self._active_synthesis.invariants:
            if not invariant.is_verified:
                return False, f"Invariant '{invariant.name}' is not verified"

        # Check genesis state exists
        if not self._active_synthesis.genesis_state:
            return False, "Genesis state not generated"

        return True, None

    def get_active_synthesis(self) -> Optional[UnifiedStructure]:
        """Get the currently active synthesis."""
        return self._active_synthesis

    def clear_active_synthesis(self) -> None:
        """Clear the active synthesis."""
        self._active_synthesis = None

    def get_collision_history(self) -> List[CollisionReport]:
        """Get history of detected collisions."""
        return self._collision_history.copy()
