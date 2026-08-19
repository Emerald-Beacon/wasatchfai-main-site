# Autonomous Publishing Runbook — wasatchfai.com

Wasatch Foot & Ankle Institute's blog publishes itself. A scheduled Claude cloud
routine ("routine") fires twice a week, writes one article from the queue below,
sources an image, wires it into the site, pushes to `main`, and confirms the URL
is live. **No human reviews the post before it goes public.**

This file is the human-readable source of truth. The live prompt lives inside the
routine. Edit this file, then ask Claude to sync the routine to match.

---

## At a glance

| | |
|---|---|
| **Routine name** | `WasatchFAI MAIN — Auto Blog (Tue/Thu)` |
| **Routine ID** | `trig_013uiBDib2mRnjDfUxrfnE46` |
| **Dashboard** | https://claude.ai/code/routines/trig_013uiBDib2mRnjDfUxrfnE46 |
| **Schedule** | `0 17 * * 2,4` **UTC** = **11:00 AM Mountain (MDT)** / 10:00 AM (MST) Tue + Thu |
| **Repo** | `github.com/Emerald-Beacon/wasatchfai-main-site` |
| **Branch** | `main` |
| **Mode** | Direct push to `main`; Netlify auto-deploys. Falls back to a PR if the push is rejected |
| **Model** | `claude-opus-4-8` (YMYL medical — guardrails are legally sensitive) |
| **Imagery** | Unsplash, downloaded into `images/` and committed |
| **Strategy doc** | `EDITORIAL-CALENDAR-2026-Q3-Q4.md` |
| **First fire** | Thursday, 2026-08-20 |

⚠️ **There are two WasatchFAI sites.** This routine is for the **MAIN** site
(`wasatchfai.com`, repo `wasatchfai-main-site`). The **Heel Pain** site
(repo `wasatch-heel-website`) is a separate property with its own Netlify project
and has **no** publishing routine. The prompt makes the agent verify `git remote -v`
and abort on a mismatch before it writes anything.

---

## How the queue works (idempotent — this is the important part)

The routine has **no memory between runs.** Each fire it walks the queue top to
bottom and publishes **the first item whose `post/<slug>.html` does not yet exist.**

Consequences, all of them good:
- A **missed run self-heals** — the next fire picks up where it left off.
- A **double fire never duplicates** — the second one sees the file and moves on.
- The queue is **advanced by the filesystem**, not by a counter someone has to maintain.
- When every item exists, the agent **stops** and reports
  `QUEUE EXHAUSTED — needs new topics from Josh.` It will **not** invent a topic.

Refresh items are the exception: they edit an existing file, so they can't be
detected by absence. They are marked `REFRESH` in the queue and gated on a
`<!-- refreshed:<slug>:YYYY -->` marker comment the agent writes into the file.

---

## The queue

Dates are the calendar's intent, not a hard binding — the queue is positional.

### New articles

