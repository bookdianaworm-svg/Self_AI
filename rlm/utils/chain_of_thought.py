"""
Chain-of-thought extraction utilities.

Extracts reasoning steps and actions from LLM responses for observability.
"""

import re
from typing import List, Dict, Any, Tuple


def extract_chain_of_thought(response: str) -> List[str]:
    """Extract reasoning steps from LLM response.

    Looks for patterns like:
    - "Let me think..."
    - "I need to..."
    - Numbered reasoning steps
    - "First...", "Then...", "Finally..."
    - Reasoning keywords (Because, Since, Therefore, etc.)

    Args:
        response: The LLM response text to analyze.

    Returns:
        List of reasoning step strings found in the response.
    """
    steps = []

    numbered_pattern = r"^\s*(\d+[.)]\s*(.{20,})$"
    for match in re.finditer(numbered_pattern, response, re.MULTILINE):
        steps.append(match.group(2).strip())

    reasoning_keywords = [
        (
            r"(?:I|I\'ll|I\'m|Let me|First|Then|Next|Finally)\s+(?:think|consider|analyze|examine|look)\s+(.{20,})",
            1,
        ),
        (r"(?:Because|Since|Therefore|Thus|Hence)\s+([^\n]{20,})", 1),
        (r"(?:However|But|Although|Meanwhile)\s+([^\n]{20,})", 1),
        (r"(?:I notice|I see|I observe)\s+([^\n]{20,})", 1),
        (r"(?:My approach|My plan|Strategy):\s*([^\n]{20,})", 1),
        (r"(?:Step \d+|Step one|Step two)\s*:?\s*([^\n]{20,})", 1),
    ]

    for pattern, group_idx in reasoning_keywords:
        matches = re.findall(pattern, response, re.IGNORECASE)
        for match in matches:
            step_text = (
                match
                if isinstance(match, str)
                else match[group_idx - 1]
                if group_idx <= len(match)
                else match[0]
            )
            if step_text and len(step_text) > 10:
                steps.append(step_text.strip())

    seen = set()
    unique_steps = []
    for step in steps:
        normalized = step.lower()[:50]
        if normalized not in seen:
            seen.add(normalized)
            unique_steps.append(step)

    return unique_steps


def identify_action_from_response(response: str) -> str:
    """Identify what action the LLM decided to take based on response content.

    Args:
        response: The LLM response text to analyze.

    Returns:
        Action type string (e.g., 'spawn_agent', 'execute_code', 'final_answer').
    """
    response_lower = response.lower()

    action_patterns = [
        (r"spawn|create|launch|start\s+(?:a\s+)?(?:new\s+)?agent", "spawn_agent"),
        (
            r"execute|run|evaluate|interpret\s+(?:the\s+)?(?:following\s+)?(?:code|python)",
            "execute_code",
        ),
        (r"query|call|ask\s+(?:the\s+)?lm|make\s+(?:a\s+)?llm\s+call", "llm_query"),
        (r"verify|check|prove|validate", "verification"),
        (r"final\s*var|final\s*answer|return\s+(?:this|that|the)", "final_answer"),
        (r"use|apply|call\s+(?:tool|function)", "use_tool"),
        (r"search|find|look\s+up", "search"),
        (r"read|load|import|open", "read_data"),
        (r"write|save|export|store", "write_data"),
        (r"analyze|examine|inspect|review", "analyze"),
        (r"summarize|compress|compact", "summarize"),
        (r"think|reason|deliberate|consider", "reasoning"),
    ]

    for pattern, action in action_patterns:
        if re.search(pattern, response_lower):
            return action

    return "unknown"


