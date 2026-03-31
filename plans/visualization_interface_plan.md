# Interactive Operations Console Plan for Self-Improving Swarm System

**Document Version:** 2.0  
**Last Updated:** 2026-03-26  
**Status:** Redesigned from visualization-only to operational control interface

---

## Overview

This document describes the **Interactive Operations Console** - the primary interface for human-in-the-loop control of an autonomous multi-agent swarm system. Unlike a passive visualization dashboard, this console serves as an **active control panel** that enables users and orchestrating agents to:

1. **Supervise** - Monitor autonomous swarm operation
2. **Intervene** - Modify agent behavior when needed
3. **Approve** - Respond to agent permission requests
4. **Configure** - Adjust system routing and parameters
5. **Communicate** - Exchange messages with agents
6. **Submit** - Feed new tasks to the swarm

**Design Philosophy**: Every control should be available at multiple granularities (global, group, agent, type), with sensible defaults for autonomous operation that can be overridden at any level in real-time.

---

## Design Principles

### 1. Modularity First
- No hardcoded flows - user/orchestrator can create custom interaction patterns
- Every setting operates at multiple scopes: Global → Group → Agent → Type
- Settings cascade but can be overridden at any granular level

### 2. Bidirectional State
- UI reflects system state (Redux store → UI)
- UI updates system state (UI → Redux dispatch → system)
- Every visible action can be triggered by user OR orchestrator agent

### 3. CLI-Fashion Interaction
- Keyboard-first with vim-style shortcuts
- Approvals: [Y]es, [N]o, [D]on't ask again, [A]sk always
- Clear visual feedback for all actions

### 4. Autonomous by Default
- System runs with minimal human-in-the-loop
- User sets preferences → system respects them autonomously
- Human intervention needed only for exceptions

### 5. Session Persistence
- All state saved for crash recovery
- `--resume <session-id>` to restore prior session
- Configurable retention limits to prevent memory exhaustion

---

## Scope Hierarchy

Every control operates within this hierarchy:

```
GLOBAL (system-wide default)
  │
  ├── GROUP (agent group)
  │     │
  │     └── AGENT (specific agent)
  │
  ├── TYPE (task/message type)
  │     │
  │     └── INSTANCE (specific task/message)
  │
  └── INSTANCE (specific task/message)
```

**Resolution Order**: Instance → Agent → Group → Type → Global

**Example**: If "pause" is set to "ask" globally, but "allow" for agent #42 specifically, agent #42 will auto-pause without asking.

---

## Core Interface Panels

### Panel 1: Task Submission Console

**Purpose**: Submit new tasks to the swarm for processing

**Components**:
- Rich text task input (markdown supported)
- Task classification display (from `TaskDescriptor.classify_intent()`)
- Complexity estimate (from `TaskDescriptor.estimate_complexity()`)
- Routing preference selector (backend, environment, mode)
- Priority slider (1-10)
- Docker isolation toggle (from `TaskDescriptor.needs_docker_isolation()`)
- Constraint specification (token limit, timeout, etc.)

**CLI Actions**:
```
[task]$ submit "Prove theorem about prime gaps"
[task]$ submit "Analyze dataset X with priority=8"
[task]$ routing --backend=openai/gpt-4 --env=modal
[task]$ constraints --max-tokens=32000 --timeout=300s
```

**Redux Integration**:
```typescript
// Dispatched actions
tasks/submitTask({ description, priority, routing, constraints })
tasks/setRoutingPreference({ backend?, environment?, mode? })
tasks/setConstraints({ maxTokens?, timeout?, docker? })

// State subscription
interface TaskSubmissionState {
  currentDraft: TaskDescriptor | null;
  classification: { intent: string; confidence: number } | null;
  complexity: { level: string; depth: number; tokens: number } | null;
  routingPreference: { backend?: string; environment?: string; mode?: string };
  constraints: { maxTokens?: number; timeout?: number; docker?: boolean };
}
```

---

### Panel 2: Permission Request Queue

**Purpose**: Handle agent requests for restricted operations (tool creation, network access, agent spawning, etc.)

**Components**:
- Queue of pending permission requests
- Request details (who, what, why, risk assessment)
- Approval action buttons
- Request history with outcomes

**CLI Approval Actions**:
```
[perm]$ list --pending
[perm]$ approve <request-id> [Y]
[perm]$ deny <request-id> [N]
[perm]$ dont-ask-again <request-id> [D]  // Remember for this TYPE
[perm]$ always-ask <request-id> [A]      // Never memorize for this TYPE
[perm]$ set-default --type=<type> --action=[approve|deny|ask]
```