| # | Slug | Title | Cluster | Format | Target keyword |
|---:|---|---|---|---|---|
| 1 | `insertional-vs-midportion-achilles-tendonitis` | Insertional vs. Midportion Achilles Tendonitis: Why the Location Changes Treatment | Achilles Tendon & Sports Injuries | comparison | insertional achilles tendonitis |
| 2 | `sever-s-disease-heel-pain-in-young-athletes` | Sever's Disease: Heel Pain in Growing Young Athletes | Achilles Tendon & Sports Injuries | how-to-guide | sever's disease heel pain kids |
| 3 | `what-causes-bunions-genetics-shoes-or-both` | What Causes Bunions: Genetics, Shoes, or Both? | Bunions & Toe Deformities | faq-knowledge | what causes bunions |
| 4 | `lapiplasty-vs-traditional-bunion-surgery` | Lapiplasty vs. Traditional Bunion Surgery: How the Two Approaches Differ | Bunions & Toe Deformities | comparison | lapiplasty vs traditional bunion surgery |
| 5 | `REFRESH` | → `post/what-you-need-to-know-about-plantar-fasciitis.html` | Heel & Arch Pain | refresh | plantar fasciitis treatment |
| 6 | `hiking-boots-for-utah-trails-preventing-foot-injuries` | Hiking Boots for Utah Trails: Preventing Foot and Ankle Injuries | Orthotics & Footwear | how-to-guide | hiking boots foot pain |
| 7 | `turf-toe-what-athletes-need-to-know` | Turf Toe: What Athletes Need to Know About a Sprained Big Toe | Achilles Tendon & Sports Injuries | how-to-guide | turf toe treatment |
| 8 | `non-surgical-bunion-relief-what-actually-helps` | Non-Surgical Bunion Relief: What Actually Helps | Bunions & Toe Deformities | how-to-guide | non surgical bunion treatment |
| 9 | `REFRESH` | → `post/sprained-ankle-here-s-when-you-need-a-doctor.html` | Ankle Injuries & Instability | refresh | sprained ankle see a doctor |
| 10 | `morton-s-neuroma-symptoms-and-treatment` | Morton's Neuroma: Why It Feels Like a Pebble in Your Shoe | Arthritis, Nerve & Circulation | how-to-guide | morton's neuroma treatment |
| 11 | `navicular-stress-fractures-in-athletes` | Navicular Stress Fractures: The Injury Runners Miss | Fractures & Foot Trauma | how-to-guide | navicular stress fracture |
| 12 | `hallux-rigidus-vs-bunion-telling-big-toe-problems-apart` | Hallux Rigidus vs. Bunion: Telling Big-Toe Problems Apart | Bunions & Toe Deformities | comparison | hallux rigidus vs bunion |
| 13 | `how-long-does-a-foot-fracture-take-to-heal` | How Long Does a Foot Fracture Take to Heal? | Fractures & Foot Trauma | faq-knowledge | how long foot fracture heal |
| 14 | `achilles-tendon-rupture-surgery-vs-nonsurgical-treatment` | Achilles Tendon Rupture: Surgery vs. Non-Surgical Treatment | Achilles Tendon & Sports Injuries | comparison | achilles rupture surgery or not |
| 15 | `REFRESH` | → `post/heel-spur-treatment-options.html` | Heel & Arch Pain | refresh | heel spur treatment |
| 16 | `walking-boot-vs-cast-which-one-and-why` | Walking Boot vs. Cast: Which One, and Why | Fractures & Foot Trauma | comparison | walking boot vs cast |
| 17 | `how-custom-orthotics-are-made-scan-to-fit` | How Custom Orthotics Are Made: From Scan to Fit | Orthotics & Footwear | tutorial | how are custom orthotics made |
| 18 | `eccentric-heel-drops-for-achilles-tendonitis` | Eccentric Heel Drops: The Exercise That Works for Achilles Tendonitis | Achilles Tendon & Sports Injuries | tutorial | eccentric heel drops achilles |
| 19 | `recovering-from-lapiplasty-week-by-week` | Recovering From Lapiplasty, Week by Week | Bunions & Toe Deformities | how-to-guide | lapiplasty recovery timeline |
| 20 | `big-toe-arthritis-treatment-options-beyond-fusion` | Big-Toe Arthritis: Treatment Options Beyond Fusion | Arthritis, Nerve & Circulation | how-to-guide | big toe arthritis treatment |
| 21 | `REFRESH` | → `post/toe-nail-fungus-removal-options.html` | Nails & Skin Conditions | refresh | toenail fungus removal |
| 22 | `diabetic-foot-ulcers-stages-and-treatment` | Diabetic Foot Ulcers: Stages, Treatment, and Why Speed Matters | Diabetic Foot Care | how-to-guide | diabetic foot ulcer treatment |
| 23 | `why-diabetic-neuropathy-hides-foot-injuries` | Why Diabetic Neuropathy Hides Foot Injuries | Diabetic Foot Care | faq-knowledge | diabetic neuropathy foot injury |
| 24 | `charcot-foot-what-diabetics-should-know` | Charcot Foot: What People With Diabetes Should Know | Diabetic Foot Care | how-to-guide | charcot foot diabetes |
| 25 | `choosing-diabetic-shoes-and-inserts` | Choosing Diabetic Shoes and Inserts | Diabetic Foot Care | how-to-guide | diabetic shoes inserts |
| 26 | `ski-and-snowboard-boot-fit-and-foot-pain` | Ski and Snowboard Boot Fit: Why Your Feet Hurt on the Mountain | Orthotics & Footwear | how-to-guide | ski boot foot pain |
| 27 | `REFRESH` | → `post/foot-pain-101-identifying-the-root-causes-and-finding-relief.html` | General Foot Health & Wellness | refresh | foot pain causes |
| 28 | `limb-salvage-when-amputation-isn-t-the-only-option` | Limb Salvage: When Amputation Isn't the Only Option | Diabetic Foot Care | how-to-guide | limb salvage foot |
| 29 | `winter-boots-and-foot-pain-in-utah` | Winter Boots and Foot Pain in Utah | Orthotics & Footwear | how-to-guide | winter boots foot pain |
| 30 | `tailor-s-bunion-bunionette-explained` | Tailor's Bunion (Bunionette): Why the Outside of Your Foot Hurts | Bunions & Toe Deformities | how-to-guide | tailor's bunion |
| 31 | `returning-to-sport-after-a-foot-or-ankle-injury` | Returning to Sport After a Foot or Ankle Injury | Achilles Tendon & Sports Injuries | how-to-guide | return to sport after ankle injury |
| 32 | `high-altitude-hiking-and-foot-swelling-in-utah` | High-Altitude Hiking and Foot Swelling in Utah | Orthotics & Footwear | faq-knowledge | feet swelling hiking altitude |
| 33 | `plantar-fasciitis-in-runners-utah-trails` | Plantar Fasciitis in Runners: Training on Utah's Hard-Packed Trails | Heel & Arch Pain | how-to-guide | plantar fasciitis runners |
| 34 | `youth-sports-preventing-foot-and-ankle-injuries` | Youth Sports: Preventing Foot and Ankle Injuries | Achilles Tendon & Sports Injuries | how-to-guide | youth sports foot injury prevention |
| 35 | `stress-fracture-vs-shin-splints-vs-tendonitis` | Stress Fracture vs. Shin Splints vs. Tendonitis | Fractures & Foot Trauma | comparison | stress fracture vs shin splints |

