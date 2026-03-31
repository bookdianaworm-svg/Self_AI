# Redux Store Design for Self-Improving Swarm System

## Store Structure

### Root State Interface

```typescript
interface SwarmRootState {
  agents: AgentSliceState;
  tasks: TaskSliceState;
  messages: MessageSliceState;
  system: SystemSliceState;
  tools: ToolSliceState;
  improvements: ImprovementSliceState;
  ui: UISliceState;
}
```

### Agent Slice

```typescript
interface AgentSliceState {
  // Map of all agents by ID
  entities: { [id: string]: AgentEntity };
  // List of all agent IDs
  ids: string[];
  // Current status of the agent system
  status: 'idle' | 'initializing' | 'running' | 'pausing' | 'paused' | 'terminating' | 'terminated';
  // ID of the main recursive instance
  mainInstanceId: string | null;
  // Statistics
  stats: AgentStats;
}

interface AgentEntity {
  id: string;
  parentId: string | null; // ID of parent agent or null for main instance
  type: 'main' | 'spawned'; // Type of agent
  status: 'idle' | 'planning' | 'executing' | 'waiting' | 'paused' | 'completed' | 'failed' | 'terminated';
  task: string; // Description of assigned task
  createdAt: number; // Timestamp
  lastUpdate: number; // Last state update timestamp
  logs: AgentLogEntry[];
  capabilities: AgentCapabilities;
  resources: ResourceAllocation;
  communication: CommunicationSettings;
  backendClient: string; // Backend client type (e.g., 'openai', 'anthropic')
  executionEnvironment: string; // Execution environment (e.g., 'local', 'docker', 'e2b')
}

interface AgentLogEntry {
  timestamp: number;
  level: 'info' | 'warning' | 'error' | 'debug' | 'improvement';
  message: string;
  data?: any;
}

interface AgentCapabilities {
  supportedLanguages: string[];
  availableTools: string[];
  executionEnvironments: string[];
  maxDepth: number; // Maximum recursion depth allowed
  selfImprovementEnabled: boolean; // Whether this agent can contribute system improvements
  backendClient: string; // Backend client type (openai, anthropropic, etc.)
}

interface ResourceAllocation {
  cpuLimit: number; // Percentage of CPU allowed
  memoryLimit: number; // MB of memory allowed
  tokenLimit: number; // Maximum tokens per request
  requestLimit: number; // Max requests per minute
  maxAgents: number; // Maximum number of agents this agent can spawn
}

interface CommunicationSettings {
  messageFrequency: number; // Min milliseconds between messages
  broadcastEnabled: boolean;
  directMessagingEnabled: boolean;
}

interface AgentStats {
  totalAgents: number;
  activeAgents: number;
  completedAgents: number;
  failedAgents: number;
  mainInstanceActive: boolean;
}
```

### Task Slice

```typescript
interface TaskSliceState {
  mainTask: string | null; // The main task assigned by the user
  subTasks: { [id: string]: SubTaskEntity };
  taskQueue: string[]; // IDs of tasks waiting to be assigned
  completedTasks: string[]; // IDs of completed tasks
  failedTasks: string[]; // IDs of failed tasks
  stats: TaskStats;
}

interface SubTaskEntity {
  id: string;
  description: string;
  assignedTo: string | null; // Agent ID or null if unassigned
  status: 'pending' | 'in-progress' | 'completed' | 'failed' | 'cancelled' | 'paused';
  priority: number; // 1-10 scale
  dependencies: string[]; // IDs of tasks this depends on
  estimatedComplexity: number; // 1-10 scale
  createdAt: number;
  startedAt: number | null;
  completedAt: number | null;
  result: any; // Result of the completed task
  error: string | null; // Error message if failed
  createdBy: string; // ID of agent that created this subtask
}

interface TaskStats {
  totalTasks: number;
  completedTasks: number;
  inProgressTasks: number;
  failedTasks: number;
  averageCompletionTime: number;
}
```

### Message Slice

