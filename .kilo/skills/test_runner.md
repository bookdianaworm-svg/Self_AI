# Test Runner Skill

## Purpose
The test_runner skill enables efficient testing across multiple git branches using worktrees, eliminating the need to merge or switch branches to run tests. It provides tools for:
- Running tests in branch-specific worktrees
- Parallel testing across multiple branches
- Test result aggregation and comparison
- Test coverage analysis across branches

## Core Principles

### 1. Never Merge to Test
- Always use worktrees to test branches independently
- Never merge a branch just to run tests
- Keep branches isolated until ready for integration

### 2. Parallel Testing
- Run tests on multiple branches simultaneously
- Leverage worktrees for concurrent execution
- Aggregate results for easy comparison

### 3. Minimal Overhead
- Create worktrees on-demand, cache when possible
- Clean up worktrees after testing
- Use selective test execution when appropriate

## Available Tools

### 1. `create_worktree`
Create a git worktree for a specific branch.

**Usage**: `create_worktree(branch: str, worktree_name: str = None) -> dict`

**Parameters**:
- `branch`: Name of the branch to create worktree for
- `worktree_name`: Optional custom name for worktree (default: auto-generated)

**Returns**: Dictionary with:
- `worktree_path`: Path to created worktree
- `status`: 'created' or 'already_exists'
- `branch`: Branch name

**Example**:
```python
result = create_worktree("feature/agent-framework")
# {
#     'worktree_path': 'worktrees/wt-feature-agent-framework',
#     'status': 'created',
#     'branch': 'feature/agent-framework'
# }
```

### 2. `list_worktrees`
List all existing worktrees.

**Usage**: `list_worktrees() -> list`

**Returns**: List of worktree information dictionaries

**Example**:
```python
worktrees = list_worktrees()
# [
#     {'branch': 'develop', 'path': 'worktrees/wt-develop', 'commit': 'abc123'},
#     {'branch': 'feature/agent-framework', 'path': 'worktrees/wt-agents', 'commit': 'def456'}
# ]
```

### 3. `remove_worktree`
Remove a git worktree.

**Usage**: `remove_worktree(worktree_name_or_path: str) -> dict`

**Parameters**:
- `worktree_name_or_path`: Name or path of worktree to remove

**Returns**: Dictionary with:
- `status`: 'removed' or 'not_found'
- `path`: Path to removed worktree

**Example**:
```python
result = remove_worktree("wt-agents")
# {
#     'status': 'removed',
#     'path': 'worktrees/wt-agents'
# }
```

### 4. `run_tests_in_worktree`
Run tests in a specific worktree.

**Usage**: `run_tests_in_worktree(worktree_name: str, test_path: str = None, args: str = "") -> dict`

**Parameters**:
- `worktree_name`: Name of the worktree
- `test_path`: Optional path to specific test file or directory (default: all tests)
- `args`: Additional pytest arguments (e.g., "-v", "-k test_name")

**Returns**: Dictionary with:
- `exit_code`: Test exit code (0 = success)
- `output`: Test output (stdout/stderr)
- `passed`: Number of passed tests
- `failed`: Number of failed tests
- `skipped`: Number of skipped tests
- `duration`: Test execution time in seconds
- `status`: 'success', 'failure', or 'error'

**Example**:
```python
# Run all tests in worktree
result = run_tests_in_worktree("wt-agents")
# {
#     'exit_code': 0,
#     'output': '=== test session starts ===...',
#     'passed': 42,
#     'failed': 0,
#     'skipped': 3,
#     'duration': 15.23,
#     'status': 'success'
# }

# Run specific test file
result = run_tests_in_worktree("wt-agents", "tests/agents/test_base_agent.py")

# Run tests with pattern
result = run_tests_in_worktree("wt-agents", args="-v -k test_spawn")
```

### 5. `run_tests_in_branch`
Convenience function to create worktree and run tests in one step.

**Usage**: `run_tests_in_branch(branch: str, test_path: str = None, args: str = "", keep_worktree: bool = False) -> dict`

**Parameters**:
- `branch`: Name of the branch to test
- `test_path`: Optional path to specific test file or directory
- `args`: Additional pytest arguments
- `keep_worktree`: If False, removes worktree after testing (default: False)

**Returns**: Same as `run_tests_in_worktree` plus:
- `branch`: Branch name
- `worktree_path`: Path to worktree (if kept)

