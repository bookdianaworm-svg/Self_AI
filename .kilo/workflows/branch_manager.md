# Branch Manager Workflow

## Purpose
The branch_manager workflow orchestrates cross-branch operations for efficient development. It coordinates the use of worktrees, manages branch transitions, and ensures proper sequencing of tasks across multiple branches.

## Core Principles

### 1. Context Optimization
- Use skeletal information before full reads
- Minimize file reads by understanding structure first
- Cache information to reduce redundant operations

### 2. Branch Isolation
- Work on branches in isolation using worktrees
- Never merge just to test or verify
- Keep branches independent until ready for integration

### 3. Dependency Awareness
- Always check dependencies before starting work
- Follow dependency levels for task sequencing
- Coordinate dependent branches to avoid conflicts

### 4. Apply-Diff Optimization
- Use apply_diff for targeted changes instead of regenerating files
- Minimize context usage by only changing what's necessary
- Maintain code style and structure

## Workflow States

### State 1: Discovery
- Understand the task requirements
- Identify relevant branches using branch_scout
- Check dependencies
- Select appropriate branch(es) to work in

### State 2: Preparation
- Create worktrees for target branches
- Get skeletal structure of files to modify
- Understand cross-branch implications

### State 3: Implementation
- Make targeted changes using apply_diff
- Use branch_scout to verify changes don't break other branches
- Run tests in worktrees using test_runner

### State 4: Verification
- Run tests on modified branches
- Compare results with develop
- Check cross-branch dependencies
- Ensure no regressions

### State 5: Integration
- Create pull requests
- Request reviews
- Merge to develop when approved
- Update develop worktree

## Decision Trees

### Decision 1: Which Branch to Work In?

```
START
  │
  ├─ Task involves Redux/state management?
  │   └─ YES → feature/redux-state-management
  │   └─ NO  → Continue
  │
  ├─ Task involves creating/modifying agents?
  │   └─ YES → feature/agent-framework
  │   └─ NO  → Continue
  │
  ├─ Task involves messaging/communication?
  │   └─ YES → feature/messaging-system
  │   └─ NO  → Continue
  │
  ├─ Task involves tools/registry?
  │   └─ YES → feature/dynamic-tools
  │   └─ NO  → Continue
  │
  ├─ Task involves verification/proofs?
  │   └─ YES → feature/verification-system
  │   └─ NO  → Continue
  │
  ├─ Task involves multiple backends?
  │   └─ YES → feature/backend-diversity
  │   └─ NO  → Continue
  │
  ├─ Task involves self-improvement?
  │   └─ YES → feature/self-improvement
  │   └─ NO  → Continue
  │
  ├─ Task involves swarm orchestration?
  │   └─ YES → feature/swarm-orchestration
  │   └─ NO  → Continue
  │
  ├─ Task involves visualization/UI?
  │   └─ YES → feature/visualization-interface
  │   └─ NO  → Continue
  │
  └─ Task involves testing infrastructure?
      └─ YES → feature/testing-infrastructure
```

### Decision 2: Do Dependencies Exist?

```
START: Have identified target branch
  │
  ├─ Check CROSS_BRANCH_DEPENDENCIES.md
  │
  ├─ Does branch have dependencies?
  │   ├─ YES → Are dependencies satisfied?
  │   │   ├─ YES → Proceed with implementation
  │   │   └─ NO  → Work on dependencies first
  │   └─ NO  → Proceed with implementation
```

### Decision 3: Should I Create Multiple Worktrees?

```
START: Ready to implement
  │
  ├─ Does task affect multiple branches?
  │   ├─ YES → Create worktree for each affected branch
  │   │         Use run_parallel_tests for verification
  │   └─ NO  → Create single worktree for target branch
  │
  ├─ Do dependent branches need testing?
  │   ├─ YES → Create worktrees for dependencies too
  │   └─ NO  → Single worktree is sufficient
```

## Workflow Commands

### Command 1: Analyze Task
Analyze a task and determine which branch(es) to work in.

**Usage**: `analyze_task(task_description: str) -> dict`

**Returns**: Dictionary with:
- `target_branch`: Primary branch to work in
- `affected_branches`: List of all branches that might be affected
- `dependencies`: List of dependencies that must be satisfied first
- `files_to_modify`: List of files likely to be modified
- `cross_branch_implications`: Potential cross-branch effects

**Example**:
```python
result = analyze_task("Implement tool approval workflow")
# {
#     'target_branch': 'feature/dynamic-tools',
#     'affected_branches': ['feature/dynamic-tools'],
#     'dependencies': [],
#     'files_to_modify': ['tools/tool_registry.py', 'tools/approval.py'],
#     'cross_branch_implications': []
# }
```

### Command 2: Prepare Worktree
Create and prepare a worktree for a branch.

**Usage**: `prepare_worktree(branch: str) -> dict`

