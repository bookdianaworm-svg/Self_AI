'use client';

import { useEffect, useCallback, useState } from 'react';
import { useConsoleStore } from '@/store/console-store';
import { wsClient } from '@/lib/websocket';
import type { PanelId } from '@/lib/types';
import { Search, X } from 'lucide-react';
import { cn } from '@/lib/utils';

export function CommandBar() {
  const closeCommandBar = useConsoleStore((s) => s.closeCommandBar);
  const commandInput = useConsoleStore((s) => s.commandInput);
  const setCommandInput = useConsoleStore((s) => s.setCommandInput);
  const mode = useConsoleStore((s) => s.mode);
  const setActivePanel = useConsoleStore((s) => s.setActivePanel);
  const dispatch = useConsoleStore((s) => s.dispatch);

  const [error, setError] = useState<string | null>(null);

  // Handle keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        closeCommandBar();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [closeCommandBar]);

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      setError(null);

      const input = commandInput.trim();
      if (!input) return;

      // Parse command
      const parts = input.split(/\s+/);
      const cmd = parts[0].toLowerCase();
      const args = parts.slice(1).join(' ');

      // Global commands
      if (cmd === 'help' || cmd === '?') {
        // Show help - could expand this
        setError('Type help in any panel for commands');
        return;
      }

      if (cmd === 'mode') {
        const modeMap: Record<string, string> = {
          task: 'task',
          perm: 'perm',
          tool: 'tool',
          improve: 'improve',
          route: 'route',
          verify: 'verify',
          msg: 'msg',
          ctrl: 'ctrl',
          config: 'config',
        };
        const targetMode = modeMap[args.toLowerCase() as keyof typeof modeMap];
        if (targetMode) {
          setActivePanel(targetMode as PanelId);
          closeCommandBar();
        } else {
          setError(`Unknown mode: ${args}`);
        }
        return;
      }

      if (cmd === 'goto' || cmd === 'g') {
        // Go to specific item
        setError(`Go to: ${args} - not implemented`);
        return;
      }

      // Panel-specific commands would be handled here
      // For now, dispatch as generic command
      wsClient.dispatch({
        type: `${mode.replace(/[\[\]]/g, '')}/${cmd}`,
        payload: { args },
      });

      closeCommandBar();
    },
    [commandInput, mode, setActivePanel, closeCommandBar]
  );

  return (
    <div className="border-b border-border bg-card/80 backdrop-blur-sm">
      <form onSubmit={handleSubmit} className="flex items-center gap-3 px-4 py-3">
        <Search className="w-4 h-4 text-muted-foreground" />
        <input
          type="text"
          value={commandInput}
          onChange={(e) => setCommandInput(e.target.value)}
          placeholder={`Type a command... (try 'mode task', 'help', or 'goto agent-1')`}
          className="flex-1 bg-transparent text-sm outline-none placeholder:text-muted-foreground"
          autoFocus
        />
        {commandInput && (
          <button
            type="button"
            onClick={() => setCommandInput('')}
            className="p-1 rounded hover:bg-accent"
          >
            <X className="w-3 h-3 text-muted-foreground" />
          </button>
        )}
        <div className="flex items-center gap-2 text-[10px] text-muted-foreground">
          <kbd className="px-1.5 py-0.5 rounded border border-border bg-muted font-mono">
            ESC
          </kbd>
          <span>to close</span>
        </div>
      </form>

      {error && (
        <div className="px-4 pb-2">
          <div className="text-xs text-status-failed bg-status-failed/10 px-3 py-2 rounded-lg">
            {error}
          </div>
        </div>
      )}
    </div>
  );
}
