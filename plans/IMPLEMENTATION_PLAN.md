# Self-Improving Swarm System - Unified Implementation Plan

## Document Info

| Field | Value |
|-------|-------|
| Version | 2.0 |
| Created | 2026-03-28 |
| Last Updated | 2026-03-28 |
| Status | IN_PROGRESS |
| Current Phase | Phase 1: Core Runtime Foundation (COMPLETED) |

---

## Executive Summary

This document is the **UNIFIED implementation plan** merging all roadmap plans for the Self-Improving Swarm System. It combines:
- Application Runtime Plan (`IMPLEMENTATION_PLAN.md`)
- Type Checking System (`.kilo/plans/1774673361830-gentle-otter.md`)
- Axiomatic RLM Routing Integration (`axiomatic_rlm_routing_integration_plan.md`)
- Formalization Domain Structure (`plans/Formalization Domain Structure/phased_implementation_roadmap.md`)
- Agent Implementation Roadmap (`plans/agent_implementation_roadmap.md`)
- RLM Routing Upgrade (`plans/rlm_upgrade/rlm-routing-upgrade-overview.md`)

---

## What Exists

- ✅ RLM Core (`rlm/core/rlm.py`) - Recursive language model execution engine
- ✅ Redux Store (`rlm/redux/store.py`) - Python state management with 9 slices
- ✅ WebSocket Server (`rlm/console/websocket.py`) - Key management interface
- ✅ Client implementations for multiple backends (OpenAI, Anthropic, MiniMax, etc.)
- ✅ Environment implementations (Local, Docker, Modal, E2B, Daytona, Prime)
- ✅ Routing system (`rlm/routing/backend_router.py`, `environment_router.py`, `task_descriptor.py`)
- ✅ Agent framework components (`rlm/agents/`)
- ✅ Layer1 verification system (`rlm/environments/layer1_bootstrap.py`)
- ✅ Backend Factory (`rlm/routing/backend_factory.py`)
- ✅ Type Checking files already partially exist (`rlm/routing/`, `rlm/environments/layer1_bootstrap.py`, `rlm/redux/slices/verification_slice.py`)
- ✅ Comprehensive test suite

---

## What is Missing

### Critical Path (Must Implement)
1. ❌ Type Checking System (Haskell GHC + Lean Lake integration) - **MUST be before Dual-Loop**
2. ❌ Application entry point with event loop (Phase 1 - COMPLETED)
3. ❌ Orchestrator that manages RLM lifecycle
4. ❌ Message bus for inter-agent communication
5. ❌ WebSocket bridge connecting UI to orchestrator
6. ❌ Real-time state synchronization to UI
7. ❌ Task execution workflow
8. ❌ Dual-Loop Architecture (Fast Loop + Slow Loop)
9. ❌ Domain Routing & Dynamic Layer 1
10. ❌ Cross-Domain Synthesis & Skunkworks Protocol
11. ❌ Empirical Fuzzing Loop
12. ❌ Universal Ontology Bootstrapping
13. ❌ Advanced Edge Domains

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                             │
│                     (React UI - ui/src/)                            │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │ WebSocket
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     APPLICATION RUNTIME                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │   app.py    │  │ orchestrator│  │ message_bus │  │ ws_bridge  │ │
│  │  (entry)    │  │             │  │             │  │            │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐
│   RLM CORE      │  │   REDUX STORE   │  │     AGENT MANAGER        │
│ rlm/core/rlm.py │  │ rlm/redux/store │  │  (spawns/manages agents) │
└─────────────────┘  └─────────────────┘  └─────────────────────────┘
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    TYPE CHECKING SYSTEM (NEW)                         │
│  ┌─────────────────┐                 ┌─────────────────┐            │
│  │ Haskell Checker │                 │   Lean Checker   │            │
│  │  (GHC Wrapper) │                 │  (Lake Wrapper) │            │
│  └─────────────────┘                 └─────────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DUAL-LOOP ARCHITECTURE (NEW)                      │
│  ┌─────────────────┐                 ┌─────────────────┐            │
│  │   FAST LOOP     │                 │   SLOW LOOP     │            │
│  │ (System 1)      │◄───────────────►│ (System 2)      │            │
│  │ Rapid generation│   Async Queue   │ Formal verify   │            │
│  └─────────────────┘                 └─────────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases (Unified)

### [Phase 0] Type Checking System Foundation ⭐ (MUST be before Phase 2)
**Status:** NOT_STARTED  
**Estimated Duration:** 21 days  
**Priority:** CRITICAL - Required for Dual-Loop verification  
**Reference:** `.kilo/plans/1774673361830-gentle-otter.md`

#### Objectives
- Implement Haskell type checking via GHC wrapper
- Implement Lean verification via Lake wrapper
- Create type checker abstraction layer
- Integration with LocalREPL and Redux

#### Tasks

**Phase 0A: Core Foundation (Days 1-3)**

- [ ] **0A.1** Create type checking module structure
  - [ ] File: `rlm/typechecking/__init__.py`
  - [ ] File: `rlm/typechecking/base.py` - Abstract TypeChecker base class
  - [ ] File: `rlm/typechecking/result.py` - TypeCheckResult, TypeError types
  - [ ] File: `rlm/typechecking/exceptions.py` - Custom exceptions

- [ ] **0A.2** Create configuration and registry
  - [ ] File: `rlm/typechecking/config.py` - Type checker configuration
  - [ ] File: `rlm/typechecking/registry.py` - Type checker registry

**Phase 0B: Haskell Type Checker (Days 4-7)**

