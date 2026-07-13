# WasatchFAI.com Phase 1 — Homepage + Templates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the new warm, modern WasatchFAI.com homepage (with an auto-rotating carousel hero) plus the 5 reusable page templates, so Phase 2 can mass-produce the remaining ~50 pages.

**Architecture:** Static HTML/CSS/JS, no build step, deployed by Netlify with `publish = "."`. One shared `css/site.css` and `js/site.js` power every page. Header and footer are hard-coded into each HTML file (best SEO for a medical site). Five layout templates cover all page types; Phase 1 ships the homepage plus one real exemplar of each other template.

**Tech Stack:** Hand-written HTML5, CSS (custom properties, grid/fl ex), vanilla JS (IntersectionObserver, a small carousel), Google Fonts (Fraunces + Inter), Netlify Forms.

## Global Constraints

- No build step. Netlify `netlify.toml` stays `[build] publish = "."`.
- Fonts: `Fraunces` (headings) + `Inter` (body), loaded from Google Fonts.
- Palette (CSS custom properties, exact values): `--blue:#1f5c8c; --blue-dark:#15426a; --blue-soft:#eaf2f9; --sage:#7ba087; --sage-dark:#5a7e67; --sand:#f6f1e8; --cream:#fbf8f3; --orange:#e8763a; --orange-dark:#c95f25; --ink:#1d2733; --ink-soft:#4a5663; --muted:#7a8492; --line:#e7e2d8`.
- Two locations everywhere: Farmington 801-451-7500 (473 W. Bourne Circle, Suite 2, Farmington, UT 84025); South Ogden 801-627-2122 (945 Chambers Street, Suite 3, South Ogden, UT 84403). Email contactus@wasatchfai.com. Hours Mon–Thu 8a–5p, Fri 8a–12p.
- Pay a Bill links to `https://pay.InstaMed.com/WASATCHFOOT`.
- Every image needs descriptive `alt`. Every page needs unique `<title>`, meta description, OG tags. Honor `prefers-reduced-motion`.
- Content is verbatim-from-source + light warmth polish; medical claims unchanged.

## File Structure

- `index.html` — NEW homepage (carousel hero). Replaces current root.
- `heel-pain-procedure/index.html` — the existing heel-pain ad funnel (moved from root `index.html`, Meta Pixel preserved).
- `css/site.css` — shared design system (extracted from `homepage/index.html` styles) + carousel + template styles.
- `js/site.js` — shared JS: mobile nav toggle, reveal-on-scroll, carousel.
- `images/` — canonical image folder (promote `homepage/images/*` here; Phase 2 adds scraped images).
- `partials/header.html`, `partials/footer.html` — reference copies of the shared header/footer markup (source of truth for humans; the markup is hard-copied into each page).
- `plantar-fasciitis.html` — Template 2 exemplar (condition/service detail).
- `staff.html` — Template 3 exemplar.
- `farmington-utah.html` — Template 4 exemplar (location).
- `recovery.html` — Template 5 exemplar (simple content/form).
- `services.html` — services index (grid of all conditions).
- `docs/templates/` — annotated copies of each template with `{{PLACEHOLDER}}` markers for Phase 2.

---

### Task 1: Project scaffolding & shared assets

**Files:**
- Create: `css/site.css`, `js/site.js`, `partials/header.html`, `partials/footer.html`
- Create dir: `images/` (promote from `homepage/images/`)
- Move: root `index.html` → `heel-pain-procedure/index.html`

**Interfaces:**
- Produces: `css/site.css` (all shared classes: `.container .btn .topbar .header .footer .eyebrow .reveal` + palette `:root`), `js/site.js` (nav toggle + reveal observer), `partials/header.html` + `partials/footer.html` markup reused verbatim by all later tasks.

