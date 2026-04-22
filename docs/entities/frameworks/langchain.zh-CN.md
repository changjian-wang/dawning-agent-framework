---
title: "LangChain 详细分析"
type: framework-entity
tags: [framework, langchain, python, ecosystem, chains]
status: active
created: 2026-04-22
---

# LangChain 详细分析

> LLM 应用生态的**基础设施层**，不是 Agent 框架本身而是构建它的原料库。LangGraph 的底座。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **官方名称** | LangChain |
| **维护者** | LangChain, Inc. |
| **仓库** | https://github.com/langchain-ai/langchain |
| **文档** | https://python.langchain.com/ |
| **语言** | Python（主）、JavaScript/TypeScript |
| **许可证** | MIT |
| **Stars** | 105k+ |
| **最新版本** | v0.3.x |
| **相关产品** | LangGraph（编排）、LangSmith（可观测）、LangServe（部署） |

---

## 1. 定位与背景

LangChain 诞生于 2022 年，是 LLM 应用生态的**奠基之作**。它的真正价值不是 Agent 编排（那是 LangGraph 的职责），而是把"LLM、Embedding、向量库、工具、记忆、Prompt"等所有常用组件封装成**可组合的 Runnable**。

**核心定位**：**LLM 应用的"标准库 + 适配器层"**。

**关键演进**：
- **2022**：Chain 概念（顺序调用）
- **2023**：LCEL（LangChain Expression Language）引入 `|` 管道语法
- **2024**：拆分为 `langchain-core` + `langchain-community` + `partner packages`
- **2025**：Agent 能力迁移到 LangGraph，LangChain 回归"组件库"本位

---

## 2. 架构设计

### 2.1 六大核心模块

````mermaid
graph TB
    subgraph APP["应用层（LangGraph / 用户应用）"]
    end

    subgraph CHAINS["Chains（LCEL）<br/>—— 编排枢纽"]
        CH1["Runnable 接口"]
        CH2["RunnableSequence（| 管道）"]
        CH3["RunnableParallel / Branch"]
    end

    subgraph MODULES["核心组件"]
        M1["Models<br/>（LLM / Chat / Embedding）"]
        M2["Prompts<br/>（模板、Few-Shot）"]
        M3["Output Parsers<br/>（Pydantic / JSON / XML）"]
        M4["Memory<br/>（对话历史、实体）"]
        M5["Retrievers<br/>（向量库、BM25）"]
        M6["Tools<br/>（Function Calling 抽象）"]
    end

    subgraph ECO["生态"]
        E1["langchain-community<br/>（500+ 集成）"]
        E2["partner packages<br/>（openai / anthropic / ...）"]
    end

    APP --> CHAINS
    CHAINS --> MODULES
    MODULES --> ECO

    style CHAINS fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    style MODULES fill:#e8f5e9,stroke:#2e7d32
    style ECO fill:#fff3e0,stroke:#e65100
````

**Chains 是中心枢纽**：所有模块都实现 `Runnable` 接口，通过 LCEL `|` 组合。

### 2.2 LCEL 管道语义

````mermaid
graph LR
    Input[Input] --> Prompt[PromptTemplate]
    Prompt --> Model[ChatModel]
    Model --> Parser[OutputParser]
    Parser --> Output[Output]

    style Prompt fill:#bbdefb
    style Model fill:#c8e6c9
    style Parser fill:#ffe082
````

对应代码：

```python
chain = prompt | model | parser
```

---

## 3. 核心抽象

| 抽象 | 职责 | 类比 Dawning |
|------|------|---------------|
| **Runnable** | 统一调用接口（`.invoke` / `.stream` / `.batch`） | `IAgent` 基类 |
| **ChatModel** | LLM 调用抽象（支持 Function Calling） | `ILLMProvider` |
| **PromptTemplate** | 模板 + 变量替换 | `IPromptTemplate` |
| **OutputParser** | 结构化输出解析 | `IResponseParser` |
| **VectorStore** | 向量库统一接口 | `IVectorStore` |
| **Tool** | 函数封装 + Schema 描述 | `ITool` |

---

## 4. 代码示例

### 4.1 最小 RAG 链

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

vectorstore = Chroma.from_texts(texts, OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

prompt = ChatPromptTemplate.from_template(
    "Context: {context}\n\nQuestion: {question}"
)
model = ChatOpenAI(model="gpt-4o")

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

chain.invoke("What is LCEL?")
```

### 4.2 并行分支

```python
from langchain.schema.runnable import RunnableParallel

chain = RunnableParallel(
    summary=prompt_summary | model | parser,
    translation=prompt_translate | model | parser,
)
chain.invoke({"text": "..."})
```

---

## 5. 与其他框架对比

| 维度 | LangChain | LangGraph | LlamaIndex | Semantic Kernel |
|------|-----------|-----------|------------|----------------|
| 定位 | 组件库 + LCEL | 状态图编排 | RAG 优先 | 企业 SDK |
| 核心抽象 | Runnable | StateGraph | QueryEngine | Kernel + Plugin |
| Agent 能力 | ❌（移交 LangGraph） | ✅ 核心 | 有限 | ✅ |
| 企业就绪 | 中 | 高 | 中 | 高 |
| 生态深度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 6. 对 Dawning Agent OS 的启示

1. **统一 Runnable 接口是生态爆炸的前提**：Dawning 应该让所有组件（Tool / Skill / Agent / Memory）实现一个统一的 `IRunnable` 基类
2. **LCEL 的价值是声明式**：`|` 管道让流程可视、可测试、可序列化——值得借鉴
3. **Split 决策**：LangChain 把 Agent 能力分出给 LangGraph 是正确的——**组件库和编排框架应该分层**
4. **Community + Partner 分层**：`langchain-community` 松散集成、`partner packages` 严格版本绑定，这种"生态分层"策略 Dawning 可学习

---

## 7. 延伸阅读

- 官方文档：<https://python.langchain.com/>
- LCEL 规范：<https://python.langchain.com/docs/concepts/lcel/>
- [comparisons/framework-modules-mapping.zh-CN.md](../../comparisons/framework-modules-mapping.zh-CN.md)
- [langgraph.zh-CN.md](langgraph.zh-CN.md)
