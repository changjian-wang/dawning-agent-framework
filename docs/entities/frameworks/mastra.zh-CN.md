---
title: "Mastra 详细分析"
type: entity
tags: [framework, mastra, typescript, nodejs, fullstack]
status: active
created: 2026-04-22
subtype: framework
sources: []
updated: 2026-04-22
---

# Mastra 详细分析

> TypeScript 全栈 Agent 框架，由 Gatsby 创始团队打造。**Node.js 生态的"LangGraph + LangSmith + LangServe 合体"**。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **官方名称** | Mastra |
| **维护者** | Mastra（Kyle Mathews 团队，Gatsby 创始人） |
| **仓库** | https://github.com/mastra-ai/mastra |
| **文档** | https://mastra.ai/ |
| **语言** | TypeScript |
| **许可证** | Elastic License 2.0 |
| **Stars** | 13k+ |
| **最新版本** | v0.x（快速演进） |
| **核心差异化** | TS-First + 内建部署 + 本地开发 UI |

---

## 1. 定位与背景

Mastra 2025 年发布，填补了 **TypeScript Agent 框架**的空白。之前 JS/TS 开发者只能用 LangChain.js（Python 移植）或 Vercel AI SDK（过于底层）。

**核心理念**：
- **TS 是 Agent 的原生语言**：类型系统天然适合 Tool Schema、结构化输出
- **全栈一体**：Agent 定义 → 本地 Playground → Serverless 部署 一把梭
- **开发者体验第一**：`mastra dev` 起本地 UI，对标 LangGraph Studio

---

## 2. 架构设计

### 2.1 四大支柱

````mermaid
graph TB
    subgraph APP["应用代码"]
        A1["new Agent({...})"]
        A2["createTool({...})"]
        A3["createWorkflow({...})"]
    end

    subgraph CORE["Mastra 核心"]
        C1["Agent 运行时"]
        C2["Workflow 引擎<br/>（.then / .branch / .parallel）"]
        C3["Tool 系统（Zod Schema）"]
        C4["Memory / RAG / Evals"]
    end

    subgraph DEV["开发者工具"]
        D1["mastra dev<br/>（本地 Playground）"]
        D2["Storage<br/>（SQLite / Postgres / Upstash）"]
    end

    subgraph DEPLOY["部署"]
        P1["Vercel / Cloudflare Workers"]
        P2["Node.js Server"]
        P3["Mastra Cloud"]
    end

    APP --> CORE
    CORE --> DEV
    CORE --> DEPLOY

    style APP fill:#e3f2fd,stroke:#1565c0
    style CORE fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style DEV fill:#fff3e0,stroke:#e65100
    style DEPLOY fill:#fce4ec,stroke:#c2185b
````

### 2.2 Workflow 链式 API

````mermaid
graph LR
    Start[input] --> S1[.then step1]
    S1 --> Branch{.branch}
    Branch -->|cond A| S2a[step A]
    Branch -->|cond B| S2b[step B]
    S2a --> Merge[.then merge]
    S2b --> Merge
    Merge --> End[output]

    style Branch fill:#ffe082
````

---

## 3. 核心抽象

| 抽象 | 职责 | 类比 |
|------|------|------|
| **Agent** | LLM + instructions + tools + memory | LangGraph ReAct |
| **Tool** | Zod-typed 函数（`id` + `execute`） | Pydantic AI Tool |
| **Workflow** | 链式步骤编排（支持 suspend/resume） | LangGraph StateGraph |
| **Memory** | Thread + Working Memory | LlamaIndex Context |
| **Evals** | 内建 LLM-as-Judge + 指标 | LangSmith Evaluators |

---

## 4. 代码示例

### 4.1 类型安全的 Agent + Tool

```typescript
import { Agent } from "@mastra/core/agent";
import { createTool } from "@mastra/core/tools";
import { openai } from "@ai-sdk/openai";
import { z } from "zod";

const weatherTool = createTool({
  id: "get-weather",
  description: "Get current weather for a city",
  inputSchema: z.object({ city: z.string() }),
  outputSchema: z.object({ temp: z.number(), condition: z.string() }),
  execute: async ({ context }) => {
    return { temp: 22, condition: "sunny" };
  },
});

export const weatherAgent = new Agent({
  name: "Weather Agent",
  instructions: "You answer weather questions.",
  model: openai("gpt-4o"),
  tools: { weatherTool },
});
```

### 4.2 Workflow 链式编排

```typescript
import { createWorkflow, createStep } from "@mastra/core/workflows";

const fetchStep = createStep({
  id: "fetch",
  inputSchema: z.object({ url: z.string() }),
  outputSchema: z.object({ content: z.string() }),
  execute: async ({ inputData }) => {
    const res = await fetch(inputData.url);
    return { content: await res.text() };
  },
});

const summarizeStep = createStep({ /* ... */ });

export const myWorkflow = createWorkflow({
  id: "fetch-and-summarize",
  inputSchema: z.object({ url: z.string() }),
  outputSchema: z.object({ summary: z.string() }),
})
  .then(fetchStep)
  .then(summarizeStep)
  .commit();
```

---

## 5. 与其他框架对比

| 维度 | Mastra | LangChain.js | Vercel AI SDK | CrewAI |
|------|--------|--------------|----------------|--------|
| 语言 | TS-first | TS 移植 | TS | Python |
| 类型安全 | ⭐⭐⭐⭐⭐（Zod） | ⭐⭐⭐ | ⭐⭐⭐⭐ | - |
| Workflow | ✅ 链式 | ⚠️ LangGraph.js | ❌ | ✅ Flow |
| 本地 UI | ✅ Playground | ❌ | 有限 | ⚠️ Enterprise |
| Evals | ✅ 内建 | ⚠️ LangSmith | ❌ | ❌ |
| 部署 | ✅ Vercel/CF/Cloud | 手动 | ✅ Vercel | 手动 |

---

## 6. 对 Dawning Agent OS 的启示

1. **TS-first 策略的成功证明跨语言 Agent 框架需求真实存在**：Dawning 作为 .NET-first 框架可复制这一路径，突出".NET 生态 Agent"定位
2. **Zod = Pydantic 在 TS 中的对应**：.NET 里可用 `System.ComponentModel.DataAnnotations` + `JsonSchema` 达到相同效果
3. **`mastra dev` 的 DX 启发**：Dawning 应该提供 `dotnet run` 起的本地 Agent Playground（浏览器里可调试 Agent、看消息流、测 Tool）
4. **全栈一体 vs 微内核分层**：Mastra 把"内核 + 工具 + 部署"合一，简化心智；而 OS 哲学坚持分层——这是**架构哲学差异**，Dawning 选择后者但要保证各层**开箱即用**

---

## 7. 延伸阅读

- 官方文档：<https://mastra.ai/>
- GitHub：<https://github.com/mastra-ai/mastra>
- Kyle Mathews 访谈（Latent Space）：<https://www.latent.space/p/mastra>

---

## 交叉引用 <!-- XREF-STUB -->

<!-- TODO 列出 2-5 个最相关的 wiki 页，每个一句话说明为何相关 -->

- [[TODO-相关页面]] — _TODO 为什么相关_

## 来源 <!-- SRC-STUB -->

<!-- TODO 补充原始来源（raw/ 路径或外链） -->
- _TODO_