- [ ] **0B.1** Create Haskell checker interface
  - [ ] File: `rlm/typechecking/haskell/__init__.py`
  - [ ] File: `rlm/typechecking/haskell/haskell_checker.py` - Abstract interface

- [ ] **0B.2** Implement GHC integration
  - [ ] File: `rlm/typechecking/haskell/ghc_checker.py` - GHC subprocess implementation
  - [ ] File: `rlm/typechecking/haskell/result.py` - Haskell-specific results

- [ ] **0B.3** Tests
  - [ ] File: `tests/typechecking/haskell/__init__.py`
  - [ ] File: `tests/typechecking/haskell/test_ghc_checker.py`

**Phase 0C: Lean Type Checker (Days 8-12)**

- [ ] **0C.1** Create Lean checker interface
  - [ ] File: `rlm/typechecking/lean/__init__.py`
  - [ ] File: `rlm/typechecking/lean/lean_checker.py` - Abstract interface

- [ ] **0C.2** Implement Lake integration
  - [ ] File: `rlm/typechecking/lean/lake_checker.py` - Lake subprocess implementation
  - [ ] File: `rlm/typechecking/lean/result.py` - Lean-specific results

- [ ] **0C.3** Tests
  - [ ] File: `tests/typechecking/lean/__init__.py`
  - [ ] File: `tests/typechecking/lean/test_lake_checker.py`

**Phase 0D: Integration (Days 13-16)**

- [ ] **0D.1** Integrate with LocalREPL
  - [ ] Modify: `rlm/environments/local_repl.py`

- [ ] **0D.2** Integrate with Redux
  - [ ] Modify: `rlm/redux/slices/verification_slice.py` (already exists - verify/update)

- [ ] **0D.3** Integrate with VerificationAgentFactory
  - [ ] Modify: `rlm/agents/verification_agent_factory.py`

**Phase 0E: Configuration (Days 17-18)**

- [ ] **0E.1** Create YAML configuration
  - [ ] File: `config/type-checking.yaml`
  - [ ] File: `rlm/typechecking/config_loader.py`

**Phase 0F: Testing and Documentation (Days 19-21)**

- [ ] **0F.1** Integration tests
  - [ ] File: `tests/typechecking/__init__.py`
  - [ ] File: `tests/typechecking/test_integration.py`
  - [ ] File: `tests/integration/test_typechecking_flow.py`

#### Verification
```python
check_haskell_types("x :: Int; x = 'hello'")  # Returns type error
verify_lean("theorem test : 1 = 2 := rfl")     # Returns verification failure
```

---

### [Phase 1] Core Runtime Foundation
**Status:** COMPLETED  
**Dependencies:** None  
**Completed:** 2026-03-28

#### Tasks
- [x] **1.1** Create `app.py` as main entry point ✅
- [x] **1.2** Create dependency container (`rlm/app/dependencies.py`) ✅
- [x] **1.3** Create base orchestrator skeleton (`rlm/app/orchestrator.py`) ✅
- [x] **1.4** Add logging configuration (`rlm/app/logging_config.py`) ✅

---

### [Phase 2] Agent Management System
**Status:** NOT_STARTED  
**Estimated Complexity:** High  
**Dependencies:** Phase 1  
**Reference:** `plans/agent_implementation_roadmap.md` Phase 3 (Base Agent Framework)

#### Objectives
- Implement AgentManager class
- Create RLM wrapper with encrypted_store integration
- Handle agent lifecycle (create, pause, resume, terminate)
- Connect agents to Redux store for state updates

#### Tasks

- [ ] **2.1** Create RLM executor wrapper
  - [ ] File: `rlm/app/rlm_executor.py`
  - [ ] Class: `RLMExecutor`
  - [ ] Wrap `RLM.completion()` method
  - [ ] Accept `encrypted_store` parameter
  - [ ] Handle callbacks: `on_subcall_start`, `on_subcall_complete`
  - [ ] Track execution metrics (time, tokens, cost)
  - [ ] Support cancellation via threading

- [ ] **2.2** Create agent configuration
  - [ ] File: `rlm/app/agent_config.py`
  - [ ] Class: `AgentConfig` (dataclass)
  - [ ] Fields: `agent_id`, `task`, `backend`, `backend_kwargs`, `environment`, `max_depth`, `max_iterations`, `max_budget`, `max_timeout`, `encrypted_store`
  - [ ] Validation in `__post_init__`

- [ ] **2.3** Create AgentManager class
  - [ ] File: `rlm/app/agent_manager.py`
  - [ ] Class: `AgentManager`
  - [ ] Create/destroy agent executors
  - [ ] Track agent states in Redux store
  - [ ] Update Redux on agent status changes
  - [ ] Handle agent errors and retries
  - [ ] Thread-safe operations with locks

- [ ] **2.4** Integrate agent state with Redux store
  - [ ] File: `rlm/app/state_sync.py`
  - [ ] Function: `sync_agent_to_store(agent, store)`
  - [ ] Update `agents` slice on status changes
  - [ ] Log agent lifecycle events
  - [ ] Handle concurrent updates

- [ ] **2.5** Add agent cancellation support
  - [ ] File: `rlm/app/agent_manager.py` (update)
  - [ ] Support cancelling running agents
  - [ ] Propagate cancellation to RLM execution
  - [ ] Update Redux state on cancellation

#### Exit Criteria
- [x] Agents can be created with configuration
- [x] Agent state updates Redux store
- [x] Agents can be paused, resumed, terminated
- [x] RLM execution completes and returns result
- [x] encrypted_store integration works (tested in Phase 3)

---

