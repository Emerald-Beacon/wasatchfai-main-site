# Wasatch FAI — SEO / GEO / AEO Audit + Local SEO Build-Out Plan

**Audited:** 2026-08-03 · **Scope:** this repo (175 HTML pages) + live URL verification
**Repo:** `Emerald-Beacon/wasatchfai-main-site` → deploys to `https://wasatchfai.netlify.app`

---

## 0. Read this first: the repo is not the live site

`www.wasatchfai.com` is served by **Wix** (`generator: Wix.com Website Builder`, `server: Pepyaka`).
This repo deploys to **`wasatchfai.netlify.app`**. They share nothing.

Verification:

| URL | Result |
|---|---|
| `www.wasatchfai.com/` | 200 — Wix site, 1.28 MB, none of this repo's assets |
| `www.wasatchfai.com/plantar-fasciitis.html` | **400** |
| `www.wasatchfai.com/post/got-gout.html` | **404** |
| `wasatchfai.netlify.app/plantar-fasciitis.html` | 200 |
| `wasatchfai.netlify.app/post/got-gout.html` | 200 |

**Consequences that reframe the whole audit:**

1. Every canonical, `sitemap.xml` entry, `llms.txt` link, and JSON-LD `@id` in this repo points at
   `https://www.wasatchfai.com/...`. Those URLs **404 or 400 today.** The structured-data entity graph
   currently resolves to nothing.
2. **The staging site is fully indexable.** `wasatchfai.netlify.app/robots.txt` is `Allow: /` with no
   `noindex` anywhere. 175 pages of the future production content are crawlable on a domain that is
   not the brand's — a textbook staging leak and a duplicate-content risk against the launch.
3. This is a **migration**, not an optimization. The single highest-value action on this list is not
   a title tag — it is cutting the domain over and 301-mapping the Wix URLs.

Everything below is graded as *launch readiness*, not as live performance.

---

## 1. SEO Health Score — **70 / 100** (pre-launch)

| Category | Weight | Score | Driver |
|---|---:|---:|---|
| Technical SEO | 22% | 78 | Valid schema, canonicals, no broken links — but 51 MB dead directory, live duplicate homepage |
| Content Quality | 23% | 68 | Good depth; org-level authorship on YMYL medical content |
| On-Page SEO | 20% | 62 | 143/175 titles over length, 150/175 descriptions over length |
| Schema / Structured Data | 10% | 72 | 169/169 blocks valid; zero physician entities, homepage has none |
| Performance (CWV proxy) | 10% | 60 | Lean CSS/JS; multi-MB unoptimized JPEGs |
| AI Search Readiness | 10% | 80 | `llms.txt`, 735 question headings, 1,020 Q&A pairs |
| Images | 5% | 65 | Alt/dimensions/lazy near-perfect; formats and weight poor |

---

## 2. What is genuinely strong

Worth stating plainly, because it's most of the site:

- **Structured data is well built.** 169 JSON-LD blocks, **100% parse-valid**, zero errors. Correct
  medical vocabulary — `MedicalClinic`, `MedicalCondition`, `MedicalTherapy`, `MedicalProcedure`,
  `MedicalSymptom` — with a shared `@id` graph (`#clinic` referenced 830 times).
- **Location schema is better than most agencies ship.** Per-clinic `GeoCoordinates`, `hasMap`,
  `openingHoursSpecification`, and an `areaServed` array naming Kaysville, Centerville, Fruit Heights,
  and Davis County.
- **Content depth is real.** 123 blog posts, median 1,261 words, **none under 969**. Root pages median
  1,450 words. No thin-content problem in the editorial library.
- **Internal linking has no breakage.** Zero broken internal targets across 175 pages.
- **Image hygiene is excellent.** 376 `<img>` tags: 375 have alt text, **100% have explicit
  width/height**, 100% have a `loading` attribute. (The one without alt is a Facebook tracking pixel.)
- **`llms.txt` is high quality** — NAP, hours, physicians, service area, condition list, and an
  explicit note for AI assistants. Most clinics have nothing here.
- **NAP is consistent.** 1,158 instances of 801-451-7500 and 1,003 of 801-627-2122 with no variants.
  The two odd numbers found are correctly-labeled fax lines.

---

