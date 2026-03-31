"use client";

import React, { useState } from "react";
import { useAgentLoopStore } from '@/store/agent-loop-store';

interface REPLHistoryProps {
  agentId: string;
  executions?: any[];
}

export const REPLHistory: React.FC<REPLHistoryProps> = ({ agentId, executions = [] }) => {
  const [filter, setFilter] = useState<"all" | "success" | "error">("all");
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const agents = useAgentLoopStore((s) => s.agents);
  const agent = agentId ? agents?.[agentId] : null;
  const replHistory = agent?.repl_history || executions;

  const filtered = replHistory.filter((e: any) => {
    if (filter === "all") return true;
    if (filter === "success") return e.success;
    if (filter === "error") return !e.success;
    return true;
  });

  return (
    <div className="repl-history">
      <div className="repl-history-header">
        <h3>REPL Executions ({filtered.length})</h3>
        <div className="filter-buttons">
          <button
            className={filter === "all" ? "active" : ""}
            onClick={() => setFilter("all")}
          >
            All
          </button>
          <button
            className={filter === "success" ? "active" : ""}
            onClick={() => setFilter("success")}
          >
            Success
          </button>
          <button
            className={filter === "error" ? "active" : ""}
            onClick={() => setFilter("error")}
          >
            Failed
          </button>
        </div>
      </div>

      <div className="repl-list">
        {filtered.length === 0 ? (
          <div className="empty-state">
            <p>No REPL executions recorded</p>
          </div>
        ) : (
          filtered.map((exec: any) => (
            <div
              key={exec.execution_id}
              className={`repl-item ${exec.success ? "success" : "error"}`}
            >
              <div
                className="repl-item-header"
                onClick={() =>
                  setExpandedId(expandedId === exec.execution_id ? null : exec.execution_id)
                }
              >
                <span className="exec-id">{exec.execution_id.slice(0, 8)}</span>
                <span className="exec-time">{exec.execution_time?.toFixed(3) || 0}s</span>
                <span className={`status ${exec.success ? "text-status-verified" : "text-status-failed"}`}>
                  {exec.success ? "✓" : "✗"}
                </span>
                <span className="expand-icon">
                  {expandedId === exec.execution_id ? "▼" : "▶"}
                </span>
              </div>

              {expandedId === exec.execution_id && (
                <div className="repl-item-content">
                  <div className="repl-code">
                    <label>CODE:</label>
                    <pre className="code-block">{exec.code || "(empty)"}</pre>
                  </div>

                  {exec.stdout && (
                    <div className="repl-stdout">
                      <label>stdout:</label>
                      <pre className="code-block text-status-verified">{exec.stdout}</pre>
                    </div>
                  )}

                  {exec.stderr && (
                    <div className="repl-stderr">
                      <label>stderr:</label>
                      <pre className="code-block text-status-failed">{exec.stderr}</pre>
                    </div>
                  )}

                  {exec.return_value_preview && (
                    <div className="repl-return">
                      <label>Return:</label>
                      <pre className="code-block">{exec.return_value_preview}</pre>
                    </div>
                  )}

                  {exec.llm_calls_made?.length > 0 && (
                    <div className="repl-llm-calls">
                      <label>LLM calls within:</label>
                      <span>{exec.llm_calls_made.length} nested calls</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default REPLHistory;
