---
title: "Pydantic AI 详细分析"
type: entity
tags: [framework, pydantic-ai, python, type-safe, structured]
status: active
created: 2026-04-22
subtype: framework
sources: []
updated: 2026-04-22
---

# Pydantic AI 详细分析

> 由 Pydantic 团队出品，把**类型安全**推到极致的 Agent 框架。FastAPI 在 LLM 领域的对应物。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **官方名称** | Pydantic AI |
| **维护者** | Pydantic Services（Samuel Colvin 团队） |
| **仓库** | https://github.com/pydantic/pydantic-ai |
| **文档** | https://ai.pydantic.dev/ |
| **语言** | Python |
| **许可证** | MIT |
| **Stars** | 7k+ |
| **最新版本** | v0.0.x → v0.x（快速演进） |
| **核心差异化** | 全链路类型安全 + 依赖注入 |

---

## 1. 定位与背景

Pydantic AI 2024 年发布，目标很直白：**把 FastAPI 的成功公式搬到 Agent 赛道**。

- FastAPI = Starlette + Pydantic → 类型安全 Web 框架
- Pydantic AI = LLM + Pydantic → 类型安全 Agent 框架

**核心理念**：
- **一切皆类型**：Prompt 入参、Tool 签名、Output 结构都用 Pydantic 模型定义
- **依赖注入**：Agent 接受 `deps_type`，工具通过 `RunContext[Deps]` 访问依赖（类似 FastAPI 的 `Depends`）
- **模型无关**：统一封装 OpenAI / Anthropic / Gemini / Ollama / Groq 等 10+ 提供商

**关键差异**：不是重新发明编排——而是给现有 LLM 调用**套上强类型外壳**。

---

## 2. 架构设计

### 2.1 类型驱动的 Agent

````mermaid
graph TB
    subgraph APP["应用代码（完全类型安全）"]
        A1["@agent.tool 装饰器"]
        A2["output_type=MyModel"]
        A3["deps_type=MyDeps"]
    end

    subgraph CORE["Pydantic AI 核心"]
        C1["Agent[Deps, Out]"]
        C2["RunContext[Deps]"]
        C3["Tool 注册 + Schema 生成"]
        C4["结构化输出解析"]
    end

    subgraph MODELS["Model 抽象层"]
        M1["OpenAIModel"]
        M2["AnthropicModel"]
        M3["GeminiModel"]
        M4["TestModel（单测）"]
    end

    APP --> CORE
    CORE --> MODELS

    style APP fill:#e3f2fd,stroke:#1565c0
    style CORE fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style MODELS fill:#fff3e0,stroke:#e65100
````

### 2.2 依赖注入类比 FastAPI

| FastAPI | Pydantic AI |
|---------|-------------|
| `Depends(get_db)` | `RunContext[Deps]` |
| `response_model=X` | `output_type=X` |
| `BackgroundTasks` | `message_history` |
| `TestClient` | `TestModel` / `FunctionModel` |

---

## 3. 核心抽象

| 抽象 | 职责 |
|------|------|
| **Agent[Deps, Out]** | 泛型 Agent，绑定依赖类型和输出类型 |
| **RunContext[Deps]** | 工具访问依赖的上下文 |
| **@agent.tool** | 注册工具（自动生成 Schema） |
| **@agent.system_prompt** | 动态系统提示 |
| **Model** | LLM 提供商抽象 |
| **Result** | 带使用量统计的结构化输出 |

---

## 4. 代码示例

### 4.1 类型安全的查询 Agent

```python
from dataclasses import dataclass
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

@dataclass
class Deps:
    db: Database
    api_key: str

class Invoice(BaseModel):
    number: str
    amount: float
    customer: str

agent = Agent(
    "openai:gpt-4o",
    deps_type=Deps,
    output_type=Invoice,
    system_prompt="You extract invoice data.",
)

@agent.tool
async def lookup_customer(ctx: RunContext[Deps], name: str) -> str:
    """Look up customer details from database."""
    return await ctx.deps.db.query(name)

result = await agent.run("Parse this: ACME invoice #123 for $500.00", deps=deps)
print(result.output.amount)  # 类型：float，IDE 完全补全
```

### 4.2 测试友好

```python
from pydantic_ai.models.test import TestModel

agent = Agent(TestModel(), output_type=Invoice)
# 无需真实 LLM，自动生成符合 schema 的假数据
```

---

## 5. 与其他框架对比

| 维度 | Pydantic AI | LangChain | CrewAI | OpenAI Agents SDK |
|------|------------|-----------|--------|--------------------|
| 类型安全 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| 依赖注入 | ✅ 核心 | ❌ | ❌ | ❌ |
| 多模型支持 | ✅ 10+ | ✅ 全部 | ✅ LiteLLM | 主要 OpenAI |
| 多 Agent 编排 | 有限 | LangGraph | ✅ | ✅ Handoff |
| 学习曲线 | 低（FastAPI 用户） | 陡峭 | 中 | 低 |

---

## 6. 对 Dawning Agent OS 的启示

1. **FastAPI 隐喻**：Dawning 是 .NET，ASP.NET Core 的 DI + 模型绑定本就是 Agent 框架的绝佳底座——Pydantic AI 验证了这条路
2. **泛型 Agent**：`IAgent<TDeps, TOutput>` 应该是 Dawning 的一等抽象
3. **TestModel 模式**：在 `ILLMProvider` 之外再加一个 `TestLLMProvider`（脚本化响应），让单测不依赖真实 LLM
4. **Schema = Prompt**：Pydantic 模型直接作为 LLM 的结构化输出契约，这种"类型即提示"的做法在 C# 里可用 `System.Text.Json.Schema` 实现

---

## 7. 延伸阅读

- 官方文档：<https://ai.pydantic.dev/>
- GitHub：<https://github.com/pydantic/pydantic-ai>
- Samuel Colvin 访谈（Latent Space）：<https://www.latent.space/p/pydantic>

---

## 交叉引用 <!-- XREF-STUB -->

<!-- TODO 列出 2-5 个最相关的 wiki 页，每个一句话说明为何相关 -->

- [[TODO-相关页面]] — _TODO 为什么相关_

## 来源 <!-- SRC-STUB -->

<!-- TODO 补充原始来源（raw/ 路径或外链） -->
- _TODO_
