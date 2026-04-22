---
title: "AutoGen 详细分析"
type: framework-entity
tags: [framework, autogen, microsoft, multi-agent, actor-model]
status: maintenance
created: 2026-04-22
---

# AutoGen 详细分析

> Microsoft Research 出品的多 Agent 对话框架，Actor 模型开创者。2025 年 10 月后进入维护模式，由 MAF 继任。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **官方名称** | AutoGen |
| **维护者** | Microsoft Research |
| **仓库** | https://github.com/microsoft/autogen |
| **文档** | https://microsoft.github.io/autogen/ |
| **语言** | Python（主）、.NET（v0.4 引入） |
| **许可证** | CC-BY-4.0 / MIT（代码） |
| **Stars** | 56.8k |
| **最新版本** | v0.4.x（Python）、v0.2.x（.NET） |
| **当前状态** | **维护模式**，新开发迁至 MAF |
| **继任者** | Microsoft Agent Framework（MAF） |

---

## 1. 定位与背景

AutoGen 是微软研究院 2023 年推出的**多 Agent 对话框架**，核心创新是把"Agent 协作"建模为**多方对话**（multi-agent conversation）。v0.4 在 2024 年重写，引入 **Actor 模型**（借鉴 Erlang/Akka），消息总线 + Agent 池，成为后续 MAF 的架构蓝本。

**核心理念**：
- Agent 之间通过**异步消息**通信（不是函数调用）
- 每个 Agent 是独立 Actor（有邮箱、有状态）
- 通过 **GroupChat** 编排多 Agent 协作

**历史定位**：启蒙了整个"多 Agent 协作"赛道，CrewAI、MAF、LangGraph Supervisor 都受其影响。

---

## 2. 架构设计

### 2.1 v0.4 三层架构

````mermaid
graph TB
    subgraph APP["应用层 AgentChat"]
        AC1["AssistantAgent"]
        AC2["UserProxyAgent"]
        AC3["GroupChat / Swarm / Magentic"]
    end

    subgraph CORE["核心层 Core"]
        CORE1["Agent（Actor 抽象）"]
        CORE2["Runtime（消息分发）"]
        CORE3["Tool / Memory / Model"]
    end

    subgraph EXT["扩展层 Extensions"]
        EXT1["OpenAI / Azure / Anthropic"]
        EXT2["Docker / Playwright / FileSurfer"]
        EXT3["LangChain Tools Adapter"]
    end

    APP --> CORE
    CORE --> EXT

    style APP fill:#e3f2fd,stroke:#1565c0
    style CORE fill:#e8f5e9,stroke:#2e7d32
    style EXT fill:#fff3e0,stroke:#e65100
````

### 2.2 Actor 模型消息流

````mermaid
sequenceDiagram
    participant U as User
    participant R as Runtime
    participant A1 as Agent A
    participant A2 as Agent B

    U->>R: send(message, recipient=A1)
    R->>A1: deliver(message)
    A1->>A1: on_messages() 处理
    A1->>R: publish(response, to=A2)
    R->>A2: deliver(response)
    A2->>A2: on_messages() 处理
    A2-->>R: publish(result)
    R-->>U: stream(result)
````

---

## 3. 核心抽象

| 抽象 | 职责 | 对应 MAF 概念 |
|------|------|---------------|
| **Agent** | Actor，有 `on_messages()` 生命周期 | `AIAgent` |
| **Runtime** | 消息分发 + Agent 注册 | `AgentRuntime` |
| **GroupChat** | 多 Agent 对话编排 | `Workflow` |
| **Selector** | 下一个发言者选择器 | `Orchestrator` |
| **Memory** | 对话记忆 + 向量检索 | `AgentThread` |

---

## 4. 代码示例

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

model = OpenAIChatCompletionClient(model="gpt-4o")

researcher = AssistantAgent(
    name="researcher",
    model_client=model,
    system_message="You research topics deeply.",
)
writer = AssistantAgent(
    name="writer",
    model_client=model,
    system_message="You write clearly.",
)

team = RoundRobinGroupChat([researcher, writer], max_turns=4)
await team.run(task="Write a summary of quantum computing.")
```

---

## 5. 与其他框架对比

| 维度 | AutoGen | MAF | LangGraph | CrewAI |
|------|---------|-----|-----------|--------|
| 编排模型 | 多方对话 | Workflow DAG | Graph + Pregel | Process（Sequential/Hierarchical） |
| Actor 模型 | ✅ 核心 | ✅ 继承 | ❌ | ❌ |
| 消息语义 | 异步 pub/sub | 异步 pub/sub | 同步 step | 同步顺序 |
| 持久化 | 有限 | Durable Agent | Checkpointer | Memory |
| 当前状态 | 维护 | 主推 | 活跃 | 活跃 |

---

## 6. 对 Dawning Agent OS 的启示

1. **消息总线即内核**：Actor 模型天然适合"Agent OS 进程间通信"，Dawning IPC 层可直接借鉴
2. **Selector = 调度器**：`GroupChat.selector_func` 本质是一个调度策略，对应 Dawning Orchestrator
3. **维护模式的教训**：v0.2 → v0.4 破坏性重写导致用户流失，提醒我们**稳定 API 比创新更重要**
4. **统一 Runtime**：Agent 不持有 Runtime 引用、由 Runtime 反向调度，这是解耦关键

---

## 7. 延伸阅读

- 官方文档：<https://microsoft.github.io/autogen/>
- v0.2 → v0.4 迁移指南：<https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/migration-guide.html>
- 论文《AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation》
- 本库相关：[microsoft-agent-framework.zh-CN.md](microsoft-agent-framework.zh-CN.md)
