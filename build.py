#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SLATE 文档站生成器 · 零依赖（只用 Python 标准库）

把 content/<lang>/*.md 渲染成 docs/ 下的双语静态站：EN 在站点根、ZH 在 /zh/，
两套树共用一个 assets/。左侧分组导航、面包屑、右侧本页目录、客户端搜索、明暗主题、
语言切换、代码复制、翻页。产物可直接部署到 GitHub Pages。

双语是**硬约束**：文件名两侧必须一一对应，order 必须相同，缺任一侧就报错不出站。

用法：
    python build.py             # 生成到 docs/
    python build.py --check     # 只校验 frontmatter、配对、站内链接与锚点，不写文件
    python build.py --clean     # 生成前清空输出目录
    python build.py --out site  # 换输出目录
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
THEME_DIR = ROOT / "theme"
DEFAULT_OUT = ROOT / "docs"

# EN 在站点根、ZH 在 /zh/ —— 与 SLATE Teams 文档站同一摆法
LANGS = ("en", "zh")
PREFIX = {"en": "./", "zh": "../"}          # 从这一层的页面回到站点根
TWIN_DIR = {"en": "zh/", "zh": ""}          # 切到对侧语言要去哪

STRINGS = {
    "zh": {
        "html_lang": "zh-CN",
        "site": "SLATE 文档",
        "docs": "文档",
        "toc": "本页目录",
        "toc_empty": "这页没有小节",
        "prev": "上一篇",
        "next": "下一篇",
        "copy": "复制",
        "copied": "已复制",
        "section": "文档",
        "search": "搜索文档",
        "search_hint": "搜索文档…",
        "no_result": "没有匹配的内容，换个关键词试试",
        "results": "条结果",
        "footer": "SLATE（砚）· 本地 AI 协作调度台",
        "license": "MIT License · 文档随产品演进",
        "skip": "跳到正文",
        "menu": "打开导航",
        "theme": "切换明暗主题",
        "nav": "文档导航",
        "crumbs": "面包屑",
        "pager": "翻页",
        "kbd_move": "↑ ↓ 选择",
        "kbd_open": "Enter 打开",
        "kbd_close": "Esc 关闭",
        "home_site": "官网",
        "guide": "使用教程",
        "alt_label": "English",
        "alt_title": "阅读英文版",
        "badge": "SLATE 文档 · 共 {n} 篇",
        "hero": "把灵感研磨成<br>结构化方案",
        "lede": ("SLATE（砚）是跑在你自己机器上的 AI 协作调度台：多模型对话、Agent 自动执行、"
                 "工具调用、团队辩论、白板逻辑链，把零散想法整理成可以直接交付的方案与提示词。"),
        "cta": ("从认识 SLATE 开始", "安装与启动", "常见问题"),
    },
    "en": {
        "html_lang": "en",
        "site": "SLATE Docs",
        "docs": "Docs",
        "toc": "On this page",
        "toc_empty": "No sections on this page",
        "prev": "Previous",
        "next": "Next",
        "copy": "Copy",
        "copied": "Copied",
        "section": "Docs",
        "search": "Search docs",
        "search_hint": "Search docs…",
        "no_result": "No matching content — try another keyword",
        "results": "results",
        "footer": "SLATE · a local AI orchestration desk",
        "license": "MIT License · docs evolve with the product",
        "skip": "Skip to content",
        "menu": "Open navigation",
        "theme": "Toggle theme",
        "nav": "Documentation navigation",
        "crumbs": "Breadcrumbs",
        "pager": "Pagination",
        "kbd_move": "↑ ↓ move",
        "kbd_open": "Enter open",
        "kbd_close": "Esc close",
        "home_site": "Home site",
        "guide": "Tutorial",
        "alt_label": "中文",
        "alt_title": "Read in Chinese",
        "badge": "SLATE docs · {n} chapters",
        "hero": "Grind inspiration<br>into structured plans",
        "lede": ("SLATE is an AI orchestration desk that runs on your own machine: multi-model chat, "
                 "autonomous agents, tool calls, team debates and whiteboard logic chains, turning "
                 "scattered ideas into plans and prompts you can hand off."),
        "cta": ("Start with SLATE", "Install & launch", "FAQ"),
    },
}

SITE_HOME = "https://slate-ai.site/"
SITE_GUIDE = "https://slate-ai.site/guide.html"

try:  # Windows 控制台默认 GBK，中文与 ✓ 会直接抛 UnicodeEncodeError
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

CALLOUT_ICONS = {
    "note": '<circle cx="10" cy="10" r="7.2"/><path d="M10 9v4.6M10 6.6v.1"/>',
    "tip": '<circle cx="10" cy="10" r="7.2"/><path d="M10 13.4V9M10 6.6v.6"/><path d="M7.6 12.4h4.8"/>',
    "warning": '<path d="M10 3.4 17.4 16.6H2.6Z"/><path d="M10 8.2v3.4M10 14v.1"/>',
    "danger": '<circle cx="10" cy="10" r="7.2"/><path d="M10 6.4v4.2M10 13.4v.2"/>',
}
CALLOUT_LABELS = {
    "zh": {"note": "说明", "tip": "提示", "warning": "注意", "danger": "警告"},
    "en": {"note": "Note", "tip": "Tip", "warning": "Warning", "danger": "Danger"},
}

LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FENCE_RE = re.compile(r"^\s*```+\s*([A-Za-z0-9_+#.-]*)\s*$")
DIRECTIVE_RE = re.compile(r"^:::(\w+)\s*(.*)$")
FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.S)


# ── frontmatter ────────────────────────────────────────────────

def split_front(text: str) -> tuple[dict, str]:
    m = FRONT_RE.match(text)
    if not m:
        return {}, text
    meta: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, text[m.end():]


def plain_text(md: str) -> str:
    s = re.sub(r"```.*?```", " ", md, flags=re.S)
    s = re.sub(r"^:::.*$", " ", s, flags=re.M)
    s = re.sub(r"^\s{0,3}#{1,6}\s*", " ", s, flags=re.M)
    s = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_`>|]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# ── 行内渲染 ───────────────────────────────────────────────────

def slugify(text: str, used: dict[str, int]) -> str:
    plain = re.sub(r"<[^>]+>", "", text)
    slug = re.sub(r"\s+", "-", plain.strip().lower())
    slug = re.sub(r"[^\w\u4e00-\u9fff-]", "", slug)
    slug = slug.strip("-") or "section"
    if slug in used:
        used[slug] += 1
        slug = f"{slug}-{used[slug]}"
    else:
        used[slug] = 0
    return slug


def map_href(href: str) -> tuple[str, bool]:
    """把 Markdown 源链接改写成站点链接；返回 (href, 是否外链)。"""
    if re.match(r"^(https?:|mailto:|tel:)", href):
        return href, True
    if href.startswith("#"):
        return href, False
    base, sep, frag = href.partition("#")
    if base.endswith(".md"):
        base = base[:-3] + ".html"
    elif base.endswith("/"):
        base += "index.html"
    elif not base:
        base = ""
    return base + (sep + frag if sep else ""), False


def render_inline(text: str) -> str:
    codes: list[str] = []

    def stash(m: re.Match) -> str:
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    out = html.escape(text, quote=False)

    def img(m: re.Match) -> str:
        alt = html.escape(m.group(1), quote=True)
        src = html.escape(map_href(m.group(2))[0], quote=True)
        return f'<img src="{src}" alt="{alt}" loading="lazy">'

    def link(m: re.Match) -> str:
        label = m.group(1)
        href, external = map_href(m.group(2).strip())
        attrs = ' target="_blank" rel="noopener"' if external else ""
        return f'<a href="{html.escape(href, quote=True)}"{attrs}>{label}</a>'

    out = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", img, out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", out)
    out = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", out)

    for i, code in enumerate(codes):
        out = out.replace(f"\x00{i}\x00", f"<code>{html.escape(code, quote=False)}</code>")
    return out


# ── 块级渲染 ───────────────────────────────────────────────────

def render_code_block(code_lang: str, body: str, ui: dict) -> str:
    label = code_lang or "text"
    return (
        '<div class="code-block">'
        f'<div class="code-head"><span class="code-lang">{html.escape(label)}</span>'
        f'<button class="code-copy" type="button" data-copy data-copied="{ui["copied"]}">'
        f'{html.escape(ui["copy"])}</button></div>'
        f'<pre><code class="language-{html.escape(label)}">{html.escape(body, quote=False)}</code></pre>'
        "</div>"
    )


def render_callout(kind: str, title: str, inner: str, ui_lang: str) -> str:
    labels = CALLOUT_LABELS[ui_lang]
    kind = kind if kind in labels else "note"
    head = title or labels[kind]
    return (
        f'<div class="callout callout-{kind}">'
        f'<div class="callout-head"><svg viewBox="0 0 20 20" aria-hidden="true">{CALLOUT_ICONS[kind]}</svg>'
        f"<span>{render_inline(head)}</span></div>"
        f'<div class="callout-body">{inner}</div>'
        "</div>"
    )


def split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def cell_attr(aligns: list[str], i: int) -> str:
    if i < len(aligns) and aligns[i]:
        return f' style="text-align:{aligns[i]}"'
    return ""


def render_table(rows: list[list[str]], aligns: list[str]) -> str:
    head, *body = rows
    ths = "".join(f"<th{cell_attr(aligns, i)}>{render_inline(c)}</th>" for i, c in enumerate(head))
    trs = []
    for row in body:
        tds = "".join(f"<td{cell_attr(aligns, i)}>{render_inline(c)}</td>" for i, c in enumerate(row))
        trs.append(f"<tr>{tds}</tr>")
    return f'<div class="table-wrap"><table><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'


def parse_list_block(lines: list[str], start: int) -> tuple[list[str], int]:
    block: list[str] = []
    i = start
    while i < len(lines):
        raw = lines[i]
        if not raw.strip():
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and LIST_RE.match(lines[j]):
                i = j
                continue
            break
        if LIST_RE.match(raw) or raw.startswith(("  ", "\t")):
            block.append(raw)
            i += 1
        else:
            break
    return block, i


def build_list_tree(block: list[str]) -> list[dict]:
    root: dict = {"children": []}
    stack: list[tuple[int, dict]] = [(-1, root)]
    last: dict | None = None
    for raw in block:
        if not raw.strip():
            continue
        m = LIST_RE.match(raw)
        if m:
            indent = len(m.group(1).expandtabs(4))
            node = {"ordered": m.group(2)[0].isdigit(), "text": [m.group(3)], "children": []}
            while len(stack) > 1 and indent <= stack[-1][0]:
                stack.pop()
            stack[-1][1]["children"].append(node)
            stack.append((indent, node))
            last = node
        elif last is not None:
            last["text"].append(raw.strip())
            last["text"].append("")
    for node in root["children"]:
        node.setdefault("children", [])
    return root["children"]


def render_list_nodes(nodes: list[dict]) -> str:
    out: list[str] = []
    i = 0
    while i < len(nodes):
        ordered = nodes[i]["ordered"]
        group = []
        while i < len(nodes) and nodes[i]["ordered"] == ordered:
            group.append(nodes[i])
            i += 1
        items = []
        for node in group:
            text = " ".join([p for p in node["text"] if p]).strip()
            inner = render_inline(text)
            if node.get("children"):
                inner += render_list_nodes(node["children"])
            items.append(f"<li>{inner}</li>")
        tag = "ol" if ordered else "ul"
        out.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
    return "".join(out)


def is_table_start(lines: list[str], i: int) -> bool:
    if i + 1 >= len(lines) or "|" not in lines[i]:
        return False
    nxt = lines[i + 1].strip()
    return bool(re.match(r"^\|?[\s:\-|]+\|[\s:\-|]*$", nxt)) and "-" in nxt


def render_blocks(lines: list[str], toc: list[dict] | None, used_ids: dict[str, int],
                  ui: dict, ui_lang: str) -> str:
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        raw = lines[i]
        stripped = raw.strip()

        if not stripped:
            i += 1
            continue

        fence = FENCE_RE.match(raw)
        if fence:
            lang = fence.group(1)
            i += 1
            buf = []
            while i < n and not FENCE_RE.match(lines[i]):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append(render_code_block(lang, "\n".join(buf), ui))
            continue

        directive = DIRECTIVE_RE.match(stripped)
        if directive:
            kind = directive.group(1).lower()
            title = directive.group(2).strip()
            i += 1
            buf = []
            while i < n and lines[i].strip() != ":::":
                buf.append(lines[i])
                i += 1
            i += 1
            inner = render_blocks(buf, None, used_ids, ui, ui_lang)
            out.append(render_callout(kind, title, inner, ui_lang))
            continue

        head = HEAD_RE.match(stripped)
        if head:
            level = len(head.group(1))
            text = head.group(2).strip()
            hid = slugify(text, used_ids)
            if toc is not None and 2 <= level <= 3:
                toc.append({"id": hid, "text": re.sub(r"<[^>]+>", "", text), "level": level})
            cls = ' class="doc-title"' if level == 1 else ""
            out.append(
                f'<h{level} id="{hid}"{cls}>'
                f'<a class="anchor" href="#{hid}" aria-hidden="true">#</a>{render_inline(text)}</h{level}>'
            )
            i += 1
            continue

        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            out.append("<hr>")
            i += 1
            continue

        if is_table_start(lines, i):
            rows = [split_row(lines[i])]
            aligns = []
            for cell in split_row(lines[i + 1]):
                left, right = cell.startswith(":"), cell.endswith(":")
                aligns.append("center" if left and right else "right" if right else "left" if left else "")
            i += 2
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1
            width = max(len(r) for r in rows)
            rows = [r + [""] * (width - len(r)) for r in rows]
            out.append(render_table(rows, aligns))
            continue

        if LIST_RE.match(raw):
            block, i = parse_list_block(lines, i)
            out.append(render_list_nodes(build_list_tree(block)))
            continue

        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append(f"<blockquote>{render_blocks(buf, None, used_ids, ui, ui_lang)}</blockquote>")
            continue

        buf = []
        while i < n:
            cur = lines[i]
            if not cur.strip():
                break
            if FENCE_RE.match(cur) or HEAD_RE.match(cur.strip()) or LIST_RE.match(cur):
                break
            if DIRECTIVE_RE.match(cur.strip()) or cur.strip().startswith(">"):
                break
            if re.match(r"^(-{3,}|\*{3,}|_{3,})$", cur.strip()) or is_table_start(lines, i):
                break
            buf.append(cur.strip())
            i += 1
        if buf:
            out.append(f"<p>{render_inline(' '.join(buf))}</p>")

    return "\n".join(out)


# ── 站点装配 ───────────────────────────────────────────────────

class Page:
    def __init__(self, meta: dict, body: str, source: Path, lang: str):
        self.source = source
        self.lang = lang
        self.ui = STRINGS[lang]
        self.slug = source.stem
        self.key = f"{lang}/{source.stem}"
        self.title = meta.get("title") or self.slug
        self.description = meta.get("description", "")
        self.section = meta.get("section", self.ui["section"])
        try:
            self.order = int(meta.get("order", "999"))
        except ValueError:
            self.order = 999
        self.toc: list[dict] = []
        self.content = render_blocks(body.splitlines(), self.toc, {}, self.ui, lang)
        self.text = plain_text(body)
        self.href = f"./{self.slug}.html"
        self.warnings: list[str] = []

    @property
    def twin(self) -> str:
        """切语言要去的那一页：EN 在根、ZH 在 /zh/，同文件名。"""
        return f"{PREFIX[self.lang]}{TWIN_DIR[self.lang]}{self.slug}.html"


def load_pages() -> list[Page]:
    pages: list[Page] = []
    for lang in LANGS:
        for path in sorted((CONTENT_DIR / lang).glob("*.md")):
            meta, body = split_front(path.read_text(encoding="utf-8"))
            page = Page(meta, body, path, lang)
            if not meta:
                page.warnings.append(f"{path.parent.name}/{path.name}: 缺少 frontmatter")
            for key in ("title", "description", "section", "order"):
                if not meta.get(key):
                    page.warnings.append(f"{path.parent.name}/{path.name}: frontmatter 缺少 {key}")
            pages.append(page)
    pages.sort(key=lambda p: (p.lang, p.order, p.slug))
    return pages


def check_pairs(pages: list[Page]) -> list[str]:
    """双语是硬约束：文件名一一对应，order 相同。"""
    problems: list[str] = []
    by_lang: dict[str, dict[str, Page]] = {lang: {} for lang in LANGS}
    for page in pages:
        by_lang[page.lang][page.slug] = page
    for slug in sorted(set(by_lang["en"]) | set(by_lang["zh"])):
        en, zh = by_lang["en"].get(slug), by_lang["zh"].get(slug)
        if en is None or zh is None:
            missing = "en" if en is None else "zh"
            problems.append(f"{slug}.md 缺 {missing} 侧（双语必须成对）")
            continue
        if en.order != zh.order:
            problems.append(f"{slug}.md 两侧 order 不一致：en={en.order} / zh={zh.order}")
    return problems


def tree(pages: list[Page], lang: str) -> list[Page]:
    return [p for p in pages if p.lang == lang]


def build_sidebar(pages: list[Page], current: Page | None) -> str:
    groups: list[tuple[str, list[Page]]] = []
    for page in pages:
        if groups and groups[-1][0] == page.section:
            groups[-1][1].append(page)
        else:
            groups.append((page.section, [page]))

    chunks = []
    for name, items in groups:
        links = []
        for page in items:
            active = " active" if current and page.slug == current.slug else ""
            links.append(f'<li><a class="nav-link{active}" href="{page.href}">{html.escape(page.title)}</a></li>')
        chunks.append(
            '<div class="nav-group">'
            f'<div class="nav-group-title">{html.escape(name)}</div>'
            f'<ul class="nav-list">{"".join(links)}</ul>'
            "</div>"
        )
    return "".join(chunks)


def build_breadcrumbs(page: Page) -> str:
    return (
        '<a href="./index.html">' + html.escape(page.ui["docs"]) + "</a>"
        '<span class="sep">/</span>'
        f'<span>{html.escape(page.section)}</span>'
        '<span class="sep">/</span>'
        f'<span class="current">{html.escape(page.title)}</span>'
    )


def build_toc(page: Page) -> str:
    ui = page.ui
    if not page.toc:
        return f'<div class="toc-title">{ui["toc"]}</div><div class="toc-empty">{ui["toc_empty"]}</div>'
    items = "".join(
        f'<li class="lv{row["level"]}"><a href="#{row["id"]}">{html.escape(row["text"])}</a></li>'
        for row in page.toc
    )
    return f'<div class="toc-title">{ui["toc"]}</div><ul class="toc-list">{items}</ul>'


def build_pager(index: int, pages: list[Page], ui: dict) -> str:
    prev_page = pages[index - 1] if index > 0 else None
    next_page = pages[index + 1] if index + 1 < len(pages) else None

    def cell(page: Page | None, direction: str) -> str:
        if not page:
            return '<span class="empty"></span>'
        label = ui["prev"] if direction == "prev" else ui["next"]
        return (
            f'<a class="{direction}" href="{page.href}">'
            f'<span class="dir">{label}</span>'
            f'<span class="ttl">{html.escape(page.title)}</span></a>'
        )

    return cell(prev_page, "prev") + cell(next_page, "next")


def build_home(pages: list[Page], lang: str) -> str:
    ui = STRINGS[lang]
    groups: list[tuple[str, list[Page]]] = []
    for page in pages:
        if groups and groups[-1][0] == page.section:
            groups[-1][1].append(page)
        else:
            groups.append((page.section, [page]))

    blocks = []
    for name, items in groups:
        cards = "".join(
            f'<a class="card" href="{page.href}">'
            f'<span class="c-index">{page.order:02d}</span>'
            f'<span class="c-title">{html.escape(page.title)}</span>'
            f'<span class="c-desc">{html.escape(page.description)}</span></a>'
            for page in items
        )
        blocks.append(
            f'<section class="home-section"><h2>{html.escape(name)}</h2>'
            f'<div class="card-grid">{cards}</div></section>'
        )

    first, second, third = ui["cta"]
    template = (THEME_DIR / "home.html").read_text(encoding="utf-8")
    filled = {
        "{{BADGE}}": ui["badge"].format(n=len(pages)),
        "{{HERO_TITLE}}": ui["hero"],
        "{{LEDE}}": html.escape(ui["lede"], quote=False),
        "{{HREF_1}}": pages[0].href if pages else "#",
        "{{HREF_2}}": next((p.href for p in pages if p.slug.startswith("02")), "./index.html"),
        "{{HREF_3}}": next((p.href for p in pages if p.slug.startswith("20")), "./index.html"),
        "{{CTA_1}}": html.escape(first),
        "{{CTA_2}}": html.escape(second),
        "{{CTA_3}}": html.escape(third),
        "{{CARDS}}": "".join(blocks),
    }
    for key, value in filled.items():
        template = template.replace(key, value)
    return template


def search_index_js(pages: list[Page]) -> str:
    """一次出两套索引；页面自己带 data-root，docs.js 负责拼回站点根。"""
    data = {
        lang: [
            {
                "t": page.title,
                "u": f"{'' if lang == 'en' else 'zh/'}{page.slug}.html",
                "s": page.section,
                "h": [row["text"] for row in page.toc],
                "x": page.text,
            }
            for page in tree(pages, lang)
        ]
        for lang in LANGS
    }
    return ("window.SLATE_DOCS_INDEX = "
            + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")


def check_links(pages: list[Page]) -> list[str]:
    known = {page.key: page for page in pages}
    problems = []
    pattern = re.compile(r"\]\(([^)\s]+\.md)(#[^)\s]*)?\)")
    for page in pages:
        body = page.source.read_text(encoding="utf-8")
        for match in pattern.finditer(body):
            target = match.group(1)
            name = Path(target).name
            stem = Path(target).stem
            if f"{page.lang}/{stem}" not in known:
                problems.append(f"{page.lang}/{page.source.name} → 链接指向不存在的页面：{target}")
                continue
            anchor = (match.group(2) or "").lstrip("#")
            if anchor:
                target_page = known[f"{page.lang}/{stem}"]
                ids = {row["id"] for row in target_page.toc}
                if anchor not in ids:
                    problems.append(
                        f"{page.lang}/{page.source.name} → 锚点不存在：{name}#{anchor}（{target_page.title}）"
                    )
    return problems


def fill(template: str, ui: dict, extra: dict) -> str:
    out = template
    for key, value in extra.items():
        out = out.replace(key, value)
    for key, value in ui.items():
        if isinstance(value, str):
            out = out.replace("{{T_" + key.upper() + "}}", html.escape(value))
    return out


def render_site(pages: list[Page], out_dir: Path) -> int:
    layout = (THEME_DIR / "layout.html").read_text(encoding="utf-8")
    icon_src = THEME_DIR / "icon.png"
    assets_dir = out_dir / "assets"

    out_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(THEME_DIR / "docs.css", assets_dir / "docs.css")
    shutil.copy2(THEME_DIR / "docs.js", assets_dir / "docs.js")
    (assets_dir / "search-index.js").write_text(search_index_js(pages), encoding="utf-8", newline="\n")
    if icon_src.exists():
        shutil.copy2(icon_src, assets_dir / "icon.png")
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")
    # CNAME 是仓库根的受跟踪文件，产物目录要被它带着走——--clean 会连它一起删掉
    cname = ROOT / "CNAME"
    if cname.exists():
        shutil.copy2(cname, out_dir / "CNAME")

    written = 0
    for lang in LANGS:
        ui = STRINGS[lang]
        lang_pages = tree(pages, lang)
        if not lang_pages:
            continue
        sub = Path("zh") if lang == "zh" else Path(".")
        (out_dir / sub).mkdir(parents=True, exist_ok=True)

        def emit(fname: str, page_title: str, description: str, body_attrs: str, sidebar: str,
                 crumbs: str, content: str, pager: str, toc: str, alt_href: str) -> None:
            alt_lang = "zh" if lang == "en" else "en"
            extra = {
                "{{PAGE_TITLE}}": html.escape(page_title, quote=True),
                "{{DESCRIPTION}}": html.escape(description, quote=True),
                "{{ROOT}}": PREFIX[lang],
                "{{LANG}}": lang,
                "{{HTML_LANG}}": ui["html_lang"],
                "{{ALT_HREF}}": alt_href,
                "{{ALT_HREFLANG}}": STRINGS[alt_lang]["html_lang"],
                "{{ALT_LABEL}}": html.escape(ui["alt_label"]),
                "{{ALT_TITLE}}": html.escape(ui["alt_title"], quote=True),
                "{{BODY_ATTRS}}": body_attrs,
                "{{SIDEBAR}}": sidebar,
                "{{BREADCRUMBS}}": crumbs,
                "{{CONTENT}}": content,
                "{{PAGER}}": pager,
                "{{TOC}}": toc,
                "{{SITE_HOME}}": SITE_HOME,
                "{{SITE_GUIDE}}": SITE_GUIDE,
            }
            (out_dir / sub / fname).write_text(fill(layout, ui, extra), encoding="utf-8", newline="\n")

        for index, page in enumerate(lang_pages):
            heading = f'<h1 class="doc-title" id="top">{render_inline(page.title)}</h1>'
            emit(
                f"{page.slug}.html",
                f"{page.title} · {ui['site']}",
                page.description,
                f'data-page="{page.slug}"',
                build_sidebar(lang_pages, page),
                build_breadcrumbs(page),
                heading + "\n" + page.content,
                build_pager(index, lang_pages, ui),
                build_toc(page),
                page.twin,
            )
            written += 1

        emit(
            "index.html",
            ui["site"],
            ui["lede"],
            'data-layout="home"',
            build_sidebar(lang_pages, None),
            "",
            build_home(lang_pages, lang),
            "",
            "",
            "zh/index.html" if lang == "en" else "../index.html",
        )
        written += 1
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 SLATE 双语文档站")
    parser.add_argument("--check", action="store_true", help="只校验，不写文件")
    parser.add_argument("--clean", action="store_true", help="生成前清空输出目录")
    parser.add_argument("--out", default="docs", help="输出目录，默认 docs/（GitHub Pages 认 main 分支的 /docs）")
    args = parser.parse_args()

    missing = [str(CONTENT_DIR / lang) for lang in LANGS if not (CONTENT_DIR / lang).is_dir()]
    if missing:
        print(f"× 找不到内容目录：{'、'.join(missing)}", file=sys.stderr)
        return 1

    pages = load_pages()
    if not pages:
        print("× content/ 下没有 .md 文件", file=sys.stderr)
        return 1

    warnings = [w for page in pages for w in page.warnings]
    problems = check_pairs(pages) + check_links(pages)

    counts = {lang: len(tree(pages, lang)) for lang in LANGS}
    print(f"· 读取 {len(pages)} 个页面（en {counts['en']} · zh {counts['zh']}）")
    for item in warnings:
        print(f"  ! {item}")
    for item in problems:
        print(f"  ! {item}")

    if args.check:
        print("× 校验失败" if (warnings or problems) else "✓ 校验通过")
        return 1 if (warnings or problems) else 0

    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    if args.clean and out_dir.exists():
        shutil.rmtree(out_dir)

    written = render_site(pages, out_dir)
    total_kb = sum(f.stat().st_size for f in out_dir.rglob("*") if f.is_file()) / 1024
    print(f"✓ 生成 {written} 个页面 → {out_dir}（{total_kb:.0f} KB）")
    if warnings or problems:
        print("  有告警，请看上面列出的条目")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
