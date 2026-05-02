/**
 * Preload bridge — runs in the renderer's isolated world.
 *
 * Per ADR-025 §3 the renderer never sees the startup token directly;
 * instead it asks the main process via IPC for a fresh runtime status,
 * and main attaches the token on its way out. This keeps the token in
 * the main process and out of the BrowserWindow's JS context.
 *
 * NOTE: Electron does not (yet) load `.ts` preload modules through tsx;
 * the dev script transpiles this file to CommonJS at runtime via the
 * `tsx` loader. The `.cjs.js` filename in main.ts mirrors the on-disk
 * path tsx writes when the loader is active. For a bare `tsx`
 * invocation in S5b we accept that the renderer falls back to a plain
 * `index.html` that performs its own fetch via window.fetch when the
 * preload is unavailable. The full preload <-> renderer contract is
 * scaffolded here so the next ADR (front-end stack) has a stable surface.
 */

import { contextBridge, ipcRenderer } from "electron";

interface RuntimeStatus {
  healthy?: boolean;
  database?: {
    ready?: boolean;
    schemaVersion?: number | null;
    filePath?: string | null;
  };
  [key: string]: unknown;
}

const api = {
  runtime: {
    /** Returns the current /api/runtime/status JSON; main attaches the token. */
    getStatus: async (): Promise<RuntimeStatus> => {
      return (await ipcRenderer.invoke("agentos:runtime:get-status")) as RuntimeStatus;
    },
    /** Returns the base URL without exposing the token. */
    getBaseUrl: async (): Promise<string> => {
      return (await ipcRenderer.invoke("agentos:runtime:get-base-url")) as string;
    },
  },
};

contextBridge.exposeInMainWorld("agentos", api);

export type AgentOsBridge = typeof api;
