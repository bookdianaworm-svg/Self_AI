"""
Tests for ImprovementRegistry class.
"""

import pytest

from rlm.improvements.improvement_registry import (
    ImprovementRegistry,
    ImprovementEntity,
    ImprovementType,
    ImprovementCategory,
    ImprovementStatus,
    ImpactLevel,
)


class TestImprovementRegistry:
    """Test suite for ImprovementRegistry class."""

    def test_register_improvement(self):
        """Test registering a new improvement."""
        registry = ImprovementRegistry()
        improvement = ImprovementEntity(
            title="Test Improvement",
            description="A test improvement",
            creator="test_agent",
        )

        result = registry.propose(improvement)

        assert result is True
        assert registry.get(improvement.id) is not None

    def test_get_improvement(self):
        """Test retrieving an improvement by ID."""
        registry = ImprovementRegistry()
        improvement = ImprovementEntity(
            title="Get Test",
            description="Testing get method",
            creator="agent_1",
        )
        registry.propose(improvement)

        retrieved = registry.get(improvement.id)

        assert retrieved is not None
        assert retrieved.title == "Get Test"

    def test_list_improvements(self):
        """Test listing all improvements."""
        registry = ImprovementRegistry()

        imp1 = ImprovementEntity(title="First", description="First desc", creator="a")
        imp2 = ImprovementEntity(title="Second", description="Second desc", creator="b")

        registry.propose(imp1)
        registry.propose(imp2)

        all_improvements = registry.get_all()

        assert len(all_improvements) == 2

    def test_improvement_scoring(self):
        """Test that improvements can be scored with votes."""
        registry = ImprovementRegistry()
        improvement = ImprovementEntity(
            title="Score Test",
            description="Testing scoring",
            creator="agent_1",
        )
        registry.propose(improvement)

        registry.vote(improvement.id, "voter_1", True)
        registry.vote(improvement.id, "voter_2", True)
        registry.vote(improvement.id, "voter_3", False)

        retrieved = registry.get(improvement.id)
        assert retrieved.votes_for == 2
        assert retrieved.votes_against == 1

    def test_best_improvement(self):
        """Test getting improvements by voting score."""
        registry = ImprovementRegistry()

        imp_low = ImprovementEntity(title="Low Score", description="Low", creator="a")
        imp_high = ImprovementEntity(
            title="High Score", description="High", creator="b"
        )
        imp_medium = ImprovementEntity(
            title="Medium Score", description="Medium", creator="c"
        )

        registry.propose(imp_low)
        registry.propose(imp_high)
        registry.propose(imp_medium)

        registry.vote(imp_low.id, "v1", False)
        registry.vote(imp_high.id, "v1", True)
        registry.vote(imp_high.id, "v2", True)
        registry.vote(imp_high.id, "v3", True)
        registry.vote(imp_medium.id, "v1", True)
        registry.vote(imp_medium.id, "v2", False)

        all_improvements = registry.get_all()
        sorted_by_score = sorted(
            all_improvements, key=lambda i: i.votes_for - i.votes_against, reverse=True
        )

        assert sorted_by_score[0].title == "High Score"
        assert sorted_by_score[1].title == "Medium Score"
        assert sorted_by_score[2].title == "Low Score"

    def test_approve_improvement(self):
        """Test approving an improvement."""
        registry = ImprovementRegistry()
        improvement = ImprovementEntity(
            title="Approve Test",
            description="Testing approval",
            creator="agent_1",
        )
        registry.propose(improvement)

        result = registry.approve(improvement.id, "approver_1", "Looks good")

        assert result is True
        retrieved = registry.get(improvement.id)
        assert retrieved.status == ImprovementStatus.APPROVED
        assert len(retrieved.approval_history) == 1
        assert retrieved.approval_history[0].action == "approved"

    def test_reject_improvement(self):
        """Test rejecting an improvement."""
        registry = ImprovementRegistry()
        improvement = ImprovementEntity(
            title="Reject Test",
            description="Testing rejection",
            creator="agent_1",
        )
        registry.propose(improvement)

        result = registry.reject(improvement.id, "rejector_1", "Not ready")

        assert result is True
        retrieved = registry.get(improvement.id)
        assert retrieved.status == ImprovementStatus.REJECTED

    def test_apply_improvement(self):
        """Test applying an approved improvement."""
        registry = ImprovementRegistry()
        improvement = ImprovementEntity(
            title="Apply Test",
            description="Testing apply",
            creator="agent_1",
        )
        registry.propose(improvement)
        registry.approve(improvement.id, "approver")

        result = registry.apply(improvement.id)

        assert result is True
        retrieved = registry.get(improvement.id)
        assert retrieved.status == ImprovementStatus.APPLIED
        assert retrieved.applied_at is not None

    def test_deprecate_improvement(self):
        """Test deprecating an applied improvement."""
        registry = ImprovementRegistry()
        improvement = ImprovementEntity(
            title="Deprecate Test",
            description="Testing deprecation",
            creator="agent_1",
        )
        registry.propose(improvement)
        registry.approve(improvement.id, "approver")
        registry.apply(improvement.id)

        result = registry.deprecate(improvement.id, "deprecator", "Outdated")

        assert result is True
        retrieved = registry.get(improvement.id)
        assert retrieved.status == ImprovementStatus.DEPRECATED

    def test_get_pending(self):
        """Test getting pending improvements."""
        registry = ImprovementRegistry()

        imp1 = ImprovementEntity(title="Pending 1", description="P1", creator="a")
        imp2 = ImprovementEntity(title="Pending 2", description="P2", creator="b")

        registry.propose(imp1)
        registry.propose(imp2)

        pending = registry.get_pending()

        assert len(pending) == 2

    def test_get_active(self):
        """Test getting active (applied) improvements."""
        registry = ImprovementRegistry()

        imp1 = ImprovementEntity(title="Active 1", description="A1", creator="a")
        imp2 = ImprovementEntity(title="Active 2", description="A2", creator="b")

        registry.propose(imp1)
        registry.approve(imp1.id, "approver")
        registry.apply(imp1.id)

        registry.propose(imp2)

        active = registry.get_active()

        assert len(active) == 1
        assert active[0].title == "Active 1"

    def test_get_by_category(self):
        """Test getting improvements by category."""
        registry = ImprovementRegistry()

        imp1 = ImprovementEntity(
            title="Efficiency",
            description="E",
            creator="a",
            category=ImprovementCategory.EFFICIENCY,
        )
        imp2 = ImprovementEntity(
            title="Security",
            description="S",
            creator="b",
            category=ImprovementCategory.SECURITY,
        )

        registry.propose(imp1)
        registry.propose(imp2)

        efficiency_improvements = registry.get_by_category(
            ImprovementCategory.EFFICIENCY
        )

        assert len(efficiency_improvements) == 1
        assert efficiency_improvements[0].title == "Efficiency"

    def test_get_by_status(self):
        """Test getting improvements by status."""
        registry = ImprovementRegistry()

        imp1 = ImprovementEntity(title="Pending", description="P", creator="a")
        imp2 = ImprovementEntity(title="Approved", description="A", creator="b")

        registry.propose(imp1)
        registry.propose(imp2)
        registry.approve(imp2.id, "approver")

        pending = registry.get_by_status(ImprovementStatus.PROPOSED)
        approved = registry.get_by_status(ImprovementStatus.APPROVED)

        assert len(pending) == 1
        assert len(approved) == 1

    def test_get_by_creator(self):
        """Test getting improvements by creator."""
        registry = ImprovementRegistry()

        imp1 = ImprovementEntity(title="By A", description="A", creator="agent_a")
        imp2 = ImprovementEntity(title="By B", description="B", creator="agent_b")

        registry.propose(imp1)
        registry.propose(imp2)

        from_agent_a = registry.get_by_creator("agent_a")

        assert len(from_agent_a) == 1
        assert from_agent_a[0].title == "By A"

    def test_validation_rejects_empty_title(self):
        """Test that improvements without title are rejected."""
        registry = ImprovementRegistry()
        improvement = ImprovementEntity(
            title="",
            description="Has description but no title",
            creator="agent_1",
        )

        result = registry.propose(improvement)

        assert result is False

    def test_validation_rejects_empty_description(self):
        """Test that improvements without description are rejected."""
        registry = ImprovementRegistry()
        improvement = ImprovementEntity(
            title="Has title",
            description="",
            creator="agent_1",
        )

        result = registry.propose(improvement)

        assert result is False

    def test_validation_rejects_empty_creator(self):
        """Test that improvements without creator are rejected."""
        registry = ImprovementRegistry()
        improvement = ImprovementEntity(
            title="Valid title",
            description="Valid description",
            creator="",
        )

        result = registry.propose(improvement)

        assert result is False

    def test_get_stats(self):
        """Test getting registry statistics."""
        registry = ImprovementRegistry()

        imp1 = ImprovementEntity(title="Stats 1", description="S1", creator="a")
        imp2 = ImprovementEntity(title="Stats 2", description="S2", creator="b")

        registry.propose(imp1)
        registry.propose(imp2)

        stats = registry.get_stats()

        assert stats["total"] == 2
        assert stats["pending"] == 2
        assert "by_category" in stats
        assert "by_status" in stats
