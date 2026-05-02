/**
 * Headless smoke probe — does not require an Electron head.
 *
 * Per ADR-025 §7 this script:
 *
 *   1. spawns dotnet (same args as `src/main.ts`);
 *   2. parses stdout for the listening port;
 *   3. polls /api/runtime/status with the startup token;
 *   4. asserts healthy=true && database.ready=true && database.schemaVersion>=1;
 *   5. SIGTERM's the child;
 *   6. exits 0 on success, 1 on failure.
 *
 * Designed for CI runners with no graphics stack; safe to run from any
 * macOS / Linux shell.
 */

import { randomUUID } from "node:crypto";

import { spawnBackend } from "../src/supervisor/spawn-backend.ts";
import { awaitListening } from "../src/supervisor/port-handshake.ts";
import { probeUntilReady } from "../src/supervisor/readiness-probe.ts";
import { shutdownBackend } from "../src/supervisor/shutdown.ts";

async function main(): Promise<void> {
  const token = randomUUID();
  // Smoke runs do not stream stdout to console by default — the
  // handshake parser owns the stream and we keep the test output
  // focused on PASS / FAIL.
  const child = spawnBackend({ token, inheritStdio: false });
  console.log(`[smoke] spawned dotnet (pid=${child.pid ?? "?"})`);

  let baseUrl: string | undefined;
  try {
    // Cold `dotnet run` (msbuild restore + JIT) can take ~30s; allow up
    // to 90s for the listening line so CI / first-run scenarios pass.
    const listening = await awaitListening(child, 90_000);
    baseUrl = listening.baseUrl;
    console.log(`[smoke] api listening on ${baseUrl}`);

    const ready = await probeUntilReady({
      baseUrl,
      token,
      intervalMs: 250,
      timeoutMs: 30_000,
    });
    const version = ready.status.database?.schemaVersion ?? "?";
    console.log(`[smoke] status ready (schemaVersion=${version}) in ${ready.durationMs}ms`);
    console.log("[smoke] PASS");
  } catch (err) {
    console.error(
      `[smoke] FAIL: ${err instanceof Error ? err.message : String(err)}`,
    );
    process.exitCode = 1;
  } finally {
    await shutdownBackend(child, 10_000);
  }
}

void main();