```typescript
interface MessageSliceState {
  inbox: { [recipientId: string]: MessageEntity[] }; // Messages organized by recipient
  outbox: MessageEntity[]; // Outgoing messages
  history: MessageEntity[]; // Historical messages
  unreadCounts: { [recipientId: string]: number }; // Unread message counts by recipient
  filters: MessageFilters; // Current filters applied to messages
  stats: MessageStats;
}

interface MessageEntity {
  id: string;
  sender: string; // Agent ID, 'user', or 'system'
  recipients: string[]; // ['all'], ['user'], ['system'], or specific agent IDs
  type: MessageType;
  subtype?: string; // Additional categorization
  content: MessageContent;
  timestamp: number;
  priority: 'low' | 'normal' | 'high' | 'critical';
  readBy: string[]; // Agent IDs that have read this message
  responseTo?: string; // ID of message this is responding to
  status: 'sent' | 'delivered' | 'read' | 'failed';
}

type MessageType = 
  | 'status-update'      // General status updates
  | 'task-request'       // Request for task assignment
  | 'task-complete'      // Notification of task completion
  | 'resource-request'   // Request for additional resources
  | 'tool-request'       // Request for a specific tool
  | 'tool-share'         // Sharing a newly created tool
  | 'permission-request' // Request for permission to proceed
  | 'error-report'       // Error notification
  | 'query'              // Information query
  | 'response'           // Response to a query
  | 'broadcast'          // General broadcast message
  | 'pause-request'      // Request to pause execution
  | 'resume-request'     // Request to resume execution
  | 'terminate-request'  // Request to terminate an agent
  | 'improvement-share'  // Sharing an improvement to the system
  | 'collaboration'      // Collaboration request
  | 'system-alert';      // System-level alert

interface MessageContent {
  title: string;
  body: string;
  attachments?: any[]; // Additional data attached to the message
  metadata?: { [key: string]: any }; // Additional metadata
}

interface MessageFilters {
  messageType: MessageType | 'all';
  sender: string | 'all';
  dateRange: { start: number; end: number } | null;
  priority: 'all' | 'low' | 'normal' | 'high' | 'critical';
}

interface MessageStats {
  totalMessages: number;
  messagesPerHour: number;
  unreadMessages: number;
  mostActiveSender: string | null;
}
```

### System Slice

```typescript
interface SystemSliceState {
  status: 'idle' | 'starting' | 'running' | 'pausing' | 'paused' | 'stopping' | 'stopped' | 'error';
  startTime: number | null;
  activeAgents: number;
  completedTasks: number;
  totalTasks: number;
  metrics: SystemMetrics;
  configuration: SystemConfiguration;
  alerts: SystemAlert[];
  stats: SystemStats;
}

interface SystemMetrics {
  cpuUsage: number; // Percentage
  memoryUsage: number; // MB
  activeConnections: number;
  messageThroughput: number; // Messages per second
  agentCreationRate: number; // Agents created per minute
  toolUsageRate: number; // Tools used per minute
  errorRate: number; // Errors per minute
}

interface SystemConfiguration {
  maxAgents: number; // Maximum number of agents allowed
  maxMessageHistory: number; // Maximum number of messages to keep in history
  resourceLimits: {
    cpu: number; // Max CPU percentage
    memory: number; // Max memory in MB
    tokens: number; // Max tokens per minute
  };
  security: {
    messageValidation: boolean;
    toolApprovalRequired: boolean;
    agentIsolation: boolean;
  };
  performance: {
    messageBatchSize: number;
    stateUpdateInterval: number; // Milliseconds
    cleanupInterval: number; // Milliseconds
  };
}

interface SystemAlert {
  id: string;
  type: 'info' | 'warning' | 'error' | 'critical';
  message: string;
  timestamp: number;
  acknowledged: boolean;
  acknowledgedBy: string | null;
}

interface SystemStats {
  uptime: number; // Milliseconds
  totalAgentsCreated: number;
  totalTasksProcessed: number;
  totalMessagesProcessed: number;
  totalImprovements: number;
  averageAgentLifespan: number; // Milliseconds
}
```

### Tool Slice

