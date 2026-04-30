---
name: wiki-lint
description: |
  Use when: 用户请求健康检查、可读性体检、矛盾检测、孤立页扫描、frontmatter 校验、受控 tag 校验、canonical 唯一性检查、链接路径检查、stale 检查
  Don't use when:
    - 提供新资料要归档（→ wiki-ingest）
    - 要回答问题（→ wiki-query）
    - 仅做单页编辑无系统性检查需求
  Inputs: 检查范围（全量 / 子目录 / 指定标签）
  Outputs: 结构化报告（阻断/重要/复查 三档）、可选修复建议
  Success criteria: 未触碰 raw/、未手维 overview.md/log.md、输出分档报告、物理删除 0 个页、修复有 SCHEMA 章节依据
---

# wiki-lint

## Authority

- 操作前必须读取 `docs/PURPOSE.md` 与 `docs/SCHEMA.md`。
- 与本 SKILL 冲突时以 SCHEMA 为准。
- **完整 lint 项以 SCHEMA §8.3 为准**；本 SKILL 只描述操作流程与分类映射，不复述全量项。
- 不修改 `docs/raw/`（§10.1 #2）。
- 不手维 `docs/overview.md` 与 `docs/log.md`（§10.1 #3，派生物）。
- 不物理删除 wiki 页；退役走 `status: archived` + 非空 `archived_reason`，取代走 `supersedes`（§10.3 #11）。

## Use when

- 用户请求健康检查、可读性体检、矛盾检测、孤立页扫描、frontmatter 校验。
- 关键词：lint, 健康检查, 可读性, 矛盾, 孤立页, stale, frontmatter, 体检, 复查。

## Don't use when

- 用户提供新资料要归档（→ `wiki-ingest`）。
- 用户提问要回答（→ `wiki-query`）。
- 仅做单页编辑，无系统性检查需求。

## Inputs

- 检查范围：全量 / 指定子目录 / 指定标签。
- 是否同时执行修复：默认先报告；阻断项可直接修复，重要项先征求用户意见。

## Steps

### 1. 扫描分类（完整项见 SCHEMA §8.3）

| # | 分类 | 严重度 | 主要内容 | 权威来源 |
|---|---|---|---|---|
| 1 | frontmatter 完整性 | 阻断 | 通用 16 字段；rule 的 `level`；adr 的 `adr_status / adr_date / adr_revisit_when`；日期格式 `YYYY-MM-DD`；空值规范 | §8.3.1 / §4 |
| 2 | 受控枚举 | 阻断 | `type / subtype / status / freshness / adr_status / level / tag` 是否在词表内；新增枚举须先改 SCHEMA | §8.3.1 / §3.2 / §5 |
| 3 | canonical 唯一性 | 阻断 | 同主题至多一页 `canonical: true`；与 status 耦合（§4.6.2） | §8.3.1 / §4.6 |
| 4 | 状态机 | 阻断 | status / adr_status 单向推进；archived 终态；stale 且 canonical:true 时 `updated` 距今 > 30 天必须降级或归档 | §8.3.1 / §4.6.1 |
| 5 | 链接合法性 | 阻断 | `sources` 以 `raw/` 开头；`supersedes / related / part_of` 以 `pages/` 开头；路径真实存在；无自指；无指向 raw；无 wikilink；数组去重 | §8.3.1 / §4.4 / §4.5 |
| 6 | 拓扑约束 | 阻断 | root hub 唯一且 `pages/hubs/agent-os.md`；hub 嵌套 ≤ 2 层 DAG；`part_of` 首元素是 hub；`part_of` 元素 type ∈ {hub, concept, rule}；非 root / 非取代页 `part_of` 不得为空 | §8.3.1 / §7.2 |
| 7 | ADR 取代关系 | 阻断 | superseded 必须被新 ADR `supersedes` 指向；supersedes DAG 无环；同 type 取代；accepted 必须有非空可观察的 `adr_revisit_when` | §8.3.1 / §4.5 / §4.6 |
| 8 | 模板合规 | 阻断 | H1 等于 frontmatter `title`；必备 H2 齐全且按 §6 顺序；正文不复述 frontmatter 字段；`sources` 非空必出现「来源」H2 | §8.3.1 / §6 |
| 9 | 命名规范 | 阻断 | 文件名 `kebab-case.md`；slug 不含 type/status/日期；`pages/{type}/` 子目录命名同规则；图片命名 `{slug}-{purpose}.{ext}` | §8.3.1 / §9 |
| 10 | 主入口合规 | 阻断 | `archived / superseded` 不作为 hub 主入口；`canonical: false` 必可经 `supersedes` 或 `part_of` 追溯到当前权威页 | §8.3.1 / §4.6.3 / §4.6.4 |
| 11 | 规模提示 | 提示 | 单页可选 H2 > 模板+4；hub「从这里开始」> 12 项 | §8.3.2 / §7 |
| 12 | 时效提示 | 提示 | `freshness: volatile` 且 `verified_at` > 90 天 | §8.3.2 |
| 13 | 链接风格 | 提示 | 正文 markdown 链接未用相对当前文件路径，或与 frontmatter 链接指向不一致 | §8.3.2 / §6.0 |
| 14 | 复查节奏 | 复查 | `freshness: evergreen` 且 `verified_at` > 365 天；`adr_status: proposed` 长期未推进；孤岛页面 | §8.3.3 |

