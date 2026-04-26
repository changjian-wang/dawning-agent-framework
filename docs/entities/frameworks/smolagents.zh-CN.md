---
title: "smolagents 详细分析"
type: entity
tags: [framework, smolagents, huggingface, code-agent, minimal]
status: active
created: 2026-04-22
subtype: framework
sources: []
updated: 2026-04-22
---

# smolagents 详细分析

> HuggingFace 出品的极简 Agent 框架，**代码即工具调用**（Code Agent）。千行代码的哲学实验。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **官方名称** | smolagents |
| **维护者** | Hugging Face |
| **仓库** | https://github.com/huggingface/smolagents |
| **文档** | https://huggingface.co/docs/smolagents |
| **语言** | Python |
| **许可证** | Apache 2.0 |
| **Stars** | 14k+ |
| **核心代码量** | ~1000 行（故意保持小） |
| **核心差异化** | Code Agent 范式（LLM 写代码调工具） |

---

## 1. 定位与背景

smolagents 2025 年初发布，HuggingFace 团队吸收了 Transformers Agents 和 HF Agents 的经验后从头重写。**核心主张**：

> "工具调用的最好表达方式不是 JSON，而是代码。"

**Code Agent 范式**：
- 传统 Function Calling：LLM 返回 `{"name": "search", "args": {"q": "cat"}}`
- smolagents Code Agent：LLM 返回 `result = search("cat"); answer = f"found: {result}"`

在沙箱里执行这段代码，工具就被"调用"了。优势：
- **组合性**：一步里可以调多个工具 + 算术 + 条件判断
- **表达力**：列表推导式、循环、错误处理都天然支持
- **Token 效率**：一段代码 ≈ 多轮 Function Calling

---

## 2. 架构设计

### 2.1 极简三层

````mermaid
graph TB
    subgraph USER["用户代码"]
        U1["CodeAgent / ToolCallingAgent"]
        U2["@tool 装饰的函数"]
    end

    subgraph CORE["smolagents 内核（~1000 LOC）"]
        C1["Agent 循环<br/>（Think → Code → Execute）"]
        C2["Code Executor<br/>（LocalPythonInterpreter / E2B / Docker）"]
        C3["Tool 抽象"]
        C4["Memory（messages）"]
    end

    subgraph MODELS["Model 适配"]
        M1["HfApiModel"]
        M2["LiteLLMModel"]
        M3["TransformersModel（本地推理）"]
        M4["OpenAIServerModel"]
    end

    USER --> CORE
    CORE --> MODELS

    style CORE fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style USER fill:#e3f2fd,stroke:#1565c0
    style MODELS fill:#fff3e0,stroke:#e65100
````

### 2.2 Code Agent 运行循环

````mermaid
sequenceDiagram
    participant U as User
    participant A as CodeAgent
    participant L as LLM
    participant S as Sandbox

    U->>A: run("Find cat videos")
    loop max_steps
        A->>L: messages + tools schema
        L-->>A: Thought + Python code
        A->>S: execute(code)
        S-->>A: stdout / return value / error
        A->>A: observation → messages
        alt final_answer() called
            A-->>U: return result
        end
    end
````

---

## 3. 核心抽象

| 抽象 | 职责 |
|------|------|
| **CodeAgent** | 让 LLM 写 Python 调用工具 |
| **ToolCallingAgent** | 传统 JSON Function Calling 模式 |
| **MultiStepAgent** | 两者的共同基类 |
| **@tool** | 工具注册装饰器 |
| **Model** | LLM 适配层（支持 HF、OpenAI、LiteLLM） |
| **CodeExecutor** | 沙箱（本地 / E2B / Docker） |

---

## 4. 代码示例

### 4.1 Code Agent 搜索

```python
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct"),
)

agent.run("How many seconds in 1.5 hours? Then multiply by the latest SpaceX launch altitude in km.")
# LLM 会生成类似：
# seconds = 1.5 * 3600
# altitude = search("latest SpaceX launch altitude km")
# final_answer(seconds * altitude)
```

### 4.2 自定义工具

```python
from smolagents import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city.
    Args:
        city: City name, e.g. "Paris"
    """
    return f"Weather in {city}: sunny 22°C"

agent = CodeAgent(tools=[get_weather], model=model)
agent.run("Compare weather in Paris and Tokyo")
```

---

## 5. 与其他框架对比

| 维度 | smolagents | CrewAI | LangGraph | OpenAI Agents SDK |
|------|-----------|--------|-----------|--------------------|
| 代码量 | ~1k LOC | ~30k LOC | ~20k LOC | ~5k LOC |
| Code Agent | ✅ 核心 | ❌ | ❌ | ❌ |
| 多 Agent | 基础（子 Agent） | ✅ | ✅ | ✅ |
| 沙箱执行 | ✅ E2B/Docker | ⚠️ | ⚠️ | ⚠️ |
| 学习曲线 | 极低 | 中 | 高 | 低 |
| Token 效率 | ✅ 最高 | 中 | 中 | 中 |

---

## 6. 对 Dawning Agent OS 的启示

1. **Code Agent 范式值得一级支持**：在 .NET 里可用 **C# Scripting** (Microsoft.CodeAnalysis.Scripting) 实现 Code Agent，沙箱用 AssemblyLoadContext
2. **小即是美**：~1000 行证明 Agent 框架的核心本就简单。Dawning 内核应坚持**微内核**原则（本就是 OS 哲学）
3. **Executor 作为一等抽象**：把"如何执行 Action"抽象出来（Function Call / Code / DSL），用户可替换——类似 Linux 的 `exec` 系统调用
4. **沙箱分层**：LocalInterpreter（内部受信） → E2B / Docker（外部工具）——Dawning 需要同样的**权限分级机制**

---

## 7. 延伸阅读

- 官方文档：<https://huggingface.co/docs/smolagents>
- Code Agent 论文《Executable Code Actions Elicit Better LLM Agents》
- 博客：<https://huggingface.co/blog/smolagents>
