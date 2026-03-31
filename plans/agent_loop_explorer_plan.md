# Agent Loop Explorer Plan

## Problem Statement

Currently, the system has `on_subcall_start`/`on_subcall_complete` callbacks in the RLM class, and `RLMChatCompletion`/`RLMIteration` types capture LLM I/O, but **none of this is wired to a UI for full observability**. Users cannot see:
- Raw LLM input/output per agent
- Every REPL code block (successful/unsuccessful)
- Chain-of-thought that led to actions
- Agent spawning decisions

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Agent Loop Explorer Architecture                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │    RLM      │───▶│  Callbacks  │───▶│  Redux      │───▶│  WebSocket  │   │
│  │  (source)   │    │  (wiring)   │    │  (new slice)│    │  (push)     │   │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘   │
│         │                                        │                │         │
│         ▼                                        ▼                ▼         │
│  ┌─────────────┐                        ┌─────────────┐    ┌─────────────┐   │
│  │ LocalREPL   │                        │ Agent Loop  │    │   React     │   │
│  │ (executes)  │                        │   Slice     │    │    UI       │   │
│  └─────────────┘                        └─────────────┘    └─────────────┘   │
│                                                  │                            │
│                                                  ▼                            │
│                                         ┌─────────────┐                       │
│                                         │   History   │                       │
│                                         │  (SQLite)   │                       │
│                                         └─────────────┘                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: Redux Slice for Agent Loop Observability

**New file: `rlm/redux/slices/agent_loop_slice.py`**

```python
@dataclass
class LLMCallRecord:
    """Single LLM call (prompt → response)."""
    call_id: str
    agent_id: str
    parent_call_id: Optional[str]  # For nested calls
    depth: int
    model: str
    prompt: str
    response: str
    input_tokens: int
    output_tokens: int
    cost: Optional[float]
    execution_time: float
    timestamp: float
    call_type: str  # "completion", "subcall", "llm_query"
    success: bool
    error: Optional[str] = None


@dataclass
class REPLExecutionRecord:
    """Single REPL code block execution."""
    execution_id: str
    agent_id: str
    parent_call_id: str
    code: str
    stdout: str
    stderr: str
    execution_time: float
    success: bool  # False if stderr contains errors
    error: Optional[str] = None
    return_value_preview: Optional[str] = None  # First 200 chars of return
    llm_calls_made: List[str]  # IDs of LLM calls within this execution


@dataclass
class IterationRecord:
    """Single RLM iteration."""
    iteration_id: str
    agent_id: str
    iteration_number: int
    depth: int
    prompt: str  # Full prompt sent to LLM
    response: str  # Raw LLM response
    code_blocks: List[REPLExecutionRecord]
    final_answer: Optional[str]
    execution_time: float
    timestamp: float


@dataclass
class AgentLoopState:
    """Full loop state for an agent."""
    agent_id: str
    agent_name: str
    status: AgentStatus
    depth: int
    current_task: str
    started_at: float
    iterations: List[IterationRecord]
    llm_calls: Dict[str, LLMCallRecord]
    repl_history: List[REPLExecutionRecord]
    spawning_events: List[SpawningEvent]
    chain_of_thought: List[ChainThoughtStep]


@dataclass
class SpawningEvent:
    """Agent spawned another agent."""
    event_id: str
    parent_agent_id: str
    child_agent_id: str
    child_task: str
    reason: str  # Why spawning was triggered
    timestamp: float


@dataclass
class ChainThoughtStep:
    """Chain-of-thought reasoning step."""
    step_id: str
    agent_id: str
    iteration: int
    thought: str  # Extracted from LLM response
    action: str  # What was decided (e.g., "spawn agent", "execute code")
    context: Dict[str, Any]  # Relevant variables/state at this point


@dataclass
class AgentLoopSlice:
    """Redux slice for agent loop observability."""
    agents: Dict[str, AgentLoopState] = field(default_factory=dict)
    active_agent_id: Optional[str] = None
    call_index: int = 0  # For generating unique call IDs
    repl_index: int = 0
    iteration_index: int = 0
    chain_thought_index: int = 0
    streaming_mode: bool = True  # If true, push updates immediately
    max_history_per_agent: int = 1000
    paused_agents: List[str] = field(default_factory=list)  # Agents paused from streaming
```

