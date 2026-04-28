---
title: ADR-009 抽象指令兜底机制
type: adr
subtype: product
canonical: true
summary: 模糊指令默认进入候选模式：L0 可直接做，L1 先预览或小范围执行，L2/L3 不执行。
tags: [agent, interaction-design, product-philosophy]
sources: []
created: 2026-04-28
updated: 2026-04-28
verified_at: 2026-04-28
freshness: volatile
status: active
archived_reason: ""
supersedes: []
related: [pages/adrs/important-action-levels-and-confirmation.md, pages/adrs/proactivity-and-interruption-boundary.md]
part_of: [pages/hubs/agent-os.md]
adr_status: accepted
adr_date: 2026-04-28
adr_revisit_when: dogfood 中出现模糊指令猜错、候选过多 / 过少、或 user 明确希望某类模糊指令可直接执行时。
---

# ADR-009 抽象指令兜底机制

> 模糊指令默认进入候选模式：L0 可直接做，L1 先预览或小范围执行，L2/L3 不执行。

## 背景

dawning-agent-os 的核心交互原则是 options-over-elaboration：user 不需要把需求写清楚，agent 应主动给候选让 user 选择。但模糊指令也带来误判风险，例如「处理一下」「整理一下」「优化一下」。

## 备选方案

- 方案 A：agent 尽量猜测 user 意图并直接执行。
- 方案 B：模糊指令默认进入候选模式，按 ADR-004 动作级别决定能否执行。
- 方案 C：遇到模糊指令一律反问 user 具体要什么。

## 被否决方案与理由

**方案 A 直接猜测执行**：

- 容易误改、误删或做出 user 没有授权的动作。
- 与「失败时优先保守」冲突。

**方案 C 一律反问**：

- 把需求重新写清楚的工作推回给 user。
- 违背 options-over-elaboration 的产品差异化。

## 决策

采用方案 B：候选兜底。

- 模糊指令默认给 2–4 个候选方案，每个候选用一句话说明核心差异。
- L0 信息型动作可以直接做，例如先搜索、读取、总结、列候选。
- L1 可逆整理型动作可以先预览，或在小范围内执行并保留回滚路径。
- L2 内容修改型动作不直接执行，除非 user 选择候选或明确指定对象与动作。
- L3 高风险动作绝不从模糊指令推断授权，必须一键确认。
- 如果 agent 猜错，默认回到候选模式：承认偏差、说明当前理解、给新的候选，不责怪 user 没说清。

## 影响

**正向影响**：

- 保留「不用写 prompt」的核心体验。
- 降低抽象指令带来的误操作风险。
- 与 ADR-004 的动作分级和 ADR-008 的主动性边界一致。

**代价 / 风险**：

- 候选质量直接决定体验；候选太泛会让 user 仍然感觉在写需求。
- L1 小范围执行的范围需要在 dogfood 中校准。
- 某些高频模糊指令未来可能需要个性化默认动作。

## 复议触发条件

`adr_revisit_when` 已写入 front matter（见 SCHEMA §4.3.2 / §6.0），本节不重复。

## 相关页面

- [PURPOSE.md](../../PURPOSE.md)：本 ADR 对应的抽象指令兜底原则。
- [SCHEMA.md](../../SCHEMA.md)：本 ADR 的结构契约。
- [ADR-004 重要性级别与确认机制](important-action-levels-and-confirmation.md)：定义 L0/L1/L2/L3 动作边界。
- [ADR-008 主动性与打断边界](proactivity-and-interruption-boundary.md)：定义候选摘要与打断边界。
- [pages/hubs/agent-os.md](../hubs/agent-os.md)：root hub。