### [Phase 3] Message Bus for Inter-Agent Communication
**Status:** NOT_STARTED  
**Estimated Complexity:** Medium  
**Dependencies:** Phase 1, Phase 2  
**Reference:** `plans/agent_implementation_roadmap.md` Phase 4 (Messaging System)

#### Objectives
- Implement message bus for agent-to-agent communication
- Create message types for different communications
- Implement pub/sub for event broadcasting
- Connect message bus to Redux store

#### Tasks

- [ ] **3.1** Define message types
  - [ ] File: `rlm/app/messages.py`
  - [ ] Enum: `MessageType` (status_update, task_request, task_complete, permission_request, tool_share, error_report, query, response, broadcast)
  - [ ] Enum: `MessagePriority` (low, normal, high, critical)
  - [ ] Dataclass: `Message` with fields: id, sender, recipients, type, priority, content, timestamp, metadata
  - [ ] Dataclass: `MessageEnvelope` for wrapping messages with delivery metadata

- [ ] **3.2** Create message bus implementation
  - [ ] File: `rlm/app/message_bus.py`
  - [ ] Class: `MessageBus`
  - [ ] In-memory message queue
  - [ ] Subscribe/unsubscribe to message types
  - [ ] Publish messages to recipients
  - [ ] Broadcast messages to all subscribers
  - [ ] Thread-safe operations

- [ ] **3.3** Implement message handlers
  - [ ] File: `rlm/app/message_handlers.py`
  - [ ] Function: `handle_agent_message(message, agent_manager)`
  - [ ] Function: `handle_system_message(message, orchestrator)`
  - [ ] Function: `handle_broadcast(message, store)`
  - [ ] Route messages to appropriate handlers

- [ ] **3.4** Connect message bus to Redux store
  - [ ] File: `rlm/app/message_bus.py` (update)
  - [ ] Update `messages` slice when messages sent/received
  - [ ] Notify UI via store subscribers when new messages arrive
  - [ ] Implement inbox/outbox per agent

- [ ] **3.5** Add message persistence (optional)
  - [ ] File: `rlm/app/message_store.py`
  - [ ] Class: `MessageStore`
  - [ ] Save messages to disk periodically
  - [ ] Load message history on startup
  - [ ] Implement retention policy

#### Verification
```python
bus = MessageBus()
bus.subscribe(MessageType.BROADCAST, handler)
bus.publish(Message(...))
```

---

### [Phase 4] WebSocket Bridge - UI to Backend
**Status:** NOT_STARTED  
**Estimated Complexity:** Medium  
**Dependencies:** Phase 1, Phase 2  
**Reference:** `plans/agent_implementation_roadmap.md` Phase 9 (API Layer - WebSocket part)

#### Objectives
- Extend existing WebSocket server for app integration
- Create command handlers for orchestrator actions
- Push Redux state changes to UI in real-time
- Handle task submission from UI

#### Tasks

- [ ] **4.1** Extend WebSocket message types
  - [ ] File: `rlm/console/websocket.py` (update)
  - [ ] Add message types: `task/submit`, `task/cancel`, `agent/pause`, `agent/resume`, `agent/terminate`, `system/status`
  - [ ] Add handlers for each message type

- [ ] **4.2** Create WebSocket bridge service
  - [ ] File: `rlm/app/ws_bridge.py`
  - [ ] Class: `WebSocketBridge`
  - [ ] Connect to existing WebSocket server (`rlm/console/websocket.py`)
  - [ ] Subscribe to Redux store changes
  - [ ] Push state updates to connected UI clients
  - [ ] Forward UI commands to orchestrator

- [ ] **4.3** Implement task submission flow
  - [ ] File: `rlm/app/ws_bridge.py` (update)
  - [ ] Handler: `handle_task_submit(payload)`
  - [ ] Create agent with task
  - [ ] Return task_id to UI
  - [ ] Stream progress updates

- [ ] **4.4** Implement agent control flow
  - [ ] Handler: `handle_agent_control(action, agent_id)`
  - [ ] Support pause, resume, terminate actions
  - [ ] Update Redux state
  - [ ] Notify UI of state changes

- [ ] **4.5** Connect encrypted_store to WebSocket
  - [ ] File: `rlm/console/websocket.py` (update)
  - [ ] Pass `conn.key_store` to orchestrator when creating agents
  - [ ] Ensure keys flow from UI unlock → stored in WebSocket connection → passed to RLM executor

#### Exit Criteria
- [x] UI can submit tasks via WebSocket
- [x] Task progress updates pushed to UI
- [x] Agent control commands work
- [x] Encrypted API keys flow from UI to RLM

---

### [Phase 5] Task Execution Workflow
**Status:** NOT_STARTED  
**Estimated Complexity:** Medium  
**Dependencies:** Phase 2, Phase 3, Phase 4  
**Reference:** `plans/agent_implementation_roadmap.md` Phase 7 (Main Recursive Instance - Task Execution)

#### Objectives
- Implement main task submission workflow
- Connect orchestrator to agent manager
- Handle task completion and result retrieval
- Implement timeout and budget enforcement

#### Tasks

- [ ] **5.1** Implement orchestrator task submission
  - [ ] File: `rlm/app/orchestrator.py` (update)
  - [ ] Method: `submit_task(task_description, options)` → task_id
  - [ ] Method: `cancel_task(task_id)`
  - [ ] Method: `get_task_status(task_id)` → status
  - [ ] Method: `get_task_result(task_id)` → result

- [ ] **5.2** Add task tracking to Redux store
  - [ ] Update `tasks` slice if needed
  - [ ] Track task state: pending, running, completed, failed, cancelled
  - [ ] Store task results
  - [ ] Handle task timeouts