**Approval Options**:
| Key | Action | Effect |
|-----|--------|--------|
| `Y` | Yes | Approve this request |
| `N` | No | Deny this request |
| `D` | Don't ask again | Remember preference for this TYPE (future auto-action) |
| `A` | Ask always | Never memorize, always prompt for this TYPE |

**Redux Integration**:
```typescript
// Dispatched actions
permissions/approveRequest({ requestId, remember?: boolean })
permissions/denyRequest({ requestId, reason?: string })
permissions/setDefault({ type, action: 'approve' | 'deny' | 'ask' })
permissions/setDefaultScope({ type, scope: 'global' | 'group' | 'agent' | 'type', scopeId?: string })

// State subscription
interface PermissionState {
  pendingRequests: PermissionRequest[];
  defaults: Record<string, 'approve' | 'deny' | 'ask'>;  // by type
  history: PermissionRecord[];
}
```

---

### Panel 3: Tool Review Interface

**Purpose**: Review and approve/deny dynamically created tools

**Components**:
- Code viewer with syntax highlighting
- Security scan results
- Compatibility information (languages, backends, environments)
- Creator agent info
- Approval/rejection actions

**CLI Actions**:
```
[tool]$ list --pending
[tool]$ review <tool-id>
[tool]$ approve <tool-id> [--scope=global|group|agent]
[tool]$ reject <tool-id> --reason="<text>"
[tool]$ sandbox-test <tool-id>  // Run in isolated environment
```

**Redux Integration**:
```typescript
// Dispatched actions
tools/approveTool({ toolId, scope?: 'global' | 'group' | 'agent', scopeId?: string })
tools/rejectTool({ toolId, reason: string })
tools/setToolDefault({ toolType, action: 'approve' | 'reject' | 'ask' })

// State subscription
interface ToolApprovalState {
  pendingTools: ToolDefinition[];
  approvedTools: string[];
  rejectedTools: string[];
  defaults: Record<string, 'approve' | 'reject' | 'ask'>;
}
```

---

### Panel 4: Improvement Review System

**Purpose**: Evaluate and act on system improvement proposals

**Components**:
- Side-by-side diff viewer
- Impact analysis display
- Dependencies visualization
- Test results (before/after metrics)
- Approval/rejection with reasoning

**CLI Actions**:
```
[improve]$ list --pending
[improve]$ review <improvement-id>
[improve]$ approve <improvement-id> [--apply-now]
[improve]$ reject <improvement-id> --reason="<text>"
[improve]$ rollback <improvement-id>
[improve]$ set-default --category=<cat> --action=[approve|reject|ask]
```

**Redux Integration**:
```typescript
// Dispatched actions
improvements/approveImprovement({ improvementId, applyNow?: boolean })
improvements/rejectImprovement({ improvementId, reason: string })
improvements/rollbackImprovement({ improvementId })
improvements/setDefault({ category, action: 'approve' | 'reject' | 'ask' })

// State subscription
interface ImprovementState {
  pendingApprovals: ImprovementEntity[];
  activeImprovements: string[];
  defaults: Record<string, 'approve' | 'reject' | 'ask'>;
}
```

---

### Panel 5: Routing Control Panel

**Purpose**: Monitor and override backend/environment routing decisions

**Connected Modules**:
- `backend_router.py` - `route()`, `record_call()`, `get_backend_metrics()`
- `environment_router.py` - `route()`, `_build_features_dict()`
- `task_descriptor.py` - `classify_intent()`, `needs_docker_isolation()`, `estimate_complexity()`

**Components**:
- Backend metrics dashboard (from `BackendMetrics`)
- Current routing state display
- Environment mode indicator
- Data sensitivity classification
- Override controls

**CLI Actions**:
```
[route]$ list-backends
[route]$ metrics <backend-id>
[route]$ override <backend-id> --scope=[O|P|T] --target=[G|A] [--filter=<filter>]
[route]$ set-default --backend=<id> --scope=[G|A|I|T]
[route]$ show-history --agent=<id>|--task=<id>|--all
```

**Override Scope Options**:
| Flag | Meaning | Description |
|------|---------|-------------|
| `O` | One-time | Apply just this task, revert after |
| `P` | Persistent | Make this the new default |
| `T` | Temporary | Revert after N tasks (prompt for N) |

**Override Target Options**:
| Flag | Meaning | Description |
|------|---------|-------------|
| `G` | Global | Apply system-wide |
| `A` | Agent | Apply to specific agent only |
| `I` | Individual | Apply to specific agent instance |
| `T` | Type | Apply to task type only |

