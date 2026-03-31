# Refined Plan: Flexible Formalization System

**Date:** 2026-03-29
**Status:** DRAFT
**Goal:** Make the formalization system FLEXIBLE - only rigidity is for output QUALITY

---

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Services over Forced Agents** | Processes are callable services ANY agent can use |
| **No Workflow Enforcement** | Task determines workflow, not system design |
| **Peer-to-Peer, Not Hierarchical** | Agents call services directly, not through other agents |
| **Verification as Quality Gate** | ONLY formal verification is non-negotiable |
| **Domain Routing is Optional** | Only if task benefits from it |
| **Orchestrator as Facilitator** | Orchestrator enables, doesn't control |

---

## Problem with Current Implementation

### What Was Built (but needs refinement):

```
┌─────────────────────────────────────────────────────────┐
│  Fast Loop (Skunkworks)                                 │
│    │                                                     │
│    ├── Generates Release Candidate                       │
│    └── Sends to Message Queue ──────────────────────►  │
│                                                        │
│                      ▼                                  │
│  Slow Loop (The Crucible)                             │
│    │                                                     │
│    ├── Picks up from Queue                             │
│    ├── Verifies (Lean/Haskell)                         │
│    ├── IF FAIL ──► Interrupt ──────────────────────►    │
│    └── IF PASS ──► Certified Candidate                 │
└─────────────────────────────────────────────────────────┘

PROBLEM: This FORCES a specific loop structure on EVERY task
```

### The Issue:
- Not every task needs a Fast/Slow loop
- Not every task needs domain routing
- Agents shouldn't HAVE to call specific processes
- The architecture imposes a workflow, not the task

---

## Refined Architecture

### 1. Process Registry (Core Change)

**Instead of**: Agents calling other agents
**Make**: All processes callable as services

```python
# rlm/processes/registry.py

class ProcessRegistry:
    """Registry of ALL available processes (not agents)"""
    
    def register(self, name: str, process: Callable, metadata: ProcessMetadata):
        """Register a process anyone can call"""
        
    def call(self, process_name: str, task_context: dict) -> ProcessResult:
        """Direct process invocation"""
        
    def discover(self, task_requirements: dict) -> List[str]:
        """Which processes might help this task (ADVISORY ONLY)"""
```

**Available Processes:**
| Process | When to Use | Mandatory |
|---------|-------------|-----------|
| `type_check` | Any code that needs verification | NO |
| `verify_lean` | Lean formalization | NO |
| `domain_classify` | When domain is unclear | NO |
| `cross_domain_synthesize` | Multi-domain tasks | NO |
| `automata_learn` | Black-box protocol discovery | NO |
| `ontology_bootstrap` | Novel domain formalization | NO |
| `formalize` | User wants formal proof | **YES** (if they want quality) |

### 2. Agent Capability Profile

**Instead of**: Fixed agent types (VerifierAgent, etc.)
**Make**: Agents declare capabilities, not fixed roles

```python
@dataclass
class AgentCapability:
    can_formalize: bool = False
    can_write_code: bool = False  
    can_research: bool = False
    can_verify: bool = False
    preferred_domains: List[str] = []
    verification_level: VerificationLevel = VerificationLevel.NONE

# Example agent profiles:
human_user = AgentCapability(
    can_formalize=True,
    can_write_code=True,
    verification_level=VerificationLevel.USER_CHOICE  # THEY choose
)

llm_coder = AgentCapability(
    can_write_code=True,
    can_formalize=True,
    verification_level=VerificationLevel.STANDARD
)

specialist_verifier = AgentCapability(
    can_verify=True,
    verification_level=VerificationLevel.MAXIMUM
)
```

### 3. Task-Driven Workflow (NOT System-Driven)

**Instead of**: RLM forcing Fast/Slow loop
**Make**: Workflow emerges from task requirements

