# Copilot Instructions — Dawning Agent OS

This repo is a product monorepo with an embedded LLM-Wiki under `docs/`. All agent instructions live in [`AGENTS.md`](../AGENTS.md).

Authoritative rules:

- Product direction and wiki scope: [`docs/PURPOSE.md`](../docs/PURPOSE.md)
- Wiki structure: [`docs/SCHEMA.md`](../docs/SCHEMA.md)
- Repository-shape ADR: [`docs/pages/adrs/repository-shape-product-monorepo-with-wiki.md`](../docs/pages/adrs/repository-shape-product-monorepo-with-wiki.md)
- Plan-first rule: [`docs/pages/rules/plan-first-implementation.md`](../docs/pages/rules/plan-first-implementation.md)
- Git commit conventions: [`docs/pages/rules/git-commit-conventions.md`](../docs/pages/rules/git-commit-conventions.md)

Read PURPOSE and SCHEMA before any write operation under `docs/`. For application code outside `docs/`, read PURPOSE and relevant ADRs first, and follow the plan-first rule. Do not duplicate rules here; this file only routes you to the authoritative sources.