- [ ] **5.3** Implement task result streaming
  - [ ] File: `rlm/app/result_streamer.py`
  - [ ] Class: `ResultStreamer`
  - [ ] Stream RLM iterations to UI as they complete
  - [ ] Push partial results
  - [ ] Push final result when complete

- [ ] **5.4** Add error handling and retry logic
  - [ ] Implement retry on transient failures
  - [ ] Circuit breaker for repeated failures
  - [ ] Graceful degradation

#### Verification
```python
orchestrator.submit_task("Write a Python function to calculate fibonacci numbers", backend="minimax")
# Should: Create agent, Execute RLM, Stream progress, Return result, Update Redux
```

---

### [Phase 6] Dual-Loop Architecture ⭐
**Status:** NOT_STARTED  
**Estimated Complexity:** High  
**Dependencies:** Phase 0 (Type Checking), Phase 5  
**Reference:** `plans/Formalization Domain Structure/phased_implementation_roadmap.md` Phase 2

#### Objectives
- Implement Fast Loop (System 1) for rapid generation
- Implement Slow Loop (System 2) for formal verification
- Implement Async Message Queue for inter-loop communication
- Implement Bounce-Back Interrupt Protocol

#### Tasks

**6.1** Fast Loop Implementation
- [ ] File: `rlm/loops/fast_loop.py`
  - FastLoop class with process_task() method
  - Agent coordination (Architect, Draftsman, Research)
  - UI streaming support
  - Release Candidate packaging
- [ ] File: `rlm/loops/release_candidate.py`
  - ReleaseCandidate dataclass
  - CandidateStatus enum
  - Serialization methods

**6.2** Slow Loop Implementation
- [ ] File: `rlm/loops/slow_loop.py`
  - SlowLoop class with verify_candidate() method
  - Agent coordination (Autoformalization, Verifier)
  - Proof generation
  - Certification logic
- [ ] Extend: `rlm/agents/verification_agent_factory.py`
  - Add create_slow_loop_agent() method
  - Add create_fast_loop_agent() method

**6.3** Async Message Queue
- [ ] File: `rlm/loops/message_queue.py`
  - AsyncMessageQueue class
  - Priority-based queue
  - Persistence support
  - Thread-safe operations

**6.4** Bounce-Back Interrupt Protocol
- [ ] File: `rlm/loops/interrupt_protocol.py`
  - InterruptProtocol class
  - Error translation from Lean to plain text
  - Interrupt dispatching
  - Handler registration

**6.5** Loop Manager
- [ ] File: `rlm/loops/loop_manager.py`
  - LoopManager class coordinating both loops
  - Lifecycle management
  - Error handling
  - Metrics collection

**6.6** RLM Integration
- [ ] Modify: `rlm/core/rlm.py`
  - Add loop_manager parameter
  - Integrate loop manager into completion() method
  - Add loop-specific callbacks

**6.7** Redux Integration
- [ ] File: `rlm/redux/slices/loop_slice.py`
  - Dual-loop state management

#### Exit Criteria
- Fast Loop generates Release Candidates
- Slow Loop verifies candidates correctly
- Message queue handles concurrent operations
- Bounce-back interrupts work as expected
- Both loops can run concurrently

---

### [Phase 7] Multi-Agent Orchestration
**Status:** NOT_STARTED  
**Estimated Complexity:** High  
**Dependencies:** Phase 5  
**Reference:** `plans/agent_implementation_roadmap.md` Phase 7 (Main Recursive Instance)

#### Objectives
- Support spawning multiple agents from main orchestrator
- Implement task decomposition
- Coordinate agent collaboration
- Aggregate results from multiple agents
- Implement agent-to-agent messaging

#### Tasks

- [ ] **7.1** Implement task decomposition
  - [ ] File: `rlm/app/task_decomposer.py`
  - [ ] Class: `TaskDecomposer`
  - [ ] Analyze task and break into subtasks
  - [ ] Assign subtasks to agents
  - [ ] Track dependencies

- [ ] **7.2** Implement main orchestrator with spawning
  - [ ] File: `rlm/app/orchestrator.py` (update)
  - [ ] Add `spawn_agent()` method
  - [ ] Add `coordinate_agents()` method
  - [ ] Aggregate results from spawned agents

- [ ] **7.3** Implement agent spawning during RLM execution
  - [ ] File: `rlm/app/rlm_executor.py` (update)
  - [ ] Detect when RLM wants to spawn sub-agent
  - [ ] Communicate with orchestrator
  - [ ] Create new agent mid-execution

- [ ] **7.4** Implement result aggregation
  - [ ] File: `rlm/app/result_aggregator.py`
  - [ ] Class: `ResultAggregator`
  - [ ] Combine results from multiple agents
  - [ ] Handle partial results
  - [ ] Return unified response

---

### [Phase 8] Backend & Environment Routing
**Status:** NOT_STARTED  
**Estimated Complexity:** Medium  
**Dependencies:** Phase 1, Phase 2  
**Reference:** 
- `plans/rlm_upgrade/rlm-routing-upgrade-overview.md`
- `plans/axiomatic_rlm_routing_integration_plan.md` Part 2
- `plans/agent_implementation_roadmap.md` Phase 8

#### Objectives
- Implement dynamic backend selection per sub-call
- Implement dynamic environment selection per sub-call
- Track metrics for adaptive routing
- Connect routing to Redux state

#### Tasks

- [ ] **8.1** Enhance Backend Router
  - [ ] File: `rlm/routing/backend_router.py` (update)
  - [ ] BackendRouter already exists - enhance with:
    - Metrics tracking for adaptive routing
    - Task descriptor integration
    - Priority-based routing

