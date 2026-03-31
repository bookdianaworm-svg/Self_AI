# Branch Mapping for AI Agents

## Purpose
This document provides a comprehensive mapping of all branches to their specific purposes, enabling AI agents to quickly determine which branch to work on without guessing or unnecessary exploration.

## Branch Reference Map

### Quick Reference Table

| Branch | Purpose | Dependencies | Key Directories | When to Use |
|--------|---------|--------------|-----------------|-------------|
| **main** | Production-ready code | None | All | Production deployment, releases |
| **develop** | Integration branch | All features | All | Testing integration, staging |
| **feature/redux-state-management** | Redux store with slices | None | `rlm/redux/` | State management, Redux slices |
| **feature/agent-framework** | Base agent classes | None | `agents/`, `rlm/agents/` | Creating/modifying agents |
| **feature/messaging-system** | Messaging infrastructure | None | `messaging/`, `rlm/messaging/` | Agent communication, messaging |
| **feature/dynamic-tools** | Tool registry system | None | `tools/`, `rlm/tools/` | Creating tools, tool management |
| **feature/verification-system** | Lean 4 verification | agent-framework | `rlm/agents/prompts/`, `rlm/agents/verification_*` | Code verification, proofs |
| **feature/backend-diversity** | Multi-backend routing | None | `rlm/routing/`, `rlm/clients/` | Adding backends, routing |
| **feature/self-improvement** | Improvement system | dynamic-tools, messaging | `improvements/`, `rlm/improvements/` | Self-improvement, learning |
| **feature/swarm-orchestration** | Swarm orchestration | redux, agents, messaging | `rlm/core/swarm_rlm.py`, `rlm/swarm/` | Swarm coordination, spawning |
| **feature/visualization-interface** | Monitoring UI | redux, messaging | `ui/`, `visualization/`, `rlm/ui/` | Dashboards, monitoring, UI |
| **feature/testing-infrastructure** | Test framework | None | `tests/`, `.github/workflows/` | Writing tests, CI/CD |

## Detailed Branch Information

### 1. main (Production Branch)

**Purpose**: Production-ready, stable code that has been fully tested and approved.

**Characteristics**:
- Read-only for development
- Only receives merges from develop
- Contains released versions
- Always stable and deployable

**When to Work Here**:
- Almost never for development
- Only for hotfixes in emergencies
- After approval from team

**Key Files**:
- All production code
- Released documentation
- Stable configuration files

**AI Agent Guidance**:
```python
if task.requires_production_fix and task.is_emergency:
    work_branch = "main"
else:
    # Work on feature branch first, then merge
    work_branch = "develop"
```

---

### 2. develop (Integration Branch)

**Purpose**: Integration branch where all completed features are merged for testing.

**Characteristics**:
- Receives merges from all feature branches
- Used for integration testing
- Pre-production staging area
- May have conflicts that need resolution

**When to Work Here**:
- Testing integration of multiple features
- Resolving merge conflicts
- Preparing for release to main
- Running full test suite

**Key Files**:
- All code from merged features
- Integration tests
- Release notes

**AI Agent Guidance**:
```python
if task.involves_integration_testing:
    work_branch = "develop"
elif task.involves_resolving_conflicts:
    work_branch = "develop"
else:
    # Work on specific feature branch
    work_branch = identify_feature_branch(task)
```

---

### 3. feature/redux-state-management

**Purpose**: Redux-style state management with slices for agents, tasks, messages, system state, tools, and improvements.

**Characteristics**:
- No dependencies
- Independent feature
- Foundation for many other features

**When to Work Here**:
- Creating Redux slices
- Modifying store configuration
- Adding state management
- Implementing middleware
- Working with state actions/reducers

**Key Directories**:
```
rlm/redux/
├── __init__.py
├── store/
│   ├── __init__.py
│   └── store.py
├── slices/
│   ├── __init__.py
│   ├── agent_slice.py
│   ├── task_slice.py
│   ├── message_slice.py
│   ├── system_slice.py
│   ├── tool_slice.py
│   └── improvement_slice.py
└── middleware/
    ├── __init__.py
    ├── state_sync_middleware.py
    ├── conflict_resolution_middleware.py
    └── performance_optimization_middleware.py
```

**Key Classes/Functions**:
- `configureStore()` - Create Redux store
- `createSlice()` - Create Redux slice
- `combineReducers()` - Combine multiple reducers
- Agent actions/reducers
- Task actions/reducers
- Message actions/reducers

