---
title: "Roadmap: Layered Learning Path"
type: decision
tags: [roadmap, architecture, learning-path]
sources: [decisions/success-criteria.md, decisions/success-criteria.zh-CN.md]
created: 2026-04-08
updated: 2026-04-08
status: active
---

# Roadmap: Layered Learning Path

> Build an enterprise-grade distributed multi-agent .NET framework with skill self-evolution, one knowledge layer at a time.

## Guiding Principles

- **Depth over speed** — Fully understand each layer before implementing.
- **Dependency-driven order** — Each layer builds on the previous. No skipping.
- **Learn → Design → Build → Verify** — Every layer produces: framework study notes, a design decision doc (`decisions/`), implementation + tests, and verified SC items.
- **dawning-assistant as first consumer** — Every feature earns its place by being used.

## Dependency Graph

```
L0  LLM Provider Abstraction
 │
L1  Agent Loop & Tool Protocol
 │
L2  Memory System ─────────────────┐
 │                                  │
L3  Multi-Agent Orchestration ──────┤
 │                                  │
L4  Skill Router (Read Phase) ──────┘
 │
L5  Skill Evolution (Write Phase)
 │
L6  Distributed Architecture (Three-Plane)
 │
L7  Governance, Compliance & Observability
```

---

## Layer 0: LLM Provider Abstraction

**Prerequisites**: None.

**Knowledge to acquire**:
- Streaming protocols (SSE, chunked transfer)
- Token counting and context window management
- Function calling / tool-use schema (OpenAI, Ollama, Azure OpenAI)
- Provider failover and retry patterns

**Deliverables**:
- `ILLMProvider` interface (ChatAsync, ChatStreamAsync, ChatStreamEventsAsync)
- Unified streaming event model (TextDelta, ToolCallRequested, ToolCallCompleted, RunCompleted, Error)
- At least 2 providers: Ollama (local) + OpenAI (remote)
- Token usage / latency / cost tracking per call
- Provider contract test suite

**Verifies**: SC-7 (LLM Provider Layer)

**Design doc**: `decisions/llm-provider-design.md`

---

## Layer 1: Agent Loop & Tool Protocol

**Prerequisites**: Layer 0.

**Knowledge to acquire**:
- Native Function Calling / Tool Use protocols (OpenAI `tool_calls`, Anthropic `tool_use`, Ollama)
- Agent execution loop: prompt assembly → LLM call → tool call decision (model-native) → tool execution → result injection → loop / terminate
- Parallel tool calling (modern models return multiple tool calls in one response)
- Tool protocol standardization: MCP (Model Context Protocol) as emerging standard
- Structured Output (JSON mode, `response_format`) for reliable parsing
- Tool definition schema (JSON Schema) and result marshalling
- Stateful prompt assembly (system instructions + skills + memory context + tool definitions)
- Loop termination strategies: model-autonomous stop vs max-step / max-token budget
- Prompt immutability during execution

**Deliverables**:
- Core agent loop: prompt assembly → LLM call → native tool call parsing → tool dispatch → result injection → repeat / terminate
- Parallel tool call support (dispatch multiple tools concurrently when model requests it)
- Tool registration via DI with JSON Schema definition
- MCP-compatible tool protocol abstraction
- Structured Output support for non-tool responses
- StatefulPrompt record with versioning
- StatefulPrompt diff between consecutive runs
- Max-step and max-token budget enforcement

**Verifies**: SC-3 (Stateful Prompt Protocol)

**Design doc**: `decisions/agent-loop-design.md`

---

## Layer 2: Memory System

**Prerequisites**: Layer 1.

**Knowledge to acquire**:
- Embedding models and vector similarity search
- Context window management strategies (buffer, sliding window, summary compression)
- Importance-weighted recall with temporal decay
- Memory compaction without knowledge loss

**Deliverables**:
- Short-term memory with configurable strategy (buffer / sliding window / summary)
- Long-term memory with semantic vector retrieval
- Composite recall scoring: semantic similarity × recency × importance
- Cross-session recall verified at >= 90% on test set
- Automatic compaction above context window threshold

**Verifies**: SC-8 (Memory System)

**Design doc**: `decisions/memory-system-design.md`

---

## Layer 3: Multi-Agent Orchestration

**Prerequisites**: Layer 1 + Layer 2.

**Knowledge to acquire**:
- Workflow primitives: sequential, parallel, conditional-branch, retry/compensation
- Handoff protocol: ownership transfer, context snapshot, budget passing
- Delegation depth control
- Shared memory namespace model (global / team / session / private)

**Deliverables**:
- Orchestrator with 4 workflow primitives
- Atomic handoff contract (HandoffEnvelope)
- Configurable delegation depth with policy violation halt
- 4-tier memory scope isolation
- 5-agent deterministic integration test with full audit trail

