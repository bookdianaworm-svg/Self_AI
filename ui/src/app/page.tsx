'use client';

import { useEffect } from 'react';
import { useConsoleStore } from '@/store/console-store';
import { wsClient } from '@/lib/websocket';
import { Header } from '@/components/Header';
import { Sidebar } from '@/components/Sidebar';
import { CommandBar } from '@/components/CommandBar';
import { StatusBar } from '@/components/StatusBar';
import { TaskPanel } from '@/components/panels/TaskPanel';
import { PermissionPanel } from '@/components/panels/PermissionPanel';
import { ToolPanel } from '@/components/panels/ToolPanel';
import { RoutePanel } from '@/components/panels/RoutePanel';
import { VerifyPanel } from '@/components/panels/VerifyPanel';
import { MessagePanel } from '@/components/panels/MessagePanel';
import { ControlPanel } from '@/components/panels/ControlPanel';
import { ConfigPanel } from '@/components/panels/ConfigPanel';
import { APIKeysPanel } from '@/components/panels/APIKeysPanel';
import { AgentLoopExplorer } from '@/components/panels/AgentLoopExplorer';
import { ImprovePanel } from '@/components/panels/ImprovePanel';
import { cn } from '@/lib/utils';

export default function Home() {
  const activePanel = useConsoleStore((s) => s.activePanel);
  const commandBarOpen = useConsoleStore((s) => s.commandBarOpen);

  useEffect(() => {
    // Connect to WebSocket on mount
    wsClient.connect();
    wsClient.subscribe(['agents', 'tasks', 'permissions', 'tools', 'messages', 'routing', 'verification', 'system']);

    return () => {
      wsClient.disconnect();
    };
  }, []);

  const renderPanel = () => {
    switch (activePanel) {
      case 'task':
        return <TaskPanel />;
      case 'perm':
        return <PermissionPanel />;
      case 'tool':
        return <ToolPanel />;
      case 'route':
        return <RoutePanel />;
      case 'verify':
        return <VerifyPanel />;
      case 'msg':
        return <MessagePanel />;
      case 'ctrl':
        return <ControlPanel />;
      case 'config':
        return <ConfigPanel />;
      case 'apikeys':
        return <APIKeysPanel />;
      case 'agent_loop':
        return <AgentLoopExplorer />;
      case 'improve':
        return <ImprovePanel />;
      default:
        return <TaskPanel />;
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Background grid pattern */}
      <div className="fixed inset-0 grid-pattern opacity-20 dark:opacity-10 pointer-events-none" />

      {/* Main content */}
      <div className="relative z-10 flex flex-col h-screen">
        <Header />

        {commandBarOpen && <CommandBar />}

        <div className="flex flex-1 overflow-hidden">
          <Sidebar />
          <main className="flex-1 overflow-auto p-6">
            <div className="max-w-6xl mx-auto">
              {renderPanel()}
            </div>
          </main>
        </div>

        <StatusBar />
      </div>
    </div>
  );
}
