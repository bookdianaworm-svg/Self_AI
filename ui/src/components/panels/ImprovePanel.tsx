'use client';

import { useConsoleStore } from '@/store/console-store';
import { wsClient } from '@/lib/websocket';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { TrendingUp, Check, X, RotateCcw } from 'lucide-react';

export function ImprovePanel() {
  // Access improvements state from store - use any to access nested properties
  const improvementsState = useConsoleStore((s: any) => s.improvements);
  const pendingImprovements = improvementsState?.pending_approvals || [];

  const handleApprove = (improvementId: string) => {
    wsClient.dispatch({
      type: 'improvements/approve_improvement',
      payload: { improvementId },
    });
  };

  const handleReject = (improvementId: string, reason: string) => {
    wsClient.dispatch({
      type: 'improvements/reject_improvement',
      payload: { improvementId, reason },
    });
  };

  const handleRollback = (improvementId: string) => {
    wsClient.dispatch({
      type: 'improvements/rollback_improvement',
      payload: { improvementId },
    });
  };

  return (
    <div className="space-y-6">
      {/* Panel Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Improvement Review System</h2>
          <p className="text-sm text-muted-foreground">
            Review and approve system improvements
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <TrendingUp className="w-4 h-4" />
          <span>{pendingImprovements.length} pending</span>
        </div>
      </div>

      {/* Improvement List */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Pending Improvements ({pendingImprovements.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[500px]">
            {pendingImprovements.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <TrendingUp className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p className="text-sm">No pending improvements</p>
                <p className="text-xs mt-1">The system is running optimally</p>
              </div>
            ) : (
              <div className="space-y-4">
                {pendingImprovements.map((improvement: any) => (
                  <div
                    key={improvement.improvement_id}
                    className="p-4 rounded-lg border border-border bg-card space-y-3"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="text-sm font-semibold">{improvement.title}</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          Type: {improvement.improvement_type || 'general'}
                        </p>
                      </div>
                    </div>

                    {improvement.description && (
                      <p className="text-sm text-muted-foreground">
                        {improvement.description}
                      </p>
                    )}

                    {improvement.code_change && (
                      <div className="relative">
                        <pre className="p-3 rounded-lg bg-muted text-xs font-mono overflow-x-auto max-h-40">
                          {improvement.code_change.slice(0, 500)}
                          {improvement.code_change.length > 500 && '...'}
                        </pre>
                      </div>
                    )}

                    {/* Action Buttons */}
                    <div className="flex items-center gap-2">
                      <Button
                        size="sm"
                        variant="default"
                        className="bg-status-verified hover:bg-status-verified/80"
                        onClick={() => handleApprove(improvement.improvement_id)}
                      >
                        <Check className="w-3 h-3 mr-1" />
                        Approve
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => handleReject(improvement.improvement_id, 'Manual rejection')}
                      >
                        <X className="w-3 h-3 mr-1" />
                        Reject
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleRollback(improvement.improvement_id)}
                      >
                        <RotateCcw className="w-3 h-3 mr-1" />
                        Rollback
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

export default ImprovePanel;