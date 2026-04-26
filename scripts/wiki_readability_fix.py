#!/usr/bin/env python3
"""Readability scaffolding (idempotent).

For every wiki page (entities/concepts/comparisons/decisions/synthesis/frameworks/readings):

1. **TL;DR** — if no `>` blockquote in the first 15 body lines after H1, insert
   a TODO blockquote stub.
2. **TOC** — if H2 count >= 10 and no existing TOC marker, insert a TOC right
   after TL;DR (auto-generated from H2 headings; ignores headers inside fenced code).
3. **## 交叉引用** — if missing, append at end with a TODO stub.
4. **## 来源** — if missing, append at end. Pre-populates from frontmatter
   `sources` field (block list); falls back to TODO if empty.

Markers (so the script is idempotent):
- `<!-- TLDR-STUB -->`     — TL;DR placeholder
- `<!-- TOC-AUTOGEN -->`   — TOC start, `<!-- /TOC-AUTOGEN -->` end
- `<!-- XREF-STUB -->`     — cross-ref placeholder
- `<!-- SRC-STUB -->`      — source placeholder

Re-running won't duplicate any of these.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("docs")
WIKI_TOPS = {"entities","concepts","comparisons","decisions","synthesis","frameworks","readings"}
SKIP_NAMES = {"README.md","README.zh-CN.md"}  # README pages have their own structure
TOC_THRESHOLD = 10  # H2 count

TLDR_STUB = """> **TL;DR** <!-- TLDR-STUB -->
> - 本页讲：_TODO 一句话_
> - 适合谁读 / 何时来：_TODO_
> - 关键结论：_TODO_
"""

XREF_STUB = """## 交叉引用 <!-- XREF-STUB -->

<!-- TODO 列出 2-5 个最相关的 wiki 页，每个一句话说明为何相关 -->

