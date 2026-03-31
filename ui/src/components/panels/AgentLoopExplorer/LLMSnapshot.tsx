"use client";

import React from "react";
import { useAgentLoopStore } from '@/store/agent-loop-store';

interface LLMSnapshotProps {
  agentId: string | null;
  isActive: boolean;
}

export const LLMSnapshot: React.FC<LLMSnapshotProps> = ({ agentId, isActive }) => {
  const agents = useAgentLoopStore((s) => s.agents);
  const agent = agentId ? agents[agentId] : null;

  const latestCall = agent && agent.llm_calls && agent.llm_calls.length > 0 
    ? agent.llm_calls[agent.llm_calls.length - 1] 
    : null;

  if (!agentId) {
    return (
      <div className="llm-snapshot empty-state">
        <p>Select an agent to view LLM activity</p>
      </div>
    );
  }

  return (
    <div className={`llm-snapshot ${isActive ? "active" : "inactive"}`}>
      <div className="snapshot-header">
        <span className={`status-badge badge-${agent?.status?.toLowerCase() || "unknown"}`}>
          {agent?.status || "UNKNOWN"}
        </span>
        <span className="depth-badge">Depth: {agent?.depth || 0}</span>
      </div>

      {latestCall ? (
        <div className="current-call">
          <div className="call-meta">
            <span className="model">{latestCall.model || "unknown"}</span>
            <span className="tokens">
              {latestCall.input_tokens || 0} → {latestCall.output_tokens || 0} tokens
            </span>
            <span className="time">{latestCall.execution_time?.toFixed(2) || 0}s</span>
            <span className={`success ${latestCall.success ? "text-status-verified" : "text-status-failed"}`}>
              {latestCall.success ? "✓" : "✗"}
            </span>
          </div>

          <div className="call-content">
            <div className="call-prompt">
              <label>PROMPT:</label>
              <pre className="code-block">{latestCall.prompt || "(empty)"}</pre>
            </div>

            <div className="call-response">
              <label>RESPONSE:</label>
              <pre className="code-block">{latestCall.response || "(empty)"}</pre>
            </div>
          </div>

          {latestCall.error && (
            <div className="call-error">
              <label>ERROR:</label>
              <pre className="code-block text-status-failed">{latestCall.error}</pre>
            </div>
          )}
        </div>
      ) : (
        <div className="no-calls">
          <p>No LLM calls yet</p>
        </div>
      )}
    </div>
  );
};

export default LLMSnapshot;
