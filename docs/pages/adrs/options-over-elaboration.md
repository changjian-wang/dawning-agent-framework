---
title: ADR-002 选择题优先于问答题
type: adr
subtype: product
canonical: true
summary: 当 user 表达模糊时，agent 先结合上下文推断并给 2–4 个候选，让 user 选择、否决或微调，而不是把需求澄清工作推回给 user。
tags: [agent, interaction-design, product-philosophy]
sources: []
created: 2026-04-28
updated: 2026-04-28
verified_at: 2026-04-28
freshness: volatile
status: active
archived_reason: ""
supersedes: []
related: [pages/adrs/abstract-instruction-fallback.md, pages/adrs/important-action-levels-and-confirmation.md]
part_of: [pages/hubs/agent-os.md]
adr_status: accepted
adr_date: 2026-04-28
adr_revisit_when: dogfood 中发现候选生成无法减少需求描述成本，或 user 高频反馈候选太泛、太多、太少、无法选择时。
---

# ADR-002 选择题优先于问答题

> 当 user 表达模糊时，agent 先结合上下文推断并给 2–4 个候选，让 user 选择、否决或微调，而不是把需求澄清工作推回给 user。

## 背景

dawning-agent-os 的差异化不在领域，而在交互形态。传统工具要求 user 先把需求写清楚，本产品反过来：user 可以用自然、抽象、不完整的方式说话，agent 负责结合上下文与长期记忆，把开放问题压缩成少量候选。

这个原则不是「永远不问问题」。更准确的边界是：先推断，能推断就给候选；推断不出来或风险越过动作级别边界时才问，而且询问也尽量是选择题。

## 备选方案

- 方案 A：开放式追问，要求 user 先把需求补全。
- 方案 B：选择题优先，agent 先结合上下文推断并给候选。
- 方案 C：完全自动推断并执行，尽量不让 user 参与。

## 被否决方案与理由

**方案 A 开放式追问**：

- 把写需求、写 prompt、维护上下文的成本重新推给 user。
- 会把产品退化成普通聊天工具。

**方案 C 完全自动推断并执行**：

- 容易误解 user 意图并直接造成误操作。
- 与 ADR-004 的动作级别边界冲突。

## 决策

采用方案 B：选择题优先于问答题。

具体规则：

- user 表达模糊时，agent 先关联当前对话、当前任务、已授权材料与长期记忆。
- 能推断时，给 2–4 个候选方案，每个候选用一句话说明核心差异。
- user 的收敛方式应尽量低成本：点选、否决、改一个词、补一句约束。
- 推断不出来、候选差异无法收敛、或风险超过动作级别边界时，才询问 user。
- 询问也优先给选择题，不优先开放问答。
- L3 高风险动作不得从模糊表达中推断授权。

## 影响

**正向影响**：

- 明确产品不是 prompt 工程工具，而是降低需求表达成本的管家。
- 支撑信息整理 MVP 中的分类、归档、命名、检索候选生成。
- 与长期记忆形成正循环：记忆越多，候选越贴近 user。

**代价 / 风险**：

- 候选质量会成为核心体验指标。
- agent 需要判断何时推断、何时询问，否则会在「过度自信」和「过度追问」之间摇摆。
- 候选过多会增加负担，候选过少会遮蔽真实可能性。

## 复议触发条件

`adr_revisit_when` 已写入 front matter（见 SCHEMA §4.3.2 / §6.0），本节不重复。

## 相关页面

- [PURPOSE.md](../../PURPOSE.md)：本 ADR 对应的交互原则。
- [SCHEMA.md](../../SCHEMA.md)：本 ADR 的结构契约。
- [ADR-004 重要性级别与确认机制](important-action-levels-and-confirmation.md)：定义哪些候选可执行、哪些必须确认。
- [ADR-009 抽象指令兜底机制](abstract-instruction-fallback.md)：定义模糊指令下的上下文推断与询问边界。
- [pages/hubs/agent-os.md](../hubs/agent-os.md)：root hub。