**Redux Integration**:
```typescript
// Dispatched actions
routing/overrideRoute({ backendId, scope: 'one-time' | 'persistent' | 'temporary', scopeTarget: string, filter?: object })
routing/setDefault({ backendId, scope: 'global' | 'agent' | 'group' | 'type', scopeId?: string })
routing/recordCall({ backendId, success: boolean, latency: number })

// State subscription
interface RoutingState {
  currentRoute: {
    backend: string;
    environment: string;
    mode: 'local' | 'modal';
    dataSensitivity: 'public' | 'internal' | 'restricted';
  };
  backends: Record<string, BackendMetrics>;
  history: RoutingRecord[];
  defaults: {
    global?: string;
    byAgent: Record<string, string>;
    byType: Record<string, string>;
  };
  temporaryOverrides: TemporaryOverride[];
}

interface BackendMetrics {
  total_calls: number;
  success_count: number;
  failure_count: number;
  total_latency: number;
  avg_latency: number;
  last_used: number;
}
```

---

### Panel 6: Verification Control Panel

**Purpose**: Monitor and trigger Layer 1 theorem verification

**Connected Modules**:
- `verification_slice.py` - `verify_theorem_request` handler
- `verification_middleware.py` - `Layer1Bootstrap`, `VerificationAgentFactory`
- `layer1_bootstrap.py` - Lean kernel, PhysLib, Haskell loading

**Components**:
- Verification queue (pending, in-progress, verified, failed)
- Layer1 bootstrap status (Lean, PhysLib, Haskell)
- Resource usage display (from `psutil`)
- Verification progress tracker
- Theorem submission form

**CLI Actions**:
```
[verify]$ list [--status=pending|in-progress|verified|failed]
[verify]$ submit "<theorem-text>"
[verify]$ status <theorem-id>
[verify]$ cancel <theorem-id>
[verify]$ layer1-status
[verify]$ resources
```

**Redux Integration**:
```typescript
// Dispatched actions
verification/verifyTheoremRequest({ theoremId, theoremText, priority?: number })
verification/cancelVerification({ theoremId })
verification/setLayer1BootstrapStatus({ lean: Status, physlib: Status, haskell: Status })

// State subscription
interface VerificationState {
  status: 'PENDING' | 'IN_PROGRESS' | 'VERIFIED' | 'FAILED';
  activeVerification: string | null;
  verificationQueue: string[];
  layer1Status: {
    lean: 'loading' | 'loaded' | 'error';
    physlib: 'loading' | 'loaded' | 'error';
    haskell: 'loading' | 'loaded' | 'error';
  };
  resourceUsage: {
    cpuPercent: number;
    memoryMB: number;
  };
  theorems: Record<string, TheoremRecord>;
}
```

---

### Panel 7: Agent Communication Console

**Purpose**: Direct messaging with agents, conversation threads

**Components**:
- Agent list with status indicators
- Active conversation threads
- Message composer
- Message history with search/filter
- Typing indicators

**CLI Actions**:
```
[msg]$ list-agents [--status=running|paused|idle]
[msg]$ thread <agent-id>
[msg]$ send <agent-id> "<message>"
[msg]$ broadcast "<message>" [--to=group|all]
[msg]$ history <agent-id> [--limit=50]
[msg]$ search "<query>" [--agent=<id>] [--type=incoming|outgoing]
```

**Redux Integration**:
```typescript
// Dispatched actions
messages/sendMessage({ recipientId, content, priority?: 'low' | 'normal' | 'high' | 'critical' })
messages/broadcastMessage({ content, recipients: 'all' | 'group', groupId?: string })
messages/markRead({ messageId })

// State subscription
interface MessageState {
  threads: Record<string, MessageThread>;  // keyed by agentId
  inbox: Record<string, MessageEntity[]>;
  outbox: MessageEntity[];
  unreadCounts: Record<string, number>;
  retention: {
    maxThreads: number;        // default: 50
    autoArchiveAfter: number;  // default: 10 sessions
    persistAll: boolean;
  };
}
```

---

### Panel 8: Intervention Controls

**Purpose**: Emergency and operational control over agent execution

**Components**:
- Pause/Resume controls (granular targeting)
- Terminate controls
- Emergency stop (all agents)
- Activity timeline
- Undo capability

**CLI Actions**:
```
[ctrl]$ pause --target=[A|G|I|T] [--id=<id>] [--duration=U|T:<minutes>]
[ctrl]$ resume --target=[A|G|I|T] [--id=<id>]
[ctrl]$ terminate --target=[A|G|I|T] [--id=<id>] [--force]
[ctrl]$ stop-all  // Emergency halt
[ctrl]$ undo      // Revert last action
[ctrl]$ timeline  // Show intervention history
```

