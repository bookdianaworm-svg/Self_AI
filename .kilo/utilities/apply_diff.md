# Apply Diff Utility

## Purpose
The apply_diff utility enables targeted code modifications without regenerating entire files, dramatically reducing context usage and improving efficiency. It focuses on making precise changes to specific parts of code rather than rewriting whole files.

## Core Principles

### 1. Minimal Changes
- Only change what's necessary
- Preserve existing code structure and style
- Maintain line breaks and indentation
- Keep comments and docstrings intact

### 2. Context Efficiency
- Avoid regenerating entire files
- Use skeletal information to identify what to change
- Apply diffs instead of full rewrites
- Minimize token usage in prompts

### 3. Precision
- Use exact string matching for old_string
- Ensure new_string matches indentation and style
- Test changes after applying
- Verify no unintended side effects

## When to Use apply_diff

### ✅ Use apply_diff when:
- Adding a new method to an existing class
- Modifying a specific function signature
- Adding a parameter to a function
- Updating import statements
- Adding a small block of code
- Fixing a bug in a specific function
- Adding a decorator
- Modifying a conditional statement

### ❌ Don't use apply_diff when:
- Completely restructuring a file
- Moving large blocks of code
- Refactoring entire classes
- Renaming multiple symbols throughout a file
- Changing file structure significantly

## apply_diff Function Signature

```python
def apply_diff(
    file_path: str,
    old_string: str,
    new_string: str,
    worktree_path: str = None
) -> dict
```

### Parameters

**file_path**: Path to file to modify (relative to repo root or worktree root)

**old_string**: Exact string to replace (must match precisely, including indentation and line breaks)

**new_string**: New string to replace old_string with (must maintain proper indentation and style)

**worktree_path**: Optional path to worktree (if modifying a file in a worktree)

### Returns

Dictionary with:
- `status`: 'success' or 'error'
- `changes_applied`: Number of changes made
- `file_path`: Path to modified file
- `diff`: Unified diff showing changes
- `error`: Error message if status is 'error'

## Usage Patterns

### Pattern 1: Add a Method to a Class

```python
# Add a new method to BaseAgent class

result = apply_diff(
    "agents/base_agent.py",
    "class BaseAgent(ABC):\n    \"\"\"\n    Base class for all agents in the swarm system.\n    \"\"\"\n    \n    def __init__(self, agent_id: str, config: AgentConfig, parent_id: Optional[str] = None):",
    "class BaseAgent(ABC):\n    \"\"\"\n    Base class for all agents in the swarm system.\n    \"\"\"\n    \n    def __init__(self, agent_id: str, config: AgentConfig, parent_id: Optional[str] = None):\n        \n    def can_spawn_agents(self) -> bool:\n        \"\"\"\n        Determine if this agent is allowed to spawn other agents.\n        Override in subclasses as needed.\n        \"\"\"\n        return False"
)
```

### Pattern 2: Modify Function Signature

```python
# Make execute_task async

result = apply_diff(
    "agents/base_agent.py",
    "    @abstractmethod\n    def execute_task(self, task_description: str) -> Any:\n        \"\"\"\n        Execute the assigned task. This method should be implemented by subclasses.\n        \"\"\"\n        pass",
    "    @abstractmethod\n    async def execute_task(self, task_description: str) -> Any:\n        \"\"\"\n        Execute the assigned task. This method should be implemented by subclasses.\n        \"\"\"\n        pass"
)
```

### Pattern 3: Add Import

```python
# Add new import at top of file

result = apply_diff(
    "agents/base_agent.py",
    "from abc import ABC, abstractmethod\nfrom typing import Any, Dict, List, Optional, Callable\nfrom dataclasses import dataclass\nfrom enum import Enum\nimport uuid",
    "from abc import ABC, abstractmethod\nfrom typing import Any, Dict, List, Optional, Callable\nfrom dataclasses import dataclass\nfrom enum import Enum\nimport uuid\nimport asyncio"
)
```

### Pattern 4: Add Parameter to Function

```python
# Add timeout parameter to spawn_agent

result = apply_diff(
    "agents/base_agent.py",
    "    def spawn_agent(self, task: str, config: Optional[AgentConfig] = None) -> 'BaseAgent':",
    "    def spawn_agent(self, task: str, config: Optional[AgentConfig] = None, timeout: float = 30.0) -> 'BaseAgent':"
)
```

### Pattern 5: Fix Bug in Specific Line

```python
# Fix bug in method

result = apply_diff(
    "agents/task_agent.py",
    "        # Use the RLM to complete the task\n        completion_result = self.rlm.completion(task_description)\n        \n        # Check if we need to spawn additional agents based on the result",
    "        # Use the RLM to complete the task\n        completion_result = await self.rlm.completion(task_description)\n        \n        # Check if we need to spawn additional agents based on the result"
)
```

