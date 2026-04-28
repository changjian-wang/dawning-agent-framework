---
title: ADR-013 兴趣画像采用权重与时间衰减
type: adr
subtype: product
canonical: true
summary: 用户兴趣不作为永久静态标签，而是在 Memory Ledger 中以带权重、置信度与时间衰减的关注信号维护。
tags: [agent, memory, memory-design, interaction-design, product-philosophy]
sources: []
created: 2026-04-28
updated: 2026-04-28
verified_at: 2026-04-28
freshness: volatile
status: active
archived_reason: ""
supersedes: []
related: [pages/adrs/mvp-main-scenario-information-curation.md, pages/adrs/long-term-memory-as-core-capability.md, pages/adrs/explicit-memory-ledger-mvp.md, pages/adrs/mvp-input-boundary-no-default-folder-reading.md, pages/adrs/mvp-first-slice-chat-inbox-read-side.md]
part_of: [pages/hubs/agent-os.md]
adr_status: accepted
adr_date: 2026-04-28
adr_revisit_when: 兴趣画像无法降低信息整理成本、权重衰减导致长期关注被误删、user 要求重置 / 导出画像、或外部平台习惯数据出现合法稳定接入方式时。
---

# ADR-013 兴趣画像采用权重与时间衰减

> 用户兴趣不作为永久静态标签，而是在 Memory Ledger 中以带权重、置信度与时间衰减的关注信号维护。

## 背景

ADR-012 已决定信息整理 MVP 不默认读取用户文件夹，而是从 user 显式提供 / 选择的材料、agent 管理的 inbox 或会话沉淀内容开始。为了让第一版有可用的冷启动入口，可以让 user 选择少量兴趣 tags。

但 user 补充指出：大部分人不会一直关注同一类信息。若把 tags 视为永久偏好，agent 会逐渐拿旧兴趣误判当前意图，甚至把已经过期的关注当成 user 身份的一部分。

外部平台习惯数据（例如短视频 / 内容平台的观看、点赞、停留数据）可能是高信号入口，但第一版不应依赖它：合法授权、平台接口、隐私解释和数据语义都很重，而且平台行为反映的是被算法投喂后的注意力，不必然等于 user 主动想长期积累的兴趣。

## 备选方案

- 方案 A：静态 tags。user 首次选择后长期有效，除非手动删除。
- 方案 B：带权重与时间衰减的兴趣画像。tags 只是冷启动种子，后续由 user 行为、确认、纠错和时间共同调整。
- 方案 C：以外部平台习惯数据作为主要兴趣来源。
- 方案 D：不做兴趣画像，每次信息整理只依赖当前输入。

## 被否决方案与理由

**方案 A 静态 tags**：

- 不能表达关注强弱，只能表达“有 / 没有”。
- 无法处理阶段性兴趣退潮，容易把旧关注误当成长期偏好。
- 与 ADR-001 的主客体边界存在张力：agent 不应把一次选择固化为 user 的身份标签。

**方案 C 外部平台习惯数据优先**：

- 授权、接入、解析、合规和用户信任成本都高，不适合作为 MVP 依赖项。
- 平台行为数据可能代表被算法塑造的注意力，而不是 user 明确选择的长期关注。
- 若处理不透明，容易从“理解主人”滑向“分析并操控注意力”，违背 ADR-007。

**方案 D 不做兴趣画像**：

- 信息整理每次都要重新解释背景，无法验证长期记忆是否减少表达成本。
- agent 难以判断 inbox 中哪些材料更值得优先整理或提醒。

## 决策

采用方案 B：兴趣画像采用权重与时间衰减。

第一版策略：

- tags 只作为冷启动种子，不作为永久偏好或身份标签。
- 兴趣画像作为 Memory Ledger 的一种记忆条目，必须可解释、可查看、可编辑、可删除。
- 每个关注信号至少应能表达：`topic`、`source`、`scope`、`weight`、`confidence`、`last_touched_at`、`decay_policy`、`explicit_or_inferred`、`status`。
- user 主动选择、反复投喂、确认保留、持续纠错后仍保留的主题，可以提升权重。
- 长时间没有被使用、没有被确认、没有新材料进入的主题，默认降低权重。
- user 明确说“这是长期关注”时，可使用更慢的衰减或 pin；user 明确否定时，应降权、归档或删除。
- 推断出的兴趣必须标注为推断，不得伪装成 user 明确选择。
- 第一版使用简单可解释规则，不引入黑盒推荐模型；具体权重参数以 dogfood 可调为准。

外部平台习惯数据不作为 MVP 默认入口。未来如需接入，只能通过 user 主动导出、平台开放 API、浏览器扩展授权或其它可解释授权方式进入，并且仍要落到可查看、可删除的 ledger 记录中。

## 影响

**正向影响**：

- 兴趣画像能表达“当前更关注什么”，而不是只记录“曾经关注过什么”。
- 信息整理可以按关注权重排序，降低 inbox 噪声。
- 长期不关注自动降权，减少旧偏好污染当前任务。
- 与 ADR-011 的显式 Memory Ledger 一致，保留可解释和可控性。

**代价 / 风险**：

- 需要设计权重更新与衰减策略，复杂度高于静态 tags。
- 衰减过快会丢失真正的长期兴趣，衰减过慢会保留过期兴趣。
- 若 UI 不透明，user 可能不知道 agent 为什么认为某个主题重要。

最低要求：第一版宁可采用简单可解释规则，也不要上来做黑盒推荐模型。

## 复议触发条件

`adr_revisit_when` 已写入 front matter（见 SCHEMA §4.3.2 / §6.0），本节不重复。

## 相关页面

- [PURPOSE.md](../../PURPOSE.md)：本 ADR 对应的兴趣画像策略。
- [SCHEMA.md](../../SCHEMA.md)：本 ADR 的结构契约。
- [ADR-003 长期记忆是核心能力](long-term-memory-as-core-capability.md)：定义长期记忆的产品地位。
- [ADR-005 MVP 主场景选型 = 信息整理](mvp-main-scenario-information-curation.md)：定义信息整理 MVP。
- [ADR-011 Memory MVP 采用显式记忆账本](explicit-memory-ledger-mvp.md)：定义第一版 Memory Ledger。
- [ADR-012 MVP 输入边界：不默认读取用户文件夹](mvp-input-boundary-no-default-folder-reading.md)：定义 MVP 默认输入边界。
- [ADR-014 MVP 第一版切片：聊天 + inbox + 读侧整理](mvp-first-slice-chat-inbox-read-side.md)：定义第一版兴趣权重采用简单规则。
- [pages/hubs/agent-os.md](../hubs/agent-os.md)：root hub。