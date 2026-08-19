#!/usr/bin/env python3
"""
Move the site to extensionless URLs (/plantar-fasciitis, not
/plantar-fasciitis.html) and generate the 301s that retire the old ones.

WHY NOW: the site went live on wasatchfai.com today and was noindexed until an
hour before this ran, so almost nothing is in Google's index yet. Changing URLs
is never cheaper than this. It also restores the URL shape the previous Wix site
used -- every archived Wix URL was extensionless -- so legacy inbound links and
any residual ranking signal land on the right page instead of a redirect.

Netlify already serves BOTH forms with a 200, which is duplicate content: every
page is reachable at two URLs. This makes the extensionless form canonical and
301s the .html form to it.

The .html redirects need force (the `!` suffix). Netlify resolves static files
BEFORE consulting redirects, and /foo.html IS a static file, so an unforced rule
would never fire. There is no loop risk: the rule matches only the literal
/foo.html, and /foo is served from foo.html without a redirect.

Idempotent. Run from the repo root:  python3 build-extensionless.py
"""
import glob
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
BASE = "https://wasatchfai.com"

# --------------------------------------------------------------- inventory ---
def pages():
    out = []
    for f in sorted(glob.glob("*.html")) + sorted(glob.glob("post/*.html")) \
            + sorted(glob.glob("heel-pain-procedure/*.html")):
        out.append(f)
    return out


def pretty(rel):
    """foo.html -> /foo ; index.html -> / ; dir/index.html -> /dir/"""
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel[:-len(".html")]


# ------------------------------------------------------------ html rewrite ---
ABS_INDEX = re.compile(re.escape(BASE) + r"/index\.html")
ABS_ANY = re.compile(re.escape(BASE) + r"/([A-Za-z0-9._/-]+?)\.html")
# href/src values ending in .html, optionally with a #fragment
REL_ATTR = re.compile(r'(href|src)=(["\'])([^"\']*?)\.html(#[^"\']*)?\2')


def rewrite_html(text):
    # 1. absolute canonical / og:url / schema @id + url values
    text = ABS_INDEX.sub(BASE + "/", text)
    text = ABS_ANY.sub(lambda m: f"{BASE}/{m.group(1)}", text)

    # 2. relative hrefs
    def rel(m):
        attr, q, path, frag = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        # index.html in any relative form points at the site root
        if path == "index" or path.endswith("/index"):
            return f'{attr}={q}/{frag}{q}'
        return f'{attr}={q}{path}{frag}{q}'
    text = REL_ATTR.sub(rel, text)
    return text


# ---------------------------------------------------------------- redirects --
# Posts retired by consolidation or renamed. Their URLs are indexed, so they
# must keep 301ing to whatever replaced them -- forever. _redirects is fully
# regenerated from disk on every run, so a rule added by hand there would be
# silently wiped; it has to live here.
#
# Format: (old path, target path, why)
RETIRED = [
    ("/post/what-to-know-about-bunion-surgery-in-2025",
     "/post/what-to-know-about-bunion-surgery",
     "the year was baked into the slug and went stale"),
    ("/post/how-to-fix-ankle-instability-for-good",
     "/post/chronic-ankle-instability-treatment-and-exercises",
     "consolidated: duplicate of the CAI treatment post"),
    ("/post/is-your-ankle-instability-holding-you-back-signs-symptoms-and-solutions",
     "/post/what-is-chronic-ankle-instability-cai",
     "consolidated: duplicate of the CAI explainer"),
    ("/post/why-your-chronic-ankle-instability-keeps-coming-back",
     "/post/why-does-chronic-ankle-instability-return",
     "consolidated: same question as why-does-...-return"),
    ("/post/toenail-fungus-removal",
     "/post/toe-nail-fungus-removal-options",
     "consolidated: subsumed by the treatment-options post"),
    ("/post/treating-toenail-fungus-and-ingrown-nails",
     "/post/toe-nail-fungus-removal-options",
     "consolidated: split-topic post duplicating both clusters"),
    ("/post/ingrown-nail-care-guide-daily-habits-treatments-and-prevention",
     "/post/long-term-ingrown-toenail-prevention-and-home-treatment",
     "consolidated: duplicate of the long-term prevention post"),
    ("/post/what-are-the-cause-s-of-ingrown-toenails-how-do-you-fix-them",
     "/post/long-term-ingrown-toenail-prevention-and-home-treatment",
     "consolidated: procedure section merged into the survivor"),
    ("/post/hammer-toe-effective-treatment-options",
     "/post/advanced-hammertoe-treatment-options",
     "consolidated: superseded by advanced-hammertoe-treatment-options"),
    ("/post/have-hammertoes-your-guide-to-what-they-are-prevention-and-treatment-options",
     "/post/advanced-hammertoe-treatment-options",
     "consolidated: superseded by advanced-hammertoe-treatment-options"),
    ("/post/what-is-a-dual-syndesmosis-tightrope-and-how-does-it-improve-recovery",
     "/post/understanding-the-dual-syndesmosis-tightrope-a-modern-fixation-option",
     "consolidated: near-identical to the other TightRope post"),
]

