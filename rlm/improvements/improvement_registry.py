"""
Improvement Registry for self-improving system.

This module provides the improvement registry that manages
system improvements proposed by agents.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class ImprovementType(Enum):
    """Types of improvements."""

    PROCESS = "process"
    TOOL = "tool"
    ALGORITHM = "algorithm"
    OPTIMIZATION = "optimization"
    FEATURE = "feature"


class ImprovementCategory(Enum):
    """Categories of improvements."""

    EFFICIENCY = "efficiency"
    ACCURACY = "accuracy"
    USABILITY = "usability"
    SECURITY = "security"
    SCALABILITY = "scalability"


class ImprovementStatus(Enum):
    """Status of an improvement."""

    PROPOSED = "proposed"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"
    DEPRECATED = "deprecated"


class ImpactLevel(Enum):
    """Impact level of an improvement."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ApprovalEvent:
    """An approval/rejection event for an improvement."""

    approver: str  # Agent ID, 'system', or 'user'
    timestamp: datetime = field(default_factory=datetime.now)
    action: str = ""  # 'approved', 'rejected', 'commented'
    comment: Optional[str] = None


@dataclass
class ImprovementTestResults:
    """Test results for an improvement."""

    automated_tests_passed: int = 0
    automated_tests_total: int = 0
    manual_tests_passed: int = 0
    manual_tests_total: int = 0
    performance_impact: Dict[str, Any] = field(default_factory=dict)
    stability: str = "stable"  # 'stable', 'needs-monitoring', 'unstable'


@dataclass
class ImprovementImplementation:
    """Implementation details for an improvement."""

    type: str = ""  # 'code-change', 'configuration', 'new-tool', 'process-change'
    target: str = ""  # Which system component to improve
    changes: List[Any] = field(default_factory=list)
    rollback_plan: Optional[Any] = None


