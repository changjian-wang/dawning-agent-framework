---
title: "LlamaIndex Workflows 详细分析"
type: framework-entity
tags: [framework, llamaindex, workflow, event-driven, rag]
status: active
created: 2026-04-22
---

# LlamaIndex Workflows 详细分析

> RAG 领域的王者扩展到 Agent 赛道，**事件驱动工作流** + 深度数据索引的组合。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **官方名称** | LlamaIndex（含 Workflows） |
| **维护者** | LlamaIndex, Inc. |
| **仓库** | https://github.com/run-llama/llama_index |
| **文档** | https://docs.llamaindex.ai/ |
| **语言** | Python（主）、TypeScript |
| **许可证** | MIT |
| **Stars** | 40k+ |
| **最新版本** | v1.x |
| **核心差异化** | RAG 深度 + 200+ Reader + Event-Driven Workflow |

---

## 1. 定位与背景

LlamaIndex 2023 年以"LLM + 数据"为核心定位诞生，前身是 `GPT-Index`。它与 LangChain 的分工最清晰：

- **LangChain** 关心"怎么把模块串起来"
- **LlamaIndex** 关心"怎么把数据喂给 LLM"

2024 年引入 **Workflows**（事件驱动工作流）后，正式进入 Agent 编排赛道。Workflow 的核心隐喻是 **Event Bus**：Agent 节点订阅事件、发布事件，而不是显式定义边。

**核心理念**：
- 数据是主角，Agent 是数据的消费者
- 工作流 = 事件订阅 + 事件发布
- Step = 一个处理器（对某类 Event 的 handler）

---

## 2. 架构设计

### 2.1 双层架构：RAG 基座 + Workflow 编排

````mermaid
graph TB
    subgraph WF["Workflow 层（编排）"]
        W1["@step 处理器"]
        W2["Event Bus"]
        W3["Context（共享状态）"]
    end

    subgraph RAG["RAG 基座"]
        R1["Reader<br/>（PDF/Notion/Slack/...）<br/>200+"]
        R2["Node Parser<br/>（Sentence / Window / Tree）"]
        R3["Index<br/>（Vector / Tree / Keyword / KG）"]
        R4["QueryEngine<br/>（Retriever + Synthesizer）"]
    end

    subgraph AGENT["Agent 层"]
        A1["FunctionCallingAgent"]
        A2["ReActAgent"]
        A3["Tool（含 QueryEngineTool）"]
    end

    WF --> AGENT
    AGENT --> RAG
    WF --> RAG

    style WF fill:#e3f2fd,stroke:#1565c0
    style RAG fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style AGENT fill:#fff3e0,stroke:#e65100
````

**关键洞察**：RAG 是 LlamaIndex 的根基，Workflow 和 Agent 都是 RAG 的延伸。

### 2.2 Event-Driven 工作流

````mermaid
graph LR
    Start[StartEvent] --> S1[Step 1]
    S1 -->|emit QueryEvent| S2[Step 2: retrieve]
    S2 -->|emit RetrieveDoneEvent| S3[Step 3: synthesize]
    S3 -->|emit StopEvent| End[End]

    S1 -.->|可选| S4[Step 4: fallback]
    S4 -->|emit QueryEvent| S2

    style Start fill:#bbdefb
    style End fill:#ffccbc
````

与 LangGraph 显式定义边不同，LlamaIndex Workflow **靠事件类型自动连接**。

---

## 3. 核心抽象

| 抽象 | 职责 | 类比 |
|------|------|------|
| **Workflow** | 事件驱动的 Agent 容器 | LangGraph `StateGraph` |
| **Event** | 步骤间消息（Pydantic 类型） | LangGraph 消息 |
| **@step** | 事件处理器（按入参类型自动订阅） | LangGraph `node` |
| **Context** | 共享状态 + 事件存储 | LangGraph `state` |
| **QueryEngine** | RAG 查询的统一封装 | 独有 |
| **Node** | 带元数据的文本块（RAG 原子） | 独有 |

---

## 4. 代码示例

### 4.1 事件驱动 Workflow

```python
from llama_index.core.workflow import (
    Workflow, Event, StartEvent, StopEvent, step, Context
)

class QueryEvent(Event):
    query: str

class ResultEvent(Event):
    result: str

class MyWorkflow(Workflow):
    @step
    async def translate(self, ev: StartEvent) -> QueryEvent:
        return QueryEvent(query=ev.input)

    @step
    async def search(self, ctx: Context, ev: QueryEvent) -> ResultEvent:
        result = await ctx.data["index"].aquery(ev.query)
        return ResultEvent(result=str(result))

    @step
    async def finalize(self, ev: ResultEvent) -> StopEvent:
        return StopEvent(result=ev.result)

flow = MyWorkflow(timeout=60)
answer = await flow.run(input="What is LlamaIndex?")
```

### 4.2 RAG + Agent

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.agent import FunctionCallingAgent
from llama_index.core.tools import QueryEngineTool

docs = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(docs)
tool = QueryEngineTool.from_defaults(
    query_engine=index.as_query_engine(),
    name="knowledge_base",
    description="Company docs.",
)

agent = FunctionCallingAgent.from_tools([tool], verbose=True)
agent.chat("How do I reset my password?")
```

---

## 5. 与其他框架对比

| 维度 | LlamaIndex | LangChain/LangGraph | LangGraph 独有 |
|------|-----------|--------------------|---------------------|
| RAG 深度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Reader 数量 | 200+ | ~150 | - |
| Index 类型 | Vector/Tree/KG/Keyword | Vector 主 | - |
| 编排模型 | Event-Driven | LCEL / StateGraph | Pregel 超步 |
| 显式边 | ❌（隐式事件订阅） | ✅ | ✅ |
| HITL | 基础 | ✅ Interrupt | ✅ Interrupt |

---

## 6. 对 Dawning Agent OS 的启示

1. **Event-Driven vs Graph-Driven**：两种编排模型各有优劣——事件驱动更松耦合，图驱动更可推理。Dawning 可以**同时支持两种心智**
2. **RAG 作为一等公民**：不要把 RAG 当成一个"工具"，而应设计为**内存子系统**（参考 [concepts/context-management.md](../../concepts/context-management.md)）
3. **按类型订阅**：`@step` 根据入参类型自动路由，这种"类型即契约"的模式比显式定义边更符合 .NET 强类型语义
4. **Reader 生态**：数据源插件化（类比 Linux VFS）是 OS 隐喻的强化

---

## 7. 延伸阅读

- 官方文档：<https://docs.llamaindex.ai/>
- Workflows 指南：<https://docs.llamaindex.ai/en/stable/module_guides/workflow/>
- [comparisons/rag-pipeline-comparison.zh-CN.md](../../comparisons/rag-pipeline-comparison.zh-CN.md)
