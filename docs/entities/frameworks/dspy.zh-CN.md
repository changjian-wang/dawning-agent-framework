---
title: "DSPy 详细分析"
type: framework-entity
tags: [framework, dspy, stanford, declarative, optimization, prompt-engineering]
status: active
created: 2026-04-22
---

# DSPy 详细分析

> Stanford 出品的**声明式 Prompt 编程**框架。不写 Prompt，写 Signature；不调 Prompt，跑 Optimizer。

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **官方名称** | DSPy |
| **维护者** | Stanford NLP（Omar Khattab 团队） |
| **仓库** | https://github.com/stanfordnlp/dspy |
| **文档** | https://dspy.ai/ |
| **语言** | Python |
| **许可证** | MIT |
| **Stars** | 20k+ |
| **最新版本** | v2.5+ |
| **核心差异化** | Prompt-as-Code → Prompt-as-Program（可编译、可优化） |

---

## 1. 定位与背景

DSPy 源自 Stanford 的 DSP（Demonstrate-Search-Predict）论文（2023），之后重写为编译器化框架。**核心主张**：

> "手写 Prompt 是 LLM 时代的汇编。DSPy 是高级语言 + 编译器。"

**三层抽象**：
1. **Signature**：声明输入/输出（不是 Prompt 字符串！）
2. **Module**：组合 Signature 的计算单元（`Predict` / `ChainOfThought` / `ReAct`）
3. **Optimizer** (Teleprompter)：用训练数据自动**优化 Prompt + Demonstrations + 权重**

**与传统框架的根本差异**：
- LangChain / LlamaIndex：提供 API 让你**写 Prompt**
- DSPy：提供编译器让你**不写 Prompt**，由优化器学出来

---

## 2. 架构设计

### 2.1 编译器范式

````mermaid
graph TB
    subgraph SRC["源码层（用户写）"]
        S1["Signature<br/>（输入输出类型）"]
        S2["Module 组合"]
        S3["Metric<br/>（评估函数）"]
        S4["Trainset<br/>（少量样例）"]
    end

    subgraph OPT["编译器层（DSPy 内核）"]
        O1["Teleprompter / Optimizer"]
        O2["BootstrapFewShot"]
        O3["MIPRO v2"]
        O4["COPRO（Prompt 重写）"]
    end

    subgraph OUT["编译产物"]
        P1["优化后的 Prompt"]
        P2["挑选的 Few-Shot 示例"]
        P3["（可选）Fine-tuned 权重"]
    end

    SRC --> OPT
    OPT --> OUT

    style SRC fill:#e3f2fd,stroke:#1565c0
    style OPT fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style OUT fill:#fff3e0,stroke:#e65100
````

### 2.2 Signature = 函数签名

```python
# 传统 Prompt（硬编码）
prompt = "Given context: {ctx}\nAnswer question: {q}\nAnswer:"

# DSPy Signature（声明式）
class QA(dspy.Signature):
    """Answer questions based on context."""
    context: str = dspy.InputField()
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()
```

编译器会从 Signature **自动生成** Prompt 模板、Few-Shot 示例、Parser。

---

## 3. 核心抽象

| 抽象 | 职责 | 类比编程语言 |
|------|------|-------------|
| **Signature** | 输入/输出声明 | 函数签名 |
| **Module** | 计算单元（`forward` 方法） | 类 / 函数 |
| **Predict** | 基础推理 Module | `call` 指令 |
| **ChainOfThought** | 带思考链的 Predict | 宏展开 |
| **ReAct** | 工具调用 Module | 库调用 |
| **Optimizer** | 编译器 | `gcc -O2` |
| **Metric** | 评估函数 | 编译目标 |

---

## 4. 代码示例

### 4.1 RAG + 自动优化

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

class RAG(dspy.Module):
    def __init__(self, retriever):
        self.retriever = retriever
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        ctx = self.retriever(question, k=3)
        return self.generate(context=ctx, question=question)

# 定义评估指标
def accuracy(gold, pred, trace=None):
    return gold.answer.lower() in pred.answer.lower()

# 自动优化：DSPy 会生成最优 Prompt + Few-Shot
teleprompter = dspy.BootstrapFewShot(metric=accuracy)
optimized_rag = teleprompter.compile(RAG(retriever), trainset=trainset)

# 使用
result = optimized_rag(question="What is DSPy?")
```

### 4.2 Prompt 重写优化

```python
# COPRO 会用 LLM 重写指令本身
copro = dspy.COPRO(metric=accuracy)
better = copro.compile(RAG(retriever), trainset=trainset)
```

---

## 5. 与其他框架对比

| 维度 | DSPy | LangChain | LlamaIndex | Pydantic AI |
|------|------|-----------|------------|-------------|
| Prompt 编写 | ❌ 声明式 | ✅ 显式 | ✅ 显式 | ✅ 显式 |
| 优化器 | ✅ 内建 | ❌ | ❌ | ❌ |
| 评估驱动 | ✅ 核心 | ⚠️ LangSmith | ⚠️ | ❌ |
| 学习曲线 | 陡峭（新范式） | 中 | 中 | 低 |
| 适用场景 | 研究、高精度、RAG | 生产、通用 | RAG 专精 | 类型安全生产 |

---

## 6. 对 Dawning Agent OS 的启示

1. **编译器隐喻**：DSPy 提示我们，Prompt 工程可以像"编译"一样自动化。Dawning 可实验 **PromptCompiler** 子系统（Signature → Optimized Prompt）
2. **Signature 作为 Skill 契约**：Dawning Skill 已经有输入输出声明，天然可用 DSPy 式优化器——这是差异化点
3. **Metric 驱动的演进**：Skill Evolution（之前 RFC 中提到）可以用 DSPy 的评估→优化循环作为理论基础
4. **编译后可部署**：DSPy 的优化结果是**纯 Prompt**，不依赖 DSPy 运行时——类似 AOT 编译，部署时零开销

---

## 7. 延伸阅读

- 官方文档：<https://dspy.ai/>
- 论文《DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines》
- [concepts/prompt-engineering-dspy.zh-CN.md](../../concepts/prompt-engineering-dspy.zh-CN.md)
