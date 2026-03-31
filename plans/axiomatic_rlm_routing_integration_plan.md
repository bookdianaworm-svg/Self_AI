# Axiomatic Seed & RLM Routing Integration Plan

**Version**: 1.0  
**Purpose**: Comprehensive integration plan for Layer 1 Axiomatic Foundation and RLM routing upgrades into existing RLM+Redux swarm system  
**Status**: Integration Specification  
**Date**: 2026-03-25

---

## Executive Summary

This document provides a detailed plan for integrating two major additions into the existing RLM-based swarm system:

1. **Layer 1 Axiomatic Foundation** - Immutable mathematical and physical verification layer using Lean 4 and Haskell
2. **RLM Routing Upgrades** - Dynamic backend and environment routing for sub-calls

The integration is designed to be **non-disruptive**, adding new capabilities while preserving all existing functionality. The plan follows an incremental approach with clear rollback points.

---

## Current System Architecture

### Existing Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    RLM Swarm System                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐  │
│  │         Redux Store (State Management)                  │  │
│  │  - Agent State, Task State, Message State              │  │
│  │  - System State, Tool State, Improvement State         │  │
│  └────────────────────┬────────────────────────────────────┘  │
│                     │                                        │
│  ┌────────────────────┴────────────────────────────────────┐  │
│  │         Main RLM Orchestrator (LocalREPL)             │  │
│  │  - Recursive task decomposition                        │  │
│  │  - Dynamic agent spawning                              │  │
│  │  - Custom tools management                             │  │
│  └────────────────────┬────────────────────────────────────┘  │
│                     │                                        │
│  ┌────────────────────┴────────────────────────────────────┐  │
│  │         Backend Clients                                 │  │
│  │  - OpenAI, Anthropic, Gemini, Portkey, LiteLLM       │  │
│  └────────────────────┬────────────────────────────────────┘  │
│                     │                                        │
│  ┌────────────────────┴────────────────────────────────────┐  │
│  │         Execution Environments                          │  │
│  │  - LocalREPL, DockerREPL, ModalREPL, E2B, Daytona  │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Existing Features

- **Recursive sub-call mechanism** via `RLM._subcall()` method
- **Custom tools** injection via `custom_tools` and `custom_sub_tools` parameters
- **Persistent mode** for multi-turn conversations
- **Callback system** for monitoring sub-calls (`on_subcall_start`, `on_subcall_complete`)
- **Multiple backend support** via `other_backends` parameter
- **Multiple environment support** via pluggable environment system

---

## Integration Overview

### High-Level Integration Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Integrated RLM+Verification System               │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │              Redux Store (Enhanced)                          │   │
│  │  - Agent State, Task State, Message State                     │   │
│  │  - System State, Tool State, Improvement State                │   │
│  │  + Verification State (NEW)                                  │   │
│  │  + Routing State (NEW)                                       │   │
│  └────────────────────┬───────────────────────────────────────────┘   │
│                       │                                            │
│  ┌────────────────────┴───────────────────────────────────────────┐   │
│  │         Main RLM Orchestrator (LocalREPL + Layer 1)          │   │
│  │  - Recursive task decomposition                               │   │
│  │  - Dynamic agent spawning                                     │   │
│  │  - Task descriptor generation (NEW)                            │   │
│  │  - Backend/Environment routing (NEW)                           │   │
│  │  - Verification orchestration (NEW)                            │   │
│  └────────────────────┬───────────────────────────────────────────┘   │
│                       │                                            │
│  ┌────────────────────┴───────────────────────────────────────────┐   │
│  │         Backend Router (NEW)                                   │   │
│  │  - Backend selection based on task descriptors                  │   │
│  │  - Metrics tracking for adaptive routing                       │   │
│  └────────────────────┬───────────────────────────────────────────┘   │
│                       │                                            │
│  ┌────────────────────┴───────────────────────────────────────────┐   │
│  │         Environment Router (NEW)                                │   │
│  │  - Environment selection based on capabilities                   │   │
│  │  - Security and isolation decisions                            │   │
│  └────────────────────┬───────────────────────────────────────────┘   │
│                       │                                            │
│  ┌────────────────────┴───────────────────────────────────────────┐   │
│  │         Backend Clients (Enhanced)                              │   │
│  │  - OpenAI, Anthropic, Gemini, Portkey, LiteLLM               │   │
│  │  + RLM Internal (for verification sub-calls) (NEW)            │   │
│  └────────────────────┬───────────────────────────────────────────┘   │
│                       │                                            │
│  ┌────────────────────┴───────────────────────────────────────────┐   │
│  │         Execution Environments (Enhanced)                        │   │
│  │  - LocalREPL (with Lean 4 + Haskell) (ENHANCED)              │   │
│  │  - DockerREPL (with optional verification tools) (ENHANCED)    │   │
│  │  - ModalREPL, E2B, Daytona                                   │   │
│  └────────────────────┬───────────────────────────────────────────┘   │
│                       │                                            │
│  ┌────────────────────┴───────────────────────────────────────────┐   │
│  │         Layer 1 Axiomatic Foundation (NEW)                      │   │
│  │  - Mathlib (Lean 4)                                          │   │
│  │  - PhysLib/SciLean (Lean 4)                                  │   │
│  │  - Haskell Dimensional Types                                   │   │
│  └────────────────────┬───────────────────────────────────────────┘   │
│                       │                                            │
│  ┌────────────────────┴───────────────────────────────────────────┐   │
│  │         Verification Agents (NEW)                               │   │
│  │  - Autoformalization Agent                                     │   │
│  │  - Verifier Agent (Lean Kernel Oracle)                        │   │
│  │  - Cross-Check Agent                                          │   │
│  │  - Physicist Agent                                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Part 1: Layer 1 Axiomatic Foundation Integration

### 1.1 Integration Strategy

Layer 1 is **loaded once at swarm initialization** and remains immutable. It provides the verification oracle that all Layer 2 theorems must satisfy.

### 1.2 Integration Points

| Component | Integration Method | Impact |
|-----------|------------------|--------|
| **LocalREPL** | Pre-load Lean 4 kernel with Mathlib, PhysLib, SciLean at startup | Medium - requires environment setup |
| **RLM.__init__** | Add Layer 1 loading parameter and verification flag | Low - optional parameter |
| **Custom Tools** | Add verification tools to `custom_tools` registry | Low - non-breaking addition |
| **Redux Store** | Add `VerificationState` slice for tracking verification status | Low - new slice only |

### 1.3 Implementation Steps

#### Step 1: Environment Setup

```python
# rlm/environments/layer1_bootstrap.py (NEW FILE)

import subprocess
import os
from pathlib import Path

class Layer1Bootstrap:
    """
    Manages loading and initialization of Layer 1 Axiomatic Foundation.
    """
    
    def __init__(self, layer1_path: str | None = None):
        self.layer1_path = layer1_path or self._default_layer1_path()
        self.lean_kernel = None
        self.haskell_compiler = None
        self.loaded = False
    
    def _default_layer1_path(self) -> str:
        """Return default path to Layer 1 libraries."""
        return os.path.join(os.path.dirname(__file__), "..", "layer1")
    
    def load_layer1(self) -> dict:
        """
        Load Layer 1 axioms and return initialization status.
        
        Returns:
            dict with keys: 'success', 'mathlib_version', 'physlib_version', 
                          'load_time_ms', 'memory_mb'
        """
        if self.loaded:
            return {"success": True, "cached": True}
        
        import time
        start_time = time.perf_counter()
        
        try:
            # Load Lean 4 with Mathlib
            self.lean_kernel = self._load_lean_kernel()
            
            # Load PhysLib/SciLean
            self._load_physlib()
            
            # Compile Haskell dimensional types
            self._compile_haskell_types()
            
            load_time = (time.perf_counter() - start_time) * 1000
            
            self.loaded = True
            
            return {
                "success": True,
                "mathlib_version": self._get_mathlib_version(),
                "physlib_version": self._get_physlib_version(),
                "load_time_ms": load_time,
                "memory_mb": self._get_memory_usage()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "load_time_ms": (time.perf_counter() - start_time) * 1000
            }
    
    def _load_lean_kernel(self):
        """Load Lean 4 kernel with Mathlib."""
        # Implementation depends on Lean 4 Python bindings
        pass
    
    def _load_physlib(self):
        """Load PhysLib/SciLean into Lean kernel."""
        pass
    
    def _compile_haskell_types(self):
        """Compile Haskell dimensional type checker."""
        pass
    
    def get_verification_oracle(self):
        """Return the verification oracle for use by agents."""
        if not self.loaded:
            raise RuntimeError("Layer 1 not loaded. Call load_layer1() first.")
        return {
            "lean_kernel": self.lean_kernel,
            "haskell_types": self.haskell_compiler
        }
```