**35 items ≈ 17.5 weeks ≈ mid-December 2026.** Top the queue up before then or the
routine will start reporting `QUEUE EXHAUSTED`.

---

## Guardrails — YMYL medical, no human pre-review

These are in the routine prompt, most consequential first. This is a medical
practice publishing health information with no editor between the model and the
public, so the rules are absolute, not preferences.

1. **No prices, ever.** Not for a procedure, a visit, an orthotic, or an imaging
   study. Not a range, not "typically around", not "many insurers cover".
   Insurance questions route to `/plans-pricing` and the phone number.
2. **No clinical guarantees.** Never "cure", "painless", "permanent fix",
   "guaranteed", "risk-free", "no downtime", or "you will recover in N weeks".
   Recovery is described as varying by patient and confirmed by their surgeon.
3. **No fabricated statistics.** A number ships only with a real, reputable,
   inline-linked source the agent verified with WebSearch/WebFetch actually exists
   and actually says that. Preferred sources: peer-reviewed journals, ACFAS, APMA,
   AOFAS, CDC, NIH/NIDDK, ADA, AAOS. **No** content-farm or competitor-clinic
   citations. If it can't be verified, the number is dropped and the claim is
   written qualitatively.
4. **Never invent people, credentials, or capabilities.** Only the four physicians
   named in FACTS, with exactly those credentials. No invented awards,
   certifications, device brands the clinic hasn't published, patient volumes,
   outcomes data, testimonials, or "same-day availability" promises.
5. **No individualized medical advice.** Content is general education. Every article
   carries the `detail-reviewed` disclaimer paragraph from the template and steers
   the reader to an in-person evaluation.
6. **Emergency framing must stay intact.** Red-flag symptoms (loss of sensation,
   non-weight-bearing, spreading redness/fever, a wound that won't heal in a
   diabetic foot) always direct the reader to call the clinic or seek urgent care —
   never "wait and see".
7. **Do not modify existing posts** other than the explicit `REFRESH` items, and
   never rename or delete a post — the URLs are indexed.
8. **No duplicate or near-duplicate content.** See the uniqueness gate below.

---

## The uniqueness gate (STEP 1.5 in the prompt)