**Example**:
```python
# Test branch and cleanup
result = run_tests_in_branch("feature/agent-framework")

# Test branch and keep worktree for further work
result = run_tests_in_branch("feature/agent-framework", keep_worktree=True)

# Run specific tests
result = run_tests_in_branch("feature/agent-framework", "tests/agents/", "-v")
```

### 6. `run_parallel_tests`
Run tests on multiple branches in parallel.

**Usage**: `run_parallel_tests(branches: list, test_path: str = None, args: str = "", max_workers: int = 4) -> dict`

**Parameters**:
- `branches`: List of branch names to test
- `test_path`: Optional path to specific test file or directory
- `args`: Additional pytest arguments
- `max_workers`: Maximum number of parallel test runs (default: 4)

**Returns**: Dictionary with:
- `results`: Dictionary mapping branch names to test results
- `summary`: Overall test summary
  - `total_branches`: Number of branches tested
  - `successful_branches`: Number of branches with all tests passing
  - `failed_branches`: Number of branches with failed tests
  - `total_tests`: Total number of tests across all branches
  - `total_passed`: Total number of passed tests
  - `total_failed`: Total number of failed tests
- `duration`: Total execution time

**Example**:
```python
results = run_parallel_tests([
    "feature/agent-framework",
    "feature/messaging-system",
    "feature/dynamic-tools"
])

# {
#     'results': {
#         'feature/agent-framework': {'passed': 42, 'failed': 0, ...},
#         'feature/messaging-system': {'passed': 38, 'failed': 1, ...},
#         'feature/dynamic-tools': {'passed': 25, 'failed': 0, ...}
#     },
#     'summary': {
#         'total_branches': 3,
#         'successful_branches': 2,
#         'failed_branches': 1,
#         'total_tests': 105,
#         'total_passed': 105,
#         'total_failed': 1
#     },
#     'duration': 23.45
# }
```

### 7. `compare_test_results`
Compare test results between branches.

**Usage**: `compare_test_results(branch1: str, branch2: str, test_path: str = None) -> dict`

**Parameters**:
- `branch1`: First branch to compare
- `branch2`: Second branch to compare
- `test_path`: Optional path to specific test file or directory

**Returns**: Dictionary with:
- `branch1_results`: Test results for branch1
- `branch2_results`: Test results for branch2
- `comparison`: Comparison metrics
  - `tests_only_in_branch1`: List of tests only in branch1
  - `tests_only_in_branch2`: List of tests only in branch2
  - `tests_with_different_outcome`: List of tests with different pass/fail status
  - `new_failures`: Tests that fail in branch1 but pass in branch2
  - `fixed_failures`: Tests that fail in branch2 but pass in branch1

**Example**:
```python
comparison = compare_test_results("develop", "feature/agent-framework")
# {
#     'branch1_results': {'passed': 100, 'failed': 5, ...},
#     'branch2_results': {'passed': 105, 'failed': 0, ...},
#     'comparison': {
#         'tests_only_in_branch1': [],
#         'tests_only_in_branch2': [
#             'tests/agents/test_task_agent.py::test_spawn_from_repl'
#         ],
#         'tests_with_different_outcome': [
#             'tests/agents/test_base_agent.py::test_execute_task'
#         ],
#         'new_failures': [],
#         'fixed_failures': ['tests/agents/test_base_agent.py::test_execute_task']
#     }
# }
```

### 8. `get_test_coverage`
Get test coverage for a specific branch or worktree.

**Usage**: `get_test_coverage(branch: str = None, worktree_name: str = None, test_path: str = None) -> dict`

**Parameters**:
- `branch`: Branch to get coverage for (optional if worktree_name provided)
- `worktree_name`: Worktree to get coverage for (optional if branch provided)
- `test_path`: Optional path to specific test file or directory

**Returns**: Dictionary with:
- `branch`: Branch name
- `overall_coverage`: Overall coverage percentage
- `line_coverage`: Line coverage percentage
- `branch_coverage`: Branch coverage percentage
- `files_coverage`: Coverage by file
  - `file_path`: Coverage for specific file
- `uncovered_lines`: List of uncovered lines
- `covered_lines`: List of covered lines

**Example**:
```python
coverage = get_test_coverage("feature/agent-framework")
# {
#     'branch': 'feature/agent-framework',
#     'overall_coverage': 87.5,
#     'line_coverage': 87.5,
#     'branch_coverage': 82.3,
#     'files_coverage': {
#         'agents/base_agent.py': 92.1,
#         'agents/task_agent.py': 85.4
#     },
#     'uncovered_lines': [...],
#     'covered_lines': [...]
# }
```

