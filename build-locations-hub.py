#!/usr/bin/env python3
"""
Generate locations.html -- the hub that ties the two clinic pages and the
eleven city pages together.

This page exists to solve a specific problem found in the audit: the
geographic pages were orphaned (zero in-content inbound links), and the nav's
"Locations" item pointed at farmington-utah.html, which made Farmington the de
facto locations index and left every other city unreachable except by search.

Reuses chrome from farmington-utah.html. Run from the repo root.
"""
import re
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
SRC = (ROOT / "farmington-utah.html").read_text(encoding="utf-8")

_h = SRC.index("<!-- TOP BAR -->")
TOPBAR_HEADER = SRC[_h:SRC.index("</header>", _h) + len("</header>")]
_f = SRC.index("<!-- FOOTER -->")
FOOTER = SRC[_f:SRC.index("</footer>", _f) + len("</footer>")]
_cb = SRC.index("<!-- MOBILE CALL BAR -->")
CALLBAR = SRC[_cb:SRC.index("</nav>", _cb) + len("</nav>")]

CLINICS = [
    {
        "page": "farmington-utah.html", "name": "Farmington",
        "street": "473 W. Bourne Circle, Suite 2", "city": "Farmington", "zip": "84025",
        "phone": "801-451-7500", "tel": "8014517500",
        "blurb": "Our Davis County clinic, just off Park Lane near Station Park and a few minutes "
                 "from I-15 Exit 325. Free ground-level parking directly outside.",
    },
    {
        "page": "ogden-utah-foot-doctor.html", "name": "South Ogden",
        "street": "945 Chambers Street, Suite 3", "city": "South Ogden", "zip": "84403",
        "phone": "801-627-2122", "tel": "8016272122",
        "blurb": "Our Weber County clinic, a short drive from Washington Boulevard and the 5600 "
                 "South exit, serving Ogden and the northern valley.",
    },
]

DAVIS = [
    ("farmington-utah.html", "Farmington", "Clinic location &middot; Davis County"),
    ("centerville-utah.html", "Centerville", "About 7 minutes to Farmington"),
    ("fruit-heights-utah.html", "Fruit Heights", "About 8 minutes to Farmington"),
    ("kaysville-utah.html", "Kaysville", "About 10 minutes to Farmington"),
    ("woods-cross-utah.html", "Woods Cross", "About 12 minutes to Farmington"),
    ("layton-utah.html", "Layton", "About 12 minutes to Farmington"),
    ("bountiful-utah.html", "Bountiful", "About 13 minutes to Farmington"),
    ("clearfield-utah.html", "Clearfield", "About 17 minutes to Farmington"),
]

WEBER = [
    ("ogden-utah-foot-doctor.html", "South Ogden", "Clinic location &middot; Weber County"),
    ("riverdale-utah.html", "Riverdale", "About 7 minutes to South Ogden"),
    ("ogden-utah.html", "Ogden", "About 8 minutes to South Ogden"),
    ("roy-utah.html", "Roy", "About 12 minutes to South Ogden"),
    ("north-ogden-utah.html", "North Ogden", "About 18 minutes to South Ogden"),
]

OUT_OF_STATE = [
    ("idaho.html", "Idaho patients", "Travelling to Utah for foot &amp; ankle care"),
    ("wyoming.html", "Wyoming patients", "Travelling to Utah for foot &amp; ankle care"),
]

TITLE = "Locations &amp; Service Areas | Wasatch Foot &amp; Ankle"
DESC = ("Wasatch Foot &amp; Ankle Institute serves Davis and Weber County from clinics in "
        "Farmington and South Ogden. Find drive times, directions, and a podiatrist near you.")
URL = "https://www.wasatchfai.com/locations.html"


def cards(items):
    return "\n".join(
        f"""      <a href="{href}" class="related-card">
        <h3>{name}</h3>
        <p>{sub}</p>
        <span>View details &rarr;</span>
      </a>""" for href, name, sub in items)


def clinic_block(c):
    return f"""      <div class="loc-card reveal">
        <h2>{c['name']} clinic</h2>
        <p>{c['blurb']}</p>
        <div class="loc-card-row">
          <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8 2 5 5 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-4-3-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>
          <div><strong>Address</strong><span>{c['street']}<br>{c['city']}, UT {c['zip']}</span></div>
        </div>
        <div class="loc-card-row">
          <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20 15.5c-1.25 0-2.45-.2-3.57-.57-.35-.11-.74-.03-1.02.24l-2.2 2.2c-2.83-1.44-5.15-3.75-6.59-6.58l2.2-2.21c.28-.27.36-.66.25-1.01-.37-1.12-.57-2.32-.57-3.57 0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1z"/></svg>
          <div><strong>Phone</strong><span><a href="tel:{c['tel']}">{c['phone']}</a></span></div>
        </div>
        <div class="hours loc-hours">
          <strong>Hours</strong>
          Mon&ndash;Thu: 8:00a &ndash; 5:00p<br>Fri: 8:00a &ndash; 12:00p<br>Sat&ndash;Sun: Closed
        </div>
        <a href="{c['page']}" class="btn btn-primary btn-arrow loc-card-btn">Visit {c['name']}</a>
      </div>"""