## 3. Critical — blocks launch

### C1. Domain cutover + 301 map (the whole project)
The Wix site owns all current rankings, reviews, and backlinks. Cutting over without a URL map
discards them. Wix URLs are path-style (`/plantar-fasciitis`) vs this repo's `.html` — **every URL
changes.** No redirect map exists in `netlify.toml` (it has exactly one rule, for `/ankle-franctures`).

### C2. Staging site is indexable
`wasatchfai.netlify.app` serves 175 crawlable pages with production canonicals. Add
`X-Robots-Tag: noindex` for the Netlify subdomain until cutover.

### C3. Homepage has zero structured data
`index.html` — the most important page — has **no JSON-LD at all**. Also missing on `staff.html`,
`services.html`, `recovery.html`. For a local medical business the homepage `MedicalClinic` +
`Organization` node is the anchor of the entity graph.

### C4. `homepage/` — 51 MB of dead weight, live and duplicated
Unreferenced by any page, tracked in git, **and serving at
`wasatchfai.netlify.app/homepage/index.html` (200)** — a second, competing homepage.
Largest offenders: `hero-card-3.jpg` **10.4 MB**, `hero-mountain-biking.jpg` **8.5 MB**,
`dr-campbell.jpg` 5.4 MB, `dr-woolley.jpg` / `dr-frost.jpg` 3.9 MB each.

---

## 4. High — fix before or at launch

### H1. YMYL authorship failure (biggest content risk)
All 123 blog posts declare `"author": {"@id": ".../#clinic"}` — an **organization, not a person** —
and **none carry `reviewedBy`**. There is **no `Person` or `Physician` schema anywhere on the site**,
and no visible author byline in any post. Four credentialed DPMs (Campbell, Frost, Woolley, Murrah)
are named in `llms.txt` and on `staff.html` but are invisible to both Google's E-E-A-T evaluation and
to LLM citation logic. For medical YMYL content this is the single largest ranking liability.

### H2. Title tags — 143 of 175 exceed 60 characters
The `| Wasatch Foot & Ankle` suffix plus `in Farmington & South Ogden, UT` blows the budget on almost
every page. Worst: 111 chars (`diabetes-and-podiatry-...`), 102, 101, 101, 101. Only 32 pages are in range.

### H3. Meta descriptions — 150 of 175 exceed 160 characters
Range up to 225 chars. No duplicates and none too short — this is purely a truncation problem.

### H4. Location page duplication
- `farmington-utah.html` vs `ogden-utah-foot-doctor.html` — **67% of Farmington's content appears
  verbatim in Ogden** (49.7% Jaccard). The two most commercially important local pages are near-twins.
- `idaho.html` vs `wyoming.html` — **55% overlap** (38.2% Jaccard).

### H5. `ogden.html` vs `ogden-utah-foot-doctor.html` cannibalization
Two pages targeting Ogden podiatry intent. `ogden.html` is **orphaned** (no in-content inbound links)
and its schema `sameAs` points at the other page — a half-finished consolidation.

### H6. Orphan pages
Zero in-content inbound links (nav/footer excluded): `ogden.html`, `idaho.html`, `wyoming.html`,
`members.html`, `medical-history.html`, `recovery-instructions.html`, `shop.html`.
**All three geographic expansion pages are orphaned.**

### H7. Homepage heading structure
`index.html` has **3 `<h1>` elements** (one per hero slide). `services.html` has **zero**.

### H8. No Google Business Profile linkage
One `sameAs` on the entire site, and it's self-referential. No GBP URL in any schema node, no review
schema, no `aggregateRating` anywhere. GBP is the dominant local ranking factor and the site does not
connect to it.

---

## 5. Medium

- **Sitemap `lastmod` is uniform and stale** — all 174 URLs say `2026-07-14`. Uniform dates are a
  weak/ignored signal; generate real per-file mtimes. Also missing the new `#foot-model` homepage change.
- **`heel-pain-procedure/index.html`** — the only page missing both a canonical and `og:image`. Also
  has heading skips (h1→h4, h2→h4) and **zero in-content outbound links**.
- **Money pages are thin**: `plans-pricing.html` 543 words, `book-appointment.html` 544,
  `recovery.html` 260. Insurance/pricing is a high-intent local query and 543 words underserves it.
