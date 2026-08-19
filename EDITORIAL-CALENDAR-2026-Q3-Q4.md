# Editorial Calendar — wasatchfai.com
## Wasatch Foot & Ankle Institute · Aug 20 – Nov 26, 2026

Generated 2026-08-18 by `blog-autopilot` + `claude-blog:blog-calendar`.
This is the **strategy document**. The machine reads the queue in
`AUTONOMOUS-PUBLISHING-RUNBOOK.md`, which is derived from this file.

---

## Starting position

| | |
|---|---|
| Existing posts | **123**, at `post/<slug>.html`, served at `/post/<slug>` |
| Newest post | `when-foot-pain-isn-t-normal` — **2026-02-02** |
| Blog status | **Dormant ~6.5 months** |
| `dateModified` on every post | `2026-07-13` — a uniform bulk stamp, carries no signal |
| Cadence chosen | **2×/week, Tuesday + Thursday** |
| Publish gate | Auto-push to `main` (Netlify auto-deploys) |
| Imagery | Unsplash, downloaded into `images/` and committed |

### Goals (all four selected)
1. **Local SEO** — Davis County (Farmington clinic) & Weber County (South Ogden clinic)
2. **GEO / AI citation** — answer-first passages, FAQPage schema, definitional openers
3. **Lead gen** — route to `/book-appointment` and the matching service page
4. **Topical authority** — fill the thin clusters, don't pile onto the deep ones

---

## Cluster coverage: where the gaps are

| Cluster (as titled on `blog.html`) | Now | Planned adds | End of quarter |
|---|---:|---:|---:|
| General Foot Health & Wellness | 21 | 0 | 21 |
| Ankle Injuries & Instability | 16 | 0 | 16 |
| Heel & Arch Pain | 13 | 1 | 14 |
| Nails & Skin Conditions | 12 | 0 | 12 |
| Surgery & Recovery | 12 | 0 | 12 |
| Arthritis, Nerve & Circulation | 11 | 2 | 13 |
| Fractures & Foot Trauma | 10 | 3 | 13 |
| Orthotics & Footwear | 10 | 4 | 14 |
| **Achilles Tendon & Sports Injuries** | **6** | **6** | **12** |
| **Diabetic Foot Care** | **6** | **5** | **11** |
| **Bunions & Toe Deformities** | **6** | **6** | **12** |

**Strategy:** the three 6-article clusters get doubled. General Foot Health (21)
and Ankle Injuries (16) get **nothing** — they are saturated and further posts
there would cannibalize. Note Ankle Instability alone already has 8 near-identical
posts ("Why Does Chronic Ankle Instability Return?", "Why Your Chronic Ankle
Instability Keeps Coming Back", "How to Fix Ankle Instability for Good",
"What Is Chronic Ankle Instability (CAI)?"…) — see *Cannibalization* below.

---

## Content decay report

`dateModified` is a uniform `2026-07-13` across all 123 posts, so it is useless
for prioritization. Ranked instead by **real publish age × commercial intent**.

| Post | Published | Age | Priority | Why |
|---|---|---:|---|---|
| ~~`what-to-know-about-bunion-surgery-in-2025`~~ | 2025-11-06 | — | ~~Critical~~ **Fixed 2026-08-19** | Renamed to `/post/what-to-know-about-bunion-surgery`, old URL 301'd |
| `what-you-need-to-know-about-plantar-fasciitis` | 2019-06-13 | 7yr | **Critical** | Highest-intent topic on the site; oldest treatment info |
| `sprained-ankle-here-s-when-you-need-a-doctor` | 2019-03-19 | 7yr | High | Urgent-intent query, heavy search volume |
| `heel-spur-treatment-options` | 2021-01-01 | 5.6yr | High | Treatment options have moved on |
| `toenail-fungus-removal` | 2019-09-12 | 7yr | High | Laser options now on-site (`laser-therapy-…`) but not cross-linked |
| `foot-pain-101-identifying-the-root-causes-and-finding-relief` | 2020-02-18 | 6.5yr | Medium | Broad top-of-funnel entry point |
| `general-foot-care-tips-to-save-on-pedicures` | 2018-11-05 | 7.8yr | Low | Oldest post, but thin commercial value |

✅ **Fixed 2026-08-19.** The year was dropped from both the title and the slug, and
`/post/what-to-know-about-bunion-surgery-in-2025` now 301s to the new URL. Its real
`datePublished` (2025-11-06) was left alone — only `dateModified` moved to today,
because that is when it was actually edited.