- [ ] **8.2** Enhance Environment Router
  - [ ] File: `rlm/routing/environment_router.py` (update/create)
  - [ ] EnvironmentRouter class with:
    - Environment selection based on capabilities
    - Security and isolation decisions
    - Support for `local`, `docker`, `modal`, `e2b`, `daytona`

- [ ] **8.3** Implement Task Descriptor
  - [ ] File: `rlm/routing/task_descriptor.py` (update)
  - [ ] Already exists - enhance with:
    - `classify_intent()` - intent classification
    - `estimate_complexity()` - complexity scoring
    - `needs_*` capability detection

- [ ] **8.4** Create Backend Factory
  - [ ] File: `rlm/routing/backend_factory.py` (update)
  - [ ] Already exists - verify integration

- [ ] **8.5** Connect to Redux
  - [ ] File: `rlm/redux/slices/routing_slice.py`
  - [ ] RoutingState with:
    - RoutingDecision records
    - BackendMetrics
    - EnvironmentMetrics

#### Verification
```python
# Sub-call routing example
desc = task_descriptor_fn(prompt, depth)
backend_route = backend_router.choose_backend(desc)
env_route = environment_router.choose_env(desc)
```

---

### [Phase 9] Domain Routing & Dynamic Layer 1
**Status:** NOT_STARTED  
**Estimated Complexity:** Medium  
**Dependencies:** Phase 0 (Type Checking), Phase 6 (Dual-Loop)  
**Reference:** `plans/Formalization Domain Structure/phased_implementation_roadmap.md` Phase 3

#### Objectives
- Implement domain classification for tasks
- Implement dynamic Layer 1 library loading
- Implement domain-specific research source routing
- Extend existing routing infrastructure

#### Tasks

- [ ] **9.1** Domain Classification
  - [ ] File: `rlm/routing/domain_classifier.py`
  - [ ] DomainClassifier class
  - [ ] Keyword-based classification
  - [ ] Confidence scoring
  - [ ] Domain enum (MATH, PHYSICS, SOFTWARE, CHEMISTRY, FINANCE, GENERAL)

- [ ] **9.2** Domain Router
  - [ ] File: `rlm/routing/domain_router.py`
  - [ ] DomainRouter class
  - [ ] Route to domain-specific configurations
  - [ ] Domain config management
  - [ ] File: `rlm/routing/domain_config.py`

- [ ] **9.3** Dynamic Layer 1 Loading
  - [ ] File: `rlm/layer1/dynamic_loader.py`
  - [ ] DynamicLayer1Loader class
  - [ ] Bootstrap file generation
  - [ ] Library loading/unloading
  - [ ] Cache management
  - [ ] Extend: `rlm/environments/layer1_bootstrap.py`

- [ ] **9.4** Domain Research Sources
  - [ ] File: `rlm/research/domain_sources.py`
  - [ ] DomainResearchSources class
  - [ ] Source validation
  - [ ] Query routing

- [ ] **9.5** Domain Metadata
  - [ ] File: `rlm/routing/domain_metadata.py`
  - [ ] DomainMetadata class
  - [ ] Constraint extraction
  - [ ] Theorem extraction

---

### [Phase 10] Self-Improvement System
**Status:** NOT_STARTED  
**Estimated Complexity:** High  
**Dependencies:** Phase 6  
**Reference:** `plans/agent_implementation_roadmap.md` Phase 6

#### Objectives
- Implement improvement proposal system
- Create tool sharing mechanism
- Implement improvement review workflow
- Apply approved improvements

#### Tasks

- [ ] **10.1** Implement improvement registry
  - [ ] File: `rlm/app/improvement_registry.py`
  - [ ] Based on `rlm/redux/slices/improvements_slice.py`
  - [ ] Register proposed improvements
  - [ ] Track improvement status
  - [ ] Apply approved improvements

- [ ] **10.2** Implement tool registry integration
  - [ ] File: `rlm/app/tool_registry.py`
  - [ ] Based on existing tool slice
  - [ ] Share tools between agents
  - [ ] Dynamic tool creation

- [ ] **10.3** Implement review workflow
  - [ ] File: `rlm/app/improvement_review.py`
  - [ ] Present improvements for review
  - [ ] Accept/reject improvements
  - [ ] Apply accepted improvements

#### Verification
```python
message_bus.publish(Message(
    sender="agent-1",
    recipients=["orchestrator"],
    type=MessageType.IMPROVEMENT_PROPOSAL,
    content={"improvement": {...}}
))
```

---

### [Phase 11] Cross-Domain Synthesis & Skunkworks
**Status:** NOT_STARTED  
**Estimated Complexity:** High  
**Dependencies:** Phase 9  
**Reference:** `plans/Formalization Domain Structure/phased_implementation_roadmap.md` Phase 4

#### Objectives
- Implement cross-domain synthesis engine
- Implement matrix engine for domain combination
- Implement Skunkworks protocol
- Implement discovery and justification phases

#### Tasks

- [ ] **11.1** Cross-Domain Synthesis Engine
  - [ ] File: `rlm/synthesis/cross_domain_engine.py`
  - [ ] CrossDomainSynthesisEngine class
  - [ ] Domain combination logic
  - [ ] Unified structure creation

- [ ] **11.2** Matrix Engine
  - [ ] File: `rlm/synthesis/matrix_engine.py`
  - [ ] MatrixEngine class
  - [ ] Matrix operations
  - [ ] Constraint extraction

