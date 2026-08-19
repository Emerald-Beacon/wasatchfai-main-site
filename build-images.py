#!/usr/bin/env python3
"""
Recompress oversized hero/content JPEGs and emit WebP alongside them.

WHY: images/ was 4.5 MB with a 631 KB hero. Server response and HTML are already
fast (TTFB ~85ms, 36 KB homepage), so unoptimised JPEGs were the only real Core
Web Vitals drag — and LCP on mobile is where local medical search is won.

Keeps the .jpg (every <img>/background-image reference still resolves) and adds a
.webp next to it, so markup can adopt <picture> incrementally without breaking.
Never upscales. Idempotent: re-running skips files already within budget.

Run from the repo root:  python3 build-images.py
"""
import pathlib, subprocess, sys
from PIL import Image

ROOT = pathlib.Path(__file__).parent
IMG = ROOT / "images"
MAX_W = 1600          # nothing on the site renders wider than this
BUDGET = 180 * 1024   # per-image target for JPEGs
QUALITY = 82

def main():
    if not IMG.is_dir():
        sys.exit("images/ not found")
    before = after = 0
    for p in sorted(IMG.iterdir()):
        if p.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        start = p.stat().st_size
        before += start
        try:
            im = Image.open(p)
        except Exception as e:
            print(f"  skip {p.name}: {e}"); after += start; continue
        w, h = im.size
        changed = False
        if p.suffix.lower() in (".jpg", ".jpeg") and (start > BUDGET or w > MAX_W):
            im = im.convert("RGB")
            if w > MAX_W:
                im = im.resize((MAX_W, round(h * MAX_W / w)), Image.LANCZOS)
            # Step quality down until the file fits the budget. Photographs of
            # clinics and landscapes tolerate this far better than flat graphics,
            # and LCP cares about bytes, not about q=82 being a nice round number.
            for q in (QUALITY, 76, 70, 64, 58):
                im.save(p, "JPEG", quality=q, optimize=True, progressive=True)
                if p.stat().st_size <= BUDGET:
                    break
            changed = True
        # WebP twin for every raster, regardless of whether the JPEG changed
        webp = p.with_suffix(".webp")
        if not webp.exists() or webp.stat().st_mtime < p.stat().st_mtime:
            Image.open(p).convert("RGB").save(webp, "WEBP", quality=QUALITY, method=6)
        end = p.stat().st_size
        after += end
        if changed:
            print(f"  {p.name:<46} {start/1024:7.0f} KB -> {end/1024:6.0f} KB")
    print(f"\n  images/ raster total: {before/1024/1024:.2f} MB -> {after/1024/1024:.2f} MB")
    print(f"  webp twins: {len(list(IMG.glob('*.webp')))}")

if __name__ == "__main__":
    main()
