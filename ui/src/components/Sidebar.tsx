'use client';

import { useConsoleStore } from '@/store/console-store';
import { CONSOLE_MODES } from '@/lib/types';
import { cn } from '@/lib/utils';
import {
  CheckSquare,
  Shield,
  Wrench,
  TrendingUp,
  Route,
  CheckCircle,
  MessageSquare,
  Pause,
  Settings,
  Key,
  Activity,
} from 'lucide-react';

const panels = [
  { id: 'task', label: 'Tasks', icon: CheckSquare, mode: CONSOLE_MODES.TASK },
  { id: 'perm', label: 'Permissions', icon: Shield, mode: CONSOLE_MODES.PERM },
  { id: 'tool', label: 'Tools', icon: Wrench, mode: CONSOLE_MODES.TOOL },
  { id: 'improve', label: 'Improve', icon: TrendingUp, mode: CONSOLE_MODES.IMPROVE },
  { id: 'route', label: 'Routing', icon: Route, mode: CONSOLE_MODES.ROUTE },
  { id: 'verify', label: 'Verify', icon: CheckCircle, mode: CONSOLE_MODES.VERIFY },
  { id: 'msg', label: 'Messages', icon: MessageSquare, mode: CONSOLE_MODES.MSG },
  { id: 'ctrl', label: 'Control', icon: Pause, mode: CONSOLE_MODES.CTRL },
  { id: 'agent_loop', label: 'Agent Loop', icon: Activity, mode: CONSOLE_MODES.AGENT_LOOP },
  { id: 'config', label: 'Config', icon: Settings, mode: CONSOLE_MODES.CONFIG },
  { id: 'apikeys', label: 'API Keys', icon: Key, mode: CONSOLE_MODES.APIKEYS },
] as const;

export function Sidebar() {
  const activePanel = useConsoleStore((s) => s.activePanel);
  const setActivePanel = useConsoleStore((s) => s.setActivePanel);
  const setMode = useConsoleStore((s) => s.setMode);

  const handlePanelClick = (panelId: typeof panels[number]['id']) => {
    setActivePanel(panelId);
    const panel = panels.find((p) => p.id === panelId);
    if (panel) {
      setMode(panel.mode);
    }
  };

  return (
    <aside className="w-48 border-r border-border bg-card/30 p-2 flex flex-col gap-1">
      <div className="px-3 py-2">
        <h2 className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">
          Panels
        </h2>
      </div>

      <nav className="flex-1 flex flex-col gap-0.5">
        {panels.map((panel) => {
          const Icon = panel.icon;
          const isActive = activePanel === panel.id;

          return (
            <button
              key={panel.id}
              onClick={() => handlePanelClick(panel.id)}
              className={cn(
                'flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-all',
                'hover:bg-accent hover:text-accent-foreground',
                isActive && 'bg-primary/10 text-primary border border-primary/20'
              )}
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              <span className="text-sm font-medium">{panel.label}</span>
              {isActive && (
                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-primary" />
              )}
            </button>
          );
        })}
      </nav>

      {/* Quick stats */}
      <div className="border-t border-border pt-2 mt-2">
        <div className="px-3 py-2 text-[10px] text-muted-foreground">
          <div className="flex justify-between mb-1">
            <span>Agents:</span>
            <span className="font-mono">0</span>
          </div>
          <div className="flex justify-between mb-1">
            <span>Tasks:</span>
            <span className="font-mono">0</span>
          </div>
          <div className="flex justify-between">
            <span>Perms:</span>
            <span className="font-mono">0</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
