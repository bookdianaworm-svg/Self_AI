"""Knowledge extraction from agent run history for future task similarity."""

import hashlib
import json
import re
from typing import Any

from rlm.storage.agent_loop_storage import AgentLoopStorage
from rlm.storage.task_fingerprint import compute as compute_fingerprint
from rlm.storage.task_knowledge_storage import TaskKnowledgeStorage


# Error pattern regex groups by error type
_ERROR_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("ImportError", re.compile(r"^\s*ImportError\s*[:]", re.MULTILINE)),
    ("TypeError", re.compile(r"^\s*TypeError\s*[:]", re.MULTILINE)),
    ("SyntaxError", re.compile(r"^\s*SyntaxError\s*[:]", re.MULTILINE)),
    ("AssertionError", re.compile(r"^\s*AssertionError\s*[:]", re.MULTILINE)),
    ("RuntimeError", re.compile(r"^\s*RuntimeError\s*[:]", re.MULTILINE)),
]

# Task type keyword classification
_TASK_TYPE_KEYWORDS: dict[str, list[str]] = {
    "bugfix": ["fix", "bug", "error", "crash"],
    "feature": ["add", "create", "implement", "build"],
    "refactor": ["update", "modify", "refactor"],
    "testing": ["test", "spec"],
    "infrastructure": ["deploy", "setup", "config"],
}


def _classify_task_type(description: str) -> str:
    """Classify task type via keyword match on task description."""
    lower = description.lower()
    for task_type, keywords in _TASK_TYPE_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return task_type
    return "investigation"


def _extract_code_artifacts(
    agent_history: dict[str, Any],
) -> list[dict[str, str]]:
    """Extract code artifacts from agent history.

    Finds file_path + content from code_blocks, hashes each (sha256 hex),
    dedupes by path keeping the latest.
    """
    seen_paths: dict[str, str] = {}  # path -> hash, for dedupe

    for iteration in agent_history.get("iterations", []):
        raw_code_blocks = iteration.get("code_blocks")
        if not raw_code_blocks:
            continue

        # code_blocks is stored as JSON string
        try:
            code_blocks = json.loads(raw_code_blocks) if isinstance(raw_code_blocks, str) else raw_code_blocks
        except (json.JSONDecodeError, TypeError):
            continue

        for block in code_blocks:
            # Extract file_path from the block structure
            # Each block may have code + result, but we look for file artifacts
            content = block.get("code", "")
            result = block.get("result", {})
            # Try to find file_path in result (e.g., result.file_path or similar)
            file_path = result.get("file_path") if isinstance(result, dict) else None
            if not file_path:
                file_path = result.get("metadata", {}).get("file_path") if isinstance(result, dict) else None
            if not file_path:
                continue

            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            # Dedupe by path keeping latest (iterations are ordered desc by timestamp)
            if file_path not in seen_paths:
                seen_paths[file_path] = content_hash

    return [
        {"file_path": path, "content_hash": hash_val}
        for path, hash_val in seen_paths.items()
    ]


def _extract_error_patterns(
    agent_history: dict[str, Any],
) -> dict[str, int]:
    """Extract error patterns from failed REPL executions.

    Regex matches stderr for error types (ImportError, TypeError, SyntaxError,
    AssertionError, RuntimeError), groups and counts.
    """
    counts: dict[str, int] = {}
    for execution in agent_history.get("repl_executions", []):
        if execution.get("success") == 1:
            continue
        stderr = execution.get("stderr", "")
        if not stderr:
            continue
        for error_name, pattern in _ERROR_PATTERNS:
            if pattern.search(stderr):
                counts[error_name] = counts.get(error_name, 0) + 1
    return counts


def _build_lessons(
    error_patterns: dict[str, int],
    code_artifacts: list[dict[str, str]],
) -> str:
    """Build rule-based lessons from error patterns and code artifacts (no LLM)."""
    lines: list[str] = []

    if error_patterns:
        error_summary = ", ".join(
            f"{name} ({count})" for name, count in sorted(error_patterns.items(), key=lambda x: -x[1])
        )
        lines.append(f"Errors encountered: {error_summary}.")

    if code_artifacts:
        paths = [a["file_path"] for a in code_artifacts]
        lines.append(f"Files modified: {', '.join(paths)}.")

    return " ".join(lines) if lines else ""


class KnowledgeExtractor:
    """Extracts structured knowledge from an agent run for future task similarity."""

    def __init__(self, kb_storage: TaskKnowledgeStorage) -> None:
        self.kb_storage = kb_storage
        self._agent_storage: AgentLoopStorage | None = None

    def _get_agent_storage(self) -> AgentLoopStorage:
        """Lazily create AgentLoopStorage on first use."""
        if self._agent_storage is None:
            self._agent_storage = AgentLoopStorage()
        return self._agent_storage

    def save(
        self,
        agent_id: str,
        task_id: str,
        runner_id: str,
        final_answer: str,
        task_description: str = "",
    ) -> str:
        """Extract and save knowledge from an agent run.

        Args:
            agent_id: The agent instance ID.
            task_id: The task identifier.
            runner_id: The runner/process ID.
            final_answer: The final answer from the agent run.
            task_description: Optional task description for fingerprinting.

        Returns:
            The saved knowledge_id from TaskKnowledgeStorage.
        """
        # 1. Extract code artifacts from agent history
        agent_storage = self._get_agent_storage()
        agent_history = agent_storage.get_agent_history(agent_id)
        code_artifacts = _extract_code_artifacts(agent_history)

        # 2. Extract error patterns from failed REPL executions
        error_patterns = _extract_error_patterns(agent_history)

        # 3. Rule-based summary: first 500 chars of final_answer stripped
        summary = final_answer[:500].strip() if final_answer else ""

        # 4. Lessons from error_patterns + code_artifacts (no LLM)
        lessons = _build_lessons(error_patterns, code_artifacts)

        # 5. Classify task_type via keyword match
        task_type = _classify_task_type(task_description)

        # 6. Fingerprint via TaskFingerprint.compute
        fingerprint = compute_fingerprint(task_description or final_answer)

        # 7. Find similar tasks via kb_storage.find_similar
        similar = self.kb_storage.find_similar(fingerprint)

        # 8. Assemble metadata
        metadata = {
            "agent_id": agent_id,
            "task_id": task_id,
            "runner_id": runner_id,
            "code_artifacts": code_artifacts,
            "similar_count": len(similar),
            "lessons": lessons,
        }

        # Build knowledge entry
        knowledge: dict[str, Any] = {
            "fingerprint": fingerprint,
            "task_type": task_type,
            "content": summary,
            "success_pattern": lessons if error_patterns else None,
            "failure_pattern": json.dumps(error_patterns) if error_patterns else None,
            "metadata": metadata,
        }

        return self.kb_storage.save(knowledge)
