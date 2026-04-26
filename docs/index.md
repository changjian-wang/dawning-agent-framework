# Dawning Agent OS — Wiki 索引

> AI Agent 的操作系统：微内核 + 三面体架构 + 技能自演化（Memento-Skills）。
>
> 📋 本索引由 LLM 在每次 Ingest 操作时自动更新。
> 📅 操作日志见 [[log]]。⚙️ 模式定义见 [[SCHEMA]]。

---

## 1. 概念 (`concepts/`)

### 1.0 基础原理 (`concepts/00-foundations/`)

| 页面 | 说明 | 状态 |
|------|------|------|
| [[concepts/00-foundations/llm-fundamentals\|LLM 技术原理]] | Token、API、采样、Function Calling | active |
| [[concepts/00-foundations/llm-wiki-pattern.zh-CN\|LLM Wiki 模式]] | Karpathy 编译式知识管理 | active |
| [[concepts/00-foundations/embedding-models.zh-CN\|嵌入模型]] | 向量化基础、模型对比 | active |
| [[concepts/00-foundations/edge-small-models.zh-CN\|边缘 / 小模型]] | 端侧 LLM 与小参数模型 | active |
| [[concepts/00-foundations/inference-time-search.zh-CN\|推理时搜索]] | Best-of-N、MCTS、推理增强 | active |
| [[concepts/00-foundations/reasoning-models.zh-CN\|推理模型]] | o1 / DeepSeek-R1 类模型分析 | active |
| [[concepts/00-foundations/reasoning-algorithms.zh-CN\|推理算法]] | CoT / ToT / GoT 等推理范式 | active |
| [[concepts/00-foundations/post-training.zh-CN\|后训练]] | SFT / RLHF / DPO 概览 | active |

### 1.1 Agent 内核 (`concepts/01-agent-core/`)

| 页面 | 说明 | 状态 |
|------|------|------|
| [[concepts/01-agent-core/agent-os-architecture.zh-CN\|Agent OS 架构]] | **核心**：微内核、三面体、命名空间 | active |
| [[concepts/01-agent-core/agent-loop\|Agent Loop]] | ReAct / Plan-and-Execute / Reflexion | active |
| [[concepts/01-agent-core/multi-agent-patterns.zh-CN\|多 Agent 模式]] | Hierarchical / Network / Supervisor | active |
| [[concepts/01-agent-core/skill-evolution.zh-CN\|技能自演化]] | Memento-Skills 落地路径 | active |
| [[concepts/01-agent-core/dawning-capability-matrix.zh-CN\|能力矩阵]] | Dawning 能力清单 | active |

### 1.2 上下文与记忆 (`concepts/02-context-memory/`)

| 页面 | 说明 | 状态 |
|------|------|------|
| [[concepts/02-context-memory/context-management\|上下文管理]] | 五种流派对比 + Dawning 双层记忆 | active |
| [[concepts/02-context-memory/memory-architecture.zh-CN\|记忆架构]] | 短期 / 长期 / 工作记忆 | active |
| [[concepts/02-context-memory/state-persistence.zh-CN\|状态持久化]] | Checkpoint / Replay / 恢复 | active |
| [[concepts/02-context-memory/dataflow-channel-version.zh-CN\|Dataflow 编排基础]] | Channel / 版本号 / 激活判定 | active |

### 1.3 IO 与数据 (`concepts/03-io-data/`)

| 页面 | 说明 | 状态 |
|------|------|------|
| [[concepts/03-io-data/structured-output.zh-CN\|结构化输出]] | JSON Schema / Function Calling | active |
| [[concepts/03-io-data/multimodal-agents.zh-CN\|多模态 Agent]] | 视觉 / 音频 / 视频处理 | active |
| [[concepts/03-io-data/next-gen-rag.zh-CN\|下一代 RAG]] | GraphRAG / Agentic RAG | active |
| [[concepts/03-io-data/dataset-building.zh-CN\|数据集构建]] | Agent 训练数据生成 | active |

### 1.4 Prompt 与评测 (`concepts/04-prompt-eval/`)

| 页面 | 说明 | 状态 |
|------|------|------|
| [[concepts/04-prompt-eval/prompt-engineering-dspy.zh-CN\|Prompt 工程 / DSPy]] | 声明式 Prompt 编程 | active |
| [[concepts/04-prompt-eval/agent-evaluation.zh-CN\|Agent 评测]] | 评测指标 / 基准 / 工具 | active |

### 1.5 安全与合规 (`concepts/05-security-compliance/`)