The site already carries several near-duplicate sets, so the routine runs a
**mandatory overlap check before it writes a word.** Writing about the same
*subject* as an existing post is fine and expected. Writing the same *article*
again is not.

Each run the agent must:
1. Grep `post/` and `blog.html` for the key terms in its title to find neighbours.
2. **Read the 2–4 closest existing articles in full** — not skim the filenames.
3. Pass all three tests: its central question isn't already answered; at least half
   its `<h2>` sections cover new ground; it doesn't restate their advice in new words.
4. If it overlaps, **narrow and differentiate rather than skip** — take the angle the
   existing posts leave open (a comparison none of them draws, a population none of
   them addresses, a stage of care they skip, a decision they don't help the reader
   make). The queue item still ships.
5. Not reuse a neighbour's `<h2>` outline or FAQ questions.
6. **Link to the 2–3 closest siblings** with descriptive anchor text — turning a
   would-be competitor into a cluster. These count toward its internal-link quota.
7. Never match an existing `<h3>` title in `blog.html` exactly.

STEP 6 repeats the check after drafting (open the closest neighbour side by side;
rewrite if any two sections make the same argument or any FAQ question repeats),
and STEP 9 requires the agent to report which posts it read and how its article
differs — so you can audit the judgement in the dashboard, not just trust it.

This does **not** clean up the existing duplicates. That's still a human job — see
*Cannibalization* in the calendar.

### Routed to a human, deliberately kept out of the queue

- **Pricing, insurance, and financing content** — rule 1 makes it unwritable.
- **Anything naming a specific patient case or outcome** — no verifiable source.
- ~~`what-to-know-about-bunion-surgery-in-2025`~~ — **done 2026-08-19.** Renamed to
  `/post/what-to-know-about-bunion-surgery`, title de-yeared, old URL 301'd.
- ~~Cannibalization cleanup~~ — **done 2026-08-19.** See *Consolidation* below.

## Consolidation — done 2026-08-19

The blog carried five sets of near-duplicate posts competing with each other.
Ten were retired into seven survivors; the library went **124 → 114**. Unique
material was merged into the survivor first, and every retired URL 301s
permanently (registered in `build-extensionless.py`'s `RETIRED` list, because
`_redirects` is regenerated from disk and a hand-added rule there would be wiped).

| Retired | Redirects to |
|---|---|
| `how-to-fix-ankle-instability-for-good` | `chronic-ankle-instability-treatment-and-exercises` |
| `is-your-ankle-instability-holding-you-back-…` | `what-is-chronic-ankle-instability-cai` |
| `why-your-chronic-ankle-instability-keeps-coming-back` | `why-does-chronic-ankle-instability-return` |
| `toenail-fungus-removal` | `toe-nail-fungus-removal-options` |
| `treating-toenail-fungus-and-ingrown-nails` | `toe-nail-fungus-removal-options` |
| `ingrown-nail-care-guide-…` | `long-term-ingrown-toenail-prevention-and-home-treatment` |
| `what-are-the-cause-s-of-ingrown-toenails-…` | `long-term-ingrown-toenail-prevention-and-home-treatment` |
| `hammer-toe-effective-treatment-options` | `advanced-hammertoe-treatment-options` |
| `have-hammertoes-your-guide-…` | `advanced-hammertoe-treatment-options` |
| `what-is-a-dual-syndesmosis-tightrope-…` | `understanding-the-dual-syndesmosis-tightrope-…` |

Content merged rather than dropped: the **partial/complete nail removal procedure**
section moved into the ingrown-toenail survivor, which had no procedure detail.
The hammertoe survivor already covered flexible vs. rigid and the ankle survivor
already covered bracing and footwear, so those needed no merge.

Cluster counts after: Ankle 16→13, Nails & Skin 12→8, Bunions & Toe 6→4,
Surgery & Recovery 12→11.

⚠️ Queue item 21 originally refreshed `toenail-fungus-removal`, now retired. It
points at `toe-nail-fungus-removal-options` instead.

---

## Integration points — 6 edits per post

Missing any one leaves the site inconsistent.

1. **`post/<slug>.html`** — the article. Built by copying
   `post/when-foot-pain-isn-t-normal.html`, the canonical structural template.
