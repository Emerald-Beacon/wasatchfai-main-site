#!/usr/bin/env python3
"""
Regenerate sitemap.xml from what is actually on disk.

The previous sitemap stamped all 174 URLs with an identical lastmod
(2026-07-14). Uniform dates carry no information and search engines largely
discount them. This uses each file's real git commit date where available and
falls back to filesystem mtime.

Excludes 404.html and any page carrying a noindex meta tag.
Run from the repo root.
"""
import pathlib
import re
import subprocess
import datetime

ROOT = pathlib.Path(__file__).parent
BASE = "https://www.wasatchfai.com"

# Priority tiers. These are hints, not commands -- kept coarse on purpose.
PRIORITY = [
    (lambda u: u == "", "1.0"),                                    # homepage
    # post/ is tested FIRST and the city rule is anchored to root-level files.
    # Without both guards, post/heel-pain-in-winter-...-in-utah.html matched
    # endswith("-utah.html") and was promoted to 0.9 alongside the city pages.
    (lambda u: u.startswith("post/"), "0.6"),
    (lambda u: u in {"locations.html", "services.html", "staff.html",
                     "book-appointment.html", "blog.html"}, "0.9"),
    (lambda u: "/" not in u and (u.endswith("-utah.html")
                                 or u == "ogden-utah-foot-doctor.html"), "0.9"),
    (lambda u: True, "0.8"),
]

CHANGEFREQ = [
    (lambda u: u == "" or u == "blog.html", "weekly"),
    (lambda u: u.startswith("post/"), "yearly"),
    (lambda u: True, "monthly"),
]

EXCLUDE = {"404.html"}


def pick(rules, url):
    for test, val in rules:
        if test(url):
            return val


def lastmod(path):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True, timeout=15,
        )
        d = out.stdout.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
            return d
    except Exception:
        pass
    ts = path.stat().st_mtime
    return datetime.date.fromtimestamp(ts).isoformat()


def is_noindex(path):
    s = path.read_text(encoding="utf-8", errors="ignore")
    return bool(re.search(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', s, re.I))


def main():
    files = sorted(ROOT.glob("*.html")) + sorted(ROOT.glob("post/*.html")) \
        + sorted(ROOT.glob("heel-pain-procedure/*.html"))
    urls = []
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        if rel in EXCLUDE or is_noindex(f):
            continue
        # Extensionless URLs are canonical since build-extensionless.py ran;
        # the .html forms 301 here, so the sitemap must list the targets.
        if rel == "index.html":
            loc, key = f"{BASE}/", ""
        elif rel.endswith("/index.html"):
            loc = f"{BASE}/{rel[:-len('index.html')]}"
            key = rel
        else:
            loc, key = f"{BASE}/{rel[:-len('.html')]}", rel
        urls.append((loc, lastmod(f), pick(CHANGEFREQ, key), pick(PRIORITY, key)))

    urls.sort(key=lambda u: (u[3] != "1.0", u[0]))

    body = "\n".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lm}</lastmod>\n"
        f"    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
        for loc, lm, cf, pr in urls)

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{body}\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")

    dates = {u[1] for u in urls}
    print(f"wrote sitemap.xml -- {len(urls)} URLs, {len(dates)} distinct lastmod dates")
    for pr in ("1.0", "0.9", "0.8", "0.6"):
        n = sum(1 for u in urls if u[3] == pr)
        if n:
            print(f"   priority {pr}: {n}")


if __name__ == "__main__":
    main()