```typescript
interface ToolSliceState {
  registry: { [name: string]: ToolDefinition };
  sharedTools: string[]; // Names of tools available to all agents
  agentTools: { [agentId: string]: string[] }; // Tools specific to agents
  recentUsage: ToolUsageRecord[];
  stats: ToolStats;
}

interface ToolDefinition {
  name: string;
  description: string;
  parameters: ToolParameter[];
  implementation: string; // Code implementation
  creator: string; // Agent ID that created the tool
  createdAt: number;
  lastUsed: number;
  usageCount: number;
  approved: boolean; // Whether the tool has been approved for use
  version: string;
  compatibility: {
    languages: string[];
    backends: string[];
    environments: string[];
  };
}

interface ToolParameter {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'array' | 'object';
  required: boolean;
  description: string;
  defaultValue?: any;
}

interface ToolUsageRecord {
  toolName: string;
  agentId: string;
  timestamp: number;
  success: boolean;
  executionTime: number;
}

interface ToolStats {
  totalTools: number;
  activeTools: number;
  mostUsedTool: string | null;
  averageUsagePerHour: number;
  approvalRate: number; // Percentage of tools that are approved
}
```

### Improvement Slice

```typescript
interface ImprovementSliceState {
  registry: { [id: string]: ImprovementEntity };
  pendingApprovals: string[]; // IDs of improvements awaiting approval
  activeImprovements: string[]; // IDs of improvements currently active in system
  history: string[]; // IDs of all improvements ever made
  stats: ImprovementStats;
}

interface ImprovementEntity {
  id: string;
  title: string;
  description: string;
  type: 'process' | 'tool' | 'algorithm' | 'optimization' | 'feature';
  category: 'efficiency' | 'accuracy' | 'usability' | 'security' | 'scalability';
  implementation: ImprovementImplementation;
  creator: string; // Agent ID that proposed the improvement
  createdAt: number;
  appliedAt: number | null;
  status: 'proposed' | 'reviewing' | 'approved' | 'rejected' | 'applied' | 'deprecated';
  impact: 'low' | 'medium' | 'high'; // Expected impact on system
  dependencies: string[]; // IDs of other improvements this depends on
  affectedComponents: string[]; // Which system components are affected
  testResults: ImprovementTestResults | null;
  approvalHistory: ApprovalEvent[];
}

interface ImprovementImplementation {
  type: 'code-change' | 'configuration' | 'new-tool' | 'process-change';
  target: string; // Which system component to improve
  changes: any[]; // Specific changes to apply
  rollbackPlan?: any; // How to revert this improvement if needed
}

interface ImprovementTestResults {
  automatedTestsPassed: number;
  automatedTestsTotal: number;
  manualTestsPassed: number;
  manualTestsTotal: number;
  performanceImpact: {
    before: SystemMetrics;
    after: SystemMetrics;
    difference: SystemMetrics;
  };
  stability: 'stable' | 'needs-monitoring' | 'unstable';
}

interface ApprovalEvent {
  approver: string; // Agent ID or 'system' or 'user'
  timestamp: number;
  action: 'approved' | 'rejected' | 'commented';
  comment?: string;
}

interface ImprovementStats {
  totalImprovements: number;
  appliedImprovements: number;
  pendingImprovements: number;
  successRate: number; // Percentage of improvements that had positive impact
  averageApprovalTime: number; // Hours
  mostActiveContributor: string | null;
}
```

### UI Slice

```typescript
interface UISliceState {
  theme: 'light' | 'dark' | 'auto';
  layout: UILayoutPreferences;
  notifications: UINotificationPreferences;
  visualization: VisualizationPreferences;
  activeView: ActiveView;
  selectedAgent: string | null;
  expandedPanels: ExpandedPanel[];
  stats: UIStats;
}

interface UILayoutPreferences {
  sidebarCollapsed: boolean;
  agentCardSize: 'compact' | 'normal' | 'expanded';
  messageDisplayLimit: number;
  autoRefreshInterval: number; // Milliseconds
}

interface UINotificationPreferences {
  showMessageNotifications: boolean;
  showAgentStatusNotifications: boolean;
  showSystemAlerts: boolean;
  notificationSound: boolean;
  emailAlerts: boolean;
}

interface VisualizationPreferences {
  agentViewMode: 'grid' | 'list' | 'tree';
  messageViewMode: 'chronological' | 'grouped' | 'filtered';
  showPerformanceMetrics: boolean;
  showSystemHealth: boolean;
  refreshRate: number; // Frames per second
}

type ActiveView = 'dashboard' | 'agents' | 'messages' | 'tasks' | 'tools' | 'improvements' | 'system';

type ExpandedPanel = 
  | 'agent-details' 
  | 'message-log' 
  | 'task-progress' 
  | 'tool-list' 
  | 'improvement-log'
  | 'system-metrics';

interface UIStats {
  activeUsers: number;
  uiRefreshCount: number;
  averageLoadTime: number; // Milliseconds
  errorCount: number;
}
```