**Verifies**: SC-2 (Multi-Agent Collaboration)

**Design doc**: `decisions/multi-agent-orchestration-design.md`

---

## Layer 4: Skill Router (Read Phase)

**Prerequisites**: Layer 2 + Layer 3.

**Knowledge to acquire**:
- Multi-signal scoring models (semantic similarity, success rate, recency, failure patterns)
- Online feedback loops (utility signals without weight updates)
- Confidence thresholds and fallback strategies
- Routing benchmark design

**Deliverables**:
- Router that accepts prompt state + task description + user hints → top-k scored skills
- 5 scoring features: semantic similarity, historical success rate, recency, failure pattern match, when-to-use metadata
- Configurable confidence threshold with fallback (full injection or user clarification)
- Online feedback: post-run utility signal per selected skill
- Top-5 hit rate >= 85% on benchmark (>= 30 scenarios)

**Verifies**: SC-4 (Skill Router)

**Design doc**: `decisions/skill-router-design.md`

---

## Layer 5: Skill Evolution (Write Phase)

**Prerequisites**: Layer 4.

**Knowledge to acquire**:
- Reflection pipelines (trajectory summarization, root-cause analysis)
- Candidate patch generation (structured markdown diff)
- Quality gates: lint, policy compliance, regression evaluation, human approval
- Skill artifact schema: intent, when-to-use, limitations, failure-patterns, examples, revision-metadata
- Canary release and automatic rollback

**Deliverables**:
- Post-run reflection pipeline → structured trajectory summary
- Candidate skill patch generation when improvement is identified
- 4-stage quality gate pipeline (lint → policy → regression → optional human approval)
- Versioned skill registry (append-only, any historical version retrievable)
- Canary release with configurable traffic percentage
- Automatic rollback on metric degradation
- Deprecated skill governance workflow (deprecate → grace period → archive)

**Verifies**: SC-5 (Reflective Skill Evolution) + SC-6 (Skill Lifecycle Management)

**Design doc**: `decisions/skill-evolution-design.md`

---

## Layer 6: Distributed Architecture (Three-Plane)

**Prerequisites**: Layer 3 + Layer 5.

**Knowledge to acquire**:
- Control Plane design: agent registry, policy store, skill lifecycle manager, evaluation scheduler
- Runtime Plane design: task queue consumers, durable checkpoints, lease/heartbeat, graceful drain
- Memory Plane as independently scalable services
- Async message contracts: AgentTaskEnvelope, HandoffEnvelope, SkillArtifact, PolicyDecision
- Idempotency protocols and chaos testing
- Schema evolution (additive-only, versioned registry)

**Deliverables**:
- Control Plane with 4 components (registry, policy store, skill lifecycle, evaluation scheduler)
- Runtime Plane with durable checkpoint/resume and rolling deploy
- Memory Plane split into independent short-term and long-term services
- Versioned async contracts with correlation/causation IDs
- Transport abstraction (`IMessageBus`) with in-memory and durable backends
- Idempotency protocol verified by chaos test suite

**Verifies**: SC-1 (Distributed Architecture)

**Design doc**: `decisions/distributed-architecture-design.md`

---

## Layer 7: Governance, Compliance & Observability

**Prerequisites**: Layer 6.

**Knowledge to acquire**:
- RBAC models for tool execution, skill publishing, agent deployment, memory access
- Immutable audit log design (append-only, tamper-evident)
- PII/secret redaction in logs and traces
- Tool execution policy engine (allowlist, denylist, risk-level gates)
- OpenTelemetry span hierarchies
- SLO definition and enforcement in CI/CD
- Evaluation report design (per-skill, per-agent, per-workflow)

**Deliverables**:
- RBAC enforcement across 5 domains
- Immutable append-only audit log
- Configurable PII/secret redaction pipeline
- Tool execution policy: allowlist + denylist + risk-level confirmation gates
- Skill evolution policy firewall (blocks unsafe patterns)
- Compliance evidence export (JSON + PDF)
- OpenTelemetry traces with run → step → call hierarchy
- Metrics: success rate, step count, tokens, cost, latency percentiles, router hit rate, evolution gain
- SLO gates blocking release promotion on regression
- Nightly evaluation report (versioned, diffable)

**Verifies**: SC-9 (Security, Compliance, Governance) + SC-10 (Observability, SLOs, Release Gates)

**Design doc**: `decisions/governance-observability-design.md`

---

## Cross-References

- [[decisions/success-criteria]] — Full 49-item verification checklist (SC-1 through SC-10)
- [[decisions/phase-0-overview]] — Technology stack and architectural principles
- [[comparisons/agent-framework-landscape.zh-CN]] — 18-framework competitive analysis
- [[concepts/llm-fundamentals]] — LLM fundamentals reference
- [[raw/papers/memento-skills-2603.18743]] — Research basis for skill self-evolution
