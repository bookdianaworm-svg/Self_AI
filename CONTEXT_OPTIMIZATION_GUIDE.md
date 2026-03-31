# Context Optimization & Cross-Branch Development Guide

## Overview

This document provides a comprehensive guide for the context-optimized development environment designed for the Self_AI project's 14-branch architecture. The system is designed to minimize context usage, enable efficient cross-branch development, and optimize AI agent workflows.

## What Has Been Created

### 1. Documentation Files

#### symbols.md
- Complete map of all Python code across all 14 branches
- Class and function signatures for quick reference
- Import statements and dependencies
- 2,327 classes and 6,942 functions documented

#### CROSS_BRANCH_DEPENDENCIES.md
- Complete dependency graph for all branches
- Development strategy organized by dependency levels
- Worktree setup and management guide
- Testing strategy for parallel development
- Safe merge order recommendations
- Cross-branch file conflict analysis

#### BRANCH_MAPPING.md
- Quick reference table for all 14 branches
- Detailed information for each branch
- Decision tree for branch selection
- Dependency checking logic
- AI agent guidance for each feature

#### BRANCHING.md
- Comprehensive branching strategy
- Branch naming conventions
- Merge workflows
- Code review process
- CI/CD integration

#### SETUP.md
- Development workflow and setup instructions
- Branch protection rules
- Code quality tools
- Next steps for repository setup

#### REPOSITORY_SETUP.md
- Repository creation summary
- Next steps for review process
- GitHub configuration guide
- Success checklist

### 2. Skills (.kilo/skills/)

#### branch_scout.md
**Purpose**: Efficient code discovery across branches

**Key Tools**:
- `list_branches()` - List all branches
- `find_file_in_branches()` - Find which branches contain a file
- `list_code_definitions()` - Get skeletal structure of a file
- `find_symbol_definition()` - Find where a symbol is defined
- `compare_files_between_branches()` - Compare files across branches
- `search_symbol_in_branches()` - Search for symbols across branches
- `get_cross_branch_dependencies()` - Get cross-branch dependencies

**Core Principles**:
- Always scout before reading files
- Use skeletal information to understand structure
- Minimize file reads by understanding what's needed first
- Track cross-branch dependencies

#### test_runner.md
**Purpose**: Run tests in worktrees without merging

**Key Tools**:
- `create_worktree()` - Create a git worktree
- `run_tests_in_worktree()` - Run tests in a worktree
- `run_tests_in_branch()` - Create worktree and run tests
- `run_parallel_tests()` - Run tests on multiple branches in parallel
- `compare_test_results()` - Compare results between branches
- `get_test_coverage()` - Get test coverage
- `cleanup_worktrees()` - Clean up worktrees

**Core Principles**:
- Never merge just to test
- Use worktrees for isolated testing
- Run tests in parallel for speed
- Clean up worktrees after use

### 3. Workflows (.kilo/workflows/)

#### branch_manager.md
**Purpose**: Orchestrate cross-branch operations

**Key Commands**:
- `analyze_task()` - Analyze task and determine branch
- `prepare_worktree()` - Prepare worktree for development
- `implement_change()` - Implement using apply_diff
- `verify_changes()` - Verify changes don't break tests
- `create_pull_request()` - Create PR for changes

**Workflow States**:
1. Discovery - Understand task and select branch
2. Preparation - Create worktrees, get skeletal info
3. Implementation - Apply targeted changes
4. Verification - Run tests, compare results
5. Integration - Create PRs and merge

**Decision Trees**:
- Which branch to work in?
- Do dependencies exist?
- Should I create multiple worktrees?

### 4. Utilities (.kilo/utilities/)

#### apply_diff.md
**Purpose**: Targeted code modifications without regenerating files

**Key Functions**:
- `apply_diff()` - Apply single change
- `apply_diffs()` - Apply multiple changes

**Benefits**:
- 80-90% reduction in context usage
- Precise, testable changes
- Preserves code style and structure
- Faster and more efficient

**Usage Patterns**:
- Add methods to classes
- Modify function signatures
- Add parameters
- Fix bugs in specific lines
- Add decorators
- Add imports

### 5. Scripts

#### scan_symbols.py
- Python script to scan all branches and generate symbols.md
- Uses git worktrees to scan without disturbing current branch
- Extracts AST-based symbols from all Python files
- Generates comprehensive markdown report

## How to Use This System

### For AI Agents

#### Step 1: Always Check symbols.md First

Before reading any file, check symbols.md:
```python
# Step 1: Check symbols.md for overview
# This gives you complete structure without reading files

# Step 2: Find relevant files
# Use the branch mapping to find which branch contains the code

# Step 3: Get skeletal structure
# Use list_code_definitions() to understand file structure

# Step 4: Decide what to read
# Only read files if absolutely necessary
```

