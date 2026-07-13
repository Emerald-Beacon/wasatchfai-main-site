# Phase 1 Progress Ledger — WasatchFAI Homepage + Templates

Plan: docs/superpowers/plans/2026-07-12-wasatchfai-phase1-homepage-templates.md
Branch: rebuild-site

## Tasks
- Task 1: Scaffolding & shared assets — complete (570639f..038f494, review clean; dropdown CSS/JS adjudicated in-scope)
- Task 2: Homepage with carousel hero — PENDING
- Task 3: Condition detail template (plantar fasciitis) — PENDING
- Task 4: Services index — PENDING
- Task 5: Staff template — PENDING
- Task 6: Location template (Farmington) — PENDING
- Task 7: Simple content template (recovery) — PENDING
- Task 8: SEO / a11y / sitemap polish — PENDING

## Minor findings (for final review)
- Task 1: ensure every page <head> includes Google Fonts (Fraunces+Inter) link — partials are body-only. (owned by controller, enforced per template)
- Task 1: partials use root-relative paths; nested pages need ../ adjustment.