**Pause/Resume Target Options**:
| Flag | Meaning | Description |
|------|---------|-------------|
| `A` | All | Entire swarm |
| `G` | Group | Specific agent group |
| `I` | Individual | Specific agent by ID |
| `T` | Type | By task/message type |

**Pause Duration Options**:
| Flag | Meaning | Description |
|------|---------|-------------|
| `U` | Until resumed | Manual resume required |
| `T:<N>` | Timed | Auto-resume after N minutes |

**Redux Integration**:
```typescript
// Dispatched actions
agents/pauseAgent({ target: 'all' | 'group' | 'individual' | 'type', targetId?: string, duration?: number })
agents/resumeAgent({ target: 'all' | 'group' | 'individual' | 'type', targetId?: string })
agents/terminateAgent({ agentId, force?: boolean })
system/emergencyStop()

// State subscription
interface InterventionState {
  pausedAgents: string[];      // agent IDs currently paused
  pausedGroups: string[];      // group IDs currently paused
  pausedTypes: string[];       // task types currently paused
  allPaused: boolean;
  lastAction: InterventionAction | null;
  timeline: InterventionRecord[];
}
```

---

### Panel 9: System Configuration

**Purpose**: Runtime adjustment of system parameters

**Components**:
- Resource limits editor
- Security settings
- Backend configuration
- Notification preferences
- Performance tuning

**CLI Actions**:
```
[config]$ get [--key=<path>]
[config]$ set --key=<path> --value=<value>
[config]$ export  // Export current config
[config]$ import  // Import config file
[config]$ reset   // Reset to defaults
[config]$ diff     // Show pending changes
```

**Configuration Hierarchy**:
```
system
├── resourceLimits
│   ├── cpu: number
│   ├── memory: number
│   └── tokens: number
├── security
│   ├── messageValidation: boolean
│   ├── toolApprovalRequired: boolean
│   └── agentIsolation: boolean
├── performance
│   ├── messageBatchSize: number
│   ├── stateUpdateInterval: number
│   └── cleanupInterval: number
├── realtime
│   ├── mode: 'websocket' | 'polling'
│   ├── pollInterval: number
│   └── perPanelMode: Record<PanelId, 'websocket' | 'polling'>
└── retention
    ├── maxThreads: number
    ├── autoArchiveAfter: number
    └── persistAll: boolean
```

**Redux Integration**:
```typescript
// Dispatched actions
system/updateConfiguration({ path: string, value: any })
system/resetConfiguration()
system/exportConfiguration()
system/importConfiguration({ config: SystemConfiguration })

// State subscription
interface SystemConfiguration {
  resourceLimits: { cpu: number; memory: number; tokens: number };
  security: { messageValidation: boolean; toolApprovalRequired: boolean; agentIsolation: boolean };
  performance: { messageBatchSize: number; stateUpdateInterval: number; cleanupInterval: number };
  realtime: { mode: 'websocket' | 'polling'; pollInterval: number; perPanelMode: Record<string, string> };
  retention: { maxThreads: number; autoArchiveAfter: number; persistAll: boolean };
}
```

---

## Real-Time Updates

### WebSocket Push (Default)
- Persistent connection from browser to server
- Server pushes state changes immediately
- Best for time-sensitive operations (permissions, verification status)

### Polling (Fallback Option)
- Browser requests state every N milliseconds
- Configurable per-panel
- Useful when WebSocket unavailable or for non-critical panels

### Configuration
```typescript
interface RealtimeConfig {
  mode: 'websocket' | 'polling';
  pollInterval: number;  // milliseconds, default: 1000
  perPanel: {
    'permission-queue': 'websocket' | 'polling';
    'verification': 'websocket' | 'polling';
    'agent-communication': 'websocket' | 'polling';
    'routing': 'polling';  // less time-sensitive
    'tool-review': 'polling';  // less time-sensitive
    // ... other panels
  };
}
```

---

## Session Persistence

### Auto-Save
- All state saved to disk every 30 seconds
- Crash recovery via `--resume <session-id>`

### Resume Flow
```
$ self-ai --resume 2026-03-26--22-45-30
Loading session 2026-03-26--22-45-30...
Restored: 3 agents, 12 messages, 2 pending permissions
Console ready.
```

### Retention Settings
| Setting | Default | Description |
|---------|---------|-------------|
| `maxThreads` | 50 | Max agent conversation threads to keep |
| `autoArchiveAfter` | 10 | Auto-archive after N sessions |
| `persistAll` | false | Never delete (warning: disk usage) |