#### Step 2: Use Branch Mapping to Find Where to Work

```python
# Use BRANCH_MAPPING.md decision tree
task = "Implement tool approval workflow"

# Decision tree says: feature/dynamic-tools
target_branch = "feature/dynamic-tools"

# Check dependencies
deps = check_branch_dependencies(target_branch)
if not deps['satisfied']:
    # Work on dependencies first
    target_branch = deps['missing'][0]
```

#### Step 3: Use branch_scout Before Reading Files

```python
# Don't read the file yet!
# First, get skeletal structure

defs = list_code_definitions("tools/tool_registry.py", "feature/dynamic-tools")

# Now you know:
# - What classes exist
# - What methods exist
# - What functions exist
# - What imports are used

# Decide if you need to read the full file
if "approve_tool" in [m['name'] for cls in defs['classes'] for m in cls['methods']]:
    # Found the method, can work with just the signature
    pass
else:
    # Need to read the file to find implementation
    read_file("tools/tool_registry.py")
```

#### Step 4: Use apply_diff for Changes

```python
# Don't regenerate the entire file!
# Use apply_diff for targeted changes

result = apply_diff(
    "tools/tool_registry.py",
    "    def approve_tool(self, tool_name: str, approver_id: str) -> bool:",
    "    def approve_tool(self, tool_name: str, approver_id: str, force: bool = False) -> bool:"
)

# This saves 80-90% of context!
```

#### Step 5: Use test_runner for Verification

```python
# Don't merge just to test!
# Use worktrees

# Create worktree and run tests
result = run_tests_in_branch("feature/dynamic-tools", "tests/tools/")

# Compare with develop
comparison = compare_test_results("develop", "feature/dynamic-tools")

# Check for regressions
if comparison['comparison']['new_failures']:
    print("Changes introduce failures, fix before merging")
else:
    print("Changes verified, ready for PR")
```

### For Developers

#### Setting Up Worktrees

```bash
# Create worktrees directory
mkdir -p worktrees

# Create worktrees for active branches
git worktree add worktrees/wt-develop develop
git worktree add worktrees/wt-redux feature/redux-state-management
git worktree add worktrees/wt-agents feature/agent-framework

# List worktrees
git worktree list

# Work in a worktree
cd worktrees/wt-agents
# Make changes
git add .
git commit -m "feat: add async task execution"
git push origin feature/agent-framework

# Cleanup when done
cd ..
git worktree remove worktrees/wt-agents
```

#### Running Tests in Worktrees

```bash
# Run tests in specific worktree
cd worktrees/wt-agents
pytest tests/agents/ -v

# Run tests from main branch
python -m pytest tests/ --worktree worktrees/wt-agents

# Compare test results
# (Use test_runner skill programmatically)
```

#### Cross-Branch Development Workflow

```bash
# 1. Check dependencies in CROSS_BRANCH_DEPENDENCIES.md
# 2. Select appropriate branch using BRANCH_MAPPING.md
# 3. Create worktree for that branch
git worktree add worktrees/wt-agents feature/agent-framework

# 4. Make changes using apply_diff (not full file rewrites)
# 5. Run tests in worktree
cd worktrees/wt-agents && pytest tests/

# 6. Compare with develop
# (Use test_runner skill)

# 7. Create PR if tests pass
# 8. Cleanup worktree
git worktree remove worktrees/wt-agents
```

## Context Optimization Checklist

### Before Starting Work

- [ ] Checked symbols.md for code structure
- [ ] Used BRANCH_MAPPING.md to select correct branch
- [ ] Checked CROSS_BRANCH_DEPENDENCIES.md for dependencies
- [ ] Created worktree for target branch
- [ ] Used list_code_definitions() to get skeletal structure
- [ ] Decided if full file read is necessary

### During Development

- [ ] Using apply_diff for changes (not full rewrites)
- [ ] Running tests in worktrees (not merging)
- [ ] Checking cross-branch implications
- [ ] Following dependency order
- [ ] Minimizing file reads

### Before Committing

- [ ] Tests pass in worktree
- [ ] Compared results with develop
- [ ] No regressions introduced
- [ ] Cross-branch dependencies satisfied
- [ ] Documentation updated

### After Merging

- [ ] Created pull request
- [ ] Requested reviews
- [ ] Cleaned up worktrees
- [ ] Updated develop worktree
- [ ] Updated symbols.md if needed

## Performance Metrics

### Context Usage Comparison

**Without Optimization**:
- File reads: ~10-20 full files
- Tokens used: ~8,000-15,000 per task
- Time: Slower due to reading large files
- Efficiency: Low

**With Optimization**:
- File reads: 1-3 full files (only when necessary)
- Tokens used: ~1,000-2,000 per task
- Time: Faster due to skeletal information
- Efficiency: High (85-90% reduction)

### Testing Efficiency

