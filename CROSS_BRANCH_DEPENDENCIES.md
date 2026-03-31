# Cross-Branch Dependency Analysis

## Overview
This document analyzes the dependencies between all 14 branches in the Self_AI repository to enable efficient parallel development and testing.

## Branch Classification

### Primary Branches (2)
- **main** - Production-ready code (no dependencies)
- **develop** - Integration branch (depends on all feature branches)

### Feature Branches (10)
- **feature/redux-state-management** - Core state management (no dependencies)
- **feature/agent-framework** - Agent base classes (no dependencies)
- **feature/messaging-system** - Communication infrastructure (no dependencies)
- **feature/dynamic-tools** - Tool registry (no dependencies)
- **feature/verification-system** - Lean 4 integration (depends on agent-framework)
- **feature/backend-diversity** - Multi-backend routing (no dependencies)
- **feature/self-improvement** - Improvement system (depends on dynamic-tools, messaging-system)
- **feature/swarm-orchestration** - Main orchestration (depends on redux-state-management, agent-framework, messaging-system)
- **feature/visualization-interface** - Monitoring UI (depends on redux-state-management, messaging-system)
- **feature/testing-infrastructure** - Test framework (no dependencies)

### Legacy Branches (2)
- **general-caravel** - Legacy (preserve for reference only)
- **test-feature** - Legacy (preserve for reference only)

## Dependency Graph

```
main (production)
  └─ develop (integration)
       ├─ feature/redux-state-management (independent)
       ├─ feature/agent-framework (independent)
       ├─ feature/messaging-system (independent)
       ├─ feature/dynamic-tools (independent)
       ├─ feature/verification-system
       │   └─ depends on: agent-framework
       ├─ feature/backend-diversity (independent)
       ├─ feature/self-improvement
       │   ├─ depends on: dynamic-tools
       │   └─ depends on: messaging-system
       ├─ feature/swarm-orchestration
       │   ├─ depends on: redux-state-management
       │   ├─ depends on: agent-framework
       │   └─ depends on: messaging-system
       ├─ feature/visualization-interface
       │   ├─ depends on: redux-state-management
       │   └─ depends on: messaging-system
       └─ feature/testing-infrastructure (independent)
```

## Dependency Levels

### Level 0: Independent Features (Can start immediately)
These branches have no dependencies and can be developed in parallel:

1. **feature/redux-state-management**
   - Purpose: Redux store with slices for agents, tasks, messages, system, tools, improvements
   - Core files: `rlm/redux/`
   - Can work on this branch without any other branches

2. **feature/agent-framework**
   - Purpose: Base agent classes (BaseAgent, TaskProcessingAgent, etc.)
   - Core files: `agents/` (to be created)
   - Can work on this branch without any other branches

3. **feature/messaging-system**
   - Purpose: Message broker, message types, communication protocols
   - Core files: `messaging/` (to be created)
   - Can work on this branch without any other branches

4. **feature/dynamic-tools**
   - Purpose: Tool registry, dynamic tool creation, approval workflow
   - Core files: `tools/` (to be created)
   - Can work on this branch without any other branches

5. **feature/backend-diversity**
   - Purpose: Multi-backend routing, environment selection
   - Core files: `rlm/routing/`
   - Can work on this branch without any other branches

6. **feature/testing-infrastructure**
   - Purpose: Test framework, CI/CD workflows
   - Core files: `tests/`, `.github/workflows/`
   - Can work on this branch without any other branches

### Level 1: Single Dependency Features (Can start after Level 0)

7. **feature/verification-system**
   - Purpose: Lean 4 axiomatic seed integration for verification
   - Depends on: **feature/agent-framework**
   - Core files: `rlm/agents/prompts/verification_prompts.py`, `rlm/agents/verification_agent_factory.py`
   - Can start after agent-framework is stable

### Level 2: Double Dependency Features (Can start after Level 0 + Level 1)

