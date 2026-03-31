# Branch Scout Skill

## Purpose
The branch_scout skill enables efficient code discovery across multiple git branches without switching branches or merging. It provides tools for:
- Scanning branches for specific files, classes, or functions
- Getting skeletal structure of files before reading them
- Finding cross-branch references and dependencies
- Locating relevant code based on symbols and patterns

## Core Principles

### 1. Always Scout Before Read
Before reading any file, use branch_scout to:
- Check if the file exists in the current branch
- Find which branches contain the file
- Get the skeletal structure (classes, functions, imports)
- Determine if reading the full file is necessary

### 2. Minimal Context Usage
- Use skeletal information to understand code structure
- Only read full files when absolutely necessary
- Leverage git to compare differences between branches
- Use grep for pattern matching instead of full file reads

### 3. Cross-Branch Awareness
- Always check multiple branches for the same symbol
- Track which branch defines each symbol
- Identify cross-branch dependencies
- Use worktrees to access branches without switching

## Available Tools

### 1. `list_branches`
List all available branches in the repository.

**Usage**: `list_branches()`

**Returns**: List of branch names

**Example**:
```python
branches = list_branches()
# ['main', 'develop', 'feature/redux-state-management', ...]
```

### 2. `find_file_in_branches`
Find which branches contain a specific file.

**Usage**: `find_file_in_branches(file_path: str) -> dict`

**Parameters**:
- `file_path`: Path to file (relative to repo root)

**Returns**: Dictionary mapping branch names to file existence status

**Example**:
```python
result = find_file_in_branches("rlm/core/rlm.py")
# {
#     'main': True,
#     'develop': True,
#     'feature/agent-framework': True,
#     'feature/redux-state-management': False,
#     ...
# }
```

### 3. `list_code_definitions`
Get skeletal structure of a file (classes, functions, imports).

**Usage**: `list_code_definitions(file_path: str, branch: str = None) -> dict`

**Parameters**:
- `file_path`: Path to file (relative to repo root)
- `branch`: Branch to check (default: current branch)

**Returns**: Dictionary with:
- `imports`: List of import statements
- `classes`: List of class names and their methods
- `functions`: List of function names and signatures
- `file_exists`: Boolean indicating if file exists

**Example**:
```python
defs = list_code_definitions("rlm/core/rlm.py", "feature/agent-framework")
# {
#     'imports': ['from typing import ...', 'import os', ...],
#     'classes': [
#         {
#             'name': 'RLM',
#             'methods': ['__init__', 'completion', '_setup_prompt', ...]
#         }
#     ],
#     'functions': ['find_final_answer', 'format_iteration', ...],
#     'file_exists': True
# }
```

### 4. `find_symbol_definition`
Find where a specific class, function, or variable is defined.

**Usage**: `find_symbol_definition(symbol_name: str) -> dict`

**Parameters**:
- `symbol_name`: Name of class, function, or variable to find

**Returns**: Dictionary with:
- `branches`: List of branches containing the symbol
- `files`: List of file paths where symbol is defined
- `type`: Type of symbol (class, function, variable)
- `definition_line`: Line number of definition

**Example**:
```python
result = find_symbol_definition("RLM")
# {
#     'branches': ['main', 'develop', 'feature/agent-framework', ...],
#     'files': ['rlm/core/rlm.py'],
#     'type': 'class',
#     'definition_line': 45
# }
```

### 5. `compare_files_between_branches`
Compare the same file across multiple branches.

**Usage**: `compare_files_between_branches(file_path: str, branches: list) -> dict`

**Parameters**:
- `file_path`: Path to file (relative to repo root)
- `branches`: List of branches to compare

**Returns**: Dictionary with:
- `identical`: List of branches with identical file content
- `different`: List of branches with different content
- `missing`: List of branches where file doesn't exist
- `differences`: Detailed diff between branches