#### Step 2: Enhance LocalREPL

```python
# rlm/environments/local_repl.py (MODIFICATION)

from rlm.environments.layer1_bootstrap import Layer1Bootstrap

class LocalREPL(BaseEnv):
    def __init__(self, lm_handler_address, context_payload, depth, **kwargs):
        # ... existing initialization ...
        
        # NEW: Layer 1 support
        self.enable_layer1 = kwargs.get("enable_layer1", False)
        self.layer1_bootstrap = None
        self.verification_oracle = None
        
        if self.enable_layer1:
            self.layer1_bootstrap = Layer1Bootstrap(
                layer1_path=kwargs.get("layer1_path")
            )
            layer1_status = self.layer1_bootstrap.load_layer1()
            if layer1_status["success"]:
                self.verification_oracle = self.layer1_bootstrap.get_verification_oracle()
                # Add verification tools to globals
                self._add_verification_tools()
            else:
                self.logger.warning(f"Layer 1 loading failed: {layer1_status.get('error')}")
    
    def _add_verification_tools(self):
        """Add verification tools to the REPL globals."""
        verification_tools = {
            "verify_lean": self._verify_lean,
            "check_haskell_types": self._check_haskell_types,
            "get_layer1_axioms": self._get_layer1_axioms,
            "prove_theorem": self._prove_theorem
        }
        self.globals.update(verification_tools)
    
    def _verify_lean(self, lean_code: str) -> dict:
        """Verify Lean 4 code against Layer 1 axioms."""
        if not self.verification_oracle:
            return {"success": False, "error": "Layer 1 not available"}
        
        # Use Lean kernel to verify
        # Implementation depends on Lean 4 Python bindings
        pass
    
    def _check_haskell_types(self, haskell_code: str) -> dict:
        """Check Haskell code for dimensional type correctness."""
        if not self.verification_oracle:
            return {"success": False, "error": "Layer 1 not available"}
        
        # Use Haskell compiler to check types
        pass
    
    def _get_layer1_axioms(self) -> dict:
        """Return available Layer 1 axioms."""
        if not self.verification_oracle:
            return {}
        
        # Return axiom registry
        pass
    
    def _prove_theorem(self, theorem_statement: str) -> dict:
        """Attempt to prove a theorem using Lean kernel."""
        if not self.verification_oracle:
            return {"success": False, "error": "Layer 1 not available"}
        
        # Use Lean kernel + LeanDojo for proof synthesis
        pass
```

#### Step 3: Add Redux Verification State

```python
# rlm/redux/slices/verification_slice.py (NEW FILE)

from dataclasses import dataclass
from typing import Optional, Dict, List
from enum import Enum

class VerificationStatus(Enum):
    PENDING = "pending"
    LOADING = "loading"
    LOADED = "loaded"
    FAILED = "failed"
    VERIFYING = "verifying"
    PASSED = "passed"
    FAILED_VERIFICATION = "failed_verification"

@dataclass
class Layer1State:
    """State of Layer 1 Axiomatic Foundation."""
    status: VerificationStatus = VerificationStatus.PENDING
    mathlib_version: Optional[str] = None
    physlib_version: Optional[str] = None
    load_time_ms: Optional[float] = None
    memory_mb: Optional[float] = None
    error: Optional[str] = None

@dataclass
class TheoremVerification:
    """State of a single theorem verification."""
    theorem_id: str
    status: VerificationStatus = VerificationStatus.PENDING
    layer2_file: Optional[str] = None
    proof_attempts: int = 0
    last_error: Optional[str] = None
    proof: Optional[str] = None

@dataclass
class VerificationState:
    """Redux slice for verification state."""
    layer1: Layer1State
    theorems: Dict[str, TheoremVerification]
    active_verification: Optional[str] = None
    verification_queue: List[str] = None
    
    def __post_init__(self):
        if self.theorems is None:
            self.theorems = {}
        if self.verification_queue is None:
            self.verification_queue = []

# Verification actions
class VerificationActions:
    @staticmethod
    def load_layer1_request():
        return {"type": "verification/load_layer1_request"}
    
    @staticmethod
    def load_layer1_success(data: dict):
        return {"type": "verification/load_layer1_success", "payload": data}
    
    @staticmethod
    def load_layer1_failure(error: str):
        return {"type": "verification/load_layer1_failure", "payload": error}
    
    @staticmethod
    def verify_theorem_request(theorem_id: str, layer2_file: str):
        return {
            "type": "verification/verify_theorem_request",
            "payload": {"theorem_id": theorem_id, "layer2_file": layer2_file}
        }
    
    @staticmethod
    def verify_theorem_success(theorem_id: str, proof: str):
        return {
            "type": "verification/verify_theorem_success",
            "payload": {"theorem_id": theorem_id, "proof": proof}
        }
    
    @staticmethod
    def verify_theorem_failure(theorem_id: str, error: str):
        return {
            "type": "verification/verify_theorem_failure",
            "payload": {"theorem_id": theorem_id, "error": error}
        }

# Verification reducer
def verification_reducer(state: VerificationState, action: dict) -> VerificationState:
    action_type = action.get("type")
    
    if action_type == "verification/load_layer1_request":
        return VerificationState(
            layer1=Layer1State(status=VerificationStatus.LOADING),
            theorems=state.theorems,
            active_verification=state.active_verification,
            verification_queue=state.verification_queue
        )
    
    elif action_type == "verification/load_layer1_success":
        payload = action.get("payload", {})
        return VerificationState(
            layer1=Layer1State(
                status=VerificationStatus.LOADED,
                mathlib_version=payload.get("mathlib_version"),
                physlib_version=payload.get("physlib_version"),
                load_time_ms=payload.get("load_time_ms"),
                memory_mb=payload.get("memory_mb")
            ),
            theorems=state.theorems,
            active_verification=state.active_verification,
            verification_queue=state.verification_queue
        )
    
    elif action_type == "verification/load_layer1_failure":
        return VerificationState(
            layer1=Layer1State(
                status=VerificationStatus.FAILED,
                error=action.get("payload")
            ),
            theorems=state.theorems,
            active_verification=state.active_verification,
            verification_queue=state.verification_queue
        )
    
    elif action_type == "verification/verify_theorem_request":
        payload = action.get("payload", {})
        theorem_id = payload.get("theorem_id")
        new_theorems = state.theorems.copy()
        new_theorems[theorem_id] = TheoremVerification(
            theorem_id=theorem_id,
            status=VerificationStatus.VERIFYING,
            layer2_file=payload.get("layer2_file")
        )
        return VerificationState(
            layer1=state.layer1,
            theorems=new_theorems,
            active_verification=theorem_id,
            verification_queue=state.verification_queue
        )
    
    elif action_type == "verification/verify_theorem_success":
        payload = action.get("payload", {})
        theorem_id = payload.get("theorem_id")
        new_theorems = state.theorems.copy()
        if theorem_id in new_theorems:
            new_theorems[theorem_id].status = VerificationStatus.PASSED
            new_theorems[theorem_id].proof = payload.get("proof")
        return VerificationState(
            layer1=state.layer1,
            theorems=new_theorems,
            active_verification=None,
            verification_queue=state.verification_queue
        )
    
    elif action_type == "verification/verify_theorem_failure":
        payload = action.get("payload", {})
        theorem_id = payload.get("theorem_id")
        new_theorems = state.theorems.copy()
        if theorem_id in new_theorems:
            new_theorems[theorem_id].status = VerificationStatus.FAILED_VERIFICATION
            new_theorems[theorem_id].last_error = payload.get("error")
            new_theorems[theorem_id].proof_attempts += 1
        return VerificationState(
            layer1=state.layer1,
            theorems=new_theorems,
            active_verification=None,
            verification_queue=state.verification_queue
        )
    
    return state
```