---

## Cannibalization — RESOLVED 2026-08-19

These overlapping sets have been consolidated: 10 posts retired into 7 survivors,
every old URL 301'd, unique content merged first. The library went 124 → 114.
Full mapping in `AUTONOMOUS-PUBLISHING-RUNBOOK.md`.

- ~~Chronic ankle instability ×8~~ → 3 retired, 5 kept (distinct angles: definition,
  why-it-returns, treatment/exercises, instability→foot-pain, prevention)
- ~~Toenail fungus ×4~~ → 2 retired, 2 kept (treatment options, combination therapy)
- ~~Ingrown toenails ×4~~ → 2 retired, 2 kept (long-term prevention + when-to-seek);
  the nail-removal procedure section was merged into the survivor
- ~~Hammertoe ×3~~ → 2 retired, 1 kept
- ~~Dual Syndesmosis TightRope ×2~~ → 1 retired, 1 kept
- Kids' flat feet / foot problems ×2 — left alone; genuinely different angles

---

## Seasonal hooks (Northern Utah)

| Window | Hook | Scheduled |
|---|---|---|
| Late Aug – Sept | Fall youth & high-school sports start | Sever's disease, turf toe, youth injury prevention |
| Sept – Oct | Peak Wasatch hiking / peak-bagging season | Hiking boots, high-altitude foot swelling |
| Oct – Nov | Marathon & trail-race season winds down | Navicular stress fractures, runner's plantar fasciitis |
| Nov | Ski/snowboard season opens (Snowbasin, Powder Mtn, Nordic Valley) | Ski & snowboard boot fit, winter boots |
| Nov – Dec | Diabetes Awareness Month (November) | Diabetic cluster concentrated in November |

---

## Content mix

29 Tue/Thu slots between 2026-08-20 and 2026-11-26.

| Type | Count | Share |
|---|---:|---:|
| New articles | 24 | 83% |
| Freshness refreshes of existing posts | 5 | 17% |
| Repurposed | 0 | — |

Deliberately above the standard 60/30 new/refresh ratio: the blog is 6 months
dormant with 123 posts already indexed, so the shortfall is *new* coverage in the
thin clusters, not re-editing a back catalogue that was already bulk-restamped in
July. Refreshes are placed on 5 Thursdays, on the Critical/High decay items only.

Content-type spread across the 24 new posts: 10 how-to/guide, 6 comparison,
4 FAQ/knowledge, 2 tutorial, 2 seasonal/local.

---

## Month 1 — August 20 – 31, 2026
### Focus: open the Achilles/Sports gap while fall sports start

| Date | Day | Type | Title | Slug | Cluster | Template | Keyword |
|---|---|---|---|---|---|---|---|
| Aug 20 | Thu | New | Insertional vs. Midportion Achilles Tendonitis: Why the Location Changes Treatment | `insertional-vs-midportion-achilles-tendonitis` | Achilles Tendon & Sports Injuries | comparison | insertional achilles tendonitis |
| Aug 25 | Tue | New | Sever's Disease: Heel Pain in Growing Young Athletes | `sever-s-disease-heel-pain-in-young-athletes` | Achilles Tendon & Sports Injuries | how-to-guide | sever's disease heel pain kids |
| Aug 27 | Thu | New | What Causes Bunions: Genetics, Shoes, or Both? | `what-causes-bunions-genetics-shoes-or-both` | Bunions & Toe Deformities | faq-knowledge | what causes bunions |

## Month 2 — September 2026
### Focus: Bunions cluster build-out + hiking season

