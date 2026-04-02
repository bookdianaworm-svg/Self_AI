import { create } from 'zustand';
import type {
  RootState,
  PanelId,
  ConsoleMode,
  AgentEntity,
  TaskEntity,
  PermissionRequest,
  ToolDefinition,
  MessageEntity,
  InterventionRecord,
  RoutingDecision,
  BackendMetrics,
  TheoremRecord,
  Layer1Status,
  Notification
} from '@/lib/types';
import { CONSOLE_MODES } from '@/lib/types';
import { wsClient } from '@/lib/websocket';

interface ConsoleStore {
  connected: boolean;
  setConnected: (connected: boolean) => void;

  mode: ConsoleMode;
  setMode: (mode: ConsoleMode) => void;

  activePanel: PanelId;
  setActivePanel: (panel: PanelId) => void;

  commandBarOpen: boolean;
  commandInput: string;
  openCommandBar: () => void;
  closeCommandBar: () => void;
  setCommandInput: (input: string) => void;

  agents: Record<string, AgentEntity>;
  pausedAgents: string[];
  allPaused: boolean;
  timeline: InterventionRecord[];
  setAgents: (agents: Record<string, AgentEntity>) => void;
  setPausedAgents: (paused: string[]) => void;
  setAllPaused: (paused: boolean) => void;
  addTimelineEntry: (entry: InterventionRecord) => void;

  tasks: Record<string, TaskEntity>;
  taskQueue: string[];
  setTasks: (tasks: Record<string, TaskEntity>) => void;
  setTaskQueue: (queue: string[]) => void;

  pendingPermissions: PermissionRequest[];
  permissionDefaults: Record<string, 'approve' | 'deny' | 'ask'>;
  setPendingPermissions: (permissions: PermissionRequest[]) => void;
  setPermissionDefaults: (defaults: Record<string, 'approve' | 'deny' | 'ask'>) => void;

  pendingTools: ToolDefinition[];
  setPendingTools: (tools: ToolDefinition[]) => void;

  threads: Record<string, MessageEntity[]>;
  unreadCounts: Record<string, number>;
  setThreads: (threads: Record<string, MessageEntity[]>) => void;
  setUnreadCounts: (counts: Record<string, number>) => void;

  currentRoute: {
    backend: string | null;
    environment: string | null;
    mode: 'local' | 'modal' | null;
    dataSensitivity: 'public' | 'internal' | 'restricted' | null;
  };
  backendMetrics: Record<string, BackendMetrics>;
  routingHistory: RoutingDecision[];
  setCurrentRoute: (route: { backend: string | null; environment: string | null; mode: 'local' | 'modal' | null; dataSensitivity: 'public' | 'internal' | 'restricted' | null }) => void;
  setBackendMetrics: (metrics: Record<string, BackendMetrics>) => void;
  addRoutingDecision: (decision: RoutingDecision) => void;

  verificationStatus: 'PENDING' | 'IN_PROGRESS' | 'VERIFIED' | 'FAILED';
  activeVerification: string | null;
  verificationQueue: string[];
  layer1Status: Layer1Status;
  theorems: Record<string, TheoremRecord>;
  setVerificationStatus: (status: 'PENDING' | 'IN_PROGRESS' | 'VERIFIED' | 'FAILED') => void;
  setLayer1Status: (status: Layer1Status) => void;
  setTheorems: (theorems: Record<string, TheoremRecord>) => void;

  notifications: Notification[];
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void;
  dismissNotification: (id: string) => void;

  systemStatus: 'idle' | 'running' | 'paused' | 'error';
  setSystemStatus: (status: 'idle' | 'running' | 'paused' | 'error') => void;

  dispatch: (action: { type: string; payload?: Record<string, unknown> }) => void;
}

export const useConsoleStore = create<ConsoleStore>((set, get) => ({
  connected: false,
  setConnected: (connected) => set({ connected }),

  mode: CONSOLE_MODES.TASK,
  setMode: (mode) => set({ mode }),

  activePanel: 'task',
  setActivePanel: (panel) => set({ activePanel: panel }),

  commandBarOpen: false,
  commandInput: '',
  openCommandBar: () => set({ commandBarOpen: true }),
  closeCommandBar: () => set({ commandBarOpen: false, commandInput: '' }),
  setCommandInput: (input) => set({ commandInput: input }),

  agents: {},
  pausedAgents: [],
  allPaused: false,
  timeline: [],
  setAgents: (agents) => set({ agents }),
  setPausedAgents: (pausedAgents) => set({ pausedAgents }),
  setAllPaused: (allPaused) => set({ allPaused }),
  addTimelineEntry: (entry) => set((state) => ({ 
    timeline: [...state.timeline.slice(-49), entry] 
  })),

  tasks: {},
  taskQueue: [],
  setTasks: (tasks) => set({ tasks }),
  setTaskQueue: (taskQueue) => set({ taskQueue }),

  pendingPermissions: [],
  permissionDefaults: {},
  setPendingPermissions: (pendingPermissions) => set({ pendingPermissions }),
  setPermissionDefaults: (permissionDefaults) => set({ permissionDefaults }),

  pendingTools: [],
  setPendingTools: (pendingTools) => set({ pendingTools }),

  threads: {},
  unreadCounts: {},
  setThreads: (threads) => set({ threads }),
  setUnreadCounts: (unreadCounts) => set({ unreadCounts }),

  currentRoute: {
    backend: null,
    environment: null,
    mode: null,
    dataSensitivity: null,
  },
  backendMetrics: {},
  routingHistory: [],
  setCurrentRoute: (currentRoute) => set({ currentRoute }),
  setBackendMetrics: (backendMetrics) => set({ backendMetrics }),
  addRoutingDecision: (decision) => set((state) => ({ 
    routingHistory: [...state.routingHistory.slice(-99), decision] 
  })),

  verificationStatus: 'PENDING',
  activeVerification: null,
  verificationQueue: [],
  layer1Status: { status: 'loading', mathlib_version: null, physlib_version: null },
  theorems: {},
  setVerificationStatus: (verificationStatus) => set({ verificationStatus }),
  setLayer1Status: (layer1Status) => set({ layer1Status }),
  setTheorems: (theorems) => set({ theorems }),

  notifications: [],
  addNotification: (notification) => set((state) => ({
    notifications: [
      ...state.notifications,
      {
        ...notification,
        id: crypto.randomUUID(),
        timestamp: Date.now(),
        read: false,
      },
    ],
  })),
  dismissNotification: (id) => set((state) => ({
    notifications: state.notifications.filter((n) => n.id !== id),
  })),

  systemStatus: 'idle',
  setSystemStatus: (systemStatus) => set({ systemStatus }),

  dispatch: (action) => {
    wsClient.dispatch(action);
  },
}));
