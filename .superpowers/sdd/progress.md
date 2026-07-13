# Phase 1 Progress Ledger — WasatchFAI Homepage + Templates

Plan: docs/superpowers/plans/2026-07-12-wasatchfai-phase1-homepage-templates.md
Branch: rebuild-site

## Tasks
- Task 1: Scaffolding & shared assets — complete (570639f..038f494, review clean; dropdown CSS/JS adjudicated in-scope)
- Task 2: Homepage with carousel hero — complete (c99ac6d..f562279, review clean; minors deferred to Task 8)
- Task 3: Condition detail template (plantar fasciitis) — complete (0da7762..a07afcc, review clean; minors deferred to Task 8)
- Task 4: Services index — PENDING
- Task 5: Staff template — PENDING
- Task 6: Location template (Farmington) — PENDING
- Task 7: Simple content template (recovery) — PENDING
- Task 8: SEO / a11y / sitemap polish — PENDING

## Minor findings (for final review)
- Task 1: ensure every page <head> includes Google Fonts (Fraunces+Inter) link — partials are body-only. (owned by controller, enforced per template)
- Task 1: partials use root-relative paths; nested pages need ../ adjustment.
- Task 3 (Minor, do in Task 8): hero uses CSS background-image with no alt/aria-label (affects .hero-slide sitewide + .detail-hero) — add aria-label or visually-hidden text; wire {{HERO_ALT}} in docs/templates/condition.html into that aria-label.
- Task 3 (verify in final review): spot-check plantar-fasciitis.html medical copy fidelity vs live wasatchfai.com/plantar-fasciitis.
- Task 2 (Minor, do in Task 8): add touchcancel->start() on carousel track; tokenize hero overlay color (rgba 21,66,106) or add --overlay; optionally complete ARIA tab/tabpanel wiring (aria-controls/id).