| Date | Day | Type | Title | Slug | Cluster | Template | Keyword |
|---|---|---|---|---|---|---|---|
| Sep 1 | Tue | New | Lapiplasty vs. Traditional Bunion Surgery: How the Two Approaches Differ | `lapiplasty-vs-traditional-bunion-surgery` | Bunions & Toe Deformities | comparison | lapiplasty vs traditional bunion surgery |
| Sep 3 | Thu | **Refresh** | `what-you-need-to-know-about-plantar-fasciitis` | — | Heel & Arch Pain | — | plantar fasciitis treatment |
| Sep 8 | Tue | New | Hiking Boots for Utah Trails: Preventing Foot and Ankle Injuries | `hiking-boots-for-utah-trails-preventing-foot-injuries` | Orthotics & Footwear | how-to-guide | hiking boots foot pain |
| Sep 10 | Thu | New | Turf Toe: What Athletes Need to Know About a Sprained Big Toe | `turf-toe-what-athletes-need-to-know` | Achilles Tendon & Sports Injuries | how-to-guide | turf toe treatment |
| Sep 15 | Tue | New | Non-Surgical Bunion Relief: What Actually Helps | `non-surgical-bunion-relief-what-actually-helps` | Bunions & Toe Deformities | how-to-guide | non surgical bunion treatment |
| Sep 17 | Thu | **Refresh** | `sprained-ankle-here-s-when-you-need-a-doctor` | — | Ankle Injuries & Instability | — | sprained ankle see a doctor |
| Sep 22 | Tue | New | Morton's Neuroma: Why It Feels Like a Pebble in Your Shoe | `morton-s-neuroma-symptoms-and-treatment` | Arthritis, Nerve & Circulation | how-to-guide | morton's neuroma treatment |
| Sep 24 | Thu | New | Navicular Stress Fractures: The Injury Runners Miss | `navicular-stress-fractures-in-athletes` | Fractures & Foot Trauma | how-to-guide | navicular stress fracture |
| Sep 29 | Tue | New | Hallux Rigidus vs. Bunion: Telling Big-Toe Problems Apart | `hallux-rigidus-vs-bunion-telling-big-toe-problems-apart` | Bunions & Toe Deformities | comparison | hallux rigidus vs bunion |

## Month 3 — October 2026
### Focus: Fractures + Orthotics, and Achilles cluster to 12

| Date | Day | Type | Title | Slug | Cluster | Template | Keyword |
|---|---|---|---|---|---|---|---|
| Oct 1 | Thu | New | How Long Does a Foot Fracture Take to Heal? | `how-long-does-a-foot-fracture-take-to-heal` | Fractures & Foot Trauma | faq-knowledge | how long foot fracture heal |
| Oct 6 | Tue | New | Achilles Tendon Rupture: Surgery vs. Non-Surgical Treatment | `achilles-tendon-rupture-surgery-vs-nonsurgical-treatment` | Achilles Tendon & Sports Injuries | comparison | achilles rupture surgery or not |
| Oct 8 | Thu | **Refresh** | `heel-spur-treatment-options` | — | Heel & Arch Pain | — | heel spur treatment |
| Oct 13 | Tue | New | Walking Boot vs. Cast: Which One, and Why | `walking-boot-vs-cast-which-one-and-why` | Fractures & Foot Trauma | comparison | walking boot vs cast |
| Oct 15 | Thu | New | How Custom Orthotics Are Made: From Scan to Fit | `how-custom-orthotics-are-made-scan-to-fit` | Orthotics & Footwear | tutorial | how are custom orthotics made |
| Oct 20 | Tue | New | Eccentric Heel Drops: The Exercise That Works for Achilles Tendonitis | `eccentric-heel-drops-for-achilles-tendonitis` | Achilles Tendon & Sports Injuries | tutorial | eccentric heel drops achilles |
| Oct 22 | Thu | New | Recovering From Lapiplasty, Week by Week | `recovering-from-lapiplasty-week-by-week` | Bunions & Toe Deformities | how-to-guide | lapiplasty recovery timeline |
| Oct 27 | Tue | New | Big-Toe Arthritis: Treatment Options Beyond Fusion | `big-toe-arthritis-treatment-options-beyond-fusion` | Arthritis, Nerve & Circulation | how-to-guide | big toe arthritis treatment |
| Oct 29 | Thu | **Refresh** | `toenail-fungus-removal` | — | Nails & Skin Conditions | — | toenail fungus removal |

## Month 4 — November 2026
### Focus: Diabetes Awareness Month + ski season