### 1.4 Non-Disruptive Integration Approach

The Layer 1 integration is designed to be **completely optional**:

```python
# Existing code continues to work without changes
rlm = RLM(backend="openai", environment="local")

# New code can enable Layer 1
rlm_with_verification = RLM(
    backend="openai",
    environment="local",
    environment_kwargs={
        "enable_layer1": True,
        "layer1_path": "/path/to/layer1"
    }
)
```

---

## Part 2: Backend Routing Integration

### 2.1 Integration Strategy

Backend routing is implemented as a **middleware layer** that intercepts sub-call creation and selects the appropriate backend based on task descriptors. This is non-disruptive because:

1. It adds a new parameter to `RLM.__init__()` with a sensible default
2. Existing `other_backends` mechanism is preserved and enhanced
3. Routing logic is externalized to configuration files

### 2.2 Integration Points

| Component | Integration Method | Impact |
|-----------|------------------|--------|
| **RLM.__init__** | Add `backend_router` parameter and `task_descriptor_fn` | Low - optional parameter |
| **RLM._subcall** | Call backend router before creating child RLM | Medium - requires modification |
| **Backend Factory** | Add factory pattern for dynamic backend creation | Low - new module |
| **Redux Store** | Add `RoutingState` slice for tracking routing decisions | Low - new slice only |

### 2.3 Implementation Steps

#### Step 1: Create Backend Router

```python
# rlm/routing/backend_router.py (NEW FILE)

import re
from typing import Dict, Any, Optional
from dataclasses import dataclass
import yaml

@dataclass
class BackendRoute:
    """Result of backend routing decision."""
    backend_id: str
    rule_name: str
    overrides: list[str]
    reasoning: str

@dataclass
class TaskDescriptor:
    """Descriptor for a sub-task used in routing decisions."""
    subtask_id: str
    parent_task_id: str
    intent: str
    complexity_score: float
    latency_budget_ms: int
    cost_sensitivity: str
    token_estimate: Optional[int] = None
    safety_level: str = "medium"
    metrics: Optional[Dict[str, Any]] = None

class BackendRouter:
    """
    Routes sub-calls to appropriate backend clients based on task descriptors.
    """
    
    def __init__(self, config_path: str | None = None):
        """
        Initialize backend router with configuration.
        
        Args:
            config_path: Path to backend-routing.yaml config file
        """
        self.config = self._load_config(config_path)
        self.metrics_store = MetricsStore()
    
    def _load_config(self, config_path: str | None) -> dict:
        """Load backend routing configuration from YAML file."""
        if config_path is None:
            config_path = self._default_config_path()
        
        try:
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Return default configuration
            return self._default_config()
    
    def _default_config_path(self) -> str:
        """Return default path to backend routing config."""
        import os
        return os.path.join(
            os.path.dirname(__file__),
            "..",
            "config",
            "backend-routing.yaml"
        )
    
    def _default_config(self) -> dict:
        """Return default backend routing configuration."""
        return {
            "version": "0.1",
            "backends": {
                "rlm_internal": {
                    "provider": "internal",
                    "description": "Default internal RLM-backed model"
                },
                "claude_agent": {
                    "provider": "anthropic",
                    "description": "Claude Agent SDK"
                },
                "openai_gpt": {
                    "provider": "openai",
                    "description": "OpenAI GPT model"
                }
            },
            "defaults": {
                "fallback_backend": "rlm_internal",
                "global_cost_priority": "medium",
                "global_quality_priority": "high"
            },
            "rules": [
                {
                    "name": "cheap_simple_research",
                    "when": {
                        "intent": "web_research",
                        "complexity_score": "<0.4",
                        "latency_budget_ms": ">=2000"
                    },
                    "choose": {
                        "backend": "rlm_internal"
                    }
                },
                {
                    "name": "deep_research_claude",
                    "when": {
                        "intent": "web_research",
                        "complexity_score": ">=0.4"
                    },
                    "choose": {
                        "backend": "claude_agent"
                    }
                },
                {
                    "name": "proof_synthesis_strong",
                    "when": {
                        "intent": "proof_synthesis",
                        "complexity_score": ">=0.3"
                    },
                    "choose": {
                        "backend": "claude_agent"
                    }
                }
            ],
            "adaptive_overrides": [
                {
                    "name": "avoid_low_pass_backend_for_proofs",
                    "when": {
                        "intent": "proof_synthesis",
                        "metrics.lean_pass_rate_last_50": "<0.6"
                    },
                    "override": {
                        "backend": "claude_agent"
                    }
                }
            ]
        }
    
    def choose_backend(self, desc: TaskDescriptor) -> BackendRoute:
        """
        Choose backend for a sub-call based on task descriptor.
        
        Args:
            desc: Task descriptor with intent, complexity, etc.
        
        Returns:
            BackendRoute with selected backend and metadata
        """
        features = self._augment_with_metrics(desc)
        backend = self._match_rules(features)
        backend, overrides = self._apply_adaptive_overrides(backend, features)
        
        return BackendRoute(
            backend_id=backend,
            rule_name=features.get("_matched_rule", "fallback"),
            overrides=overrides,
            reasoning=self._generate_reasoning(features, backend, overrides)
        )
    
    def _augment_with_metrics(self, desc: TaskDescriptor) -> Dict[str, Any]:
        """Fetch rolling metrics and add to descriptor."""
        features = desc.__dict__.copy()
        metrics = self.metrics_store.get_for_intent(desc.intent)
        features["metrics"] = metrics
        return features
    
    def _match_rules(self, features: Dict[str, Any]) -> str:
        """Match task descriptor against routing rules."""
        for rule in self.config.get("rules", []):
            if self._matches(rule["when"], features):
                features["_matched_rule"] = rule["name"]
                return rule["choose"]["backend"]
        return self.config["defaults"]["fallback_backend"]
    
    def _apply_adaptive_overrides(
        self, 
        backend: str, 
        features: Dict[str, Any]
    ) -> tuple[str, list[str]]:
        """Apply adaptive overrides based on metrics."""
        applied = []
        for override in self.config.get("adaptive_overrides", []):
            if self._matches(override["when"], features):
                backend = override["override"]["backend"]
                applied.append(override["name"])
        return backend, applied
    
    def _matches(self, cond: Dict[str, Any], features: Dict[str, Any]) -> bool:
        """Check if condition matches features."""
        for key, pattern in cond.items():
            value = self._get_nested(features, key)
            if not self._match_single(value, pattern):
                return False
        return True
    
    def _get_nested(self, obj: Dict[str, Any], key: str) -> Any:
        """Get nested value from dict using dot notation."""
        parts = key.split(".")
        cur = obj
        for p in parts:
            if not isinstance(cur, dict):
                return None
            cur = cur.get(p)
            if cur is None:
                return None
        return cur
    
    def _match_single(self, value: Any, pattern: str) -> bool:
        """Match a single value against a pattern."""
        if value is None:
            return False
        
        # Numeric comparison pattern
        if isinstance(value, (int, float)) and isinstance(pattern, str):
            m = re.match(r"([<>]=?)([0-9.]+)", pattern)
            if m:
                op, num = m.group(1), float(m.group(2))
                if op == ">":
                    return value > num
                if op == ">=":
                    return value >= num
                if op == "<":
                    return value < num
                if op == "<=":
                    return value <= num
        
        # Exact match
        return value == pattern
    
    def _generate_reasoning(
        self, 
        features: Dict[str, Any], 
        backend: str, 
        overrides: list[str]
    ) -> str:
        """Generate human-readable reasoning for routing decision."""
        rule = features.get("_matched_rule", "fallback")
        reasoning = f"Rule '{rule}' matched, selected backend '{backend}'"
        if overrides:
            reasoning += f", overrides applied: {', '.join(overrides)}"
        return reasoning


class MetricsStore:
    """
    Stores rolling metrics for backend performance tracking.
    """
    
    def __init__(self):
        self.metrics: Dict[tuple[str, str], Dict[str, Any]] = {}
        self.window_size = 50
    
    def update(
        self, 
        backend_id: str, 
        intent: str, 
        verification_result: Dict[str, Any]
    ):
        """Update metrics after a sub-call completes."""
        key = (backend_id, intent)
        
        if key not in self.metrics:
            self.metrics[key] = {
                "samples": 0,
                "lean_pass_count": 0,
                "total_iterations": 0,
                "total_latency_ms": 0,
                "total_cost": 0
            }
        
        metrics = self.metrics[key]
        metrics["samples"] += 1
        metrics["lean_pass_count"] += verification_result.get("passed", 0)
        metrics["total_iterations"] += verification_result.get("iterations", 0)
        metrics["total_latency_ms"] += verification_result.get("latency_ms", 0)
        metrics["total_cost"] += verification_result.get("cost", 0)
        
        # Keep only last N samples
        if metrics["samples"] > self.window_size:
            # Simple FIFO - in production, use proper rolling window
            pass
    
    def get_for_intent(self, intent: str) -> Dict[str, Any]:
        """Get aggregated metrics for all backends for an intent."""
        result = {}
        for (backend_id, intent_key), metrics in self.metrics.items():
            if intent_key == intent:
                samples = metrics["samples"]
                if samples > 0:
                    result[f"{backend_id}.lean_pass_rate_last_{samples}"] = (
                        metrics["lean_pass_count"] / samples
                    )
                    result[f"{backend_id}.avg_iterations_to_pass_last_{samples}"] = (
                        metrics["total_iterations"] / samples
                    )
                    result[f"{backend_id}.avg_latency_ms_last_{samples}"] = (
                        metrics["total_latency_ms"] / samples
                    )
                    result[f"{backend_id}.avg_cost_last_{samples}"] = (
                        metrics["total_cost"] / samples
                    )
        return result
```