```python
@dataclass
class TaskRequirements:
    """What the task ACTUALLY needs"""
    
    # Quality requirements (user choice)
    wants_formal_proof: bool = False
    verification_level: VerificationLevel = VerificationLevel.NONE
    
    # Domain requirements (auto-detected or user)
    domain: Optional[DomainType] = None
    
    # Complexity requirements
    is_multi_domain: bool = False
    needs_ontology: bool = False
    
    # Constraints
    max_verification_time: Optional[float] = None
    user_override_axioms: bool = False


# Workflow emerges like this:

task = "prove this theorem formally"

if task.wants_formal_proof:
    result = process_registry.call("verify_lean", ctx)
    # That's IT. No forced loops.
    
task = "design trading bot for oil shipments"

if task.is_multi_domain:
    structure = process_registry.call("cross_domain_synthesize", ctx)
    result = process_registry.call("verify_lean", ctx)  # Only verification is mandatory
```

### 4. Orchestrator as Facilitator

**Instead of**: Orchestrator controlling workflow
**Make**: Orchestrator provides options, doesn't decide

```python
class Orchestrator:
    """Facilitates, doesn't control"""
    
    def suggest_processes(self, task: str, context: dict) -> List[ProcessSuggestion]:
        """Here are processes that MIGHT help - you decide"""
        
    def allocate_resources(self, needed: List[str]) -> ResourceAllocation:
        """I'll provision what you need"""
        
    def coordinate_parallel(self, processes: List[str]) -> List[ProcessResult]:
        """Run these in parallel if you want"""
```

### 5. Verification as the ONLY Mandatory Gate

**This is the ONLY rigidity in the system:**

```python
class VerificationGate:
    """
    The ONLY forced structure: 
    If user WANTS quality, they MUST pass verification.
    """
    
    def verify(self, artifact: Any, level: VerificationLevel) -> VerificationResult:
        """
        Verification is non-negotiable IF quality is requested.
        But which verification? User chooses.
        """
        
        if level == VerificationLevel.NONE:
            return VerificationResult(skip=True)
        
        if level == VerificationLevel.BASIC:
            return self._type_check(artifact)
        
        if level == VerificationLevel.STANDARD:
            return self._lean_check(artifact)
            
        if level == VerificationLevel.MAXIMUM:
            return self._full_proof_check(artifact)
```

---

## What Needs to Change in Current Implementation

### Current State → Desired State

| Current | Problem | Refined |
|---------|---------|---------|
| Fast Loop → Slow Loop mandatory | Forces dual-loop | Processes are optional |
| `VerificationAgentFactory` creates agents | Forces agent hierarchy | Services callable directly |
| Domain routing on all tasks | Overhead for simple tasks | Only if task needs it |
| `submit_candidate()` mandatory | Loop-centric design | User chooses workflow |
| `loop_slice` Redux state | Tracks forced loop | Track what USED (optional) |

### Key Files to Refactor

1. **`rlm/processes/`** (NEW - process registry and service layer)
   - `registry.py` - Process registration and discovery
   - `base_process.py` - Abstract process interface
   - `verification_process.py` - Type checking/Lean verification
   - `synthesis_process.py` - Cross-domain synthesis
   - `fuzzing_process.py` - Automata learning

2. **`rlm/agents/base_agent.py`** - Refactor to use process registry
   - Remove hardcoded agent-to-agent calls
   - Add `can_use_process(process_name)` check

3. **`rlm/environments/local_repl.py`** - Make processes directly callable
   - `call_process(name, args)` - universal process call
   - `list_processes()` - what's available
   - Remove forced `verify_lean()` if not needed

4. **`rlm/core/rlm.py`** - Remove forced iteration patterns
   - Make verification optional per task
   - Allow user to define custom workflow

5. **`rlm/loops/`** - Refactor from "loops" to "processes"
   - `fast_loop.py` → `exploration_process.py` (optional)
   - `slow_loop.py` → `verification_process.py` (mandatory IF quality wanted)
   - `loop_manager.py` → `process_coordinator.py` (facilitator)

6. **`rlm/redux/slices/loop_slice.py`** - Refactor state to track optional usage
   - `used_processes: List[str]` - what was actually used
   - Remove `fast_loop_active` if it's optional

---

## Implementation Plan (Refined)

### Phase 1: Process Registry (Foundation)

**Goal:** Make all processes callable as services

```
1.1 Create ProcessRegistry
    - Register existing processes (type_check, domain_classify, etc.)
    - Discovery mechanism (which processes help this task)
    - Direct invocation API

1.2 Refactor processes to be standalone
    - `verification_process.py` - from current verification middleware
    - `synthesis_process.py` - from cross_domain_engine
    - `fuzzing_process.py` - from fuzzing_loop
    - `domain_process.py` - from domain_classifier

1.3 Update local_repl.py to expose process calls
    - `call_process("verify_lean", code)`
    - `list_processes()`
    - Remove forced verification calls
```