- [ ] **Step 1:** Move the heel-pain funnel: `mkdir -p heel-pain-procedure && git mv index.html heel-pain-procedure/index.html`. Fix its relative asset paths (root PNGs it references) to `../<file>`.
- [ ] **Step 2:** Create `images/` and copy the existing assets: `cp homepage/images/* images/`.
- [ ] **Step 3:** Create `css/site.css` by extracting the `<style>` block from `homepage/index.html` verbatim (palette `:root`, base, topbar, header, nav, buttons, sections, footer, reveal, responsive). Leave hero-specific rules; they will be replaced by carousel rules in Task 2.
- [ ] **Step 4:** Create `js/site.js` with the mobile-menu toggle and the IntersectionObserver reveal code currently inline in `homepage/index.html` (lines ~757–773). Wrap in `DOMContentLoaded`.
- [ ] **Step 5:** Extract the header markup (top bar + sticky header/nav) into `partials/header.html` and footer markup into `partials/footer.html`. Update nav links to real page URLs (`/staff.html`, `/services.html`, `/recovery.html`, `/farmington-utah.html`, `/blog.html`, `/feedback.html`, `https://pay.InstaMed.com/WASATCHFOOT`, `/book-appointment.html`). Add a Services dropdown listing the ~25 conditions.
- [ ] **Step 6: Verify** — open `heel-pain-procedure/index.html` in the browser; confirm it renders with images intact. Confirm `css/site.css` is valid (no unclosed braces) by loading a scratch HTML that links it.
- [ ] **Step 7: Commit** — `git add -A && git commit -m "Scaffold shared assets; relocate heel-pain funnel"`.

---

### Task 2: Homepage with carousel hero

**Files:**
- Create: `index.html` (new homepage)
- Modify: `css/site.css` (add `.hero-carousel*` rules), `js/site.js` (add carousel controller)

**Interfaces:**
- Consumes: header/footer partials, `css/site.css`, `js/site.js` from Task 1.
- Produces: `initCarousel()` in `js/site.js` bound to `.hero-carousel` (auto-advance 6s, dots, arrows, pause-on-hover, swipe, reduced-motion aware).

- [ ] **Step 1:** Build `index.html` starting from `homepage/index.html` body, swapping inline `<style>`/`<script>` for `<link rel="stylesheet" href="css/site.css">` and `<script src="js/site.js" defer></script>`, and hard-coding the header/footer partials. Keep sections: how-we-help, about, ARYSE promo, Wasatch CAP promo, team, insurance, contact/locations + Netlify form.
- [ ] **Step 2:** Replace the static hero with carousel markup:

```html
<section class="hero-carousel" aria-roledescription="carousel" aria-label="Welcome">
  <div class="hero-track">
    <div class="hero-slide is-active" style="--img:url('images/hero-mountain-biking.jpg')">
      <div class="container hero-slide-inner">
        <span class="eyebrow">Northern Utah · Farmington & South Ogden</span>
        <h1>Keep moving. We'll keep you <em>on the trail.</em></h1>
        <p class="hero-lede">From the slightest discomfort to chronic pain, we find the source and get you back to the life you love.</p>
        <div class="hero-cta"><a href="book-appointment.html" class="btn btn-primary btn-arrow">Request Appointment</a>
        <a href="tel:8014517500" class="btn btn-ghost hero-ghost">Call Us Today</a></div>
      </div>
    </div>
    <div class="hero-slide" style="--img:url('images/hero-card-1.jpg')"> ...slide 2 headline + CTA... </div>
    <div class="hero-slide" style="--img:url('images/hero-card-3.jpg')"> ...slide 3 headline + CTA... </div>
  </div>
  <button class="hero-arrow prev" aria-label="Previous slide">‹</button>
  <button class="hero-arrow next" aria-label="Next slide">›</button>
  <div class="hero-dots" role="tablist" aria-label="Choose slide"></div>
</section>
```

- [ ] **Step 3:** Add carousel CSS to `css/site.css`: full-bleed slides, dark gradient overlay over `var(--img)` for text legibility, absolute-stacked slides with opacity crossfade, `.is-active{opacity:1}`, styled arrows + dots, `@media(prefers-reduced-motion:reduce)` disables transitions.
- [ ] **Step 4:** Add `initCarousel()` to `js/site.js`: builds dots from slide count, `goTo(i)` toggles `is-active` + `aria-selected`, auto-advance `setInterval(6000)` cleared on `mouseenter`/touch and restarted on leave, arrow + dot click handlers, touch swipe (track `touchstart`/`touchend` deltaX), and `if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;` before starting the timer.
- [ ] **Step 5: Verify** — open `index.html`; confirm slides auto-advance, arrows/dots work, hover pauses, mobile swipe works (narrow the window + devtools touch), and reduced-motion (emulate in devtools) stops auto-advance. Check the reveal-on-scroll still fires for lower sections. Check responsive at 375px / 768px / 1280px.
- [ ] **Step 6: Commit** — `git add -A && git commit -m "Build homepage with auto-rotating carousel hero"`.