---

## Implemented Components Reference

This console connects to these **implemented and passing** modules:

| Module | File | Connected Panels |
|--------|------|------------------|
| BackendRouter | `rlm/routing/backend_router.py` | Routing Control, Dashboard |
| EnvironmentRouter | `rlm/routing/environment_router.py` | Routing Control |
| TaskDescriptor | `rlm/routing/task_descriptor.py` | Task Submission, Routing Control |
| RoutingSlice | `rlm/redux/slices/routing_slice.py` | Routing Control |
| VerificationSlice | `rlm/redux/slices/verification_slice.py` | Verification Control |
| VerificationMiddleware | `rlm/redux/middleware/verification_middleware.py` | Verification Control |
| Layer1Bootstrap | `rlm/environments/layer1_bootstrap.py` | Verification Control |

---

## Component Hierarchy

```
InteractiveOperationsConsole
├── Header
│   ├── Logo
│   ├── SessionInfo
│   └── GlobalControls
│
├── CommandBar  // CLI-style input
│   ├── ModeIndicator
│   ├── CommandInput
│   └── QuickActions
│
├── MainPanel (tabbed/split view)
│   ├── TaskSubmissionConsole
│   ├── PermissionRequestQueue
│   ├── ToolReviewInterface
│   ├── ImprovementReviewSystem
│   ├── RoutingControlPanel
│   ├── VerificationControlPanel
│   ├── AgentCommunicationConsole
│   ├── InterventionControls
│   └── SystemConfiguration
│
├── StatusBar
│   ├── SystemHealth
│   ├── ActiveAgents
│   ├── RealtimeIndicator
│   └── NotificationCount
│
└── SlideOutPanels (contextual)
    ├── AgentDetailPanel
    ├── MessageDetailPanel
    └── DiffViewerPanel
```

---

## Keyboard Shortcuts

### Global
| Key | Action |
|-----|--------|
| `Ctrl+K` | Open command palette |
| `Ctrl+S` | Save session |
| `Ctrl+Z` | Undo last action |
| `Esc` | Close modal/panel |

### Navigation
| Key | Action |
|-----|--------|
| `1-9` | Switch to panel N |
| `g` | Go to... (jump to agent/task) |
| `/` | Search |
| `j/k` | Next/previous item (vim-style) |

### Approvals (when in approval mode)
| Key | Action |
|-----|--------|
| `Y` | Yes/Approve |
| `N` | No/Deny |
| `D` | Don't ask again |
| `A` | Ask always |

---

## Technical Requirements

### Performance
- WebSocket connection management with automatic reconnection
- Lazy loading for message/verification history
- Virtual scrolling for large lists (100+ agents)
- Debounced state updates to prevent UI thrashing

### Scalability
- Handle 100+ simultaneous agents
- Efficient state selectors to minimize re-renders
- Message batching for high-throughput scenarios

### Integration
- Full Redux store connection (all slices)
- WebSocket server for real-time push
- REST API fallback for configuration
- Session persistence to filesystem

---

## Implementation Priority

### Phase 1: Core Infrastructure
1. Redux store connection for all slices
2. WebSocket server and client
3. Session persistence system
4. Command bar with basic navigation

### Phase 2: Essential Panels
1. Task Submission Console
2. Intervention Controls (pause/resume/terminate)
3. Routing Control Panel
4. System Configuration

### Phase 3: Approval Workflows
1. Permission Request Queue
2. Tool Review Interface
3. Improvement Review System

### Phase 4: Communication
1. Agent Communication Console
2. Verification Control Panel

---

## Section 14: Visual Design Specification

### 14.1 CSS Custom Properties

