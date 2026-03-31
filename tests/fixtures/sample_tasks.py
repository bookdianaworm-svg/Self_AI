"""
Sample task descriptors and prompts for testing.

This module provides sample task data used across multiple test modules.
"""

from typing import Any, Dict, List
from rlm.routing.backend_router import TaskDescriptor


# =============================================================================
# Sample Prompts
# =============================================================================

SAMPLE_PROMPTS = {
    "simple_code": "Write a function that adds two numbers.",
    "complex_code": "Implement a binary search tree with insert, delete, and search operations.",
    "proof_synthesis": "Prove that the sum of two even numbers is even.",
    "web_research": "Search for recent papers on quantum computing.",
    "refactor": "Refactor this code to improve performance.",
    "summarization": "Summarize the following text in 3 sentences.",
    "general": "What is the capital of France?",
    "lean_verification": "Verify the following Lean theorem: theorem add_comm (a b : Nat) : a + b = b + a.",
    "haskell_types": "Check the dimensional types in this Haskell code.",
    "high_complexity": "Design and implement a distributed consensus algorithm with fault tolerance."
}


# =============================================================================
# Sample Task Descriptors
# =============================================================================

SAMPLE_TASK_DESCRIPTORS = {
    "simple_code": TaskDescriptor(
        subtask_id="task-001",
        parent_task_id="main",
        intent="code_generation",
        complexity_score=0.2,
        latency_budget_ms=3000,
        cost_sensitivity="medium",
        token_estimate=50,
        safety_level="low"
    ),

    "complex_code": TaskDescriptor(
        subtask_id="task-002",
        parent_task_id="main",
        intent="code_generation",
        complexity_score=0.6,
        latency_budget_ms=10000,
        cost_sensitivity="low",
        token_estimate=300,
        safety_level="medium"
    ),

    "proof_synthesis": TaskDescriptor(
        subtask_id="task-003",
        parent_task_id="main",
        intent="proof_synthesis",
        complexity_score=0.7,
        latency_budget_ms=15000,
        cost_sensitivity="low",
        token_estimate=200,
        safety_level="high",
        metrics={"needs_lean": True}
    ),

    "web_research": TaskDescriptor(
        subtask_id="task-004",
        parent_task_id="main",
        intent="web_research",
        complexity_score=0.4,
        latency_budget_ms=8000,
        cost_sensitivity="medium",
        token_estimate=100,
        safety_level="medium",
        metrics={"needs_internet": True}
    ),

    "high_complexity": TaskDescriptor(
        subtask_id="task-005",
        parent_task_id="main",
        intent="code_generation",
        complexity_score=0.9,
        latency_budget_ms=30000,
        cost_sensitivity="low",
        token_estimate=1000,
        safety_level="high",
        metrics={"needs_internet": True, "estimated_cpu_seconds": 60}
    )
}


# =============================================================================
# Sample Task Descriptor Dictionaries
# =============================================================================

SAMPLE_TASK_DICTS = {
    "simple": {
        "subtask_id": "subtask-1-1000",
        "parent_task_id": "main",
        "intent": "code_generation",
        "complexity_score": 0.2,
        "latency_budget_ms": 3000,
        "cost_sensitivity": "medium",
        "token_estimate": 50,
        "safety_level": "low",
        "capabilities": {
            "needs_internet": False,
            "needs_filesystem": False,
            "needs_lean_access": False,
            "needs_haskell_access": False,
            "needs_docker_isolation": False
        },
        "security": {"data_sensitivity": "internal"},
        "performance": {"expected_cpu_seconds": 1.0},
        "mode": "dev"
    },

    "complex": {
        "subtask_id": "subtask-2-2000",
        "parent_task_id": "main",
        "intent": "proof_synthesis",
        "complexity_score": 0.8,
        "latency_budget_ms": 15000,
        "cost_sensitivity": "low",
        "token_estimate": 300,
        "safety_level": "high",
        "capabilities": {
            "needs_internet": False,
            "needs_filesystem": True,
            "needs_lean_access": True,
            "needs_haskell_access": False,
            "needs_docker_isolation": False
        },
        "security": {"data_sensitivity": "internal"},
        "performance": {"expected_cpu_seconds": 30.0},
        "mode": "dev"
    },

    "web_task": {
        "subtask_id": "subtask-3-3000",
        "parent_task_id": "main",
        "intent": "web_research",
        "complexity_score": 0.5,
        "latency_budget_ms": 10000,
        "cost_sensitivity": "medium",
        "token_estimate": 150,
        "safety_level": "medium",
        "capabilities": {
            "needs_internet": True,
            "needs_filesystem": False,
            "needs_lean_access": False,
            "needs_haskell_access": False,
            "needs_docker_isolation": False
        },
        "security": {"data_sensitivity": "internal"},
        "performance": {"expected_cpu_seconds": 5.0},
        "mode": "dev"
    }
}


# =============================================================================
# Sample Theorem Data
# =============================================================================

