---
name: wiki-query
description: |
  Use when: 用户对 wiki 内容提问、要求综合 / 对比 / 综述 已有页面
  Don't use when:
    - 提供了新原始资料要归档（→ wiki-ingest）
    - 要求修复 wiki 健康问题（→ wiki-lint）
    - 问题与 wiki 内容无关
  Inputs: 用户问题或综合需求
  Outputs: 带引用的回答；如有持久价值，回写到 pages/{adrs,comparisons,concepts,rules}/ 或更新现有页
  Success criteria: 入口为 root hub、所有判断附引用、已评估回写价值并执行、未修改 raw/、未引用 archived/superseded 页
---

# wiki-query

## Authority

- 操作前必须读取 `docs/PURPOSE.md` 与 `docs/SCHEMA.md`。
- 与本 SKILL 冲突时以 SCHEMA 为准。
- 不基于通用知识硬编 wiki 当前结论（§10.2 #6）；查不到时返回「未收录」并提示是否走 ingest。
- 不把 `draft / archived / superseded` 页面作为当前结论或主入口引用（§10.2 #7）。
- 不修改 `docs/raw/`（§10.1 #2）。
- 不手维 `docs/overview.md` 与 `docs/log.md`（§10.1 #3）。

## Use when

- 用户对 wiki 内容提出问题。
- 用户要求综合 / 对比 / 综述已有页面。
- 关键词：查询 wiki, 回答, 综合, 对比, 比较, 找一下, 综述, query。

## Don't use when

- 用户提供了新原始资料要归档（→ `wiki-ingest`）。
- 用户要求修复 wiki 健康问题（→ `wiki-lint`）。
- 问题与 wiki 内容无关（直接回答即可）。

## Inputs

- 用户的问题或综合需求。

## Steps（薄壳，详见 SCHEMA §8.2）

1. **从 root hub 进入定位**
   - 入口：`docs/pages/hubs/agent-os.md`（§7.2 唯一 root hub，`canonical: true / status: active / part_of: []`）。
   - 沿 hub「从这里开始」与子 hub 跳转到 canonical 页；不绕过 hub 直接全文搜索（§8.2 #2）。
   - 关键词检索 `pages/{entities,concepts,comparisons,rules,adrs}/` 仅作辅助；不要先 grep 整个 `docs/`。

2. **深读相关页面**
   - 沿 frontmatter `related / part_of / supersedes` 扩展 1–2 跳。
   - 必要时回查 `sources` 字段对应的 `raw/` 资料（只读，§10.1 #2）。

3. **带引用综合回答**
   - 每个关键判断标注来源，使用相对当前文件的 markdown 链接（§6.0），**禁止 Obsidian `[[wikilink]]`**。
   - 区分「wiki 已有结论 / 本次推论 / 未收录」三类。
   - 仅引用 `canonical: true` 且 `status ∈ {active, stale}` 的页；不要引用 `draft / archived / superseded`（§10.2 #7）。
   - 发现矛盾时明确指出，并触发 `wiki-lint` 待办；不在 query 流程内自行修复结构。
   - 查不到答案时返回「未收录」并提示是否走 wiki-ingest（§8.2 #4）。

4. **判断是否回写**（关键步骤，不要跳过）

   仅当答案有持续复用价值时回写（§8.2 #5）。一句话能答完且不需复用的回答**不**回写为页面，避免 SCHEMA-bypass 长答案。

   回写映射：

   | 回答性质 | 落地位置 | 模板 |
   |---|---|---|
   | 新决策 / 已有决策的更新 | `pages/adrs/`，新建 ADR 或在现有 ADR 走 §8.4 supersede | §6.6 + §4.3.2 |
   | 多对象横向选型 / 选型分析 | `pages/comparisons/` | §6.4 |
   | 概念解释 / 模式 / 方法论 | `pages/concepts/` 或更新已有 | §6.3 |
   | 单具名对象的展开 | `pages/entities/` 或更新已有 | §6.2 |
   | 新硬约束 / 流程规则 | `pages/rules/` | §6.5 + §4.3.1 |
   | 对已有页的补充 | 直接更新该页 | 同原模板，刷新 `updated` 与 `verified_at` |

   回写按 `wiki-ingest` 步骤执行：填全 frontmatter 16 字段（rule/adr 加专属字段）、按 §6 模板起草、加入站链接、§8.3.1 自检。

## Success criteria

- [ ] 入口为 `pages/hubs/agent-os.md`，不是直接全文搜索。
- [ ] 所有关键判断附引用，使用相对当前文件的 markdown 路径。
- [ ] 已识别"是否需要回写"并执行（回写或显式判定无需）。
- [ ] 回写页面（如有）满足 SCHEMA §4 frontmatter 与 §6 模板。
- [ ] 未引用 `draft / archived / superseded` 页作为当前结论。
- [ ] 未修改 `docs/raw/`，未手维 `docs/overview.md` / `docs/log.md`。

## Anti-patterns

- ❌ 不查 hub 直接 grep / 全文搜索。
- ❌ 答完就走，不评估回写价值（探索成果会丢失）。
- ❌ 把综合内容写到不存在的 `synthesis/` / `decisions/` 目录。
- ❌ 维护已废弃的 `docs/index.md` / `docs/log.md`。
- ❌ 用 Obsidian `[[wikilink]]`；正文链接必须用相对路径 markdown。
- ❌ 引用 archived / superseded 页作为当前结论。
- ❌ 在 query 流程内动 lint（结构问题留给 `wiki-lint`）。

## References

- 范围与意图：`docs/PURPOSE.md`
- 结构契约：`docs/SCHEMA.md` §4.6 状态与 canonical / §6 模板 / §6.0 链接风格 / §7.2 拓扑 / §8.2 query / §10 红线
- root hub：`docs/pages/hubs/agent-os.md`
- 关联 SKILL：`wiki-ingest`（回写时按其步骤）、`wiki-lint`（结构问题留给它）