**AI Agent Guidance**:
```python
if "redux" in task.description.lower() or "state" in task.description.lower():
    if "agent" in task.description.lower():
        work_on = "rlm/redux/slices/agent_slice.py"
    elif "task" in task.description.lower():
        work_on = "rlm/redux/slices/task_slice.py"
    elif "message" in task.description.lower():
        work_on = "rlm/redux/slices/message_slice.py"
    else:
        work_branch = "feature/redux-state-management"
```

---

### 4. feature/agent-framework

**Purpose**: Base agent classes and specialized agent implementations.

**Characteristics**:
- No dependencies
- Independent feature
- Foundation for swarm system
- Dependency for verification-system

**When to Work Here**:
- Creating new agent types
- Modifying agent behavior
- Implementing agent lifecycle
- Adding agent capabilities
- Working with agent spawning

**Key Directories**:
```
agents/
├── __init__.py
├── base_agent.py
├── task_agent.py
├── intelligent_agent.py
└── specialized/

rlm/agents/
├── __init__.py
├── base_agent.py
├── prompts/
│   ├── __init__.py
│   └── base_prompts.py
└── utils/
    ├── __init__.py
    └── agent_utils.py
```

**Key Classes**:
- `BaseAgent` - Abstract base class for all agents
- `TaskProcessingAgent` - Agent specialized for task execution
- `IntelligentAgent` - Agent with advanced capabilities
- `AgentConfig` - Configuration for agent initialization
- `AgentStatus` - Agent status enum

**Key Methods**:
- `execute_task()` - Execute assigned task
- `spawn_agent()` - Create new agent
- `send_message()` - Send message to another agent
- `receive_message()` - Receive and process message

**AI Agent Guidance**:
```python
if "agent" in task.description.lower():
    if "spawn" in task.description.lower():
        work_on = "agents/base_agent.py"
    elif "task" in task.description.lower():
        work_on = "agents/task_agent.py"
    elif "base" in task.description.lower():
        work_on = "agents/base_agent.py"
    else:
        work_branch = "feature/agent-framework"
```

---

### 5. feature/messaging-system

**Purpose**: Messaging and communication infrastructure for agents and system components.

**Characteristics**:
- No dependencies
- Independent feature
- Foundation for swarm communication
- Dependency for self-improvement and visualization

**When to Work Here**:
- Implementing agent communication
- Creating message types
- Setting up message routing
- Working with publish-subscribe
- Implementing broadcast patterns

**Key Directories**:
```
messaging/
├── __init__.py
├── message_broker.py
├── message_types.py
└── protocols/
    ├── __init__.py
    ├── request_response.py
    ├── pub_sub.py
    └── broadcast.py

rlm/messaging/
├── __init__.py
├── message_broker.py
└── message_utils.py
```

**Key Classes**:
- `MessageBroker` - Central message routing hub
- `Message` - Message data class
- `MessageType` - Message type enum
- `MessagePriority` - Message priority enum

**Key Methods**:
- `send_message()` - Send a message
- `register_agent()` - Register agent with broker
- `subscribe_to_topic()` - Subscribe to message topic
- `broadcast()` - Send message to all

**AI Agent Guidance**:
```python
if any(word in task.description.lower() for word in ["message", "communicate", "send", "receive"]):
    if "broker" in task.description.lower():
        work_on = "messaging/message_broker.py"
    elif "type" in task.description.lower():
        work_on = "messaging/message_types.py"
    else:
        work_branch = "feature/messaging-system"
```

---

### 6. feature/dynamic-tools

**Purpose**: Dynamic tool discovery, creation, registry, and approval workflow.

**Characteristics**:
- No dependencies
- Independent feature
- Dependency for self-improvement

**When to Work Here**:
- Creating tools
- Implementing tool registry
- Setting up tool approval
- Working with dynamic tool creation
- Managing tool sharing

**Key Directories**:
```
tools/
├── __init__.py
├── tool_registry.py
├── tool_creator.py
└── validators/
    ├── __init__.py
    └── tool_validator.py

rlm/tools/
├── __init__.py
├── base_tool.py
└── builtins/
    ├── __init__.py
    ├── file_tool.py
    └── network_tool.py
```

**Key Classes**:
- `ToolRegistry` - Registry for managing tools
- `ToolDefinition` - Tool definition data class
- `ToolParameter` - Tool parameter data class
- `BaseTool` - Abstract base class for tools

**Key Methods**:
- `register_tool()` - Register a new tool
- `get_tool()` - Retrieve a tool
- `create_dynamic_tool()` - Create tool from code
- `approve_tool()` - Approve a tool for use

