'use client';

import { useConsoleStore } from '@/store/console-store';
import { wsClient } from '@/lib/websocket';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Shield, AlertTriangle, Check } from 'lucide-react';
import { cn } from '@/lib/utils';

export function PermissionPanel() {
  const pendingPermissions = useConsoleStore((s) => s.pendingPermissions);
  const permissionDefaults = useConsoleStore((s) => s.permissionDefaults);

  const handleApprove = (requestId: string) => {
    wsClient.dispatch({
      type: 'permissions/approve_request',
      payload: { requestId },
    });
  };

  const handleDeny = (requestId: string) => {
    wsClient.dispatch({
      type: 'permissions/deny_request',
      payload: { requestId },
    });
  };

  const handleDontAskAgain = (requestId: string) => {
    wsClient.dispatch({
      type: 'permissions/set_default',
      payload: { requestId, remember: true, action: 'approve' },
    });
  };

  return (
    <div className="space-y-6">
      {/* Panel Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Permission Request Queue</h2>
          <p className="text-sm text-muted-foreground">
            Review and respond to agent permission requests
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Shield className="w-4 h-4" />
          <span>{pendingPermissions.length} pending</span>
        </div>
      </div>

      {/* Permission Defaults */}
      {Object.keys(permissionDefaults).length > 0 && (
        <Card className="border-panel-permission/30 bg-panel-permission/5">
          <CardHeader className="pb-2">
            <CardTitle className="text-base flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-status-pending" />
              Active Defaults
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {Object.entries(permissionDefaults).map(([type, action]) => (
                <span
                  key={type}
                  className={cn(
                    'px-2 py-1 rounded-full text-xs font-medium border',
                    action === 'approve'
                      ? 'badge-verified'
                      : action === 'deny'
                      ? 'badge-failed'
                      : 'badge-pending'
                  )}
                >
                  {type}: {action}
                </span>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Pending Requests */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Pending Requests ({pendingPermissions.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[400px]">
            {pendingPermissions.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <Check className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p className="text-sm">All clear!</p>
                <p className="text-xs mt-1">No pending permission requests</p>
              </div>
            ) : (
              <div className="space-y-4">
                {pendingPermissions.map((perm) => (
                  <div
                    key={perm.request_id}
                    className="p-4 rounded-lg border border-border bg-card space-y-3"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="text-sm font-medium">{perm.description}</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          From: {perm.agent_id} | Type: {perm.permission_type}
                        </p>
                      </div>
                    </div>

                    {perm.risk_assessment && (
                      <div className="text-xs text-muted-foreground p-2 rounded bg-muted">
                        Risk: {perm.risk_assessment}
                      </div>
                    )}

                    {/* Approval Buttons */}
                    <div className="grid grid-cols-4 gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        className="approval-btn-yes"
                        onClick={() => handleApprove(perm.request_id)}
                      >
                        <span className="font-bold">[Y]</span>
                        <span className="text-xs">Yes</span>
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        className="approval-btn-no"
                        onClick={() => handleDeny(perm.request_id)}
                      >
                        <span className="font-bold">[N]</span>
                        <span className="text-xs">No</span>
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        className="approval-btn-dont-ask"
                        onClick={() => handleDontAskAgain(perm.request_id)}
                      >
                        <span className="font-bold">[D]</span>
                        <span className="text-xs">Don't ask</span>
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        className="approval-btn-ask"
                      >
                        <span className="font-bold">[A]</span>
                        <span className="text-xs">Ask always</span>
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