#### Step 2: Create Backend Factory

```python
# rlm/routing/backend_factory.py (NEW FILE)

from typing import Dict, Any
from rlm.clients import BaseLM, get_client
from rlm.core.types import ClientBackend

class BackendFactory:
    """
    Factory for creating backend clients dynamically based on routing decisions.
    """
    
    def __init__(self, backend_configs: Dict[str, Dict[str, Any]] | None = None):
        """
        Initialize backend factory with backend configurations.
        
        Args:
            backend_configs: Mapping of backend_id to configuration kwargs
        """
        self.backend_configs = backend_configs or {}
    
    def get_backend(
        self, 
        backend_id: str, 
        default_kwargs: Dict[str, Any] | None = None
    ) -> BaseLM:
        """
        Get a backend client instance.
        
        Args:
            backend_id: Identifier of the backend to create
            default_kwargs: Default kwargs to use if not in config
        
        Returns:
            BaseLM instance configured for the specified backend
        """
        # Get configuration for this backend
        config = self.backend_configs.get(backend_id, default_kwargs or {})
        
        # Map backend_id to ClientBackend type
        client_backend = self._map_to_client_backend(backend_id)
        
        # Create client
        return get_client(client_backend, config)
    
    def _map_to_client_backend(self, backend_id: str) -> ClientBackend:
        """Map backend_id string to ClientBackend enum."""
        # This mapping should be configurable
        mapping = {
            "rlm_internal": "openai",  # Or whatever the default is
            "claude_agent": "anthropic",
            "openai_gpt": "openai",
            "gemini": "gemini",
            "portkey": "portkey",
            "litellm": "litellm"
        }
        return mapping.get(backend_id, "openai")
```

#### Step 3: Modify RLM._subcall to Use Backend Router

```python
# rlm/core/rlm.py (MODIFICATION - _subcall method)

def _subcall(self, prompt: str, model: str | None = None) -> RLMChatCompletion:
    """
    Handle a subcall from the environment, potentially spawning a child RLM.
    
    This method is passed as a callback to LocalREPL to enable recursive RLM calls.
    When depth allows, it spawns a child RLM with its own REPL. At max depth,
    it falls back to a plain LM completion.
    
    Args:
        prompt: The prompt to process.
        model: Optional model name. If specified, the child RLM will use this model
            instead of inheriting the parent's default backend.
    
    Returns:
        The full RLMChatCompletion from either a child RLM or plain LM completion.
        On error, returns a completion with the error message as the response.
    """
    next_depth = self.depth + 1
    
    # NEW: Use backend router if available
    child_backend = self.backend
    child_backend_kwargs = self.backend_kwargs
    
    if hasattr(self, 'backend_router') and self.backend_router is not None:
        # Generate task descriptor for routing
        desc = self._generate_task_descriptor(prompt, next_depth)
        
        # Get routing decision
        route = self.backend_router.choose_backend(desc)
        
        # Apply routing decision
        if hasattr(self, 'backend_factory') and self.backend_factory is not None:
            child_client = self.backend_factory.get_backend(
                route.backend_id,
                default_kwargs=self.backend_kwargs
            )
            # Extract backend type from client
            child_backend = child_client.backend_type
            child_backend_kwargs = child_client.kwargs
        else:
            # Fallback to model parameter
            if model is not None:
                child_backend_kwargs = (self.backend_kwargs or {}).copy()
                child_backend_kwargs["model_name"] = model
    
    # Determine which backend/kwargs to use (model override or parent's default)
    if model is not None and not hasattr(self, 'backend_router'):
        child_backend_kwargs = (self.backend_kwargs or {}).copy()
        child_backend_kwargs["model_name"] = model
    else:
        child_backend_kwargs = child_backend_kwargs or self.backend_kwargs
    resolved_model = model or (child_backend_kwargs or {}).get("model_name", "unknown")
    
    # ... rest of the method remains the same ...
```

#### Step 4: Add Backend Router Parameters to RLM.__init__

