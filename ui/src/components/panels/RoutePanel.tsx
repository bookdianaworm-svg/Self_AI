'use client';

import { useConsoleStore } from '@/store/console-store';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Route, Cpu, Clock, CheckCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

export function RoutePanel() {
  const currentRoute = useConsoleStore((s) => s.currentRoute);
  const backendMetrics = useConsoleStore((s) => s.backendMetrics);
  const routingHistory = useConsoleStore((s) => s.routingHistory);

  const metricsList = Object.entries(backendMetrics);

  return (
    <div className="space-y-6">
      {/* Panel Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Routing Control Panel</h2>
          <p className="text-sm text-muted-foreground">
            Monitor and override backend/environment routing decisions
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Route className="w-4 h-4" />
          <span>{metricsList.length} backends</span>
        </div>
      </div>

      {/* Current Route */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">Current Route</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-3 rounded-lg bg-muted">
              <p className="text-xs text-muted-foreground mb-1">Backend</p>
              <p className="text-sm font-medium">
                {currentRoute.backend || 'Not selected'}
              </p>
            </div>
            <div className="p-3 rounded-lg bg-muted">
              <p className="text-xs text-muted-foreground mb-1">Environment</p>
              <p className="text-sm font-medium">
                {currentRoute.environment || 'Not selected'}
              </p>
            </div>
            <div className="p-3 rounded-lg bg-muted">
              <p className="text-xs text-muted-foreground mb-1">Mode</p>
              <p className="text-sm font-medium">
                {currentRoute.mode || 'auto'}
              </p>
            </div>
            <div className="p-3 rounded-lg bg-muted">
              <p className="text-xs text-muted-foreground mb-1">Data Sensitivity</p>
              <p className="text-sm font-medium">
                {currentRoute.dataSensitivity || 'Not set'}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Backend Metrics */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Backend Metrics ({metricsList.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[300px]">
            {metricsList.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <p className="text-sm">No backend metrics available</p>
              </div>
            ) : (
              <div className="space-y-3">
                {metricsList.map(([backendId, metrics]) => (
                  <div
                    key={backendId}
                    className={cn(
                      'p-4 rounded-lg border bg-card',
                      currentRoute.backend === backendId && 'border-primary border-2'
                    )}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <p className="font-medium text-sm">{backendId}</p>
                      {currentRoute.backend === backendId && (
                        <span className="text-xs text-primary font-medium">
                          ACTIVE
                        </span>
                      )}
                    </div>
                    <div className="grid grid-cols-4 gap-2 text-xs">
                      <div className="flex items-center gap-1">
                        <Cpu className="w-3 h-3 text-muted-foreground" />
                        <span>{metrics.total_calls}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <CheckCircle className="w-3 h-3 text-status-verified" />
                        <span>{metrics.success_count}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Clock className="w-3 h-3 text-muted-foreground" />
                        <span>{metrics.avg_latency.toFixed(0)}ms</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">
                          {(metrics.failure_count / Math.max(metrics.total_calls, 1) * 100).toFixed(1)}%
                        </span>
                        <span className="text-muted-foreground ml-1">fail</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </ScrollArea>
        </CardContent>
      </Card>

      {/* Routing History */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Recent Decisions ({routingHistory.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[200px]">
            {routingHistory.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <p className="text-sm">No routing history yet</p>
              </div>
            ) : (
              <div className="space-y-2">
                {routingHistory.slice(-10).reverse().map((decision) => (
                  <div
                    key={decision.decision_id}
                    className="flex items-center gap-3 p-2 rounded-lg bg-muted/50"
                  >
                    <div className="w-2 h-2 rounded-full bg-status-running" />
                    <span className="text-xs text-muted-foreground font-mono">
                      {new Date(decision.timestamp).toLocaleTimeString()}
                    </span>
                    <span className="text-xs">
                      {decision.decision_type}: <strong>{decision.selected}</strong>
                    </span>
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
