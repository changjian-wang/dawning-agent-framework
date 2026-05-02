/**
 * Electron main process entry.
 *
 * Per ADR-025 §1 / §3 / §4 / §5 / §6 this file:
 *
 *   1. Generates a startup token (crypto.randomUUID()).
 *   2. Spawns dotnet as a child process with the token + ASPNETCORE_URLS env.
 *   3. Waits for the child's `Now listening on:` line to learn the port.
 *   4. HTTP-polls /api/runtime/status until healthy + database.ready.
 *   5. Opens the BrowserWindow only after readiness; renderer fetches
 *      its status through the preload bridge.
 *   6. On window-all-closed, sends SIGTERM (10s grace, then SIGKILL) and
 *      quits Electron. process.exit / crash also runs the SIGTERM path.
 */

import { app, BrowserWindow, ipcMain } from "electron";
import { randomUUID } from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";
import type { BackendChildProcess } from "./supervisor/spawn-backend.ts";

import { spawnBackend, HEADER_NAME } from "./supervisor/spawn-backend.ts";
import { awaitListening } from "./supervisor/port-handshake.ts";
import { probeUntilReady } from "./supervisor/readiness-probe.ts";
import { shutdownBackend } from "./supervisor/shutdown.ts";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

interface RuntimeContext {
  child: BackendChildProcess;
  baseUrl: string;
  token: string;
}

let runtime: RuntimeContext | undefined;

async function startBackend(): Promise<RuntimeContext> {
  const token = randomUUID();
  const child = spawnBackend({ token });

  const onceProcessDies = () => {
    if (runtime?.child === child) {
      void shutdownBackend(child).then(() => {
        // best-effort; process is exiting anyway
      });
    }
  };
  process.once("exit", onceProcessDies);
  process.once("SIGINT", onceProcessDies);
  process.once("SIGTERM", onceProcessDies);

  const listening = await awaitListening(child, 30_000);
  const ready = await probeUntilReady({
    baseUrl: listening.baseUrl,
    token,
    intervalMs: 250,
    timeoutMs: 30_000,
  });
  console.log(
    `[main] api ready in ${ready.durationMs}ms (schemaVersion=${ready.status.database?.schemaVersion ?? "?"})`,
  );

  return { child, baseUrl: listening.baseUrl, token };
}

function createWindow(context: RuntimeContext): BrowserWindow {
  const window = new BrowserWindow({
    width: 720,
    height: 480,
    title: "Dawning Agent OS — V0",
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs.js"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      additionalArguments: [
        `--agentos-base-url=${context.baseUrl}`,
        `--agentos-token=${context.token}`,
      ],
    },
  });

  void window.loadFile(path.join(__dirname, "renderer", "index.html"));
  return window;
}

// Register an IPC handler so the preload bridge can ask main for a
// fresh runtime status without exposing the token to the renderer
// process directly. The token lives in the main process only.
ipcMain.handle("agentos:runtime:get-status", async () => {
  if (!runtime) {
    throw new Error("runtime not initialized");
  }
  const response = await fetch(`${runtime.baseUrl}/api/runtime/status`, {
    headers: { [HEADER_NAME]: runtime.token },
  });
  return response.json();
});

ipcMain.handle("agentos:runtime:get-base-url", () => {
  return runtime?.baseUrl ?? "";
});

app.whenReady().then(async () => {
  try {
    runtime = await startBackend();
  } catch (err) {
    console.error("[main] failed to start backend:", err);
    app.exit(1);
    return;
  }
  createWindow(runtime);
});

app.on("window-all-closed", () => {
  void (async () => {
    if (runtime) {
      await shutdownBackend(runtime.child, 10_000);
    }
    app.quit();
  })();
});
