---
name: wiki-ingest
description: |
  Use when: 用户在 docs/raw/ 新增原始资料（论文/博文/repo/官方文档）需要摄入为 wiki 页面
  Don't use when:
    - 仅回答已有问题（→ wiki-query）
    - 仅做健康检查（→ wiki-lint）
    - 需要修改 docs/raw/（禁止）
  Inputs: docs/raw/ 下的新文件路径，可选指定要点
  Outputs: 新建/更新的 wiki 页面（含完整 frontmatter）、必要时更新 hub 入站链接
  Success criteria: 未修改 raw/、frontmatter 完整、所有声明可追溯、有入站链接、§8.3.1 自检通过
---

# wiki-ingest

## Authority

- 操作前必须读取 `docs/PURPOSE.md` 与 `docs/SCHEMA.md`。
- 与本 SKILL 冲突时以 SCHEMA 为准。
- 不修改 `docs/raw/`（SCHEMA §10.1 #2）。
- 不手维 `docs/overview.md` 与 `docs/log.md`（SCHEMA §10.1 #3，派生物）。
- 不收录 `PURPOSE.md` 范围之外的资料（§10.1 #4）。

## Use when

- 用户在 `docs/raw/{papers|articles|repos|official|meetings|assets}/` 下新增了文件。
- 关键词：摄入, ingest, 新资料, 加入 raw, 新论文, 新博文, 新增来源。

## Don't use when

- 仅回答已有问题（→ `wiki-query`）。
- 仅做健康检查或修复（→ `wiki-lint`）。
- 需要修改 `docs/raw/` 内容（禁止）。

## Inputs

- `docs/raw/{category}/{file}.md` 中的新文件路径。
- 可选：用户对要点和方向的提示。

## Steps（薄壳，详见 SCHEMA §8.1）

1. **范围确认**：按 PURPOSE 判定资料是否在收录范围；不在则拒收。
2. **路由判定**：按 SCHEMA §3.1 路由口诀确定本次新建/更新的 `type`，仅限 `hub / entity / concept / comparison / rule / adr` 六类；禁止发明新类型，禁止使用已废弃名（如 `decision / synthesis`）。
3. **优先更新而非新建**：检查同主题是否已有 `canonical: true` 页（§1 #3 / §4.6.2）；有则优先更新，刷新 `updated` 与 `verified_at`。
4. **frontmatter 起草**：按 §4.2 通用字段表填写全部 16 个字段；rule 追加 §4.3.1 `level`；adr 追加 §4.3.2 `adr_status / adr_date / adr_revisit_when`。
5. **正文起草**：从 §6 对应 type 模板复制 H2 骨架；H1 必须等于 frontmatter `title`，紧跟 `> {summary}`；可增 H2，不得删必备 H2，不得复述 frontmatter 字段（§6.0）。
6. **链接落地**：
   - `sources` 写 `raw/{category}/{file}.md`（§4.4），全小写 kebab-case。
   - `supersedes / related / part_of` 写 `pages/{type}/{slug}.md`（§4.5）；`part_of` 首元素必须是 hub。
   - 正文 markdown 链接用相对当前文件的路径（§6.0），**禁止 Obsidian `[[wikilink]]`**。
7. **入站链接**：至少从一个 hub 链接到新页（避免孤岛，§7.2）；通常更新 `pages/hubs/agent-os.md`「从这里开始」。
8. **自检**：按 §8.3.1 阻断项逐项核对，全部通过才算完成。

## Frontmatter 通用骨架

```yaml
---
title: ...
type: hub | entity | concept | comparison | rule | adr
subtype: ...                       # 可选；按 §3.2 选择，不适用则省略本行
canonical: true | false
summary: 一句话摘要
tags: [...]                         # §5 受控词表，1–6 个，至少 1 个领域 tag
sources: [raw/.../x.md]             # entity/concept/comparison 必非空；hub/rule/adr 可为 []
created: YYYY-MM-DD
updated: YYYY-MM-DD
verified_at: YYYY-MM-DD
freshness: evergreen | volatile
status: draft | active | stale | archived
archived_reason: ""                 # status=archived 时必填
supersedes: []
related: []
part_of: [pages/hubs/agent-os.md]   # 非 root hub / 非取代页必须非空
---
```

类型专属追加：

- `rule`：`level: 强制 | 推荐 | 参考`
- `adr`：`adr_status: proposed | accepted | superseded`、`adr_date: YYYY-MM-DD`、`adr_revisit_when: ""`（accepted 时必须非空可观察事件）

## Success criteria

- [ ] 未修改 `docs/raw/` 任何文件。
- [ ] 新建/更新页面 frontmatter 完整，type 与 `pages/{type}/` 目录匹配。
- [ ] 每条事实性判断可追溯到 `sources`。
- [ ] 至少一处入站链接（来自 hub 或同类型页）。
- [ ] 正文链接为相对当前文件的 markdown 路径（无 wikilink）。
- [ ] 通过 SCHEMA §8.3.1 阻断项自检。

## Anti-patterns

- ❌ 使用已废弃 type 名 `decision / synthesis`（应为 `adr` / 更新已有 `concept|comparison`）。
- ❌ 维护已不存在的 `docs/index.md`、双语 `.zh-CN.md` twin。
- ❌ 手动追加 `docs/log.md` 或 `docs/overview.md`（派生物）。
- ❌ frontmatter 仅写 7 个字段，缺 `canonical / verified_at / freshness / archived_reason / part_of` 等。
- ❌ 使用 Obsidian `[[wikilink]]`。
- ❌ 创建孤岛页面（无任何 hub 入站链接）。
- ❌ 基于通用知识写 wiki 没收录的"事实"。
- ❌ 在 `pages/{type}/` 之外的目录创建 wiki 页（如直接放 `docs/synthesis/`）。

## References

- 范围与意图：`docs/PURPOSE.md`
- 结构契约：`docs/SCHEMA.md` §3 类型 / §4 frontmatter / §5 tag / §6 模板 / §8.1 ingest / §8.3 lint / §10 红线
- 关联规则：`docs/pages/rules/plan-first-implementation.md`、`docs/pages/rules/git-commit-conventions.md`