8. **feature/self-improvement**
   - Purpose: Improvement contribution system with approval and application
   - Depends on: **feature/dynamic-tools**, **feature/messaging-system**
   - Core files: `improvements/` (to be created)
   - Can start after tools and messaging are stable

9. **feature/swarm-orchestration**
   - Purpose: Main swarm instance with continuous spawning and coordination
   - Depends on: **feature/redux-state-management**, **feature/agent-framework**, **feature/messaging-system**
   - Core files: `rlm/core/swarm_rlm.py` (to be created)
   - Can start after Redux, agents, and messaging are stable

10. **feature/visualization-interface**
    - Purpose: Real-time monitoring UI with agent grid, communication log
    - Depends on: **feature/redux-state-management**, **feature/messaging-system**
    - Core files: `ui/` or `visualization/` (to be created)
    - Can start after Redux and messaging are stable

## Development Strategy

### Phase 1: Foundation (Parallel Development - Week 1-2)
All Level 0 branches can be developed simultaneously:
- **Teams**: Split into 6 teams (one per Level 0 branch)
- **Worktrees**: Create worktrees for each branch to enable parallel development
- **Communication**: Use feature branches for code review

### Phase 2: First Integration (Week 3)
Integrate Level 0 features into develop:
- Merge all Level 0 branches to develop
- Test integration
- Resolve any conflicts

### Phase 3: Secondary Features (Week 3-4)
Start Level 1 and Level 2 features:
- Start **feature/verification-system** after agent-framework is stable
- Start **feature/self-improvement** after tools and messaging are stable
- Start **feature/swarm-orchestration** after Redux, agents, messaging are stable
- Start **feature/visualization-interface** after Redux and messaging are stable

### Phase 4: Final Integration (Week 5-6)
Integrate all features:
- Merge all remaining features to develop
- Full integration testing
- Performance testing
- Documentation

### Phase 5: Production Release (Week 7)
- Merge develop to main
- Tag release v1.0.0
- Deploy to production

## Cross-Branch File Conflicts

### Potential Conflicts (High Priority)

1. **`rlm/` directory**
   - Multiple branches modify files in `rlm/`
   - **Conflicts**: `rlm/core/`, `rlm/agents/`, `rlm/routing/`
   - **Resolution**: Use merge strategies, resolve conflicts manually
   - **Prevention**: Coordinate through develop branch, review changes before merging

2. **`tests/` directory**
   - All branches add tests
   - **Conflicts**: Test files with similar names
   - **Resolution**: Use descriptive test names, organize by feature
   - **Prevention**: Create feature-specific test directories (e.g., `tests/agent_framework/`)

3. **Configuration files**
   - Multiple branches may modify `requirements.txt`, `pytest.ini`
   - **Conflicts**: Dependency versions, test configurations
   - **Resolution**: Merge carefully, test after merging
   - **Prevention**: Coordinate dependency additions through develop

### Low Risk Conflicts

1. **New directories**
   - Each feature branch creates its own directory
   - **Example**: `agents/`, `messaging/`, `tools/`, `improvements/`, `ui/`
   - **Risk**: Low - no direct conflicts
   - **Strategy**: Each feature owns its directory

2. **Documentation**
   - Each branch updates its own documentation
   - **Example**: `docs/feature_redux.md`, `docs/feature_agents.md`
   - **Risk**: Low - minimal conflicts
   - **Strategy**: Separate documentation files per feature

## Worktree Setup Strategy

### Recommended Worktree Layout

```
Self_AI/
├── main/                    # Main worktree (current)
├── develop/                 # Integration worktree
├── wt-redux/               # feature/redux-state-management worktree
├── wt-agents/              # feature/agent-framework worktree
├── wt-messaging/           # feature/messaging-system worktree
├── wt-tools/               # feature/dynamic-tools worktree
├── wt-verification/        # feature/verification-system worktree
├── wt-backend/             # feature/backend-diversity worktree
├── wt-improvement/         # feature/self-improvement worktree
├── wt-swarm/               # feature/swarm-orchestration worktree
├── wt-visualization/        # feature/visualization-interface worktree
└── wt-testing/             # feature/testing-infrastructure worktree
```

