"use client";

import React, { useState, useEffect } from "react";
import { useAgentLoopStore } from '@/store/agent-loop-store';
import { useConsoleStore } from '@/store/console-store';
import { wsClient } from '@/lib/websocket';
import { AgentSelector } from "./AgentSelector";
import { LLMSnapshot } from "./LLMSnapshot";
import { REPLHistory } from "./REPLHistory";
import { ChainOfThoughtViewer } from "./ChainOfThoughtViewer";

type ViewMode = "live" | "history";

export const AgentLoopExplorer: React.FC = () => {
  const agentLoop = useAgentLoopStore();
  const consoleAgents = useConsoleStore((s) => s.agents);
  const connected = useConsoleStore((s) => s.connected);
  const { agents, active_agent_id, setActiveAgent, registerAgent } = agentLoop;

  const [viewMode, setViewMode] = useState<ViewMode>("live");
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null);

  // Sync agents from console-store to agent-loop-store when they change
  useEffect(() => {
    Object.entries(consoleAgents).forEach(([agentId, agent]) => {
      if (!agentLoop.agents[agentId]) {
        // Register new agent from console store
        registerAgent(
          agentId,
          agent.name || agent.agent_name || `Agent-${agentId.slice(0, 8)}`,
          agent.depth || 0,
          agent.parent_id || null
        );
      }
    });
  }, [consoleAgents, agentLoop.agents, registerAgent]);

  useEffect(() => {
    if (!selectedAgentId && Object.keys(agents).length > 0) {
      const firstAgentId = Object.keys(agents)[0];
      setSelectedAgentId(firstAgentId);
      setActiveAgent(firstAgentId);
    }
  }, [agents, selectedAgentId, setActiveAgent]);

  const handleAgentSelect = (agentId: string | null) => {
    setSelectedAgentId(agentId);
    setActiveAgent(agentId);
  };

  const handleViewModeChange = (mode: ViewMode) => {
    setViewMode(mode);
  };

  const selectedAgent = selectedAgentId ? agents[selectedAgentId] : null;
  const isActive = selectedAgentId === active_agent_id;

  return (
    <div className="agent-loop-explorer">
      <div className="agent-loop-header">
        <h2>Agent Loop Explorer</h2>
        <div className="connection-status">
          <span className={`status-dot ${connected ? "connected" : "disconnected"}`} />
          {connected ? "Connected" : "Disconnected"}
        </div>
      </div>

      <div className="agent-loop-controls">
        <AgentSelector
          agents={agents}
          selectedId={selectedAgentId}
          onSelect={handleAgentSelect}
        />

        <div className="view-mode-toggle">
          <button
            className={viewMode === "live" ? "active" : ""}
            onClick={() => handleViewModeChange("live")}
          >
            Live
          </button>
          <button
            className={viewMode === "history" ? "active" : ""}
            onClick={() => handleViewModeChange("history")}
          >
            History
          </button>
        </div>
      </div>

      <div className="agent-loop-content">
        {viewMode === "live" ? (
          <>
            <div className="panel llm-snapshot-panel">
              <h3>Current LLM Activity</h3>
              <LLMSnapshot agentId={selectedAgentId} isActive={isActive} />
            </div>

            <div className="panel repl-panel">
              <h3>REPL Executions</h3>
              <REPLHistory agentId={selectedAgentId || ""} />
            </div>

            <div className="panel cot-panel">
              <h3>Chain of Thought</h3>
              <ChainOfThoughtViewer agentId={selectedAgentId || ""} />
            </div>
          </>
        ) : (
          <>
            <div className="panel history-panel">
              <h3>Full History - {selectedAgent?.agent_name || selectedAgentId}</h3>
              <div className="history-stats">
                <div className="stat">
                  <span className="stat-label">Total Iterations</span>
                  <span className="stat-value">
                    {selectedAgent?.iterations?.length || 0}
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Total LLM Calls</span>
                  <span className="stat-value">
                    {selectedAgent?.llm_calls?.length || 0}
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Total REPL Executions</span>
                  <span className="stat-value">
                    {selectedAgent?.repl_history?.length || 0}
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Chain Thought Steps</span>
                  <span className="stat-value">
                    {selectedAgent?.chain_of_thought?.length || 0}
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Spawned Agents</span>
                  <span className="stat-value">
                    {selectedAgent?.spawning_events?.length || 0}
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Successful REPLs</span>
                  <span className="stat-value success">
                    {selectedAgent?.successful_repl_executions || 0}
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Failed REPLs</span>
                  <span className="stat-value error">
                    {selectedAgent?.failed_repl_executions || 0}
                  </span>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {selectedAgentId && (
        <div className="agent-loop-footer">
          <button
            className="btn-secondary"
            onClick={() => {
            }}
          >
            Pause Agent
          </button>
          <button
            className="btn-secondary"
            onClick={() => {
              agentLoop.clearAgentHistory(selectedAgentId);
            }}
          >
            Clear History
          </button>
        </div>
      )}
    </div>
  );
};

export default AgentLoopExplorer;
