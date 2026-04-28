---
title: ADR-007 记忆隐私与用户控制
type: adr
subtype: product
canonical: true
summary: 将 user-agent 对话作为主要记忆来源，禁止 agent 主动扫描用户电脑，并要求关键记忆可查看、可编辑、可删除。
tags: [agent, memory, privacy, product-philosophy]
sources: []
created: 2026-04-28
updated: 2026-04-28
verified_at: 2026-04-28
freshness: volatile
status: active
archived_reason: ""
supersedes: []
related: [pages/adrs/important-action-levels-and-confirmation.md, pages/adrs/mvp-main-scenario-information-curation.md]
part_of: [pages/hubs/agent-os.md]
adr_status: accepted
adr_date: 2026-04-28
adr_revisit_when: 出现用户要求扫描全盘文件、接入云同步、记忆删除 / 导出需求、或记忆误用导致信任问题时。
---

# ADR-007 记忆隐私与用户控制

> 将 user-agent 对话作为主要记忆来源，禁止 agent 主动扫描用户电脑，并要求关键记忆可查看、可编辑、可删除。

## 背景

[PURPOSE.md](../../PURPOSE.md) 已确认长期记忆是产品核心能力，但未定义记忆来源与隐私边界。

用户已明确：

- user 与 agent 沟通的所有话题都可以作为记忆存储。
- agent 不可以主动去翻 user 的电脑。
- 只有当 user 明确要求扫描电脑所有文件，或明确指定扫描范围时，agent 才可以读取对应文件系统内容。
- 其它记忆控制默认采用保守方案：关键记忆可查看、可编辑、可删除；推断性记忆需要标注为推断。

## 备选方案

- 方案 A：默认主动扫描用户电脑，尽快建立完整 user model。
- 方案 B：只把 user-agent 对话作为默认记忆来源；文件系统读取必须由 user 明确授权。
- 方案 C：默认不存长期记忆，每次会话从零开始。

## 被否决方案与理由

**方案 A 默认主动扫描电脑**：

- 侵犯边界感，会让 personal OS 变成窥探系统。
- 用户无法预期 agent 看到了什么，也无法信任记忆来源。
- 与「记忆服务于侍奉，不用于行为操控」冲突。

**方案 C 默认不存长期记忆**：

- 会丢失管家形态的核心价值。
- 每次都要 user 重复上下文，退化成普通聊天工具。

## 决策

采用方案 B：conversation-first memory，文件系统读取必须显式授权。

具体规则：

- user 与 agent 沟通的所有话题都可以作为记忆存储。
- conversation memory 是默认记忆来源；agent 可以用它理解 user 的长期偏好、表达习惯、项目上下文和反复出现的问题。
- agent 不主动扫描 user 的电脑，不主动翻本地文件，不主动枚举目录。
- user 明确要求扫描指定文件 / 文件夹 / 全盘文件时，agent 才能读取对应范围；授权只覆盖本次指定范围，不自动扩展。
- 关键记忆必须可查看、可编辑、可删除。
- 推断性记忆必须标注为「推断」，不能伪装成 user 明确说过的话。
- 高敏感推断（健康、财务、亲密关系、身份认同、情绪状态）不得自动升级为稳定 user profile；若确需长期使用，必须先让 user 确认。
- 记忆默认本地优先；云同步、跨设备同步、第三方托管需要单独决策。

## 影响

**正向影响**：

- 保留长期记忆价值，同时避免 agent 主动窥探用户电脑。
- user 能理解记忆来源：默认来自对话，而不是暗中扫描。
- 未来实现 memory UI 时，有明确的查看 / 编辑 / 删除要求。

**代价 / 风险**：

- conversation-first memory 可能错过本地文件里的隐含上下文，需要 user 主动授权扫描。
- 「所有对话话题都可作为记忆」会增加数据治理压力，必须尽早设计删除、导出、审计能力。
- 推断性记忆如果标注不清，仍可能造成“agent 以为它懂我”的误用。

## 复议触发条件

`adr_revisit_when` 已写入 front matter（见 SCHEMA §4.3.2 / §6.0），本节不重复。

## 相关页面

- [PURPOSE.md](../../PURPOSE.md)：本 ADR 对应的记忆红线。
- [SCHEMA.md](../../SCHEMA.md)：本 ADR 的结构契约。
- [ADR-004 重要性级别与确认机制](important-action-levels-and-confirmation.md)：定义文件扫描 / 删除等动作的确认边界。
- [ADR-005 MVP 主场景选型 = 信息整理](mvp-main-scenario-information-curation.md)：首个使用 conversation memory 与文件整理能力的 MVP 场景。
- [pages/hubs/agent-os.md](../hubs/agent-os.md)：root hub。