2. **`blog.html`** — insert an alphabetically-placed `related-card` anchor into the
   correct cluster's `related-grid`, **and increment that cluster's
   `<span class="eyebrow">N Articles</span>` count.** Both, or the page lies.
3. **`images/<slug>-hero.jpg`** — the downloaded Unsplash photo, committed.
4. **`blog.html` JSON-LD** — regenerated by `python3 build-blog-schema.py`. The page
   lists its articles **twice**: the visible cards above, and a
   `Blog > mainEntity > ItemList` in the JSON-LD. That list is flat, globally
   slug-sorted, and contiguously numbered, so inserting one entry renumbers every
   entry after it (the first post landed at position 54 and shifted 71 others).
   Too error-prone to hand-edit — the script derives it from the cards, so the two
   can no longer disagree. Do not hand-edit.
5. **`sitemap.xml`** — regenerated by `python3 build-sitemap.py`. Do not hand-edit;
   it derives `<lastmod>` from real git dates and assigns priority tiers.
6. **`_redirects`** — regenerated by `python3 build-extensionless.py`, which adds the
   forced `301` from `/post/<slug>.html` to the canonical extensionless
   `/post/<slug>`. Do not hand-edit.

**`llms.txt` needs no per-post edit** — it lists the blog as a whole
(`https://wasatchfai.com/blog`), not individual articles.

### Known gaps

- **There is no `rss.xml`.** The other house sites have one; this one never did.
  Adding it means creating the file, linking it from every page's `<head>`, and
  adding a sixth integration step. Not done — decide whether it's worth it.
- The hero image is a CSS `background-image` on `.detail-hero`, **not an `<img>`**.
  A new post needs the image path swapped in the inline `style` attribute *and* in
  `og:image`, `twitter:image`, and the JSON-LD `image` field (absolute URLs there).

---

## URL and file conventions

| | |
|---|---|
| Article file | `post/<slug>.html` |
| Live URL | `https://wasatchfai.com/post/<slug>` (**extensionless is canonical**) |
| Canonical tag | must be the extensionless form |
| Repo root | **is** the site root — `publish = "."` in `netlify.toml` |
| Build step | none; plain static HTML. The `build-*.py` scripts are local generators, not a Netlify build |
| Deploy | Netlify auto-deploys on push to `main`. No build hook to POST |

---

## Secrets

The routine prompt contains the **Unsplash access key inlined**, because cloud
agents get no local environment — `~/.claude/settings.json` `env` values are not
present in the sandbox. The prompt is stored privately in the routine.

🔒 **The Unsplash key must never be committed to this repo.** It is not in this
file and must not be added to it, to any script, or to any HTML.

---

## To change things

| Want to | Do this |
|---|---|
| Add/remove/reorder topics | Edit the queue above, then ask Claude to sync the routine prompt |
| Change the schedule | `RemoteTrigger` `update` with a new `cron_expression` (**UTC**) |
| Pause publishing | `RemoteTrigger` `update` with `{"enabled": false}` |
| Publish one now, off-schedule | `RemoteTrigger` `run` — **this publishes live** |
| See what a run did | `RemoteTrigger` `list_runs` then `get_run_log`, or the dashboard link above |
| Switch to PR-gated | Change STEP 7 of the prompt to always branch + `gh pr create` |
| Tighten a guardrail | Edit the guardrails above, then sync the prompt. Put the most important rule first — models weight early instructions more |

### Verify a run independently — don't trust the agent's self-report

```bash
curl -sI https://wasatchfai.com/post/<slug> | head -1        # expect 200
git -C . fetch && git -C . log origin/main -1 --stat          # expect the new commit
python3 -c "import json,re,sys; h=open('post/<slug>.html').read(); \
  [json.loads(m) for m in re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>',h,16)]" \
  && echo "JSON-LD OK"
grep -c 'when-foot-pain-isn-t-normal' post/<slug>.html        # expect 0 — no template leakage
```

---

## Commit status

`EDITORIAL-CALENDAR-2026-Q3-Q4.md` and this runbook are **written to the working
tree but not committed.** This repo has strict commit rules (see
`Websites/CLAUDE.md`) — commit only when asked. The routine itself is live and
does not depend on either file being committed.