### Phase 2: Wire Callbacks to Redux

**Modified file: `rlm/core/rlm.py`**

The RLM class already has callbacks:
- `on_subcall_start(depth, model, prompt_preview)`
- `on_subcall_complete(depth, model, duration, error)`
- `on_iteration_start(depth, iteration_num)`
- `on_iteration_complete(depth, iteration_num, duration)`

**New file: `rlm/redux/middleware/agent_loop_middleware.py`**

Create a callback handler that dispatches to Redux:

```python
class AgentLoopCallbacks:
    def __init__(self, store: ReduxStore, agent_id: str, agent_name: str):
        self.store = store
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.parent_call_id: Optional[str] = None
        self.current_iteration: Optional[int] = None
        
    def on_iteration_start(self, depth: int, iteration_num: int):
        self.current_iteration = iteration_num
        self.store.dispatch(AgentLoopActions.iteration_started(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            depth=depth,
            iteration=iteration_num
        ))
    
    def on_iteration_complete(self, depth: int, iteration_num: int, duration: float):
        self.store.dispatch(AgentLoopActions.iteration_completed(
            agent_id=self.agent_id,
            iteration=iteration_num,
            duration=duration
        ))
    
    def on_subcall_start(self, depth: int, model: str, prompt_preview: str):
        call_id = self.store.dispatch(AgentLoopActions.llm_call_started(
            agent_id=self.agent_id,
            parent_call_id=self.parent_call_id,
            depth=depth,
            model=model,
            prompt=prompt_preview,
            call_type="subcall"
        ))
        self.parent_call_id = call_id  # Nested calls track parent
    
    def on_subcall_complete(self, depth: int, model: str, duration: float, error: Optional[str]):
        self.store.dispatch(AgentLoopActions.llm_call_completed(
            agent_id=self.agent_id,
            duration=duration,
            error=error,
            success=error is None
        ))
        self.parent_call_id = None  # Reset after subcall completes
```

### Phase 3: Capture Full LLM I/O

**Modified: `rlm/core/rlm.py` `_completion_turn()` method**

Currently:
```python
def _completion_turn(self, prompt, lm_handler, environment):
    iter_start = time.perf_counter()
    response = lm_handler.completion(prompt)
    # ... code execution ...
```

**Add full capture**:
```python
def _completion_turn(self, prompt, lm_handler, environment):
    iter_start = time.perf_counter()
    
    # Capture the full prompt
    full_prompt = self._build_current_prompt(prompt)
    
    # Make the LLM call
    response = lm_handler.completion(prompt)
    
    # Capture usage info
    usage = lm_handler.get_last_usage()
    
    # Record this LLM call
    call_id = self._callbacks.record_llm_call(
        agent_id=self.agent_id,
        model=self.backend_kwargs.get("model_name", "unknown"),
        prompt=full_prompt,
        response=response,
        input_tokens=usage.input_tokens if usage else 0,
        output_tokens=usage.output_tokens if usage else 0,
        cost=usage.cost if usage else None,
        execution_time=time.perf_counter() - iter_start,
        call_type="completion"
    )
    
    # ... rest of code execution, recording each REPL block ...
```

### Phase 4: Capture REPL Executions

**Modified: `rlm/environments/local_repl.py` `execute_code()` method**

Currently returns `REPLResult` but nowhere persists it.

**Add execution tracking**:
```python
def execute_code(self, code: str, execution_context: Dict[str, Any]) -> REPLResult:
    # ... existing execution logic ...
    
    result = REPLResult(...)
    
    # NEW: Dispatch execution record if we have a callback
    if execution_context.get("track_execution"):
        execution_context["callback"](
            execution_id=str(uuid.uuid4()),
            agent_id=execution_context["agent_id"],
            code=code,
            stdout=result.stdout,
            stderr=result.stderr,
            execution_time=result.execution_time,
            success=not result.stderr or "Error" not in result.stderr,
            error=result.stderr if result.stderr else None,
            llm_calls_made=[c.call_id for c in result.rlm_calls]
        )
    
    return result
```