def extract_reasoning_context(response: str, code_blocks: List[str]) -> Dict[str, Any]:
    """Extract context about what variables and state were relevant for reasoning.

    Args:
        response: The LLM response text.
        code_blocks: List of code blocks that were executed.

    Returns:
        Dictionary with context about the reasoning (variables mentioned, operations, etc.).
    """
    context: Dict[str, Any] = {
        "variables_mentioned": [],
        "functions_called": [],
        "operations": [],
        "has_code_blocks": len(code_blocks) > 0,
        "code_block_count": len(code_blocks),
    }

    var_pattern = r"\b([a-zA-Z_][a-zA-Z0-9_]{2,30})\b"
    all_text = response + " ".join(code_blocks)
    potential_vars = re.findall(var_pattern, all_text)

    common_words = {
        "the",
        "and",
        "for",
        "with",
        "this",
        "that",
        "these",
        "those",
        "from",
        "have",
        "has",
        "been",
        "being",
        "will",
        "would",
        "could",
        "should",
        "about",
        "which",
        "what",
        "when",
        "where",
        "why",
        "how",
        "all",
        "each",
        "every",
        "both",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "only",
        "own",
        "same",
        "than",
        "too",
        "very",
        "just",
        "also",
        "now",
        "here",
        "there",
        "then",
        "once",
        "always",
        "never",
        "ever",
        "still",
        "already",
        "yet",
        "before",
        "after",
        "later",
        "above",
        "below",
        "up",
        "down",
        "in",
        "out",
        "on",
        "off",
        "over",
        "under",
        "into",
        "within",
        "through",
        "during",
        "before",
        "between",
        "among",
        "since",
        "until",
        "while",
        "if",
        "or",
        "and",
        "not",
        "no",
        "yes",
        "but",
        "so",
        "it",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "done",
        "make",
        "made",
        "doing",
        "can",
        "may",
        "might",
        "must",
        "shall",
        "let",
        "say",
        "said",
        "like",
        "get",
        "got",
        "go",
        "went",
        "come",
        "came",
        "take",
        "took",
        "see",
        "saw",
        "know",
        "knew",
        "think",
        "thought",
        "want",
        "wanted",
        "use",
        "used",
        "find",
        "found",
        "give",
        "gave",
        "tell",
        "told",
        "call",
        "called",
        "first",
        "last",
        "long",
        "great",
        "little",
        "own",
        "good",
        "new",
        "old",
        "right",
        "big",
        "high",
        "different",
        "small",
        "large",
        "next",
        "early",
        "young",
        "important",
        "public",
        "bad",
        "same",
        "able",
        "image",
        "data",
        "function",
        "code",
        "result",
        "error",
        "value",
        "number",
        "type",
        "class",
        "method",
        "return",
        "import",
        "print",
        "file",
        "list",
        "dict",
        "string",
        "int",
        "float",
        "bool",
        "true",
        "false",
        "none",
        "self",
        "args",
        "kwargs",
        "await",
        "async",
        "def",
        "class",
    }

    context["variables_mentioned"] = [
        v for v in potential_vars if v not in common_words
    ][:20]

    func_pattern = r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\("
    functions = re.findall(func_pattern, all_text)
    context["functions_called"] = list(set(functions))[:15]

    if "spawn" in response.lower() or "create" in response.lower():
        context["operations"].append("spawning_agent")
    if "loop" in response.lower() or "iterate" in response.lower():
        context["operations"].append("iteration")
    if "recursive" in response.lower() or "subcall" in response.lower():
        context["operations"].append("recursion")
    if "verify" in response.lower() or "proof" in response.lower():
        context["operations"].append("verification")

    return context


def extract_spawn_reason(response: str, iterations: List[Dict[str, Any]]) -> str:
    """Determine why an agent decided to spawn a child.

    Args:
        response: The LLM response that triggered spawning.
        iterations: Previous iterations for context.

    Returns:
        Human-readable reason for spawning.
    """
    response_lower = response.lower()

    if "subtask" in response_lower or "delegate" in response_lower:
        return "Task delegation to specialized agent"
    if "different approach" in response_lower or "specialist" in response_lower:
        return "Different approach needed"
    if "parallel" in response_lower or "concurrent" in response_lower:
        return "Parallel processing"
    if "deep analysis" in response_lower or "investigate" in response_lower:
        return "Deep investigation required"
    if "independent" in response_lower or "separate" in response_lower:
        return "Independent subtask"
    if "complex" in response_lower or " multifaceted" in response_lower:
        return "Complex task decomposition"

    return "General task delegation"
