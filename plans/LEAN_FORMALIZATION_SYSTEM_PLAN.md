# Plan: Lean 4 Domain-Agnostic Formalization System

**Date:** 2026-03-29
**Goal:** Get Lean 4 formalization pipeline running for Software/Math, plan for Physics integration
**Status:** PLANNED

---

## Executive Summary

This plan establishes a Lean 4-based domain-agnostic formalization system that allows any user to input a task and receive verified output. The system uses formal verification as a quality gate while supporting multiple domains through configurable domain libraries.

### Core Architecture

```
User Task → Domain Classification → Formal Spec (Genesis) → Code Generation → Verification → Output
              ↓
        ┌─────────────────────────────────────────┐
        │           Lean 4 Kernel                  │
        │  (Domain-Agnostic Verification)         │
        │                                          │
        │  • Software/Math: Mathlib             │
        │  • Physics: PhysLean, SciLean         │
        │  • Custom: Layer 1.5 Axioms           │
        └─────────────────────────────────────────┘
```

---

## Phase 1: Enable Current Software/Math Pipeline

### 1.1 Assessment Summary

| Component | Status | Action Required |
|-----------|--------|-----------------|
| **Domain Classification** | ✅ Working | None |
| **Lean 4 Integration** | ⚠️ Partial | Fix subprocess calls, enable |
| **Haskell Type Checking** | ⚠️ Partial | Fix subprocess calls, enable |
| **Type Checker Registry** | ✅ Working | None |
| **Verification Redux Slice** | ✅ Working | None |
| **Verification Middleware** | ✅ Working | None |
| **Verification Agents** | ⚠️ Framework | Need real Lean/Haskell tools |
| **Dual-Loop Config** | ❌ Disabled | Enable `dual_loop.yaml` |

### 1.2 Enable Dual-Loop Configuration

**File:** `config/dual-loop.yaml`

**Current State:**
```yaml
dual_loop:
  enabled: false  # <-- Disabled
```

**Action:**
```yaml
dual_loop:
  enabled: true  # Enable formalization pipeline
```

### 1.3 Fix Type Checker Subprocess Issues

**Issue:** Subprocess calls have type annotation errors (GHCChecker, LakeChecker)

**Files to review:**
- `rlm/typechecking/haskell/ghc_checker.py`
- `rlm/typechecking/lean/lake_checker.py`

**Issue:** `ghc_cmd: Optional[str]` and `lean_cmd: Optional[str]` type annotations causing issues