### Phase 5: Chain-of-Thought Extraction

**New file: `rlm/utils/chain_of_thought.py`**

Extract reasoning steps from LLM responses:

```python
def extract_chain_of_thought(response: str) -> List[str]:
    """Extract reasoning steps from LLM response.
    
    Looks for patterns like:
    - "Let me think..."
    - "I need to..."
    - Numbered reasoning steps
    - "First...", "Then...", "Finally..."
    """
    steps = []
    
    # Pattern 1: Numbered steps
    numbered = re.findall(r'\d+\.\s*([^\n]+)', response)
    steps.extend(numbered)
    
    # Pattern 2: Reasoning keywords
    reasoning_keywords = [
        r'(?:I|I\'ll|I\'m|Let me|First|Then|Next|Finally)\s+([^\.]{10,})',
        r'(?:Because|Since|Therefore|Thus|Hence)\s+([^\.]{10,})',
        r'(?:However|But|Although|Meanwhile)\s+([^\.]{10,})',
    ]
    
    for pattern in reasoning_keywords:
        matches = re.findall(pattern, response, re.IGNORECASE)
        steps.extend(matches)
    
    return steps


def identify_action_from_response(response: str) -> str:
    """Identify what action the LLM decided to take."""
    action_patterns = [
        (r'(?:spawn|create|launch)\s+(?:a\s+)?(?:new\s+)?agent', 'spawn_agent'),
        (r'(?:execute|run|evaluate)\s+(?:the\s+)?(?:following\s+)?code', 'execute_code'),
        (r'(?:query|call|ask)\s+(?:the\s+)?LM', 'llm_query'),
        (r'(?:verify|check|prove)\s+', 'verification'),
        (r'FINAL_VAR', 'final_answer'),
        (r'(?:use|apply)\s+(?:tool|function)', 'use_tool'),
    ]
    
    for pattern, action in action_patterns:
        if re.search(pattern, response, re.IGNORECASE):
            return action
    
    return 'reasoning'
```

### Phase 6: SQLite Persistence Layer

**New file: `rlm/storage/agent_loop_storage.py`**

