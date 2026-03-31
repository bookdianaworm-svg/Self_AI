# Type Checking System - Deployment Integration Plan

**Version:** 1.0  
**Date:** 2026-03-28  
**Status:** Ready for Integration  
**Dependency:** 
- `.kilo/plans/1774673361830-gentle-otter.md` (Type Checking System Implementation Plan)
- `docs/deployment.md` (Deployment Guide - Phase 0)

---

## Overview

This plan coordinates the **Type Checking System Implementation Plan** with the **Deployment Guide** to ensure type checking (GHC for Haskell, Lake for Lean 4) is properly deployed as part of the overall system setup.

### Relationship Between Documents

| Document | Purpose | Phase |
|----------|---------|-------|
| `docs/deployment.md` | System-wide deployment instructions | Phase 0 (prerequisite) |
| `.kilo/plans/1774673361830-gentle-otter.md` | Type checking implementation details | 21-day sprint |
| **This document** | Coordinate both documents | Integration layer |

---

## Integration Points

### 1. Configuration Alignment

The deployment guide specifies `config/type-checking.yaml` structure. The implementation plan details the code that reads this config.

**Deployment Guide (Line 477-489):**
```yaml
# config/type-checking.yaml
haskell:
  enabled: true
  ghc_path: "ghc"
  timeout_seconds: 30

lean:
  enabled: true
  lake_path: "lake"
  mathlib: true
  timeout_seconds: 60
```

**Implementation Plan (Line 201):**
```
- config/type-checking.yaml
```

**Coordination:** These must remain synchronized. The implementation plan creates the config file matching the deployment guide specification.

### 2. Installation Instructions Alignment

**Deployment Guide (Lines 413-473):**

| Component | Install Command | Verify Command |
|-----------|-----------------|----------------|
| GHC (Ubuntu) | `sudo apt-get install -y ghc libghc-dimensions-dev` | `ghc --version` |
| GHC (macOS) | `brew install ghc cabal-install` | `ghc --version` |
| Lean (Ubuntu) | `elan toolchain install leanprover/lean4:v4.8.0` | `lake --version` |
| Lean (macOS) | `brew install leanprover/lean/elan` | `lake --version` |
| Lean (Windows) | `scoop install elan` | `lake --version` |

**Implementation Plan - Day 1-3 (Foundation):**
- No external tool installation required
- Focuses on abstraction layer and interfaces

**Implementation Plan - Day 4-7 (Haskell):**
- Assumes GHC is pre-installed (per deployment guide)
- Implements Python wrapper around GHC

**Implementation Plan - Day 8-12 (Lean):**
- Assumes Lake is pre-installed (per deployment guide)
- Implements Python wrapper around Lake

### 3. File Manifest Alignment

The implementation plan creates:
```
rlm/typechecking/__init__.py
rlm/typechecking/base.py
rlm/typechecking/result.py
rlm/typechecking/exceptions.py
rlm/typechecking/config.py
rlm/typechecking/registry.py
rlm/typechecking/haskell/__init__.py
rlm/typechecking/haskell/haskell_checker.py
rlm/typechecking/haskell/ghc_checker.py
rlm/typechecking/haskell/result.py
rlm/typechecking/lean/__init__.py
rlm/typechecking/lean/lean_checker.py
rlm/typechecking/lean/lake_checker.py
rlm/typechecking/lean/result.py
config/type-checking.yaml
tests/typechecking/__init__.py
tests/typechecking/haskell/__init__.py
tests/typechecking/haskell/test_ghc_checker.py
tests/typechecking/lean/__init__.py
tests/typechecking/lean/test_lake_checker.py
tests/typechecking/test_integration.py
```

The deployment guide references:
- `config/type-checking.yaml` (line 309, 477)
- Type checking as "Phase 0" (line 602)

**Gap:** The deployment guide does NOT reference the `rlm/typechecking/` directory structure. This coordination document ensures consistency.

---

## Implementation Sequence

### Phase 0: Infrastructure (Deployment Guide)

This is already documented in `docs/deployment.md`. Execute before implementation.

```bash
# 1. Install GHC
sudo apt-get install -y ghc libghc-dimensions-dev  # Ubuntu
# or: brew install ghc cabal-install              # macOS

# 2. Install Lean 4 via elan
elan toolchain install leanprover/lean4:v4.8.0
elan default leanprover/lean4:v4.8.0

# 3. Verify installations
ghc --version
lake --version
```