LEGACY = [
    # Wix-era URLs found in the Wayback archive that have no direct equivalent.
    ("/heal-pain", "/heel-pain", "the old site shipped this typo of heel-pain"),
    ("/post", "/blog", "Wix used /post as the blog index; ours is /blog"),
    ("/old-home", "/", "abandoned Wix draft page"),
    ("/product-page/performance-orthotics", "/shop", "Wix Stores product page"),
    ("/blog/categories/*", "/blog", "Wix blog category archives"),
    ("/blog/page/*", "/blog", "Wix blog pagination"),
]


def build_redirects(files):
    lines = [
        "# Generated by build-extensionless.py -- do not hand-edit.",
        "#",
        "# 1. Retire the .html URLs in favour of extensionless ones.",
        "#    The `!` forces the rule: Netlify resolves static files before",
        "#    redirects, and /foo.html is a static file, so an unforced rule",
        "#    would never fire. /foo still serves foo.html directly, so there",
        "#    is no loop.",
        "",
    ]
    for f in files:
        target = pretty(f)
        # Explicit separators, NOT ljust padding. ljust(66) only pads strings
        # SHORTER than 66 chars -- and 90 of these blog-post paths are longer,
        # so the source ran straight into the destination and then into "301!"
        # with no whitespace at all. Netlify silently failed to parse 90 of 192
        # rules and those .html URLs kept serving 200 instead of redirecting.
        lines.append(f"/{f}".ljust(64) + "  " + target.ljust(44) + "  301!")
    lines += [
        "",
        "# 2. Posts retired by consolidation or renamed. These URLs were indexed",
        "#    and may still carry links, so the redirects are permanent.",
        "",
    ]
    for frm, to, why in RETIRED:
        lines.append(f"# {why}")
        lines.append(frm.ljust(64) + "  " + to.ljust(44) + "  301")
    lines += [
        "",
        "# 3. Legacy URLs from the previous Wix site (found via the Wayback CDX",
        "#    index). These have no direct equivalent in the new structure.",
        "",
    ]
    for frm, to, why in LEGACY:
        lines.append(f"# {why}")
        lines.append(frm.ljust(64) + "  " + to.ljust(44) + "  301")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------- main --
if __name__ == "__main__":
    files = pages()

    changed = 0
    for f in files:
        p = ROOT / f
        s = p.read_text(encoding="utf-8")
        new = rewrite_html(s)
        if new != s:
            p.write_text(new, encoding="utf-8")
            changed += 1
    print(f"rewrote links/canonicals in {changed}/{len(files)} pages")

    # llms.txt carries absolute URLs too
    llms = ROOT / "llms.txt"
    s = llms.read_text(encoding="utf-8")
    new = ABS_INDEX.sub(BASE + "/", s)
    new = ABS_ANY.sub(lambda m: f"{BASE}/{m.group(1)}", new)
    if new != s:
        llms.write_text(new, encoding="utf-8")
        print("updated llms.txt")

    redirects = build_redirects(files)
    # Every rule must be three whitespace-separated fields. This check exists
    # because the ljust bug above shipped and broke 90 rules unnoticed.
    bad = [l for l in redirects.split("\n")
           if l.strip() and not l.lstrip().startswith("#") and len(l.split()) != 3]
    if bad:
        raise SystemExit(f"refusing to write _redirects: {len(bad)} malformed rules, "
                         f"first is: {bad[0]!r}")
    (ROOT / "_redirects").write_text(redirects, encoding="utf-8")
    print(f"wrote _redirects ({len(files)} .html retirements + {len(RETIRED)} retired posts "
          f"+ {len(LEGACY)} legacy rules, all parseable)")