### Pattern 6: Add Decorator

```python
# Add retry decorator to method

result = apply_diff(
    "agents/task_agent.py",
    "    async def execute_task(self, task_description: str) -> Any:",
    "    @retry(max_attempts=3, delay=1.0)\n    async def execute_task(self, task_description: str) -> Any:"
)
```

## Multi-Change apply_diff

Sometimes you need to make multiple changes to a file. Use `apply_diffs` for this:

```python
def apply_diffs(
    file_path: str,
    changes: List[dict],
    worktree_path: str = None
) -> dict
```

### Example: Multiple Changes

```python
changes = [
    {
        "old_string": "def execute_task(self, task_description: str) -> Any:",
        "new_string": "async def execute_task(self, task_description: str) -> Any:"
    },
    {
        "old_string": "completion_result = self.rlm.completion(task_description)",
        "new_string": "completion_result = await self.rlm.completion(task_description)"
    },
    {
        "old_string": "from abc import ABC, abstractmethod",
        "new_string": "from abc import ABC, abstractmethod\nimport asyncio"
    }
]

result = apply_diffs("agents/task_agent.py", changes)
```

## Best Practices

### 1. Use Skeletal Information First

Before applying a diff, understand the structure:

```python
# Step 1: Get skeletal structure
defs = list_code_definitions("agents/base_agent.py", "feature/agent-framework")

# Step 2: Find exact location
for cls in defs['classes']:
    if cls['name'] == 'BaseAgent':
        print(f"Found BaseAgent with methods: {cls['methods']}")

# Step 3: Apply targeted change
result = apply_diff(...)
```

### 2. Match Exact Indentation

Always match the exact indentation of the old_string:

```python
# ❌ WRONG - doesn't match indentation
old_string = "class BaseAgent(ABC):"

# ✅ CORRECT - matches indentation
old_string = "class BaseAgent(ABC):\n    \"\"\"\n    Base class for all agents in the swarm system.\n    \"\"\"\n    \n    def __init__(self, agent_id: str, config: AgentConfig, parent_id: Optional[str] = None):"
```

### 3. Preserve Style

Maintain the existing code style:

```python
# Preserve line breaks
old_string = "def method1():\n    pass\n\ndef method2():\n    pass"
new_string = "def method1():\n    pass\n\ndef method2():\n    pass\n\ndef method3():\n    pass"

# Preserve docstring style
old_string = "\"\"\"Single-line docstring.\"\"\""
new_string = "\"\"\"Multi-line docstring\n\nWith multiple paragraphs.\n\"\"\""
```

### 4. Test After Changes

Always verify changes work:

```python
# Apply change
result = apply_diff(...)

# Check if successful
if result['status'] == 'success':
    # Run tests
    test_result = run_tests_in_worktree("wt-agents")
    
    if test_result['status'] == 'success':
        print("Changes verified successfully")
    else:
        print("Tests failed after changes, reverting")
        # Handle error
else:
    print(f"Failed to apply changes: {result['error']}")
```

### 5. Use Context-Specific Changes

Make changes that fit the surrounding context:

```python
# Context-aware change
old_string = "        # Use the RLM to complete the task\n        completion_result = self.rlm.completion(task_description)"
new_string = "        # Use the RLM to complete the task\n        try:\n            completion_result = await self.rlm.completion(task_description)\n        except Exception as e:\n            self.error = str(e)\n            self.status = AgentStatus.FAILED\n            raise"
```

## Common Mistakes

### ❌ Mistake 1: Not Matching Exact Strings

```python
# WRONG - doesn't match exactly
old_string = "class BaseAgent(ABC):"

# CORRECT - match the full class definition
old_string = "class BaseAgent(ABC):\n    \"\"\"\n    Base class for all agents in the swarm system.\n    \"\"\""
```

### ❌ Mistake 2: Not Including Enough Context

```python
# WRONG - too little context, might match in multiple places
old_string = "def execute_task(self, task_description: str):"

# CORRECT - include method body for unique match
old_string = "    @abstractmethod\n    def execute_task(self, task_description: str) -> Any:\n        \"\"\"\n        Execute the assigned task. This method should be implemented by subclasses.\n        \"\"\"\n        pass"
```

### ❌ Mistake 3: Changing Indentation

```python
# WRONG - changes indentation
new_string = "    def execute_task(self, task_description: str) -> Any:\n        pass"

# CORRECT - maintains indentation
new_string = "    @abstractmethod\n    def execute_task(self, task_description: str) -> Any:\n        \"\"\"\n        Execute the assigned task. This method should be implemented by subclasses.\n        \"\"\"\n        pass"
```

### ❌ Mistake 4: Forgetting to Make Functions Async

