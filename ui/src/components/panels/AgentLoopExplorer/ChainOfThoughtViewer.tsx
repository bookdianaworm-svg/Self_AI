"use client";

import React from "react";
import { useAgentLoopStore } from '@/store/agent-loop-store';

interface ChainThoughtStep {
  step_id: string;
  agent_id: string;
  iteration: number;
  thought: string;
  action: string;
  context: Record<string, any>;
}

interface ChainOfThoughtViewerProps {
  agentId: string;
  steps?: ChainThoughtStep[];
}

export const ChainOfThoughtViewer: React.FC<ChainOfThoughtViewerProps> = ({ agentId, steps = [] }) => {
  const agents = useAgentLoopStore((s) => s.agents);
  const agent = agentId ? agents?.[agentId] : null;
  const chainOfThought: ChainThoughtStep[] = agent?.chain_of_thought || steps;

  if (chainOfThought.length === 0) {
    return (
      <div className="chain-of-thought-viewer empty-state">
        <h3>Chain of Thought</h3>
        <p>No reasoning steps recorded</p>
      </div>
    );
  }

  const actionColors: Record<string, string> = {
    spawn_agent: "bg-purple-600",
    execute_code: "bg-blue-600",
    llm_query: "bg-green-600",
    verification: "bg-yellow-600",
    final_answer: "bg-red-600",
    use_tool: "bg-cyan-600",
    reasoning: "bg-gray-600",
    unknown: "bg-muted-foreground",
  };

  return (
    <div className="chain-of-thought-viewer">
      <h3>Chain of Thought</h3>

      <div className="cot-timeline">
        {chainOfThought.map((step, index) => (
          <div key={step.step_id} className="cot-step">
            <div className="cot-step-connector">
              <div
                className={`cot-dot ${actionColors[step.action] || actionColors.unknown}`}
              >
                {index + 1}
              </div>
              {index < chainOfThought.length - 1 && <div className="cot-line" />}
            </div>

            <div className="cot-step-content">
              <div className="cot-step-header">
                <span className="cot-iteration">Iteration {step.iteration}</span>
                <span
                  className={`action-badge ${actionColors[step.action] || actionColors.unknown}`}
                >
                  {step.action.replace("_", " ")}
                </span>
              </div>

              <div className="cot-thought">"{step.thought}"</div>

              {step.context && Object.keys(step.context).length > 0 && (
                <div className="cot-context">
                  <details>
                    <summary>Context ({Object.keys(step.context).length})</summary>
                    <ul>
                      {step.context.variables_mentioned?.length > 0 && (
                        <li>Variables: {step.context.variables_mentioned.slice(0, 5).join(", ")}</li>
                      )}
                      {step.context.functions_called?.length > 0 && (
                        <li>Functions: {step.context.functions_called.slice(0, 5).join(", ")}</li>
                      )}
                      {step.context.operations?.length > 0 && (
                        <li>Operations: {step.context.operations.join(", ")}</li>
                      )}
                    </ul>
                  </details>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChainOfThoughtViewer;