**AI Agent Guidance**:
```python
if any(word in task.description.lower() for word in ["tool", "registry", "dynamic"]):
    if "registry" in task.description.lower():
        work_on = "tools/tool_registry.py"
    elif "create" in task.description.lower():
        work_on = "tools/tool_creator.py"
    else:
        work_branch = "feature/dynamic-tools"
```

---

### 7. feature/verification-system

**Purpose**: Lean 4 axiomatic seed integration for code verification and proof checking.

**Characteristics**:
- Depends on: feature/agent-framework
- Requires agents to be implemented first

**When to Work Here**:
- Implementing code verification
- Integrating Lean 4
- Creating verification prompts
- Setting up proof checking
- Working with axiomatic seeds

**Key Directories**:
```
rlm/agents/
├── prompts/
│   ├── __init__.py
│   ├── verification_prompts.py
│   └── lean_prompts.py
├── verification_agent_factory.py
└── verification/
    ├── __init__.py
    ├── lean_interface.py
    └── proof_checker.py
```

**Key Classes**:
- `VerificationAgent` - Agent for code verification
- `LeanInterface` - Interface to Lean 4
- `ProofChecker` - Proof checking utilities
- `AxiomaticSeed` - Axiomatic seed definitions

**Key Methods**:
- `verify_code()` - Verify code correctness
- `generate_proof()` - Generate formal proof
- `check_proof()` - Check proof validity
- `extract_axioms()` - Extract axioms from code

**AI Agent Guidance**:
```python
if any(word in task.description.lower() for word in ["verify", "proof", "lean", "axiom"]):
    # Check if agent-framework is available
    if check_branch_status("feature/agent-framework"):
        work_branch = "feature/verification-system"
    else:
        # Work on agent-framework first
        work_branch = "feature/agent-framework"
        task.add_dependency("feature/agent-framework")
```

---

### 8. feature/backend-diversity

**Purpose**: Multi-backend routing, environment selection, and backend optimization.

**Characteristics**:
- No dependencies
- Independent feature

**When to Work Here**:
- Adding new AI backends
- Implementing routing logic
- Optimizing backend selection
- Working with multiple environments
- Setting up backend factories

**Key Directories**:
```
rlm/
├── clients/
│   ├── __init__.py
│   ├── base_lm.py
│   ├── openai.py
│   ├── anthropic.py
│   ├── gemini.py
│   ├── litellm.py
│   └── portkey.py
├── routing/
│   ├── __init__.py
│   ├── backend_router.py
│   ├── backend_factory.py
│   ├── task_descriptor.py
│   └── environment_selector.py
└── environments/
    ├── __init__.py
    ├── base_env.py
    ├── local_repl.py
    └── daytona_repl.py
```

**Key Classes**:
- `BackendRouter` - Route tasks to appropriate backends
- `BackendFactory` - Create backend instances
- `TaskDescriptor` - Describe task characteristics
- `EnvironmentSelector` - Select execution environment

**Key Methods**:
- `route_task()` - Route task to backend
- `create_backend()` - Create backend instance
- `select_backend()` - Select optimal backend
- `select_environment()` - Select execution environment

**AI Agent Guidance**:
```python
if any(word in task.description.lower() for word in ["backend", "routing", "environment", "llm", "model"]):
    if "router" in task.description.lower():
        work_on = "rlm/routing/backend_router.py"
    elif "client" in task.description.lower():
        work_on = "rlm/clients/"
    else:
        work_branch = "feature/backend-diversity"
```

---

### 9. feature/self-improvement

**Purpose**: Self-improvement system with contribution, approval, and application workflows.

**Characteristics**:
- Depends on: feature/dynamic-tools, feature/messaging-system
- Requires tools and messaging to be implemented first

**When to Work Here**:
- Implementing self-improvement
- Creating improvement proposals
- Setting up approval workflow
- Managing improvement application
- Working with learning capabilities

**Key Directories**:
```
improvements/
├── __init__.py
├── improvement_registry.py
├── improvement_proposer.py
├── improvement_applicator.py
└── evaluators/
    ├── __init__.py
    ├── performance_evaluator.py
    └── safety_evaluator.py

rlm/improvements/
├── __init__.py
├── base_improvement.py
└── strategies/
    ├── __init__.py
    ├── performance_optimization.py
    └── code_refactoring.py
```