> **复查节奏 vs 状态机硬约束**：第 12 行「volatile 90 天 / evergreen 365 天」是 §8.3.2/§8.3.3 的提示性复查节奏；与 §4.6.1 / 第 4 行的 `stale + canonical:true` 30 天降级**不同**。前者是建议提醒，后者是硬约束。两者并存，不要混淆。

### 2. 输出报告（先报告，再修复）

```markdown
## Lint 报告 [YYYY-MM-DD]

### 阻断（lint error，必须修）
- [ ] {问题简述} — {页面相对路径} — SCHEMA §X.Y

### 重要（lint warning，建议修）
- [ ] ...

### 复查（lint info，周期提醒）
- [ ] ...
```

每条问题必须给出 SCHEMA 章节依据，不凭直觉判定。

### 3. 修复执行

- 阻断项本次修复，除非需要人类提供缺失事实（如缺 `sources` 但无原始资料）。
- 重要项先征求用户意见。
- 不物理删除页面；退役走 §8.5 archive，取代走 §8.4 supersede。
- 不修改 `docs/raw/`；不手维 `docs/overview.md` 与 `docs/log.md`。
- 修复后刷新受影响页 `updated`；若变更涉及事实复核，同步刷新 `verified_at`。

## Success criteria

- [ ] 输出结构化报告（阻断 / 重要 / 复查 三档）。
- [ ] 每条问题引用具体 SCHEMA 章节作为依据。
- [ ] 未触碰 `docs/raw/`。
- [ ] 未手维 `docs/overview.md` / `docs/log.md`。
- [ ] 修复后受影响 wiki 页 `updated`（必要时 `verified_at`）字段已刷新。
- [ ] 物理删除 0 个页面；退役一律走 `archived` / `superseded`。

## Anti-patterns

- ❌ 边查边改不输出报告（用户失去审查机会）。
- ❌ 物理删除"无价值"页面。
- ❌ 手动维护 `overview.md` / `log.md`。
- ❌ 按已废弃规则检查 `docs/index.md` 漂移或 `.zh-CN.md` 双语 twin 同步。
- ❌ 在 frontmatter 链接字段使用 Obsidian wikilink。
- ❌ 把 90/365 天复查提示与 30 天 stale 硬降级混淆。
- ❌ 不引用 SCHEMA 章节凭经验判定问题（结论难以审查）。

## References

- 范围与意图：`docs/PURPOSE.md`
- 结构契约：`docs/SCHEMA.md` §3 类型 / §4 frontmatter / §5 tag / §6 模板 / §7 拓扑 / §8.3 lint / §8.4 supersede / §8.5 archive / §9 命名 / §10 红线
- 关联规则：`docs/pages/rules/git-commit-conventions.md`（修复后提交时一并适用）
- 关联 SKILL：`wiki-ingest`（新建/更新页时按其步骤）、`wiki-query`（结构无关的查询走它）
