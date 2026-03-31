'use client';

import { useState, useEffect } from 'react';
import { wsClient } from '@/lib/websocket';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Key, Lock, Unlock, Trash2, Plus, AlertCircle, CheckCircle } from 'lucide-react';

const PROVIDERS = [
  { value: 'minimax', label: 'MiniMax' },
  { value: 'openai', label: 'OpenAI' },
  { value: 'anthropic', label: 'Anthropic' },
  { value: 'gemini', label: 'Google Gemini' },
  { value: 'openrouter', label: 'OpenRouter' },
  { value: 'litellm', label: 'LiteLLM' },
];

export function APIKeysPanel() {
  const [masterKey, setMasterKey] = useState('');
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [providers, setProviders] = useState<string[]>([]);
  const [selectedProvider, setSelectedProvider] = useState('minimax');
  const [apiKey, setApiKey] = useState('');
  const [statusMessage, setStatusMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    checkStatus();
  }, []);

  const checkStatus = async () => {
    try {
      const status = await wsClient.apiKeysStatus();
      setIsUnlocked(status.isUnlocked);
      setProviders(status.providers);
    } catch (e) {
      console.error('Failed to check API keys status:', e);
    }
  };

  const handleUnlock = async () => {
    if (!masterKey.trim()) {
      setStatusMessage({ type: 'error', text: 'Please enter a master key' });
      return;
    }
    setIsLoading(true);
    setStatusMessage(null);
    try {
      const result = await wsClient.apiKeysUnlock(masterKey);
      if (result.success) {
        setIsUnlocked(true);
        setProviders(result.providers || []);
        setStatusMessage({ type: 'success', text: 'Session unlocked successfully' });
      } else {
        setStatusMessage({ type: 'error', text: result.error || 'Failed to unlock' });
      }
    } catch (e) {
      setStatusMessage({ type: 'error', text: 'Failed to unlock session' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleLock = async () => {
    setIsLoading(true);
    try {
      await wsClient.apiKeysLock();
      setIsUnlocked(false);
      setProviders([]);
      setMasterKey('');
      setStatusMessage({ type: 'success', text: 'Session locked' });
    } catch (e) {
      setStatusMessage({ type: 'error', text: 'Failed to lock session' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveKey = async () => {
    if (!apiKey.trim()) {
      setStatusMessage({ type: 'error', text: 'Please enter an API key' });
      return;
    }
    setIsLoading(true);
    setStatusMessage(null);
    try {
      const result = await wsClient.apiKeysSet(selectedProvider, apiKey, masterKey);
      if (result.success) {
        setApiKey('');
        if (!providers.includes(selectedProvider)) {
          setProviders([...providers, selectedProvider]);
        }
        setStatusMessage({ type: 'success', text: `${selectedProvider} API key saved` });
      } else {
        setStatusMessage({ type: 'error', text: result.error || 'Failed to save key' });
      }
    } catch (e) {
      setStatusMessage({ type: 'error', text: 'Failed to save API key' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteKey = async (provider: string) => {
    setIsLoading(true);
    setStatusMessage(null);
    try {
      const result = await wsClient.apiKeysDelete(provider, masterKey);
      if (result.success) {
        setProviders(providers.filter(p => p !== provider));
        setStatusMessage({ type: 'success', text: `${provider} API key deleted` });
      } else {
        setStatusMessage({ type: 'error', text: result.error || 'Failed to delete key' });
      }
    } catch (e) {
      setStatusMessage({ type: 'error', text: 'Failed to delete API key' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">API Key Management</h2>
          <p className="text-sm text-muted-foreground">
            Securely store and manage your API keys
          </p>
        </div>
        <Button size="sm" variant="outline" onClick={handleLock} disabled={!isUnlocked || isLoading}>
          <Lock className="w-3 h-3 mr-1" />
          Lock
        </Button>
      </div>

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base flex items-center gap-2">
            {isUnlocked ? <Unlock className="w-4 h-4 text-green-500" /> : <Lock className="w-4 h-4" />}
            Session {isUnlocked ? 'Unlocked' : 'Locked'}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
            <input
              type="password"
              placeholder="Enter master key to unlock session"
              className="flex-1 p-2 rounded-lg border border-border bg-background text-sm"
              value={masterKey}
              onChange={(e) => setMasterKey(e.target.value)}
              disabled={isUnlocked}
            />
            {!isUnlocked && (
              <Button onClick={handleUnlock} disabled={isLoading}>
                <Unlock className="w-3 h-3 mr-1" />
                Unlock
              </Button>
            )}
          </div>
          {isUnlocked && (
            <p className="text-xs text-muted-foreground">
              Session unlocked. Master key is kept in memory only.
            </p>
          )}
        </CardContent>
      </Card>

      {statusMessage && (
        <div className={`flex items-center gap-2 p-3 rounded-lg ${statusMessage.type === 'success' ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'}`}>
          {statusMessage.type === 'success' ? <CheckCircle className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
          <span className="text-sm">{statusMessage.text}</span>
        </div>
      )}

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base flex items-center gap-2">
            <Plus className="w-4 h-4" />
            Add API Key
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                Provider
              </label>
              <select
                className="w-full p-2 rounded-lg border border-border bg-background text-sm"
                value={selectedProvider}
                onChange={(e) => setSelectedProvider(e.target.value)}
                disabled={!isUnlocked}
              >
                {PROVIDERS.map((p) => (
                  <option key={p.value} value={p.value}>
                    {p.label}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                API Key
              </label>
              <input
                type="password"
                placeholder="Enter API key"
                className="w-full p-2 rounded-lg border border-border bg-background text-sm"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                disabled={!isUnlocked}
              />
            </div>
          </div>
          <Button onClick={handleSaveKey} disabled={!isUnlocked || isLoading} className="w-full">
            <Key className="w-3 h-3 mr-1" />
            Save Key
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base flex items-center gap-2">
            <Key className="w-4 h-4" />
            Stored Keys
          </CardTitle>
        </CardHeader>
        <CardContent>
          {providers.length === 0 ? (
            <p className="text-sm text-muted-foreground text-center py-4">
              No API keys stored. Unlock the session and add a key above.
            </p>
          ) : (
            <div className="space-y-2">
              {providers.map((provider) => (
                <div key={provider} className="flex items-center justify-between p-3 rounded-lg border border-border">
                  <div className="flex items-center gap-2">
                    <Key className="w-4 h-4 text-muted-foreground" />
                    <span className="text-sm font-medium">{provider}</span>
                  </div>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => handleDeleteKey(provider)}
                    disabled={isLoading}
                    className="text-red-500 hover:text-red-400 hover:bg-red-500/10"
                  >
                    <Trash2 className="w-3 h-3" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}