```python
# rlm/core/rlm.py (MODIFICATION - __init__ method)

def __init__(
    self,
    backend: ClientBackend = "openai",
    backend_kwargs: dict[str, Any] | None = None,
    environment: EnvironmentType = "local",
    environment_kwargs: dict[str, Any] | None = None,
    depth: int = 0,
    max_depth: int = 1,
    max_iterations: int = 30,
    max_budget: float | None = None,
    max_timeout: float | None = None,
    max_tokens: int | None = None,
    max_errors: int | None = None,
    custom_system_prompt: str | None = None,
    other_backends: list[ClientBackend] | None = None,
    other_backend_kwargs: list[dict[str, Any]] | None = None,
    logger: RLMLogger | None = None,
    verbose: bool = False,
    persistent: bool = False,
    custom_tools: dict[str, Any] | None = None,
    custom_sub_tools: dict[str, Any] | None = None,
    compaction: bool = False,
    compaction_threshold_pct: float = 0.85,
    on_subcall_start: Callable[[int, str, str], None] | None = None,
    on_subcall_complete: Callable[[int, str, float, str | None], None] | None = None,
    on_iteration_start: Callable[[int, int], None] | None = None,
    on_iteration_complete: Callable[[int, int, float], None] | None = None,
    # NEW: Backend routing parameters
    backend_router_config: str | None = None,
    backend_configs: dict[str, dict[str, Any]] | None = None,
    task_descriptor_fn: Callable[[str, int], dict] | None = None,
):
    """
    Args:
        backend: The backend to use for the RLM.
        backend_kwargs: The kwargs to pass to the backend.
        environment: The environment to use for the RLM.
        environment_kwargs: The kwargs to pass to the environment.
        depth: The current depth of the RLM (0-indexed).
        max_depth: The maximum depth of recursion. When depth >= max_depth, falls back to plain LM completion.
        max_iterations: The maximum number of iterations of the RLM.
        max_budget: Maximum budget in USD. Execution stops if exceeded. Requires cost-tracking backend (e.g., OpenRouter).
        max_timeout: Maximum execution time in seconds. Execution stops if exceeded, returning best answer if available.
        max_tokens: Maximum total tokens (input + output). Execution stops if exceeded, returning best answer if available.
        max_errors: Maximum consecutive errors before stopping. Execution stops if exceeded, returning best answer if available.
        custom_system_prompt: The custom system prompt to use for the RLM.
        other_backends: A list of other client backends that the environments can use to make sub-calls.
        other_backend_kwargs: The kwargs to pass to the other client backends (ordered to match other_backends).
        logger: The logger to use for the RLM.
        verbose: Whether to print verbose output in rich to console.
        persistent: If True, reuse the environment across completion() calls for multi-turn conversations.
        custom_tools: Dict of custom functions/tools available in the REPL. Keys are function names,
            values are callable functions. These are injected into the REPL globals.
        custom_sub_tools: Dict of custom tools for sub-agents (llm_query calls). If None, inherits
            from custom_tools. Pass an empty dict {} to disable tools for sub-agents.
        compaction: If True, keep full root model history in REPL variable `history` and compact
            when root context reaches compaction_threshold_pct of the model's context limit.
        compaction_threshold_pct: When compaction is on, trigger summarization when root
            message token count reaches this fraction of the model context limit (default 0.85).
        on_subcall_start: Callback fired when a child RLM starts. Args: (depth, model, prompt_preview).
        on_subcall_complete: Callback fired when a child RLM completes. Args: (depth, model, duration, error_or_none).
        on_iteration_start: Callback fired when an iteration starts. Args: (depth, iteration_num).
        on_iteration_complete: Callback fired when an iteration completes. Args: (depth, iteration_num, duration).
        backend_router_config: Path to backend routing configuration YAML file (NEW).
        backend_configs: Dictionary mapping backend_id to backend configuration kwargs (NEW).
        task_descriptor_fn: Function to generate task descriptors for routing (NEW).
    """
    # ... existing initialization ...
    
    # NEW: Backend routing setup
    self.backend_router_config = backend_router_config
    self.backend_configs = backend_configs
    self.task_descriptor_fn = task_descriptor_fn
    self.backend_router = None
    self.backend_factory = None
    
    if backend_router_config is not None or backend_configs is not None:
        from rlm.routing.backend_router import BackendRouter
        from rlm.routing.backend_factory import BackendFactory
        
        self.backend_router = BackendRouter(config_path=backend_router_config)
        self.backend_factory = BackendFactory(backend_configs=backend_configs)
    
    # ... rest of initialization ...
```

#### Step 5: Add Default Task Descriptor Function

```python
# rlm/routing/task_descriptor.py (NEW FILE)

from typing import Callable, Dict, Any
import re

def default_task_descriptor_fn(prompt: str, depth: int) -> Dict[str, Any]:
    """
    Default function to generate task descriptors from prompts.
    
    This function analyzes the prompt and generates a task descriptor
    that can be used by the backend and environment routers.
    
    Args:
        prompt: The prompt for the sub-call
        depth: The depth of this sub-call
    
    Returns:
        Dictionary with task descriptor fields
    """
    # Simple heuristic-based classification
    # In production, this could use an LLM to classify
    
    intent = classify_intent(prompt)
    complexity_score = estimate_complexity(prompt, depth)
    
    return {
        "subtask_id": f"subtask-{depth}-{hash(prompt) % 10000}",
        "parent_task_id": "main",
        "intent": intent,
        "complexity_score": complexity_score,
        "latency_budget_ms": 5000,  # Default 5 second budget
        "cost_sensitivity": "medium",
        "token_estimate": len(prompt.split()) * 1.3,  # Rough estimate
        "safety_level": "medium",
        "capabilities": {
            "needs_internet": needs_internet(prompt),
            "needs_filesystem": needs_filesystem(prompt),
            "needs_lean_access": needs_lean_access(prompt),
            "needs_haskell_access": needs_haskell_access(prompt),
            "needs_docker_isolation": needs_docker_isolation(prompt)
        },
        "security": {
            "data_sensitivity": "internal"
        },
        "performance": {
            "expected_cpu_seconds": estimate_cpu_time(prompt, complexity_score)
        },
        "mode": "dev"
    }

def classify_intent(prompt: str) -> str:
    """Classify the intent of a prompt."""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["search", "research", "find", "look up", "arxiv", "google"]):
        return "web_research"
    elif any(word in prompt_lower for word in ["prove", "theorem", "lean", "formal", "verify"]):
        return "proof_synthesis"
    elif any(word in prompt_lower for word in ["code", "implement", "function", "class", "write"]):
        return "code_generation"
    elif any(word in prompt_lower for word in ["refactor", "improve", "optimize", "clean"]):
        return "refactor"
    elif any(word in prompt_lower for word in ["summarize", "summary", "brief"]):
        return "summarization"
    else:
        return "general"

def estimate_complexity(prompt: str, depth: int) -> float:
    """Estimate complexity score (0.0-1.0) for a prompt."""
    # Base complexity from depth
    base = min(depth / 10.0, 0.5)
    
    # Add complexity from prompt length and structure
    length_factor = min(len(prompt) / 5000.0, 0.3)
    
    # Add complexity from keywords
    complexity_keywords = ["prove", "theorem", "optimize", "design", "architecture"]
    keyword_factor = sum(1 for kw in complexity_keywords if kw.lower() in prompt.lower()) * 0.05
    
    return min(base + length_factor + keyword_factor, 1.0)

def needs_internet(prompt: str) -> bool:
    """Check if prompt likely needs internet access."""
    internet_keywords = ["search", "research", "arxiv", "google", "download", "fetch", "url", "http"]
    return any(kw in prompt.lower() for kw in internet_keywords)

def needs_filesystem(prompt: str) -> bool:
    """Check if prompt likely needs filesystem access."""
    fs_keywords = ["file", "read", "write", "save", "load", "directory", "path"]
    return any(kw in prompt.lower() for kw in fs_keywords)

def needs_lean_access(prompt: str) -> bool:
    """Check if prompt likely needs Lean verification."""
    lean_keywords = ["prove", "theorem", "lean", "formal", "verify", "axiom"]
    return any(kw in prompt.lower() for kw in lean_keywords)

def needs_haskell_access(prompt: str) -> bool:
    """Check if prompt likely needs Haskell type checking."""
    haskell_keywords = ["type", "dimensional", "unit", "haskell"]
    return any(kw in prompt.lower() for kw in haskell_keywords)

def needs_docker_isolation(prompt: str) -> bool:
    """Check if prompt likely needs Docker isolation."""
    docker_keywords = ["install", "package", "pip", "npm", "untrusted", "sandbox"]
    return any(kw in prompt.lower() for kw in docker_keywords)

def estimate_cpu_time(prompt: str, complexity: float) -> int:
    """Estimate expected CPU time in seconds."""
    base_time = 1.0
    complexity_multiplier = 1.0 + (complexity * 10.0)
    length_multiplier = 1.0 + (len(prompt) / 10000.0)
    return int(base_time * complexity_multiplier * length_multiplier)
```

### 2.4 Redux Routing State