| Date | Day | Type | Title | Slug | Cluster | Template | Keyword |
|---|---|---|---|---|---|---|---|
| Nov 3 | Tue | New | Diabetic Foot Ulcers: Stages, Treatment, and Why Speed Matters | `diabetic-foot-ulcers-stages-and-treatment` | Diabetic Foot Care | how-to-guide | diabetic foot ulcer treatment |
| Nov 5 | Thu | New | Why Diabetic Neuropathy Hides Foot Injuries | `why-diabetic-neuropathy-hides-foot-injuries` | Diabetic Foot Care | faq-knowledge | diabetic neuropathy foot injury |
| Nov 10 | Tue | New | Charcot Foot: What People With Diabetes Should Know | `charcot-foot-what-diabetics-should-know` | Diabetic Foot Care | how-to-guide | charcot foot diabetes |
| Nov 12 | Thu | New | Choosing Diabetic Shoes and Inserts | `choosing-diabetic-shoes-and-inserts` | Diabetic Foot Care | how-to-guide | diabetic shoes inserts |
| Nov 17 | Tue | New | Ski and Snowboard Boot Fit: Why Your Feet Hurt on the Mountain | `ski-and-snowboard-boot-fit-and-foot-pain` | Orthotics & Footwear | how-to-guide | ski boot foot pain |
| Nov 19 | Thu | **Refresh** | `foot-pain-101-identifying-the-root-causes-and-finding-relief` | — | General Foot Health & Wellness | — | foot pain causes |
| Nov 24 | Tue | New | Limb Salvage: When Amputation Isn't the Only Option | `limb-salvage-when-amputation-isn-t-the-only-option` | Diabetic Foot Care | how-to-guide | limb salvage foot |
| Nov 26 | Thu | New | Winter Boots and Foot Pain in Utah | `winter-boots-and-foot-pain-in-utah` | Orthotics & Footwear | how-to-guide | winter boots foot pain |

### Overflow queue (runs on into December if the routine outpaces the calendar)

| Title | Slug | Cluster | Template |
|---|---|---|---|
| Tailor's Bunion (Bunionette): Why the Outside of Your Foot Hurts | `tailor-s-bunion-bunionette-explained` | Bunions & Toe Deformities | how-to-guide |
| Returning to Sport After a Foot or Ankle Injury | `returning-to-sport-after-a-foot-or-ankle-injury` | Achilles Tendon & Sports Injuries | how-to-guide |
| High-Altitude Hiking and Foot Swelling in Utah | `high-altitude-hiking-and-foot-swelling-in-utah` | Orthotics & Footwear | faq-knowledge |
| Plantar Fasciitis in Runners: Training on Utah's Hard-Packed Trails | `plantar-fasciitis-in-runners-utah-trails` | Heel & Arch Pain | how-to-guide |
| Youth Sports in Davis County: Preventing Foot and Ankle Injuries | `youth-sports-preventing-foot-and-ankle-injuries` | Achilles Tendon & Sports Injuries | how-to-guide |
| Stress Fracture vs. Shin Splints vs. Tendonitis | `stress-fracture-vs-shin-splints-vs-tendonitis` | Fractures & Foot Trauma | comparison |

---

## Internal-linking plan

Every new post links to, at minimum:
1. **Its matching service page** (extensionless, root-relative from `post/` → `../`):
   `../heel-pain`, `../plantar-fasciitis`, `../bunion-removal`, `../lapiplasty`,
   `../tailor-s-bunion`, `../hallux-rigidus`, `../achilles-tendonitis`,
   `../ankle-fractures`, `../calcaneal-fractures`, `../fifth-metatarsal-fractures`,
   `../toe-metatarsal-fractures`, `../lisfranc-injuries`, `../diabetic-foot-care-1`,
   `../charcot-arthropathy`, `../limb-salvage`, `../custom-orthotics`,
   `../lateral-ankle-instability`, `../talar-dome-lesions`, `../tarsal-tunnel-syndrome`,
   `../posterior-tibial-tendon`, `../arthritis`, `../rheumatoid-arthritis`, `../gout`,
   `../flat-feet`, `../ingrown-nails`, `../nail-proceedure`,
   `../dual-syndesmosis-tightrope`, `../conscious-sedation`, `../recovery`
2. **2–3 sibling posts in the same cluster**
3. **`../book-appointment`** in the closing CTA band
4. **A city or clinic page** where the topic is genuinely local
   (`../farmington-utah`, `../ogden-utah-foot-doctor`, `../locations`)

## Distribution

Not automated in this quarter. Site has no `rss.xml` — see the runbook's
*Known gaps*. LinkedIn posting is handled by separate existing routines.

---

## Quarterly goals

- [ ] Publish 24 new posts; blog reaches **147** articles
- [ ] Achilles/Sports 6 → 12, Bunions 6 → 12, Diabetic 6 → 11
- [ ] Refresh the 5 highest-decay high-intent posts
- [ ] No new posts in the two saturated clusters
- [x] ~~Retitle `…-bunion-surgery-in-2025`~~ — done 2026-08-19
- [x] ~~Consolidate the duplicate sets~~ — done 2026-08-19, 124 → 114 posts
- [ ] Decide on `rss.xml` — still the one open item