---

### Task 3: Condition/Service detail template (exemplar: Plantar Fasciitis)

**Files:**
- Create: `plantar-fasciitis.html`, `docs/templates/condition.html`
- Modify: `css/site.css` (add `.detail-*` rules)

**Interfaces:**
- Consumes: header/footer, `site.css`, `site.js`.
- Produces: the condition template structure Phase 2 clones (`.detail-hero`, `.detail-body`, `.detail-aside`, related-conditions grid, CTA band).

- [ ] **Step 1:** Fetch the live content: `https://www.wasatchfai.com/plantar-fasciitis` — capture heading, body copy, any images verbatim.
- [ ] **Step 2:** Build `plantar-fasciitis.html`: breadcrumb (Home / Services / Plantar Fasciitis), `.detail-hero` (condition name + one-line summary + hero image), two-column `.detail-body` (verbatim polished content) + `.detail-aside` (sticky "Request an appointment" card with both phones), a "Related conditions" card grid, and a warm CTA band before the footer. Unique `<title>`/meta/OG.
- [ ] **Step 3:** Add `.detail-*` styles to `css/site.css`.
- [ ] **Step 4:** Save a genericized copy to `docs/templates/condition.html` with `{{CONDITION_NAME}}`, `{{SUMMARY}}`, `{{HERO_IMG}}`, `{{BODY_HTML}}`, `{{RELATED}}`, `{{TITLE}}`, `{{META_DESC}}` markers.
- [ ] **Step 5: Verify** — render `plantar-fasciitis.html`; check reading width, sticky aside behavior, responsive collapse to one column, alt text present.
- [ ] **Step 6: Commit** — `git add -A && git commit -m "Add condition detail template (plantar fasciitis exemplar)"`.

---

### Task 4: Services index page

**Files:**
- Create: `services.html`
- Modify: `css/site.css` if needed (reuse `.help-grid`/`.help-card`)

**Interfaces:**
- Consumes: header/footer, `site.css`, `.help-card` styles.
- Produces: the services index linking every condition page (Phase 2 fills all 25 links).

- [ ] **Step 1:** Build `services.html`: intro ("Most Common Services" + "Call us for same-day emergencies — ingrown toenails, sprains, breaks, etc."), a searchable/filterable grid of all ~25 conditions as cards (name + one-line + link). Grid cards link to each condition page (`plantar-fasciitis.html` live now; others are stubs until Phase 2).
- [ ] **Step 2: Verify** — render; confirm grid is responsive and the Plantar Fasciitis card links correctly.
- [ ] **Step 3: Commit** — `git add -A && git commit -m "Add services index page"`.

---

### Task 5: Staff template

**Files:**
- Create: `staff.html`, `docs/templates/staff.html`

**Interfaces:**
- Consumes: header/footer, `site.css`, `.team-*` styles (from homepage).
- Produces: doctor-card layout reused as-is (single page, not cloned).

- [ ] **Step 1:** Fetch `https://www.wasatchfai.com/staff` — capture each doctor's name, credentials, bio verbatim.
- [ ] **Step 2:** Build `staff.html`: page hero, one section per physician with photo (`images/dr-campbell.jpg`, `dr-frost.jpg`, `dr-woolley.jpg`, `dr-murrah.jpg`), name, credentials, bio; warm "meet the team" framing; CTA band. Genericize to `docs/templates/staff.html`.
- [ ] **Step 3: Verify** — render; check photos load, bios readable, responsive stack.
- [ ] **Step 4: Commit** — `git add -A && git commit -m "Add staff page + template"`.

---

### Task 6: Location template (exemplar: Farmington)

**Files:**
- Create: `farmington-utah.html`, `docs/templates/location.html`
- Modify: `css/site.css` (add `.loc-*` rules)

