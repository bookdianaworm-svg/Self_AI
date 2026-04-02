"""
Self-Awareness Task Pairing

Integrates inbox messages with self-reflection loops.
When an inbox message has self_awareness=True, triggers metacognitive check.

Pairing Pattern:
    InboxMessage (self_awareness=True)
        → triggers SelfAwarenessLoop
            → generates reflection_prompt
            → verifies check_internal_state
            → surfaces confidence and adjustments
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ConfidenceLevel(Enum):
    """Self-rated confidence in current approach."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ReflectionEntry:
    """A single reflection entry in the self-awareness log."""

    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    message_id: str = ""
    task_id: str = ""
    prompt: str = ""
    what_went_well: str = ""
    what_could_improve: str = ""
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    adjustments_planned: str = ""
    state_verified: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


class SelfAwarenessLoop:
    """
    Self-awareness metacognitive loop.

    Activated when inbox message has self_awareness=True.
    Generates structured reflection and state verification.
    """

    def __init__(self):
        self.log: List[ReflectionEntry] = []

    def create_entry(
        self,
        message_id: str,
        task_id: str,
        prompt: str,
    ) -> ReflectionEntry:
        """Create a new reflection entry for an inbox message."""
        entry = ReflectionEntry(
            message_id=message_id,
            task_id=task_id,
            prompt=prompt,
        )
        self.log.append(entry)
        return entry

    def generate_reflection_prompt(
        self,
        base_prompt: str,
        state_checks: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a structured self-reflection prompt.

        Args:
            base_prompt: Original reflection prompt from inbox
            state_checks: Dict of state keys → expected values to verify

        Returns:
            Formatted multi-part reflection prompt
        """
        parts = [
            "[META-COGNITIVE REFLECTION]",
            "",
            base_prompt,
            "",
            "Please reflect on the following dimensions:",
            "",
            "1. WHAT WENT WELL",
            "   - What approach worked better than expected?",
            "   - What patterns emerged that I should reuse?",
            "",
            "2. WHAT COULD IMPROVE",
            "   - Where did I make assumptions that proved wrong?",
            "   - What took more effort than anticipated?",
            "",
            "3. CONFIDENCE ASSESSMENT",
            "   - Rate your confidence in the current approach: high / medium / low",
            "   - What would increase your confidence?",
            "",
            "4. ADJUSTMENTS PLANNED",
            "   - What specific changes will you make going forward?",
            "   - How will you verify those changes work?",
            "",
        ]

        if state_checks:
            parts.append("5. STATE VERIFICATION")
            parts.append("   Required state checks:")
            for key, expected in state_checks.items():
                parts.append(f"   - {key}: expected={expected}")
            parts.append("")

        return "\n".join(parts)

    def verify_state(
        self,
        entry: ReflectionEntry,
        actual_state: Dict[str, Any],
    ) -> Dict[str, bool]:
        """
        Verify internal state against expected values.

        Args:
            entry: The reflection entry with state_verified dict
            actual_state: Current actual state values

        Returns:
            Dict mapping keys to pass/fail
        """
        results = {}
        for key, expected in entry.state_verified.items():
            actual = actual_state.get(key)
            # Handle dict comparison
            if isinstance(expected, dict) and isinstance(actual, dict):
                results[key] = self._dict_matches(expected, actual)
            else:
                results[key] = (actual == expected)
        return results

    def _dict_matches(self, expected: Dict, actual: Dict) -> bool:
        """Check if actual dict contains expected key-value pairs."""
        return all(
            key in actual and actual[key] == value
            for key, value in expected.items()
        )

    def get_recent_reflections(
        self,
        n: int = 5,
        task_id: Optional[str] = None,
    ) -> List[ReflectionEntry]:
        """Get N most recent reflection entries, optionally filtered by task."""
        entries = self.log
        if task_id:
            entries = [e for e in entries if e.task_id == task_id]
        return entries[-n:]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize awareness log for storage."""
        return {
            "entries": [
                {
                    "timestamp": e.timestamp,
                    "message_id": e.message_id,
                    "task_id": e.task_id,
                    "prompt": e.prompt,
                    "what_went_well": e.what_went_well,
                    "what_could_improve": e.what_could_improve,
                    "confidence": e.confidence.value,
                    "adjustments_planned": e.adjustments_planned,
                    "state_verified": e.state_verified,
                    "tags": e.tags,
                }
                for e in self.log
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SelfAwarenessLoop":
        """Deserialize from storage."""
        loop = cls()
        for entry_data in data.get("entries", []):
            entry = ReflectionEntry(
                timestamp=entry_data.get("timestamp", datetime.now().isoformat()),
                message_id=entry_data.get("message_id", ""),
                task_id=entry_data.get("task_id", ""),
                prompt=entry_data.get("prompt", ""),
                what_went_well=entry_data.get("what_went_well", ""),
                what_could_improve=entry_data.get("what_could_improve", ""),
                confidence=ConfidenceLevel(entry_data.get("confidence", "medium")),
                adjustments_planned=entry_data.get("adjustments_planned", ""),
                state_verified=entry_data.get("state_verified", {}),
                tags=entry_data.get("tags", []),
            )
            loop.log.append(entry)
        return loop


# =============================================================================
# Integration helpers
# =============================================================================

def pair_inbox_with_awareness(
    inbox_message,  # InboxMessage
    awareness_loop: SelfAwarenessLoop,
) -> str:
    """
    Pair an inbox message with self-awareness reflection.

    Returns the generated reflection prompt.
    """
    if not inbox_message.self_awareness:
        return ""  # No pairing needed

    entry = awareness_loop.create_entry(
        message_id=inbox_message.id,
        task_id=inbox_message.task_id,
        prompt=inbox_message.reflection_prompt
        or "Reflect on your current approach.",
    )

    if inbox_message.check_internal_state:
        entry.state_verified = inbox_message.check_internal_state

    return awareness_loop.generate_reflection_prompt(
        base_prompt=entry.prompt,
        state_checks=inbox_message.check_internal_state,
    )