When changing sync to async, update all calls:

```python
# WRONG - only changed function signature
result = apply_diff("def execute_task(self, task):", "async def execute_task(self, task):")

# CORRECT - also update the call sites
changes = [
    {"old_string": "def execute_task(self, task):", "new_string": "async def execute_task(self, task):"},
    {"old_string": "result = self.execute_task(task)", "new_string": "result = await self.execute_task(task)"}
]
apply_diffs("file.py", changes)
```

## Integration with branch_manager

```python
# Typical workflow with branch_manager

# Step 1: Analyze task
task_result = analyze_task("Add timeout to spawn_agent")
target_branch = task_result['target_branch']

# Step 2: Prepare worktree
worktree_result = prepare_worktree(target_branch)
worktree_path = worktree_result['worktree_path']

# Step 3: Get skeletal structure
defs = list_code_definitions("agents/base_agent.py", target_branch)

# Step 4: Find method to modify
for method in defs['functions']:
    if method['name'] == 'spawn_agent':
        # Found the method, now apply change
        break

# Step 5: Apply change
diff_result = apply_diff(
    "agents/base_agent.py",
    "    def spawn_agent(self, task: str, config: Optional[AgentConfig] = None) -> 'BaseAgent':",
    "    def spawn_agent(self, task: str, config: Optional[AgentConfig] = None, timeout: float = 30.0) -> 'BaseAgent':",
    worktree_path
)

# Step 6: Verify changes
test_result = run_tests_in_worktree(worktree_path.split('/')[-1])

# Step 7: If tests pass, create PR
if test_result['status'] == 'success':
    create_pull_request(target_branch)
```

## Context Savings

### Without apply_diff (inefficient):

```
User: "Add a timeout parameter to spawn_agent method in BaseAgent class"

AI: Reads entire base_agent.py (500 lines)
AI: Regenerates entire file with timeout parameter added
AI: Writes 500 lines back to file
Context used: ~5000 tokens for file read + ~3000 tokens for regeneration = ~8000 tokens
```

### With apply_diff (efficient):

```
User: "Add a timeout parameter to spawn_agent method in BaseAgent class"

AI: Uses list_code_definitions to see structure (100 tokens)
AI: Applies targeted diff (50 tokens)
AI: Tests the change (1000 tokens)
Context used: ~1150 tokens
Savings: ~85% reduction in context usage
```

## Advanced Patterns

### Pattern 1: Conditional Logic Addition

```python
result = apply_diff(
    "agents/task_agent.py",
    "        # Use the RLM to complete the task\n        completion_result = await self.rlm.completion(task_description)",
    "        # Use the RLM to complete the task\n        completion_result = await self.rlm.completion(task_description)\n        \n        # Check if response is valid\n        if not completion_result or not completion_result.response:\n            raise ValueError(\"Invalid response from RLM\")"
)
```

### Pattern 2: Error Handling Addition

```python
result = apply_diff(
    "agents/task_agent.py",
    "    async def execute_task(self, task_description: str) -> Any:\n        \"\"\"\n        Execute the task using the underlying RLM.\n        \"\"\"\n        print(f\"Agent {self.id} executing task: {task_description}\")",
    "    async def execute_task(self, task_description: str) -> Any:\n        \"\"\"\n        Execute the task using the underlying RLM.\n        \"\"\"\n        print(f\"Agent {self.id} executing task: {task_description}\")\n        \n        try:\n            # Use the RLM to complete the task\n            completion_result = await self.rlm.completion(task_description)\n            return completion_result.response\n        except Exception as e:\n            self.error = str(e)\n            self.status = AgentStatus.FAILED\n            raise"
)
```

### Pattern 3: Logging Addition

```python
result = apply_diff(
    "agents/base_agent.py",
    "from typing import Any, Dict, List, Optional, Callable\nfrom dataclasses import dataclass\nfrom enum import Enum\nimport uuid",
    "from typing import Any, Dict, List, Optional, Callable\nfrom dataclasses import dataclass\nfrom enum import Enum\nimport uuid\nimport logging\n\nlogger = logging.getLogger(__name__)"
)
```

## Summary

The apply_diff utility provides:
- ✅ Targeted code modifications
- ✅ Dramatic reduction in context usage (80-90% savings)
- ✅ Preservation of code style and structure
- ✅ Precise, testable changes
- ✅ Integration with branch_manager workflow
- ✅ Support for multiple changes in one operation

Always use apply_diff when:
- Making small to medium-sized changes
- Adding methods or parameters
- Fixing specific bugs
- Modifying function signatures
- Adding imports or decorators

Never use apply_diff when:
- Restructuring entire files
- Moving large code blocks
- Changing file organization
- Needing comprehensive refactoring