**Interfaces:**
- Consumes: header/footer, `site.css`, `site.js`.
- Produces: location template Phase 2 clones for South Ogden + geo pages (`{{CITY}}`, `{{ADDRESS}}`, `{{PHONE}}`, `{{FAX}}`, `{{MAP_EMBED}}`, `{{BODY}}`).

- [ ] **Step 1:** Fetch `https://www.wasatchfai.com/farmington-utah` — capture verbatim content.
- [ ] **Step 2:** Build `farmington-utah.html`: hero, address/phone/fax/hours block, embedded Google Map iframe for the Farmington address, per-location content, both clinics cross-linked, appointment CTA + Netlify-wired mini form. Genericize to `docs/templates/location.html`.
- [ ] **Step 3:** Add `.loc-*` styles.
- [ ] **Step 4: Verify** — render; map iframe loads, hours/phones correct, responsive.
- [ ] **Step 5: Commit** — `git add -A && git commit -m "Add location template (Farmington exemplar)"`.

---

### Task 7: Simple content/form template (exemplar: Recovery)

**Files:**
- Create: `recovery.html`, `docs/templates/simple.html`
- Modify: `css/site.css` (add `.prose` rules)

**Interfaces:**
- Consumes: header/footer, `site.css`.
- Produces: `.prose` article layout + generic template Phase 2 clones for recovery-instructions, plans-pricing, patient forms, feedback, COVID, etc.

- [ ] **Step 1:** Fetch `https://www.wasatchfai.com/recovery` — capture verbatim content.
- [ ] **Step 2:** Build `recovery.html`: page hero + centered `.prose` article with the migrated content + CTA band. Genericize to `docs/templates/simple.html` with `{{TITLE}}`, `{{INTRO}}`, `{{BODY_HTML}}`.
- [ ] **Step 3:** Add `.prose` styles (comfortable reading measure, heading rhythm, lists, blockquotes).
- [ ] **Step 4: Verify** — render; check reading width and typography rhythm.
- [ ] **Step 5: Commit** — `git add -A && git commit -m "Add simple content template (recovery exemplar)"`.

---

### Task 8: Cross-cutting polish, SEO, and Phase-1 review

**Files:**
- Create: `robots.txt`, `sitemap.xml` (Phase-1 pages only), `404.html`
- Modify: all Phase-1 pages (meta/OG audit), `partials/*` if nav needs fixes

**Interfaces:**
- Consumes: all pages built above.

- [ ] **Step 1:** Add per-page `<title>`, meta description, and OG tags where missing; verify nav links resolve to real files or clearly-stubbed ones.
- [ ] **Step 2:** Create `robots.txt` (allow all, point to sitemap) and a Phase-1 `sitemap.xml`; add a friendly on-brand `404.html`.
- [ ] **Step 3:** Confirm Netlify form(s) have `data-netlify="true"`, `name`, hidden `form-name`, and honeypot (match commit `edd1939`).
- [ ] **Step 4: Verify (full pass)** — open every Phase-1 page; run through at 375/768/1280px; keyboard-tab the header + carousel; emulate reduced-motion; check color contrast on orange/blue CTAs; confirm no broken images or console errors.
- [ ] **Step 5:** Deploy preview: `netlify deploy` (draft) if available, and eyeball the deploy URL. (Optional — skip if not authenticated.)
- [ ] **Step 6: Commit** — `git add -A && git commit -m "Phase 1 SEO, 404, sitemap, and a11y polish"`.

---

## Self-Review

**Spec coverage:** design system → Task 1/2; carousel hero → Task 2; 5 templates → Tasks 2–7; services IA → Task 4; heel-pain funnel preserved → Task 1; Netlify forms → Task 2/6/8; SEO/sitemap/robots → Task 8; a11y/reduced-motion → Tasks 2 & 8; image reuse → Task 1. Phase 2 (mass page build, blog posts, workflow-vs-subagents) intentionally out of scope. No gaps.

**Placeholder scan:** `{{...}}` markers appear only inside `docs/templates/*` deliverables (intended), not as unfinished plan steps. No TBD/TODO in task steps.

**Type consistency:** `initCarousel()` referenced consistently (Task 2). Shared classes (`.container`, `.btn`, `.help-card`, `.team-photo`, `.eyebrow`, `.reveal`) named identically to `homepage/index.html` source. Template placeholder names consistent between each build task and its `docs/templates/*` copy.