- [ ] **11.3** Skunkworks Protocol
  - [ ] File: `rlm/skunkworks/skunkworks_protocol.py`
  - [ ] SkunkworksProtocol class
  - [ ] Discovery and justification coordination
  - [ ] File: `rlm/skunkworks/discovery_phase.py`
  - [ ] File: `rlm/skunkworks/justification_phase.py`
  - [ ] File: `rlm/skunkworks/hypothesis_manager.py`
  - [ ] File: `rlm/skunkworks/translation_engine.py`

---

### [Phase 12] Empirical Fuzzing & Universal Ontology
**Status:** NOT_STARTED  
**Estimated Complexity:** High  
**Dependencies:** Phase 11  
**Reference:** `plans/Formalization Domain Structure/phased_implementation_roadmap.md` Phase 5

#### Objectives
- Implement empirical fuzzing loop with automata learning
- Implement black-box sandbox for isolated testing
- Implement universal ontology bootstrapping for novel domains
- Implement naked axiom ban enforcement

#### Tasks

- [ ] **12.1** Empirical Fuzzing Loop
  - [ ] File: `rlm/fuzzing/empirical_loop.py`
  - [ ] File: `rlm/fuzzing/black_box_sandbox.py`
  - [ ] File: `rlm/fuzzing/automata_learner.py`
  - [ ] File: `rlm/fuzzing/fsm_generator.py`
  - [ ] File: `rlm/fuzzing/probing_agent.py`

- [ ] **12.2** Universal Ontology Bootstrapping
  - [ ] File: `rlm/ontology/universal_ontology.py`
  - [ ] File: `rlm/ontology/domain_zero.py`
  - [ ] File: `rlm/ontology/structure_generator.py`
  - [ ] File: `rlm/ontology/genesis_prover.py`
  - [ ] File: `rlm/ontology/naked_axiom_ban.py`

---

### [Phase 13] Advanced Edge Domains
**Status:** NOT_STARTED  
**Estimated Complexity:** Medium-High  
**Dependencies:** Phase 12  
**Reference:** `plans/Formalization Domain Structure/phased_implementation_roadmap.md` Phase 6

#### Objectives
- Implement advanced edge domains (cybersecurity, reverse engineering)
- Implement user-defined axiomatic overrides
- Implement hardware discovery
- Final integration and testing

#### Tasks

- [ ] **13.1** Advanced Edge Domains
  - [ ] File: `rlm/edge/advanced_edge_domains.py`
  - [ ] File: `rlm/edge/user_overrides.py`
  - [ ] File: `rlm/edge/edge_layer.py`
  - [ ] File: `rlm/edge/cybersec_tools.py`
  - [ ] File: `rlm/edge/reverse_engineering.py`
  - [ ] File: `rlm/edge/hardware_discovery.py`

---

### [Phase 14] Persistence and Session Management
**Status:** NOT_STARTED  
**Estimated Complexity:** Medium  
**Dependencies:** Phase 5  
**Reference:** `plans/agent_implementation_roadmap.md` Phase 12 (partially)

#### Objectives
- Implement session save/load
- Add checkpointing for long-running tasks
- Support session recovery on restart
- Add session history

#### Tasks

- [ ] **14.1** Enhance session persistence
  - [ ] File: `rlm/app/session_manager.py`
  - [ ] Extend existing `SessionPersistence` class
  - [ ] Save full system state (agents, messages, improvements)
  - [ ] Implement incremental checkpoints

- [ ] **14.2** Implement session recovery
  - [ ] Load session on startup
  - [ ] Resume agents from checkpoint
  - [ ] Reconnect WebSocket clients

- [ ] **14.3** Add session history UI
  - [ ] List past sessions
  - [ ] View session details
  - [ ] Delete old sessions

---

### [Phase 15] Integration Testing
**Status:** NOT_STARTED  
**Estimated Complexity:** Medium  
**Dependencies:** All previous phases  
**Reference:** `plans/agent_implementation_roadmap.md` Phase 11

#### Objectives
- End-to-end integration tests
- Performance testing
- Error scenario testing
- UI integration testing

#### Tasks

- [ ] **15.1** Create integration test suite
  - [ ] File: `tests/app/test_integration.py`
  - [ ] Test full workflow from UI to backend
  - [ ] Test agent spawning
  - [ ] Test message bus
  - [ ] Test error scenarios

- [ ] **15.2** Performance benchmarks
  - [ ] File: `tests/app/benchmarks.py`
  - [ ] Measure latency
  - [ ] Measure throughput
  - [ ] Identify bottlenecks

- [ ] **15.3** UI integration tests
  - [ ] File: `tests/app/test_ui_integration.py`
  - [ ] Test WebSocket connection
  - [ ] Test state updates
  - [ ] Test task submission

---

### [Phase 16] Documentation and Polish
**Status:** NOT_STARTED  
**Estimated Complexity:** Low  
**Dependencies:** All previous phases  
**Reference:** `plans/agent_implementation_roadmap.md` Phase 12

#### Objectives
- Complete documentation
- Code comments and docstrings
- README updates
- API documentation

#### Tasks

- [ ] **16.1** Document all public APIs
  - [ ] Docstrings for all classes and methods
  - [ ] Type hints complete
  - [ ] Usage examples

- [ ] **16.2** Update README
  - [ ] Installation instructions
  - [ ] Quick start guide
  - [ ] Architecture overview
  - [ ] API reference

- [ ] **16.3** Create deployment guide
  - [ ] File: `docs/deployment.md`
  - [ ] Docker setup
  - [ ] Environment variables
  - [ ] Production configuration

---

## Progress Tracking

### Phase Completion Summary