#### Light Theme
```css
:root {
  /* Surface Colors */
  --surface-primary: #ffffff;
  --surface-secondary: #f8fafc;
  --surface-tertiary: #f1f5f9;
  --surface-elevated: #ffffff;
  --surface-overlay: rgba(0, 0, 0, 0.5);
  
  /* Text Colors */
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-tertiary: #94a3b8;
  --text-inverse: #ffffff;
  --text-link: #2563eb;
  --text-link-hover: #1d4ed8;
  
  /* Border Colors */
  --border-default: #e2e8f0;
  --border-hover: #cbd5e1;
  --border-focus: #2563eb;
  --border-strong: #94a3b8;
  
  /* Accent Colors */
  --accent-primary: #2563eb;
  --accent-primary-hover: #1d4ed8;
  --accent-secondary: #7c3aed;
  --accent-success: #16a34a;
  --accent-warning: #ca8a04;
  --accent-danger: #dc2626;
  --accent-info: #0891b2;
  
  /* Status Colors */
  --status-pending: #f59e0b;
  --status-running: #22c55e;
  --status-paused: #6366f1;
  --status-failed: #ef4444;
  --status-verified: #10b981;
  --status-idle: #6b7280;
  
  /* Panel Colors */
  --panel-task: #dbeafe;
  --panel-permission: #fef3c7;
  --panel-tool: #f3e8ff;
  --panel-improve: #dcfce7;
  --panel-route: #e0e7ff;
  --panel-verify: #ccfbf1;
  --panel-message: #fce7f3;
  --panel-control: #fee2e2;
  --panel-config: #f1f5f9;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  
  /* Focus Ring */
  --focus-ring: 0 0 0 3px rgba(37, 99, 235, 0.3);
  --focus-ring-danger: 0 0 0 3px rgba(220, 38, 38, 0.3);
}
```

#### Dark Theme
```css
[data-theme="dark"] {
  /* Surface Colors */
  --surface-primary: #0f172a;
  --surface-secondary: #1e293b;
  --surface-tertiary: #334155;
  --surface-elevated: #1e293b;
  --surface-overlay: rgba(0, 0, 0, 0.7);
  
  /* Text Colors */
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-tertiary: #64748b;
  --text-inverse: #0f172a;
  --text-link: #60a5fa;
  --text-link-hover: #93c5fd;
  
  /* Border Colors */
  --border-default: #334155;
  --border-hover: #475569;
  --border-focus: #60a5fa;
  --border-strong: #64748b;
  
  /* Accent Colors */
  --accent-primary: #3b82f6;
  --accent-primary-hover: #60a5fa;
  --accent-secondary: #a78bfa;
  --accent-success: #22c55e;
  --accent-warning: #eab308;
  --accent-danger: #f87171;
  --accent-info: #22d3ee;
  
  /* Status Colors (remain vibrant for visibility) */
  --status-pending: #fbbf24;
  --status-running: #4ade80;
  --status-paused: #818cf8;
  --status-failed: #f87171;
  --status-verified: #34d399;
  --status-idle: #9ca3af;
  
  /* Panel Colors (muted in dark mode) */
  --panel-task: #1e3a5f;
  --panel-permission: #3d2e1e;
  --panel-tool: #2e1d3d;
  --panel-improve: #1a3d2e;
  --panel-route: #1e2d5f;
  --panel-verify: #1a3d3d;
  --panel-message: #3d1a2e;
  --panel-control: #3d1a1a;
  --panel-config: #1e293b;
  
  /* Shadows (darker for depth) */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
  
  /* Focus Ring */
  --focus-ring: 0 0 0 3px rgba(59, 130, 246, 0.4);
  --focus-ring-danger: 0 0 0 3px rgba(248, 113, 113, 0.4);
}
```

---

### 14.2 Typography Scale

```css
:root {
  /* Font Families */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  --font-serif: 'Georgia', 'Times New Roman', serif;
  
  /* Font Sizes */
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;      /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
  --text-4xl: 2.25rem;     /* 36px */
  
  /* Line Heights */
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  
  /* Font Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  
  /* Letter Spacing */
  --tracking-tighter: -0.05em;
  --tracking-tight: -0.025em;
  --tracking-normal: 0;
  --tracking-wide: 0.025em;
  --tracking-wider: 0.05em;
}
```

**Type Scale for Console:**
```css
:root {
  /* CLI Command Line */
  --cli-prompt: var(--font-mono) var(--text-sm);
  --cli-input: var(--font-mono) var(--text-base);
  --cli-output: var(--font-mono) var(--text-sm);
  
  /* Panel Headers */
  --panel-title: var(--font-sans) var(--font-semibold) var(--text-xl);
  --panel-subtitle: var(--font-sans) var(--font-medium) var(--text-sm);
  
  /* Body Text */
  --body-large: var(--font-sans) var(--font-normal) var(--text-lg);
  --body-base: var(--font-sans) var(--font-normal) var(--text-base);
  --body-small: var(--font-sans) var(--font-normal) var(--text-sm);
  
  /* Labels */
  --label: var(--font-sans) var(--font-medium) var(--text-sm);
  --label-small: var(--font-sans) var(--font-medium) var(--text-xs);
  
  /* Status/Badge Text */
  --badge: var(--font-sans) var(--font-semibold) var(--text-xs);
}
```

---

### 14.3 Spacing Tokens

