'use client';

import { useConsoleStore } from '@/store/console-store';
import { wsClient } from '@/lib/websocket';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Settings, Save, RotateCcw, Globe, Shield } from 'lucide-react';

export function ConfigPanel() {
  const systemStatus = useConsoleStore((s) => s.systemStatus);

  const handleUpdateConfig = (key: string, value: unknown) => {
    wsClient.dispatch({
      type: 'system/update_configuration',
      payload: { key, value },
    });
  };

  const handleResetConfig = () => {
    wsClient.dispatch({
      type: 'system/reset_configuration',
      payload: {},
    });
  };

  const handleExportConfig = () => {
    wsClient.dispatch({
      type: 'system/export_configuration',
      payload: {},
    });
  };

  return (
    <div className="space-y-6">
      {/* Panel Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">System Configuration</h2>
          <p className="text-sm text-muted-foreground">
            Runtime adjustment of system parameters
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button size="sm" variant="outline" onClick={handleExportConfig}>
            <Save className="w-3 h-3 mr-1" />
            Export
          </Button>
          <Button size="sm" variant="outline" onClick={handleResetConfig}>
            <RotateCcw className="w-3 h-3 mr-1" />
            Reset
          </Button>
        </div>
      </div>

      {/* Real-time Settings */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base flex items-center gap-2">
            <Globe className="w-4 h-4" />
            Real-time Updates
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                Connection Mode
              </label>
              <select
                className="w-full p-2 rounded-lg border border-border bg-background text-sm"
                onChange={(e) =>
                  handleUpdateConfig('realtime.mode', e.target.value)
                }
              >
                <option value="websocket">WebSocket (Push)</option>
                <option value="polling">Polling</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                Poll Interval (ms)
              </label>
              <input
                type="number"
                className="w-full p-2 rounded-lg border border-border bg-background text-sm"
                defaultValue={1000}
                onChange={(e) =>
                  handleUpdateConfig('realtime.pollInterval', parseInt(e.target.value))
                }
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Security Settings */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base flex items-center gap-2">
            <Shield className="w-4 h-4" />
            Security Settings
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <label className="flex items-center justify-between">
              <span className="text-sm">Message Validation</span>
              <input
                type="checkbox"
                className="w-4 h-4"
                defaultChecked
                onChange={(e) =>
                  handleUpdateConfig('security.messageValidation', e.target.checked)
                }
              />
            </label>
            <label className="flex items-center justify-between">
              <span className="text-sm">Tool Approval Required</span>
              <input
                type="checkbox"
                className="w-4 h-4"
                defaultChecked
                onChange={(e) =>
                  handleUpdateConfig('security.toolApprovalRequired', e.target.checked)
                }
              />
            </label>
            <label className="flex items-center justify-between">
              <span className="text-sm">Agent Isolation</span>
              <input
                type="checkbox"
                className="w-4 h-4"
                defaultChecked
                onChange={(e) =>
                  handleUpdateConfig('security.agentIsolation', e.target.checked)
                }
              />
            </label>
          </div>
        </CardContent>
      </Card>

      {/* Resource Limits */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base flex items-center gap-2">
            <Settings className="w-4 h-4" />
            Resource Limits
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                Max CPU (%)
              </label>
              <input
                type="number"
                className="w-full p-2 rounded-lg border border-border bg-background text-sm"
                defaultValue={80}
                onChange={(e) =>
                  handleUpdateConfig('resourceLimits.cpu', parseInt(e.target.value))
                }
              />
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                Max Memory (MB)
              </label>
              <input
                type="number"
                className="w-full p-2 rounded-lg border border-border bg-background text-sm"
                defaultValue={4096}
                onChange={(e) =>
                  handleUpdateConfig('resourceLimits.memory', parseInt(e.target.value))
                }
              />
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                Max Tokens/min
              </label>
              <input
                type="number"
                className="w-full p-2 rounded-lg border border-border bg-background text-sm"
                defaultValue={100000}
                onChange={(e) =>
                  handleUpdateConfig('resourceLimits.tokens', parseInt(e.target.value))
                }
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Retention Settings */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">Session & Retention</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                Max Threads
              </label>
              <input
                type="number"
                className="w-full p-2 rounded-lg border border-border bg-background text-sm"
                defaultValue={50}
                onChange={(e) =>
                  handleUpdateConfig('retention.maxThreads', parseInt(e.target.value))
                }
              />
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                Auto-archive After (sessions)
              </label>
              <input
                type="number"
                className="w-full p-2 rounded-lg border border-border bg-background text-sm"
                defaultValue={10}
                onChange={(e) =>
                  handleUpdateConfig('retention.autoArchiveAfter', parseInt(e.target.value))
                }
              />
            </div>
          </div>
          <label className="flex items-center justify-between">
            <span className="text-sm">Save all sessions (no auto-cleanup)</span>
            <input
              type="checkbox"
              className="w-4 h-4"
              onChange={(e) =>
                handleUpdateConfig('retention.persistAll', e.target.checked)
              }
            />
          </label>
        </CardContent>
      </Card>
    </div>
  );
}