**Example**:
```python
result = compare_files_between_branches(
    "rlm/core/rlm.py",
    ["main", "develop", "feature/agent-framework"]
)
# {
#     'identical': ['main', 'develop'],
#     'different': ['feature/agent-framework'],
#     'missing': [],
#     'differences': {
#         'main vs feature/agent-framework': '--- a/rlm/core/rlm.py\n+++ b/rlm/core/rlm.py\n...'
#     }
# }
```

### 6. `list_files_in_branch`
List all files in a specific branch with optional filtering.

**Usage**: `list_files_in_branch(branch: str, pattern: str = None) -> list`

**Parameters**:
- `branch`: Branch to list files from
- `pattern`: Optional glob pattern to filter files (e.g., "*.py", "rlm/**/*.py")

**Returns**: List of file paths

**Example**:
```python
# All Python files in branch
all_py_files = list_files_in_branch("feature/agent-framework", "*.py")

# Files in rlm directory
rlm_files = list_files_in_branch("develop", "rlm/**/*.py")

# All files in branch
all_files = list_files_in_branch("main")
```

### 7. `search_symbol_in_branches`
Search for a symbol (class, function, variable) across all branches.

**Usage**: `search_symbol_in_branches(symbol_name: str) -> dict`

**Parameters**:
- `symbol_name`: Name of symbol to search for

**Returns**: Dictionary mapping branch names to list of locations where symbol is found

**Example**:
```python
results = search_symbol_in_branches("spawn_agent")
# {
#     'main': [],
#     'develop': [],
#     'feature/swarm-orchestration': [
#         'rlm/core/swarm_rlm.py:231',
#         'rlm/core/swarm_rlm.py:489'
#     ],
#     'feature/agent-framework': []
# }
```

### 8. `get_cross_branch_dependencies`
Identify cross-branch dependencies for a specific file or symbol.

**Usage**: `get_cross_branch_dependencies(file_path: str = None, symbol_name: str = None) -> dict`

**Parameters**:
- `file_path`: Path to file to analyze (optional)
- `symbol_name`: Symbol to analyze (optional)

**Returns**: Dictionary with:
- `dependencies`: List of symbols/files from other branches
- `dependent_branches`: List of branches that depend on this
- `usage_locations`: Where this is used in other branches

**Example**:
```python
deps = get_cross_branch_dependencies(symbol_name="MessageBroker")
# {
#     'dependencies': [],
#     'dependent_branches': ['feature/swarm-orchestration', 'feature/visualization-interface'],
#     'usage_locations': {
#         'feature/swarm-orchestration': ['rlm/core/swarm_rlm.py:45'],
#         'feature/visualization-interface': ['ui/dashboard.py:123']
#     }
# }
```

## Usage Patterns

### Pattern 1: Finding Where to Work

When you need to find which branch contains the code you want to modify:

```python
# Step 1: Find which branches have the file
file_path = "rlm/core/rlm.py"
branches_with_file = find_file_in_branches(file_path)

# Step 2: Get skeletal definitions from each relevant branch
for branch in branches_with_file.keys():
    if branches_with_file[branch]:
        defs = list_code_definitions(file_path, branch)
        print(f"Branch: {branch}")
        print(f"  Classes: {defs['classes']}")
        print(f"  Functions: {defs['functions']}")
```

### Pattern 2: Understanding Code Structure

Before reading a file, understand its structure:

```python
file_path = "rlm/core/swarm_rlm.py"

# Get skeletal structure first
defs = list_code_definitions(file_path, "feature/swarm-orchestration")

# Decide which parts to read based on what you're looking for
if "spawn_agent" in defs['functions']:
    # Read only the relevant parts or search for the function
    # Use grep or targeted read instead of reading entire file
    pass
```

### Pattern 3: Cross-Branch Analysis

When checking if changes in one branch affect others:

