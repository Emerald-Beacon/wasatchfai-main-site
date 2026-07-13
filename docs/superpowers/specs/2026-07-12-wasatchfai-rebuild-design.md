# WasatchFAI.com Rebuild — Design Spec

**Date:** 2026-07-12
**Status:** Approved (design), phased build

## Goal

Completely rebuild WasatchFAI.com as a warm, modern, inviting website for a local
foot & ankle clinic. Avoid the coldness of typical medical sites — it should feel
homey, like a neighborhood clinic. Recreate every page from the live site, migrate
all content (verbatim, then lightly polished) and all images, on a customized design.

## Approach (phased)

- **Phase 1:** Build the homepage + the reusable page templates (5 layouts). Get sign-off
  on the look and system.
- **Phase 2:** Scale out to all ~50 pages using the approved templates, migrating verbatim
  content and images from the live site.

Deferred to Phase 2 kickoff:
- Whether to use a full multi-agent **workflow** vs. batched parallel subagents for the 50-page build.
- Whether to recreate every individual **blog post** or ship a Blog index first.

## Design system

Formalized from the in-progress `homepage/index.html`, extracted into shared `css/site.css`.

- **Type:** Fraunces (serif headings) + Inter (body).
- **Palette:** blue `#1f5c8c` / `#15426a`, sage `#7ba087` / `#5a7e67`, sand `#f6f1e8`,
  cream `#fbf8f3`, warm orange CTA `#e8763a` / `#c95f25`, ink `#1d2733`.
- **Feel:** rounded cards (`--r:14px` / `--r-lg:24px`), soft layered shadows, generous
  spacing, reveal-on-scroll, lifestyle photography. "Neighbors treating neighbors."
- **Shared header** (top bar with both phone numbers + hours + socials; sticky main nav
  with a Services dropdown; Pay-a-Bill + Request-Appointment CTAs) and **footer**,
  hard-coded into every page for SEO (no JS-injected navigation).

## Information architecture

Mirrors the live site's ~50 URLs.

- **Primary nav:** Home · Staff · Services · Recovery · Locations · Blog · Contact
- **Conditions/Services (~25 detail pages):** achilles-tendonitis, ankle-fractures,
  arthritis, calcaneal-fractures, charcot-arthropathy, conscious-sedation,
  custom-orthotics, diabetic-foot-care, dual-syndesmosis-tightrope,
  fifth-metatarsal-fractures, flat-feet, gout, hallux-rigidus, ingrown-nails,
  lapiplasty, lateral-ankle-instability, limb-salvage, lisfranc-injuries,
  plantar-fasciitis, posterior-tibial-tendon, rheumatoid-arthritis, tailor-s-bunion,
  talar-dome-lesions, tarsal-tunnel-syndrome, toe-metatarsal-fractures, bunion-removal,
  heel-pain.
- **Locations:** Farmington, South Ogden + local-SEO landing pages (ogden,
  farmington-utah, ogden-utah-foot-doctor, wyoming, idaho).
- **Utility:** book-appointment, Pay a Bill (external InstaMed), patient-intake-forms
  (new-patient, medical-history, summary-of-npp), plans-pricing, recovery,
  recovery-instructions, shop, feedback, covid-19-response, staff, services,
  services-list.
- **Preserved:** existing heel-pain ad funnel (`index.html` w/ Meta Pixel) moves to
  `/heel-pain-procedure/` so paid campaigns keep working; the new homepage takes the root.

## Page templates (5 layouts → ~50 pages)

1. **Home** — carousel hero, how-we-help grid, about/lifestyle, partner promos
   (ARYSE, Wasatch CAP), team, insurance strip, contact/locations + form.
2. **Condition/Service detail** — hero image, verbatim content, symptoms/treatment
   blocks, related conditions, appointment CTA. One template → ~25 pages.
3. **Staff** — doctor cards: photo, name, credentials, bio.
4. **Location** — address, embedded map, hours, phone, per-location content.
5. **Simple content / form** — recovery, plans & pricing, patient forms, feedback,
   COVID, etc.

## Hero carousel (signature element)

Pure CSS/JS, no third-party library.

- 3 full-bleed warm lifestyle slides (hiking / trail-running / active family), each
  with its own headline + subhead + CTA.
- Auto-advance ~6s; dot indicators + prev/next arrows.
- Pause on hover; swipe on touch; keyboard accessible; honors
  `prefers-reduced-motion` (no auto-advance, static first slide).

## Content & image migration

- Scrape all live pages → capture verbatim text + image URLs (Phase 2 uses parallel agents).
- Light warmth polish on wording; **medical claims left unchanged**.
- Download every old-site image into `/images`; reuse doctor photos and lifestyle shots
  already present in `homepage/images/`.
- Wire appointment/feedback forms to **Netlify Forms** (consistent with recent commit
  `edd1939`).

## Technical

- Static HTML/CSS/JS, **no build step**. `netlify.toml` stays `publish = "."`.
- Per-page `<title>`, meta description, Open Graph tags for SEO.
- Regenerate `sitemap.xml` + `robots.txt`.
- Accessibility: semantic landmarks, alt text on all images, focus states, reduced-motion.

## Success criteria

- New homepage live at root with working, accessible carousel hero and warm design.
- 5 templates built and demonstrably reusable.
- After Phase 2: every live-site page recreated with migrated content + images, deploying
  cleanly to Netlify.
