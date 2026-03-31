# Main Implementation Guide for Self-Improving Swarm System

## Overview

This guide provides detailed implementation instructions for the core components of the Self-Improving Swarm System, focusing on the main recursive instance, agent framework, and integration with the existing RLM system.

## 1. Core Redux Store Implementation

### 1.1 Store Setup

First, create the main store configuration:

```typescript
// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import { combineReducers } from 'redux';
import agentReducer from './slices/agentSlice';
import taskReducer from './slices/taskSlice';
import messageReducer from './slices/messageSlice';
import systemReducer from './slices/systemSlice';
import toolReducer from './slices/toolSlice';
import improvementReducer from './slices/improvementSlice';
import uiReducer from './slices/uiSlice';

// Middleware
import { stateSyncMiddleware } from './middleware/stateSyncMiddleware';
import { conflictResolutionMiddleware } from './middleware/conflictResolutionMiddleware';
import { performanceOptimizationMiddleware } from './middleware/performanceOptimizationMiddleware';

const rootReducer = combineReducers({
  agents: agentReducer,
  tasks: taskReducer,
  messages: messageReducer,
  system: systemReducer,
  tools: toolReducer,
  improvements: improvementReducer,
  ui: uiReducer,
});

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
        ignoredPaths: ['messages.history'],
      },
    }).concat([
      stateSyncMiddleware,
      conflictResolutionMiddleware,
      performanceOptimizationMiddleware,
    ]),
  devTools: process.env.NODE_ENV !== 'production',
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### 1.2 Slice Implementations

Create each slice according to the design specifications:

```typescript
// slices/agentSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AgentEntity, AgentSliceState } from '../types/agentTypes';

const initialState: AgentSliceState = {
  entities: {},
  ids: [],
  status: 'idle',
  mainInstanceId: null,
  stats: {
    totalAgents: 0,
    activeAgents: 0,
    completedAgents: 0,
    failedAgents: 0,
    mainInstanceActive: false
  }
};

export const agentSlice = createSlice({
  name: 'agents',
  initialState,
  reducers: {
    addAgent: (state, action: PayloadAction<AgentEntity>) => {
      const agent = action.payload;
      state.entities[agent.id] = agent;
      state.ids.push(agent.id);
      
      if (agent.type === 'main') {
        state.mainInstanceId = agent.id;
        state.stats.mainInstanceActive = true;
      }
      
      state.stats.totalAgents++;
      if (agent.status === 'executing') {
        state.stats.activeAgents++;
      }
    },
    
    updateAgentStatus: (state, action: PayloadAction<{ agentId: string; status: AgentEntity['status'] }>) => {
      const { agentId, status } = action.payload;
      const agent = state.entities[agentId];
      
      if (agent) {
        const oldStatus = agent.status;
        agent.status = status;
        agent.lastUpdate = Date.now();
        
        // Update stats based on status change
        if (oldStatus === 'executing' && status !== 'executing') {
          state.stats.activeAgents--;
        } else if (oldStatus !== 'executing' && status === 'executing') {
          state.stats.activeAgents++;
        }
        
        if (status === 'completed') {
          state.stats.completedAgents++;
        } else if (status === 'failed') {
          state.stats.failedAgents++;
        }
      }
    },
    
    removeAgent: (state, action: PayloadAction<string>) => {
      const agentId = action.payload;
      const agent = state.entities[agentId];
      
      if (agent) {
        delete state.entities[agentId];
        state.ids = state.ids.filter(id => id !== agentId);
        
        if (agent.status === 'executing') {
          state.stats.activeAgents--;
        }
        
        if (agent.type === 'main') {
          state.mainInstanceId = null;
          state.stats.mainInstanceActive = false;
        }
      }
    },
    
    updateAgentResources: (state, action: PayloadAction<{ agentId: string; resources: Partial<AgentEntity['resources']> }>) => {
      const { agentId, resources } = action.payload;
      const agent = state.entities[agentId];
      
      if (agent) {
        Object.assign(agent.resources, resources);
      }
    },
  },
});

export const { addAgent, updateAgentStatus, removeAgent, updateAgentResources } = agentSlice.actions;
export default agentSlice.reducer;
```

## 2. Main Recursive Instance Development

### 2.1 Enhanced RLM Class

Extend the existing RLM class to support continuous spawning:

```python
# rlm/core/swarm_rlm.py
import asyncio
import threading
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import uuid
from datetime import datetime

from rlm.core.rlm import RLM
from rlm.core.types import RLMChatCompletion
from rlm.core.comms_utils import LMRequest, LMResponse


