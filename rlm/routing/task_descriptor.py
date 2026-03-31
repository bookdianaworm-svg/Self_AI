"""
Task descriptor generation for routing decisions.
"""

from typing import Any, Callable, Dict


def default_task_descriptor_fn(prompt: str, depth: int) -> Dict[str, Any]:
    """
    Default function to generate task descriptors from prompts.

    This function analyzes the prompt and generates a task descriptor
    that can be used by the backend and environment routers.

    Args:
        prompt: The prompt for the sub-call
        depth: The depth of this sub-call

    Returns:
        Dictionary with task descriptor fields
    """
    # Simple heuristic-based classification
    # In production, this could use an LLM to classify

    intent = classify_intent(prompt)
    complexity_score = estimate_complexity(prompt, depth)

    return {
        "subtask_id": f"subtask-{depth}-{hash(prompt) % 10000}",
        "parent_task_id": "main",
        "intent": intent,
        "complexity_score": complexity_score,
        "latency_budget_ms": 5000,  # Default 5 second budget
        "cost_sensitivity": "medium",
        "token_estimate": len(prompt.split()) * 1.3,  # Rough estimate
        "safety_level": "medium",
        "capabilities": {
            "needs_internet": needs_internet(prompt),
            "needs_filesystem": needs_filesystem(prompt),
            "needs_lean_access": needs_lean_access(prompt),
            "needs_haskell_access": needs_haskell_access(prompt),
            "needs_docker_isolation": needs_docker_isolation(prompt)
        },
        "security": {
            "data_sensitivity": "internal"
        },
        "performance": {
            "expected_cpu_seconds": estimate_cpu_time(prompt, complexity_score)
        },
        "mode": "dev"
    }


def classify_intent(prompt: str) -> str:
    """Classify the intent of a prompt."""
    import re
    prompt_lower = prompt.lower()
    
    # Tokenize to avoid substring matching
    words = set(re.findall(r'\b\w+\b', prompt_lower))
    
    # Check for web research first (including "search" as standalone word)
    web_research_words = {"research", "find", "lookup", "arxiv", "google", "search"}
    if words & web_research_words:
        # If "search" is combined with programming terms, it's code generation
        programming_search_terms = {"binary", "linear", "sort", "tree", "graph", "algorithm", "depth", "breadth", "node", "edge", "path"}
        if "search" in words and words & programming_search_terms:
            return "code_generation"
        return "web_research"
    
    # Check for proof synthesis (before refactor and code generation)
    proof_words = {"prove", "theorem", "lean", "formal", "verify"}
    if words & proof_words:
        return "proof_synthesis"
    
    # Check for refactor (before code generation)
    refactor_words = {"refactor", "improve", "optimize", "clean"}
    if words & refactor_words:
        return "refactor"
    
    # Check for code generation
    code_words = {"code", "implement", "function", "class", "write"}
    if words & code_words:
        return "code_generation"
    
    # Check for summarization
    summary_words = {"summarize", "summary", "brief"}
    if words & summary_words:
        return "summarization"
    
    return "general"


def estimate_complexity(prompt: str, depth: int) -> float:
    """Estimate complexity score (0.0-1.0) for a prompt."""
    # Base complexity from depth (ensure non-negative)
    base = max(0.0, min(depth / 10.0, 0.5))

    # Add complexity from prompt length and structure
    length_factor = min(len(prompt) / 5000.0, 0.3)

    # Add complexity from keywords
    complexity_keywords = ["prove", "theorem", "optimize", "design", "architecture"]
    keyword_factor = sum(1 for kw in complexity_keywords if kw.lower() in prompt.lower()) * 0.05

    return max(0.0, min(base + length_factor + keyword_factor, 1.0))


def needs_internet(prompt: str) -> bool:
    """Check if prompt likely needs internet access."""
    internet_keywords = ["search", "research", "arxiv", "google", "download", "fetch", "url", "http"]
    return any(kw in prompt.lower() for kw in internet_keywords)


def needs_filesystem(prompt: str) -> bool:
    """Check if prompt likely needs filesystem access."""
    fs_keywords = ["file", "read", "write", "save", "load", "directory", "path"]
    return any(kw in prompt.lower() for kw in fs_keywords)


def needs_lean_access(prompt: str) -> bool:
    """Check if prompt likely needs Lean verification."""
    lean_keywords = ["prove", "theorem", "lean", "formal", "verify", "axiom"]
    return any(kw in prompt.lower() for kw in lean_keywords)


def needs_haskell_access(prompt: str) -> bool:
    """Check if prompt likely needs Haskell type checking."""
    haskell_keywords = ["type", "dimensional", "unit", "haskell"]
    return any(kw in prompt.lower() for kw in haskell_keywords)


def needs_docker_isolation(prompt: str) -> bool:
    """Check if prompt likely needs Docker isolation."""
    prompt_lower = prompt.lower()
    docker_keywords = ["docker", "container", "isolation", "sandbox", "untrusted"]
    return any(kw in prompt_lower for kw in docker_keywords)


def estimate_cpu_time(prompt: str, complexity: float) -> int:
    """Estimate expected CPU time in seconds."""
    base_time = 1.0
    complexity_multiplier = 1.0 + (complexity * 10.0)
    length_multiplier = 1.0 + (len(prompt) / 10000.0)
    return int(base_time * complexity_multiplier * length_multiplier)