| Phase | Name | Status | Dependencies |
|-------|------|--------|--------------|
| Phase 0 | Type Checking System | NOT_STARTED | None (MUST be before Phase 2) |
| Phase 1 | Core Runtime Foundation | COMPLETED | None |
| Phase 2 | Agent Management System | NOT_STARTED | Phase 1 |
| Phase 3 | Message Bus | NOT_STARTED | Phase 1, 2 |
| Phase 4 | WebSocket Bridge | NOT_STARTED | Phase 1, 2 |
| Phase 5 | Task Execution Workflow | NOT_STARTED | Phase 2, 3, 4 |
| Phase 6 | Dual-Loop Architecture | NOT_STARTED | Phase 0, 5 |
| Phase 7 | Multi-Agent Orchestration | NOT_STARTED | Phase 5 |
| Phase 8 | Backend & Environment Routing | NOT_STARTED | Phase 1, 2 |
| Phase 9 | Domain Routing & Dynamic Layer 1 | NOT_STARTED | Phase 0, 6 |
| Phase 10 | Self-Improvement System | NOT_STARTED | Phase 6 |
| Phase 11 | Cross-Domain Synthesis & Skunkworks | NOT_STARTED | Phase 9 |
| Phase 12 | Empirical Fuzzing & Ontology | NOT_STARTED | Phase 11 |
| Phase 13 | Advanced Edge Domains | NOT_STARTED | Phase 12 |
| Phase 14 | Persistence & Session | NOT_STARTED | Phase 5 |
| Phase 15 | Integration Testing | NOT_STARTED | All phases |
| Phase 16 | Documentation & Polish | NOT_STARTED | All phases |

---

## Dependencies Graph

```
Phase 0 (Type Checking) ──────────────────────────────────────────┐
    │                                                              │
    ├──────────────────────────────────────────────────────────────┤
    │                                                              │
Phase 1                                                            │
    │                                                              │
    ├──────────────────┬───────────────────┐                       │
    │                  │                   │                       │
Phase 2              Phase 4             Phase 8                   │
    │                  │                   │                       │
    ├──────────────────┴───────────────────┤                       │
    │                                      │                       │
Phase 3 ◄─────────────────────────────────┘                       │
    │                                                              │
Phase 4 ──────────────────────────────────────────────────────────┤
    │                                                              │
Phase 5 ──────────────────────────────────────────────────────────┤
    │                                                              │
Phase 6 ◄─────────────────────────────────────────────────────────┤
    │                                                              │
Phase 7                                                             │
    │                                                              │
Phase 9 ◄─────────────────────────────────────────────────────────┤
    │                                                              │
Phase 10                                                            │
    │                                                              │
Phase 11                                                            │
    │                                                              │
Phase 12                                                            │
    │                                                              │
Phase 13                                                            │
    │                                                              │
Phase 14                                                            │
    │                                                              │
Phase 15 (Integration Tests)                                       │
    │                                                              │
Phase 16 (Documentation)                                           │
```

---

## Reference Documents

This unified plan consolidates the following plans:

| Source Plan | Reference | Key Content |
|-------------|-----------|-------------|
| Type Checking System | `.kilo/plans/1774673361830-gentle-otter.md` | Phase 0: Haskell & Lean checkers |
| Application Runtime | `plans/IMPLEMENTATION_PLAN.md` | Phases 1-10 (original) |
| Axiomatic RLM Routing | `plans/axiomatic_rlm_routing_integration_plan.md` | Layer 1 + routing integration |
| Formalization Domain Structure | `plans/Formalization Domain Structure/phased_implementation_roadmap.md` | Phases 6-13 |
| Agent Implementation Roadmap | `plans/agent_implementation_roadmap.md` | Phases 2-16 (agents, tools, UI) |
| RLM Routing Upgrade | `plans/rlm_upgrade/rlm-routing-upgrade-overview.md` | Phase 8: Backend/Env routing |

---

## File Structure (Updated)