**Key Classes**:
- `ImprovementRegistry` - Registry for improvements
- `ImprovementEntity` - Improvement data structure
- `ImprovementProposer` - Propose improvements
- `ImprovementApplicator` - Apply improvements

**Key Methods**:
- `propose_improvement()` - Propose a new improvement
- `approve_improvement()` - Approve an improvement
- `apply_improvement()` - Apply an improvement
- `evaluate_improvement()` - Evaluate improvement impact

**AI Agent Guidance**:
```python
if any(word in task.description.lower() for word in ["improve", "optimization", "refactor", "learn"]):
    # Check dependencies
    deps_ok = all(check_branch_status(b) for b in ["feature/dynamic-tools", "feature/messaging-system"])
    
    if deps_ok:
        work_branch = "feature/self-improvement"
    else:
        # Work on dependencies first
        work_branch = "feature/dynamic-tools"  # or messaging-system
```

---

### 10. feature/swarm-orchestration

**Purpose**: Main swarm instance with continuous spawning, coordination, and orchestration.

**Characteristics**:
- Depends on: feature/redux-state-management, feature/agent-framework, feature/messaging-system
- Core orchestration for entire system

**When to Work Here**:
- Implementing swarm coordination
- Creating spawning logic
- Managing agent lifecycles
- Working with orchestration
- Implementing swarm behavior

**Key Directories**:
```
rlm/
├── core/
│   ├── swarm_rlm.py
│   ├── rlm.py
│   └── types.py
└── swarm/
    ├── __init__.py
    ├── orchestrator.py
    ├── coordinator.py
    └── strategies/
        ├── __init__.py
        ├── spawning_strategy.py
        └── load_balancing.py
```

**Key Classes**:
- `SwarmRLM` - Enhanced RLM with swarm capabilities
- `Orchestrator` - Orchestrate swarm operations
- `SwarmAgent` - Agent in swarm system
- `SpawningStrategy` - Strategy for spawning agents

**Key Methods**:
- `spawn_agent()` - Spawn new agent
- `coordinate_agents()` - Coordinate multiple agents
- `orchestrate_task()` - Orchestrate task execution
- `balance_load()` - Balance load across agents

**AI Agent Guidance**:
```python
if any(word in task.description.lower() for word in ["swarm", "orchestrate", "coordinate", "spawn"]):
    # Check dependencies
    deps_ok = all(check_branch_status(b) for b in [
        "feature/redux-state-management",
        "feature/agent-framework",
        "feature/messaging-system"
    ])
    
    if deps_ok:
        work_branch = "feature/swarm-orchestration"
    else:
        # Work on dependencies first
        work_branch = "feature/redux-state-management"
```

---

### 11. feature/visualization-interface

**Purpose**: Real-time monitoring UI, agent grid, communication log, and system metrics.

**Characteristics**:
- Depends on: feature/redux-state-management, feature/messaging-system
- Provides visualization for swarm system

**When to Work Here**:
- Creating dashboards
- Implementing monitoring
- Building UI components
- Working with visualization
- Setting up real-time updates

**Key Directories**:
```
ui/
├── __init__.py
├── dashboard.py
├── agent_grid.py
├── communication_log.py
├── system_metrics.py
└── components/
    ├── __init__.py
    ├── agent_card.py
    ├── message_display.py
    └── metric_chart.py

rlm/ui/
├── __init__.py
└── state_viewer.py
```

**Key Classes**:
- `Dashboard` - Main dashboard component
- `AgentGrid` - Display agents in grid
- `CommunicationLog` - Log communications
- `SystemMetrics` - Display system metrics
- `StateViewer` - View Redux state

**Key Methods**:
- `update_dashboard()` - Update dashboard display
- `render_agent_grid()` - Render agent grid
- `log_communication()` - Log communication event
- `display_metrics()` - Display system metrics

**AI Agent Guidance**:
```python
if any(word in task.description.lower() for word in ["ui", "dashboard", "visual", "monitor", "display"]):
    # Check dependencies
    deps_ok = all(check_branch_status(b) for b in [
        "feature/redux-state-management",
        "feature/messaging-system"
    ])
    
    if deps_ok:
        work_branch = "feature/visualization-interface"
    else:
        # Work on dependencies first
        work_branch = "feature/redux-state-management"
```

---

### 12. feature/testing-infrastructure

**Purpose**: Test framework, CI/CD workflows, and testing utilities.

**Characteristics**:
- No dependencies
- Independent feature

**When to Work Here**:
- Writing tests
- Setting up CI/CD
- Creating test utilities
- Implementing test fixtures
- Working with test automation

