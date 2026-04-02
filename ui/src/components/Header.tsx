'use client';

import { useTheme } from 'next-themes';
import { useEffect, useState } from 'react';
import { useConsoleStore } from '@/store/console-store';
import { Moon, Sun, Keyboard } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function Header() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const openCommandBar = useConsoleStore((s) => s.openCommandBar);
  const mode = useConsoleStore((s) => s.mode);
  const sessionId = useConsoleStore((s) => s.systemStatus);

  // Avoid hydration mismatch by only rendering theme-dependent UI after mount
  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <header className="h-14 border-b border-border bg-card/50 backdrop-blur-sm px-4 flex items-center justify-between">
      <div className="flex items-center gap-4">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-sm">SW</span>
          </div>
          <div>
            <h1 className="text-sm font-semibold tracking-tight">
              <span className="text-foreground">Swarm</span>
              <span className="text-muted-foreground ml-1">Console</span>
            </h1>
            <p className="text-[10px] text-muted-foreground">
              Interactive Operations
            </p>
          </div>
        </div>

        {/* Mode indicator */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-panel-task/30 border border-panel-task/50">
          <span className="text-xs font-mono text-primary">{mode}</span>
        </div>
      </div>

      <div className="flex items-center gap-2">
        {/* Keyboard shortcut hint */}
        <Button
          variant="ghost"
          size="sm"
          onClick={openCommandBar}
          className="text-muted-foreground gap-2"
        >
          <Keyboard className="w-4 h-4" />
          <span className="text-xs">Ctrl+K</span>
        </Button>

        {/* Theme toggle */}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
        >
          {mounted && resolvedTheme === 'dark' ? (
            <Sun className="w-4 h-4" />
          ) : (
            <Moon className="w-4 h-4" />
          )}
        </Button>

        {/* Connection status */}
        <ConnectionIndicator />
      </div>
    </header>
  );
}

function ConnectionIndicator() {
  const connected = useConsoleStore((s) => s.connected);

  return (
    <div className="flex items-center gap-2 px-2 py-1 rounded-full border border-border">
      <div
        className={`w-2 h-2 rounded-full ${
          connected
            ? 'bg-status-running animate-pulse-dot'
            : 'bg-status-failed'
        }`}
      />
      <span className="text-[10px] font-mono text-muted-foreground">
        {connected ? 'LIVE' : 'OFFLINE'}
      </span>
    </div>
  );
}
