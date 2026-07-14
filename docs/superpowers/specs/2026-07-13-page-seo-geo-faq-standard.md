# WasatchFAI.com Page SEO / GEO / FAQ Standard (Phase 2)

Every Phase-2 page follows this standard. Source of truth for all fan-out subagents.
Informed by the Claude SEO plugin (claude-seo) guidance, adapted for a local,
YMYL (medical) podiatry site.

## Non-negotiables (all page types)

- **Shared shell:** same `<head>` (Google Fonts preconnect + Fraunces/Inter link,
  `css/site.css`), hard-coded header + footer from `partials/`, `js/site.js` deferred.
  Black full-lockup logo (`images/logo-full.png`), no side text (matches current homepage).
- **Unique meta:** `<title>` (~50-60 chars, primary keyword + location + brand),
  meta description (~150-160 chars, benefit + CTA), `<link rel="canonical">` (absolute
  `https://www.wasatchfai.com/<slug>.html`), Open Graph + Twitter tags. All unique per page.
- **Breadcrumb** (visible + BreadcrumbList JSON-LD).
- **Answer-first content:** the H1 is followed by a concise 40-60 word lead paragraph
  that directly defines/answers the page's core question (citable by AI engines). Each
  H2 opens with a 1-2 sentence direct answer, then detail.
- **FAQ section on every page** (visible) + `FAQPage` JSON-LD. FAQ = real patient
  questions, concise answer-first replies (1-3 sentences). Rationale: Google retired FAQ
  rich results (May 2026), but FAQ content + FAQPage schema remain high-value for AI
  search / LLM citation (GEO) and user experience — which is the goal here.
- **Schema (JSON-LD), never HowTo:** BreadcrumbList + FAQPage + a page-appropriate type
  (MedicalWebPage for conditions, MedicalClinic/LocalBusiness for locations, Article for
  blog posts) + the shared clinic Organization/MedicalClinic node with NAP.
- **Internal links:** 3-5 contextual links to related conditions/services + the relevant
  location + `book-appointment.html`, with descriptive anchor text.
- **E-E-A-T:** a "Reviewed by the physicians at Wasatch Foot & Ankle Institute" line;
  reference board-certified, fellowship-trained care; local roots (Farmington & South Ogden).
- **GEO/AI citability:** clear entity definitions, natural-language question headings,
  concise self-contained sentences, local entities (Farmington, South Ogden, Davis County,
  Weber County, Northern Utah). 
- **MEDICAL ACCURACY (critical):** never fabricate statistics, study citations, success
  rates, or clinical claims. Keep clinical content general standard-of-care. When precise
  numbers aren't verifiable, describe qualitatively. Preserve any factual claims migrated
  from the old site; do not invent new ones.
- **Accessibility:** descriptive `alt` on every image; hero images via relative
  `background-image:url('images/..')` inline (not `--img`); `aria-hidden` on decorative svgs.
- **Contact facts verbatim:** Farmington 801-451-7500 / 473 W. Bourne Circle, Suite 2,
  Farmington, UT 84025; South Ogden 801-627-2122 / 945 Chambers Street, Suite 3, South
  Ogden, UT 84403; contactus@wasatchfai.com; hours Mon-Thu 8a-5p, Fri 8a-12p; Pay a Bill
  → https://pay.InstaMed.com/WASATCHFOOT.

## Condition / service pages (~27) — template: docs/templates/condition.html

- **H1:** condition name. **Title:** e.g. "Plantar Fasciitis Treatment — Farmington &
  South Ogden, UT | Wasatch Foot & Ankle".
- **Body sections (H2s, answer-first), ~900-1400 unique words:**
  1. What is [condition]? (definition lead)
  2. Symptoms / signs
  3. Causes & risk factors
  4. How we diagnose it
  5. Treatment options (conservative → advanced; include the clinic's in-office /
     minimally-invasive options where truthful)
  6. Recovery / what to expect
  7. When to see a podiatrist
  8. Why choose Wasatch Foot & Ankle Institute (E-E-A-T, local)
- **FAQ:** 5-8 Q&As.
- **Schema:** MedicalWebPage (about a MedicalCondition) + BreadcrumbList + FAQPage +
  clinic MedicalClinic node.
- Source the old page content (WebFetch the live URL) and EXPAND it; keep migrated facts.

## Location pages (~5: farmington-utah, ogden-utah-foot-doctor, ogden, wyoming, idaho)

- **Title:** "[City] Foot & Ankle Clinic / Podiatrist | Wasatch Foot & Ankle".
- NAP block, embedded Google Map iframe (title + loading=lazy), hours, directions/service
  area, community/local content, both-clinic cross-links, appointment CTA + Netlify form.
- **FAQ:** local questions (parking, same-day, insurance, what to bring, service area).
- **Schema:** MedicalClinic/LocalBusiness with THAT location's NAP + geo + openingHours +
  BreadcrumbList + FAQPage. (Geo landing pages like wyoming/idaho: service-area framing,
  60%+ unique content, no fake local addresses — they point to the two real clinics.)
- Template: docs/templates/location.html.

## Utility / forms / legal pages (light-appropriate)

Pages: book-appointment, feedback, plans-pricing, patient-intake-forms, new-patient,
medical-history, summary-of-npp, recovery-instructions, nail-proceedure, conscious-sedation,
diabetic-foot-care-1, limb-salvage, shop, members, covid-19-response, services-list.

- Clean, correct, useful. Proper unique meta + canonical + breadcrumb.
- A SHORT, practical FAQ (3-5 Q&As) fitted to the page (e.g. "What should I bring to my
  appointment?", "How do I submit my forms?"). No keyword-stuffed marketing copy.
- Schema: WebPage/ContactPage/MedicalWebPage as fits + BreadcrumbList + FAQPage + clinic node.
- Forms wired to Netlify Forms where they collect input.

## Blog

- **blog.html:** index/landing — intro, featured + recent post cards, category grouping,
  FAQ, CollectionPage/Blog schema. Links to posts.
- **Posts (141 total):** migrate in prioritized waves. Each post: `post/<slug>.html`
  (preserve old URL path via redirect), Article schema (headline, author=Wasatch FAI,
  datePublished/Modified, image), answer-first intro, expanded/refreshed body, FAQ where
  natural, internal links to related condition/service pages. Batch, don't do all at once.
- Preserve old `/post/<slug>` URLs via Netlify redirects to the new files (SEO continuity).

## Site-level GEO/technical tasks

- Regenerate `sitemap.xml` to include every built page (absolute URLs).
- Add `llms.txt` at site root (clinic overview + key page list) for AI-search discovery.
- Shared clinic Organization/MedicalClinic JSON-LD (NAP for both locations) referenced by
  page-level schema (or embedded per page).
- Keep `robots.txt` allowing all + sitemap reference.
