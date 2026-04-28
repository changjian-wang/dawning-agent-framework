---
title: ADR-010 客观代笔语气
type: adr
subtype: product
canonical: true
summary: agent 代笔默认冷静、客观、可靠，不加入不必要情绪，不深度拟人模仿 user。
tags: [agent, subject-object-boundary, product-philosophy]
sources: []
created: 2026-04-28
updated: 2026-04-28
verified_at: 2026-04-28
freshness: volatile
status: active
archived_reason: ""
supersedes: []
related: [pages/adrs/important-action-levels-and-confirmation.md]
part_of: [pages/hubs/agent-os.md]
adr_status: accepted
adr_date: 2026-04-28
adr_revisit_when: 开始实现邮件 / 文档 / 对外消息起草功能；或 user 需要区分不同语气模板；或出现代笔内容过度拟人 / 情绪化问题时。
---

# ADR-010 客观代笔语气

> agent 代笔默认冷静、客观、可靠，不加入不必要情绪，不深度拟人模仿 user。

## 背景

管家可以替 user 起草内容，但不能替 user 形成观点、定义身份或伪装成 user 本人。用户已明确：代笔应以做事靠谱为主，采用客观描述、冷静客观的风格，不需要混入不必要的情感。

## 备选方案

- 方案 A：深度模仿 user 的语气、情绪和表达习惯。
- 方案 B：默认冷静客观、可靠清晰，只做轻量格式与措辞适配。
- 方案 C：完全中性模板化，不学习 user 的任何表达偏好。

## 被否决方案与理由

**方案 A 深度模仿 user**：

- 容易让代笔越过主体 / 客体边界。
- 对外内容可能让 user 感到「这不是我，但它假装是我」。
- 情绪化表达增加误解风险。

**方案 C 完全模板化**：

- 虽然安全，但可能不够好用。
- 无法利用长期记忆中的格式偏好、称呼习惯、信息密度偏好。

## 决策

采用方案 B：客观可靠代笔。

- 默认语气为冷静、客观、清晰、可靠。
- 不加入不必要的情绪表达，不强行热情、安慰、共情或拟人化。
- 可以学习 user 的格式偏好、称呼习惯、长短偏好、信息密度偏好。
- 不深度模仿 user 的身份表达、价值判断、情绪状态或私人风格。
- 对外内容默认只是草稿；发送、发布、提交等对外动作必须按 ADR-004 走确认。
- 若 user 明确要求某种语气，agent 可临时按要求起草，但必须避免冒充 user 形成观点。

## 影响

**正向影响**：

- 降低代笔越界和情绪误伤风险。
- 保持产品定位：靠谱做事，而不是情绪陪伴。
- 与主体 / 客体边界一致，user 保留最终表达权。

**代价 / 风险**：

- 某些生活场景可能显得不够亲切。
- 未来如果需要更丰富的语气模板，需要另行设计显式选择机制。
- user 明确要求情绪化表达时，需要区分「临时语气要求」和「长期风格记忆」。

## 复议触发条件

`adr_revisit_when` 已写入 front matter（见 SCHEMA §4.3.2 / §6.0），本节不重复。

## 相关页面

- [PURPOSE.md](../../PURPOSE.md)：本 ADR 对应的代笔语气边界。
- [SCHEMA.md](../../SCHEMA.md)：本 ADR 的结构契约。
- [ADR-004 重要性级别与确认机制](important-action-levels-and-confirmation.md)：定义对外发送前的确认边界。
- [pages/hubs/agent-os.md](../hubs/agent-os.md)：root hub。
