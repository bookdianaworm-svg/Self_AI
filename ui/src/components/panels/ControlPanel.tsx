'use client';

import { useConsoleStore } from '@/store/console-store';
import { wsClient } from '@/lib/websocket';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Pause, Play, Square, Undo2, AlertTriangle } from 'lucide-react';
import { cn } from '@/lib/utils';

export function ControlPanel() {
  const agents = useConsoleStore((s) => s.agents);
  const pausedAgents = useConsoleStore((s) => s.pausedAgents);
  const allPaused = useConsoleStore((s) => s.allPaused);
  const timeline = useConsoleStore((s) => s.timeline);

  const agentList = Object.values(agents);
  const runningAgents = agentList.filter((a) => a.status === 'executing');

  const handlePause = (target: 'all' | string, targetType?: string) => {
    wsClient.dispatch({
      type: 'agents/pause_agent',
      payload: { target, targetId: targetType },
    });
  };

  const handleResume = (target: 'all' | string, targetType?: string) => {
    wsClient.dispatch({
      type: 'agents/resume_agent',
      payload: { target, targetId: targetType },
    });
  };

  const handleTerminate = (agentId: string) => {
    wsClient.dispatch({
      type: 'agents/terminate_agent',
      payload: { agentId },
    });
  };

  const handleEmergencyStop = () => {
    wsClient.dispatch({
      type: 'agents/emergency_stop',
      payload: {},
    });
  };

  const handleUndo = () => {
    wsClient.dispatch({
      type: 'agents/undo',
      payload: {},
    });
  };

  return (
    <div className="space-y-6">
      {/* Panel Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Intervention Controls</h2>
          <p className="text-sm text-muted-foreground">
            Emergency and operational control over agent execution
          </p>
        </div>
        <div className="flex items-center gap-2">
          {allPaused ? (
            <span className="px-3 py-1.5 rounded-full bg-status-paused/20 text-status-paused text-sm font-medium border border-status-paused/30">
              ALL PAUSED
            </span>
          ) : (
            <span className="px-3 py-1.5 rounded-full bg-status-running/20 text-status-running text-sm font-medium border border-status-running/30">
              RUNNING
            </span>
          )}
        </div>
      </div>

      {/* Emergency Controls */}
      <Card className="border-panel-control/30 bg-panel-control/5">
        <CardHeader className="pb-3">
          <CardTitle className="text-base flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-status-failed" />
            Emergency Controls
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <Button
              variant="destructive"
              className="h-20 flex-col gap-2"
              onClick={handleEmergencyStop}
            >
              <Square className="w-5 h-5" />
              <span className="text-xs font-semibold">STOP ALL</span>
            </Button>
            <Button
              variant="outline"
              className="h-20 flex-col gap-2"
              onClick={() => handlePause('all')}
            >
              <Pause className="w-5 h-5" />
              <span className="text-xs">Pause All</span>
            </Button>
            <Button
              variant="outline"
              className="h-20 flex-col gap-2"
              onClick={() => handleResume('all')}
            >
              <Play className="w-5 h-5" />
              <span className="text-xs">Resume All</span>
            </Button>
            <Button
              variant="outline"
              className="h-20 flex-col gap-2"
              onClick={handleUndo}
            >
              <Undo2 className="w-5 h-5" />
              <span className="text-xs">Undo</span>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Individual Agent Controls */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Agent Controls ({runningAgents.length} running)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[300px]">
            {agentList.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <p className="text-sm">No agents</p>
              </div>
            ) : (
              <div className="space-y-2">
                {agentList.map((agent) => {
                  const isPaused = pausedAgents.includes(agent.agent_id);
                  return (
                    <div
                      key={agent.agent_id}
                      className="flex items-center justify-between p-3 rounded-lg border border-border bg-card"
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={cn(
                            'w-2 h-2 rounded-full',
                            isPaused
                              ? 'bg-status-paused'
                              : agent.status === 'executing'
                              ? 'bg-status-running animate-pulse-dot'
                              : 'bg-status-idle'
                          )}
                        />
                        <div>
                          <p className="text-sm font-medium">{agent.name}</p>
                          <p className="text-xs text-muted-foreground">
                            {agent.agent_id}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {isPaused ? (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleResume('individual', agent.agent_id)}
                          >
                            <Play className="w-3 h-3 mr-1" />
                            Resume
                          </Button>
                        ) : (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handlePause('individual', agent.agent_id)}
                          >
                            <Pause className="w-3 h-3 mr-1" />
                            Pause
                          </Button>
                        )}
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => handleTerminate(agent.agent_id)}
                        >
                          <Square className="w-3 h-3 mr-1" />
                          Terminate
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </ScrollArea>
        </CardContent>
      </Card>

      {/* Intervention Timeline */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Intervention Timeline ({timeline.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[200px]">
            {timeline.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <p className="text-sm">No interventions yet</p>
              </div>
            ) : (
              <div className="relative pl-6 space-y-3">
                <div className="absolute left-[7px] top-0 bottom-0 w-[2px] bg-border" />
                {timeline.slice(-10).reverse().map((entry, i) => (
                  <div key={entry.id} className="relative">
                    <div
                      className={cn(
                        'absolute left-[-13px] top-1.5 w-[12px] h-[12px] rounded-full border-2 border-background',
                        entry.action_type === 'pause' && 'bg-status-paused',
                        entry.action_type === 'resume' && 'bg-status-running',
                        entry.action_type === 'terminate' && 'bg-status-failed',
                        entry.action_type === 'emergency_stop' && 'bg-status-failed'
                      )}
                    />
                    <div className="flex items-center gap-2 text-xs">
                      <span className="font-mono text-muted-foreground">
                        {new Date(entry.timestamp).toLocaleTimeString()}
                      </span>
                      <span className="font-medium capitalize">
                        {entry.action_type.replace('_', ' ')}
                      </span>
                      <span className="text-muted-foreground">
                        {entry.target_type}: {entry.target_id || 'all'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}
