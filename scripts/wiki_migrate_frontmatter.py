#!/usr/bin/env python3
"""One-shot frontmatter migration to SCHEMA 1.1.

Idempotent: safe to re-run. Outputs a summary of changes.

Mappings:
- type=framework-entity     -> type=entity,     subtype=framework
- type=source-analysis      -> type=synthesis,  subtype=internals
- type=intuition            -> type=synthesis,  subtype=intuition
- type=overview             -> type=synthesis,  subtype=overview
- type=index                -> type=synthesis,  subtype=overview
- type=case-index           -> type=synthesis,  subtype=overview
- type=case-study           -> type=synthesis,  subtype=case-study
- type=case-analysis        -> type=synthesis,  subtype=case-study
- type=cross-module-comparison -> type=comparison, subtype=cross-comparison
- type=cross-case-comparison   -> type=comparison, subtype=cross-comparison

Repairs:
- status=maintenance -> status=stale
- missing `updated`  -> set to existing `created`, else today
- missing `sources`  -> set to []
- missing `title`    -> derive from first markdown H1
- no frontmatter at all -> prepend a minimal block (type inferred from path)
"""
from __future__ import annotations

import datetime as _dt
import re
import sys
from pathlib import Path

ROOT = Path("docs")
TODAY = _dt.date.today().isoformat()

TYPE_MAP = {
    "framework-entity": ("entity", "framework"),
    "source-analysis": ("synthesis", "internals"),
    "intuition": ("synthesis", "intuition"),
    "overview": ("synthesis", "overview"),
    "index": ("synthesis", "overview"),
    "case-index": ("synthesis", "overview"),
    "case-study": ("synthesis", "case-study"),
    "case-analysis": ("synthesis", "case-study"),
    "cross-module-comparison": ("comparison", "cross-comparison"),
    "cross-case-comparison": ("comparison", "cross-comparison"),
}

PATH_TYPE_DEFAULTS = {
    "entities": ("entity", None),
    "concepts": ("concept", None),
    "comparisons": ("comparison", None),
    "decisions": ("decision", None),
    "synthesis": ("synthesis", None),
    "readings": ("reading", "chapter"),
    "frameworks": ("synthesis", None),  # framework deep dives
}


def derive_subtype_from_path(path: Path):
    parts = path.parts
    if "tier-1-intuition" in parts:
        return "intuition"
    if "tier-2-architecture" in parts:
        return "architecture"
    if "tier-3-internals" in parts:
        return "internals"
    if "cases" in parts:
        if path.name.startswith("_cross-") or "cross-case" in path.stem:
            return "cross-comparison"
        if path.name in {"README.md", "README.zh-CN.md"}:
            return "overview"
        return "case-study"
    if path.name.startswith("_cross-"):
        return "cross-comparison"
    return None