| 页面 | 说明 | 状态 |
|------|------|------|
| [[concepts/05-security-compliance/agent-security.zh-CN\|Agent 安全]] | Prompt 注入、沙箱隔离 | active |
| [[concepts/05-security-compliance/agent-identity-auth.zh-CN\|Agent 身份认证]] | Agent-to-Agent 鉴权 | active |
| [[concepts/05-security-compliance/ai-compliance.zh-CN\|AI 合规]] | EU AI Act / NIST RMF | active |

### 1.6 运营 (`concepts/06-operations/`)

| 页面 | 说明 | 状态 |
|------|------|------|
| [[concepts/06-operations/observability-deep.zh-CN\|可观测性深潜]] | Tracing / Metrics / Eval-Loop | active |
| [[concepts/06-operations/deployment-architectures.zh-CN\|部署架构]] | Serverless / Edge / Hybrid | active |
| [[concepts/06-operations/cost-optimization.zh-CN\|成本优化]] | Token / 缓存 / 路由策略 | active |
| [[concepts/06-operations/enterprise-roadmap.zh-CN\|企业路线图]] | 企业级落地节奏 | active |

### 1.7 互操作与 UX (`concepts/07-interop-ux/`)

| 页面 | 说明 | 状态 |
|------|------|------|
| [[concepts/07-interop-ux/protocols-a2a-mcp.zh-CN\|A2A / MCP 协议]] | Agent 间通信协议 | active |
| [[concepts/07-interop-ux/agent-ux-patterns.zh-CN\|Agent UX 模式]] | Human-in-the-loop / Streaming | active |

## 2. 架构决策 (`decisions/`)

| 页面 | 说明 | 状态 |
|------|------|------|
| [[decisions/roadmap.zh-CN\|分层构建路线图]] | Layer 0–7 分层路径 | active |
| [[decisions/success-criteria.zh-CN\|成功标准清单]] | SC-1 ~ SC-10，49 项验收 | active |
| [[decisions/phase-0-overview\|Phase 0 概览]] | 历史文档（Agent Framework 时期）| active |
| [[decisions/layer-0-requirements.zh-CN\|L0 需求说明]] | LLM Driver 问题/约束 | active |
| [[decisions/layer-0-features.zh-CN\|L0 功能清单]] | 7 大功能域、63 项 | active |
| [[decisions/layer-0-tech-spec.zh-CN\|L0 技术规格]] | API / 数据模型 / DI | draft |

## 3. 实体页 (`entities/`)

### 3.1 Agent 框架 (`entities/frameworks/`)

| 框架 | 页面 | 语言 |
|------|------|------|
| MAF | [[entities/frameworks/microsoft-agent-framework.zh-CN]] | .NET / Python |
| Semantic Kernel | [[entities/frameworks/semantic-kernel.zh-CN]] | .NET / Python / Java |
| LangGraph | [[entities/frameworks/langgraph.zh-CN]] | Python / JS |
| LangChain | [[entities/frameworks/langchain.zh-CN]] | Python / JS |
| LlamaIndex | [[entities/frameworks/llamaindex.zh-CN]] | Python |
| CrewAI | [[entities/frameworks/crewai.zh-CN]] | Python |
| AutoGen | [[entities/frameworks/autogen.zh-CN]] | Python（停维 → MAF）|
| OpenAI Agents SDK | [[entities/frameworks/openai-agents-sdk.zh-CN]] | Python |
| Google ADK | [[entities/frameworks/google-adk.zh-CN]] | Python / Java / Go |
| Pydantic AI | [[entities/frameworks/pydantic-ai.zh-CN]] | Python |
| DSPy | [[entities/frameworks/dspy.zh-CN]] | Python |
| Smolagents | [[entities/frameworks/smolagents.zh-CN]] | Python |
| Agno | [[entities/frameworks/agno.zh-CN]] | Python |
| Mastra | [[entities/frameworks/mastra.zh-CN]] | TypeScript |
| Spring AI | [[entities/frameworks/spring-ai.zh-CN]] | Java |

## 4. 对比分析 (`comparisons/`)

| 页面 | 主题 |
|------|------|
| [[comparisons/agent-framework-landscape.zh-CN]] | 18 个框架横向全景 |
| [[comparisons/maf-vs-langgraph.zh-CN]] | MAF vs LangGraph 双雄对比 |
| [[comparisons/framework-modules-mapping.zh-CN]] | 框架模块到 Dawning 的映射 |
| [[comparisons/polyglot-agent-ecosystem.zh-CN]] | 多语言 Agent 生态 |
| [[comparisons/workflow-vs-agent.zh-CN]] | Workflow vs Agent 范式 |
| [[comparisons/function-calling-comparison.zh-CN]] | Function Calling 实现对比 |
| [[comparisons/llm-gateway-comparison.zh-CN]] | LLM Gateway 网关对比 |
| [[comparisons/local-llm-comparison.zh-CN]] | 本地 LLM 部署方案对比 |
| [[comparisons/vector-database-comparison.zh-CN]] | 向量数据库对比 |
| [[comparisons/rag-pipeline-comparison.zh-CN]] | RAG 流水线对比 |
| [[comparisons/research-agents.zh-CN]] | 研究型 Agent 对比 |
| [[comparisons/agentic-coding-deep-dive.zh-CN]] | Agentic Coding 深度对比 |
| [[comparisons/computer-use-agents.zh-CN]] | Computer-Use Agent 对比 |
| [[comparisons/agent-marketplace.zh-CN]] | Agent 市场/生态 |