```css
:root {
  /* Base Spacing Unit: 4px */
  --space-0: 0;
  --space-px: 1px;
  --space-0-5: 0.125rem;  /* 2px */
  --space-1: 0.25rem;     /* 4px */
  --space-1-5: 0.375rem;  /* 6px */
  --space-2: 0.5rem;      /* 8px */
  --space-2-5: 0.625rem; /* 10px */
  --space-3: 0.75rem;     /* 12px */
  --space-3-5: 0.875rem; /* 14px */
  --space-4: 1rem;        /* 16px */
  --space-5: 1.25rem;     /* 20px */
  --space-6: 1.5rem;      /* 24px */
  --space-7: 1.75rem;     /* 28px */
  --space-8: 2rem;        /* 32px */
  --space-9: 2.25rem;    /* 36px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;       /* 48px */
  --space-14: 3.5rem;    /* 56px */
  --space-16: 4rem;       /* 64px */
  --space-20: 5rem;       /* 80px */
  
  /* Semantic Spacing */
  --space-xs: var(--space-1);
  --space-sm: var(--space-2);
  --space-md: var(--space-4);
  --space-lg: var(--space-6);
  --space-xl: var(--space-8);
  --space-2xl: var(--space-12);
  
  /* Component-Specific */
  --panel-padding: var(--space-4);
  --panel-gap: var(--space-4);
  --panel-header-gap: var(--space-3);
  --item-gap: var(--space-2);
  --icon-gap: var(--space-2);
  --button-padding-x: var(--space-4);
  --button-padding-y: var(--space-2);
  
  /* Border Radius */
  --radius-none: 0;
  --radius-sm: 0.125rem;
  --radius-default: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-full: 9999px;
}
```

---

### 14.4 Component Specifications

#### 14.4.1 Command Bar

```
┌─────────────────────────────────────────────────────────────────┐
│ [mode] > █                                                     │
└─────────────────────────────────────────────────────────────────┘

Width: 100% of container
Height: 48px
Padding: var(--space-3) var(--space-4)
Background: var(--surface-primary)
Border: 1px solid var(--border-default)
Border-radius: var(--radius-lg)
Font: var(--cli-input)
```

**Mode Indicator Colors:**
| Mode | Background | Text |
|------|------------|------|
| `task` | var(--panel-task) | var(--accent-primary) |
| `perm` | var(--panel-permission) | var(--accent-warning) |
| `tool` | var(--panel-tool) | var(--accent-secondary) |
| `improve` | var(--panel-improve) | var(--accent-success) |
| `route` | var(--panel-route) | var(--accent-primary) |
| `verify` | var(--panel-verify) | var(--accent-info) |
| `msg` | var(--panel-message) | #db2777 |
| `ctrl` | var(--panel-control) | var(--accent-danger) |
| `config` | var(--panel-config) | var(--text-secondary) |

#### 14.4.2 Panel Card

```
┌─ Panel Title ─────────────────────────────────────┄─────────────▄┐
│                                                                 │
│  Content area with padding var(--panel-padding)                │
│                                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Background: var(--surface-secondary)
Border: 1px solid var(--border-default)
Border-radius: var(--radius-xl)
Header padding: var(--space-3) var(--space-4)
Content padding: var(--space-4)
Shadow: var(--shadow-md)
```

#### 14.4.3 Approval Button Group

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   [Y]   │  │   [N]   │  │    [D]      │  │     [A]     │  │
│  │  Yes    │  │   No    │  │ Don't ask   │  │ Ask always  │  │
│  └─────────┘  └─────────┘  └─────────────┘  └─────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘

Button Size: 80px × 64px
Gap: var(--space-3)
Border-radius: var(--radius-lg)
Font: var(--badge)
```

**Button States:**
| State | Background | Border | Text |
|-------|------------|--------|------|
| Default | var(--surface-primary) | var(--border-default) | var(--text-primary) |
| Hover | var(--accent-success) | transparent | white |
| Active/Pressed | var(--accent-success) | transparent | white |
| Focus | var(--focus-ring) | - | - |

**Per-Button Colors:**
| Button | Hover Background |
|--------|------------------|
| Y/Yes | var(--accent-success) |
| N/No | var(--accent-danger) |
| D/Don't ask | var(--accent-warning) |
| A/Ask always | var(--accent-info) |

#### 14.4.4 Status Badge

```
● Running    ○ Idle    ◐ Paused    ✕ Failed    ✓ Verified

