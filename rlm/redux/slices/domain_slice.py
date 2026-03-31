"""
Redux slice for domain classification and routing state management.

This module provides state management for the Axiomatic Seed Domain Routing Protocol,
handling task classification and dynamic Layer 1 axiom mounting.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum
import time


class DomainType(Enum):
    """Known domain types for task classification."""

    MATH = "math"
    PHYSICS = "physics"
    SOFTWARE = "software"
    CHEMISTRY = "chemistry"
    FINANCE = "finance"
    CYBER_SEC = "cyber_sec"
    REVERSE_ENGINEERING = "reverse_engineering"
    DOMAIN_ZERO = "domain_zero"
    GENERAL = "general"


class ClassificationConfidence(Enum):
    """Confidence level of domain classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CERTAIN = "certain"


@dataclass
class DomainConfig:
    """Configuration for a specific domain."""

    domain_type: DomainType
    lean_imports: List[str]
    haskell_imports: List[str]
    research_sources: List[str]
    enabled: bool = True


@dataclass
class Layer1Context:
    """Context for a loaded Layer 1."""

    domain: str
    lean_bootstrap: str
    haskell_types: str
    loaded_at: float = field(default_factory=time.time)
    loaded_by: Optional[str] = None


@dataclass
class DomainClassification:
    """Record of a domain classification decision."""

    task_id: str
    domain: DomainType
    confidence: ClassificationConfidence
    keywords_matched: List[str]
    keywords_total: int
    classified_at: float = field(default_factory=time.time)
    fallback_domain: Optional[DomainType] = None


@dataclass
class DomainMismatchRecord:
    """Record of a domain mismatch detection."""

    task_id: str
    attempted_domain: DomainType
    correct_domain: DomainType
    proof_failure_count: int
    detected_at: float = field(default_factory=time.time)


@dataclass
class DomainState:
    """Redux slice for domain routing state."""

    active_domain: Optional[str] = None
    domain_configs: Dict[str, DomainConfig] = field(default_factory=dict)
    loaded_libraries: Dict[str, Layer1Context] = field(default_factory=dict)
    classification_history: List[DomainClassification] = field(default_factory=list)
    mismatch_history: List[DomainMismatchRecord] = field(default_factory=list)
    current_task_id: Optional[str] = None
    domain_keyword_scores: Dict[str, float] = field(default_factory=dict)


DEFAULT_DOMAIN_CONFIGS: Dict[str, DomainConfig] = {
    "MATH": DomainConfig(
        domain_type=DomainType.MATH,
        lean_imports=["Mathlib.All"],
        haskell_imports=["Data.Numeral.Decimal"],
        research_sources=["arXiv:math", "zbMATH", "IACR"],
    ),
    "PHYSICS": DomainConfig(
        domain_type=DomainType.PHYSICS,
        lean_imports=["SciLean", "PhysLib", "Mathlib.Analysis"],
        haskell_imports=["Physics.Dimensional", "Data.Units.Physical"],
        research_sources=["NIST", "IEEE Xplore", "ASM"],
    ),
    "SOFTWARE": DomainConfig(
        domain_type=DomainType.SOFTWARE,
        lean_imports=["Batteries", "Std", "Lean.Meta"],
        haskell_imports=["Language.Haskell", "Data.Aeson"],
        research_sources=["ACM Digital Library", "IEEE CS", "arXiv:cs"],
    ),
    "CHEMISTRY": DomainConfig(
        domain_type=DomainType.CHEMISTRY,
        lean_imports=["ChemLean", "PhysLib.Thermodynamics"],
        haskell_imports=["Chemistry.Structure", "Data.Molecule"],
        research_sources=["PubChem", "ChemRxiv", "Materials Project"],
    ),
    "FINANCE": DomainConfig(
        domain_type=DomainType.FINANCE,
        lean_imports=["Mathlib.Probability", "Mathlib.MeasureTheory"],
        haskell_imports=["Finance.Yahoo", "Data.Time.Series"],
        research_sources=["SSRN", "NBER", "arXiv:q-fin"],
    ),
    "CYBER_SEC": DomainConfig(
        domain_type=DomainType.CYBER_SEC,
        lean_imports=["Lean.SMT", "Mathlib.Data.BitVec"],
        haskell_imports=["InfoSec.Taint", "Data.BitVector"],
        research_sources=["CVE MITRE DB", "RFCs", "Phrack", "Exploit-DB"],
    ),
    "DOMAIN_ZERO": DomainConfig(
        domain_type=DomainType.DOMAIN_ZERO,
        lean_imports=[],
        haskell_imports=[],
        research_sources=["Generic literature", "API docs"],
    ),
}


