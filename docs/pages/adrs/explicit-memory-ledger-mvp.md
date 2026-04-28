---
title: ADR-011 Memory MVP 采用显式记忆账本
type: adr
subtype: architecture
canonical: true
summary: 第一版 Memory 先采用显式 Memory Ledger，记录可解释、可查看、可编辑、可删除的关键记忆，向量 / embedding 检索后置。
tags: [agent, memory, memory-design, privacy]
sources: []
created: 2026-04-28
updated: 2026-04-28
verified_at: 2026-04-28
freshness: volatile
status: active
archived_reason: ""
supersedes: []
related: [pages/adrs/long-term-memory-as-core-capability.md, pages/adrs/memory-privacy-and-user-control.md]
part_of: [pages/hubs/agent-os.md]
adr_status: accepted
adr_date: 2026-04-28
adr_revisit_when: Memory Ledger 无法支撑信息整理 dogfood、需要语义召回能力、记忆量增长导致人工查看不可用，或出现记忆删除 / 导出 / 审计需求时。
---

# ADR-011 Memory MVP 采用显式记忆账本

> 第一版 Memory 先采用显式 Memory Ledger，记录可解释、可查看、可编辑、可删除的关键记忆，向量 / embedding 检索后置。

## 背景

用户已确认长期记忆是核心能力，并同意第一版采用显式 Memory Ledger。这个决策解决的是「MVP 第一版 Memory 长什么样」：先做可解释账本，还是先做隐藏向量记忆。

ADR-007 已要求关键记忆可查看、可编辑、可删除，推断性记忆必须标注。若第一版直接采用隐藏向量记忆，容易在隐私、可解释、删除、审计上欠债。

## 备选方案

- 方案 A：第一版只做隐藏向量 / embedding 记忆，追求语义召回效果。
- 方案 B：第一版采用显式 Memory Ledger，向量 / embedding 检索后置。
- 方案 C：第一版不做持久记忆，只保留会话摘要。

## 被否决方案与理由

**方案 A 隐藏向量记忆优先**：

- user 很难知道 agent 记住了什么、为什么这么判断。
- 删除、导出、编辑、审计都会变复杂。
- 与 ADR-007 的可控性要求不匹配。

**方案 C 不做持久记忆**：

- 无法验证长期记忆是否减少重复表达成本。
- 信息整理 MVP 难以学习 user 的分类、命名和纠错习惯。

## 决策

采用方案 B：第一版 Memory 采用显式 Memory Ledger。

Ledger 中每条关键记忆至少应表达：

- `source`：来自对话、用户确认、文件整理操作、纠错记录或其它授权来源。
- `scope`：适用范围，例如全局、项目、文件夹、某类任务。
- `content`：可读的人类语言记忆内容。
- `explicit_or_inferred`：明确记忆还是推断记忆。
- `confidence`：置信度或稳定度。
- `sensitivity`：普通 / 敏感 / 高敏感。
- `created_at` 与必要的更新时间。
- `status`：active / corrected / deleted / archived 等生命周期状态。

默认策略：

- user 明确表达的偏好可进入 ledger。
- agent 从行为中推断的记忆必须标注为推断，不得伪装成 user 明确说过。
- 高敏感推断不得自动升级为稳定 user profile。
- 向量 / embedding 检索可以作为后续索引层，但不能取代 ledger 作为用户可控的真相源。

## 影响

**正向影响**：

- 第一版 Memory 与隐私 / 控制边界一致。
- dogfood 时能直接观察哪些记忆被使用、哪些记忆错了、哪些应删除。
- 后续增加向量检索时，有明确的结构化真相源可索引。

**代价 / 风险**：

- 语义召回能力会弱于向量记忆优先方案。
- 需要设计 memory UI / 命令来查看、编辑、删除 ledger。
- ledger 字段如果过早复杂化，会拖慢 MVP；字段应以能支撑 dogfood 为准。

## 复议触发条件

`adr_revisit_when` 已写入 front matter（见 SCHEMA §4.3.2 / §6.0），本节不重复。

## 相关页面

- [PURPOSE.md](../../PURPOSE.md)：本 ADR 对应的 Memory MVP 策略。
- [SCHEMA.md](../../SCHEMA.md)：本 ADR 的结构契约。
- [ADR-003 长期记忆是核心能力](long-term-memory-as-core-capability.md)：定义长期记忆的产品地位。
- [ADR-007 记忆隐私与用户控制](memory-privacy-and-user-control.md)：定义记忆来源、隐私与用户控制边界。
- [pages/hubs/agent-os.md](../hubs/agent-os.md)：root hub。