## 5. 框架深读 (`frameworks/`)

入口：[[frameworks/README.zh-CN]]

### 5.1 LangGraph 深读 (`frameworks/langgraph/`)

入口：[[frameworks/langgraph/README.zh-CN]]

**Tier 1 — 直觉**

| # | 页面 |
|---|------|
| 01 | [[frameworks/langgraph/tier-1-intuition/01-what-is-langgraph.zh-CN]] |
| 02 | [[frameworks/langgraph/tier-1-intuition/02-hello-world.zh-CN]] |
| 03 | [[frameworks/langgraph/tier-1-intuition/03-mental-model.zh-CN]] |
| 04 | [[frameworks/langgraph/tier-1-intuition/04-tour-by-example.zh-CN]] |

**Tier 2 — 架构**

| # | 页面 |
|---|------|
| 00 | [[frameworks/langgraph/tier-2-architecture/00-overview.zh-CN]] |
| 01 | [[frameworks/langgraph/tier-2-architecture/01-architecture.zh-CN]] |

**Tier 3 — 源码内核**

| # | 页面 |
|---|------|
| 02 | [[frameworks/langgraph/tier-3-internals/02-state-graph.zh-CN]] |
| 03 | [[frameworks/langgraph/tier-3-internals/03-pregel-runtime.zh-CN]] |
| 04 | [[frameworks/langgraph/tier-3-internals/04-channels.zh-CN]] |
| 05 | [[frameworks/langgraph/tier-3-internals/05-checkpointer.zh-CN]] |
| 06 | [[frameworks/langgraph/tier-3-internals/06-interrupt-hitl.zh-CN]] |
| 07 | [[frameworks/langgraph/tier-3-internals/07-streaming.zh-CN]] |
| 08 | [[frameworks/langgraph/tier-3-internals/08-prebuilt-agents.zh-CN]] |
| 09 | [[frameworks/langgraph/tier-3-internals/09-subgraph-functional-api.zh-CN]] |
| 10 | [[frameworks/langgraph/tier-3-internals/10-platform-integration.zh-CN]] |

**Cases — 案例**

| 页面 | 场景 |
|------|------|
| [[frameworks/langgraph/cases/README.zh-CN]] | 案例索引 |
| [[frameworks/langgraph/cases/klarna-customer-support.zh-CN]] | Klarna 客服 |
| [[frameworks/langgraph/cases/linkedin-hr-agent.zh-CN]] | LinkedIn HR |
| [[frameworks/langgraph/cases/open-deep-research.zh-CN]] | Open Deep Research |
| [[frameworks/langgraph/cases/replit-agent.zh-CN]] | Replit Agent |
| [[frameworks/langgraph/cases/cross-case-comparison.zh-CN]] | 跨案例横评 |

**跨模块**

| 页面 |
|------|
| [[frameworks/langgraph/cross-module-comparison.zh-CN]] |

## 6. 深度阅读 (`readings/`)

### 6.1 MAF 源码解析 (`readings/frameworks/maf/`)

| 页面 | 说明 |
|------|------|
| [[readings/frameworks/maf/00-overview.zh-CN]] | MAF 项目结构全景 |
| [[readings/frameworks/maf/01-abstractions.zh-CN]] | Abstractions 层 |
| [[readings/frameworks/maf/02-agent-lifecycle.zh-CN]] | Agent 生命周期 |
| *03-llm-provider 等* | 待写 |

## 7. 综合分析 (`synthesis/`)

| 页面 | 说明 |
|------|------|
| *待补* | — |

## 8. 原始资料 (`raw/`)

| 资料 | 类型 | 摘入日期 |
|------|------|---------|
| [[raw/papers/memento-skills-2603.18743\|Memento-Skills]] | 论文 | 2026-04-07 |
| [[raw/articles/karpathy-llm-wiki\|Karpathy LLM Wiki]] | 博文 | 2026-04-07 |

---

## 统计

- 📄 Wiki 页面：94（含 frameworks/langgraph 深读体系）
- 📁 原始资料：2
- 📅 最后操作：2026-04-26 lint — SCHEMA 1.1 升级 + 全量 frontmatter 迁移

---

*最后更新：2026-04-26*