@dataclass
class ImprovementEntity:
    """
    An improvement proposed by an agent.

    Improvements can be process changes, new tools, algorithm updates,
    or any other type of system enhancement.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    type: ImprovementType = ImprovementType.PROCESS
    category: ImprovementCategory = ImprovementCategory.EFFICIENCY
    implementation: ImprovementImplementation = field(
        default_factory=ImprovementImplementation
    )
    creator: str = ""  # Agent ID that proposed the improvement
    created_at: datetime = field(default_factory=datetime.now)
    applied_at: Optional[datetime] = None
    status: ImprovementStatus = ImprovementStatus.PROPOSED
    impact: ImpactLevel = ImpactLevel.MEDIUM
    dependencies: List[str] = field(default_factory=list)  # IDs of other improvements
    affected_components: List[str] = field(default_factory=list)
    test_results: Optional[ImprovementTestResults] = None
    approval_history: List[ApprovalEvent] = field(default_factory=list)
    version: str = "1.0"
    votes_for: int = 0
    votes_against: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type.value,
            "category": self.category.value,
            "implementation": {
                "type": self.implementation.type,
                "target": self.implementation.target,
                "changes": self.implementation.changes,
            },
            "creator": self.creator,
            "created_at": self.created_at.isoformat(),
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
            "status": self.status.value,
            "impact": self.impact.value,
            "dependencies": self.dependencies,
            "affected_components": self.affected_components,
            "test_results": self.test_results.__dict__ if self.test_results else None,
            "approval_history": [
                {
                    "approver": e.approver,
                    "timestamp": e.timestamp.isoformat(),
                    "action": e.action,
                    "comment": e.comment,
                }
                for e in self.approval_history
            ],
            "version": self.version,
            "votes_for": self.votes_for,
            "votes_against": self.votes_against,
        }


class ImprovementRegistry:
    """
    Registry for managing system improvements.

    The registry tracks improvements proposed by agents,
    their approval status, and implementation state.
    """

    def __init__(self):
        """Initialize the improvement registry."""
        self._improvements: Dict[str, ImprovementEntity] = {}
        self._pending_approvals: List[str] = []
        self._active_improvements: List[str] = []
        self._history: List[str] = []
        self._applied_improvements: List[str] = []

    def propose(self, improvement: ImprovementEntity) -> bool:
        """
        Propose a new improvement.

        Args:
            improvement: The improvement to propose.

        Returns:
            True if proposed successfully.
        """
        if not self._validate_improvement(improvement):
            return False

        self._improvements[improvement.id] = improvement
        self._pending_approvals.append(improvement.id)
        self._history.append(improvement.id)

        return True

    def approve(
        self, improvement_id: str, approver: str, comment: Optional[str] = None
    ) -> bool:
        """
        Approve an improvement.

        Args:
            improvement_id: ID of the improvement.
            approver: ID of the approver.
            comment: Optional comment.

        Returns:
            True if approved successfully.
        """
        improvement = self._improvements.get(improvement_id)
        if not improvement:
            return False

        improvement.status = ImprovementStatus.APPROVED
        improvement.approval_history.append(
            ApprovalEvent(
                approver=approver,
                action="approved",
                comment=comment,
            )
        )

        if improvement_id in self._pending_approvals:
            self._pending_approvals.remove(improvement_id)

        return True

    def reject(
        self, improvement_id: str, rejector: str, comment: Optional[str] = None
    ) -> bool:
        """
        Reject an improvement.

        Args:
            improvement_id: ID of the improvement.
            rejector: ID of the rejector.
            comment: Optional comment.

        Returns:
            True if rejected successfully.
        """
        improvement = self._improvements.get(improvement_id)
        if not improvement:
            return False

        improvement.status = ImprovementStatus.REJECTED
        improvement.approval_history.append(
            ApprovalEvent(
                approver=rejector,
                action="rejected",
                comment=comment,
            )
        )

        if improvement_id in self._pending_approvals:
            self._pending_approvals.remove(improvement_id)

        return True

    def apply(self, improvement_id: str) -> bool:
        """
        Mark an improvement as applied.

        Args:
            improvement_id: ID of the improvement.

        Returns:
            True if applied successfully.
        """
        improvement = self._improvements.get(improvement_id)
        if not improvement:
            return False

        if improvement.status != ImprovementStatus.APPROVED:
            return False

        improvement.status = ImprovementStatus.APPLIED
        improvement.applied_at = datetime.now()

        self._applied_improvements.append(improvement_id)
        if improvement_id not in self._active_improvements:
            self._active_improvements.append(improvement_id)

        return True

    def deprecate(self, improvement_id: str, deprecated_by: str, reason: str) -> bool:
        """
        Deprecate an applied improvement.

        Args:
            improvement_id: ID of the improvement.
            deprecated_by: ID of the deprecator.
            reason: Reason for deprecation.

        Returns:
            True if deprecated successfully.
        """
        improvement = self._improvements.get(improvement_id)
        if not improvement:
            return False

        improvement.status = ImprovementStatus.DEPRECATED
        improvement.approval_history.append(
            ApprovalEvent(
                approver=deprecated_by,
                action="deprecated",
                comment=reason,
            )
        )

        if improvement_id in self._active_improvements:
            self._active_improvements.remove(improvement_id)

        return True

    def vote(self, improvement_id: str, voter: str, vote_for: bool) -> bool:
        """
        Vote on an improvement.

        Args:
            improvement_id: ID of the improvement.
            voter: ID of the voter.
            vote_for: True if voting for, False if against.

        Returns:
            True if vote recorded.
        """
        improvement = self._improvements.get(improvement_id)
        if not improvement:
            return False

        if vote_for:
            improvement.votes_for += 1
        else:
            improvement.votes_against += 1

        return True

    def get(self, improvement_id: str) -> Optional[ImprovementEntity]:
        """
        Get an improvement by ID.

        Args:
            improvement_id: ID of the improvement.

        Returns:
            The improvement or None.
        """
        return self._improvements.get(improvement_id)

    def get_all(self) -> List[ImprovementEntity]:
        """Get all improvements."""
        return list(self._improvements.values())

    def get_pending(self) -> List[ImprovementEntity]:
        """Get improvements pending approval."""
        return [
            self._improvements[iid]
            for iid in self._pending_approvals
            if iid in self._improvements
        ]

    def get_active(self) -> List[ImprovementEntity]:
        """Get active (applied) improvements."""
        return [
            self._improvements[iid]
            for iid in self._active_improvements
            if iid in self._improvements
        ]

    def get_by_category(self, category: ImprovementCategory) -> List[ImprovementEntity]:
        """Get improvements by category."""
        return [imp for imp in self._improvements.values() if imp.category == category]

    def get_by_status(self, status: ImprovementStatus) -> List[ImprovementEntity]:
        """Get improvements by status."""
        return [imp for imp in self._improvements.values() if imp.status == status]

    def get_by_creator(self, creator_id: str) -> List[ImprovementEntity]:
        """Get improvements by creator."""
        return [imp for imp in self._improvements.values() if imp.creator == creator_id]

    def _validate_improvement(self, improvement: ImprovementEntity) -> bool:
        """Validate an improvement before accepting."""
        if not improvement.title:
            return False
        if not improvement.description:
            return False
        if not improvement.creator:
            return False
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        return {
            "total": len(self._improvements),
            "pending": len(self._pending_approvals),
            "active": len(self._active_improvements),
            "applied": len(self._applied_improvements),
            "by_category": {
                cat.value: len(self.get_by_category(cat)) for cat in ImprovementCategory
            },
            "by_status": {
                status.value: len(self.get_by_status(status))
                for status in ImprovementStatus
            },
        }