**Returns**: Dictionary with:
- `worktree_path`: Path to worktree
- `status`: 'ready' or 'error'
- `files_modified`: List of files modified in this branch (vs main)

**Example**:
```python
result = prepare_worktree("feature/agent-framework")
# {
#     'worktree_path': 'worktrees/wt-agents',
#     'status': 'ready',
#     'files_modified': ['agents/base_agent.py', 'agents/task_agent.py']
# }
```

### Command 3: Implement Change
Implement a change using apply_diff.

**Usage**: `implement_change(file_path: str, changes: list, worktree_path: str = None) -> dict`

**Parameters**:
- `file_path`: Path to file to modify
- `changes`: List of changes to apply (old_string, new_string pairs)
- `worktree_path`: Optional worktree path (default: current directory)

**Returns**: Dictionary with:
- `status`: 'success' or 'error'
- `changes_applied`: Number of changes applied
- `file_path`: Path to modified file
- `diff`: Unified diff of changes

**Example**:
```python
result = implement_change(
    "agents/base_agent.py",
    [
        {
            "old_string": "def execute_task(self, task_description: str):",
            "new_string": "async def execute_task(self, task_description: str):"
        }
    ],
    "worktrees/wt-agents"
)
```

### Command 4: Verify Changes
Verify changes don't break tests or other branches.

**Usage**: `verify_changes(branch: str, affected_branches: list = None) -> dict`

**Returns**: Dictionary with:
- `target_branch_tests`: Test results for target branch
- `dependent_branch_tests`: Test results for dependent branches
- `comparison`: Comparison with develop
- `status': 'verified', 'needs_fixes', or 'failed'

**Example**:
```python
result = verify_changes("feature/agent-framework")
# {
#     'target_branch_tests': {'passed': 42, 'failed': 0, ...},
#     'dependent_branch_tests': [],
#     'comparison': {'new_failures': [], 'fixed_failures': [...]},
#     'status': 'verified'
# }
```

### Command 5: Create Pull Request
Create a pull request for the changes.

**Usage**: `create_pull_request(source_branch: str, target_branch: str = "develop", description: str = None) -> dict`

**Returns**: Dictionary with:
- `pr_url`: URL to pull request
- `status': 'created' or 'error'
- `reviewers`: List of reviewers assigned

**Example**:
```python
result = create_pull_request(
    "feature/agent-framework",
    "develop",
    "Implement async task execution in BaseAgent"
)
```

## Workflows

### Workflow 1: Simple Feature Implementation

For tasks that affect a single branch with no dependencies:

```
1. analyze_task("Implement task filtering in agent spawning")
   → Returns: target_branch = 'feature/agent-framework'

2. prepare_worktree('feature/agent-framework')
   → Creates worktree at worktrees/wt-agents

3. Use branch_scout.list_code_definitions() to understand structure
   → Gets skeletal info of agents/base_agent.py

4. Use branch_scout.find_symbol_definition() to locate relevant code
   → Finds spawn_agent() method

5. Use apply_diff to implement changes
   → Makes targeted changes to spawn_agent()

6. verify_changes('feature/agent-framework')
   → Runs tests in worktree

7. If tests pass, create_pull_request()
   → Creates PR to develop

8. Cleanup worktree
   → remove_worktree('wt-agents')
```

### Workflow 2: Multi-Branch Task

For tasks that affect multiple branches:

```
1. analyze_task("Add message timestamp tracking")
   → Returns: target_branch = 'feature/messaging-system'
   → affected_branches = ['feature/swarm-orchestration', 'feature/visualization-interface']

2. prepare_worktrees(['feature/messaging-system', 'feature/swarm-orchestration', 'feature/visualization-interface'])
   → Creates 3 worktrees

3. Implement in target branch (messaging-system)
   → Add timestamp to Message class

4. Use branch_scout to find usages in other branches
   → search_symbol_in_branches('Message')

5. Update affected branches
   → Use apply_diff in each worktree

6. verify_changes() with parallel testing
   → run_parallel_tests() on all 3 branches

7. Compare with develop
   → compare_test_results()

8. If all pass, create PRs
   → One PR per affected branch (in dependency order)

9. Cleanup worktrees
   → cleanup_worktrees()
```

### Workflow 3: Dependency-First Implementation

For tasks where dependencies must be implemented first:

```
1. analyze_task("Implement self-improvement system")
   → Returns: target_branch = 'feature/self-improvement'
   → dependencies = ['feature/dynamic-tools', 'feature/messaging-system']

2. Check if dependencies are ready
   → find_symbol_definition('ToolRegistry') → exists
   → find_symbol_definition('MessageBroker') → exists
   → Dependencies are satisfied

3. prepare_worktree('feature/self-improvement')

4. Implement changes

5. verify_changes() with dependent branches
   → Also test feature/dynamic-tools and feature/messaging-system
   → Ensure improvements don't break existing tools or messaging

6. If all tests pass, create PR

7. Cleanup

   (ALTERNATIVE: If dependencies not satisfied)

2. Dependencies not ready
   → Must work on dependencies first

3. Start with feature/dynamic-tools
   → Follow Simple Feature Implementation workflow

4. Then feature/messaging-system
   → Follow Simple Feature Implementation workflow

5. Finally feature/self-improvement
   → Now dependencies are satisfied
```

