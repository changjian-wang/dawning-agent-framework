# Dawning Agent OS — Copilot Instructions

## 项目概述

Dawning Agent OS 是一个以 LLM Wiki 模式组织的知识库 + 架构研究仓库。

- **核心产物**：`docs/` 下的编译式 wiki（不是源代码项目）
- **工作模式**：人类策展原始资料、LLM 编译并维护知识页面
- **权威规则**：[docs/SCHEMA.md](../docs/SCHEMA.md)（与本文冲突一律以 SCHEMA 为准）

## 核心红线（任何变更必须遵守）

1. **`docs/raw/` 不可变** — LLM 只读，永不修改、永不删除
2. **wiki 页面必须有完整 YAML frontmatter** — `title / type / tags / sources / created / updated / status` 缺一不可
3. **每个声明可追溯** — wiki 中所有判断必须能落到 `docs/raw/` 上的资料
4. **目录命名空间固定** — 编译产物只进 `entities/ concepts/ comparisons/ decisions/ synthesis/` 五选一
5. **Ingest / Query / Lint 后必须更新 `index.md` 和 `log.md`**
6. **不物理删除 wiki 页** — 用 `status: archived`
7. **双语同步** — 更新 `.zh-CN.md` 时检查英文版是否同步；优先写中文
8. **链接约定** — 内部用 Obsidian wikilink `[[...]]`，引用 raw 用相对路径

## Skill 索引

| Skill | 触发关键词 | 用途 |
|---|---|---|
| `wiki-ingest` | 摄入, ingest, 新资料, 加入 raw, 新论文, 新博文 | 处理 raw/ 新资料 → 创建/更新 wiki 页 → 更新 index + log |
| `wiki-query` | 查询 wiki, 回写, query wiki, 综合, 综述 | 走 index → 深读 → 带引用回答 → 有价值时回写 → log |
| `wiki-lint` | lint, 健康检查, 可读性体检, 矛盾检测, 孤立页, frontmatter | 检查 frontmatter / 孤立页 / stale / 矛盾 / 重复 |

## Skill 使用规则

- 所有涉及 `docs/` 的写操作必须先匹配到对应 skill 并按其步骤执行
- SKILL 是操作手册；规则细节以 [docs/SCHEMA.md](../docs/SCHEMA.md) 为准
- 单次任务可串联多个 skill（如 ingest → lint）

## 标准编排链

- **新资料进入**：`wiki-ingest` →（可选）`wiki-lint`
- **回答 + 沉淀**：`wiki-query` →（有回写时）`wiki-lint`
- **定期维护**：`wiki-lint`

## 参考

- [docs/SCHEMA.md](../docs/SCHEMA.md) — 唯一权威规则
- [docs/concepts/00-foundations/llm-wiki-pattern.zh-CN.md](../docs/concepts/00-foundations/llm-wiki-pattern.zh-CN.md) — 模式说明
- [docs/index.md](../docs/index.md) — 内容入口
- [docs/log.md](../docs/log.md) — 操作历史
