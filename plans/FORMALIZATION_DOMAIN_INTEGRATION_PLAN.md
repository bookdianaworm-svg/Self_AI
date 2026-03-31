# Integration Plan: Formalization Domain Structure

**Date:** 2026-03-28  
**Status:** PLANNED  
**Priority:** HIGH

---

## Executive Summary

The Formalization Domain Structure provides the capability to handle **ANY open-ended user task with ANY level of complexity** using Lean 4/Haskell verification. The architecture is extensively documented in `plans/Formalization Domain Structure/` but is **~85% unimplemented**.

**Current State:**
- Type checking infrastructure: PARTIALLY implemented (Lean works, Haskell disabled)
- Loop modules (Fast/Slow): NOT implemented
- Redux slices for loops/domains: NOT implemented (7 slices missing)
- Config files: Exist but disabled
- Full Formalization Domain Structure: ~15% implemented

---

## Phase 0: Type Checking System Updates

### 0.1 Enable Haskell Checker

**Files to Update:**
- `config/type-checking.yaml` - Set `haskell.enabled: true`
- `rlm/environments/layer1_bootstrap.py` - Implement `_compile_haskell_types()` stub

**Reason:** Haskell provides dimensional type checking for physical units (critical for physics/engineering tasks).

### 0.2 Add Domain-Agnostic TypeChecker Interface Extension

**Files to Create:**
- `rlm/typechecking/domain_checker.py` - Abstract interface for domain-specific checkers

**Purpose:** Allow adding new checkers (Coq, Agda, etc.) without modifying core.

### 0.3 Integrate TypeCheckerRegistry with Layer1Bootstrap

**Files to Modify:**
- `rlm/environments/layer1_bootstrap.py` - Use `TypeCheckerRegistry` instead of direct checker creation
- `rlm/typechecking/registry.py` - Add `register_from_bootstrap()` method

### 0.4 Update Type Checking Tests

**Files to Create/Update:**
- `tests/typechecking/test_registry.py` - New tests for registry
- `tests/typechecking/haskell/test_ghc_checker.py` - Enable if GHC available
- `tests/typechecking/lean/test_lake_checker.py` - Expand coverage
- `tests/typechecking/test_domain_checker.py` - Tests for domain checker interface

**Test Coverage Target:** 80% for typechecking module

---

## Phase 1: Redux Slices Implementation (Foundation)

### 1.1 Create Loop Slice

**File:** `rlm/redux/slices/loop_slice.py`

**State:**
```python
@dataclass
class LoopState:
    fast_loop_active: bool
    slow_loop_active: bool
    active_candidates: Dict[str, ReleaseCandidate]
    certified_candidates: Dict[str, CertifiedCandidate]
    pending_interrupts: List[Interrupt]
    loop_metrics: LoopMetrics
```

**Actions:** `start_fast_loop`, `stop_fast_loop`, `start_slow_loop`, `stop_slow_loop`, `submit_candidate`, `certify_candidate`, `reject_candidate`, `send_interrupt`

### 1.2 Create Domain Slice

**File:** `rlm/redux/slices/domain_slice.py`

**State:**
```python
@dataclass  
class DomainState:
    active_domain: Optional[str]  # MATH, PHYSICS, SOFTWARE, CHEMISTRY, FINANCE, DOMAIN_ZERO
    domain_configs: Dict[str, DomainConfig]
    loaded_libraries: Dict[str, Layer1Context]
    classification_history: List[DomainClassification]
```

**Actions:** `classify_task`, `mount_domain_libraries`, `unmount_libraries`

### 1.3 Create Synthesis Slice

**File:** `rlm/redux/slices/synthesis_slice.py`

**State:**
```python
@dataclass
class SynthesisState:
    active_syntheses: Dict[str, SynthesisTask]
    unified_structures: Dict[str, UnifiedDomainStructure]
    genesis_proofs: Dict[str, Proof]
```

### 1.4 Create Fuzzing Slice

**File:** `rlm/redux/slices/fuzzing_slice.py`

### 1.5 Create Skunkworks Slice

**File:** `rlm/redux/slices/skunkworks_slice.py`

### 1.6 Create Ontology Slice

**File:** `rlm/redux/slices/ontology_slice.py`

### 1.7 Create Edge Slice

