'use client';

import { useConsoleStore } from '@/store/console-store';
import { wsClient } from '@/lib/websocket';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { MessageSquare, Send, Users } from 'lucide-react';
import { cn } from '@/lib/utils';

export function MessagePanel() {
  const agents = useConsoleStore((s) => s.agents);
  const threads = useConsoleStore((s) => s.threads);
  const unreadCounts = useConsoleStore((s) => s.unreadCounts);

  const agentList = Object.values(agents);

  const handleSendMessage = (agentId: string, message: string) => {
    wsClient.dispatch({
      type: 'messages/send_message',
      payload: { recipientId: agentId, content: message },
    });
  };

  const handleBroadcast = (message: string) => {
    wsClient.dispatch({
      type: 'messages/broadcast_message',
      payload: { content: message },
    });
  };

  return (
    <div className="space-y-6">
      {/* Panel Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Agent Communication Console</h2>
          <p className="text-sm text-muted-foreground">
            Direct messaging with agents
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Users className="w-4 h-4" />
          <span>{agentList.length} agents</span>
        </div>
      </div>

      {/* Agent List */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Active Agents ({agentList.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[400px]">
            {agentList.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <MessageSquare className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p className="text-sm">No active agents</p>
              </div>
            ) : (
              <div className="space-y-3">
                {agentList.map((agent) => {
                  const thread = threads[agent.agent_id] || [];
                  const unread = unreadCounts[agent.agent_id] || 0;

                  return (
                    <div
                      key={agent.agent_id}
                      className="p-4 rounded-lg border border-border bg-card space-y-3"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <div
                            className={cn(
                              'w-2 h-2 rounded-full',
                              agent.status === 'executing'
                                ? 'bg-status-running animate-pulse-dot'
                                : agent.status === 'idle'
                                ? 'bg-status-idle'
                                : 'bg-status-paused'
                            )}
                          />
                          <div>
                            <p className="text-sm font-medium">{agent.name}</p>
                            <p className="text-xs text-muted-foreground">
                              {agent.agent_id}
                            </p>
                          </div>
                        </div>
                        <span
                          className={cn(
                            'px-2 py-1 rounded-full text-xs border',
                            agent.status === 'executing'
                              ? 'badge-running'
                              : agent.status === 'idle'
                              ? 'badge-idle'
                              : 'badge-paused'
                          )}
                        >
                          {agent.status}
                        </span>
                      </div>

                      {/* Thread Preview */}
                      {thread.length > 0 && (
                        <div className="text-xs text-muted-foreground p-2 rounded bg-muted">
                          Last message: {thread[thread.length - 1].content.slice(0, 50)}
                          {thread[thread.length - 1].content.length > 50 && '...'}
                        </div>
                      )}

                      {/* Quick Actions */}
                      <div className="flex items-center gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          className="flex-1"
                          onClick={() =>
                            handleSendMessage(agent.agent_id, 'Status check')
                          }
                        >
                          <Send className="w-3 h-3 mr-1" />
                          Send Message
                        </Button>
                        {unread > 0 && (
                          <span className="px-2 py-1 rounded-full bg-primary text-primary-foreground text-xs">
                            {unread} new
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}