```python
import sqlite3
from typing import Optional, List
from dataclasses import asdict

class AgentLoopStorage:
    """SQLite-backed storage for agent loop history (enabled by default)."""
    
    def __init__(self, db_path: str = ".agent_loop.db", enabled: bool = True):
        self.db_path = db_path
        self.enabled = enabled
        if enabled:
            self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS llm_calls (
                    call_id TEXT PRIMARY KEY,
                    agent_id TEXT,
                    parent_call_id TEXT,
                    depth INTEGER,
                    model TEXT,
                    prompt TEXT,
                    response TEXT,
                    input_tokens INTEGER,
                    output_tokens INTEGER,
                    cost REAL,
                    execution_time REAL,
                    call_type TEXT,
                    success INTEGER,
                    error TEXT,
                    timestamp REAL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS repl_executions (
                    execution_id TEXT PRIMARY KEY,
                    agent_id TEXT,
                    parent_call_id TEXT,
                    code TEXT,
                    stdout TEXT,
                    stderr TEXT,
                    execution_time REAL,
                    success INTEGER,
                    error TEXT,
                    return_value_preview TEXT,
                    llm_calls_made TEXT,
                    timestamp REAL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS iterations (
                    iteration_id TEXT PRIMARY KEY,
                    agent_id TEXT,
                    iteration_number INTEGER,
                    depth INTEGER,
                    prompt TEXT,
                    response TEXT,
                    code_blocks TEXT,
                    final_answer TEXT,
                    execution_time REAL,
                    timestamp REAL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS spawning_events (
                    event_id TEXT PRIMARY KEY,
                    parent_agent_id TEXT,
                    child_agent_id TEXT,
                    child_task TEXT,
                    reason TEXT,
                    timestamp REAL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chain_thoughts (
                    step_id TEXT PRIMARY KEY,
                    agent_id TEXT,
                    iteration INTEGER,
                    thought TEXT,
                    action TEXT,
                    context TEXT,
                    timestamp REAL
                )
            """)
    
    def save_llm_call(self, call: LLMCallRecord):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO llm_calls VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, asdict(call).values())
    
    def save_repl_execution(self, exec: REPLExecutionRecord):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO repl_executions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                exec.execution_id, exec.agent_id, exec.parent_call_id,
                exec.code, exec.stdout, exec.stderr, exec.execution_time,
                int(exec.success), exec.error, exec.return_value_preview,
                json.dumps(exec.llm_calls_made), 0.0  # timestamp
            ])
    
    def get_agent_history(self, agent_id: str, limit: int = 100) -> Dict[str, Any]:
        """Get full history for an agent."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            calls = conn.execute(
                "SELECT * FROM llm_calls WHERE agent_id = ? ORDER BY timestamp DESC LIMIT ?",
                (agent_id, limit)
            ).fetchall()
            
            repls = conn.execute(
                "SELECT * FROM repl_executions WHERE agent_id = ? ORDER BY timestamp DESC LIMIT ?",
                (agent_id, limit)
            ).fetchall()
            
            iterations = conn.execute(
                "SELECT * FROM iterations WHERE agent_id = ? ORDER BY timestamp DESC LIMIT ?",
                (agent_id, limit)
            ).fetchall()
            
            spawns = conn.execute(
                "SELECT * FROM spawning_events WHERE parent_agent_id = ? ORDER BY timestamp DESC",
                (agent_id,)
            ).fetchall()
            
            return {
                "llm_calls": [dict(r) for r in calls],
                "repl_executions": [dict(r) for r in repls],
                "iterations": [dict(r) for r in iterations],
                "spawning_events": [dict(r) for r in spawns]
            }
```

### Phase 7: WebSocket Real-Time Push

**New file: `rlm/redux/middleware/agent_loop_websocket.py`**

```python
class AgentLoopWebSocket:
    """WebSocket server for real-time agent loop updates."""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[WebSocket] = set()
        self.store_subscription = None
    
    async def connect(self, websocket: WebSocket):
        self.clients.add(websocket)
        # Send current state on connect
        state = self.store.get_state()
        await websocket.send_json(self._serialize_state(state))
    
    def start(self, store: ReduxStore):
        self.store = store
        self.store_subscription = store.subscribe(self._on_state_change)
    
    def _on_state_change(self, state: RootState):
        if not self.clients:
            return
        
        payload = self._serialize_updates(state.agent_loop)
        
        # Broadcast to all connected clients
        for client in self.clients:
            try:
                asyncio.create_task(client.send_json(payload))
            except Exception:
                self.clients.discard(client)
    
    def _serialize_state(self, state: RootState) -> Dict[str, Any]:
        """Serialize current Redux state for initial sync."""
        loop_state = state.agent_loop
        return {
            "type": "full_state",
            "agents": {
                aid: {
                    "status": a.status.value,
                    "iterations": len(a.iterations),
                    "llm_calls": len(a.llm_calls),
                    "repl_history": len(a.repl_history),
                    "current_task": a.current_task[:100] if a.current_task else None
                }
                for aid, a in loop_state.agents.items()
            },
            "active_agent_id": loop_state.active_agent_id
        }
    
    def _serialize_updates(self, loop_state: AgentLoopSlice) -> Dict[str, Any]:
        """Serialize incremental updates."""
        return {
            "type": "incremental_update",
            "active_agent_id": loop_state.active_agent_id,
            # Include latest iteration if streaming mode
            "latest_iteration": self._get_latest_iteration(loop_state)
        }
```

### Phase 8: React UI - Agent Loop Explorer Panel