**Key Directories**:
```
tests/
├── __init__.py
├── conftest.py
├── unit/
│   ├── __init__.py
│   ├── test_agents/
│   ├── test_messaging/
│   ├── test_redux/
│   ├── test_tools/
│   └── test_verification/
├── integration/
│   ├── __init__.py
│   ├── test_swarm/
│   └── test_ui/
└── e2e/
    ├── __init__.py
    └── test_full_swarm/

.github/
└── workflows/
    ├── test.yml
    ├── lint.yml
    └── deploy.yml
```

**Key Files**:
- `pytest.ini` - Pytest configuration
- `conftest.py` - Pytest fixtures
- Test files (test_*.py)
- CI/CD workflow files

**AI Agent Guidance**:
```python
if any(word in task.description.lower() for word in ["test", "ci", "cd", "workflow"]):
    if "pytest" in task.description.lower():
        work_on = "pytest.ini"
    elif "workflow" in task.description.lower():
        work_on = ".github/workflows/"
    else:
        work_branch = "feature/testing-infrastructure"
```

---

## Decision Tree for Branch Selection

```python
def select_branch(task_description: str) -> str:
    """
    Select the appropriate branch based on task description.
    """
    task_lower = task_description.lower()
    
    # Production hotfix (rare)
    if "hotfix" in task_lower or "production" in task_lower:
        return "main"
    
    # Integration testing
    if "integration" in task_lower or "conflict" in task_lower:
        return "develop"
    
    # Testing infrastructure
    if any(word in task_lower for word in ["test", "ci", "cd", "workflow"]):
        return "feature/testing-infrastructure"
    
    # Redux/State management
    if any(word in task_lower for word in ["redux", "state", "store", "slice", "reducer"]):
        return "feature/redux-state-management"
    
    # Agent framework
    if any(word in task_lower for word in ["agent", "spawn", "agent lifecycle"]):
        return "feature/agent-framework"
    
    # Messaging system
    if any(word in task_lower for word in ["message", "communicate", "broker", "pubsub"]):
        return "feature/messaging-system"
    
    # Dynamic tools
    if any(word in task_lower for word in ["tool", "registry", "dynamic tool"]):
        return "feature/dynamic-tools"
    
    # Verification system
    if any(word in task_lower for word in ["verify", "proof", "lean", "axiom"]):
        return "feature/verification-system"
    
    # Backend diversity
    if any(word in task_lower for word in ["backend", "routing", "llm", "model"]):
        return "feature/backend-diversity"
    
    # Self-improvement
    if any(word in task_lower for word in ["improve", "optimization", "refactor", "learn"]):
        return "feature/self-improvement"
    
    # Swarm orchestration
    if any(word in task_lower for word in ["swarm", "orchestrate", "coordinate"]):
        return "feature/swarm-orchestration"
    
    # Visualization interface
    if any(word in task_lower for word in ["ui", "dashboard", "visual", "monitor"]):
        return "feature/visualization-interface"
    
    # Default to develop
    return "develop"
```

## Dependency Checking

```python
def check_branch_dependencies(branch: str) -> dict:
    """
    Check if branch dependencies are satisfied.
    Returns dict with 'satisfied' (bool) and 'missing' (list).
    """
    dependencies = {
        "feature/verification-system": ["feature/agent-framework"],
        "feature/self-improvement": ["feature/dynamic-tools", "feature/messaging-system"],
        "feature/swarm-orchestration": [
            "feature/redux-state-management",
            "feature/agent-framework",
            "feature/messaging-system"
        ],
        "feature/visualization-interface": [
            "feature/redux-state-management",
            "feature/messaging-system"
        ]
    }
    
    if branch not in dependencies:
        return {"satisfied": True, "missing": []}
    
    missing = []
    for dep in dependencies[branch]:
        # Check if dependency branch is ready
        # This would check if the branch has been merged to develop
        if not branch_is_ready(dep):
            missing.append(dep)
    
    return {
        "satisfied": len(missing) == 0,
        "missing": missing
    }
```

## Summary

This branch mapping document provides:
- ✅ Complete reference for all 14 branches
- ✅ Quick decision tree for branch selection
- ✅ Detailed information for each branch
- ✅ Key files and classes for each branch
- ✅ Dependency checking logic
- ✅ AI agent guidance for each feature

Use this document whenever you need to:
- Select the appropriate branch for a task
- Understand branch purposes
- Check branch dependencies
- Navigate the codebase structure
- Guide AI agents to correct branches
- Plan development work
