'use client';

import { useState, useCallback } from 'react';
import { useConsoleStore } from '@/store/console-store';
import { wsClient } from '@/lib/websocket';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Send, Brain, Clock, Zap } from 'lucide-react';

export function TaskPanel() {
  const [description, setDescription] = useState('');
  const tasks = useConsoleStore((s) => s.tasks);
  const taskQueue = useConsoleStore((s) => s.taskQueue);

  const handleSubmit = useCallback(() => {
    if (!description.trim()) return;

    wsClient.dispatch({
      type: 'tasks/submit_task',
      payload: { description },
    });

    setDescription('');
  }, [description]);

  const taskList = Object.values(tasks);
  const pendingTasks = taskList.filter((t) => t.status === 'pending' || t.status === 'in_progress');

  return (
    <div className="space-y-6">
      {/* Panel Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Task Submission Console</h2>
          <p className="text-sm text-muted-foreground">
            Submit tasks to the swarm for processing
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Brain className="w-4 h-4" />
          <span>{pendingTasks.length} pending</span>
        </div>
      </div>

      {/* Task Input */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">New Task</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe the task you want the swarm to process..."
            className="w-full h-32 p-3 rounded-lg border border-border bg-background text-sm resize-none focus:outline-none focus:ring-2 focus:ring-ring"
          />
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 text-xs text-muted-foreground">
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" />
                Auto-classified
              </span>
              <span className="flex items-center gap-1">
                <Zap className="w-3 h-3" />
                Priority: Normal
              </span>
            </div>
            <Button onClick={handleSubmit} disabled={!description.trim()}>
              <Send className="w-4 h-4 mr-2" />
              Submit Task
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Task Queue */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Task Queue ({taskQueue.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[300px]">
            {taskList.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <p className="text-sm">No tasks yet</p>
                <p className="text-xs mt-1">Submit a task to get started</p>
              </div>
            ) : (
              <div className="space-y-2">
                {taskList.map((task) => (
                  <div
                    key={task.task_id}
                    className="flex items-center justify-between p-3 rounded-lg border border-border bg-card hover:bg-accent/50 transition-colors"
                  >
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">
                        {task.description}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {task.task_id}
                      </p>
                    </div>
                    <StatusBadge status={task.status} />
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

function StatusBadge({ status }: { status: string }) {
  const statusClasses: Record<string, string> = {
    pending: 'badge-pending',
    in_progress: 'badge-running',
    completed: 'badge-verified',
    failed: 'badge-failed',
    cancelled: 'badge-idle',
  };

  return (
    <span
      className={`px-2 py-1 rounded-full text-xs font-medium border ${
        statusClasses[status] || 'badge-idle'
      }`}
    >
      {status.replace('_', ' ')}
    </span>
  );
}