### 9. `find_failing_tests`
Find failing tests across multiple branches.

**Usage**: `find_failing_tests(branches: list = None) -> dict`

**Parameters**:
- `branches`: List of branches to check (default: all feature branches)

**Returns**: Dictionary mapping branch names to lists of failing tests

**Example**:
```python
failing = find_failing_tests([
    "feature/agent-framework",
    "feature/messaging-system"
])
# {
#     'feature/agent-framework': [
#         'tests/agents/test_base_agent.py::test_execute_task',
#         'tests/agents/test_task_agent.py::test_spawn'
#     ],
#     'feature/messaging-system': []
# }
```

### 10. `cleanup_worktrees`
Remove all or specific worktrees.

**Usage**: `cleanup_worktrees(worktree_names: list = None, keep_develop: bool = True) -> dict`

**Parameters**:
- `worktree_names`: List of specific worktree names to remove (default: all)
- `keep_develop`: If True, keeps the develop worktree (default: True)

**Returns**: Dictionary with:
- `removed`: List of removed worktrees
- `kept`: List of kept worktrees
- `errors`: List of errors during removal

**Example**:
```python
# Remove all worktrees except develop
result = cleanup_worktrees()
# {
#     'removed': ['wt-agents', 'wt-messaging', 'wt-tools', ...],
#     'kept': ['wt-develop'],
#     'errors': []
# }

# Remove specific worktrees
result = cleanup_worktrees(['wt-agents', 'wt-messaging'])
```

## Usage Patterns

### Pattern 1: Single Branch Testing

Test a single branch without merging:

```python
# Test a specific branch
result = run_tests_in_branch("feature/agent-framework")

# Check if tests passed
if result['status'] == 'success':
    print("All tests passed!")
else:
    print(f"Tests failed: {result['output']}")
```

### Pattern 2: Parallel Branch Testing

Test multiple branches simultaneously:

```python
# Test all feature branches in parallel
branches = [
    "feature/agent-framework",
    "feature/messaging-system",
    "feature/dynamic-tools",
    "feature/backend-diversity"
]

results = run_parallel_tests(branches, max_workers=4)

# Check which branches have failing tests
for branch, result in results['results'].items():
    if result['failed'] > 0:
        print(f"Branch {branch} has {result['failed']} failing tests")
```

### Pattern 3: Comparison Testing

Compare test results between branches:

```python
# Compare develop with a feature branch
comparison = compare_test_results("develop", "feature/agent-framework")

# Check for regressions
if comparison['comparison']['new_failures']:
    print("New test failures introduced:")
    for test in comparison['comparison']['new_failures']:
        print(f"  - {test}")
```

### Pattern 4: Targeted Testing

Run only specific tests:

```python
# Run tests related to agent spawning
result = run_tests_in_branch(
    "feature/agent-framework",
    args="-k spawn"
)

# Run tests in specific file
result = run_tests_in_branch(
    "feature/agent-framework",
    "tests/agents/test_base_agent.py"
)
```

### Pattern 5: Integration Preparation

Before merging, run tests on integration branch:

```python
# Test develop branch to ensure integration stability
result = run_tests_in_branch("develop", keep_worktree=True)

if result['status'] == 'success':
    print("Develop branch is stable, ready for merge to main")
else:
    print("Develop branch has failing tests, fix before merging")
```

## Integration with Other Skills

### With branch_scout Skill
```python
# Find all test files in a branch
test_files = list_files_in_branch("feature/agent-framework", "tests/**/*.py")

# Run only specific test files
for test_file in test_files:
    result = run_tests_in_branch("feature/agent-framework", test_file)
```

### With branch_manager Workflow
```python
# When working on a task, run tests on dependent branches
task = "Implement agent spawning"

# Find dependent branches
deps = get_branch_dependencies("feature/swarm-orchestration")

# Run tests on all dependent branches
results = run_parallel_tests(deps)
```

## Best Practices

1. **Always test in worktrees** - Never merge just to test
2. **Use parallel testing** - Test multiple branches simultaneously
3. **Clean up worktrees** - Remove worktrees after testing to save disk space
4. **Compare with develop** - Always compare feature branch results with develop
5. **Keep develop worktree** - Cache develop worktree for frequent testing
6. **Use selective testing** - Run specific tests when appropriate
7. **Check coverage** - Ensure test coverage is adequate
8. **Monitor regressions** - Compare results to catch breaking changes