### Worktree Creation Commands

```bash
# Create worktrees directory
mkdir -p worktrees

# Create worktrees for each branch
git worktree add worktrees/wt-develop develop
git worktree add worktrees/wt-redux feature/redux-state-management
git worktree add worktrees/wt-agents feature/agent-framework
git worktree add worktrees/wt-messaging feature/messaging-system
git worktree add worktrees/wt-tools feature/dynamic-tools
git worktree add worktrees/wt-verification feature/verification-system
git worktree add worktrees/wt-backend feature/backend-diversity
git worktree add worktrees/wt-improvement feature/self-improvement
git worktree add worktrees/wt-swarm feature/swarm-orchestration
git worktree add worktrees/wt-visualization feature/visualization-interface
git worktree add worktrees/wt-testing feature/testing-infrastructure

# List all worktrees
git worktree list
```

### Worktree Management

```bash
# Remove a worktree when done
git worktree remove worktrees/wt-redux

# Remove all worktrees at once
for wt in worktrees/wt-*; do
    git worktree remove "$wt"
done
```

## Testing Strategy

### Unit Testing (Per Branch)
- Each branch runs its own unit tests
- Use worktrees to run tests without merging
- **Command**: `cd worktrees/wt-redux && pytest tests/redux/`

### Integration Testing (After Merging)
- Run integration tests on develop branch
- Test interactions between features
- **Command**: `cd worktrees/wt-develop && pytest tests/integration/`

### End-to-End Testing (On main)
- Run full test suite on main before release
- Test entire system
- **Command**: `pytest tests/`

## Merge Order Recommendation

### Safe Merge Order (Following Dependency Levels)

1. **Merge Level 0 to develop** (can be done in any order):
   ```bash
   git checkout develop
   git merge feature/redux-state-management
   git merge feature/agent-framework
   git merge feature/messaging-system
   git merge feature/dynamic-tools
   git merge feature/backend-diversity
   git merge feature/testing-infrastructure
   ```

2. **Merge Level 1 to develop** (after agent-framework):
   ```bash
   git merge feature/verification-system
   ```

3. **Merge Level 2 to develop** (after dependencies are stable):
   ```bash
   git merge feature/self-improvement
   git merge feature/swarm-orchestration
   git merge feature/visualization-interface
   ```

4. **Merge develop to main**:
   ```bash
   git checkout main
   git merge develop
   ```

## Branch Purposes for AI Agents

### For AI Agent Reference

When AI agents need to understand which branch to use for specific tasks:

