---
title: ADR-001 管家定位与主客体边界
type: adr
subtype: product
canonical: true
summary: 将 dawning-agent-os 定位为 AI 管家，明确 user 是主体、agent 是客体，agent 只能起草判断与学习偏好，不能替 user 下结论或塑造偏好。
tags: [agent, butler-positioning, subject-object-boundary, product-philosophy]
sources: []
created: 2026-04-28
updated: 2026-04-28
verified_at: 2026-04-28
freshness: volatile
status: active
archived_reason: ""
supersedes: []
related: [pages/adrs/important-action-levels-and-confirmation.md, pages/adrs/objective-drafting-style.md]
part_of: [pages/hubs/agent-os.md]
adr_status: accepted
adr_date: 2026-04-28
adr_revisit_when: dogfood 中出现 agent 替 user 下结论、塑造偏好、伪装成 user 对外表达，或产品定位从管家形态转向工具 / 工作流平台时。
---

# ADR-001 管家定位与主客体边界

> 将 dawning-agent-os 定位为 AI 管家，明确 user 是主体、agent 是客体，agent 只能起草判断与学习偏好，不能替 user 下结论或塑造偏好。

## 背景

[PURPOSE.md](../../PURPOSE.md) 已将 dawning-agent-os 定位为通用个人 AI agent，即 AI 管家形态。这个定位不是装饰性隐喻，而是产品边界：管家可以像主人的分身一样执行、整理、起草和提醒，但不能把自己变成主人。

如果没有主客体边界，agent 很容易在三个地方越界：替 user 做最终判断、替 user 形成偏好、替 user 对外表达立场。越界后的产品不再是管家，而会变成操控者、替身或不透明自动化系统。

## 备选方案

- 方案 A：把 agent 定位为自主代理，允许它在足够置信时替 user 决策。
- 方案 B：把 agent 定位为管家：执行层可代劳，判断层只起草，意志层只学习不塑造。
- 方案 C：把 agent 定位为普通工具，只响应明确命令，不学习长期偏好。

## 被否决方案与理由

**方案 A 自主代理**：

- 容易把最终判断权从 user 手里拿走。
- 会模糊责任边界，尤其在生活决策、专业判断、对外发言中风险过高。
- 与「记忆服务于侍奉，不用于行为操控」冲突。

**方案 C 普通工具**：

- 安全但失去管家形态的核心价值。
- 不学习长期偏好，也就无法减少 user 的重复表达成本。

## 决策

采用方案 B：AI 管家定位，严格区分主体与客体。

具体边界：

- user 是主体，agent 是客体。
- 执行层：agent 可以替 user 做事，例如整理、归类、起草、检索、提醒。
- 判断层：agent 可以替 user 起草判断、列 tradeoff、给候选，但不能替 user 下最终结论。
- 意志层：agent 可以学习 user 的偏好、习惯、表达方式和项目上下文，但不能塑造 user 的偏好、定义 user 的身份，或引导 user 的注意力。
- 涉及价值观、身份认同、生活重大选择、专业终局判断时，agent 必须停在建议 / 草稿 / tradeoff 层。
- 对外表达必须让 user 知道这是草稿；发送、发布、提交等动作必须走确认机制。

## 影响

**正向影响**：

- 为后续所有动作分级、代笔、记忆、主动性设计提供最高层边界。
- 允许 agent 足够有用，同时避免变成替 user 做人的系统。
- 解释了为什么本产品不是普通工具，也不是完全自主代理。

**代价 / 风险**：

- 某些用户可能希望 agent 更强势地直接替他决定，本产品默认不满足这种期待。
- 边界判断在具体场景中仍需 dogfood 校准，尤其是「起草判断」与「下结论」之间的灰区。

## 复议触发条件

`adr_revisit_when` 已写入 front matter（见 SCHEMA §4.3.2 / §6.0），本节不重复。

## 相关页面

- [PURPOSE.md](../../PURPOSE.md)：本 ADR 对应的管家定位与主客体边界。
- [SCHEMA.md](../../SCHEMA.md)：本 ADR 的结构契约。
- [ADR-004 重要性级别与确认机制](important-action-levels-and-confirmation.md)：定义高风险动作确认边界。
- [ADR-010 客观代笔语气](objective-drafting-style.md)：定义代笔时不深度拟人模仿 user。
- [pages/hubs/agent-os.md](../hubs/agent-os.md)：root hub。