class DomainActions:
    """Action creators for domain state updates."""

    @staticmethod
    def classify_task(
        task_id: str,
        domain: DomainType,
        confidence: ClassificationConfidence,
        keywords_matched: List[str],
        keywords_total: int,
    ) -> dict:
        """Create action to record domain classification."""
        return {
            "type": "domain/classify_task",
            "payload": {
                "task_id": task_id,
                "domain": domain.value,
                "confidence": confidence.value,
                "keywords_matched": keywords_matched,
                "keywords_total": keywords_total,
            },
        }

    @staticmethod
    def mount_domain_libraries(domain: str, context: Layer1Context) -> dict:
        """Create action to mount domain libraries."""
        return {
            "type": "domain/mount_domain_libraries",
            "payload": {
                "domain": domain,
                "lean_bootstrap": context.lean_bootstrap,
                "haskell_types": context.haskell_types,
                "loaded_by": context.loaded_by,
            },
        }

    @staticmethod
    def unmount_libraries(domain: str) -> dict:
        """Create action to unmount domain libraries."""
        return {
            "type": "domain/unmount_libraries",
            "payload": {"domain": domain},
        }

    @staticmethod
    def detect_domain_mismatch(
        task_id: str,
        attempted_domain: DomainType,
        correct_domain: DomainType,
        proof_failure_count: int,
    ) -> dict:
        """Create action to detect and record domain mismatch."""
        return {
            "type": "domain/detect_mismatch",
            "payload": {
                "task_id": task_id,
                "attempted_domain": attempted_domain.value,
                "correct_domain": correct_domain.value,
                "proof_failure_count": proof_failure_count,
            },
        }

    @staticmethod
    def set_active_domain(domain: Optional[str]) -> dict:
        """Create action to set the active domain."""
        return {
            "type": "domain/set_active_domain",
            "payload": {"domain": domain},
        }

    @staticmethod
    def update_keyword_scores(scores: Dict[str, float]) -> dict:
        """Create action to update domain keyword scores."""
        return {
            "type": "domain/update_keyword_scores",
            "payload": {"scores": scores},
        }

    @staticmethod
    def clear_classification_history() -> dict:
        """Create action to clear classification history."""
        return {"type": "domain/clear_classification_history"}


def domain_reducer(state: DomainState, action: dict) -> DomainState:
    """
    Reducer function for domain state.

    Args:
        state: Current domain state.
        action: Action to apply to the state.

    Returns:
        New domain state.
    """
    action_type = action.get("type")

    if action_type == "domain/classify_task":
        payload = action.get("payload", {})
        classification = DomainClassification(
            task_id=payload.get("task_id"),
            domain=DomainType(payload.get("domain")),
            confidence=ClassificationConfidence(payload.get("confidence")),
            keywords_matched=payload.get("keywords_matched", []),
            keywords_total=payload.get("keywords_total", 0),
        )
        new_history = (state.classification_history + [classification])[-100:]
        return DomainState(
            active_domain=payload.get("domain"),
            domain_configs=state.domain_configs,
            loaded_libraries=state.loaded_libraries,
            classification_history=new_history,
            mismatch_history=state.mismatch_history,
            current_task_id=payload.get("task_id"),
            domain_keyword_scores=state.domain_keyword_scores,
        )

    elif action_type == "domain/mount_domain_libraries":
        payload = action.get("payload", {})
        domain = payload.get("domain")
        context = Layer1Context(
            domain=domain,
            lean_bootstrap=payload.get("lean_bootstrap"),
            haskell_types=payload.get("haskell_types"),
            loaded_by=payload.get("loaded_by"),
        )
        new_loaded = state.loaded_libraries.copy()
        new_loaded[domain] = context
        return DomainState(
            active_domain=state.active_domain,
            domain_configs=state.domain_configs,
            loaded_libraries=new_loaded,
            classification_history=state.classification_history,
            mismatch_history=state.mismatch_history,
            current_task_id=state.current_task_id,
            domain_keyword_scores=state.domain_keyword_scores,
        )

    elif action_type == "domain/unmount_libraries":
        payload = action.get("payload", {})
        domain = payload.get("domain")
        new_loaded = state.loaded_libraries.copy()
        if domain in new_loaded:
            del new_loaded[domain]
        return DomainState(
            active_domain=state.active_domain,
            domain_configs=state.domain_configs,
            loaded_libraries=new_loaded,
            classification_history=state.classification_history,
            mismatch_history=state.mismatch_history,
            current_task_id=state.current_task_id,
            domain_keyword_scores=state.domain_keyword_scores,
        )

    elif action_type == "domain/detect_mismatch":
        payload = action.get("payload", {})
        mismatch = DomainMismatchRecord(
            task_id=payload.get("task_id"),
            attempted_domain=DomainType(payload.get("attempted_domain")),
            correct_domain=DomainType(payload.get("correct_domain")),
            proof_failure_count=payload.get("proof_failure_count"),
        )
        new_mismatch_history = (state.mismatch_history + [mismatch])[-100:]
        return DomainState(
            active_domain=state.active_domain,
            domain_configs=state.domain_configs,
            loaded_libraries=state.loaded_libraries,
            classification_history=state.classification_history,
            mismatch_history=new_mismatch_history,
            current_task_id=state.current_task_id,
            domain_keyword_scores=state.domain_keyword_scores,
        )

    elif action_type == "domain/set_active_domain":
        payload = action.get("payload", {})
        return DomainState(
            active_domain=payload.get("domain"),
            domain_configs=state.domain_configs,
            loaded_libraries=state.loaded_libraries,
            classification_history=state.classification_history,
            mismatch_history=state.mismatch_history,
            current_task_id=state.current_task_id,
            domain_keyword_scores=state.domain_keyword_scores,
        )

    elif action_type == "domain/update_keyword_scores":
        payload = action.get("payload", {})
        return DomainState(
            active_domain=state.active_domain,
            domain_configs=state.domain_configs,
            loaded_libraries=state.loaded_libraries,
            classification_history=state.classification_history,
            mismatch_history=state.mismatch_history,
            current_task_id=state.current_task_id,
            domain_keyword_scores=payload.get("scores", {}),
        )

    elif action_type == "domain/clear_classification_history":
        return DomainState(
            active_domain=state.active_domain,
            domain_configs=state.domain_configs,
            loaded_libraries=state.loaded_libraries,
            classification_history=[],
            mismatch_history=state.mismatch_history,
            current_task_id=state.current_task_id,
            domain_keyword_scores=state.domain_keyword_scores,
        )

    return state