**New file: `ui/src/components/AgentLoopExplorer/`**

#### Component Structure

```
AgentLoopExplorer/
├── index.tsx                    # Main panel container
├── AgentSelector.tsx            # Dropdown to select agent
├── LLMSnapshot.tsx             # Live/current LLM call view
├── LLMHistory.tsx              # Historical LLM calls list
├── REPLHistory.tsx             # REPL code block history
├── ChainOfThoughtViewer.tsx    # Visual chain-of-thought display
├── IterationTimeline.tsx       # Visual iteration timeline
└── styles.css                   # Component styles
```

#### Main Panel (`index.tsx`)

```tsx
export const AgentLoopExplorer: React.FC = () => {
  const dispatch = useDispatch();
  const agentLoop = useSelector(state => state.agentLoop);
  
  const [viewMode, setViewMode] = useState<'live' | 'history'>('live');
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null);
  const [selectedCallId, setSelectedCallId] = useState<string | null>(null);
  
  useEffect(() => {
    // Connect WebSocket on mount
    const ws = new WebSocket('ws://localhost:8765');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'full_state') {
        dispatch(agentLoopActions.syncState(data));
      } else if (data.type === 'incremental_update') {
        dispatch(agentLoopActions.applyUpdates(data));
      }
    };
    return () => ws.close();
  }, []);
  
  return (
    <div className="agent-loop-explorer">
      <div className="agent-loop-header">
        <h2>Agent Loop Explorer</h2>
        <AgentSelector 
          agents={agentLoop.agents}
          selectedId={selectedAgentId}
          onSelect={setSelectedAgentId}
        />
        <ViewModeToggle 
          mode={viewMode} 
          onChange={setViewMode} 
        />
      </div>
      
      <div className="agent-loop-content">
        {viewMode === 'live' ? (
          <>
            <LIVEMODE>
              <LLMSnapshot 
                agentId={selectedAgentId}
                isActive={selectedAgentId === agentLoop.activeAgentId}
              />
              <CurrentIteration 
                agentId={selectedAgentId}
              />
              <StreamingREPL 
                agentId={selectedAgentId}
              />
            </>
          ) : (
            <>
              <LLMHistory 
                agentId={selectedAgentId}
                calls={agentLoop.agents[selectedAgentId]?.llm_calls || []}
                onSelectCall={setSelectedCallId}
              />
              <REPLHistory 
                agentId={selectedAgentId}
                executions={agentLoop.agents[selectedAgentId]?.repl_history || []}
              />
              <ChainOfThoughtViewer 
                agentId={selectedAgentId}
                steps={agentLoop.agents[selectedAgentId]?.chain_of_thought || []}
              />
            </>
          )}
        </div>
        
        {selectedCallId && (
          <CallDetailDrawer 
            callId={selectedCallId}
            call={findCall(selectedCallId)}
            onClose={() => setSelectedCallId(null)}
          />
        )}
      </div>
    </div>
  );
};
```

#### Live LLM Snapshot (`LLMSnapshot.tsx`)

```tsx
export const LLMSnapshot: React.FC<{agentId: string | null, isActive: boolean}> = ({agentId, isActive}) => {
  const agent = useSelector(state => 
    agentId ? state.agentLoop.agents[agentId] : null
  );
  
  if (!agent) return <div className="empty-state">Select an agent</div>;
  
  const latestCall = agent.llm_calls.length > 0 
    ? agent.llm_calls[agent.llm_calls.length - 1] 
    : null;
  
  return (
    <div className={`llm-snapshot ${isActive ? 'active' : 'inactive'}`}>
      <div className="snapshot-header">
        <span className="status-badge">{agent.status}</span>
        <span className="depth-badge">Depth: {agent.depth}</span>
      </div>
      
      {latestCall && (
        <div className="current-call">
          <div className="call-prompt">
            <label>PROMPT:</label>
            <pre>{latestCall.prompt}</pre>
          </div>
          
          <div className="call-response">
            <label>RESPONSE:</label>
            <pre>{latestCall.response}</pre>
          </div>
          
          <div className="call-meta">
            <span>Model: {latestCall.model}</span>
            <span>Tokens: {latestCall.input_tokens} → {latestCall.output_tokens}</span>
            <span>Time: {latestCall.execution_time.toFixed(2)}s</span>
            <span className={latestCall.success ? 'success' : 'error'}>
              {latestCall.success ? '✓' : '✗'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};
```

