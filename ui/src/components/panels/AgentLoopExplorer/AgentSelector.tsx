"use client";

import React from "react";
import { useAgentLoopStore } from '@/store/agent-loop-store';

interface AgentSelectorProps {
  agents: Record<string, any>;
  selectedId: string | null;
  onSelect: (id: string | null) => void;
}

export const AgentSelector: React.FC<AgentSelectorProps> = ({
  agents,
  selectedId,
  onSelect,
}) => {
  const agentList = Object.values(agents || {});

  const getStatusColor = (status: string) => {
    switch (status?.toUpperCase()) {
      case "RUNNING":
        return "bg-status-running";
      case "IDLE":
        return "bg-status-idle";
      case "PAUSED":
        return "bg-status-paused";
      case "COMPLETED":
        return "bg-status-verified";
      case "FAILED":
        return "bg-status-failed";
      default:
        return "bg-muted-foreground";
    }
  };

  return (
    <div className="agent-selector">
      <select
        value={selectedId || ""}
        onChange={(e) => onSelect(e.target.value || null)}
        className="agent-select"
      >
        <option value="">Select an agent...</option>
        {agentList.map((agent) => (
          <option key={agent.agent_id} value={agent.agent_id}>
            {agent.agent_name || agent.agent_id} ({agent.status}) - Depth{" "}
            {agent.depth}
          </option>
        ))}
      </select>

      {selectedId && agents[selectedId] && (
        <div className="agent-preview">
          <div className="agent-preview-header">
            <span
              className={`status-dot ${getStatusColor(agents[selectedId].status)}`}
            />
            <span className="agent-name">
              {agents[selectedId].agent_name || selectedId}
            </span>
          </div>
          <div className="agent-preview-stats">
            <span>Iterations: {agents[selectedId].iterations?.length || 0}</span>
            <span>LLM Calls: {agents[selectedId].llm_calls?.length || 0}</span>
            <span>
              REPLs: {agents[selectedId].repl_history?.length || 0}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default AgentSelector;
