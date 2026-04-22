# Concepts Documentation / 概念文档

> Core concept documents for Dawning Agent OS, organized into 8 thematic categories.
> Dawning Agent OS 的核心概念文档，按 8 大主题分类组织。

---

## Learning Path / 学习路径

**Recommended order / 推荐顺序**: `00 → 01 → 02 → 03 → 04 → 05 → 06 → 07`

- **Beginner 入门**: 00 → 01 (understand LLM + Agent Loop)
- **Builder 构建者**: 02 → 03 → 04 (memory + I/O + prompting)
- **Production 生产**: 05 → 06 (security + ops)
- **Ecosystem 生态**: 07 (interop + UX)

---

## 00. Foundations / 基础 — LLM & Model Fundamentals

LLM 工作原理、推理与训练、模型选型

| Document | Description |
|----------|-------------|
| [llm-fundamentals.md](00-foundations/llm-fundamentals.md) | LLM 基础：Transformer, token, attention |
| [llm-wiki-pattern.zh-CN.md](00-foundations/llm-wiki-pattern.zh-CN.md) | Karpathy LLM Wiki 模式 |
| [post-training.zh-CN.md](00-foundations/post-training.zh-CN.md) | 后训练：SFT / RLHF / DPO |
| [reasoning-models.zh-CN.md](00-foundations/reasoning-models.zh-CN.md) | 推理模型：o1 / R1 / CoT |
| [reasoning-algorithms.zh-CN.md](00-foundations/reasoning-algorithms.zh-CN.md) | 推理算法：ToT / GoT / Self-Consistency |
| [inference-time-search.zh-CN.md](00-foundations/inference-time-search.zh-CN.md) | 推理时搜索与扩展 |
| [embedding-models.zh-CN.md](00-foundations/embedding-models.zh-CN.md) | Embedding 模型与向量检索 |
| [edge-small-models.zh-CN.md](00-foundations/edge-small-models.zh-CN.md) | 边缘与小模型部署 |

## 01. Agent Core / Agent 核心 — Loop, Architecture, Capabilities

Agent 执行循环、架构、能力矩阵

| Document | Description |
|----------|-------------|
| [agent-loop.md](01-agent-core/agent-loop.md) | Agent 执行循环（Perceive-Plan-Act） |
| [agent-os-architecture.zh-CN.md](01-agent-core/agent-os-architecture.zh-CN.md) | Agent OS 微内核架构 |
| [multi-agent-patterns.zh-CN.md](01-agent-core/multi-agent-patterns.zh-CN.md) | 多 Agent 协作模式 |
| [skill-evolution.zh-CN.md](01-agent-core/skill-evolution.zh-CN.md) | Skill 演化与自学习 |
| [dawning-capability-matrix.zh-CN.md](01-agent-core/dawning-capability-matrix.zh-CN.md) | Dawning 能力矩阵 |

## 02. Context & Memory / 上下文与记忆 — State Management

上下文工程、记忆架构、状态持久化

| Document | Description |
|----------|-------------|
| [context-management.md](02-context-memory/context-management.md) | Context 工程与窗口管理 |
| [memory-architecture.zh-CN.md](02-context-memory/memory-architecture.zh-CN.md) | 短期 / 长期 / 工作记忆架构 |
| [state-persistence.zh-CN.md](02-context-memory/state-persistence.zh-CN.md) | 状态持久化（Checkpoint/Event Sourcing） |
| [dataflow-channel-version.zh-CN.md](02-context-memory/dataflow-channel-version.zh-CN.md) | 数据流通道与版本控制 |

## 03. I/O & Data / 输入输出与数据 — Structured Output, Multimodal, RAG

结构化输出、多模态、RAG、数据集

| Document | Description |
|----------|-------------|
| [structured-output.zh-CN.md](03-io-data/structured-output.zh-CN.md) | 结构化输出（Function Call / JSON Schema） |
| [multimodal-agents.zh-CN.md](03-io-data/multimodal-agents.zh-CN.md) | 多模态 Agent |
| [next-gen-rag.zh-CN.md](03-io-data/next-gen-rag.zh-CN.md) | 下一代 RAG |
| [dataset-building.zh-CN.md](03-io-data/dataset-building.zh-CN.md) | 数据集构建 |

## 04. Prompt & Evaluation / 提示与评估 — Engineering & Measurement

提示工程与 Agent 评估

| Document | Description |
|----------|-------------|
| [prompt-engineering-dspy.zh-CN.md](04-prompt-eval/prompt-engineering-dspy.zh-CN.md) | 提示工程与 DSPy |
| [agent-evaluation.zh-CN.md](04-prompt-eval/agent-evaluation.zh-CN.md) | Agent 评估方法论 |

## 05. Security & Compliance / 安全与合规

Agent 安全、身份认证、AI 合规

| Document | Description |
|----------|-------------|
| [agent-security.zh-CN.md](05-security-compliance/agent-security.zh-CN.md) | Agent 安全威胁与防护 |
| [agent-identity-auth.zh-CN.md](05-security-compliance/agent-identity-auth.zh-CN.md) | Agent 身份与授权 |
| [ai-compliance.zh-CN.md](05-security-compliance/ai-compliance.zh-CN.md) | AI 合规（EU AI Act / GDPR） |

## 06. Operations / 运维 — Deployment, Observability, Cost

部署架构、可观测性、成本优化、企业路线图

| Document | Description |
|----------|-------------|
| [deployment-architectures.zh-CN.md](06-operations/deployment-architectures.zh-CN.md) | 部署架构（Cloud / Edge / Hybrid） |
| [observability-deep.zh-CN.md](06-operations/observability-deep.zh-CN.md) | 深度可观测性 |
| [cost-optimization.zh-CN.md](06-operations/cost-optimization.zh-CN.md) | 成本优化策略 |
| [enterprise-roadmap.zh-CN.md](06-operations/enterprise-roadmap.zh-CN.md) | 企业 Agent 落地路线图 |

## 07. Interop & UX / 互操作与用户体验

协议互通与 Agent 用户体验

| Document | Description |
|----------|-------------|
| [protocols-a2a-mcp.zh-CN.md](07-interop-ux/protocols-a2a-mcp.zh-CN.md) | A2A 与 MCP 协议 |
| [agent-ux-patterns.zh-CN.md](07-interop-ux/agent-ux-patterns.zh-CN.md) | Agent UX 设计模式 |

---

## Related Sections / 相关章节

- [../decisions/](../decisions/) — Architecture decisions (ADR) / 架构决策
- [../entities/frameworks/](../entities/frameworks/) — Framework deep-dives / 框架深度分析
- [../comparisons/](../comparisons/) — Framework landscape / 框架全景对比
- [../frameworks/](../frameworks/) — Framework quick reference / 框架速查