#### REPL History (`REPLHistory.tsx`)

```tsx
export const REPLHistory: React.FC<{agentId: string, executions: REPLExecutionRecord[]}> = ({agentId, executions}) => {
  const [filter, setFilter] = useState<'all' | 'success' | 'error'>('all');
  
  const filtered = executions.filter(e => {
    if (filter === 'all') return true;
    if (filter === 'success') return e.success;
    if (filter === 'error') return !e.success;
  });
  
  return (
    <div className="repl-history">
      <div className="repl-history-header">
        <h3>REPL Executions ({filtered.length})</h3>
        <FilterButtons filter={filter} onChange={setFilter} />
      </div>
      
      <div className="repl-list">
        {filtered.map(exec => (
          <div key={exec.execution_id} className={`repl-item ${exec.success ? 'success' : 'error'}`}>
            <div className="repl-item-header">
              <span className="exec-time">{exec.execution_time.toFixed(3)}s</span>
              <span className={`status ${exec.success ? 'success' : 'error'}`}>
                {exec.success ? '✓' : '✗'}
              </span>
            </div>
            
            <div className="repl-code">
              <CodeBlock code={exec.code} language="python" />
            </div>
            
            {exec.stdout && (
              <div className="repl-stdout">
                <label>stdout:</label>
                <pre>{exec.stdout}</pre>
              </div>
            )}
            
            {exec.stderr && (
              <div className="repl-stderr">
                <label>stderr:</label>
                <pre>{exec.stderr}</pre>
              </div>
            )}
            
            {exec.llm_calls_made.length > 0 && (
              <div className="repl-llm-calls">
                <label>LLM calls within:</label>
                <span>{exec.llm_calls_made.length} nested calls</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
```

#### Chain of Thought Viewer (`ChainOfThoughtViewer.tsx`)

```tsx
export const ChainOfThoughtViewer: React.FC<{agentId: string, steps: ChainThoughtStep[]}> = ({agentId, steps}) => {
  return (
    <div className="chain-of-thought-viewer">
      <h3>Chain of Thought</h3>
      
      <div className="cot-timeline">
        {steps.map((step, index) => (
          <div key={step.step_id} className="cot-step">
            <div className="cot-step-connector">
              <div className="cot-dot">{index + 1}</div>
              {index < steps.length - 1 && <div className="cot-line" />}
            </div>
            
            <div className="cot-step-content">
              <div className="cot-iteration">Iteration {step.iteration}</div>
              <div className="cot-thought">"{step.thought}"</div>
              <div className="cot-action">
                <span className="action-badge">{step.action}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

### Phase 9: Child Agent Visibility

**Modified: `rlm/agents/base/swarm_agent.py`**

When an agent spawns a child, the child needs to be registered and have its loop tracked:

```python
def spawn_child(self, task, backend=None, environment=None, agent_id=None) -> "SwarmAgent":
    child_id = agent_id or f"{self.id}-child-{len(self.child_agent_ids)}"
    
    child = SwarmAgent(
        agent_id=child_id,
        config=self._create_child_config(),
        parent_id=self.id,
        task=task,
        loop_callbacks=self._create_child_callbacks(child_id)
    )
    
    # Register with Redux for visibility
    if self.store:
        self.store.dispatch(AgentLoopActions.register_agent(
            agent_id=child_id,
            agent_name=f"Child of {self.id}",
            parent_id=self.id,
            depth=self.depth + 1,
            task=task
        ))
    
    # Track spawning event
    self.store.dispatch(AgentLoopActions.agent_spawned(
        parent_agent_id=self.id,
        child_agent_id=child_id,
        reason="Task delegation"
    ))
    
    return child
