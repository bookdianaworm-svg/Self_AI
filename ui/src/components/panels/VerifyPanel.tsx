'use client';

import { useConsoleStore } from '@/store/console-store';
import { wsClient } from '@/lib/websocket';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { CheckCircle, Clock, Cpu, HardDrive } from 'lucide-react';
import { cn } from '@/lib/utils';

export function VerifyPanel() {
  const verificationStatus = useConsoleStore((s) => s.verificationStatus);
  const layer1Status = useConsoleStore((s) => s.layer1Status);
  const theorems = useConsoleStore((s) => s.theorems);
  const verificationQueue = useConsoleStore((s) => s.verificationQueue);

  const theoremList = Object.values(theorems);

  const handleSubmit = (theoremText: string) => {
    wsClient.dispatch({
      type: 'verification/verify_theorem_request',
      payload: { theoremText },
    });
  };

  return (
    <div className="space-y-6">
      {/* Panel Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Verification Control Panel</h2>
          <p className="text-sm text-muted-foreground">
            Monitor and trigger Layer 1 theorem verification
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Layer1StatusIndicator status={layer1Status} />
        </div>
      </div>

      {/* Layer1 Status */}
      <Card className="border-panel-verify/30 bg-panel-verify/5">
        <CardHeader className="pb-3">
          <CardTitle className="text-base flex items-center gap-2">
            <HardDrive className="w-4 h-4" />
            Layer1 Bootstrap Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4">
            <div className="flex items-center gap-2">
              <div
                className={cn(
                  'w-2 h-2 rounded-full',
                  layer1Status.status === 'loaded'
                    ? 'bg-status-verified'
                    : layer1Status.status === 'loading'
                    ? 'bg-status-pending animate-pulse'
                    : 'bg-status-failed'
                )}
              />
              <span className="text-sm">
                Lean: {layer1Status.mathlib_version || 'N/A'}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <div
                className={cn(
                  'w-2 h-2 rounded-full',
                  layer1Status.physlib_version
                    ? 'bg-status-verified'
                    : 'bg-status-idle'
                )}
              />
              <span className="text-sm">
                PhysLib: {layer1Status.physlib_version || 'N/A'}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm">Haskell: Ready</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Verification Queue */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Verification Queue ({verificationQueue.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[400px]">
            {theoremList.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <CheckCircle className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p className="text-sm">Queue empty</p>
                <p className="text-xs mt-1">Submit a theorem to verify</p>
              </div>
            ) : (
              <div className="space-y-3">
                {theoremList.map((theorem) => (
                  <div
                    key={theorem.theorem_id}
                    className="p-4 rounded-lg border border-border bg-card space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <p className="text-xs font-mono text-muted-foreground">
                        {theorem.theorem_id}
                      </p>
                      <StatusBadge status={theorem.status} />
                    </div>
                    <p className="text-sm font-medium line-clamp-2">
                      {theorem.theorem_text}
                    </p>
                    <div className="flex items-center gap-4 text-xs text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {theorem.proof_attempts} attempts
                      </span>
                      {theorem.completed_at && (
                        <span>
                          Completed:{' '}
                          {new Date(theorem.completed_at).toLocaleTimeString()}
                        </span>
                      )}
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

function Layer1StatusIndicator({
  status,
}: {
  status: { status: string; mathlib_version: string | null; physlib_version: string | null };
}) {
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-border">
      <div
        className={cn(
          'w-2 h-2 rounded-full',
          status.status === 'loaded' && 'bg-status-verified animate-pulse-dot',
          status.status === 'loading' && 'bg-status-pending animate-pulse',
          status.status === 'error' && 'bg-status-failed'
        )}
      />
      <span className="text-xs font-medium">
        Layer1: {status.status}
      </span>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const statusClasses: Record<string, string> = {
    PENDING: 'badge-pending',
    IN_PROGRESS: 'badge-running',
    VERIFIED: 'badge-verified',
    FAILED: 'badge-failed',
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