Shape: pill (border-radius: var(--radius-full))
Padding: var(--space-1) var(--space-3)
Font: var(--badge)
```

**Status Badge Colors:**
| Status | Light Mode | Dark Mode |
|--------|------------|-----------|
| Pending | `#f59e0b` on `#fef3c7` | `#fbbf24` on `#3d2e1e` |
| Running | `#16a34a` on `#dcfce7` | `#4ade80` on `#1a3d2e` |
| Paused | `#6366f1` on `#e0e7ff` | `#818cf8` on `#1e2d5f` |
| Failed | `#dc2626` on `#fee2e2` | `#f87171` on `#3d1a1a` |
| Verified | `#10b981` on `#d1fae5` | `#34d399` on `#1a3d3d` |
| Idle | `#6b7280` on `#f3f4f6` | `#9ca3af` on `#1e293b` |

#### 14.4.5 Intervention Controls

**Emergency Stop Button:**
```
┌──────────────────────┐
│    ■ STOP ALL        │
└──────────────────────┘

Width: 120px
Height: 48px
Background: var(--accent-danger)
Color: white
Border-radius: var(--radius-lg)
Font: var(--font-bold) var(--text-base)
Hover: darken 10%
Active: darken 15%
```

**Pause/Resume Toggle:**
```
┌──────────────────────┐
│    ⏸ PAUSE           │
│    ▶ RESUME          │
└──────────────────────┘

Width: 100px
Height: 40px
Background: var(--status-paused)
Color: white
Border-radius: var(--radius-md)
Font: var(--font-semibold) var(--text-sm)
```

#### 14.4.6 Input Fields

```
┌─────────────────────────────────────┐
│ Label                               │
│ ┌─────────────────────────────────┐ │
│ │ Input value                     │ │
│ └─────────────────────────────────┘ │
│ Helper text                         │
└─────────────────────────────────────┘

Height: 40px
Padding: var(--space-2) var(--space-3)
Border: 1px solid var(--border-default)
Border-radius: var(--radius-md)
Background: var(--surface-primary)
Font: var(--body-base)
Label: var(--label)
Helper: var(--text-tertiary) var(--text-sm)
```

**States:**
| State | Border Color | Shadow |
|-------|--------------|--------|
| Default | var(--border-default) | none |
| Hover | var(--border-hover) | none |
| Focus | var(--border-focus) | var(--focus-ring) |
| Error | var(--accent-danger) | var(--focus-ring-danger) |
| Disabled | var(--border-default) | none, opacity: 0.5 |

#### 14.4.7 Timeline Component

```
●─── Agent #42 paused by user (2s ago)
│
●─── Task #128 routed to backend/openai (5s ago)
│
●─── Permission "create_tool" denied (10s ago)
```

**Timeline Dot:** 12px diameter circle  
**Timeline Line:** 2px wide, var(--border-default)  
**Entry Padding:** var(--space-3) vertical  
**Entry Text:** var(--body-small)  
**Timestamp:** var(--text-tertiary) var(--text-xs)

---

### 14.5 Responsive Breakpoints

```css
/* Mobile (single column, stacked panels) */
@media (max-width: 640px) {
  --panel-padding: var(--space-3);
  --cli-input: var(--font-mono) var(--text-sm);
}

/* Tablet (2-column grid) */
@media (min-width: 641px) and (max-width: 1024px) {
  --panel-grid: repeat(2, 1fr);
}

/* Desktop (3-column grid, full features) */
@media (min-width: 1025px) {
  --panel-grid: repeat(3, 1fr);
  --sidebar-width: 280px;
}
```

---

### 14.6 Animation Tokens

```css
:root {
  /* Durations */
  --duration-instant: 0ms;
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;
  --duration-slower: 600ms;
  
  /* Easing Functions */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  
  /* Transitions */
  --transition-colors: color var(--duration-fast) var(--ease-in-out),
                       background-color var(--duration-fast) var(--ease-in-out),
                       border-color var(--duration-fast) var(--ease-in-out);
  --transition-transform: transform var(--duration-normal) var(--ease-out);
  --transition-opacity: opacity var(--duration-fast) var(--ease-in-out);
}
```

---

## Future Enhancements

### Advanced Features
- Multi-user collaboration (multiple operators)
- Role-based access control
- Automated response rules (if X then Y)
- Scheduled operations

### Analytics
- Routing optimization recommendations
- Approval pattern analysis
- Performance trending
- Cost estimation by backend

### AI Integration
- Predictive intervention suggestions
- Anomaly detection for system behavior
- Natural language task submission
- Automated routine approvals

---

This Interactive Operations Console plan provides a comprehensive framework for building an interface that enables full bidirectional control of the self-improving swarm system, while respecting the modularity and autonomy principles that allow the system to operate with minimal human-in-the-loop when desired.
