'use client';

import { useConsoleStore } from '@/store/console-store';
import { cn } from '@/lib/utils';

export function StatusBar() {
  const connected = useConsoleStore((s) => s.connected);
  const systemStatus = useConsoleStore((s) => s.systemStatus);
  const agents = useConsoleStore((s) => s.agents);
  const tasks = useConsoleStore((s) => s.tasks);
  const pendingPermissions = useConsoleStore((s) => s.pendingPermissions);
  const mode = useConsoleStore((s) => s.mode);

  const activeAgentCount = Object.values(agents).filter(
    (a) => a.status === 'executing' || a.status === 'planning'
  ).length;

  const pendingTaskCount = Object.keys(tasks).filter(
    (id) => tasks[id].status === 'pending' || tasks[id].status === 'in_progress'
  ).length;

  return (
    <footer className="h-8 border-t border-border bg-card/50 px-4 flex items-center justify-between text-[10px] font-mono">
      <div className="flex items-center gap-4">
        {/* System status */}
        <div className="flex items-center gap-1.5">
          <div
            className={cn(
              'w-1.5 h-1.5 rounded-full',
              systemStatus === 'running' && 'bg-status-running animate-pulse-dot',
              systemStatus === 'paused' && 'bg-status-paused',
              systemStatus === 'idle' && 'bg-status-idle',
              systemStatus === 'error' && 'bg-status-failed'
            )}
          />
          <span className="text-muted-foreground">System:</span>
          <span className="capitalize">{systemStatus}</span>
        </div>

        {/* Active agents */}
        <div className="flex items-center gap-1.5">
          <span className="text-muted-foreground">Agents:</span>
          <span className={activeAgentCount > 0 ? 'text-status-running' : 'text-muted-foreground'}>
            {activeAgentCount} active
          </span>
        </div>

        {/* Pending tasks */}
        <div className="flex items-center gap-1.5">
          <span className="text-muted-foreground">Tasks:</span>
          <span className={pendingTaskCount > 0 ? 'text-status-pending' : 'text-muted-foreground'}>
            {pendingTaskCount}
          </span>
        </div>

        {/* Pending permissions */}
        <div className="flex items-center gap-1.5">
          <span className="text-muted-foreground">Perms:</span>
          <span className={pendingPermissions.length > 0 ? 'text-status-pending' : 'text-muted-foreground'}>
            {pendingPermissions.length}
          </span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Current mode */}
        <div className="flex items-center gap-1.5">
          <span className="text-muted-foreground">Mode:</span>
          <span className="text-primary">{mode}</span>
        </div>

        {/* WebSocket status */}
        <div className="flex items-center gap-1.5">
          <div
            className={cn(
              'w-1.5 h-1.5 rounded-full',
              connected ? 'bg-status-running' : 'bg-status-failed'
            )}
          />
          <span className="text-muted-foreground">
            WebSocket: {connected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>
    </footer>
  );
}