```
Self_AI/
├── app.py                              # Phase 1: Application entry point
├── config/
│   ├── type-checking.yaml               # Phase 0E: Type checking config
│   ├── dual-loop.yaml                   # Phase 6: Dual-loop config
│   ├── domain-routing.yaml              # Phase 9: Domain routing config
│   └── ... (other configs)
├── rlm/
│   ├── app/
│   │   ├── dependencies.py              # Phase 1: Dependency container
│   │   ├── logging_config.py            # Phase 1: Logging setup
│   │   ├── orchestrator.py             # Phase 1, 5, 7: Orchestrator
│   │   ├── agent_config.py              # Phase 2: Agent config
│   │   ├── rlm_executor.py              # Phase 2, 7: RLM wrapper
│   │   ├── agent_manager.py             # Phase 2: Agent lifecycle
│   │   ├── state_sync.py                # Phase 2: Redux sync
│   │   ├── messages.py                  # Phase 3: Message types
│   │   ├── message_bus.py              # Phase 3: Message bus
│   │   ├── message_handlers.py         # Phase 3: Message handlers
│   │   ├── ws_bridge.py                 # Phase 4: WebSocket bridge
│   │   ├── result_streamer.py           # Phase 5: Result streaming
│   │   ├── task_decomposer.py           # Phase 7: Task decomposition
│   │   ├── result_aggregator.py         # Phase 7: Result aggregation
│   │   ├── improvement_registry.py     # Phase 10: Improvements
│   │   ├── tool_registry.py            # Phase 10: Tool registry
│   │   ├── improvement_review.py       # Phase 10: Review workflow
│   │   └── session_manager.py          # Phase 14: Session management
│   ├── typechecking/                    # Phase 0: NEW
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── result.py
│   │   ├── exceptions.py
│   │   ├── config.py
│   │   ├── registry.py
│   │   ├── config_loader.py
│   │   ├── haskell/
│   │   │   ├── haskell_checker.py
│   │   │   ├── ghc_checker.py
│   │   │   └── result.py
│   │   └── lean/
│   │       ├── lean_checker.py
│   │       ├── lake_checker.py
│   │       └── result.py
│   ├── loops/                           # Phase 6: NEW
│   │   ├── fast_loop.py
│   │   ├── slow_loop.py
│   │   ├── release_candidate.py
│   │   ├── message_queue.py
│   │   ├── interrupt_protocol.py
│   │   └── loop_manager.py
│   ├── routing/
│   │   ├── backend_router.py            # Phase 8: (exists, enhance)
│   │   ├── backend_factory.py           # Phase 8: (exists, verify)
│   │   ├── task_descriptor.py           # Phase 8: (exists, enhance)
│   │   ├── environment_router.py       # Phase 8: NEW
│   │   ├── domain_classifier.py         # Phase 9: NEW
│   │   ├── domain_router.py             # Phase 9: NEW
│   │   ├── domain_config.py             # Phase 9: NEW
│   │   └── domain_metadata.py          # Phase 9: NEW
│   ├── layer1/                         # Phase 9: NEW
│   │   └── dynamic_loader.py
│   ├── synthesis/                        # Phase 11: NEW
│   │   ├── cross_domain_engine.py
│   │   ├── matrix_engine.py
│   │   ├── domain_structure.py
│   │   ├── synthesis_translator.py
│   │   └── genesis_prover.py
│   ├── skunkworks/                      # Phase 11: NEW
│   │   ├── skunkworks_protocol.py
│   │   ├── discovery_phase.py
│   │   ├── justification_phase.py
│   │   ├── hypothesis_manager.py
│   │   ├── skunkworks_environment.py
│   │   └── translation_engine.py
│   ├── fuzzing/                         # Phase 12: NEW
│   │   ├── empirical_loop.py
│   │   ├── black_box_sandbox.py
│   │   ├── automata_learner.py
│   │   ├── fsm_generator.py
│   │   └── probing_agent.py
│   ├── ontology/                        # Phase 12: NEW
│   │   ├── universal_ontology.py
│   │   ├── domain_zero.py
│   │   ├── structure_generator.py
│   │   ├── genesis_prover.py
│   │   └── naked_axiom_ban.py
│   ├── edge/                            # Phase 13: NEW
│   │   ├── advanced_edge_domains.py
│   │   ├── user_overrides.py
│   │   ├── edge_layer.py
│   │   ├── cybersec_tools.py
│   │   ├── reverse_engineering.py
│   │   └── hardware_discovery.py
│   ├── research/                        # Phase 9: NEW
│   │   └── domain_sources.py
│   ├── core/
│   │   └── rlm.py                       # Enhanced with loop_manager
│   ├── redux/
│   │   ├── store.py                     # Enhanced
│   │   └── slices/
│   │       ├── verification_slice.py     # Phase 0: (exists, verify)
│   │       ├── loop_slice.py            # Phase 6: NEW
│   │       ├── routing_slice.py         # Phase 8: NEW
│   │       ├── domain_slice.py          # Phase 9: NEW
│   │       ├── synthesis_slice.py       # Phase 11: NEW
│   │       ├── fuzzing_slice.py        # Phase 12: NEW
│   │       ├── ontology_slice.py        # Phase 12: NEW
│   │       └── edge_slice.py            # Phase 13: NEW
│   ├── agents/
│   │   └── verification_agent_factory.py # Enhanced for dual-loop
│   ├── environments/
│   │   ├── layer1_bootstrap.py         # Enhanced for dynamic loading
│   │   └── local_repl.py                # Enhanced with type checking
│   └── utils/
│       └── key_encryption.py            # Existing
├── tests/
│   ├── typechecking/                    # Phase 0F: NEW
│   ├── loops/                           # Phase 6: NEW
│   ├── routing/                         # Phase 9: NEW
│   ├── synthesis/                       # Phase 11: NEW
│   ├── skunkworks/                      # Phase 11: NEW
│   ├── fuzzing/                         # Phase 12: NEW
│   ├── ontology/                        # Phase 12: NEW
│   ├── edge/                            # Phase 13: NEW
│   ├── app/                             # Phase 15: Integration tests
│   └── integration/
│       └── test_typechecking_flow.py    # Phase 0F: NEW
└── docs/
    └── deployment.md                    # Phase 16: NEW
```

---

## Notes for Next Agent

### Session Resume Instructions

If resuming from this plan:

1. **Check phase status** in the "Progress Tracking" section above
2. **Read current implementation** in the files listed for the current phase
3. **Run existing tests** to verify nothing is broken:
   ```bash
   cd /path/to/Self_AI
   python -m pytest tests/ -v
   ```
4. **Read this entire document** before making changes
5. **Mark tasks as started** when beginning work

### Critical Path

The **CRITICAL PATH** is:
```
Phase 0 (Type Checking) → Phase 5 (Task Execution) → Phase 6 (Dual-Loop)
```

### Coding Standards

- Use `asyncio` for all async operations
- Follow existing code style (Python standard with type hints)
- Add docstrings to all public methods
- Add tests for new functionality
- Update this document when completing tasks

---

## Changelog

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-03-28 | 1.0 | Initial document created | Kilo |
| 2026-03-28 | 2.0 | Unified with Type Checking, Formalization Domain, Agent Roadmap, RLM Routing plans | Kilo |