- **`staff.html` has one outbound content link** — the physician page should be a hub.
- **Render-blocking Google Fonts** on every page (Fraunces + Inter, two families). Self-host or preload.
- **Image formats**: 35 JPG + 8 PNG, exactly 1 AVIF. No WebP/AVIF pipeline.
- **`robots.txt` is bare** — fine, but no AI-crawler declarations and no `Crawl-delay` for aggressive bots.

---

## 6. GEO / AEO assessment — **80/100, the strongest dimension**

**Working:**
- `llms.txt` present, accurate, well structured — genuinely above-average.
- **735 question-form headings** across the site; **169 `FAQPage` blocks / 1,020 Q&A pairs.**
- Clean entity graph with stable `@id`s — exactly what retrieval systems need to resolve "who is this".
- All AI crawlers allowed (`Allow: /`).
- Condition pages use `MedicalCondition` + `MedicalSymptom` + `MedicalTherapy` — strong semantic typing.

**Gaps:**
- **Zero tables sitewide.** Comparison tables are among the most-extracted structures for AI answers
  (e.g. "plantar fasciitis vs heel spurs", "custom orthotics vs store-bought" — both already exist as posts).
- **Zero "Key Takeaways" / TL;DR blocks.** No answer-first summary any engine can lift.
- **28 pages have no question heading**, including `index.html`, `book-appointment.html`,
  `plans-pricing.html`, `ogden.html`.
- **No author entity** (see H1) — LLMs cite named credentialed humans over anonymous org content.
- No `speakable` markup.

**Note on FAQ schema:** Google retired FAQ rich results for all sites on **2026-05-07**. The 169
existing `FAQPage` blocks no longer earn a SERP feature — but keep them; they retain real AI/LLM
citation value. Don't add new `FAQPage` expecting Google SERP benefit.

---

## 7. Local SEO Build-Out Plan

### Current local footprint
Two real city pages (Farmington, South Ogden) + one duplicate (`ogden.html`) + two state pages
(Idaho, Wyoming, both orphaned). "Farmington" and "South Ogden" appear on all 174 pages — but that's
the footer NAP, not localized content.

**The gap:** schema `areaServed` already claims Kaysville, Centerville, Fruit Heights, and Davis
County, but **no page backs those claims.** Content coverage for surrounding cities:

| City | Pages mentioning |
|---|---:|
| Kaysville | 1 |
| Centerville | 1 |
| Bountiful | 1 |
| Fruit Heights | 1 |
| Riverdale | 1 |
| Roy | 1 |
| Layton | 2 |
| Clearfield, Syracuse, Clinton, West Point, North Salt Lake | **0** |

### Phase 0 — Migration (must precede everything)
1. Crawl the live Wix site; export every indexed URL.
2. Build the Wix → Netlify 301 map in `netlify.toml`. Every URL changes (`/plantar-fasciitis` → `/plantar-fasciitis.html`).
3. Decide `.html` vs extensionless permanently — do it **before** launch, not after.
4. `noindex` the Netlify subdomain now; remove at cutover.
5. Verify both properties in Search Console; submit the sitemap post-cutover; keep the old property for 6+ months.

### Phase 1 — Foundation (launch week)
6. Homepage `MedicalClinic` + `Organization` + `WebSite` JSON-LD (C3).
7. `Physician` schema for all four DPMs on `staff.html`, with `hasCredential`, `memberOf` (ACFAS),
   `medicalSpecialty`, `worksFor` → `#clinic`, and individual `@id`s.
8. Rewrite all 143 long titles and 150 long descriptions. Shorten the brand suffix to `| Wasatch FAI`
   and drop `in Farmington & South Ogden, UT` from condition pages — the city belongs in the H1/body,
   not burning 32 chars of title.
9. Fix `index.html` to a single H1; add an H1 to `services.html`.
10. Delete `homepage/` (51 MB); convert remaining hero images to WebP/AVIF with JPEG fallback.
11. Add GBP `sameAs` to every `MedicalClinic` node, both locations.

