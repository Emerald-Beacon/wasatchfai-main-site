#!/usr/bin/env python3
"""
Generate thank-you.html and point every Netlify form at it.

Without an action attribute Netlify serves its own generic success page after a
submission -- unbranded, no clinic phone number, no indication of what happens
next. For a medical practice that is the worst possible moment to drop someone
onto a stock page: they have just asked for an appointment and want to know
they were heard.

The page is noindex,follow. It is a post-submission confirmation, not content;
indexing it would put "Thank you" in search results and let people land there
without ever submitting anything.

Run from the repo root.
"""
import glob
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = (ROOT / "farmington-utah.html").read_text(encoding="utf-8")
BASE = "https://wasatchfai.com"

_h = SRC.index("<!-- TOP BAR -->")
TOPBAR_HEADER = SRC[_h:SRC.index("</header>", _h) + len("</header>")]
_f = SRC.index("<!-- FOOTER -->")
FOOTER = SRC[_f:SRC.index("</footer>", _f) + len("</footer>")]
_cb = SRC.index("<!-- MOBILE CALL BAR -->")
CALLBAR = SRC[_cb:SRC.index("</nav>", _cb) + len("</nav>")]

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Thank You &mdash; We&rsquo;ve Got Your Request | Wasatch Foot &amp; Ankle</title>
<meta name="description" content="Thanks for reaching out to Wasatch Foot &amp; Ankle Institute. We'll be in touch within one business day.">
<link rel="canonical" href="{BASE}/thank-you">
<!-- A post-submission confirmation, not content. Indexing it would surface
     "Thank you" in search and let people arrive without submitting anything. -->
<meta name="robots" content="noindex, follow">
<meta name="author" content="Wasatch Foot &amp; Ankle Institute">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="css/site.css">
</head>
<body>

{TOPBAR_HEADER}

<!-- CONFIRMATION -->
<section class="detail-section">
  <div class="container">
    <div class="thanks-card">
      <div class="thanks-mark" aria-hidden="true">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <span class="eyebrow">Request Received</span>
      <h1>Thanks &mdash; we&rsquo;ve got it.</h1>
      <p class="thanks-lede">Someone from our team will call or email you within one business day to get you scheduled. If you sent this outside office hours, we&rsquo;ll reach out the next morning we&rsquo;re open.</p>

      <div class="thanks-urgent">
        <strong>Need to be seen today?</strong>
        <p>Don&rsquo;t wait on this form. Call the clinic nearest you &mdash; we hold time each day for urgent foot and ankle problems.</p>
        <div class="thanks-phones">
          <a href="tel:8014517500" class="btn btn-primary btn-arrow">Call Farmington &middot; 801-451-7500</a>
          <a href="tel:8016272122" class="btn btn-secondary btn-arrow">Call South Ogden &middot; 801-627-2122</a>
        </div>
      </div>

      <h2>While you wait</h2>
      <ul class="thanks-next">
        <li><a href="patient-intake-forms">Complete your intake forms</a> &mdash; both of them, so your visit starts on time.</li>
        <li><a href="plans-pricing">Check your insurance</a> &mdash; we accept most major carriers, and we&rsquo;ll verify before you arrive.</li>
        <li><a href="locations">Find your clinic</a> &mdash; directions, parking, and drive times from your city.</li>
        <li><a href="blog">Read up on your symptoms</a> &mdash; our education library covers most of what we treat.</li>
      </ul>

      <p class="thanks-back"><a href="/">&larr; Back to the homepage</a></p>
    </div>
  </div>
</section>

{FOOTER}

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "WebPage",
      "@id": "{BASE}/thank-you#webpage",
      "url": "{BASE}/thank-you",
      "name": "Thank You — Request Received",
      "inLanguage": "en-US",
      "isPartOf": {{ "@id": "{BASE}/#website" }},
      "about": {{ "@id": "{BASE}/#clinic" }}
    }}
  ]
}}
</script>

<script src="js/site.js" defer></script>

{CALLBAR}
</body>
</html>
"""

CSS = """
/* ============ THANK YOU ============
   Shown after a Netlify form submission. Deliberately plain: the job is to
   confirm receipt, set the callback expectation, and give an urgent path for
   anyone who should not be waiting on a form. */
.thanks-card{
  max-width:720px;margin:0 auto;background:var(--white);
  border:1px solid var(--line);border-radius:var(--r-lg);
  box-shadow:var(--shadow);padding:48px;
}
.thanks-mark{
  width:64px;height:64px;border-radius:999px;display:flex;
  align-items:center;justify-content:center;
  background:var(--sage);color:#fff;margin-bottom:22px;
}
.thanks-card h1{font-size:clamp(2rem,4vw,2.8rem);margin-bottom:16px}
.thanks-lede{font-size:1.1rem;margin-bottom:32px}
.thanks-urgent{
  background:var(--blue-soft);border-radius:var(--r);
  padding:26px;margin-bottom:36px;
}
.thanks-urgent strong{display:block;font-size:1.05rem;margin-bottom:6px;color:var(--blue-dark)}
.thanks-urgent p{margin-bottom:18px;font-size:.95rem}
.thanks-phones{display:flex;gap:12px;flex-wrap:wrap}
.thanks-card h2{font-size:1.4rem;margin-bottom:14px}
.thanks-next{margin:0 0 28px 20px;display:grid;gap:10px}
.thanks-next a{color:var(--blue);font-weight:600;text-decoration:underline;text-underline-offset:3px}
.thanks-next a:hover{color:var(--orange)}
.thanks-back a{color:var(--muted);font-weight:600}
.thanks-back a:hover{color:var(--blue)}
@media (max-width:600px){
  .thanks-card{padding:28px 22px}
  .thanks-phones .btn{width:100%;justify-content:center}
}
"""

if __name__ == "__main__":
    (ROOT / "thank-you.html").write_text(PAGE, encoding="utf-8")
    print("wrote thank-you.html")

    css = ROOT / "css/site.css"
    s = css.read_text(encoding="utf-8")
    if ".thanks-card{" not in s:
        marker = "/* ============ VERY SMALL SCREENS"
        s = s.replace(marker, CSS.strip() + "\n\n" + marker, 1)
        css.write_text(s, encoding="utf-8")
        print("added thank-you styles")

    # Point every real form at the confirmation page. The heel-pain quiz posts
    # via fetch() and renders its own success state, so it is left alone.
    n = 0
    for f in sorted(glob.glob("*.html")) + sorted(glob.glob("post/*.html")):
        p = ROOT / f
        t = p.read_text(encoding="utf-8")
        o = t
        t = re.sub(r'(<form\b(?![^>]*\baction=)[^>]*\bdata-netlify="true"[^>]*?)>',
                   r'\1 action="/thank-you">', t)
        if t != o:
            p.write_text(t, encoding="utf-8")
            n += 1
    print(f"added action=\"/thank-you\" to forms on {n} pages")
