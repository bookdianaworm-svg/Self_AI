'use client';

import { useConsoleStore } from '@/store/console-store';
import { wsClient } from '@/lib/websocket';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Wrench, Check, X, Code } from 'lucide-react';

export function ToolPanel() {
  const pendingTools = useConsoleStore((s) => s.pendingTools);

  const handleApprove = (toolId: string) => {
    wsClient.dispatch({
      type: 'tools/approve_tool',
      payload: { toolId },
    });
  };

  const handleReject = (toolId: string, reason: string) => {
    wsClient.dispatch({
      type: 'tools/reject_tool',
      payload: { toolId, reason },
    });
  };

  return (
    <div className="space-y-6">
      {/* Panel Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Tool Review Interface</h2>
          <p className="text-sm text-muted-foreground">
            Review and approve dynamically created tools
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Wrench className="w-4 h-4" />
          <span>{pendingTools.length} pending</span>
        </div>
      </div>

      {/* Tool List */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Pending Tools ({pendingTools.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[500px]">
            {pendingTools.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <Check className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p className="text-sm">All tools approved!</p>
                <p className="text-xs mt-1">No pending tool reviews</p>
              </div>
            ) : (
              <div className="space-y-4">
                {pendingTools.map((tool) => (
                  <div
                    key={tool.tool_id}
                    className="p-4 rounded-lg border border-border bg-card space-y-3"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="text-sm font-semibold">{tool.name}</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          Created by: {tool.created_by}
                        </p>
                      </div>
                    </div>

                    <p className="text-sm text-muted-foreground">
                      {tool.description}
                    </p>

                    {/* Code Preview */}
                    <div className="relative">
                      <div className="absolute right-2 top-2 z-10">
                        <Button size="icon" variant="ghost" className="h-6 w-6">
                          <Code className="w-3 h-3" />
                        </Button>
                      </div>
                      <pre className="p-3 rounded-lg bg-muted text-xs font-mono overflow-x-auto max-h-40">
                        {tool.code.slice(0, 500)}
                        {tool.code.length > 500 && '...'}
                      </pre>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex items-center gap-2">
                      <Button
                        size="sm"
                        variant="default"
                        className="bg-status-verified hover:bg-status-verified/80"
                        onClick={() => handleApprove(tool.tool_id)}
                      >
                        <Check className="w-3 h-3 mr-1" />
                        Approve
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => handleReject(tool.tool_id, 'Manual rejection')}
                      >
                        <X className="w-3 h-3 mr-1" />
                        Reject
                      </Button>
                      <Button size="sm" variant="outline">
                        Sandbox Test
                      </Button>
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
