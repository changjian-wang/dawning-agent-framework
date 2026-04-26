#!/usr/bin/env python3
"""Wiki health-check lint script (read-only).

Usage: python3 scripts/wiki_lint.py
Exits 0 always; failures are reported, not enforced. Used by the wiki-lint SKILL.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("docs")
EXCLUDED = {
    "docs/SCHEMA.md",
    "docs/index.md",
    "docs/log.md",
    "docs/REVIEW_INDEX.zh-CN.md",
    "docs/concepts/README.md",
    "docs/raw/README.md",
}
REQUIRED = ["title", "type", "tags", "sources", "created", "updated", "status"]
VALID_STATUS = {"draft", "active", "stale", "archived"}
VALID_TYPE = {"entity", "concept", "comparison", "decision", "synthesis", "reading"}
WIKI_TOPS = {
    "entities", "concepts", "comparisons", "decisions",
    "synthesis", "frameworks", "readings",
}
ALLOWED_TOP_DIRS = {
    "raw", "entities", "concepts", "comparisons", "decisions",
    "synthesis", "frameworks", "readings", "images",
}
README_NAMES = {"README.md", "README.zh-CN.md"}


def all_md():
    out = []
    for p in ROOT.rglob("*.md"):
        if str(p).startswith("docs/raw/"):
            continue
        out.append(p)
    return out


def parse_fm(p):
    try:
        txt = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    if not txt.startswith("---"):
        return {"_missing_block": True}
    end = txt.find("\n---", 3)
    if end < 0:
        return {"_missing_block": True}
    block = txt[3:end].strip()
    fm = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def wikilinks(text):
    """Yield wikilink targets, treating both `|` and `\\|` as aliases."""
    # Normalize `\|` -> `|` so escaped pipes in markdown tables don't break alias parsing.
    norm = text.replace(r"\|", "|")
    for m in re.finditer(r"\[\[([^\]\|]+)(\|[^\]]*)?\]\]", norm):
        yield m.group(1).strip()


def main():
    wiki_files = []
    fm_problems = []
    for p in all_md():
        s = str(p)
        if s in EXCLUDED:
            continue
        rel_parts = p.relative_to(ROOT).parts
        if not rel_parts or rel_parts[0] not in WIKI_TOPS:
            continue
        if p.name in README_NAMES:
            # README is whitelisted but still needs frontmatter
            pass
        wiki_files.append(p)
        fm = parse_fm(p)
        if fm is None:
            fm_problems.append((s, "读取失败"))
            continue
        if fm.get("_missing_block"):
            fm_problems.append((s, "无 frontmatter 块"))
            continue
        missing = [k for k in REQUIRED if k not in fm]
        if missing:
            fm_problems.append((s, f"缺字段: {','.join(missing)}"))
        if "status" in fm and fm["status"] not in VALID_STATUS:
            fm_problems.append((s, f"非法 status: {fm['status']}"))
        if "type" in fm and fm["type"] not in VALID_TYPE:
            fm_problems.append((s, f"非法 type: {fm['type']}"))

    print("=" * 60)
    print("1) FRONTMATTER")
    print("=" * 60)
    print(f"扫描 wiki 页: {len(wiki_files)}  问题数: {len(fm_problems)}")
    for s, r in fm_problems:
        print(f"  - {s} :: {r}")

    # Orphan detection
    print("\n" + "=" * 60)
    print("2) ORPHANS")
    print("=" * 60)
    all_files = [p for p in all_md() if str(p) not in EXCLUDED]
    name_map = {}
    for p in all_files:
        name_map.setdefault(p.stem, []).append(p)
    incoming = {str(p): 0 for p in all_files}
    for p in ROOT.rglob("*.md"):
        if str(p).startswith("docs/raw/"):
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for target in wikilinks(txt):
            leaf = target.split("/")[-1].replace(".md", "")
            for cand_stem, paths in name_map.items():
                if cand_stem == leaf:
                    for cp in paths:
                        if cp != p:
                            incoming[str(cp)] = incoming.get(str(cp), 0) + 1
        for m in re.finditer(r"\]\(([^)]+\.md)(#[^)]*)?\)", txt):
            link = m.group(1)
            try:
                target = (p.parent / link).resolve()
                ws = Path.cwd().resolve()
                rel = str(target.relative_to(ws))
                if rel in incoming and target != p.resolve():
                    incoming[rel] += 1
            except Exception:
                pass
    orphans = sorted(
        s for s, c in incoming.items()
        if c == 0
        and Path(s).parts[1] in WIKI_TOPS
        and Path(s).name not in README_NAMES
    )
    print(f"孤立页数: {len(orphans)}")
    for s in orphans:
        print(f"  - {s}")

    # Stale / archived
    print("\n" + "=" * 60)
    print("3) STALE / ARCHIVED")
    print("=" * 60)
    stales, archived = [], []
    for p in wiki_files:
        fm = parse_fm(p) or {}
        if fm.get("status") == "stale":
            stales.append(str(p))
        if fm.get("status") == "archived":
            archived.append(str(p))
    print(f"stale: {len(stales)}")
    for s in stales:
        print(f"  - {s}")
    print(f"archived: {len(archived)}")
    for s in archived:
        print(f"  - {s}")

    # Index drift
    print("\n" + "=" * 60)
    print("4) INDEX 漂移")
    print("=" * 60)
    idx = Path("docs/index.md").read_text(encoding="utf-8", errors="replace")
    indexed_stems = set()
    for target in wikilinks(idx):
        indexed_stems.add(target.split("/")[-1].replace(".md", ""))
    for m in re.finditer(r"\]\(([^)]+\.md)\)", idx):
        indexed_stems.add(Path(m.group(1)).stem)
    not_in_idx = []
    for p in wiki_files:
        if p.name in README_NAMES:
            continue
        base = p.stem.replace(".zh-CN", "")
        if p.stem in indexed_stems or base in indexed_stems:
            continue
        not_in_idx.append(str(p))
    print(f"未出现在 index.md: {len(not_in_idx)}")
    for s in sorted(not_in_idx):
        print(f"  - {s}")

    # Naming
    print("\n" + "=" * 60)
    print("5) 命名")
    print("=" * 60)
    bad_names = []
    for p in all_files:
        if p.name in README_NAMES:
            continue
        stem = p.stem
        base = stem[:-6] if stem.endswith(".zh-CN") else stem
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", base):
            bad_names.append(str(p))
    print(f"非 kebab-case: {len(bad_names)}")
    for s in bad_names:
        print(f"  - {s}")

    # Bilingual: only flag when SCHEMA-explicit pair is broken — both sides exist but stale.
    # Per SCHEMA 1.1 §7: solo-language presence is legal. So we DON'T flag missing sides.
    print("\n" + "=" * 60)
    print("6) 双语 (SCHEMA 1.1: solo 合法,不强制)")
    print("=" * 60)
    print("跳过 — 解读为单语合法。如需对称版本,显式创建对端文件。")

    # Raw
    print("\n" + "=" * 60)
    print("7) RAW/ 改动")
    print("=" * 60)
    r = subprocess.run(
        ["git", "status", "--short", "docs/raw/"],
        capture_output=True, text=True
    )
    print("git status:", r.stdout.strip() or "(clean)")

    # Top dirs
    print("\n" + "=" * 60)
    print("8) 顶层目录")
    print("=" * 60)
    bad_top = []
    for d in sorted(os.listdir(ROOT)):
        if (ROOT / d).is_dir():
            if d in ALLOWED_TOP_DIRS:
                print(f"  - {d}/")
            else:
                bad_top.append(d)
                print(f"  - {d}/  ⚠ 非 SCHEMA 标准")
    return 0


if __name__ == "__main__":
    sys.exit(main())