**Fix:** Ensure subprocess calls handle Optional[str> correctly

### 1.4 Verify Lean 4 Installation

**Requirement:** Lean 4 installed at system level or via Lake

**Check:**
```bash
lean --version  # or
lake --version
```

**If missing:** Document installation requirement

### 1.5 Create Simple Test Case

**Test Case:** Simple function with type specification

```
Task: "Write a function that takes two integers and returns their sum"

Expected Flow:
1. Classify as SOFTWARE domain
2. Generate Lean type signature
3. Verify compilation
4. Output verified code
```

---

## Phase 2: Establish Verification Pipeline

### 2.1 Verification Flow for Software/Math

```
┌─────────────────────────────────────────────────────────────────┐
│  1. USER INPUT                                                  │
│     "Create a function that sorts a list"                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. DOMAIN CLASSIFICATION                                       │
│     → SOFTWARE domain (via keywords)                            │
│     → Lean imports: Batteries, Std, Lean.Meta                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. FORMAL SPEC GENERATION (Genesis)                           │
│     Lean:                                                         │
│     ```lean                                                      │
│     def sort_list {α : Type} [Ord α] (xs : List α) : List α │
│     -- satisfies: sorted result AND permutation of input         │
│     ```                                                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. CODE GENERATION                                             │
│     Agent generates code satisfying spec                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. VERIFICATION (Lean 4 Kernel)                               │
│     lake --check generated_code.lean                             │
│     ├── SUCCESS → Certified output                               │
│     └── FAIL → Return to step 4 (self-heal)                    │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Verification Levels (User Choice)

| Level | Meaning | Use Case |
|-------|---------|----------|
| **NONE** | No verification | Quick prototyping |
| **BASIC** | Type syntax check | Basic correctness |
| **CONSISTENCY** | Genesis proof | Structure verification |
| **CORRECTNESS** | Full proof verification | Academic/critical |

### 2.3 Self-Healing Loop

**When verification fails:**
1. Agent receives error details
2. Agent modifies code
3. Re-submit for verification
4. Repeat (up to N retries)
5. If exhausted, escalate to user

**Implementation:**
```python
MAX_RETRIES = 3

def verify_with_retry(code, spec, retries=MAX_RETRIES):
    for i in range(retries):
        result = verify(code, spec)
        if result.passed:
            return result
        code = regenerate(code, result.error)
    return result  # Return last failure
```

---

## Phase 3: Domain Library Configuration

### 3.1 Domain-Agnostic Library Structure

```
rlm/layer1/
├── __init__.py
├── dynamic_loader.py          # Domain-specific bootstrap generation
├── lean/                     # Lean 4 configuration
│   └── lake-manifest.json
├── haskell/                  # Haskell type configuration
│   └── package.yaml
└── user_axioms/              # User-provided Layer 1.5
```

### 3.2 Software/Math Library Configuration

**Lean Imports:**
- `Batteries` - Extended standard library
- `Std` - Standard library utilities
- `Lean.Meta` - Metaprogramming support

**Haskell Imports:**
- `Data.List` - List operations
- `Data.Maybe` - Maybe monad
- `Control.Monad` - Monad utilities

### 3.3 Domain-Specific Verification Rules

**Software:**
```lean
-- Example: Function specification
@[simp]
def sort_list {α : Type} [Ord α] (xs : List α) : List α :=
  match xs with
  | [] => []
  | x :: xs' => insert x (sort_list xs')

-- Verification: Output is sorted AND permutation of input
theorem sort_list_sorted {α : Type} [Ord α] (xs : List α) :
  sorted (sort_list xs) := by sorry

theorem sort_list_perm {α : Type} [Ord α] (xs : List α) :
  permutation (sort_list xs) xs := by sorry
```

---

## Phase 4: Physics Library Integration (Future)

### 4.1 Target Libraries

| Library | Purpose | Status |
|---------|---------|--------|
| **PhysLean** | Physics formalization | External, needs integration |
| **SciLean** | Scientific computing | External, needs integration |
| **Mathlib** | Mathematics | Installed, working |

### 4.2 Integration Steps

1. **Locate PhysLean/SciLean repositories**
   - Check Lean's community GitHub org
   - Verify installation via `lake env`

2. **Configure Layer 1 Bootstrap**
   ```python
   # rlm/environments/layer1_bootstrap.py
   PHYS_LEAN_IMPORTS = [
       "PhysLean.Mechanics",
       "PhysLean.Thermodynamics", 
       "PhysLean.Electromagnetism",
   ]
   
   SCI_LEAN_IMPORTS = [
       "SciLean.Analysis",
       "SciLean.Numerics",
   ]
   ```

3. **Add Physics Domain Config**
   ```python
   DOMAIN_CONFIG[DomainType.PHYSICS] = {
       "lean_imports": PHYS_LEAN_IMPORTS,
       "haskell_imports": ["Physics.Dimensional", "Data.Units.SI"],
       "research_sources": ["NIST", "arXiv:physics"],
   }
   ```

4. **Verify Integration**
   ```
   Task: "Create a heat engine with 40% efficiency"
   
   Verification:
   1. Formalize thermodynamics constraints
   2. Lean proves: Carnot efficiency < 100%
   3. Check: 40% < Carnot limit for given temperatures
   ```

### 4.3 External Source Integration

| Source | Integration Method | Priority |
|--------|-------------------|----------|
| **arXiv** | arXiv API + paper parsing | High |
| **NIST** | NIST Web API for constants | High |
| **PubChem** | PubChem REST API | Medium |
| **Materials Project** | Materials Project API | Low |

---

## Phase 5: User Interaction Model

### 5.1 Verification Level Selection

**At task submission, user sees:**

```
┌─────────────────────────────────────────────────────────────┐
│  Verification Level                                        │
│                                                             │
│  ○ None     - No verification (fastest)                   │
│  ○ Basic    - Type checking only                           │
│  ● Standard - Genesis proof (recommended)                  │
│  ○ Full     - Complete formal verification                 │
│                                                             │
│  ☑ Allow AI to adjust level if needed                    │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Pause Points