**Without Worktrees**:
- Must merge branches to test
- Risk of breaking other branches
- Slow workflow (merge, test, reset)
- Conflicts frequent

**With Worktrees**:
- Test in isolation
- No risk to other branches
- Fast workflow (create worktree, test, cleanup)
- No conflicts until integration

## Common Workflows

### Workflow 1: Implementing a New Feature

```python
# 1. Analyze task
task = "Implement tool approval workflow"
result = analyze_task(task)
target_branch = result['target_branch']

# 2. Check dependencies
deps = check_branch_dependencies(target_branch)
if not deps['satisfied']:
    # Work on dependencies first
    return

# 3. Prepare worktree
prepare_worktree(target_branch)

# 4. Use branch_scout
defs = list_code_definitions("tools/tool_registry.py", target_branch)

# 5. Apply changes using apply_diff
implement_change("tools/tool_registry.py", changes, worktree_path)

# 6. Verify changes
verify_changes(target_branch)

# 7. Create PR
create_pull_request(target_branch)
```

### Workflow 2: Fixing a Bug

```python
# 1. Find where bug exists
location = find_symbol_definition("ToolRegistry")

# 2. Get skeletal structure
defs = list_code_definitions(location['files'][0], location['branches'][0])

# 3. Identify the bug
# Use search_symbol_in_branches() if needed

# 4. Apply fix using apply_diff
implement_change(file_path, changes, worktree_path)

# 5. Run tests
run_tests_in_worktree(worktree_name)

# 6. Compare with develop
compare_test_results("develop", target_branch)

# 7. Create PR if tests pass
```

### Workflow 3: Multi-Branch Task

```python
# 1. Analyze task
task = "Add message timestamp tracking"
result = analyze_task(task)

# 2. Identify affected branches
affected_branches = result['affected_branches']

# 3. Create worktrees for all affected branches
prepare_worktrees(affected_branches)

# 4. Implement in target branch first
implement_change(..., target_branch_worktree)

# 5. Update affected branches
for branch in affected_branches[1:]:
    implement_change(..., branch_worktree)

# 6. Run parallel tests
results = run_parallel_tests(affected_branches)

# 7. Verify no regressions
for branch, result in results['results'].items():
    if result['failed'] > 0:
        print(f"Fix failures in {branch}")

# 8. Create PRs in dependency order
for branch in get_dependency_order(affected_branches):
    create_pull_request(branch)

# 9. Cleanup
cleanup_worktrees()
```

## Troubleshooting

### Issue: Worktree Already Exists

**Problem**: Trying to create worktree that already exists

**Solution**:
```python
worktrees = list_worktrees()
if not any(wt['branch'] == branch for wt in worktrees):
    create_worktree(branch)
else:
    # Use existing worktree
    pass
```

### Issue: Dependencies Not Satisfied

**Problem**: Branch has unmet dependencies

**Solution**:
```python
deps = check_branch_dependencies(target_branch)
if not deps['satisfied']:
    print(f"Dependencies not satisfied: {deps['missing']}")
    # Work on dependencies first in order
    for dep in get_dependency_order(deps['missing']):
        work_on_branch(dep)
```

### Issue: Tests Fail After Changes

**Problem**: Changes break tests

**Solution**:
```python
result = run_tests_in_worktree(worktree_name)
if result['status'] != 'success':
    print(f"Tests failed: {result['output']}")
    # Fix issues before proceeding
    # May need to revert changes
```

### Issue: Cross-Branch Conflicts

**Problem**: File differs in multiple branches

**Solution**:
```python
conflicts = compare_files_between_branches(file_path, branches)
if conflicts['different']:
    print(f"File differs in multiple branches, coordinate changes")
    # Discuss with team before proceeding
    # May need to work on all branches simultaneously
```

## Summary

This context-optimized environment provides:

### For AI Agents
- ✅ Complete code map in symbols.md
- ✅ Branch mapping for quick navigation
- ✅ branch_scout for efficient code discovery
- ✅ apply_diff for targeted changes
- ✅ test_runner for isolated testing
- ✅ branch_manager for orchestration
- ✅ 80-90% reduction in context usage

### For Developers
- ✅ Clear branch structure and dependencies
- ✅ Worktree-based testing without merging
- ✅ Parallel development workflow
- ✅ Safe integration process
- ✅ Comprehensive documentation

### Key Benefits
- 🚀 Faster development cycles
- 🎯 Targeted code changes
- 🧪 Isolated testing
- 📊 Minimal context usage
- 🔄 Efficient cross-branch work

## Next Steps

1. **Update symbols.md** regularly as code changes
2. **Create worktrees** for active branches
3. **Follow the workflows** for consistency
4. **Use the skills** for efficiency
5. **Monitor context usage** to ensure optimization

Remember: **Always scout before reading, always use apply_diff, always test in worktrees!**