**File:** `rlm/redux/slices/edge_slice.py`

### 1.8 Create Tests for All Slices

**Files:** `tests/redux/test_loop_slice.py`, `test_domain_slice.py`, etc.

---

## Phase 2: Dual-Loop Architecture

### 2.1 Implement Async Message Queue

**File:** `rlm/loops/message_queue.py`

**Interface:**
```python
class AsyncMessageQueue:
    def enqueue(self, candidate: ReleaseCandidate) -> None
    def dequeue(self) -> ReleaseCandidate
    def register_handler(self, handler: Callable) -> None
```

### 2.2 Implement Fast Loop

**File:** `rlm/loops/fast_loop.py`

**Interface:**
```python
class FastLoop:
    def process_task(self, task: TaskDescriptor) -> ReleaseCandidate
    def handle_interrupt(self, interrupt: Interrupt) -> None
    def stream_to_ui(self, event: LoopEvent) -> None
```

### 2.3 Implement Slow Loop

**File:** `rlm/loops/slow_loop.py`

**Interface:**
```python
class SlowLoop:
    def verify_candidate(self, candidate: ReleaseCandidate) -> VerificationResult
    def generate_proof(self, candidate: ReleaseCandidate) -> Proof
    def certify_candidate(self, candidate: ReleaseCandidate) -> CertifiedCandidate
```

### 2.4 Implement Bounce-Back Interrupt Protocol

**File:** `rlm/loops/interrupt_protocol.py`

### 2.5 Implement Loop Manager

**File:** `rlm/loops/loop_manager.py`

### 2.6 Create Release Candidate Structure

**File:** `rlm/loops/release_candidate.py`

### 2.7 Update Config

**File:** `config/dual-loop.yaml` - Set `enabled: true`

### 2.8 Tests

**Files:** `tests/loops/test_fast_loop.py`, `test_slow_loop.py`, `test_message_queue.py`, `test_interrupt_protocol.py`, `test_loop_manager.py`, `tests/integration/test_dual_loop.py`

---

## Phase 3: Domain Routing & Dynamic Layer 1

### 3.1 Implement Domain Classifier

**File:** `rlm/routing/domain_classifier.py`

**Interface:**
```python
class DomainClassifier:
    def classify(self, task: str) -> Domain
    def get_confidence(self, task: str, domain: Domain) -> float
    def extract_keywords(self, task: str) -> List[str]
```

### 3.2 Implement Domain Router

**File:** `rlm/routing/domain_router.py`

### 3.3 Implement Dynamic Layer 1 Loader

**File:** `rlm/layer1/dynamic_loader.py`

**Interface:**
```python
class DynamicLayer1Loader:
    def load_domain_libraries(self, domain: Domain) -> Layer1Context
    def generate_bootstrap_file(self, domain: Domain) -> str
    def get_available_domains(self) -> List[Domain]
```

### 3.4 Update Layer1Bootstrap

**File:** `rlm/environments/layer1_bootstrap.py`
- Add dynamic loading methods
- Implement library management

### 3.5 Create Domain Config

**File:** `config/domain-routing.yaml`

### 3.6 Update Backend Router

**File:** `rlm/routing/backend_router.py`
- Add domain-based routing rules

### 3.7 Tests

**Files:** `tests/routing/test_domain_classifier.py`, `tests/routing/test_domain_router.py`, `tests/layer1/test_dynamic_loader.py`, `tests/integration/test_domain_routing.py`

---

## Phase 4: Cross-Domain Synthesis & Skunkworks

### 4.1 Implement Cross-Domain Synthesis Engine

**File:** `rlm/synthesis/cross_domain_engine.py`

### 4.2 Implement Matrix Engine

**File:** `rlm/synthesis/matrix_engine.py`

### 4.3 Implement Genesis Prover

**File:** `rlm/synthesis/genesis_prover.py`

### 4.4 Implement Skunkworks Protocol

**File:** `rlm/skunkworks/skunkworks_protocol.py`

### 4.5 Implement Discovery Phase

**File:** `rlm/skunkworks/discovery_phase.py`

### 4.6 Implement Justification Phase

**File:** `rlm/skunkworks/justification_phase.py`

### 4.7 Create Synthesis Config