```python
# rlm/redux/slices/routing_slice.py (NEW FILE)

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class RoutingDecisionType(Enum):
    BACKEND = "backend"
    ENVIRONMENT = "environment"

@dataclass
class RoutingDecision:
    """Record of a routing decision."""
    decision_id: str
    decision_type: RoutingDecisionType
    subtask_id: str
    selected: str
    rule_name: str
    overrides: List[str]
    reasoning: str
    timestamp: float

@dataclass
class BackendMetrics:
    """Metrics for a backend."""
    backend_id: str
    total_calls: int
    successful_calls: int
    total_cost: float
    avg_latency_ms: float
    lean_pass_rate: float

@dataclass
class RoutingState:
    """Redux slice for routing state."""
    decisions: Dict[str, RoutingDecision]
    backend_metrics: Dict[str, BackendMetrics]
    environment_metrics: Dict[str, BackendMetrics]
    active_routing: Optional[str] = None
    
    def __post_init__(self):
        if self.decisions is None:
            self.decisions = {}
        if self.backend_metrics is None:
            self.backend_metrics = {}
        if self.environment_metrics is None:
            self.environment_metrics = {}

# Routing actions
class RoutingActions:
    @staticmethod
    def routing_decision_made(decision: RoutingDecision):
        return {
            "type": "routing/decision_made",
            "payload": decision
        }
    
    @staticmethod
    def routing_started(subtask_id: str):
        return {
            "type": "routing/started",
            "payload": {"subtask_id": subtask_id}
        }
    
    @staticmethod
    def routing_completed(subtask_id: str, result: dict):
        return {
            "type": "routing/completed",
            "payload": {"subtask_id": subtask_id, "result": result}
        }
    
    @staticmethod
    def backend_metrics_updated(backend_id: str, metrics: dict):
        return {
            "type": "routing/backend_metrics_updated",
            "payload": {"backend_id": backend_id, "metrics": metrics}
        }

# Routing reducer
def routing_reducer(state: RoutingState, action: dict) -> RoutingState:
    action_type = action.get("type")
    
    if action_type == "routing/decision_made":
        decision = action.get("payload")
        new_decisions = state.decisions.copy()
        new_decisions[decision.decision_id] = decision
        return RoutingState(
            decisions=new_decisions,
            backend_metrics=state.backend_metrics,
            environment_metrics=state.environment_metrics,
            active_routing=None
        )
    
    elif action_type == "routing/started":
        return RoutingState(
            decisions=state.decisions,
            backend_metrics=state.backend_metrics,
            environment_metrics=state.environment_metrics,
            active_routing=action.get("payload", {}).get("subtask_id")
        )
    
    elif action_type == "routing/completed":
        # Update metrics based on result
        payload = action.get("payload", {})
        subtask_id = payload.get("subtask_id")
        result = payload.get("result", {})
        
        # Find the routing decision for this subtask
        decision = None
        for dec in state.decisions.values():
            if dec.subtask_id == subtask_id:
                decision = dec
                break
        
        if decision and decision.decision_type == RoutingDecisionType.BACKEND:
            new_backend_metrics = state.backend_metrics.copy()
            backend_id = decision.selected
            if backend_id not in new_backend_metrics:
                new_backend_metrics[backend_id] = BackendMetrics(
                    backend_id=backend_id,
                    total_calls=0,
                    successful_calls=0,
                    total_cost=0.0,
                    avg_latency_ms=0.0,
                    lean_pass_rate=0.0
                )
            
            # Update metrics
            metrics = new_backend_metrics[backend_id]
            metrics.total_calls += 1
            if result.get("success"):
                metrics.successful_calls += 1
            metrics.total_cost += result.get("cost", 0)
            metrics.avg_latency_ms = (
                (metrics.avg_latency_ms * (metrics.total_calls - 1) + result.get("latency_ms", 0))
                / metrics.total_calls
            )
            metrics.lean_pass_rate = (
                (metrics.lean_pass_rate * (metrics.total_calls - 1) + result.get("lean_passed", 0))
                / metrics.total_calls
            )
            
            return RoutingState(
                decisions=state.decisions,
                backend_metrics=new_backend_metrics,
                environment_metrics=state.environment_metrics,
                active_routing=None
            )
    
    return state
```

---

## Part 3: Environment Routing Integration

### 3.1 Integration Strategy

Environment routing follows the same pattern as backend routing - a middleware layer that selects the appropriate environment based on task capabilities and security requirements.

### 3.2 Integration Points

| Component | Integration Method | Impact |
|-----------|------------------|--------|
| **RLM._subcall** | Call environment router before creating child RLM | Medium - requires modification |
| **Environment Factory** | Add factory pattern for dynamic environment creation | Low - new module |
| **RoutingState** | Extend to include environment routing decisions | Low - existing slice |

### 3.3 Implementation Steps

#### Step 1: Create Environment Router

```python
# rlm/routing/environment_router.py (NEW FILE)

import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class EnvironmentRoute:
    """Result of environment routing decision."""
    environment_id: str
    rule_name: str
    reasoning: str

class EnvironmentRouter:
    """
    Routes sub-calls to appropriate execution environments based on task descriptors.
    """
    
    def __init__(self, config_path: str | None = None):
        """
        Initialize environment router with configuration.
        
        Args:
            config_path: Path to environment-routing.yaml config file
        """
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: str | None) -> dict:
        """Load environment routing configuration from YAML file."""
        if config_path is None:
            config_path = self._default_config_path()
        
        try:
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._default_config()
    
    def _default_config_path(self) -> str:
        """Return default path to environment routing config."""
        import os
        return os.path.join(
            os.path.dirname(__file__),
            "..",
            "config",
            "environment-routing.yaml"
        )
    
    def _default_config(self) -> dict:
        """Return default environment routing configuration."""
        return {
            "version": "0.1",
            "environments": {
                "local": {
                    "kind": "localrepl",
                    "description": "Host Python REPL (Lean/Haskell installed here)",
                    "default": True
                },
                "docker": {
                    "kind": "dockerrepl",
                    "description": "Docker container with optional internet access",
                    "image": "python:3.11-slim",
                    "network_mode": "bridge",
                    "cpu_limit": 1.0,
                    "memory_limit_gb": 2
                },
                "modal": {
                    "kind": "modalrepl",
                    "description": "Modal Sandbox for internet-facing subtasks",
                    "profile": "default",
                    "cpu_limit": 2.0,
                    "memory_limit_gb": 4
                }
            },
            "defaults": {
                "fallback_environment": "local",
                "allow_remote_compute_in_dev": False,
                "strict_local_for_sensitive_data": True
            },
            "rules": [
                {
                    "name": "lean_and_haskell_always_local",
                    "when": {
                        "capabilities.needs_lean_access": True
                    },
                    "choose": {
                        "environment": "local"
                    }
                },
                {
                    "name": "pure_filesystem_local",
                    "when": {
                        "capabilities.needs_filesystem": True,
                        "capabilities.needs_internet": False,
                        "security.data_sensitivity": "local_only"
                    },
                    "choose": {
                        "environment": "local"
                    }
                },
                {
                    "name": "untrusted_code_docker",
                    "when": {
                        "capabilities.needs_docker_isolation": True,
                        "capabilities.needs_internet": False
                    },
                    "choose": {
                        "environment": "docker"
                    }
                },
                {
                    "name": "internet_research_dev_mode_docker",
                    "when": {
                        "mode": "dev",
                        "capabilities.needs_internet": True
                    },
                    "choose": {
                        "environment": "docker"
                    }
                },
                {
                    "name": "internet_research_hosted_mode_modal",
                    "when": {
                        "mode": "hosted",
                        "capabilities.needs_internet": True,
                        "security.data_sensitivity": "external_ok"
                    },
                    "choose": {
                        "environment": "modal"
                    }
                },
                {
                    "name": "sensitive_data_force_local",
                    "when": {
                        "security.data_sensitivity": "local_only"
                    },
                    "choose": {
                        "environment": "local"
                    }
                }
            ]
        }
    
    def choose_env(self, desc: Dict[str, Any]) -> EnvironmentRoute:
        """
        Choose environment for a sub-call based on task descriptor.
        
        Args:
            desc: Task descriptor with capabilities, security, mode
        
        Returns:
            EnvironmentRoute with selected environment and metadata
        """
        env_id = self._match_rules(desc)
        rule_name = desc.get("_matched_rule", "fallback")
        
        return EnvironmentRoute(
            environment_id=env_id,
            rule_name=rule_name,
            reasoning=self._generate_reasoning(desc, env_id, rule_name)
        )
    
    def _match_rules(self, features: Dict[str, Any]) -> str:
        """Match task descriptor against routing rules."""
        for rule in self.config.get("rules", []):
            if self._matches(rule["when"], features):
                features["_matched_rule"] = rule["name"]
                return rule["choose"]["environment"]
        return self.config["defaults"]["fallback_environment"]
    
    def _matches(self, cond: Dict[str, Any], features: Dict[str, Any]) -> bool:
        """Check if condition matches features."""
        for key, pattern in cond.items():
            value = self._get_nested(features, key)
            if value != pattern:
                return False
        return True
    
    def _get_nested(self, obj: Dict[str, Any], key: str) -> Any:
        """Get nested value from dict using dot notation."""
        parts = key.split(".")
        cur = obj
        for p in parts:
            if not isinstance(cur, dict):
                return None
            cur = cur.get(p)
            if cur is None:
                return None
        return cur
    
    def _generate_reasoning(
        self, 
        features: Dict[str, Any], 
        env_id: str, 
        rule_name: str
    ) -> str:
        """Generate human-readable reasoning for routing decision."""
        return f"Rule '{rule_name}' matched, selected environment '{env_id}'"
```