**System pauses and prompts user:**

1. **Source Approval** - When external sources conflict
2. **Verification Failure** - After N retries, escalate
3. **Level Recommendation** - If AI suggests higher level
4. **Manual Override** - User can intervene anytime

### 5.3 User Actions at Pause

| Action | Behavior |
|--------|----------|
| **Continue** | Proceed with current state |
| **Adjust Level** | Change verification level |
| **Provide Input** | User submits their own answer |
| **Cancel** | Abort task |
| **Regenerate** | Force regeneration from formal spec |

---

## Phase 6: Quality Assurance

### 6.1 Test Cases Required

| Test | Domain | Verification Level | Expected |
|------|--------|-------------------|----------|
| Simple addition | Math | BASIC | Pass |
| List sort | Software | STANDARD | Genesis proof |
| Binary search | Software | STANDARD | Full proof |
| Quick sort | Software | NONE | Skip |
| Heat engine | Physics | CORRECTNESS | Physics constraints |

### 6.2 Success Criteria

1. **Compilation:** All code compiles in Lean 4
2. **Type Safety:** Haskell type checker passes
3. **Self-Healing:** Failed verification regenerates correctly
4. **User Control:** Verification level changes are honored
5. **Performance:** Simple tasks complete in < 30 seconds

---

## Implementation Order

### Week 1: Foundation
- [ ] Enable dual-loop configuration
- [ ] Fix type checker subprocess issues
- [ ] Verify Lean 4 installation
- [ ] Create simple test case (addition function)

### Week 2: Verification Pipeline
- [ ] Implement self-healing loop
- [ ] Add verification level selection UI
- [ ] Create pause point handlers
- [ ] Test regeneration flow

### Week 3: Software/Math Library
- [ ] Configure Software domain Lean imports
- [ ] Add Haskell type libraries
- [ ] Test sort function verification
- [ ] Test binary search with proofs

### Week 4: Integration & Polish
- [ ] End-to-end test with user interaction
- [ ] Performance optimization
- [ ] Error handling improvements
- [ ] Documentation

### Future: Physics Integration
- [ ] Locate and install PhysLean
- [ ] Configure physics domain
- [ ] Test thermodynamics constraints
- [ ] Integrate arXiv API

---

## Open Questions

1. **Lean 4 Installation:** Should we bundle Lean 4 or require user installation?
2. **Self-Healing Retries:** Default N=3, configurable?
3. **Haskell Optional:** Require Haskell for type checking or make optional?
4. **Performance SLA:** What's acceptable latency for verification?

---

## Dependencies

| Dependency | Source | Required For |
|-----------|--------|--------------|
| Lean 4 | github.com/leanprover/lean4 | Formal verification |
| Lake | github.com/leanprover/lake | Lean build system |
| Mathlib | github.com/leanprover-community/mathlib4 | Mathematics |
| GHC | ghc.gitlab.haskell.org | Haskell type checking |

---

## Files to Modify

| File | Change |
|------|--------|
| `config/dual-loop.yaml` | Enable dual-loop |
| `rlm/typechecking/haskell/ghc_checker.py` | Fix subprocess types |
| `rlm/typechecking/lean/lake_checker.py` | Fix subprocess types |
| `rlm/environments/layer1_bootstrap.py` | Add physics config |
| `rlm/routing/domain_classifier.py` | Add physics sources |
| `tests/formalization/` | Create test suite |

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Test pass rate | > 90% |
| Verification time (simple) | < 5 seconds |
| Verification time (complex) | < 60 seconds |
| Self-healing success | > 70% |
| User satisfaction | > 80% |

---

## Notes

- **Domain-Agnosticism:** Achieved through configurable Lean imports per domain
- **Quality Gate:** Formal verification ensures output correctness
- **User Control:** Verification level always user-selectable
- **Extensibility:** Adding domains = adding library configurations