```

## Data Flow Summary

```
1. RLM.completion() starts
   └─▶ Registers callbacks with AgentLoopCallbacks handler

2. Each iteration:
   ├─▶ on_iteration_start → Redux: iteration_started
   ├─▶ lm_handler.completion() → LLMCallRecord → Redux: llm_call_completed
   │   └─▶ Prompt + Response captured in full
   ├─▶ REPL.execute_code() → REPLExecutionRecord → Redux: repl_execution_completed
   │   └─▶ Code + stdout/stderr + success/failure captured
   ├─▶ Chain-of-thought extraction → ChainThoughtStep → Redux
   └─▶ on_iteration_complete → Redux: iteration_completed

3. If subcall (spawn):
   ├─▶ on_subcall_start → Redux: llm_call_started (type=subcall)
   │   └─▶ Child RLM repeats from step 1 with parent_call_id set
   └─▶ on_subcall_complete → Redux: llm_call_completed

4. Redux state changes → WebSocket → React UI updates in real-time

5. All data persisted to SQLite for history viewing
```

## File Changes Summary

| File | Change |
|------|--------|
| `rlm/redux/slices/agent_loop_slice.py` | **NEW** - Complete Redux slice for agent loop |
| `rlm/redux/middleware/agent_loop_middleware.py` | **NEW** - Callback handler wiring |
| `rlm/redux/middleware/agent_loop_websocket.py` | **NEW** - WebSocket server |
| `rlm/storage/agent_loop_storage.py` | **NEW** - SQLite persistence |
| `rlm/utils/chain_of_thought.py` | **NEW** - CoT extraction utilities |
| `rlm/core/rlm.py` | **MODIFY** - Add full LLM I/O capture in `_completion_turn` |
| `rlm/environments/local_repl.py` | **MODIFY** - Add execution tracking callback |
| `rlm/agents/base/swarm_agent.py` | **MODIFY** - Register child agents with Redux |
| `rlm/redux/store.py` | **MODIFY** - Add agent_loop slice |
| `ui/src/components/AgentLoopExplorer/` | **NEW** - React UI components |

## Key Design Decisions

1. **WebSocket for real-time updates** - Push-based, low latency for live streaming (as confirmed by user)

2. **SQLite storage enabled by default** - All agent loop data persisted automatically for history inspection (as confirmed by user)

3. **Callbacks over direct Redux imports**: RLM shouldn't import Redux directly. Use callback pattern so RLM is reusable.

4. **Redux for live, SQLite for history**: Redux holds live state (limited buffer), SQLite holds full history (unlimited).

5. **Streaming mode toggle**: Users can pause live updates to avoid overwhelming the UI.

6. **Full prompt/response capture**: Unlike current implementation which only has prompt preview, we capture full prompts.

7. **Per-agent isolation**: Each agent's loop state is isolated but visible in aggregate.

8. **Hierarchical call tracking**: `parent_call_id` links nested LLM calls (e.g., llm_query within a REPL block).

## Usage Example

```python
# Creating an RLM with full observability
from rlm.redux.store import create_store
from rlm.redux.middleware.agent_loop_middleware import create_loop_handler

store = create_store()
loop_handler = create_loop_handler(store, agent_id="main-1", agent_name="Main Agent")

rlm = RLM(
    backend="openai",
    on_subcall_start=loop_handler.on_subcall_start,
    on_subcall_complete=loop_handler.on_subcall_complete,
    on_iteration_start=loop_handler.on_iteration_start,
    on_iteration_complete=loop_handler.on_iteration_complete,
)

# Run the agent
result = rlm.completion("Analyze this dataset")

# View results in UI (connects via WebSocket)
# Or query history from SQLite
history = AgentLoopStorage().get_agent_history("main-1")
print(f"Total LLM calls: {len(history['llm_calls'])}")
print(f"Total REPL executions: {len(history['repl_executions'])}")
```