### Phase 2 — Local authority (weeks 2–6)
12. **Resolve the Ogden conflict.** Keep `ogden-utah-foot-doctor.html`; 301 `ogden.html` → it.
13. **Rewrite the two clinic pages to 70%+ unique** (currently 33%). Each needs genuinely local
    substance: parking and building directions, cross-streets, transit, staff for *that* office,
    location-specific photos, insurance networks, and the conditions that office actually sees most.
14. **Build 6 city pages** — Kaysville, Layton, Centerville, Bountiful, Clearfield, Roy. Hard rule:
    **60%+ unique content each**, minimum 800 words, and each must contain something only a local
    would know (drive time from that city to the clinic, local trail/rec context, nearest ER,
    schools/sports leagues served). Do **not** template these — templated city pages are the most
    common local SEO penalty vector.
15. Cap city pages at 10 total. Past that, the uniqueness requirement stops being satisfiable and the
    pages become a liability. Revisit only with demonstrated traffic.
16. Fix Idaho/Wyoming: merge into one "Traveling for Care" page, or make each genuinely distinct
    (referral pathways, travel/lodging, follow-up-by-telehealth logistics).
17. Interlink: every condition page → nearest clinic page; every city page → its clinic + top 5
    conditions. De-orphan all geographic pages.
18. Expand `plans-pricing.html` to 1,200+ words with a named insurance-carrier list — high-intent
    local query, currently underserved.

### Phase 3 — GBP + reviews (parallel, ongoing)
19. Audit both GBP listings: categories (primary **Podiatrist**), services, attributes, photos, hours,
    Q&A seeding, and per-location description.
20. Review generation program. Add `AggregateRating` to clinic schema **only once it reflects real,
    verifiable review data** — never fabricate it.
21. Citation audit across podiatry-specific directories (ACFAS, APMA, Healthgrades, Vitals, WebMD)
    plus general NAP (Yelp, Apple Maps, Bing Places). NAP is already internally consistent — the work
    is external alignment.

### Phase 4 — GEO/AEO (weeks 4–10)
22. Add a "Key Takeaways" block to the top of the 30 highest-value condition and blog pages.
23. Add comparison tables where posts already imply them — plantar fasciitis vs heel spurs, custom
    vs store-bought orthotics, flat feet vs high arches, hammertoe treatment options.
24. Named physician bylines + `reviewedBy` on all 123 posts (depends on #7).
25. Add question headings to the 28 pages that lack them.
26. Refresh `llms.txt` post-launch with the new city pages.
27. Real per-file `lastmod` in the sitemap; automate regeneration.

---

## 8. Sequencing — what unblocks what

```
Phase 0 (migration + noindex)  ─┬─► everything else
                                │
  #7 Physician schema ──────────┼─► #24 post bylines/reviewedBy  ─► E-E-A-T recovery
                                │
  #12 Ogden consolidation ──────┼─► #13 clinic page rewrite ─► #14 city pages
                                │
  #10 delete homepage/ ─────────┴─► image pipeline ─► CWV
```

Do not build city pages (#14) before the clinic pages are unique (#13) — you would be multiplying a
duplication problem across six new URLs.

---

## 9. How we'd know each bet failed

| Action | Falsifiability check | Leading indicator |
|---|---|---|
| Domain cutover | Organic sessions drop >30% and don't recover in 8 weeks | GSC "Pages" indexed count on new property |
| Physician schema + bylines | Condition pages don't gain impressions in 90 days | Rich Results Test shows `Physician` parsing |
| City page build-out | New pages get impressions but <1% CTR, or don't index within 30 days | GSC coverage per URL |
| Clinic page de-duplication | Both pages still rank for each other's city term | Rank split between the two URLs |
| Key Takeaways / tables | No increase in AI Overview or LLM citations at 90 days | Manual monthly prompt checks across ChatGPT/Perplexity |

---

## 10. Unverified — needs external data

I audited the repo and confirmed HTTP status of live URLs. I did **not** have access to:
- Google Search Console / GA4 (no credentials in environment) — no impressions, rankings, or traffic data
- Google Business Profile status for either location
- Backlink profile of the existing Wix domain
- Real Core Web Vitals field data (CrUX)
- Actual review counts/ratings

Any ranking or traffic claim in this document is inference from on-page evidence, not measurement.
Phase 0 should start by connecting GSC and GA4 so the migration has a baseline to be judged against.