### Phase 1-3: Type Checking Implementation (21 days)

See `.kilo/plans/1774673361830-gentle-otter.md` for detailed 21-day sprint plan.

| Week | Days | Focus | Deliverables |
|------|------|-------|--------------|
| 1 | 1-3 | Foundation | base.py, result.py, exceptions.py, registry.py |
| 1 | 4-7 | Haskell | ghc_checker.py, haskell/result.py, tests |
| 2 | 8-12 | Lean | lake_checker.py, lean/result.py, tests |
| 3 | 13-16 | Integration | LocalREPL, Redux, VerificationAgentFactory |
| 3 | 17-18 | Config | config/type-checking.yaml, config_loader.py |
| 3 | 19-21 | Testing | Integration tests, documentation |

---

## Verification Workflow

After implementation, verify the entire system:

### 1. Installation Verification (from Deployment Guide)

```bash
# GHC
ghc --version
# Expected: The Glorious Glasgow Haskell Compilation System, version x.x.x

# Lake
lake --version
# Expected: Lake version x.x.x
```

### 2. Configuration Verification

```bash
# Check config file exists and is valid
cat config/type-checking.yaml
```

### 3. Python Module Verification

```bash
# Check type checking module loads
python -c "from rlm.typechecking import TypeCheckerRegistry; print('OK')"

# Check GHC checker
python -c "from rlm.typechecking.haskell import GHCChecker; c = GHCChecker(); print(c.health_check())"

# Check Lake checker
python -c "from rlm.typechecking.lean import LakeChecker; c = LakeChecker(); print(c.health_check())"
```

### 4. Functional Verification (from Implementation Plan)

```bash
# Haskell type check
python -c "
from rlm.typechecking.haskell import GHCChecker
c = GHCChecker()
result = c.check('x :: Int; x = \"hello\"')
print(result.success, result.errors)
"

# Lean verification
python -c "
from rlm.typechecking.lean import LakeChecker
c = LakeChecker()
result = c.verify('theorem test : 1 = 2 := rfl')
print(result.success, result.errors)
"
```

---

## Troubleshooting Alignment

### Deployment Guide Troubleshooting (Line 566-577)

```bash
# Verify GHC installation
ghc --version

# Verify Lake installation
lake --version

# Check configuration
cat config/type-checking.yaml
```

### Implementation Plan Troubleshooting

| Error Code | Meaning | Resolution |
|------------|---------|------------|
| HC001 | Haskell checker not available | Install GHC, verify ghc_path in config |
| HC002 | Haskell type error | Fix code based on error message |
| HC003 | Haskell timeout | Increase timeout_seconds in config |
| LN001 | Lean checker not available | Install Lake, verify lake_path in config |
| LN002 | Lean type error | Fix theorem based on error message |
| LN003 | Lean timeout | Increase timeout_seconds in config |

---

## Next Steps After Type Checking

### Integration with Dual-Loop (Phase 2)

The Type Checking System feeds into the Dual-Loop Architecture:

```
Fast Loop (System 1)
    ↓ Release Candidate
Async Message Queue
    ↓
Slow Loop (System 2)
    ↓
Type Checkers (Haskell/GHC + Lean/Lake)
    ↓
Verification Result
    ↓
Bounce-Back Interrupt (if failed)
    ↓
Fast Loop (retry)
```

### Integration with Domain Routing (Phase 3)

Type checkers provide verification oracle for domain classification:

```
Task → Domain Classifier → Domain-Specific Layer 1
                              ↓
                        Type Checker Verification
                              ↓
                     Certified vs Uncertified Domain
```

---

## File Summary

| File | Location | Purpose |
|------|----------|---------|
| Type Checking Implementation Plan | `.kilo/plans/1774673361830-gentle-otter.md` | 21-day implementation sprint |
| Deployment Guide | `docs/deployment.md` | System deployment instructions |
| Type Checking Deployment Integration | `.kilo/plans/1774673361830-type-checking-deployment.md` | **This document** - coordinates both |

---

**Plan Status:** Ready for integration  
**Next Action:** Execute Phase 0 from deployment guide, then begin implementation plan
