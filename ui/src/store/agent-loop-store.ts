import { create } from 'zustand';

export interface LLMCallRecord {
  call_id: string;
  agent_id: string;
  depth: number;
  model: string;
  prompt: string;
  response: string;
  input_tokens: number;
  output_tokens: number;
  execution_time: number;
  success: boolean;
  error: string | null;
  timestamp: number;
}

export interface REPLExecutionRecord {
  execution_id: string;
  agent_id: string;
  code: string;
  stdout: string;
  stderr: string;
  execution_time: number;
  success: boolean;
  error: string | null;
  return_value_preview: string | null;
  llm_calls_made: string[];
  timestamp: number;
}

export interface ChainThoughtStep {
  step_id: string;
  agent_id: string;
  iteration: number;
  thought: string;
  action: string;
  context: Record<string, unknown>;
}

export interface IterationRecord {
  iteration_id: string;
  agent_id: string;
  iteration_number: number;
  llm_call_id: string | null;
  repl_execution_id: string | null;
  timestamp: number;
}

export interface SpawningEvent {
  event_id: string;
  parent_agent_id: string;
  child_agent_id: string;
  child_agent_name: string;
  timestamp: number;
}

interface AgentLoopStore {
  agents: Record<string, {
    agent_id: string;
    agent_name: string;
    status: string;
    depth: number;
    parent_id: string | null;
    iterations: IterationRecord[];
    llm_calls: LLMCallRecord[];
    repl_history: REPLExecutionRecord[];
    chain_of_thought: ChainThoughtStep[];
    spawning_events: SpawningEvent[];
    successful_repl_executions: number;
    failed_repl_executions: number;
  }>;
  active_agent_id: string | null;
  wsConnected: boolean;
  setWsConnected: (connected: boolean) => void;
  setActiveAgent: (agentId: string | null) => void;
  addLLMCall: (agentId: string, call: LLMCallRecord) => void;
  addREPLExecution: (agentId: string, execution: REPLExecutionRecord) => void;
  addChainThought: (agentId: string, step: ChainThoughtStep) => void;
  addSpawningEvent: (agentId: string, event: SpawningEvent) => void;
  addIteration: (agentId: string, iteration: IterationRecord) => void;
  updateAgentStatus: (agentId: string, status: string) => void;
  registerAgent: (agentId: string, agentName: string, depth: number, parentId: string | null) => void;
  clearAgentHistory: (agentId: string) => void;
}

export const useAgentLoopStore = create<AgentLoopStore>((set) => ({
  agents: {},
  active_agent_id: null,
  wsConnected: false,
  setWsConnected: (connected) => set({ wsConnected: connected }),
  setActiveAgent: (agentId) => set({ active_agent_id: agentId }),
  addLLMCall: (agentId, call) => set((state) => {
    const agent = state.agents[agentId];
    if (!agent) return state;
    return {
      agents: {
        ...state.agents,
        [agentId]: {
          ...agent,
          llm_calls: [...agent.llm_calls, call],
        },
      },
    };
  }),
  addREPLExecution: (agentId, execution) => set((state) => {
    const agent = state.agents[agentId];
    if (!agent) return state;
    return {
      agents: {
        ...state.agents,
        [agentId]: {
          ...agent,
          repl_history: [...agent.repl_history, execution],
          successful_repl_executions: execution.success
            ? agent.successful_repl_executions + 1
            : agent.successful_repl_executions,
          failed_repl_executions: !execution.success
            ? agent.failed_repl_executions + 1
            : agent.failed_repl_executions,
        },
      },
    };
  }),
  addChainThought: (agentId, step) => set((state) => {
    const agent = state.agents[agentId];
    if (!agent) return state;
    return {
      agents: {
        ...state.agents,
        [agentId]: {
          ...agent,
          chain_of_thought: [...agent.chain_of_thought, step],
        },
      },
    };
  }),
  addSpawningEvent: (agentId, event) => set((state) => {
    const agent = state.agents[agentId];
    if (!agent) return state;
    return {
      agents: {
        ...state.agents,
        [agentId]: {
          ...agent,
          spawning_events: [...agent.spawning_events, event],
        },
      },
    };
  }),
  addIteration: (agentId, iteration) => set((state) => {
    const agent = state.agents[agentId];
    if (!agent) return state;
    return {
      agents: {
        ...state.agents,
        [agentId]: {
          ...agent,
          iterations: [...agent.iterations, iteration],
        },
      },
    };
  }),
  updateAgentStatus: (agentId, status) => set((state) => {
    const agent = state.agents[agentId];
    if (!agent) return state;
    return {
      agents: {
        ...state.agents,
        [agentId]: {
          ...agent,
          status,
        },
      },
    };
  }),
  registerAgent: (agentId, agentName, depth, parentId) => set((state) => {
    if (state.agents[agentId]) return state;
    return {
      agents: {
        ...state.agents,
        [agentId]: {
          agent_id: agentId,
          agent_name: agentName,
          status: 'idle',
          depth,
          parent_id: parentId,
          iterations: [],
          llm_calls: [],
          repl_history: [],
          chain_of_thought: [],
          spawning_events: [],
          successful_repl_executions: 0,
          failed_repl_executions: 0,
        },
      },
    };
  }),
  clearAgentHistory: (agentId) => set((state) => {
    const agent = state.agents[agentId];
    if (!agent) return state;
    return {
      agents: {
        ...state.agents,
        [agentId]: {
          ...agent,
          iterations: [],
          llm_calls: [],
          repl_history: [],
          chain_of_thought: [],
          spawning_events: [],
          successful_repl_executions: 0,
          failed_repl_executions: 0,
        },
      },
    };
  }),
}));