class AgentStatus(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    TERMINATED = "terminated"


@dataclass
class SwarmAgent:
    id: str
    parent_id: Optional[str]
    task: str
    status: AgentStatus
    created_at: datetime
    last_update: datetime
    backend: str
    environment: str
    rlm_instance: RLM


class SwarmRLM(RLM):
    """
    Enhanced RLM that supports continuous spawning of agents during its recursive loop.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agents: Dict[str, SwarmAgent] = {}
        self.agent_lock = threading.Lock()
        self.message_queue = asyncio.Queue()
        self.should_spawn_agents = True
        
    def spawn_agent(self, task: str, backend: str = None, environment: str = None) -> str:
        """
        Spawn a new agent to work on a specific task.
        """
        with self.agent_lock:
            agent_id = str(uuid.uuid4())
            
            # Create a new RLM instance for the agent
            agent_rlm = RLM(
                backend=backend or self.backend,
                backend_kwargs=backend_kwargs or self.backend_kwargs,
                environment=environment or self.environment_type,
                environment_kwargs=self.environment_kwargs,
                depth=self.depth + 1,
                max_depth=self.max_depth,
                max_iterations=self.max_iterations,
                max_budget=self.max_budget,
                max_timeout=self.max_timeout,
                max_tokens=self.max_tokens,
                max_errors=self.max_errors,
                custom_system_prompt=self.system_prompt,
                other_backends=self.other_backends,
                other_backend_kwargs=self.other_backend_kwargs,
                logger=self.logger,
                verbose=False,
                persistent=False,
                custom_tools=self.custom_tools,
                custom_sub_tools=self.custom_sub_tools,
                compaction=self.compaction,
                compaction_threshold_pct=self.compaction_threshold_pct,
                on_subcall_start=self.on_subcall_start,
                on_subcall_complete=self.on_subcall_complete,
            )
            
            agent = SwarmAgent(
                id=agent_id,
                parent_id=self.id if hasattr(self, 'id') else None,
                task=task,
                status=AgentStatus.IDLE,
                created_at=datetime.now(),
                last_update=datetime.now(),
                backend=backend or self.backend,
                environment=environment or self.environment_type,
                rlm_instance=agent_rlm
            )
            
            self.agents[agent_id] = agent
            
            # Start the agent in a separate thread
            agent_thread = threading.Thread(target=self._run_agent, args=(agent_id,))
            agent_thread.daemon = True
            agent_thread.start()
            
            return agent_id
    
    def _run_agent(self, agent_id: str):
        """
        Run the agent's recursive loop in a separate thread.
        """
        agent = self.agents[agent_id]
        agent.status = AgentStatus.EXECUTING
        agent.last_update = datetime.now()
        
        try:
            result = agent.rlm_instance.completion(agent.task)
            agent.status = AgentStatus.COMPLETED
        except Exception as e:
            agent.status = AgentStatus.FAILED
            print(f"Agent {agent_id} failed: {str(e)}")
        finally:
            agent.last_update = datetime.now()
    
    def _check_if_should_spawn_agent(self, current_iteration: int, message_history: List[Dict]) -> Optional[str]:
        """
        Determine if a new agent should be spawned based on the current state.
        This method analyzes the conversation and decides if delegation is needed.
        """
        # Analyze the current message history to see if a new agent would be beneficial
        analysis_prompt = f"""
        Analyze the following conversation and determine if a specialized agent should be spawned to help with the task.
        
        Current conversation:
        {str(message_history[-5:])}  # Look at the last few exchanges
        
        Task: {self.current_task if hasattr(self, 'current_task') else 'Unknown'}
        
        Respond with "SPAWN: <task_for_new_agent>" if a new agent should be spawned, or "CONTINUE" if the current process should continue.
        """
        
        # Use the LM to decide whether to spawn an agent
        decision = self.client.completion(analysis_prompt)
        
        if decision.startswith("SPAWN:"):
            task_for_new_agent = decision[len("SPAWN:"):].strip()
            return task_for_new_agent
        
        return None
    
    def completion(self, prompt: str | dict[str, Any], root_prompt: str | None = None) -> RLMChatCompletion:
        """
        Enhanced completion method that can spawn agents during the recursive loop.
        """
        self.current_task = prompt if isinstance(prompt, str) else str(prompt)
        
        time_start = time.perf_counter()
        self._completion_start_time = time_start

        # Reset tracking state for this completion
        self._consecutive_errors = 0
        self._last_error = None
        self._best_partial_answer = None
        
        # If we're at max depth, the RLM is an LM, so we fallback to the regular LM.
        if self.depth >= self.max_depth:
            return self._fallback_answer(prompt)

        if self.logger:
            self.logger.clear_iterations()

        with self._spawn_completion_context(prompt) as (lm_handler, environment):
            message_history = self._setup_prompt(prompt)

            compaction_count = 0
            try:
                for i in range(self.max_iterations):
                    # Check timeout before each iteration
                    self._check_timeout(i, time_start)

                    # Check if we should spawn an agent based on the current state
                    task_for_new_agent = self._check_if_should_spawn_agent(i, message_history)
                    if task_for_new_agent and self.should_spawn_agents:
                        print(f"Spawning new agent for task: {task_for_new_agent}")
                        self.spawn_agent(task_for_new_agent)
                    
                    # Check if any agents have completed and incorporate their results
                    completed_agents = self._get_completed_agents()
                    for agent_id, result in completed_agents:
                        # Add agent's result to the message history
                        message_history.append({
                            "role": "system",
                            "content": f"Agent {agent_id} completed its task with result: {result}"
                        })

                    # Compaction: check if context needs summarization
                    if self.compaction and hasattr(environment, "append_compaction_entry"):
                        current_tokens, threshold_tokens, max_tokens = self._get_compaction_status(
                            message_history
                        )
                        self.verbose.print_compaction_status(
                            current_tokens, threshold_tokens, max_tokens
                        )
                        if current_tokens >= threshold_tokens:
                            compaction_count += 1
                            self.verbose.print_compaction()
                            message_history = self._compact_history(
                                lm_handler, environment, message_history, compaction_count)

                    # Current prompt = message history + additional prompt suffix
                    context_count = (
                        environment.get_context_count()
                        if isinstance(environment, SupportsPersistence)
                        else 1
                    )
                    history_count = (
                        environment.get_history_count()
                        if isinstance(environment, SupportsPersistence)
                        else 0
                    )
                    current_prompt = message_history + [
                        build_user_prompt(root_prompt, i, context_count, history_count)
                    ]

                    iteration: RLMIteration = self._completion_turn(
                        prompt=current_prompt,
                        lm_handler=lm_handler,
                        environment=environment,
                    )

                    # Check error/budget/token limits after each iteration
                    self._check_iteration_limits(iteration, i, lm_handler)

                    # Check if RLM is done and has a final answer.
                    # Prefer FINAL_VAR result from REPL execution.
                    final_answer = None
                    for block in iteration.code_blocks:
                        if getattr(block.result, "final_answer", None):
                            final_answer = block.result.final_answer
                            break
                    if final_answer is None:
                        final_answer = find_final_answer(
                            iteration.response, environment=environment
                        )
                    iteration.final_answer = final_answer

                    # Store as best partial answer (most recent response with content)
                    if iteration.response and iteration.response.strip():
                        self._best_partial_answer = iteration.response

                    # If logger is used, log the iteration.
                    if self.logger:
                        self.logger.log(iteration)

                    # Verbose output for this iteration
                    self.verbose.print_iteration(iteration, i + 1)

                    if final_answer is not None:
                        time_end = time.perf_counter()
                        usage = lm_handler.get_usage_summary()
                        self.verbose.print_final_answer(final_answer)
                        self.verbose.print_summary(i + 1, time_end - time_start, usage.to_dict())

                        # Store message history in persistent environment
                        if self.persistent and isinstance(environment, SupportsPersistence):
                            environment.add_history(message_history)

                        return RLMChatCompletion(
                            root_model=self.backend_kwargs.get("model_name", "unknown")
                            if self.backend_kwargs
                            else "unknown",
                            prompt=prompt,
                            response=final_answer,
                            usage_summary=usage,
                            execution_time=time_end - time_start,
                            metadata=self.logger.get_trajectory() if self.logger else None,
                        )

                    # Format the iteration for the next prompt.
                    new_messages = format_iteration(iteration)

                    # Update message history with the new messages.
                    message_history.extend(new_messages)
                    if self.compaction and hasattr(environment, "append_compaction_entry"):
                        environment.append_compaction_entry(new_messages)

            except KeyboardInterrupt:
                self.verbose.print_limit_exceeded("cancelled", "User interrupted execution")
                raise CancellationError(
                    partial_answer=self._best_partial_answer,
                    message="Execution cancelled by user (Ctrl+C)",
                ) from None

            # Default behavior: we run out of iterations, provide one final answer
            time_end = time.perf_counter()
            final_answer = self._default_answer(message_history, lm_handler)
            usage = lm_handler.get_usage_summary()
            self.verbose.print_final_answer(final_answer)
            self.verbose.print_summary(self.max_iterations, time_end - time_start, usage.to_dict())

            # Store message history in persistent environment
            if self.persistent and isinstance(environment, SupportsPersistence):
                environment.add_history(message_history)

            return RLMChatCompletion(
                root_model=self.backend_kwargs.get("model_name", "unknown")
                if self.backend_kwargs
                else "unknown",
                prompt=prompt,
                response=final_answer,
                usage_summary=usage,
                execution_time=time_end - time_start,
                metadata=self.logger.get_trajectory() if self.logger else None,
            )
    
    def _get_completed_agents(self) -> List[tuple[str, Any]]:
        """
        Get results from agents that have completed their tasks.
        """
        completed = []
        with self.agent_lock:
            for agent_id, agent in self.agents.items():
                if agent.status == AgentStatus.COMPLETED and not hasattr(agent, '_result_returned'):
                    # Get the result from the agent's RLM instance
                    # This is a simplified approach - in practice, you'd need a more robust
                    # mechanism to retrieve results from completed threads
                    result = f"Agent {agent_id} completed task: {agent.task}"
                    completed.append((agent_id, result))
                    agent._result_returned = True  # Mark as returned
        
        return completed
```

## 3. Agent Framework Implementation

### 3.1 Base Agent Class

```python
# agents/base_agent.py
import asyncio
import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import uuid
from datetime import datetime

from rlm.core.rlm import RLM
from rlm.core.types import RLMChatCompletion


class AgentStatus(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    TERMINATED = "terminated"


@dataclass
class AgentConfig:
    backend: str = "openai"
    backend_kwargs: Optional[Dict[str, Any]] = None
    environment: str = "local"
    environment_kwargs: Optional[Dict[str, Any]] = None
    max_depth: int = 1
    max_iterations: int = 30
    max_budget: Optional[float] = None
    max_timeout: Optional[float] = None
    max_tokens: Optional[int] = None
    max_errors: Optional[int] = None
    custom_system_prompt: Optional[str] = None
    custom_tools: Optional[Dict[str, Any]] = None
    custom_sub_tools: Optional[Dict[str, Any]] = None
    compaction: bool = False
    compaction_threshold_pct: float = 0.85


class BaseAgent(ABC):
    """
    Base class for all agents in the swarm system.
    """
    
    def __init__(self, agent_id: str, config: AgentConfig, parent_id: Optional[str] = None):
        self.id = agent_id
        self.parent_id = parent_id
        self.config = config
        self.status = AgentStatus.IDLE
        self.created_at = datetime.now()
        self.last_update = datetime.now()
        self.start_time = None
        self.end_time = None
        self.result = None
        self.error = None
        
        # Create the underlying RLM instance
        self.rlm = RLM(
            backend=self.config.backend,
            backend_kwargs=self.config.backend_kwargs,
            environment=self.config.environment,
            environment_kwargs=self.config.environment_kwargs,
            depth=0,  # Agents start at depth 0
            max_depth=self.config.max_depth,
            max_iterations=self.config.max_iterations,
            max_budget=self.config.max_budget,
            max_timeout=self.config.max_timeout,
            max_tokens=self.config.max_tokens,
            max_errors=self.config.max_errors,
            custom_system_prompt=self.config.custom_system_prompt,
            # Note: other_backends not specified for agents, they use the same backend
            logger=None,  # Could add agent-specific logging
            verbose=False,
            persistent=False,
            custom_tools=self.config.custom_tools,
            custom_sub_tools=self.config.custom_sub_tools,
            compaction=self.config.compaction,
            compaction_threshold_pct=self.config.compaction_threshold_pct,
        )
        
        # For communication with other agents
        self.message_handlers: List[Callable] = []
        self.inbox = asyncio.Queue()
        self.outbox = []
    
    @abstractmethod
    async def execute_task(self, task_description: str) -> Any:
        """
        Execute the assigned task. This method should be implemented by subclasses.
        """
        pass
    
    async def run(self, task_description: str) -> Any:
        """
        Main execution method that manages the agent lifecycle.
        """
        self.status = AgentStatus.EXECUTING
        self.start_time = datetime.now()
        self.last_update = datetime.now()
        
        try:
            self.result = await self.execute_task(task_description)
            self.status = AgentStatus.COMPLETED
        except Exception as e:
            self.error = str(e)
            self.status = AgentStatus.FAILED
            print(f"Agent {self.id} failed: {self.error}")
        finally:
            self.end_time = datetime.now()
            self.last_update = datetime.now()
        
        return self.result
    
    def send_message(self, recipient_id: str, message: Dict[str, Any]):
        """
        Send a message to another agent.
        """
        message_obj = {
            "id": str(uuid.uuid4()),
            "sender": self.id,
            "recipient": recipient_id,
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "type": "agent_message"
        }
        self.outbox.append(message_obj)
    
    def register_message_handler(self, handler: Callable):
        """
        Register a function to handle incoming messages.
        """
        self.message_handlers.append(handler)
    
    async def process_incoming_messages(self):
        """
        Process messages from the inbox.
        """
        while not self.inbox.empty():
            message = await self.inbox.get()
            for handler in self.message_handlers:
                await handler(message)
    
    def can_spawn_agents(self) -> bool:
        """
        Determine if this agent is allowed to spawn other agents.
        Override in subclasses as needed.
        """
        return False
    
    def spawn_agent(self, task: str, config: Optional[AgentConfig] = None) -> 'BaseAgent':
        """
        Spawn a new agent. This is a simplified implementation -
        in a full system, this would involve more complex orchestration.
        """
        if not self.can_spawn_agents():
            raise PermissionError(f"Agent {self.id} is not allowed to spawn agents")
        
        if config is None:
            config = self.config  # Inherit configuration from parent
        
        new_agent_id = str(uuid.uuid4())
        new_agent = BaseAgent(new_agent_id, config, parent_id=self.id)
        return new_agent


class TaskProcessingAgent(BaseAgent):
    """
    An agent specialized for processing specific tasks.
    """
    
    def can_spawn_agents(self) -> bool:
        # Allow task processing agents to spawn other agents if needed
        return True
    
    async def execute_task(self, task_description: str) -> Any:
        """
        Execute the task using the underlying RLM.
        """
        print(f"Agent {self.id} executing task: {task_description}")
        
        # Use the RLM to complete the task
        completion_result = self.rlm.completion(task_description)
        
        # Process the result as needed
        result = completion_result.response
        
        # Check if we need to spawn additional agents based on the result
        if self._should_spawn_additional_agents(result):
            await self._spawn_additional_agents(result)
        
        return result
    
    def _should_spawn_additional_agents(self, result: str) -> bool:
        """
        Determine if additional agents should be spawned based on the result.
        """
        # Simple heuristic - in a real system, this would be more sophisticated
        spawn_indicators = [
            "need more information",
            "requires additional analysis",
            "should be broken down further",
            "another agent should handle"
        ]
        
        result_lower = result.lower()
        return any(indicator in result_lower for indicator in spawn_indicators)
    
    async def _spawn_additional_agents(self, result: str):
        """
        Spawn additional agents based on the result.
        """
        # Extract potential subtasks from the result
        # This is a simplified approach - in reality, you'd use more sophisticated NLP
        subtasks = self._extract_subtasks(result)
        
        for subtask in subtasks:
            print(f"Agent {self.id} spawning agent for subtask: {subtask}")
            # In a real implementation, this would involve actual agent spawning
            # and integration with the swarm management system
            pass
    
    def _extract_subtasks(self, result: str) -> List[str]:
        """
        Extract potential subtasks from the result.
        """
        # Simplified extraction - in reality, use NLP techniques
        import re
        
        # Look for numbered lists or bullet points indicating subtasks
        subtask_patterns = [
            r'\d+\.\s*([^\n]+)',  # Numbered list items
            r'-\s*([^\n]+)',      # Bullet points
            r'\*\s*([^\n]+)',     # Asterisk bullets
        ]
        
        subtasks = []
        for pattern in subtask_patterns:
            matches = re.findall(pattern, result)
            subtasks.extend(matches)
        
        return subtasks[:3]  # Limit to first 3 subtasks to avoid too many agents
```

## 4. Shared Messaging System

### 4.1 Message Broker Implementation

```python
# messaging/message_broker.py
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import threading
import queue

from messaging.message_types import Message, MessageType


class MessagePriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class QueuedMessage:
    message: Message
    priority: MessagePriority
    created_at: datetime


class MessageBroker:
    """
    Central hub for routing messages between agents, the main instance, and the user.
    """
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}  # Agent ID -> Agent object
        self.user_callbacks: List[Callable] = []
        self.system_callbacks: List[Callable] = []
        self.message_queues: Dict[str, asyncio.Queue] = {}  # Per-recipient queues
        self.broadcast_subscribers: List[str] = []  # Agents subscribed to broadcasts
        self.topic_subscribers: Dict[str, List[str]] = {}  # Topic -> [agent_ids]
        self.lock = threading.Lock()
        
        # Start the message processing loop
        self.running = True
        self.processing_thread = threading.Thread(target=self._process_messages, daemon=True)
        self.processing_thread.start()
    
    def register_agent(self, agent_id: str, agent_obj: Any):
        """
        Register an agent with the message broker.
        """
        with self.lock:
            self.agents[agent_id] = agent_obj
            self.message_queues[agent_id] = asyncio.Queue()
    
    def unregister_agent(self, agent_id: str):
        """
        Unregister an agent from the message broker.
        """
        with self.lock:
            if agent_id in self.agents:
                del self.agents[agent_id]
            if agent_id in self.message_queues:
                del self.message_queues[agent_id]
    
    def subscribe_to_broadcasts(self, agent_id: str):
        """
        Subscribe an agent to broadcast messages.
        """
        with self.lock:
            if agent_id not in self.broadcast_subscribers:
                self.broadcast_subscribers.append(agent_id)
    
    def unsubscribe_from_broadcasts(self, agent_id: str):
        """
        Unsubscribe an agent from broadcast messages.
        """
        with self.lock:
            if agent_id in self.broadcast_subscribers:
                self.broadcast_subscribers.remove(agent_id)
    
    def subscribe_to_topic(self, agent_id: str, topic: str):
        """
        Subscribe an agent to a specific topic.
        """
        with self.lock:
            if topic not in self.topic_subscribers:
                self.topic_subscribers[topic] = []
            if agent_id not in self.topic_subscribers[topic]:
                self.topic_subscribers[topic].append(agent_id)
    
    def unsubscribe_from_topic(self, agent_id: str, topic: str):
        """
        Unsubscribe an agent from a specific topic.
        """
        with self.lock:
            if topic in self.topic_subscribers:
                if agent_id in self.topic_subscribers[topic]:
                    self.topic_subscribers[topic].remove(agent_id)
    
    def send_message(self, message: Message):
        """
        Send a message to the appropriate recipients.
        """
        # Validate message
        if not self._validate_message(message):
            print(f"Invalid message: {message}")
            return False
        
        # Route message based on recipients
        if 'all' in message.recipients:
            # Send to all agents and user
            self._route_to_all(message)
        elif 'user' in message.recipients:
            # Send to user
            self._route_to_user(message)
        elif 'system' in message.recipients:
            # Send to system handlers
            self._route_to_system(message)
        else:
            # Send to specific agents
            for recipient_id in message.recipients:
                self._route_to_agent(recipient_id, message)
        
        return True
    
    def _validate_message(self, message: Message) -> bool:
        """
        Validate a message before sending.
        """
        if not message.id:
            message.id = str(uuid.uuid4())
        
        if not message.timestamp:
            message.timestamp = datetime.now().isoformat()
        
        # Check for required fields
        if not message.sender:
            print("Message must have a sender")
            return False
        
        if not message.recipients:
            print("Message must have recipients")
            return False
        
        if not message.content:
            print("Message must have content")
            return False
        
        return True
    
    def _route_to_agent(self, agent_id: str, message: Message):
        """
        Route a message to a specific agent.
        """
        if agent_id in self.message_queues:
            try:
                self.message_queues[agent_id].put_nowait(message)
            except asyncio.QueueFull:
                print(f"Message queue for agent {agent_id} is full")
        else:
            print(f"Agent {agent_id} not found in message broker")
    
    def _route_to_all(self, message: Message):
        """
        Route a message to all agents and the user.
        """
        # Send to all registered agents
        for agent_id in self.agents.keys():
            self._route_to_agent(agent_id, message)
        
        # Send to user
        self._route_to_user(message)
    
    def _route_to_user(self, message: Message):
        """
        Route a message to the user.
        """
        for callback in self.user_callbacks:
            try:
                callback(message)
            except Exception as e:
                print(f"Error in user callback: {e}")
    
    def _route_to_system(self, message: Message):
        """
        Route a message to system handlers.
        """
        for callback in self.system_callbacks:
            try:
                callback(message)
            except Exception as e:
                print(f"Error in system callback: {e}")
    
    def _process_messages(self):
        """
        Background thread to process messages.
        """
        while self.running:
            # Process messages for each agent
            for agent_id, msg_queue in self.message_queues.items():
                try:
                    # Non-blocking get to avoid hanging
                    while not msg_queue.empty():
                        message = msg_queue.get_nowait()
                        
                        # Deliver message to agent
                        if agent_id in self.agents:
                            agent = self.agents[agent_id]
                            if hasattr(agent, 'receive_message'):
                                agent.receive_message(message)
                
                except asyncio.QueueEmpty:
                    # No messages to process, continue to next agent
                    continue
                except Exception as e:
                    print(f"Error processing messages for agent {agent_id}: {e}")
            
            # Small delay to prevent busy waiting
            time.sleep(0.01)
    
    def add_user_callback(self, callback: Callable):
        """
        Add a callback for user-bound messages.
        """
        self.user_callbacks.append(callback)
    
    def add_system_callback(self, callback: Callable):
        """
        Add a callback for system-bound messages.
        """
        self.system_callbacks.append(callback)
    
    def get_message_history(self, agent_id: Optional[str] = None, message_type: Optional[MessageType] = None) -> List[Message]:
        """
        Retrieve message history (in a real implementation, this would come from storage).
        """
        # This is a simplified implementation - in reality, you'd store messages persistently
        return []
    
    def stop(self):
        """
        Stop the message broker.
        """
        self.running = False
        self.processing_thread.join(timeout=5.0)  # Wait up to 5 seconds for graceful shutdown
```

### 4.2 Message Types Definition

```python
# messaging/message_types.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class MessageType(Enum):
    STATUS_UPDATE = "status-update"
    TASK_REQUEST = "task-request"
    TASK_COMPLETE = "task-complete"
    RESOURCE_REQUEST = "resource-request"
    TOOL_REQUEST = "tool-request"
    TOOL_SHARE = "tool-share"
    PERMISSION_REQUEST = "permission-request"
    ERROR_REPORT = "error-report"
    QUERY = "query"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    PAUSE_REQUEST = "pause-request"
    RESUME_REQUEST = "resume-request"
    TERMINATE_REQUEST = "terminate-request"
    IMPROVEMENT_SHARE = "improvement-share"
    COLLABORATION = "collaboration"
    SYSTEM_ALERT = "system-alert"


@dataclass
class MessageContent:
    title: str
    body: str
    attachments: Optional[List[Any]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Message:
    id: str
    sender: str  # Agent ID, 'user', or 'system'
    recipients: List[str]  # ['all'], ['user'], ['system'], or specific agent IDs
    type: MessageType
    subtype: Optional[str] = None
    content: MessageContent = None
    timestamp: Optional[str] = None
    priority: str = 'normal'  # 'low', 'normal', 'high', 'critical'
    read_by: Optional[List[str]] = None
    response_to: Optional[str] = None
    status: str = 'sent'  # 'sent', 'delivered', 'read', 'failed'
    
    def __post_init__(self):
        if self.content is None:
            self.content = MessageContent(title="", body="")
        if self.read_by is None:
            self.read_by = []
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
```

## 5. Dynamic Tool Creation System

### 5.1 Tool Registry Implementation

```python
# tools/tool_registry.py
import importlib.util
import tempfile
import os
import sys
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
from datetime import datetime
import inspect
import ast
import uuid


@dataclass
class ToolParameter:
    name: str
    type_hint: str
    required: bool
    description: str
    default_value: Any = None


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: List[ToolParameter]
    implementation: str  # Source code as string
    creator: str  # Agent ID that created the tool
    created_at: datetime
    last_used: datetime
    usage_count: int
    approved: bool
    version: str
    compatibility: Dict[str, List[str]]  # languages, backends, environments


class ToolRegistry:
    """
    Registry for managing tools that can be created dynamically by agents.
    """
    
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.shared_tools: List[str] = []  # Tools available to all agents
        self.agent_tools: Dict[str, List[str]] = {}  # Agent-specific tools
        self.approved_tools: List[str] = []  # Approved tools
        self.pending_approval: List[str] = []  # Tools awaiting approval
        self.tool_modules: Dict[str, Any] = {}  # Loaded tool modules
    
    def register_tool(self, tool_def: ToolDefinition) -> bool:
        """
        Register a new tool in the registry.
        """
        # Validate the tool implementation
        if not self._validate_tool_implementation(tool_def.implementation):
            print(f"Tool {tool_def.name} has invalid implementation")
            return False
        
        # Check for naming conflicts
        if tool_def.name in self.tools:
            print(f"Tool {tool_def.name} already exists")
            return False
        
        # Add the tool to the registry
        self.tools[tool_def.name] = tool_def
        
        # Add to pending approval if not pre-approved
        if tool_def.approved:
            self.approved_tools.append(tool_def.name)
        else:
            self.pending_approval.append(tool_def.name)
        
        # Load the tool module
        self._load_tool_module(tool_def)
        
        return True
    
    def _validate_tool_implementation(self, implementation: str) -> bool:
        """
        Validate that the tool implementation is safe and syntactically correct.
        """
        try:
            # Parse the code to check for syntax errors
            ast.parse(implementation)
            
            # Check for dangerous operations
            dangerous_patterns = [
                'import os', 'import sys', 'import subprocess', 'import shutil',
                '__import__', 'eval', 'exec', 'compile', 'open',
                'file', 'input', 'raw_input'
            ]
            
            for pattern in dangerous_patterns:
                if pattern in implementation:
                    print(f"Dangerous pattern detected: {pattern}")
                    return False
            
            return True
        except SyntaxError as e:
            print(f"Syntax error in tool implementation: {e}")
            return False
    
    def _load_tool_module(self, tool_def: ToolDefinition):
        """
        Load the tool implementation as a module.
        """
        try:
            # Create a temporary file for the tool
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(tool_def.implementation)
                temp_file_path = f.name
            
            # Load the module
            spec = importlib.util.spec_from_file_location(tool_def.name, temp_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Store the module
            self.tool_modules[tool_def.name] = module
            
            # Clean up the temporary file after a delay
            import threading
            def cleanup():
                import time
                time.sleep(30)  # Wait 30 seconds before cleaning up
                try:
                    os.unlink(temp_file_path)
                except OSError:
                    pass  # File might already be deleted
            
            cleanup_thread = threading.Thread(target=cleanup, daemon=True)
            cleanup_thread.start()
            
        except Exception as e:
            print(f"Error loading tool module {tool_def.name}: {e}")
            return False
    
    def get_tool(self, tool_name: str) -> Optional[ToolDefinition]:
        """
        Get a tool definition by name.
        """
        return self.tools.get(tool_name)
    
    def get_tool_function(self, tool_name: str) -> Optional[Callable]:
        """
        Get the actual function for a tool.
        """
        if tool_name in self.tool_modules:
            module = self.tool_modules[tool_name]
            # Assume the function name matches the tool name
            if hasattr(module, tool_name):
                return getattr(module, tool_name)
        return None
    
    def share_tool(self, tool_name: str, agent_id: str) -> bool:
        """
        Share a tool with a specific agent.
        """
        if tool_name not in self.tools:
            print(f"Tool {tool_name} does not exist")
            return False
        
        if agent_id not in self.agent_tools:
            self.agent_tools[agent_id] = []
        
        if tool_name not in self.agent_tools[agent_id]:
            self.agent_tools[agent_id].append(tool_name)
        
        return True
    
    def make_tool_shared(self, tool_name: str) -> bool:
        """
        Make a tool available to all agents.
        """
        if tool_name not in self.tools:
            print(f"Tool {tool_name} does not exist")
            return False
        
        if tool_name not in self.shared_tools:
            self.shared_tools.append(tool_name)
        
        return True
    
    def approve_tool(self, tool_name: str, approver_id: str) -> bool:
        """
        Approve a tool for use.
        """
        if tool_name not in self.tools:
            print(f"Tool {tool_name} does not exist")
            return False
        
        if tool_name in self.pending_approval:
            self.tools[tool_name].approved = True
            self.pending_approval.remove(tool_name)
            self.approved_tools.append(tool_name)
            
            # Log the approval
            print(f"Tool {tool_name} approved by {approver_id}")
            return True
        
        return False
    
    def create_dynamic_tool(self, name: str, description: str, implementation: str, creator_id: str) -> Optional[ToolDefinition]:
        """
        Create a new tool dynamically from source code.
        """
        # Parse the function to extract parameters
        try:
            tree = ast.parse(implementation)
            func_node = None
            
            # Find the function definition
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == name:
                    func_node = node
                    break
            
            if not func_node:
                print(f"Function {name} not found in implementation")
                return None
            
            # Extract parameters
            parameters = []
            for arg in func_node.args.args[1:]:  # Skip 'self' if it's a method
                param = ToolParameter(
                    name=arg.arg,
                    type_hint=getattr(arg, 'annotation', None),
                    required=True,  # For simplicity, assume all params are required
                    description="Parameter for dynamic tool"
                )
                parameters.append(param)
            
            # Create tool definition
            tool_def = ToolDefinition(
                name=name,
                description=description,
                parameters=parameters,
                implementation=implementation,
                creator=creator_id,
                created_at=datetime.now(),
                last_used=datetime.now(),
                usage_count=0,
                approved=False,  # Newly created tools need approval
                version="1.0",
                compatibility={
                    "languages": ["python"],
                    "backends": ["all"],  # Initially available to all backends
                    "environments": ["all"]  # Initially available in all environments
                }
            )
            
            # Register the tool
            if self.register_tool(tool_def):
                return tool_def
            else:
                return None
                
        except Exception as e:
            print(f"Error creating dynamic tool {name}: {e}")
            return None
    
    def get_agent_tools(self, agent_id: str) -> List[ToolDefinition]:
        """
        Get all tools available to an agent (shared + agent-specific).
        """
        agent_tool_names = set(self.shared_tools)
        
        if agent_id in self.agent_tools:
            agent_tool_names.update(self.agent_tools[agent_id])
        
        return [self.tools[name] for name in agent_tool_names if name in self.tools]
```

## 6. Self-Improvement Contribution System

### 6.1 Improvement Registry Implementation

```python
# improvements/improvement_registry.py
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import uuid


class ImprovementType(Enum):
    PROCESS = "process"
    TOOL = "tool"
    ALGORITHM = "algorithm"
    OPTIMIZATION = "optimization"
    FEATURE = "feature"


class ImprovementCategory(Enum):
    EFFICIENCY = "efficiency"
    ACCURACY = "accuracy"
    USABILITY = "usability"
    SECURITY = "security"
    SCALABILITY = "scalability"


class ImprovementStatus(Enum):
    PROPOSED = "proposed"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"
    DEPRECATED = "deprecated"


class ImpactLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ApprovalEvent:
    approver: str  # Agent ID or 'system' or 'user'
    timestamp: datetime
    action: str  # 'approved', 'rejected', 'commented'
    comment: Optional[str] = None


@dataclass
class ImprovementTestResults:
    automated_tests_passed: int
    automated_tests_total: int
    manual_tests_passed: int
    manual_tests_total: int
    performance_impact: Dict[str, Any]  # Before/after metrics
    stability: str  # 'stable', 'needs-monitoring', 'unstable'


@dataclass
class ImprovementImplementation:
    type: str  # 'code-change', 'configuration', 'new-tool', 'process-change'
    target: str  # Which system component to improve
    changes: List[Any]  # Specific changes to apply
    rollback_plan: Optional[Any] = None  # How to revert this improvement


@dataclass
class ImprovementEntity:
    id: str
    title: str
    description: str
    type: ImprovementType
    category: ImprovementCategory
    implementation: ImprovementImplementation
    creator: str  # Agent ID that proposed the improvement
    created_at: datetime
    applied_at: Optional[datetime]
    status: ImprovementStatus
    impact: ImpactLevel
    dependencies: List[str]  # IDs of other improvements this depends on
    affected_components: List[str]  # Which system components are affected
    test_results: Optional[ImprovementTestResults]
    approval_history: List[ApprovalEvent]


class ImprovementRegistry:
    """
    Registry for managing system improvements contributed by agents.
    """
    
    def __init__(self):
        self.improvements: Dict[str, ImprovementEntity] = {}
        self.pending_approvals: List[str] = []  # IDs of improvements awaiting approval
        self.active_improvements: List[str] = []  # IDs of improvements currently active in system
        self.history: List[str] = []  # IDs of all improvements ever made
        self.applied_improvements: List[str] = []  # IDs of improvements that have been applied
    
    def propose_improvement(self, improvement: ImprovementEntity) -> bool:
        """
        Propose a new improvement to the system.
        """
        # Validate the improvement
        if not self._validate_improvement(improvement):
            print(f"Improvement {improvement.title} is invalid")
            return False
        
        # Add to registry
        self.improvements[improvement.id] = improvement
        self.pending_approvals.append(improvement.id)
        self.history.append(improvement.id)
        
        print(f"Improvement '{improvement.title}' proposed by {improvement.creator}")
        return True
    
    def _validate_improvement(self, improvement: ImprovementEntity) -> bool:
        """
        Validate an improvement before accepting it.
        """
        # Check for required fields
        if not improvement.title or not improvement.description:
            print("Improvement must have title and description")
            return False
        
        if not improvement.creator:
            print("Improvement must have a creator")
            return False
        
        # Check dependencies exist
        for dep_id in improvement.dependencies:
            if dep_id not in self.improvements:
                print(f"Dependency {dep_id} does not exist")
                return False
        
        return True
    
    def approve_improvement(self, improvement_id: str, approver_id: str, comment: Optional[str] = None) -> bool:
        """
        Approve an improvement.
        """
        if improvement_id not in self.improvements:
            print(f"Improvement {improvement_id} does not exist")
            return False
        
        improvement = self.improvements[improvement_id]
        
        if improvement.status != ImprovementStatus.PROPOSED:
            print(f"Improvement {improvement_id} is not in proposed state")
            return False
        
        # Add approval event
        approval_event = ApprovalEvent(
            approver=approver_id,
            timestamp=datetime.now(),
            action="approved",
            comment=comment
        )
        improvement.approval_history.append(approval_event)
        
        # Update status
        improvement.status = ImprovementStatus.APPROVED
        
        # Remove from pending approvals
        if improvement_id in self.pending_approvals:
            self.pending_approvals.remove(improvement_id)
        
        print(f"Improvement '{improvement.title}' approved by {approver_id}")
        return True
    
    def reject_improvement(self, improvement_id: str, approver_id: str, comment: str) -> bool:
        """
        Reject an improvement.
        """
        if improvement_id not in self.improvements:
            print(f"Improvement {improvement_id} does not exist")
            return False
        
        improvement = self.improvements[improvement_id]
        
        if improvement.status != ImprovementStatus.PROPOSED:
            print(f"Improvement {improvement_id} is not in proposed state")
            return False
        
        # Add rejection event
        rejection_event = ApprovalEvent(
            approver=approver_id,
            timestamp=datetime.now(),
            action="rejected",
            comment=comment
        )
        improvement.approval_history.append(rejection_event)
        
        # Update status
        improvement.status = ImprovementStatus.REJECTED
        
        # Remove from pending approvals
        if improvement_id in self.pending_approvals:
            self.pending_approvals.remove(improvement_id)
        
        print(f"Improvement '{improvement.title}' rejected by {approver_id}")
        return True
    
    def apply_improvement(self, improvement_id: str) -> bool:
        """
        Apply an approved improvement to the system.
        """
        if improvement_id not in self.improvements:
            print(f"Improvement {improvement_id} does not exist")
            return False
        
        improvement = self.improvements[improvement_id]
        
        if improvement.status != ImprovementStatus.APPROVED:
            print(f"Improvement {improvement_id} is not approved")
            return False
        
        # Apply the improvement (this would involve actual system changes)
        success = self._apply_improvement_changes(improvement)
        
        if success:
            improvement.status = ImprovementStatus.APPLIED
            improvement.applied_at = datetime.now()
            self.applied_improvements.append(improvement_id)
            self.active_improvements.append(improvement_id)
            
            print(f"Improvement '{improvement.title}' applied to system")
            return True
        else:
            print(f"Failed to apply improvement '{improvement.title}'")
            return False
    
    def _apply_improvement_changes(self, improvement: ImprovementEntity) -> bool:
        """
        Actually apply the improvement changes to the system.
        This is a simplified implementation - in reality, this would involve
        complex system modifications based on the improvement type.
        """
        try:
            # Based on the improvement type, apply the changes
            imp_type = improvement.implementation.type
            
            if imp_type == "new-tool":
                # Add a new tool to the system
                print(f"Adding new tool: {improvement.title}")
            elif imp_type == "process-change":
                # Modify a process
                print(f"Modifying process: {improvement.title}")
            elif imp_type == "optimization":
                # Apply optimization
                print(f"Applying optimization: {improvement.title}")
            elif imp_type == "code-change":
                # Apply code changes
                print(f"Applying code changes: {improvement.title}")
            elif imp_type == "configuration":
                # Update configuration
                print(f"Updating configuration: {improvement.title}")
            else:
                print(f"Unknown improvement type: {imp_type}")
                return False
            
            return True
        except Exception as e:
            print(f"Error applying improvement: {e}")
            return False
    
    def get_improvements_by_creator(self, creator_id: str) -> List[ImprovementEntity]:
        """
        Get all improvements proposed by a specific creator.
        """
        return [imp for imp in self.improvements.values() if imp.creator == creator_id]
    
    def get_improvements_by_status(self, status: ImprovementStatus) -> List[ImprovementEntity]:
        """
        Get all improvements with a specific status.
        """
        return [imp for imp in self.improvements.values() if imp.status == status]
    
    def get_active_improvements(self) -> List[ImprovementEntity]:
        """
        Get all currently active improvements.
        """
        return [self.improvements[imp_id] for imp_id in self.active_improvements]
    
    def deprecate_improvement(self, improvement_id: str, reason: str) -> bool:
        """
        Mark an improvement as deprecated.
        """
        if improvement_id not in self.improvements:
            print(f"Improvement {improvement_id} does not exist")
            return False
        
        improvement = self.improvements[improvement_id]
        improvement.status = ImprovementStatus.DEPRECATED
        
        # Remove from active improvements
        if improvement_id in self.active_improvements:
            self.active_improvements.remove(improvement_id)
        
        print(f"Improvement '{improvement.title}' marked as deprecated: {reason}")
        return True
```

This implementation guide provides the core components needed for the Self-Improving Swarm System. Each section includes detailed code examples that demonstrate how to implement the various system components, from the Redux store to the agent framework, messaging system, tool creation, and improvement registry.