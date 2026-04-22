---
title: "Agno 详细分析"
type: framework-entity
tags: [framework, agno, python, performance, memory]
status: active
created: 2026-04-22
---

# Agno 详细分析

> 前身 Phidata，2025 年改名 Agno。主打**极致性能**（~3μs Agent 实例化）+ 统一多模态 + 内建记忆。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **官方名称** | Agno |
| **前身** | Phidata |
| **维护者** | Agno Inc. |
| **仓库** | https://github.com/agno-agi/agno |
| **文档** | https://docs.agno.com/ |
| **语言** | Python |
| **许可证** | MPL 2.0 |
| **Stars** | 17k+ |
| **核心差异化** | 3μs 实例化 / 6.5KiB 内存 / 原生多模态 |

---

## 1. 定位与背景

Agno（前身 Phidata）是 2024 年后期快速崛起的 Python Agent 框架。团队主张：**Agent 框架不应成为性能瓶颈**。他们公布的基准（vs LangGraph、CrewAI）显示：

| 指标 | Agno | LangGraph | CrewAI |
|------|------|-----------|--------|
| Agent 实例化 | ~3μs | ~20ms | ~50ms |
| 内存占用 | ~6.5KiB | ~500KiB | ~1MiB |

**核心理念**：
- **5 层能力**：Model → Tools → Memory → Knowledge → Reasoning（逐层叠加）
- **多模态一等公民**：Text / Image / Audio / Video 作为输入输出统一类型
- **内建 Agent UI**：自带 Playground（对标 LangGraph Studio）

---

## 2. 架构设计

### 2.1 5 层 Agent 能力

````mermaid
graph TB
    L5["Layer 5: Reasoning<br/>（CoT / ReAct / Reflection）"]
    L4["Layer 4: Knowledge<br/>（向量库 / 文档 / URL）"]
    L3["Layer 3: Memory<br/>（SessionMemory / UserMemory）"]
    L2["Layer 2: Tools<br/>（Function Calling）"]
    L1["Layer 1: Model<br/>（LLM 调用）"]

    L1 --> L2 --> L3 --> L4 --> L5

    style L1 fill:#e1f5fe
    style L2 fill:#c8e6c9
    style L3 fill:#fff9c4
    style L4 fill:#ffe0b2
    style L5 fill:#f8bbd0
````

**关键设计**：每层可单独启用/禁用，Agent 不需要为不用的能力付代价（这是性能的秘密）。

### 2.2 多模态统一类型

````mermaid
graph LR
    subgraph IN["Input 统一类型"]
        I1["Text"]
        I2["Image (URL/bytes)"]
        I3["Audio (URL/bytes)"]
        I4["Video (URL/bytes)"]
    end

    A[Agent]

    subgraph OUT["Output"]
        O1["RunResponse<br/>（含 messages + metrics）"]
    end

    IN --> A
    A --> OUT

    style IN fill:#e3f2fd
    style A fill:#e8f5e9
    style OUT fill:#fff3e0
````

---

## 3. 核心抽象

| 抽象 | 职责 |
|------|------|
| **Agent** | 主入口，承载 5 层能力 |
| **Team** | Agent 协作容器（Route / Coordinate / Collaborate 三种模式） |
| **Workflow** | 代码化流程（纯 Python 函数组合 Agent） |
| **Memory** | Session + User 双层记忆 |
| **Knowledge** | 向量化知识库（内建 LanceDB / PgVector） |
| **Model** | 25+ LLM 提供商适配 |

---

## 4. 代码示例

### 4.1 5 层能力的 Agent

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.url import UrlKnowledge
from agno.vectordb.lancedb import LanceDb
from agno.memory.v2 import Memory

knowledge = UrlKnowledge(
    urls=["https://docs.agno.com/"],
    vector_db=LanceDb(uri="tmp/lancedb"),
)
knowledge.load()

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    memory=Memory(),
    knowledge=knowledge,
    reasoning=True,  # 开启 CoT
    markdown=True,
)

agent.print_response("Explain how Agno compares to LangGraph.")
```

### 4.2 多 Agent Team

```python
from agno.team import Team

researcher = Agent(name="researcher", tools=[...])
writer = Agent(name="writer", tools=[...])

team = Team(
    mode="coordinate",  # 或 route / collaborate
    members=[researcher, writer],
    model=OpenAIChat(id="gpt-4o"),
)
team.print_response("Write a blog post about Agno.")
```

---

## 5. 与其他框架对比

| 维度 | Agno | CrewAI | LangGraph | Pydantic AI |
|------|------|--------|-----------|-------------|
| 实例化速度 | ⭐⭐⭐⭐⭐ 3μs | 中 | 中 | 快 |
| 多模态 | ✅ 原生 | 有限 | 通过工具 | 基础 |
| 内建 UI | ✅ Playground | ❌（需 Enterprise） | ✅ Studio | ❌ |
| 记忆系统 | ✅ v2（结构化） | ✅ | 通过 checkpointer | 有限 |
| 知识库 | ✅ 内建 | ⚠️ 外挂 | ⚠️ 外挂 | ⚠️ 外挂 |
| 多 Agent | Team | ✅ Crew | ✅ | 有限 |

---

## 6. 对 Dawning Agent OS 的启示

1. **性能即功能**：μs 级实例化 → 对 Serverless / FaaS 场景非常关键。Dawning 应该公布类似基准（对标 Agno）
2. **能力分层**：5 层模型（Model / Tools / Memory / Knowledge / Reasoning）清晰——但 OS 视角下应该是 **7 层**（加入 IPC 和 Security），Dawning 已经这样做
3. **按需启用**：不用某层就不为它付代价——对应 Dawning 的"按需注入"哲学（`AddMemory()` 可选）
4. **多模态统一类型**：.NET 可用 `IAgentMessage` 基类 + `TextContent / ImageContent / AudioContent` 变体统一建模

---

## 7. 延伸阅读

- 官方文档：<https://docs.agno.com/>
- 性能基准：<https://docs.agno.com/introduction/agents#performance>
- GitHub：<https://github.com/agno-agi/agno>
