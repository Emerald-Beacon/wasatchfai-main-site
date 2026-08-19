#!/usr/bin/env python3
"""
Regenerate the blog index's ItemList schema from the cards actually on the page.

WHY THIS EXISTS: blog.html carries the article list TWICE -- once as visible
`related-card` anchors inside each cluster's `related-grid`, and once as a
`Blog > mainEntity > ItemList` in the JSON-LD. The autonomous publisher adds a
card for each new post but the ItemList is a flat, globally slug-sorted,
contiguously-numbered array: inserting one entry renumbers every entry after it
(a new post at position 54 shifts 70 others). That is not a safe hand-edit, and
the first automated run duly added the card and left the ItemList at 123 while
the grid went to 124 -- the page's own structured data contradicting the page.

This derives the ItemList from the grid, so the two can no longer disagree.
The grid is the source of truth; the schema is generated.

Idempotent -- rewrites the managed array in place, changing nothing else.
Run from the repo root:  python3 build-blog-schema.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
BASE = "https://wasatchfai.com"
PAGE = ROOT / "blog.html"
INDENT = " " * 12

# The visible cards. These are the truth.
CARD = re.compile(
    r'<a href="post/(?P<slug>[^"]+)" class="related-card"><h3>(?P<title>.*?)</h3>'
)


def unescape(s):
    """The cards carry HTML entities; JSON-LD wants the plain characters."""
    return (s.replace("&amp;", "&").replace("&lt;", "<")
             .replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'"))


def main():
    html = PAGE.read_text()

    cards = [(m.group("slug"), unescape(m.group("title")))
             for m in CARD.finditer(html)]
    if not cards:
        sys.exit("build-blog-schema.py: found no article cards in blog.html -- refusing to write")

    dupes = {s for s, _ in cards if [x for x, _ in cards].count(s) > 1}
    if dupes:
        sys.exit(f"build-blog-schema.py: duplicate cards in blog.html: {sorted(dupes)}")

    # Globally slug-sorted, matching the ordering the list already used.
    cards.sort(key=lambda c: c[0])

    lines = []
    for i, (slug, title) in enumerate(cards, start=1):
        entry = {"@type": "ListItem", "position": i,
                 "url": f"{BASE}/post/{slug}", "name": title}
        # Compact one-entry-per-line form, matching the existing file.
        body = ", ".join(f'"{k}": {json.dumps(v, ensure_ascii=False)}'
                         for k, v in entry.items())
        lines.append(f"{INDENT}{{ {body} }}")
    array = ",\n".join(lines)

    # Replace numberOfItems and the managed array, and nothing else.
    new, n = re.subn(r'("numberOfItems":\s*)\d+', rf'\g<1>{len(cards)}', html, count=1)
    if n != 1:
        sys.exit("build-blog-schema.py: could not locate numberOfItems")

    pat = re.compile(
        r'("@type":\s*"ItemList",.*?"itemListElement":\s*\[\n).*?(\n\s*\])',
        re.S)
    new, n = pat.subn(lambda m: m.group(1) + array + m.group(2), new, count=1)
    if n != 1:
        sys.exit("build-blog-schema.py: could not locate the ItemList array")

    # Prove we emitted parseable JSON-LD before touching the file.
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                            new, re.S):
        json.loads(block)

    if new == html:
        print(f"blog.html ItemList already in sync ({len(cards)} articles)")
        return
    PAGE.write_text(new)
    print(f"blog.html ItemList regenerated -- {len(cards)} articles")


if __name__ == "__main__":
    main()