**File:** `config/cross-domain-synthesis.yaml`

### 4.8 Create Skunkworks Config

**File:** `config/skunkworks.yaml`

### 4.9 Tests

**Files:** `tests/synthesis/test_cross_domain_engine.py`, `tests/skunkworks/test_skunkworks_protocol.py`, `tests/integration/test_cross_domain_synthesis.py`, `tests/integration/test_skunkworks.py`

---

## Phase 5: Empirical Fuzzing & Universal Ontology

### 5.1 Implement Black-Box Sandbox

**File:** `rlm/fuzzing/black_box_sandbox.py`

### 5.2 Implement Automata Learner (L* Algorithm)

**File:** `rlm/fuzzing/automata_learner.py`

### 5.3 Implement FSM Generator

**File:** `rlm/fuzzing/fsm_generator.py`

### 5.4 Implement Universal Ontology Bootstrapping

**File:** `rlm/ontology/universal_ontology.py`

### 5.5 Implement Domain Zero

**File:** `rlm/ontology/domain_zero.py`

### 5.6 Implement Naked Axiom Ban

**File:** `rlm/ontology/naked_axiom_ban.py`

### 5.7 Create Fuzzing Config

**File:** `config/empirical-fuzzing.yaml`

### 5.8 Create Ontology Config

**File:** `config/universal-ontology.yaml`

### 5.9 Tests

**Files:** `tests/fuzzing/test_automata_learner.py`, `tests/ontology/test_universal_ontology.py`, `tests/integration/test_empirical_fuzzing.py`

---

## Phase 6: Advanced Edge Domains

### 6.1 Implement Advanced Edge Domains

**File:** `rlm/edge/advanced_edge_domains.py`

### 6.2 Implement User Overrides

**File:** `rlm/edge/user_overrides.py`

### 6.3 Implement Cybersecurity Tools

**File:** `rlm/edge/cybersec_tools.py`

### 6.4 Implement Reverse Engineering

**File:** `rlm/edge/reverse_engineering.py`

### 6.5 Create Edge Config

**File:** `config/advanced-edge-domains.yaml`

### 6.6 Tests

**Files:** `tests/edge/test_advanced_edge_domains.py`, `tests/integration/test_edge_domains.py`

---

## Test Coverage Requirements

| Phase | Target Coverage |
|-------|----------------|
| Phase 0 (Type Checking) | 80% |
| Phase 1 (Redux Slices) | 85% |
| Phase 2 (Dual-Loop) | 80% |
| Phase 3 (Domain Routing) | 80% |
| Phase 4 (Synthesis/Skunkworks) | 75% |
| Phase 5 (Fuzzing/Ontology) | 70% |
| Phase 6 (Edge) | 70% |

---

## Implementation Order (Dependencies)

```
Phase 0 (Type Checking)
         ↓
Phase 1 (Redux Slices) ← Foundation for ALL phases
         ↓
Phase 2 (Dual-Loop) ← Depends on Phase 1
         ↓
Phase 3 (Domain Routing) ← Depends on Phase 1
         ↓
Phase 4 (Synthesis/Skunkworks) ← Depends on Phase 1, 2, 3
         ↓
Phase 5 (Fuzzing/Ontology) ← Depends on Phase 1
         ↓
Phase 6 (Edge) ← Depends on Phase 3
```

---

## Files to Create/Modify Summary

| Phase | Create | Modify |
|-------|--------|--------|
| 0 | 2 | 3 |
| 1 | 7 slices | 1 (store) |
| 2 | 5 | 2 |
| 3 | 3 | 4 |
| 4 | 7 | 2 |
| 5 | 5 | 1 |
| 6 | 4 | 1 |
| **Total** | **33** | **14** |

---

## Rollback Strategy

1. Feature flags for all major features
2. Config-based enable/disable for each phase
3. Each phase independently testable
4. Incremental integration - no big bang

---

## Success Criteria

1. All type checking tests pass (Lean + Haskell)
2. All 7 new Redux slices implemented and tested
3. Dual-loop architecture functional
4. Domain routing correctly classifies and loads libraries
5. Cross-domain synthesis works for 2+ domains
6. Skunkworks discovery/justification loop functional
7. Domain Zero bootstrapping works for novel domains
8. Test coverage meets targets per phase