## Integration with Skills

### With branch_scout

```python
# Always use branch_scout before implementing

# Step 1: Find where to work
task = "Add tool validation"
result = analyze_task(task)

# Step 2: Get skeletal structure
defs = list_code_definitions(
    "tools/tool_registry.py",
    result['target_branch']
)

# Step 3: Find specific symbol
location = find_symbol_definition("ToolRegistry")

# Step 4: Understand dependencies
deps = get_cross_branch_dependencies(symbol_name="ToolRegistry")
```

### With test_runner

```python
# Always use test_runner after implementing

# Step 1: Run tests in worktree
result = run_tests_in_worktree(
    "wt-tools",
    "tests/tools/"
)

# Step 2: Compare with develop
comparison = compare_test_results(
    "develop",
    "feature/dynamic-tools"
)

# Step 3: Run parallel tests on dependencies
results = run_parallel_tests(
    deps['dependent_branches']
)
```

### With apply_diff

```python
# Always use apply_diff for implementation

# Step 1: Understand what to change
defs = list_code_definitions(file_path, branch)

# Step 2: Apply targeted changes
result = implement_change(
    file_path,
    [
        {
            "old_string": "class ToolRegistry:",
            "new_string": "class ToolRegistry:\n    def validate_tool(self, tool):"
        }
    ],
    worktree_path
)
```

## Best Practices

1. **Always analyze task first** - Understand scope and dependencies
2. **Use branch_scout before reading** - Get skeletal information first
3. **Work in worktrees** - Never merge just to test
4. **Test in isolation** - Run tests in worktrees, not on main branch
5. **Verify cross-branch implications** - Check if changes affect other branches
6. **Use apply_diff** - Make targeted changes, don't regenerate files
7. **Follow dependency order** - Implement dependencies before dependents
8. **Compare with develop** - Always compare test results with develop
9. **Cleanup worktrees** - Remove worktrees after use
10. **Create PRs in dependency order** - Merge dependencies first

## Context Optimization Checklist

Before implementing any change:

- [ ] Analyzed task to understand scope
- [ ] Checked CROSS_BRANCH_DEPENDENCIES.md for branch dependencies
- [ ] Used branch_scout to find relevant branches
- [ ] Used list_code_definitions to understand structure
- [ ] Used find_symbol_definition to locate code
- [ ] Checked cross_branch_dependencies for implications
- [ ] Created worktrees for affected branches
- [ ] Understood which files will be modified
- [ ] Prepared targeted changes using apply_diff

After implementing changes:

- [ ] Ran tests in worktree(s)
- [ ] Compared results with develop
- [ ] Tested dependent branches
- [ ] Verified no regressions
- [ ] Cleaned up worktrees
- [ ] Created pull request(s)

## Error Handling

### Common Scenarios

**Scenario 1: Worktree already exists**
```python
# Check if worktree exists first
worktrees = list_worktrees()
if not any(wt['branch'] == branch for wt in worktrees):
    create_worktree(branch)
else:
    # Use existing worktree
    pass
```

**Scenario 2: Dependency not satisfied**
```python
# Check dependencies
deps = get_cross_branch_dependencies(symbol_name="ToolRegistry")
if deps['missing']:
    print(f"Dependencies not satisfied: {deps['missing']}")
    # Work on dependencies first
    return
```

**Scenario 3: Tests fail after changes**
```python
# Run tests
result = run_tests_in_worktree("wt-agents")
if result['status'] != 'success':
    print(f"Tests failed: {result['failed']} failures")
    # Fix issues before proceeding
    return
```

**Scenario 4: Cross-branch conflict**
```python
# Check for conflicts
conflicts = compare_files_between_branches(
    file_path,
    ['feature/agent-framework', 'feature/swarm-orchestration']
)
if conflicts['different']:
    print(f"File differs in multiple branches, coordinate changes")
    # Discuss with team before proceeding
    return
```

## Summary

The branch_manager workflow provides:
- ✅ Task analysis and branch selection
- ✅ Dependency-aware implementation
- ✅ Worktree management
- ✅ apply_diff integration
- ✅ Cross-branch verification
- ✅ Optimized context usage
- ✅ Safe integration process

Use branch_manager whenever you need to:
- Implement a new feature
- Fix a bug across multiple branches
- Coordinate changes between branches
- Prepare branches for integration
- Ensure safe cross-branch development