#### Step 2: Create Environment Factory

```python
# rlm/routing/environment_factory.py (NEW FILE)

from typing import Dict, Any
from rlm.environments import BaseEnv, get_environment
from rlm.core.types import EnvironmentType

class EnvironmentFactory:
    """
    Factory for creating environment instances dynamically based on routing decisions.
    """
    
    def __init__(self, environment_configs: Dict[str, Dict[str, Any]] | None = None):
        """
        Initialize environment factory with environment configurations.
        
        Args:
            environment_configs: Mapping of environment_id to configuration kwargs
        """
        self.environment_configs = environment_configs or {}
    
    def get_environment(
        self, 
        environment_id: str, 
        default_kwargs: Dict[str, Any] | None = None
    ) -> BaseEnv:
        """
        Get an environment instance.
        
        Args:
            environment_id: Identifier of the environment to create
            default_kwargs: Default kwargs to use if not in config
        
        Returns:
            BaseEnv instance configured for the specified environment
        """
        # Get configuration for this environment
        config = self.environment_configs.get(environment_id, default_kwargs or {})
        
        # Map environment_id to EnvironmentType
        env_type = self._map_to_environment_type(environment_id)
        
        # Create environment
        return get_environment(env_type, config)
    
    def _map_to_environment_type(self, environment_id: str) -> EnvironmentType:
        """Map environment_id string to EnvironmentType."""
        mapping = {
            "local": "local",
            "docker": "docker",
            "modal": "modal",
            "e2b": "e2b",
            "daytona": "daytona",
            "prime": "prime"
        }
        return mapping.get(environment_id, "local")
```

#### Step 3: Modify RLM._subcall to Use Environment Router

```python
# rlm/core/rlm.py (MODIFICATION - _subcall method)

def _subcall(self, prompt: str, model: str | None = None) -> RLMChatCompletion:
    """
    Handle a subcall from the environment, potentially spawning a child RLM.
    """
    next_depth = self.depth + 1
    
    # NEW: Use backend router if available
    child_backend = self.backend
    child_backend_kwargs = self.backend_kwargs
    
    if hasattr(self, 'backend_router') and self.backend_router is not None:
        desc = self._generate_task_descriptor(prompt, next_depth)
        route = self.backend_router.choose_backend(desc)
        
        if hasattr(self, 'backend_factory') and self.backend_factory is not None:
            child_client = self.backend_factory.get_backend(
                route.backend_id,
                default_kwargs=self.backend_kwargs
            )
            child_backend = child_client.backend_type
            child_backend_kwargs = child_client.kwargs
        else:
            if model is not None:
                child_backend_kwargs = (self.backend_kwargs or {}).copy()
                child_backend_kwargs["model_name"] = model
    
    # NEW: Use environment router if available
    child_environment = self.environment_type
    child_environment_kwargs = self.environment_kwargs
    
    if hasattr(self, 'environment_router') and self.environment_router is not None:
        desc = self._generate_task_descriptor(prompt, next_depth)
        env_route = self.environment_router.choose_env(desc)
        
        if hasattr(self, 'environment_factory') and self.environment_factory is not None:
            # Get environment configuration
            env_config = self.environment_configs.get(env_route.environment_id, {})
            
            # Add required kwargs
            env_config = env_config.copy()
            if "lm_handler_address" not in env_config:
                env_config["lm_handler_address"] = None  # Will be set by child RLM
            if "context_payload" not in env_config:
                env_config["context_payload"] = prompt
            if "depth" not in env_config:
                env_config["depth"] = next_depth
            if "subcall_fn" not in env_config and next_depth < self.max_depth:
                env_config["subcall_fn"] = self._subcall
            
            child_environment = env_route.environment_id
            child_environment_kwargs = env_config
    
    # ... rest of the method continues with child_backend, child_backend_kwargs,
    # child_environment, child_environment_kwargs ...
```

#### Step 4: Add Environment Router Parameters to RLM.__init__

```python
# rlm/core/rlm.py (MODIFICATION - __init__ method)

def __init__(
    self,
    # ... existing parameters ...
    # NEW: Environment routing parameters
    environment_router_config: str | None = None,
    environment_configs: dict[str, dict[str, Any]] | None = None,
):
    """
    Args:
        # ... existing args ...
        environment_router_config: Path to environment routing configuration YAML file (NEW).
        environment_configs: Dictionary mapping environment_id to environment configuration kwargs (NEW).
    """
    # ... existing initialization ...
    
    # NEW: Environment routing setup
    self.environment_router_config = environment_router_config
    self.environment_configs = environment_configs
    self.environment_router = None
    self.environment_factory = None
    
    if environment_router_config is not None or environment_configs is not None:
        from rlm.routing.environment_router import EnvironmentRouter
        from rlm.routing.environment_factory import EnvironmentFactory
        
        self.environment_router = EnvironmentRouter(config_path=environment_router_config)
        self.environment_factory = EnvironmentFactory(environment_configs=environment_configs)
    
    # ... rest of initialization ...
```

---

## Part 4: Verification Stack Integration

### 4.1 Integration Strategy

The verification stack is implemented as **specialized agents** that can be spawned by the main orchestrator. These agents use the Layer 1 foundation loaded in LocalREPL to verify designs and theorems.

### 4.2 Verification Agents as RLM Sub-calls

Instead of implementing verification agents as separate processes, they can be implemented as **specialized RLM sub-calls** with:

1. Custom tools for Lean/Haskell verification
2. Specific system prompts for verification tasks
3. Backend routing to appropriate models (e.g., Claude for proof synthesis)

### 4.3 Implementation Steps

#### Step 1: Create Verification Agent System Prompts

```python
# rlm/agents/prompts/verification_prompts.py (NEW FILE)

AUTOFORMALIZATION_SYSTEM_PROMPT = """
You are the Autoformalization Agent. Your task is to translate research findings 
into formal Lean 4 theorem statements that can be verified against Layer 1 axioms.

Your responsibilities:
1. Parse informal rules and equations from research output
2. Generate Lean 4 theorem statements with proper type signatures
3. Map each theorem to its dependencies in Layer 1 (Mathlib, PhysLib, SciLean)
4. Create skeleton proofs (using `sorry` initially)
5. Include source citations in comments

Layer 1 Axioms Available:
- Mathlib: Peano arithmetic, real numbers, calculus, linear algebra
- PhysLib/SciLean: Conservation laws, Ohm's Law, Fourier's Law, Newton's laws
- Haskell Dimensional Types: Type-safe unit checking

Output format:
```lean
import Mathlib.Data.Real.Basic
import SciLean.Core
import PhysLib.Physics

-- Source: [citation]
theorem theorem_name : Prop :=
  sorry