## Test Organization

### Recommended Test Structure

```
tests/
├── unit/                    # Unit tests
│   ├── agents/             # Agent framework tests
│   ├── messaging/          # Messaging system tests
│   ├── redux/             # Redux state management tests
│   ├── tools/              # Tool registry tests
│   └── verification/       # Verification system tests
├── integration/            # Integration tests
│   ├── swarm/             # Swarm orchestration tests
│   ├── ui/                # UI integration tests
│   └── backend/           # Backend diversity tests
├── e2e/                   # End-to-end tests
│   ├── full_swarm/        # Full swarm system tests
│   └── user_workflows/     # User workflow tests
└── conftest.py            # Pytest configuration
```

### Branch-Specific Tests

Each feature branch should have its own test directory:

```
tests/feature/
├── agent_framework/       # Tests for agent-framework branch
├── messaging_system/      # Tests for messaging-system branch
├── dynamic_tools/         # Tests for dynamic-tools branch
├── verification_system/    # Tests for verification-system branch
├── backend_diversity/      # Tests for backend-diversity branch
├── self_improvement/      # Tests for self-improvement branch
├── swarm_orchestration/   # Tests for swarm-orchestration branch
├── visualization_interface/# Tests for visualization-interface branch
└── testing_infrastructure/# Tests for testing-infrastructure branch
```

## Performance Considerations

- **create_worktree**: Medium - creates a new git worktree (seconds)
- **run_tests_in_worktree**: Varies - depends on test suite (seconds to minutes)
- **run_parallel_tests**: Fast to Medium - runs tests in parallel
- **compare_test_results**: Fast - compares results (milliseconds)
- **cleanup_worktrees**: Fast - removes worktrees (seconds)

For best performance:
- Use parallel testing for multiple branches
- Cache develop worktree
- Use selective testing when appropriate
- Clean up unused worktrees

## Error Handling

All tools handle errors gracefully:
- Branch not found: Returns error in result dictionary
- Worktree creation failed: Returns error with details
- Test execution failed: Returns error output and exit code
- File not found: Returns appropriate error message

## Example Workflows

### Workflow 1: Pre-Merge Testing

Before merging a feature branch to develop:

```python
# Step 1: Run tests on feature branch
feature_result = run_tests_in_branch("feature/agent-framework")

if feature_result['status'] != 'success':
    print("Feature branch has failing tests, fix before merging")
    return

# Step 2: Create develop worktree (cached)
run_tests_in_branch("develop", keep_worktree=True)

# Step 3: Compare results
comparison = compare_test_results("develop", "feature/agent-framework")

if comparison['comparison']['new_failures']:
    print("Feature branch introduces new failures:")
    for test in comparison['comparison']['new_failures']:
        print(f"  - {test}")
else:
    print("Feature branch ready for merge")
```

### Workflow 2: Daily CI Testing

Run daily tests on all feature branches:

```python
# Get all feature branches
branches = list_branches()
feature_branches = [b for b in branches if b.startswith('feature/')]

# Run parallel tests
results = run_parallel_tests(feature_branches)

# Generate report
for branch, result in results['results'].items():
    status = "✓ PASS" if result['status'] == 'success' else "✗ FAIL"
    print(f"{status} {branch}: {result['passed']}/{result['passed']+result['failed']} tests passed")

# Cleanup
cleanup_worktrees(keep_develop=True)
```

### Workflow 3: Dependency Testing

When working on a feature with dependencies:

```python
# Find dependencies
deps = get_cross_branch_dependencies(symbol_name="MessageBroker")

# Run tests on dependent branches
results = run_parallel_tests(deps['dependent_branches'])

# Check if dependencies are stable
all_passing = all(r['status'] == 'success' for r in results['results'].values())

if all_passing:
    print("All dependent branches are stable")
else:
    print("Some dependent branches have failing tests")
```

## Summary

The test_runner skill enables efficient cross-branch testing:
- ✅ Test branches without merging or switching
- ✅ Parallel testing for speed
- ✅ Compare results across branches
- ✅ Coverage analysis
- ✅ Identify regressions
- ✅ Minimal overhead with worktree management

Use test_runner whenever you need to:
- Test a feature branch before merging
- Compare test results between branches
- Run tests on multiple branches in parallel
- Check for test regressions
- Analyze test coverage
- Prepare branches for integration