- [[TODO-相关页面]] — _TODO 为什么相关_
"""

def slugify(text: str) -> str:
    """GitHub-ish anchor for Chinese+English headers."""
    s = text.strip().lower()
    s = re.sub(r"[`*_~]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^\w\u4e00-\u9fff\-]", "", s)
    return s.strip("-")

def split_fm(text: str):
    if not text.startswith("---"):
        return None, "", text
    end = text.find("\n---", 3)
    if end < 0: return None, "", text
    return text[:end+4], text[3:end].strip("\n"), text[end+4:]

def parse_sources_field(fm_block: str):
    """Return list of source strings from frontmatter `sources` (inline or block)."""
    if not fm_block:
        return []
    lines = fm_block.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^sources\s*:\s*(.*)$", line)
        if not m:
            continue
        val = m.group(1).strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            if not inner:
                return []
            return [s.strip().strip('"').strip("'") for s in inner.split(",") if s.strip()]
        # block list
        out = []
        j = i + 1
        while j < len(lines) and lines[j].lstrip().startswith("- "):
            out.append(lines[j].lstrip()[2:].strip().strip('"').strip("'"))
            j += 1
        return out
    return []

def has_marker(body: str, marker: str) -> bool:
    return marker in body

def find_h1_end(lines):
    """Return index after the first H1 line (skipping nothing). -1 if no H1."""
    in_code = False
    for i, l in enumerate(lines):
        if l.startswith("```") or l.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r"^#\s+", l):
            return i
    return -1

def has_existing_summary_blockquote(lines, h1_idx):
    """Check first 20 non-empty lines after H1 for a `>` blockquote."""
    seen = 0
    in_code = False
    for l in lines[h1_idx+1 : h1_idx+25]:
        if l.startswith("```") or l.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        s = l.strip()
        if s.startswith(">"):
            return True
        if s.startswith("#"):
            return False  # next header reached, no summary
        if s != "":
            seen += 1
            if seen > 5:
                return False
    return False

def collect_h2_for_toc(lines):
    """Return list of (text, anchor) for top-level H2s (skip code blocks)."""
    out = []
    in_code = False
    for l in lines:
        if l.startswith("```") or l.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^##\s+(.+?)\s*$", l)
        if m:
            text = m.group(1)
            text_clean = re.sub(r"<!--.*?-->", "", text).strip()
            if text_clean.startswith("交叉引用") or text_clean.startswith("来源"):
                continue  # skip our own scaffolds
            out.append((text_clean, slugify(text_clean)))
    return out

def build_toc(h2_list):
    if not h2_list:
        return ""
    body = ["", "## 目录 <!-- TOC-AUTOGEN -->", ""]
    for text, anchor in h2_list:
        body.append(f"- [{text}](#{anchor})")
    body.append("<!-- /TOC-AUTOGEN -->")
    body.append("")
    return "\n".join(body)

def build_src(sources):
    lines = ["## 来源 <!-- SRC-STUB -->", ""]
    if sources:
        for s in sources:
            if s.startswith("http"):
                lines.append(f"- <{s}>")
            elif s.startswith("raw/") or s.startswith("docs/raw/"):
                # raw path → wikilink to its stem (Obsidian friendly)
                stem = Path(s).stem
                lines.append(f"- [[{s}|{stem}]]")
            elif s.endswith(".md"):
                # likely a wiki page reference — convert to wikilink
                stem = Path(s).stem
                lines.append(f"- [[{s.replace('.md','')}|{stem}]] (交叉引用，非原始来源)")
            else:
                lines.append(f"- {s}")
    else:
        lines.append("<!-- TODO 补充原始来源（raw/ 路径或外链） -->")
        lines.append("- _TODO_")
    return "\n".join(lines)

def process(p: Path):
    text = p.read_text(encoding="utf-8")
    fm_full, fm_block, body = split_fm(text)
    if fm_full is None:
        return False, "no frontmatter (skip)"

    body = body.lstrip("\n")
    lines = body.splitlines()
    actions = []

    # 1. TL;DR
    h1_idx = find_h1_end(lines)
    if h1_idx >= 0 and not has_marker(body, "<!-- TLDR-STUB -->"):
        if not has_existing_summary_blockquote(lines, h1_idx):
            insert_at = h1_idx + 1
            # add a blank line before insertion if needed
            stub = "\n" + TLDR_STUB
            lines.insert(insert_at, stub)
            actions.append("TL;DR")

    # rebuild after potential TL;DR insert
    body = "\n".join(lines)

    # 2. TOC
    h2_list = collect_h2_for_toc(body.splitlines())
    if len(h2_list) >= TOC_THRESHOLD and not has_marker(body, "<!-- TOC-AUTOGEN -->"):
        # find insertion point: after TL;DR block (last `>` line in first 30 lines)
        cur_lines = body.splitlines()
        h1_idx = find_h1_end(cur_lines)
        ins = h1_idx + 1 if h1_idx >= 0 else 0
        # advance through blank + blockquote lines
        i = ins
        seen_blockquote = False
        while i < len(cur_lines) and i < (h1_idx + 30):
            s = cur_lines[i].strip()
            if s.startswith(">"):
                seen_blockquote = True
                i += 1
                continue
            if seen_blockquote and s == "":
                i += 1
                break
            if s.startswith("#"):
                break
            i += 1
        toc_text = build_toc(h2_list).rstrip() + "\n"
        cur_lines.insert(i, toc_text)
        body = "\n".join(cur_lines)
        actions.append(f"TOC ({len(h2_list)} entries)")

    # 3. 交叉引用
    if not has_marker(body, "<!-- XREF-STUB -->"):
        # also accept existing 交叉引用 section (without our marker)
        if not re.search(r"^##+\s+(交叉引用|相关|See also|Related)", body, re.M):
            body = body.rstrip() + "\n\n---\n\n" + XREF_STUB
            actions.append("交叉引用")

    # 4. 来源
    if not has_marker(body, "<!-- SRC-STUB -->"):
        if not re.search(r"^##+\s+(来源|参考|References|Sources)", body, re.M):
            sources = parse_sources_field(fm_block)
            body = body.rstrip() + "\n\n" + build_src(sources) + "\n"
            actions.append(f"来源 ({len(sources)} src)")

    if not actions:
        return False, "already scaffolded"

    new_text = fm_full + "\n\n" + body.lstrip("\n")
    new_text = re.sub(r"\n{4,}", "\n\n\n", new_text)
    if not new_text.endswith("\n"):
        new_text += "\n"
    p.write_text(new_text, encoding="utf-8")
    return True, ", ".join(actions)

def main():
    targets = []
    for p in ROOT.rglob("*.md"):
        if str(p).startswith("docs/raw/"): continue
        rel = p.relative_to(ROOT).parts
        if not rel or rel[0] not in WIKI_TOPS: continue
        if p.name in SKIP_NAMES: continue
        targets.append(p)

    changed = 0
    for p in sorted(targets):
        ok, info = process(p)
        if ok:
            changed += 1
            print(f"[{p}] {info}")
        else:
            print(f"-- [{p}] {info}")
    print(f"\nDone. Scaffolded {changed}/{len(targets)} files.")

if __name__ == "__main__":
    main()