```

Use the verify_lean() tool to check your formalizations.
"""

VERIFIER_SYSTEM_PROMPT = """
You are the Verifier Agent. Your task is to verify Lean 4 theorems against 
Layer 1 axioms using the Lean kernel.

Your responsibilities:
1. Load Layer 1 context (Mathlib, PhysLib, SciLean)
2. Compile the provided Lean 4 code
3. Attempt proof synthesis using available tactics
4. Report compilation errors or proof failures
5. Mark theorems as PASSED or FAILED

Available tools:
- verify_lean(lean_code: str) -> dict: Verify Lean code against Layer 1
- prove_theorem(theorem_statement: str) -> dict: Attempt to prove a theorem

Output format:
```json
{
  "status": "PASSED" | "FAILED",
  "errors": [],
  "proof": "proof content if passed",
  "verification_time_ms": 1234
}
```
"""

PHYSICIST_SYSTEM_PROMPT = """
You are the Physicist Agent. Your task is to verify that designs satisfy 
Layer 2 physics constraints.

Your responsibilities:
1. Extract design parameters from design specs
2. Instantiate Layer 2 theorems with design parameters
3. Write Lean proofs that design satisfies invariants
4. Validate: thermal limits, energy balance, stress constraints, etc.

Available tools:
- verify_lean(lean_code: str) -> dict: Verify Lean code
- prove_theorem(theorem_statement: str) -> dict: Attempt proofs
- get_layer1_axioms() -> dict: Get available Layer 1 axioms

Output format:
```json
{
  "status": "PHYSICALLY_SOUND" | "INVALID",
  "violations": [],
  "proofs": ["proof1.lean", "proof2.lean"],
  "feedback": "Refinement suggestions if invalid"
}
```
"""

CROSS_CHECK_SYSTEM_PROMPT = """
You are the Cross-Check Agent. Your task is to verify Layer 2 consistency 
across multiple source interpretations.

Your responsibilities:
1. Formalize the same rule from 2+ independent sources
2. Prove equivalence in Lean
3. Flag divergences for re-research

Available tools:
- verify_lean(lean_code: str) -> dict: Verify Lean code
- prove_theorem(theorem_statement: str) -> dict: Attempt proofs

Output format:
```json
{
  "status": "EQUIVALENT" | "DIVERGENCE",
  "equivalence_proof": "proof if equivalent",
  "divergence_reason": "reason if divergent",
  "action": "PROCEED" | "INVESTIGATE"
}
```
"""
```

#### Step 2: Create Verification Agent Factory

```python
# rlm/agents/verification_agent_factory.py (NEW FILE)

from typing import Dict, Any, Optional
from rlm import RLM
from rlm.agents.prompts.verification_prompts import (
    AUTOFORMALIZATION_SYSTEM_PROMPT,
    VERIFIER_SYSTEM_PROMPT,
    PHYSICIST_SYSTEM_PROMPT,
    CROSS_CHECK_SYSTEM_PROMPT
)

class VerificationAgentFactory:
    """
    Factory for creating verification agent RLM instances.
    """
    
    def __init__(self, parent_rlm: RLM):
        """
        Initialize verification agent factory.
        
        Args:
            parent_rlm: Parent RLM instance (for inheriting configuration)
        """
        self.parent_rlm = parent_rlm
    
    def create_autoformalization_agent(
        self, 
        research_output: Dict[str, Any]
    ) -> RLM:
        """
        Create an Autoformalization Agent.
        
        Args:
            research_output: Research output to formalize
        
        Returns:
            RLM instance configured as Autoformalization Agent
        """
        return RLM(
            backend=self.parent_rlm.backend,
            backend_kwargs=self.parent_rlm.backend_kwargs,
            environment="local",  # Always local for Layer 1 access
            environment_kwargs={
                "enable_layer1": True,
                "custom_tools": {
                    "verify_lean": self._verify_lean_tool,
                    "get_layer1_axioms": self._get_layer1_axioms_tool
                }
            },
            depth=self.parent_rlm.depth + 1,
            max_depth=self.parent_rlm.max_depth,
            custom_system_prompt=AUTOFORMALIZATION_SYSTEM_PROMPT,
            logger=self.parent_rlm.logger,
            verbose=False
        )
    
    def create_verifier_agent(
        self, 
        layer2_file: str
    ) -> RLM:
        """
        Create a Verifier Agent.
        
        Args:
            layer2_file: Path to Layer 2 Lean file to verify
        
        Returns:
            RLM instance configured as Verifier Agent
        """
        return RLM(
            backend=self.parent_rlm.backend,
            backend_kwargs=self.parent_rlm.backend_kwargs,
            environment="local",  # Always local for Layer 1 access
            environment_kwargs={
                "enable_layer1": True,
                "custom_tools": {
                    "verify_lean": self._verify_lean_tool,
                    "prove_theorem": self._prove_theorem_tool,
                    "get_layer1_axioms": self._get_layer1_axioms_tool
                }
            },
            depth=self.parent_rlm.depth + 1,
            max_depth=self.parent_rlm.max_depth,
            custom_system_prompt=VERIFIER_SYSTEM_PROMPT,
            logger=self.parent_rlm.logger,
            verbose=False
        )
    
    def create_physicist_agent(
        self, 
        design_draft: Dict[str, Any],
        layer2: Dict[str, Any]
    ) -> RLM:
        """
        Create a Physicist Agent.
        
        Args:
            design_draft: Design specification to validate
            layer2: Layer 2 theorems to use
        
        Returns:
            RLM instance configured as Physicist Agent
        """
        return RLM(
            backend=self.parent_rlm.backend,
            backend_kwargs=self.parent_rlm.backend_kwargs,
            environment="local",  # Always local for Layer 1 access
            environment_kwargs={
                "enable_layer1": True,
                "custom_tools": {
                    "verify_lean": self._verify_lean_tool,
                    "prove_theorem": self._prove_theorem_tool,
                    "get_layer1_axioms": self._get_layer1_axioms_tool
                }
            },
            depth=self.parent_rlm.depth + 1,
            max_depth=self.parent_rlm.max_depth,
            custom_system_prompt=PHYSICIST_SYSTEM_PROMPT,
            logger=self.parent_rlm.logger,
            verbose=False
        )
    
    def create_cross_check_agent(
        self, 
        layer2_files: list[str]
    ) -> RLM:
        """
        Create a Cross-Check Agent.
        
        Args:
            layer2_files: List of Layer 2 files to cross-check
        
        Returns:
            RLM instance configured as Cross-Check Agent
        """
        return RLM(
            backend=self.parent_rlm.backend,
            backend_kwargs=self.parent_rlm.backend_kwargs,
            environment="local",  # Always local for Layer 1 access
            environment_kwargs={
                "enable_layer1": True,
                "custom_tools": {
                    "verify_lean": self._verify_lean_tool,
                    "prove_theorem": self._prove_theorem_tool
                }
            },
            depth=self.parent_rlm.depth + 1,
            max_depth=self.parent_rlm.max_depth,
            custom_system_prompt=CROSS_CHECK_SYSTEM_PROMPT,
            logger=self.parent_rlm.logger,
            verbose=False
        )
    
    def _verify_lean_tool(self, lean_code: str) -> dict:
        """Tool for verifying Lean code."""
        # This would be implemented in the environment
        # For now, return a placeholder
        return {"success": True, "message": "Verification tool called"}
    
    def _prove_theorem_tool(self, theorem_statement: str) -> dict:
        """Tool for proving theorems."""
        # This would be implemented in the environment
        return {"success": True, "message": "Proof tool called"}
    
    def _get_layer1_axioms_tool(self) -> dict:
        """Tool for getting Layer 1 axioms."""
        # This would be implemented in the environment
        return {"axioms": ["conservation_energy", "ohms_law", "fourier_law"]}
```

#### Step 3: Integrate Verification with Redux Store

```python
# rlm/redux/middleware/verification_middleware.py (NEW FILE)

from typing import Callable, Any
from rlm.agents.verification_agent_factory import VerificationAgentFactory

class VerificationMiddleware:
    """
    Redux middleware for handling verification-related actions.
    """
    
    def __init__(self, store):
        """
        Initialize verification middleware.
        
        Args:
            store: Redux store instance
        """
        self.store = store
        self.agent_factory = None
    
    def __call__(self, store: Callable) -> Callable:
        def middleware(next: Callable) -> Callable:
            def dispatch(action: dict) -> Any:
                # Handle verification actions
                if action.get("type") == "verification/load_layer1_request":
                    self._handle_load_layer1(action)
                elif action.get("type") == "verification/verify_theorem_request":
                    self._handle_verify_theorem(action)
                
                return next(action)
            return dispatch
        return middleware
    
    def _handle_load_layer1(self, action: dict):