```python
BRANCH_PURPOSES = {
    "main": {
        "purpose": "Production-ready code",
        "when_to_use": "When deploying to production or creating releases",
        "read_only": True
    },
    "develop": {
        "purpose": "Integration branch",
        "when_to_use": "When testing integration of multiple features",
        "read_only": False
    },
    "feature/redux-state-management": {
        "purpose": "Redux store with slices for agents, tasks, messages, system, tools, improvements",
        "when_to_use": "When working on state management, creating Redux slices, or modifying store",
        "dependencies": [],
        "key_files": ["rlm/redux/slices/*.py", "rlm/redux/middleware/*.py"]
    },
    "feature/agent-framework": {
        "purpose": "Base agent classes (BaseAgent, TaskProcessingAgent, etc.)",
        "when_to_use": "When creating agents, modifying agent behavior, or implementing new agent types",
        "dependencies": [],
        "key_files": ["agents/*.py", "rlm/agents/*.py"]
    },
    "feature/messaging-system": {
        "purpose": "Message broker, message types, communication protocols",
        "when_to_use": "When working on agent communication, message routing, or implementing messaging patterns",
        "dependencies": [],
        "key_files": ["messaging/*.py", "rlm/messaging/*.py"]
    },
    "feature/dynamic-tools": {
        "purpose": "Tool registry, dynamic tool creation, approval workflow",
        "when_to_use": "When creating tools, managing tool registry, or implementing tool approval",
        "dependencies": [],
        "key_files": ["tools/*.py", "rlm/tools/*.py"]
    },
    "feature/verification-system": {
        "purpose": "Lean 4 axiomatic seed integration for verification",
        "when_to_use": "When working on code verification, Lean integration, or proof checking",
        "dependencies": ["feature/agent-framework"],
        "key_files": ["rlm/agents/prompts/verification_prompts.py", "rlm/agents/verification_agent_factory.py"]
    },
    "feature/backend-diversity": {
        "purpose": "Multi-backend routing, environment selection",
        "when_to_use": "When adding new AI backends, implementing routing logic, or optimizing backend selection",
        "dependencies": [],
        "key_files": ["rlm/routing/*.py", "rlm/clients/*.py"]
    },
    "feature/self-improvement": {
        "purpose": "Improvement contribution system with approval and application",
        "when_to_use": "When working on self-improvement, creating improvement proposals, or managing improvement workflows",
        "dependencies": ["feature/dynamic-tools", "feature/messaging-system"],
        "key_files": ["improvements/*.py", "rlm/improvements/*.py"]
    },
    "feature/swarm-orchestration": {
        "purpose": "Main swarm instance with continuous spawning and coordination",
        "when_to_use": "When working on swarm coordination, agent spawning, or orchestration logic",
        "dependencies": ["feature/redux-state-management", "feature/agent-framework", "feature/messaging-system"],
        "key_files": ["rlm/core/swarm_rlm.py", "rlm/swarm/*.py"]
    },
    "feature/visualization-interface": {
        "purpose": "Real-time monitoring UI with agent grid, communication log",
        "when_to_use": "When working on visualization, monitoring dashboards, or user interface",
        "dependencies": ["feature/redux-state-management", "feature/messaging-system"],
        "key_files": ["ui/*.py", "visualization/*.py", "rlm/ui/*.py"]
    },
    "feature/testing-infrastructure": {
        "purpose": "Test framework, CI/CD workflows",
        "when_to_use": "When writing tests, setting up CI/CD, or improving test infrastructure",
        "dependencies": [],
        "key_files": ["tests/*.py", ".github/workflows/*.yml"]
    }
}
```

## Context Optimization Recommendations

### For AI Agents Working Across Branches

1. **Use `symbols.md` First**: Always check `symbols.md` before reading files
   - Provides quick overview of all code across branches
   - Avoids unnecessary file reads
   - Shows relationships between branches

2. **Use Worktrees for Testing**: Never merge just to test
   - Create worktrees for branches you need to test
   - Run tests in worktree without affecting main branch
   - Clean up worktrees after testing

3. **Use `apply_diff` for Changes**: Never regenerate entire files
   - Use skeletal rules to identify what to change
   - Use `apply_diff` to make targeted changes
   - Minimizes context usage and improves efficiency

4. **Branch Selection Heuristics**:
   - If modifying Redux: use `feature/redux-state-management`
   - If creating agents: use `feature/agent-framework`
   - If working on messaging: use `feature/messaging-system`
   - If creating tools: use `feature/dynamic-tools`
   - If working on verification: use `feature/verification-system`
   - If adding backends: use `feature/backend-diversity`
   - If working on improvements: use `feature/self-improvement`
   - If working on orchestration: use `feature/swarm-orchestration`
   - If working on UI: use `feature/visualization-interface`
   - If writing tests: use `feature/testing-infrastructure`

5. **Dependency-Aware Branch Selection**:
   - Always check if dependencies are met before starting a task
   - If dependencies aren't met, start with dependency branches first
   - Use dependency levels to plan task order

## Summary

This analysis provides:
- ✅ Complete dependency graph for all 14 branches
- ✅ Development strategy organized by dependency levels
- ✅ Worktree setup and management guide
- ✅ Testing strategy for parallel development
- ✅ Safe merge order recommendations
- ✅ Branch purpose mapping for AI agents
- ✅ Context optimization recommendations

Use this document to plan development, manage dependencies, and optimize AI agent workflows across branches.
