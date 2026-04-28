---
title: ADR-003 长期记忆是核心能力
type: adr
subtype: product
canonical: true
summary: 将长期记忆定义为 AI 管家形态的核心能力，自研重点放在记忆模型、用户画像语义、可解释与可控策略，而不是底层存储基础设施。
tags: [agent, memory, memory-design, product-philosophy]
sources: []
created: 2026-04-28
updated: 2026-04-28
verified_at: 2026-04-28
freshness: volatile
status: active
archived_reason: ""
supersedes: []
related: [pages/adrs/memory-privacy-and-user-control.md, pages/adrs/explicit-memory-ledger-mvp.md]
part_of: [pages/hubs/agent-os.md]
adr_status: accepted
adr_date: 2026-04-28
adr_revisit_when: dogfood 中 Memory 没有减少重复表达成本、记忆误用损害信任、或 Memory 模块被副场景复用 ≥ 2 次需要抽象边界时。
---

# ADR-003 长期记忆是核心能力

> 将长期记忆定义为 AI 管家形态的核心能力，自研重点放在记忆模型、用户画像语义、可解释与可控策略，而不是底层存储基础设施。

## 背景

AI 管家的价值来自「他了解你」。如果每次对话都从零开始，user 仍然需要反复解释项目上下文、分类偏好、表达习惯、常见约束和曾经纠正过的错误。那不是管家，只是响应速度更快的前台。

同时，长期记忆也是最高风险能力之一。记忆越强，越需要可解释、可查看、可编辑、可删除；否则它会从服务 user 变成操控 user。

## 备选方案

- 方案 A：不做长期记忆，只依赖当前会话上下文。
- 方案 B：长期记忆是核心能力，但自研重点放在记忆模型与控制策略，底层存储 / 检索 / embedding 可复用成熟组件。
- 方案 C：从第一版开始全栈自研记忆系统，包括存储、embedding、向量检索与同步。

## 被否决方案与理由

**方案 A 不做长期记忆**：

- 产品会退化成普通聊天工具。
- 无法验证「选择题优先」是否能随 user 记忆积累而变好。

**方案 C 全栈自研**：

- 会在 MVP 阶段过早投入基础设施，拖慢信息整理闭环。
- 底层存储、检索、embedding 已有成熟组件，真正差异化不在这里。

## 决策

采用方案 B：长期记忆是核心能力，但自研重点放在产品语义层。

具体规则：

- 长期记忆不是可选模块，而是 AI 管家形态的核心地基。
- 自研重点是记忆模型、用户画像语义、可解释策略、可控策略、误用防护。
- 底层存储、检索、embedding、索引等基础设施可以复用成熟组件。
- 记忆必须服务于侍奉，不用于行为操控、内容推送、消费引导或注意力塑造。
- 记忆必须与 ADR-007 的隐私边界兼容：关键记忆可查看、可编辑、可删除；推断性记忆必须标注。
- MVP 的第一版实现采用 ADR-011 的显式 Memory Ledger；向量 / embedding 检索后置。

## 影响

**正向影响**：

- 明确产品差异化来自长期理解 user，而不是单轮回答质量。
- 防止团队在底层基础设施上过早自研。
- 为信息整理 MVP 提供可验证目标：新任务应复用历史分类、命名、偏好或纠错记录。

**代价 / 风险**：

- 记忆设计复杂度会提前进入 MVP。
- 记忆误用会比普通错误更伤害信任。
- 如果底层组件替换成本过高，未来可能影响 framework 抽取。

## 复议触发条件

`adr_revisit_when` 已写入 front matter（见 SCHEMA §4.3.2 / §6.0），本节不重复。

## 相关页面

- [PURPOSE.md](../../PURPOSE.md)：本 ADR 对应的长期记忆核心地位。
- [SCHEMA.md](../../SCHEMA.md)：本 ADR 的结构契约。
- [ADR-007 记忆隐私与用户控制](memory-privacy-and-user-control.md)：定义记忆来源与用户控制边界。
- [ADR-011 Memory MVP 采用显式记忆账本](explicit-memory-ledger-mvp.md)：定义第一版 Memory 的实现形态。
- [pages/hubs/agent-os.md](../hubs/agent-os.md)：root hub。