```python
symbol = "MessageBroker"

# Find all locations where this symbol is used
locations = search_symbol_in_branches(symbol)

# Get cross-branch dependencies
deps = get_cross_branch_dependencies(symbol_name=symbol)

# This tells you which branches will be affected by changes to MessageBroker
```

### Pattern 4: Efficient Code Navigation

When trying to understand the codebase structure:

```python
# Step 1: List all Python files in a branch
py_files = list_files_in_branch("feature/agent-framework", "*.py")

# Step 2: For each file, get skeletal structure
for file_path in py_files[:10]:  # Limit to first 10 for exploration
    defs = list_code_definitions(file_path, "feature/agent-framework")
    if defs['classes'] or defs['functions']:
        print(f"{file_path}: {len(defs['classes'])} classes, {len(defs['functions'])} functions")
```

## Integration with Other Skills

### With test_runner Skill
```python
# Find test files across branches
test_files = list_files_in_branch("feature/testing-infrastructure", "tests/**/*.py")

# For each test file, get its structure
for test_file in test_files:
    defs = list_code_definitions(test_file, "feature/testing-infrastructure")
    # Identify which tests exist
```

### With branch_manager Workflow
```python
# Before creating a new branch, check if work already exists
symbol = "ToolRegistry"
existing = search_symbol_in_branches(symbol)

if existing:
    # Decide which branch to work in based on existing work
    pass
```

## Best Practices

1. **Always check symbols.md first** - It provides a complete map of all code across branches

2. **Use skeletal information** - Get structure before reading full files

3. **Target specific branches** - Don't scan all branches unless necessary

4. **Use worktrees for deeper analysis** - When you need to read files from multiple branches

5. **Cache results** - Branch information doesn't change frequently, cache where possible

6. **Minimize git operations** - Git operations can be slow, batch them when possible

7. **Use pattern matching** - Use glob patterns to filter results before processing

## Performance Considerations

- **list_code_definitions**: Fast - uses AST parsing, minimal git operations
- **find_file_in_branches**: Medium - checks existence in all branches
- **search_symbol_in_branches**: Slow - searches all files in all branches
- **compare_files_between_branches**: Medium to Slow - depends on file size

For best performance:
- Use more specific tools when possible
- Limit the number of branches you check
- Use pattern matching to filter results
- Cache results when branches haven't changed

## Error Handling

All tools handle errors gracefully:
- File not found: Returns empty results or `{'file_exists': False}`
- Branch not found: Returns empty results or `{'branch_exists': False}`
- Invalid input: Returns error message in result

## Example Workflow

```python
# User wants to modify the MessageBroker class

# Step 1: Find where MessageBroker is defined
location = find_symbol_definition("MessageBroker")
# Result: defined in feature/messaging-system at messaging/message_broker.py

# Step 2: Get skeletal structure
defs = list_code_definitions("messaging/message_broker.py", "feature/messaging-system")

# Step 3: Check which branches use MessageBroker
usage = search_symbol_in_branches("MessageBroker")
# Result: used in feature/swarm-orchestration, feature/visualization-interface

# Step 4: Get cross-branch dependencies
deps = get_cross_branch_dependencies(symbol_name="MessageBroker")

# Step 5: Decide which branch to work in
# Since MessageBroker is defined in feature/messaging-system,
# work should happen in that branch

# Step 6: Use worktree to access the branch
# (This would be handled by branch_manager workflow)

# Step 7: Use apply_diff to make targeted changes
# (This would be handled by apply_diff utility)
```

## Summary

The branch_scout skill provides efficient code discovery across branches:
- ✅ Scout before reading to minimize context usage
- ✅ Get skeletal structure before full file reads
- ✅ Track cross-branch dependencies
- ✅ Enable parallel development with worktrees
- ✅ Optimize for minimal context usage

Use branch_scout whenever you need to:
- Find where code is defined
- Understand code structure before reading
- Check cross-branch dependencies
- Locate relevant code for a task
- Compare code across branches