### Phase 2: Agent Refactor (Flexibility)

**Goal:** Agents use processes, not call other agents

```
2.1 Refactor BaseAgent
    - Remove agent spawning hierarchy requirement
    - Add process registry access
    - Agent declares capabilities, not fixed role

2.2 Remove VerificationAgentFactory
    - Replace with direct process calls
    - Any agent can call verification_process

2.3 Update SwarmAgent
    - Peer-to-peer process calls
    - No forced parent-child agent chain
```

### Phase 3: Orchestrator as Facilitator

**Goal:** Orchestrator enables, doesn't control

```
3.1 Refactor Orchestrator
    - `suggest_processes(task)` - advisory only
    - `allocate_resources(needs)` - provision what asked for
    - `coordinate_parallel(processes)` - run in parallel if wanted

3.2 Remove forced workflow
    - Task defines workflow, not orchestrator
    - Orchestrator just facilitates

3.3 Add process coordination state
    - Track what's running
    - Handle resource allocation
```

### Phase 4: Verification as Quality Gate

**Goal:** ONLY mandatory rigidity is verification (if quality requested)

```
4.1 Create VerificationGate
    - VerificationLevel enum (NONE, BASIC, STANDARD, MAXIMUM)
    - User CHOOSES verification level
    - Gate only enforced IF user wants quality

4.2 Update type checking to use VerificationGate
    - Type check is optional
    - Full Lean verification is optional
    - Only mandatory if task.wants_formal_proof

4.3 Add user verification preference
    - Per-task verification level
    - Stored in task context
```

### Phase 5: Clean Up & Integration

**Goal:** Remove forced structures

```
5.1 Refactor Redux slices
    - `loop_slice` → `process_usage_slice` (track what was used)
    - Make state ADVISORY, not controlling

5.2 Update config
    - Remove `dual_loop.enabled: false`
    - Processes are enabled by default

5.3 Integration test
    - Verify any agent can call any process
    - Verify no forced workflow
    - Verify verification is only mandatory gate
```

---

## Summary: Key Changes

| Before | After |
|--------|-------|
| Agents call agents (hierarchical) | Agents call processes (peer) |
| Fast/Slow loop on all tasks | Loop optional, task-driven |
| Domain routing on all tasks | Domain routing advisory only |
| VerificationAgentFactory | Direct process calls |
| Orchestrator controls | Orchestrator facilitates |
| Redux slices track forced state | Redux slices track optional usage |

---

## Success Criteria

1. **Any agent can call any process** - No agent-to-agent hierarchy
2. **Task defines workflow** - Not system design
3. **Verification is the ONLY gate** - But user chooses level
4. **No forced structures** - Unless task actually needs it
5. **Orchestrator enables** - Doesn't control

---

## Files to Create/Refactor

| File | Action | Purpose |
|------|--------|---------|
| `rlm/processes/__init__.py` | CREATE | Process module |
| `rlm/processes/registry.py` | CREATE | Process registry |
| `rlm/processes/base_process.py` | CREATE | Process interface |
| `rlm/processes/verification_process.py` | CREATE | Verification service |
| `rlm/processes/synthesis_process.py` | CREATE | Synthesis service |
| `rlm/agents/base_agent.py` | REFACTOR | Use process registry |
| `rlm/environments/local_repl.py` | REFACTOR | Expose process calls |
| `rlm/core/rlm.py` | REFACTOR | Remove forced iteration |
| `rlm/app/orchestrator.py` | REFACTOR | Facilitator pattern |
| `rlm/redux/slices/loop_slice.py` | REFACTOR | Optional usage tracking |

---

## Questions/Clarifications Needed

1. **Verification levels**: What should each level mean?
   - NONE: No verification
   - BASIC: Type check only
   - STANDARD: Lean syntax check
   - MAXIMUM: Full proof verification

2. **User control**: Should users be able to:
   - Skip verification entirely?
   - Choose verification level per task?
   - Override verification for speed?

3. **Process discovery**: Should the system:
   - Auto-suggest helpful processes?
   - Let user/agent decide completely?
   - Track which processes work well for what task types?
