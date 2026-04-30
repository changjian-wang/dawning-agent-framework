---
title: Rule Git Commit 规范
type: rule
subtype: convention
canonical: true
summary: dawning-agent-os 仓库的 commit 信息格式、type/scope 词表、原子性与 body 要求。
tags: [meta, convention, process]
sources: []
created: 2026-04-30
updated: 2026-04-30
verified_at: 2026-04-30
freshness: evergreen
status: active
archived_reason: ""
supersedes: []
related: [pages/rules/plan-first-implementation.md, pages/adrs/engineering-skeleton-v0.md, pages/adrs/backend-architecture-equinox-reference.md]
part_of: [pages/hubs/agent-os.md]
level: 强制
---

# Rule Git Commit 规范

> dawning-agent-os 仓库的 commit 信息格式、type/scope 词表、原子性与 body 要求。

## 规则

### 1. 主题行格式

```text
<type>(<scope>): <subject>
```

- 主题行 ≤ 72 字符。
- subject 全小写（`add` 不是 `Add`）。
- 不以句号结尾。
- 用祈使句（`add ADR-019`，不是 `added ADR-019`）。
- subject 用英文，避免终端编码问题。
- ADR / rule / hub 等 wiki 页面正文按 SCHEMA 仍可写中文。

### 2. type 白名单

| type | 用途 |
|---|---|
| `feat` | 产品代码新功能 |
| `fix` | 产品代码 bug 修复 |
| `refactor` | 产品代码不改行为的重构 |
| `test` | 仅改测试代码 |
| `build` | 构建系统、依赖、SDK 配置 |
| `ci` | CI/CD 配置 |
| `chore` | 杂项（删除过时文件、批量重命名、配置初始化等） |
| `docs` | 所有 wiki / 文档变更，包括新增 ADR、rule、hub |

不允许在 type 之外发明新值；新增需先改本节。

### 3. scope 白名单

| scope | 触发条件 |
|---|---|
| `adr` | `docs/pages/adrs/**` |
| `hub` | `docs/pages/hubs/**` |
| `rules` | `docs/pages/rules/**` |
| `concepts` | `docs/concepts/**` |
| `frameworks` | `docs/frameworks/**` |
| `entities` | `docs/entities/**` |
| `comparisons` | `docs/comparisons/**` |
| `readings` | `docs/readings/**` |
| `schema` | `docs/SCHEMA.md` 或 `docs/PURPOSE.md` |
| `agents` | `AGENTS.md` / `CLAUDE.md` / `.github/copilot-instructions.md` |
| `scripts` | `scripts/**` |
| `scaffold` | 仓库根配置：`.editorconfig` / `.gitignore` / `Directory.Build.props` / `global.json` / `*.slnx` |
| `domain-core` / `domain` / `domain-services` / `application` / `infra-data` / `infra-bus` / `infra-ioc` / `infra-security` / `services-api` | `src/` 下对应后端项目 |
| `apps-desktop` | `apps/desktop/**` |
| `tests` | `tests/**` |

`scope` 取小写、`kebab-case`。新增 scope 必须先改本节。

### 4. body 要求

以下任一情况**必须**写 body（用 `-` 列点说明，每行 ≤ 100 字符）：

- 单 commit 改动 ≥ 3 个文件。
- 单 commit 行变更 ≥ 100 行（`+/-` 合计）。
- 新增 ADR / rule / hub。
- `refactor:` 类型。
- 删除文件（必须给删除原因）。

body 与主题行之间空一行。

### 5. 原子性铁律

- **一个 ADR = 一个 commit**：包括其引发的 `PURPOSE.md` 与 hub 链接更新一并入同一 commit；不与其他 ADR 合并。
- **一个 rule = 一个 commit**：同上。
- 不同 scope 不混在同一 commit；例如 `adr` 与 `agents` 同改时拆两个 commit。
- 例外：纯链接修补（如新建 ADR 时同步 hub 引用）允许并入；规则变更不算链接修补。

### 6. AI 协作署名

- 允许保留 `Co-authored-by: Copilot <copilot@github.com>`。
- 不强制；署名缺失不构成违规。

### 7. 与 plan-first 的关系

- 实现 / 架构 / 目录变更必须先经 [plan-first](./plan-first-implementation.md) 确认；commit 信息**不**替代方案确认。
- ADR / rule 落盘前已经走过 plan-first，commit 阶段直接按本规则写信息即可。

## 正例

```text
docs(adr): add ADR-018 backend architecture reference

- Reference EquinoxProject as DDD baseline
- Decide MediatR v12 and dawning-style IUnitOfWork
- Add 11 NetArchTest assertions
```

```text
chore(scaffold): step 0 repository root configuration

- Add .editorconfig / .gitignore
- Pin .NET SDK 10.0.107 via global.json
- Create empty Dawning.AgentOS.slnx
```

```text
fix(docs): clarify language rules for entity pages
```

## 反例

- `feat: Add new ADRs and update existing ones for agent design principles`：type 错（应为 `docs`）；一次塞 5 个 ADR；subject 大写；超长。
- `Refactor SCHEMA.md: Update structure...`：缺 type 前缀；主题行 200+ 字符；无 body。
- `Remove outdated documents: deleted "MAF..." 和 "Pregel..."`：缺 type；中文与英文混用。

## 落地动作

- 历史 commit **不**改写。
- 本规则自落盘日起对新增 commit 生效。
- 违规由 reviewer 在 PR / 自审阶段拦截；后续可加 commitlint 工具自动校验。

## 相关页面

- [Rule 实现前必须方案先行](./plan-first-implementation.md)：commit 之前的方案约束。
- [ADR-017 工程骨架 V0](../adrs/engineering-skeleton-v0.md)：scope `scaffold` 的来源。
- [ADR-018 后端架构参考 Equinox](../adrs/backend-architecture-equinox-reference.md)：scope `domain-core / domain / ...` 的来源。
- [pages/hubs/agent-os.md](../hubs/agent-os.md)：root hub。