ALL_CITIES = [n for _, n, _ in DAVIS + WEBER]
item_list = ",\n".join(
    f'        {{ "@type": "ListItem", "position": {i}, "url": "https://www.wasatchfai.com/{h}", "name": {json.dumps(re.sub("&[a-z]+;", "", n))} }}'
    for i, (h, n, _) in enumerate(DAVIS + WEBER, 1))

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta name="author" content="Wasatch Foot &amp; Ankle Institute">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wasatch Foot &amp; Ankle Institute">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://www.wasatchfai.com/images/hero-mountain-biking.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="https://www.wasatchfai.com/images/hero-mountain-biking.jpg">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="css/site.css">
</head>
<body>

{TOPBAR_HEADER}

<!-- BREADCRUMB -->
<nav class="breadcrumb" aria-label="Breadcrumb">
  <div class="container">
    <ol>
      <li><a href="index.html">Home</a></li>
      <li aria-current="page">Locations</li>
    </ol>
  </div>
</nav>

<!-- HERO -->
<section class="detail-hero" style="background-image:url('images/hero-mountain-biking.jpg')">
  <div class="container detail-hero-inner">
    <span class="visually-hidden">The Wasatch range above Davis and Weber County, Utah</span>
    <span class="eyebrow">Northern Utah</span>
    <h1>Locations &amp; Service Areas</h1>
    <p class="detail-hero-lede">Two clinics &mdash; Farmington and South Ogden &mdash; covering Davis County, Weber County, and the communities between them. Find the one nearest you, with honest drive times rather than a vague service-area map.</p>
  </div>
</section>

<!-- CLINICS -->
<section class="loc-section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Our Clinics</span>
      <h2>Where you&rsquo;ll actually be seen</h2>
      <p>Both clinics are staffed by the same physicians and offer the same services. Choose whichever is closer &mdash; your records follow you either way.</p>
    </div>
    <div class="loc-layout">
{clinic_block(CLINICS[0])}
{clinic_block(CLINICS[1])}
    </div>
  </div>
</section>

<!-- SERVICE AREAS -->
<section class="detail-section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Davis County</span>
      <h2>Communities we serve from Farmington</h2>
      <p>Drive times are typical off-peak estimates from the centre of each city to 473 W. Bourne Circle.</p>
    </div>
    <div class="related-grid reveal">
{cards(DAVIS)}
    </div>
  </div>
</section>

<section class="detail-section" style="background:var(--cream)">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Weber County</span>
      <h2>Communities we serve from South Ogden</h2>
      <p>Drive times are typical off-peak estimates from the centre of each city to 945 Chambers Street.</p>
    </div>
    <div class="related-grid reveal">
{cards(WEBER)}
    </div>
  </div>
</section>

<section class="detail-section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Beyond Utah</span>
      <h2>Travelling for care</h2>
      <p>We regularly see patients who travel from out of state for foot and ankle surgery and complex reconstruction.</p>
    </div>
    <div class="related-grid reveal">
{cards(OUT_OF_STATE)}
    </div>
  </div>
</section>

<!-- CTA BAND -->
<section class="cta-band">
  <div class="container cta-band-inner reveal">
    <div>
      <span class="eyebrow" style="color:#ffe5cc">Ready When You Are</span>
      <h2>Not sure which clinic is closer?</h2>
      <p>Call either number and our team will point you to whichever office gets you seen soonest.</p>
    </div>
    <div class="cta-band-actions">
      <a href="book-appointment.html" class="btn btn-light btn-arrow">Request Appointment</a>
      <a href="tel:8014517500" class="btn btn-ghost cta-ghost">Call Farmington</a>
    </div>
  </div>
</section>

{FOOTER}

<!-- JSON-LD STRUCTURED DATA -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "@id": "{URL}#breadcrumb",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.wasatchfai.com/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Locations", "item": "{URL}" }}
      ]
    }},
    {{
      "@type": "CollectionPage",
      "@id": "{URL}#webpage",
      "url": "{URL}",
      "name": "Locations & Service Areas",
      "description": "Wasatch Foot & Ankle Institute serves Davis and Weber County from clinics in Farmington and South Ogden.",
      "inLanguage": "en-US",
      "isPartOf": {{ "@id": "https://www.wasatchfai.com/#website" }},
      "about": {{ "@id": "https://www.wasatchfai.com/#clinic" }},
      "mainEntity": {{ "@id": "{URL}#arealist" }}
    }},
    {{
      "@type": "ItemList",
      "@id": "{URL}#arealist",
      "name": "Cities served by Wasatch Foot & Ankle Institute",
      "numberOfItems": {len(DAVIS) + len(WEBER)},
      "itemListElement": [
{item_list}
      ]
    }}
  ]
}}
</script>

<script src="js/site.js" defer></script>

{CALLBAR}
</body>
</html>
"""

if __name__ == "__main__":
    (ROOT / "locations.html").write_text(PAGE, encoding="utf-8")
    print(f"wrote locations.html ({len(DAVIS) + len(WEBER)} cities + {len(OUT_OF_STATE)} out-of-state)")