SAMPLE_THEOREMS = {
    "simple": {
        "theorem_id": "theorem-simple-001",
        "statement": "theorem add_comm (a b : Nat) : a + b = b + a",
        "layer2_file": "layer2/simple.lean",
        "expected_status": "passed"
    },

    "complex": {
        "theorem_id": "theorem-complex-001",
        "statement": "theorem distributive_law (a b c : Nat) : a * (b + c) = a * b + a * c",
        "layer2_file": "layer2/complex.lean",
        "expected_status": "passed"
    },

    "failing": {
        "theorem_id": "theorem-failing-001",
        "statement": "theorem false_statement : 1 = 2",
        "layer2_file": "layer2/failing.lean",
        "expected_status": "failed_verification"
    }
}


# =============================================================================
# Sample Layer1 Loading Results
# =============================================================================

SAMPLE_LAYER1_RESULTS = {
    "success": {
        "success": True,
        "mathlib_version": "v4.0.0",
        "physlib_version": "v1.0.0",
        "load_time_ms": 1500.0,
        "memory_mb": 256.0
    },

    "failure": {
        "success": False,
        "error": "Failed to load Lean kernel: Module not found",
        "load_time_ms": 500.0
    },

    "cached": {
        "success": True,
        "cached": True
    }
}


# =============================================================================
# Sample Routing Decisions
# =============================================================================

SAMPLE_ROUTING_DECISIONS = {
    "backend_claude": {
        "decision_id": "decision-001",
        "decision_type": "backend",
        "subtask_id": "task-003",
        "selected": "claude_agent",
        "rule_name": "proof_synthesis_uses_claude",
        "overrides": ["temperature: 0.1", "max_tokens: 4096"],
        "reasoning": "Claude has higher pass rate for proof synthesis tasks",
        "timestamp": 1234567890.0
    },

    "backend_openai": {
        "decision_id": "decision-002",
        "decision_type": "backend",
        "subtask_id": "task-001",
        "selected": "openai_gpt",
        "rule_name": "simple_code_uses_openai",
        "overrides": [],
        "reasoning": "OpenAI is faster for simple code generation",
        "timestamp": 1234567891.0
    },

    "environment_local": {
        "decision_id": "decision-003",
        "decision_type": "environment",
        "subtask_id": "task-003",
        "selected": "local",
        "rule_name": "lean_and_haskell_always_local",
        "reasoning": "Lean and Haskell require local installation",
        "timestamp": 1234567892.0
    },

    "environment_modal": {
        "decision_id": "decision-004",
        "decision_type": "environment",
        "subtask_id": "task-004",
        "selected": "modal",
        "rule_name": "internet_uses_modal",
        "reasoning": "Modal provides internet access for internal data",
        "timestamp": 1234567893.0
    }
}


# =============================================================================
# Helper Functions
# =============================================================================

def get_sample_prompt(prompt_key: str) -> str:
    """
    Get a sample prompt by key.

    Args:
        prompt_key: Key from SAMPLE_PROMPTS

    Returns:
        Sample prompt string

    Raises:
        KeyError: If prompt_key is not found
    """
    return SAMPLE_PROMPTS[prompt_key]


def get_sample_task_descriptor(task_key: str) -> TaskDescriptor:
    """
    Get a sample task descriptor by key.

    Args:
        task_key: Key from SAMPLE_TASK_DESCRIPTORS

    Returns:
        TaskDescriptor instance

    Raises:
        KeyError: If task_key is not found
    """
    return SAMPLE_TASK_DESCRIPTORS[task_key]


def get_sample_task_dict(task_key: str) -> Dict[str, Any]:
    """
    Get a sample task dictionary by key.

    Args:
        task_key: Key from SAMPLE_TASK_DICTS

    Returns:
        Dictionary with task descriptor fields

    Raises:
        KeyError: If task_key is not found
    """
    return SAMPLE_TASK_DICTS[task_key]


def get_sample_theorem(theorem_key: str) -> Dict[str, Any]:
    """
    Get a sample theorem by key.

    Args:
        theorem_key: Key from SAMPLE_THEOREMS

    Returns:
        Dictionary with theorem data

    Raises:
        KeyError: If theorem_key is not found
    """
    return SAMPLE_THEOREMS[theorem_key]


def get_sample_layer1_result(result_key: str) -> Dict[str, Any]:
    """
    Get a sample Layer1 loading result by key.

    Args:
        result_key: Key from SAMPLE_LAYER1_RESULTS

    Returns:
        Dictionary with Layer1 loading result

    Raises:
        KeyError: If result_key is not found
    """
    return SAMPLE_LAYER1_RESULTS[result_key]


def get_sample_routing_decision(decision_key: str) -> Dict[str, Any]:
    """
    Get a sample routing decision by key.

    Args:
        decision_key: Key from SAMPLE_ROUTING_DECISIONS

    Returns:
        Dictionary with routing decision data

    Raises:
        KeyError: If decision_key is not found
    """
    return SAMPLE_ROUTING_DECISIONS[decision_key]
