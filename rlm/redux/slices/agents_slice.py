"""
Redux slice for agents state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    TERMINATED = "terminated"


class InterventionActionType(Enum):
    PAUSE = "pause"
    RESUME = "resume"
    TERMINATE = "terminate"
    EMERGENCY_STOP = "emergency_stop"


@dataclass
class AgentEntity:
    agent_id: str
    name: str
    status: AgentStatus = AgentStatus.IDLE
    group_id: Optional[str] = None
    created_at: float = 0.0
    last_activity: float = 0.0
    current_task_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InterventionRecord:
    action_id: str
    action_type: InterventionActionType
    target_type: str
    target_id: Optional[str]
    timestamp: float
    undone: bool = False


@dataclass
class AgentsState:
    agents: Dict[str, AgentEntity] = field(default_factory=dict)
    paused_agents: List[str] = field(default_factory=list)
    paused_groups: List[str] = field(default_factory=list)
    paused_types: List[str] = field(default_factory=list)
    all_paused: bool = False
    last_action: Optional[InterventionRecord] = None
    timeline: List[InterventionRecord] = field(default_factory=list)


class AgentsActions:
    @staticmethod
    def pause_agent(target: str, target_id: Optional[str] = None, duration: Optional[int] = None) -> dict:
        return {"type": "agents/pause_agent", "payload": {"target": target, "target_id": target_id, "duration": duration}}

    @staticmethod
    def resume_agent(target: str, target_id: Optional[str] = None) -> dict:
        return {"type": "agents/resume_agent", "payload": {"target": target, "target_id": target_id}}

    @staticmethod
    def terminate_agent(agent_id: str, force: bool = False) -> dict:
        return {"type": "agents/terminate_agent", "payload": {"agent_id": agent_id, "force": force}}

    @staticmethod
    def emergency_stop() -> dict:
        return {"type": "agents/emergency_stop"}

    @staticmethod
    def undo_last_action() -> dict:
        return {"type": "agents/undo"}

    @staticmethod
    def add_agent(agent: AgentEntity) -> dict:
        return {"type": "agents/add_agent", "payload": agent}

    @staticmethod
    def update_agent_status(agent_id: str, status: AgentStatus) -> dict:
        return {"type": "agents/update_status", "payload": {"agent_id": agent_id, "status": status.value}}


def agents_reducer(state: AgentsState, action: dict) -> AgentsState:
    action_type = action.get("type")

    if action_type == "agents/pause_agent":
        payload = action.get("payload", {})
        target = payload.get("target")
        target_id = payload.get("target_id")
        new_paused_agents = state.paused_agents.copy()
        new_paused_groups = state.paused_groups.copy()
        new_paused_types = state.paused_types.copy()
        new_all_paused = state.all_paused
        new_agents = state.agents.copy()

        if target == "all":
            new_all_paused = True
            for ag in new_agents.values():
                ag.status = AgentStatus.PAUSED
                if ag.agent_id not in new_paused_agents:
                    new_paused_agents.append(ag.agent_id)
        elif target == "group" and target_id:
            new_paused_groups.append(target_id)
            for ag in new_agents.values():
                if ag.group_id == target_id and ag.agent_id not in new_paused_agents:
                    new_paused_agents.append(ag.agent_id)
                    ag.status = AgentStatus.PAUSED
        elif target == "individual" and target_id:
            if target_id not in new_paused_agents:
                new_paused_agents.append(target_id)
            if target_id in new_agents:
                new_agents[target_id].status = AgentStatus.PAUSED
        elif target == "type" and target_id:
            new_paused_types.append(target_id)

        last_action = InterventionRecord(
            action_id=f"pause-{target}-{target_id or 'all'}",
            action_type=InterventionActionType.PAUSE,
            target_type=target,
            target_id=target_id,
            timestamp=payload.get("timestamp", 0.0)
        )
        new_timeline = state.timeline.copy()
        new_timeline.append(last_action)

        return AgentsState(
            agents=new_agents,
            paused_agents=new_paused_agents,
            paused_groups=new_paused_groups,
            paused_types=new_paused_types,
            all_paused=new_all_paused,
            last_action=last_action,
            timeline=new_timeline
        )

    elif action_type == "agents/resume_agent":
        payload = action.get("payload", {})
        target = payload.get("target")
        target_id = payload.get("target_id")
        new_paused_agents = state.paused_agents.copy()
        new_paused_groups = state.paused_groups.copy()
        new_paused_types = state.paused_types.copy()
        new_all_paused = state.all_paused
        new_agents = state.agents.copy()

        if target == "all":
            new_all_paused = False
            new_paused_agents = []
            new_paused_groups = []
            new_paused_types = []
            for ag in new_agents.values():
                if ag.status == AgentStatus.PAUSED:
                    ag.status = AgentStatus.IDLE
        elif target == "group" and target_id:
            new_paused_groups = [g for g in new_paused_groups if g != target_id]
            for ag in new_agents.values():
                if ag.group_id == target_id and ag.agent_id in new_paused_agents:
                    new_paused_agents.remove(ag.agent_id)
                    ag.status = AgentStatus.IDLE
        elif target == "individual" and target_id:
            if target_id in new_paused_agents:
                new_paused_agents.remove(target_id)
            if target_id in new_agents:
                new_agents[target_id].status = AgentStatus.IDLE
        elif target == "type" and target_id:
            new_paused_types = [t for t in new_paused_types if t != target_id]

        last_action = InterventionRecord(
            action_id=f"resume-{target}-{target_id or 'all'}",
            action_type=InterventionActionType.RESUME,
            target_type=target,
            target_id=target_id,
            timestamp=payload.get("timestamp", 0.0)
        )
        new_timeline = state.timeline.copy()
        new_timeline.append(last_action)

        return AgentsState(
            agents=new_agents,
            paused_agents=new_paused_agents,
            paused_groups=new_paused_groups,
            paused_types=new_paused_types,
            all_paused=new_all_paused,
            last_action=last_action,
            timeline=new_timeline
        )

    elif action_type == "agents/terminate_agent":
        payload = action.get("payload", {})
        agent_id = payload.get("agent_id")
        new_agents = state.agents.copy()
        new_paused_agents = state.paused_agents.copy()
        if agent_id in new_agents:
            new_agents[agent_id].status = AgentStatus.TERMINATED
            if agent_id in new_paused_agents:
                new_paused_agents.remove(agent_id)

        last_action = InterventionRecord(
            action_id=f"terminate-{agent_id}",
            action_type=InterventionActionType.TERMINATE,
            target_type="individual",
            target_id=agent_id,
            timestamp=payload.get("timestamp", 0.0)
        )
        new_timeline = state.timeline.copy()
        new_timeline.append(last_action)

        return AgentsState(
            agents=new_agents,
            paused_agents=new_paused_agents,
            paused_groups=state.paused_groups,
            paused_types=state.paused_types,
            all_paused=state.all_paused,
            last_action=last_action,
            timeline=new_timeline
        )

    elif action_type == "agents/emergency_stop":
        new_agents = state.agents.copy()
        new_paused_agents = []
        for ag in new_agents.values():
            ag.status = AgentStatus.PAUSED
            new_paused_agents.append(ag.agent_id)

        payload = action.get("payload", {})
        last_action = InterventionRecord(
            action_id="emergency-stop-all",
            action_type=InterventionActionType.EMERGENCY_STOP,
            target_type="all",
            target_id=None,
            timestamp=payload.get("timestamp", 0.0)
        )
        new_timeline = state.timeline.copy()
        new_timeline.append(last_action)

        return AgentsState(
            agents=new_agents,
            paused_agents=new_paused_agents,
            paused_groups=state.paused_groups,
            paused_types=state.paused_types,
            all_paused=True,
            last_action=last_action,
            timeline=new_timeline
        )

    elif action_type == "agents/undo":
        if not state.timeline:
            return state
        last_record = state.timeline[-1]
        if last_record.undone:
            return state
        last_record.undone = True
        if last_record.action_type == InterventionActionType.PAUSE:
            target = last_record.target_type
            target_id = last_record.target_id
            new_agents = state.agents.copy()
            new_paused_agents = state.paused_agents.copy()
            if target == "all":
                for ag in new_agents.values():
                    ag.status = AgentStatus.IDLE
                new_paused_agents = []
            elif target == "individual" and target_id:
                if target_id in new_paused_agents:
                    new_paused_agents.remove(target_id)
                if target_id in new_agents:
                    new_agents[target_id].status = AgentStatus.IDLE
            return AgentsState(
                agents=new_agents,
                paused_agents=new_paused_agents,
                paused_groups=state.paused_groups,
                paused_types=state.paused_types,
                all_paused=False,
                last_action=None,
                timeline=state.timeline
            )
        return state

    elif action_type == "agents/add_agent":
        new_agents = state.agents.copy()
        agent: Any = action.get("payload")
        if agent is None:
            return state
        new_agents[agent.agent_id] = agent
        return AgentsState(
            agents=new_agents,
            paused_agents=state.paused_agents,
            paused_groups=state.paused_groups,
            paused_types=state.paused_types,
            all_paused=state.all_paused,
            last_action=state.last_action,
            timeline=state.timeline
        )

    elif action_type == "agents/update_status":
        payload = action.get("payload", {})
        agent_id = payload.get("agent_id")
        status_str = payload.get("status")
        new_agents = state.agents.copy()
        if agent_id in new_agents:
            new_agents[agent_id].status = AgentStatus(status_str)
        return AgentsState(
            agents=new_agents,
            paused_agents=state.paused_agents,
            paused_groups=state.paused_groups,
            paused_types=state.paused_types,
            all_paused=state.all_paused,
            last_action=state.last_action,
            timeline=state.timeline
        )

    return state