def split_frontmatter(text: str):
    """Return (fm_block, body) or (None, text) if no fm."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    block = text[3:end].strip("\n")
    body_start = end + len("\n---")
    if body_start < len(text) and text[body_start] == "\n":
        body_start += 1
    return block, text[body_start:]


def parse_block(block: str):
    """Very small YAML parser preserving order. Supports scalar values and inline-list values like `[a, b]`. Nested 'sources:' as block-list parsed separately."""
    items = []  # list of (key, raw_value, original_line) or ("__raw__", text)
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if not m:
            items.append(("__raw__", line))
            i += 1
            continue
        key, val = m.group(1), m.group(2).rstrip()
        # If value is empty AND next lines start with "  - ", collect as list block
        if val == "" and i + 1 < len(lines) and lines[i + 1].lstrip().startswith("- "):
            collected = []
            j = i + 1
            while j < len(lines) and lines[j].lstrip().startswith("- "):
                collected.append(lines[j].lstrip()[2:].strip())
                j += 1
            items.append((key, collected, "__list__"))
            i = j
            continue
        items.append((key, val, "scalar"))
        i += 1
    return items


def serialize_block(items):
    out = []
    for it in items:
        if it[0] == "__raw__":
            out.append(it[1])
            continue
        key, val, kind = it
        if kind == "__list__":
            if not val:
                out.append(f"{key}: []")
            else:
                out.append(f"{key}:")
                for x in val:
                    out.append(f"  - {x}")
        else:
            out.append(f"{key}: {val}")
    return "\n".join(out)


def get_item(items, key):
    for idx, it in enumerate(items):
        if it[0] == key:
            return idx, it
    return -1, None


def set_item(items, key, val, kind="scalar"):
    idx, _ = get_item(items, key)
    if idx >= 0:
        items[idx] = (key, val, kind)
    else:
        items.append((key, val, kind))


def first_h1(body: str):
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def infer_type_from_path(path: Path):
    parts = path.relative_to(ROOT).parts
    if not parts:
        return ("concept", None)
    return PATH_TYPE_DEFAULTS.get(parts[0], ("concept", None))


def migrate(path: Path):
    """Return (changed: bool, reasons: list[str])."""
    text = path.read_text(encoding="utf-8")
    fm_block, body = split_frontmatter(text)
    reasons = []

    if fm_block is None:
        # Build new block
        title = first_h1(body) or path.stem.replace(".zh-CN", "").replace("-", " ").title()
        ty, sub = infer_type_from_path(path)
        sub = sub or derive_subtype_from_path(path)
        items = []
        items.append(("title", title, "scalar"))
        items.append(("type", ty, "scalar"))
        if sub:
            items.append(("subtype", sub, "scalar"))
        items.append(("tags", "[]", "scalar"))
        items.append(("sources", [], "__list__"))
        items.append(("created", TODAY, "scalar"))
        items.append(("updated", TODAY, "scalar"))
        items.append(("status", "active", "scalar"))
        new_block = serialize_block(items)
        new_text = f"---\n{new_block}\n---\n\n{body.lstrip()}"
        path.write_text(new_text, encoding="utf-8")
        reasons.append("prepended new frontmatter block")
        return True, reasons

    items = parse_block(fm_block)
    changed = False

    # 1) type rename
    idx, item = get_item(items, "type")
    if item:
        cur_type = item[1].strip().strip('"').strip("'")
        if cur_type in TYPE_MAP:
            new_type, new_sub = TYPE_MAP[cur_type]
            set_item(items, "type", new_type)
            # set subtype only if not already set
            sub_idx, sub_item = get_item(items, "subtype")
            if sub_item is None:
                set_item(items, "subtype", new_sub)
            reasons.append(f"type {cur_type} -> {new_type}/{new_sub}")
            changed = True

    # 2) status fix
    idx, item = get_item(items, "status")
    if item and item[1].strip().strip('"').strip("'") not in {
        "draft", "active", "stale", "archived"
    }:
        set_item(items, "status", "stale")
        reasons.append(f"status {item[1]} -> stale")
        changed = True

    # 3) Required field defaults
    if get_item(items, "title")[1] is None:
        title = first_h1(body) or path.stem.replace(".zh-CN", "").replace("-", " ").title()
        set_item(items, "title", title)
        reasons.append("added title")
        changed = True

    if get_item(items, "tags")[1] is None:
        set_item(items, "tags", "[]")
        reasons.append("added empty tags")
        changed = True

    if get_item(items, "sources")[1] is None:
        set_item(items, "sources", [], "__list__")
        reasons.append("added empty sources")
        changed = True

    if get_item(items, "created")[1] is None:
        set_item(items, "created", TODAY)
        reasons.append("added created")
        changed = True

    if get_item(items, "updated")[1] is None:
        # use created if available
        ci = get_item(items, "created")[1]
        u = ci[1].strip() if ci else TODAY
        set_item(items, "updated", u or TODAY)
        reasons.append("added updated")
        changed = True

    if get_item(items, "status")[1] is None:
        set_item(items, "status", "active")
        reasons.append("added status=active")
        changed = True

    if not changed:
        return False, reasons

    new_block = serialize_block(items)
    new_text = f"---\n{new_block}\n---\n{body if body.startswith(chr(10)) else chr(10)+body}"
    # Avoid double newline drift
    new_text = re.sub(r"^(---\n.*?\n---)\n+", r"\1\n\n", new_text, count=1, flags=re.S)
    path.write_text(new_text, encoding="utf-8")
    return True, reasons


def main():
    targets = []
    for p in ROOT.rglob("*.md"):
        if str(p).startswith("docs/raw/"):
            continue
        if str(p) in {
            "docs/SCHEMA.md", "docs/index.md", "docs/log.md",
            "docs/REVIEW_INDEX.zh-CN.md", "docs/concepts/README.md",
        }:
            continue
        rel_parts = p.relative_to(ROOT).parts
        if not rel_parts:
            continue
        if rel_parts[0] not in {
            "entities", "concepts", "comparisons", "decisions",
            "synthesis", "frameworks", "readings",
        }:
            continue
        targets.append(p)

    changed_count = 0
    for p in sorted(targets):
        ch, reasons = migrate(p)
        if ch:
            changed_count += 1
            print(f"[{p}] " + "; ".join(reasons))
    print(f"\nDone. Changed {changed_count}/{len(targets)} files.")


if __name__ == "__main__":
    sys.exit(main())
