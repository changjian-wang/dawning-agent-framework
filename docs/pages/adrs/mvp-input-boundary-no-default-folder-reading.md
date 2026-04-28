---
title: ADR-012 MVP 输入边界：不默认读取用户文件夹
type: adr
subtype: scope
canonical: true
summary: 信息整理 MVP 第一版不默认读取用户文件夹，而是从 user 显式提供 / 选择的材料、agent 管理的 inbox 或会话中沉淀的待整理内容开始。
tags: [agent, memory, privacy, product-philosophy]
sources: []
created: 2026-04-28
updated: 2026-04-28
verified_at: 2026-04-28
freshness: volatile
status: active
archived_reason: ""
supersedes: []
related: [pages/adrs/mvp-main-scenario-information-curation.md, pages/adrs/memory-privacy-and-user-control.md, pages/adrs/interest-profile-weighting-and-decay.md]
part_of: [pages/hubs/agent-os.md]
adr_status: accepted
adr_date: 2026-04-28
adr_revisit_when: 信息整理 MVP 需要扩大输入来源；user 明确要求读取文件夹；agent 管理的 inbox 无法支撑 dogfood；或出现用户文件夹读取带来的隐私 / 噪声 / 误整理问题时。
---

# ADR-012 MVP 输入边界：不默认读取用户文件夹

> 信息整理 MVP 第一版不默认读取用户文件夹，而是从 user 显式提供 / 选择的材料、agent 管理的 inbox 或会话中沉淀的待整理内容开始。

## 背景

ADR-005 已把 MVP 主场景锁定为信息整理，但“信息整理”不能被误读为“默认扫描用户电脑上的文件夹”。用户指出：大部分人没有稳定整理文件夹的习惯。如果第一版产品默认读取用户文件夹，就会假设用户已经有可利用的目录结构，而这正是产品要帮助解决的问题。

这条判断也与 ADR-007 的隐私边界一致：agent 不主动翻 user 的电脑，不主动枚举目录；只有 user 明确要求扫描指定范围或全盘文件时，才可读取对应文件系统内容。

## 备选方案

- 方案 A：默认让 user 选择一个本地文件夹，agent 从该文件夹开始整理。
- 方案 B：不默认读取用户文件夹，第一版从 user 显式提供 / 选择的材料、agent 管理的 inbox、或会话中沉淀的待整理内容开始。
- 方案 C：第一版直接接入邮件 / 云盘 / 日历等外部数据源，用真实应用数据驱动整理。

## 被否决方案与理由

**方案 A 默认选择本地文件夹**：

- 错误假设用户已有稳定整理文件夹的习惯。
- 用户文件夹通常混杂、命名不稳定、历史包袱重，噪声会淹没 MVP 验证目标。
- 容易让 user 感到 agent 在翻电脑，即便有授权也会增加不适感。

**方案 C 直接接入外部数据源**：

- OAuth、同步、权限、隐私和错误恢复链路都更重。
- 邮件 / 日历等外部系统一旦写错或误读，信任损失比本地 inbox 更大。
- 会把 MVP 从“验证记忆和候选生成”拖向“集成工程”。

## 决策

采用方案 B：不默认读取用户文件夹。

第一版输入入口：

- user 在对话中显式提供的文本、链接、摘录、文件片段或待整理材料。
- user 明确选择的单个文件或小批量文件。
- user 显式选择的兴趣 / 关注 tags，但这些只作为冷启动信号，不替代待整理材料。
- agent 管理的 inbox，例如“丢给管家的待整理箱”。
- 会话中自然沉淀的待整理内容，例如需求、想法、笔记草稿、分类偏好和纠错记录。

默认不做：

- 不默认扫描用户文件夹。
- 不默认读取桌面、下载目录、文档目录或项目根目录。
- 不把用户已有目录结构视为可信分类真相。
- 不把“读取文件夹”作为信息整理 MVP 的第一步。

允许但需显式授权：

- user 明确指定文件夹，并说明要 agent 整理 / 分析该范围时，可以读取对应范围。
- 授权只覆盖指定范围，不自动扩展到父目录、兄弟目录或全盘。
- 执行动作仍按 ADR-004 分级：只读分析可自决，移动 / 重命名 / 删除等动作必须遵守确认与恢复规则。

## 影响

**正向影响**：

- MVP 不建立在“用户已经整理过文件夹”的错误前提上。
- 输入边界更符合隐私预期，也更容易解释给 user。
- agent 管理的 inbox 能形成更干净的 dogfood 数据：哪些东西被丢进来、怎么分类、怎么纠错，都更可观察。

**代价 / 风险**：

- 第一版无法自动发现用户电脑里的历史材料，需要 user 主动投喂或选择。
- 信息整理的“自动化感”会弱于默认扫描文件夹方案。
- 后续如果要扩展到文件夹整理，需要单独设计授权 UI、范围预览、噪声过滤和回滚机制。

## 复议触发条件

`adr_revisit_when` 已写入 front matter（见 SCHEMA §4.3.2 / §6.0），本节不重复。

## 相关页面

- [PURPOSE.md](../../PURPOSE.md)：本 ADR 对应的 MVP 输入边界。
- [SCHEMA.md](../../SCHEMA.md)：本 ADR 的结构契约。
- [ADR-005 MVP 主场景选型 = 信息整理](mvp-main-scenario-information-curation.md)：定义 MVP 主场景。
- [ADR-007 记忆隐私与用户控制](memory-privacy-and-user-control.md)：定义文件读取授权与记忆隐私边界。
- [ADR-013 兴趣画像采用权重与时间衰减](interest-profile-weighting-and-decay.md)：定义兴趣 tags 的权重与衰减策略。
- [pages/hubs/agent-os.md](../hubs/agent-os.md)：root hub。