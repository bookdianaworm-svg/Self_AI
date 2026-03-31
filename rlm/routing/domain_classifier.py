"""
Domain Classifier for Task Routing.

This module implements the Axiomatic Seed Domain Routing Protocol,
classifying user tasks into predefined domains and selecting the
appropriate Layer 1 axioms and research sources.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import re


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
class DomainScore:
    """Score for a single domain classification."""

    domain: DomainType
    score: float
    matched_keywords: List[str] = field(default_factory=list)


@dataclass
class ClassificationResult:
    """Result of domain classification."""

    primary_domain: DomainType
    confidence: ClassificationConfidence
    all_scores: List[DomainScore]
    matched_keywords: List[str]
    fallback_domain: Optional[DomainType] = None


# Domain keyword definitions for classification
DOMAIN_KEYWORDS: Dict[DomainType, List[str]] = {
    DomainType.MATH: [
        "theorem",
        "proof",
        "prove",
        "lemma",
        "corollary",
        "algebra",
        "geometry",
        "topology",
        "analysis",
        "calculus",
        "number theory",
        "combinatorics",
        "graph",
        "polynomial",
        "matrix",
        "vector",
        "eigenvalue",
        "group",
        "ring",
        "field",
        "category",
        "functor",
        "natural transformation",
        "homotopy",
        "manifolds",
        "differential",
        "integral",
        "derivative",
        "limit",
        "convergence",
        "series",
        "prime",
        "cardinality",
        "ordinal",
        "ordinal",
        "measure",
        "lebesgue",
    ],
    DomainType.PHYSICS: [
        "force",
        "energy",
        "mass",
        "velocity",
        "acceleration",
        "momentum",
        "heat",
        "temperature",
        "pressure",
        "volume",
        "density",
        "gravity",
        "electromagnetic",
        "quantum",
        "relativity",
        "mechanics",
        "thermodynamics",
        "fluid",
        "wave",
        "oscillation",
        "harmonic",
        "pendulum",
        "spring",
        "circuit",
        "voltage",
        "current",
        "resistance",
        "capacitor",
        "inductor",
        "magnetic",
        "electric field",
        "photon",
        "electron",
        "proton",
        "neutron",
        "entropy",
        "hamiltonian",
        "lagrangian",
        "newtonian",
        "einstein",
        "physical",
        "dimension",
        "unit",
        "meter",
        "kilogram",
        "second",
    ],
    DomainType.SOFTWARE: [
        "algorithm",
        "code",
        "implement",
        "function",
        "class",
        "interface",
        "api",
        "software",
        "program",
        "compile",
        "debug",
        "test",
        "refactor",
        "architecture",
        "design pattern",
        "oop",
        "functional",
        "recursive",
        "data structure",
        "array",
        "linked list",
        "tree",
        "hash",
        "heap",
        "stack",
        "queue",
        "graph",
        "sort",
        "search",
        "dynamic programming",
        "greedy",
        "divide and conquer",
        "backtracking",
        "memoization",
        "software engineering",
        "agile",
        "scrum",
        "ci/cd",
        "deployment",
        "microservice",
        "container",
        "docker",
        "kubernetes",
        "database",
        "sql",
        "nosql",
        "cache",
        "queue",
        "message broker",
        "rest",
        "graphql",
        "http",
    ],
    DomainType.CHEMISTRY: [
        "molecule",
        "atom",
        "reaction",
        "bond",
        "periodic",
        "element",
        "organic",
        "inorganic",
        "biochemistry",
        "polymer",
        "catalyst",
        "enzyme",
        "protein",
        "dna",
        "rna",
        "metabolism",
        "equilibrium",
        "thermodynamics",
        "kinetics",
        "oxidation",
        "reduction",
        "acid",
        "base",
        "ph",
        "concentration",
        "stoichiometry",
        "gas",
        "liquid",
        "solid",
        "crystal",
        "spectroscopy",
        "chromatography",
        "mass spectrometry",
    ],
    DomainType.FINANCE: [
        "market",
        "stock",
        "bond",
        "derivative",
        "option",
        "future",
        "swap",
        "portfolio",
        "risk",
        "return",
        "volatility",
        "alpha",
        "beta",
        "sharpe",
        "trading",
        "arbitrage",
        "hedging",
        "speculation",
        "investment",
        "capital",
        "asset",
        "liability",
        "equity",
        "debt",
        "balance sheet",
        "income statement",
        "cash flow",
        "valuation",
        "dcf",
        "npv",
        "irr",
        "black-scholes",
        "binomial",
        "monte carlo",
        "portfolio theory",
        "efficient market",
        "emh",
        "behavioral finance",
        "algorithmic trading",
    ],
    DomainType.CYBER_SEC: [
        "vulnerability",
        "exploit",
        "malware",
        "ransomware",
        "trojan",
        "virus",
        "worm",
        "rootkit",
        "keylogger",
        "phishing",
        "social engineering",
        "authentication",
        "authorization",
        "encryption",
        "cryptography",
        "cipher",
        "aes",
        "rsa",
        "hash",
        "signature",
        "certificate",
        "tls",
        "firewall",
        "ids",
        "ips",
        "penetration testing",
        "red team",
        "blue team",
        "ctf",
        "capture the flag",
        "zero-day",
        "patch",
        "cve",
        "mitre",
        "buffer overflow",
        "sql injection",
        "xss",
        "csrf",
        "csrf",
        "authentication",
    ],
    DomainType.REVERSE_ENGINEERING: [
        "reverse engineer",
        "disassemble",
        "debugger",
        "decompile",
        "binary",
        "assembly",
        "machine code",
        "opcode",
        "disassembly",
        "hex",
        "bytecode",
        "firmware",
        "embbeded",
        "microcontroller",
        "protocol",
        "can bus",
        "uart",
        "spi",
        "i2c",
        "gpio",
        "hardware",
        "chip",
        "pcb",
        "schematic",
        "oscilloscope",
        "logic analyzer",
        "jtag",
        "swd",
        "debug probe",
    ],
}

# Edge case keywords that override normal classification
EDGE_CASE_KEYWORDS: Dict[DomainType, List[str]] = {
    DomainType.CYBER_SEC: [
        "intercept",
        "vulnerability",
        "exploit",
        "fuzz",
        "cleanroom",
        "protocol analysis",
        "pen test",
        "penetration test",
        "attack",
        "defense",
        "security audit",
        "intrusion detection",
    ],
    DomainType.REVERSE_ENGINEERING: [
        "reverse engineer",
        "disassemble",
        "decompile",
        "extract firmware",
        "hardware analysis",
        "chip decode",
        "protocol reverse",
    ],
}

# Configuration for each domain
DOMAIN_CONFIG: Dict[DomainType, Dict[str, Any]] = {
    DomainType.MATH: {
        "lean_imports": ["Mathlib.All"],
        "haskell_imports": ["Data.Numeral.Decimal"],
        "research_sources": ["arXiv:math", "zbMATH", "IACR"],
    },
    DomainType.PHYSICS: {
        "lean_imports": ["SciLean", "PhysLib", "Mathlib.Analysis"],
        "haskell_imports": ["Physics.Dimensional", "Data.Units.Physical"],
        "research_sources": ["NIST", "IEEE Xplore", "ASM"],
    },
    DomainType.SOFTWARE: {
        "lean_imports": ["Batteries", "Std", "Lean.Meta"],
        "haskell_imports": ["Language.Haskell", "Data.Aeson"],
        "research_sources": ["ACM Digital Library", "IEEE CS", "arXiv:cs"],
    },
    DomainType.CHEMISTRY: {
        "lean_imports": ["ChemLean", "PhysLib.Thermodynamics"],
        "haskell_imports": ["Chemistry.Structure", "Data.Molecule"],
        "research_sources": ["PubChem", "ChemRxiv", "Materials Project"],
    },
    DomainType.FINANCE: {
        "lean_imports": ["Mathlib.Probability", "Mathlib.MeasureTheory"],
        "haskell_imports": ["Finance.Yahoo", "Data.Time.Series"],
        "research_sources": ["SSRN", "NBER", "arXiv:q-fin"],
    },
    DomainType.CYBER_SEC: {
        "lean_imports": ["Lean.SMT", "Mathlib.Data.BitVec"],
        "haskell_imports": ["InfoSec.Taint", "Data.BitVector"],
        "research_sources": ["CVE MITRE DB", "RFCs", "Phrack", "Exploit-DB"],
    },
    DomainType.REVERSE_ENGINEERING: {
        "lean_imports": ["Mathlib.Data.BitVec", "Mathlib.Data.ByteArray"],
        "haskell_imports": ["Data.BitVector", "Decoding"],
        "research_sources": ["GitHub", "OEM Manuals", "Protocol Specs"],
    },
    DomainType.DOMAIN_ZERO: {
        "lean_imports": [],
        "haskell_imports": [],
        "research_sources": ["Generic literature", "API docs", "Web search"],
    },
    DomainType.GENERAL: {
        "lean_imports": ["Batteries"],
        "haskell_imports": [],
        "research_sources": ["Web search"],
    },
}


class DomainClassifier:
    """
    Classifier for determining the domain of a user task.

    Uses keyword matching to score tasks against known domains and
    returns the highest-scoring domain along with confidence level.
    """

    def __init__(self, confidence_threshold: float = 0.3):
        """
        Initialize the domain classifier.

        Args:
            confidence_threshold: Minimum score difference to claim a domain
                               as the clear winner (vs falling back to GENERAL)
        """
        self._confidence_threshold = confidence_threshold

    def classify(self, task_description: str) -> ClassificationResult:
        """
        Classify a task description into a domain.

        Args:
            task_description: The raw user prompt or task description

        Returns:
            ClassificationResult with domain, confidence, and scores
        """
        # Tokenize the input
        words = self._tokenize(task_description)

        # Check for edge cases first (they have high priority)
        edge_case_domain = self._check_edge_cases(words)
        if edge_case_domain:
            scores = self._score_all_domains(words)
            return ClassificationResult(
                primary_domain=edge_case_domain,
                confidence=ClassificationConfidence.HIGH,
                all_scores=scores,
                matched_keywords=self._get_matched_keywords(edge_case_domain, words),
            )

        # Score all domains
        scores = self._score_all_domains(words)

        # Sort by score descending
        scores.sort(key=lambda s: s.score, reverse=True)

        if not scores:
            return self._default_classification()

        primary = scores[0]
        secondary = scores[1] if len(scores) > 1 else None

        # Determine confidence
        confidence = self._determine_confidence(primary, secondary)

        # Determine fallback
        fallback = (
            scores[1].domain
            if len(scores) > 1 and scores[1].score > 0
            else DomainType.GENERAL
        )

        return ClassificationResult(
            primary_domain=primary.domain,
            confidence=confidence,
            all_scores=scores,
            matched_keywords=primary.matched_keywords,
            fallback_domain=fallback,
        )

    def classify_with_fallback(
        self, task_description: str, max_attempts: int = 3
    ) -> Tuple[ClassificationResult, List[DomainType]]:
        """
        Classify with automatic fallback on failure.

        Args:
            task_description: The task description
            max_attempts: Maximum number of domains to try

        Returns:
            Tuple of (final result, list of attempted domains)
        """
        result = self.classify(task_description)
        attempted = [result.primary_domain]

        # If initial classification has low confidence, try fallback
        if result.confidence == ClassificationConfidence.LOW:
            if result.fallback_domain and result.fallback_domain not in attempted:
                attempted.append(result.fallback_domain)
                result = ClassificationResult(
                    primary_domain=result.fallback_domain,
                    confidence=result.confidence,
                    all_scores=result.all_scores,
                    matched_keywords=[],
                    fallback_domain=DomainType.GENERAL,
                )

        return result, attempted

    def get_domain_config(self, domain: DomainType) -> Dict[str, Any]:
        """
        Get the configuration for a domain.

        Args:
            domain: The domain type

        Returns:
            Dictionary with lean_imports, haskell_imports, research_sources
        """
        return DOMAIN_CONFIG.get(domain, DOMAIN_CONFIG[DomainType.GENERAL])

    def generate_layer1_bootstrap(self, domain: DomainType) -> str:
        """
        Generate Layer 1 bootstrap content for a domain.

        Args:
            domain: The domain type

        Returns:
            Lean import statements for the domain
        """
        config = self.get_domain_config(domain)
        imports = config.get("lean_imports", [])

        if not imports:
            return ""

        return "\n".join(f"import {imp}" for imp in imports)

    def _tokenize(self, text: str) -> set:
        """Tokenize text into lowercase words."""
        words = set(re.findall(r"\b\w+\b", text.lower()))
        return words

    def _check_edge_cases(self, words: set) -> Optional[DomainType]:
        """Check if any edge case keywords match."""
        for domain, keywords in EDGE_CASE_KEYWORDS.items():
            matches = [
                kw
                for kw in keywords
                if kw.lower() in words or kw.lower() in " ".join(words)
            ]
            if matches:
                return domain
        return None

    def _score_all_domains(self, words: set) -> List[DomainScore]:
        """Score all domains against the given words."""
        scores = []
        for domain, keywords in DOMAIN_KEYWORDS.items():
            matched = [kw for kw in keywords if kw.lower() in words]
            score = len(matched) / max(len(keywords), 1)
            scores.append(
                DomainScore(
                    domain=domain,
                    score=score,
                    matched_keywords=matched,
                )
            )
        return scores

    def _get_matched_keywords(self, domain: DomainType, words: set) -> List[str]:
        """Get keywords that matched for a specific domain."""
        keywords = DOMAIN_KEYWORDS.get(domain, [])
        return [kw for kw in keywords if kw.lower() in words]

    def _determine_confidence(
        self, primary: DomainScore, secondary: Optional[DomainScore]
    ) -> ClassificationConfidence:
        """Determine the confidence level of a classification."""
        if primary.score == 0:
            return ClassificationConfidence.LOW

        if secondary is None or secondary.score == 0:
            if primary.score >= 0.1:
                return ClassificationConfidence.HIGH
            return ClassificationConfidence.MEDIUM

        # Calculate the gap between primary and secondary
        gap = primary.score - secondary.score

        # Check how many keywords matched
        match_ratio = len(primary.matched_keywords) / max(
            len(DOMAIN_KEYWORDS.get(primary.domain, [])), 1
        )

        if match_ratio >= 0.1 and gap >= 0.1:
            return ClassificationConfidence.HIGH
        elif match_ratio >= 0.05 and gap >= 0.05:
            return ClassificationConfidence.MEDIUM
        else:
            return ClassificationConfidence.LOW

    def _default_classification(self) -> ClassificationResult:
        """Return default classification for unrecognized input."""
        return ClassificationResult(
            primary_domain=DomainType.GENERAL,
            confidence=ClassificationConfidence.LOW,
            all_scores=[],
            matched_keywords=[],
            fallback_domain=DomainType.GENERAL,
        )