## Middleware Design

### State Synchronization Middleware

```typescript
// Middleware to handle state updates from multiple sources
const stateSyncMiddleware: Middleware = (store) => (next) => (action) => {
  // Log the action
  console.log('Action received:', action.type, action.payload);
  
  // Process the action through the reducer
  const result = next(action);
  
  // Broadcast state changes to interested parties
  const newState = store.getState();
  broadcastStateChange(action.type, newState);
  
  return result;
};

// Function to broadcast state changes
function broadcastStateChange(actionType: string, newState: SwarmRootState) {
  // Send updates to visualization service
  if (visualizationService.isConnected()) {
    visualizationService.updateState(newState);
  }
  
  // Send relevant updates to agents
  notifyAgentsOfStateChange(actionType, newState);
  
  // Log significant state changes
  logSignificantChanges(actionType, newState);
}
```

### Conflict Resolution Middleware

```typescript
// Middleware to resolve conflicts when multiple agents update state simultaneously
const conflictResolutionMiddleware: Middleware = (store) => (next) => (action) => {
  if (action.type.endsWith('_CONFLICT')) {
    // Handle conflict resolution
    return resolveConflict(action, store.getState());
  }
  
  // Check for potential conflicts before applying action
  const currentState = store.getState();
  if (wouldCauseConflict(action, currentState)) {
    // Queue action for later processing or resolve conflict
    return handlePotentialConflict(action, currentState);
  }
  
  return next(action);
};

function wouldCauseConflict(action: AnyAction, state: SwarmRootState): boolean {
  // Implement conflict detection logic
  // For example, check if multiple agents are trying to modify the same task
  return false;
}

function resolveConflict(action: AnyAction, state: SwarmRootState): any {
  // Implement conflict resolution strategy
  // For example, prioritize actions based on agent hierarchy or timestamp
  return action;
}
```

### Performance Optimization Middleware

```typescript
// Middleware to optimize performance by batching updates
const performanceOptimizationMiddleware: Middleware = (store) => (next) => (action) => {
  // Batch rapid-fire actions to reduce state updates
  if (shouldBatchAction(action)) {
    return addToBatch(action, next);
  }
  
  return next(action);
};

let actionBatch: AnyAction[] = [];
let batchTimeout: NodeJS.Timeout | null = null;

function addToBatch(action: AnyAction, next: Dispatch) {
  actionBatch.push(action);
  
  if (batchTimeout) {
    clearTimeout(batchTimeout);
  }
  
  batchTimeout = setTimeout(() => {
    // Process all batched actions together
    actionBatch.forEach(batchedAction => next(batchedAction));
    actionBatch = [];
  }, 16); // ~60fps
  
  return action;
}

function shouldBatchAction(action: AnyAction): boolean {
  // Define which actions should be batched
  return action.type.includes('AGENT_STATUS_UPDATE') || 
         action.type.includes('MESSAGE_ADD');
}
```

## Reducer Design

### Agent Reducer

```typescript
const initialAgentState: AgentSliceState = {
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

const agentReducer = createReducer(initialAgentState, (builder) => {
  builder
    // Add agent
    .addCase(addAgent, (state, action) => {
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
    })
    
    // Update agent status
    .addCase(updateAgentStatus, (state, action) => {
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
    })
    
    // Remove agent
    .addCase(removeAgent, (state, action) => {
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
    });
});
```

This Redux store design provides a comprehensive state management solution for the self-improving swarm system, supporting all the required functionality including agent management, task tracking, messaging, tool management, and system improvements.