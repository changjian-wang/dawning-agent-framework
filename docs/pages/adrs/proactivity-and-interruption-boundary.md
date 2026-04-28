---
title: ADR-008 主动性与打断边界
type: adr
subtype: product
canonical: true
summary: agent 默认不实时打断用户，普通主动性汇总为候选摘要，只有高优先级风险才立即打断。
tags: [agent, proactivity, interaction-design, product-philosophy]
sources: []
created: 2026-04-28
updated: 2026-04-28
verified_at: 2026-04-28
freshness: volatile
status: active
archived_reason: ""
supersedes: []
related: [pages/adrs/important-action-levels-and-confirmation.md, pages/adrs/abstract-instruction-fallback.md]
part_of: [pages/hubs/agent-os.md]
adr_status: accepted
adr_date: 2026-04-28
adr_revisit_when: dogfood 中出现主动提示打扰、漏报重要风险、或接入日程 / 文件监控等持续观察能力时。
---

# ADR-008 主动性与打断边界

> agent 默认不实时打断用户，普通主动性汇总为候选摘要，只有高优先级风险才立即打断。

## 背景

管家形态需要主动性，但主动性过度会变成骚扰。用户接受采用保守默认：默认不实时打断；普通主动性走候选摘要；只有安全、截止时间、数据丢失、误删 / 误改风险等高优先级事件才打断。

## 备选方案

- 方案 A：agent 实时主动提醒，只要发现机会就打断。
- 方案 B：默认不实时打断，普通建议汇总，高优先级风险才打断。
- 方案 C：agent 永不主动，只响应 user 明确请求。

## 被否决方案与理由

**方案 A 实时主动提醒**：

- 容易把管家变成噪音源。
- user 需要不断处理 agent 的判断，反而增加认知负担。

**方案 C 永不主动**：

- 会退化成普通工具，无法体现管家价值。
- 错过日程冲突、误删风险、数据丢失等必须及时提醒的场景。

## 决策

采用方案 B：主动性分层。

- 默认不实时打断。
- 普通主动建议汇总成候选摘要，在任务结束、阶段性检查点或 user 主动查看时呈现。
- 只有高优先级事件允许立即打断，包括安全风险、截止时间风险、数据丢失风险、误删 / 误改风险、不可逆外部动作风险。
- 信息整理场景中，agent 默认先安静整理 / 分析，再给候选；除非发现即将发生的数据损坏或不可恢复操作，否则不打断。
- 主动建议仍遵守 options-over-elaboration：给 2–4 个候选，而不是丢一段长解释让 user 自己拆。

## 影响

**正向影响**：

- 保留管家的主动价值，同时降低骚扰感。
- user 能形成预期：普通建议等摘要，风险事件才打断。
- 与 ADR-004 的动作分级兼容，高风险动作仍需确认。

**代价 / 风险**：

- 高优先级事件的判定需要在 dogfood 中校准。
- 如果摘要频率过低，可能让主动性价值不明显。
- 如果摘要频率过高，仍会变成低强度骚扰。

## 复议触发条件

`adr_revisit_when` 已写入 front matter（见 SCHEMA §4.3.2 / §6.0），本节不重复。

## 相关页面

- [PURPOSE.md](../../PURPOSE.md)：本 ADR 对应的主动性边界。
- [SCHEMA.md](../../SCHEMA.md)：本 ADR 的结构契约。
- [ADR-004 重要性级别与确认机制](important-action-levels-and-confirmation.md)：定义高风险动作确认边界。
- [ADR-009 抽象指令兜底机制](abstract-instruction-fallback.md)：定义模糊指令下如何给候选。
- [pages/hubs/agent-os.md](../hubs/agent-os.md)：root hub。
