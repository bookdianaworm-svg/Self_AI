"""
Redux slice for improvements state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ImprovementStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"
    ROLLED_BACK = "rolled_back"


@dataclass
class ImprovementEntity:
    improvement_id: str
    title: str
    description: str
    category: str
    created_by: str
    created_at: float
    status: ImprovementStatus = ImprovementStatus.PENDING
    diff_view: Optional[str] = None
    impact_analysis: Optional[Dict[str, Any]] = None
    dependencies: List[str] = field(default_factory=list)
    test_results: Optional[Dict[str, Any]] = None
    rejection_reason: Optional[str] = None


@dataclass
class ImprovementDefaults:
    action: str = "ask"
    category: Optional[str] = None


@dataclass
class ImprovementsState:
    pending_approvals: List[ImprovementEntity] = field(default_factory=list)
    active_improvements: List[str] = field(default_factory=list)
    applied_improvements: Dict[str, ImprovementEntity] = field(default_factory=dict)
    rolled_back_improvements: Dict[str, ImprovementEntity] = field(default_factory=dict)
    defaults: Dict[str, ImprovementDefaults] = field(default_factory=dict)


class ImprovementsActions:
    @staticmethod
    def approve_improvement(improvement_id: str, apply_now: bool = False) -> dict:
        return {"type": "improvements/approve_improvement", "payload": {"improvement_id": improvement_id, "apply_now": apply_now}}

    @staticmethod
    def reject_improvement(improvement_id: str, reason: str) -> dict:
        return {"type": "improvements/reject_improvement", "payload": {"improvement_id": improvement_id, "reason": reason}}

    @staticmethod
    def rollback_improvement(improvement_id: str) -> dict:
        return {"type": "improvements/rollback_improvement", "payload": {"improvement_id": improvement_id}}

    @staticmethod
    def set_default(category: str, action: str) -> dict:
        return {"type": "improvements/set_default", "payload": {"category": category, "action": action}}

    @staticmethod
    def add_improvement(improvement: ImprovementEntity) -> dict:
        return {"type": "improvements/add_improvement", "payload": improvement}


def improvements_reducer(state: ImprovementsState, action: dict) -> ImprovementsState:
    action_type = action.get("type")

    if action_type == "improvements/approve_improvement":
        payload = action.get("payload", {})
        improvement_id = payload.get("improvement_id")
        apply_now = payload.get("apply_now", False)
        new_pending = [i for i in state.pending_approvals if i.improvement_id != improvement_id]
        new_active = state.active_improvements.copy()
        new_applied = state.applied_improvements.copy()
        for imp in state.pending_approvals:
            if imp.improvement_id == improvement_id:
                imp.status = ImprovementStatus.APPROVED if not apply_now else ImprovementStatus.APPLIED
                if apply_now:
                    new_active.append(improvement_id)
                    new_applied[improvement_id] = imp
                break
        return ImprovementsState(
            pending_approvals=new_pending,
            active_improvements=new_active,
            applied_improvements=new_applied,
            rolled_back_improvements=state.rolled_back_improvements,
            defaults=state.defaults
        )

    elif action_type == "improvements/reject_improvement":
        payload = action.get("payload", {})
        improvement_id = payload.get("improvement_id")
        reason = payload.get("reason")
        new_pending = [i for i in state.pending_approvals if i.improvement_id != improvement_id]
        new_applied = state.applied_improvements.copy()
        for imp in state.pending_approvals:
            if imp.improvement_id == improvement_id:
                imp.status = ImprovementStatus.REJECTED
                imp.rejection_reason = reason
                new_applied[improvement_id] = imp
                break
        return ImprovementsState(
            pending_approvals=new_pending,
            active_improvements=state.active_improvements,
            applied_improvements=new_applied,
            rolled_back_improvements=state.rolled_back_improvements,
            defaults=state.defaults
        )

    elif action_type == "improvements/rollback_improvement":
        payload = action.get("payload", {})
        improvement_id = payload.get("improvement_id")
        new_active = [i for i in state.active_improvements if i != improvement_id]
        new_rolled_back = state.rolled_back_improvements.copy()
        new_applied = state.applied_improvements.copy()
        if improvement_id in new_applied:
            imp = new_applied[improvement_id]
            imp.status = ImprovementStatus.ROLLED_BACK
            new_rolled_back[improvement_id] = imp
            del new_applied[improvement_id]
        return ImprovementsState(
            pending_approvals=state.pending_approvals,
            active_improvements=new_active,
            applied_improvements=new_applied,
            rolled_back_improvements=new_rolled_back,
            defaults=state.defaults
        )

    elif action_type == "improvements/set_default":
        payload = action.get("payload", {})
        category = payload.get("category")
        action_str = payload.get("action")
        new_defaults = state.defaults.copy()
        new_defaults[category] = ImprovementDefaults(action=action_str, category=category)
        return ImprovementsState(
            pending_approvals=state.pending_approvals,
            active_improvements=state.active_improvements,
            applied_improvements=state.applied_improvements,
            rolled_back_improvements=state.rolled_back_improvements,
            defaults=new_defaults
        )

    elif action_type == "improvements/add_improvement":
        new_pending = state.pending_approvals.copy()
        new_improvement: Any = action.get("payload")
        if new_improvement is not None:
            new_pending.append(new_improvement)
        return ImprovementsState(
            pending_approvals=new_pending,
            active_improvements=state.active_improvements,
            applied_improvements=state.applied_improvements,
            rolled_back_improvements=state.rolled_back_improvements,
            defaults=state.defaults
        )

    return state
