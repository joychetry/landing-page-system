# Method overview

Sixteen steps (plus step 0 for redesigns) that take a product from "we need a page" to a live, measured landing page. Same process every time: copy first, design second, and every block on the page does one job before handing the visitor to the next.

## The four phases

1. **Research (steps 1 to 6).** Product-level. Done once per product and reused by every page.
2. **Write (steps 7 to 8).** Per page. Structure first, then the copy, in the customer's own words.
3. **Design (steps 9 to 12).** Per page, except brand guidelines (step 10), which is product-level.
4. **Launch (steps 13 to 16).** Per page. Polish, check, ship, then measure and improve on a loop.

## Phases and gates

```
 [0 Audit existing site]   (redesign mode only, once)
            |
            v
 +-------------------------------------------------------------+
 | PHASE 1  RESEARCH   product-level, once, reused by all pages |
 | 1 Goal and offer -> 2 Customers -> 3 Competitors             |
 | 4 Proof and assets -> 5 Brand story -> 6 SEO research        |
 +-------------------------------------------------------------+
            |
            v   (each page starts here)
 +-------------------------------------------------------------+
 | PHASE 2  WRITE   per page                                    |
 | 7 Page structure -> 8 Page copy                              |
 +-------------------------------------------------------------+
            |
            v
 +-------------------------------------------------------------+
 | PHASE 3  DESIGN                                              |
 | 9 Wireframe                                                  |
 |      ==== GATE 1: human approves the wireframe ====          |
 | 10 Brand guidelines (product-level, first page only)         |
 | 11 Final design                                              |
 |      ==== GATE 2: human approves the final design ====       |
 | 12 Page visuals                                              |
 +-------------------------------------------------------------+
            |
            v
 +-------------------------------------------------------------+
 | PHASE 4  LAUNCH   per page                                   |
 | 13 Polish -> 14 Last checks                                  |
 |      ==== GATE 3: human approves shipping ====               |
 | 15 Ship -> 16 Measure and iterate --+                        |
 |              ^                      |                        |
 |              +---- repeat ----------+                        |
 +-------------------------------------------------------------+
```

The agent never approves a gate. At each gate it stops, shows the human the work, and asks them to run `lp approve gateN --page <page> --by "<their name>"`. `lp next` will not move past an unapproved gate.

## Step table

| Step | Title | Scope | Output file | Guide file |
|---|---|---|---|---|
| 0 | Audit the existing site | Product, redesign only, once | audit/site-audit.md, audit/url-map.csv, audit/pages/*.md | steps/00-audit-existing.md |
| 1 | Goal and offer | Product, once | research/01-goal-offer.md | steps/01-goal-offer.md |
| 2 | Customer research | Product, once | research/02-customers.md | steps/02-customer-research.md |
| 3 | Competitor research | Product, once | research/03-competitors.md | steps/03-competitor-research.md |
| 4 | Proof and assets | Product, once | research/04-proof.md | steps/04-proof-assets.md |
| 5 | Brand story | Product, once | research/05-brand-story.md | steps/05-brand-story.md |
| 6 | SEO research | Product, once (maps keywords to all planned pages) | research/06-seo.md | steps/06-seo-research.md |
| 7 | Page structure | Per page | pages/<page>/07-structure.md | steps/07-page-structure.md |
| 8 | Page copy | Per page | pages/<page>/08-copy.md | steps/08-page-copy.md |
| 9 | Wireframe | Per page, Gate 1 after | pages/<page>/09-wireframe.html | steps/09-wireframe.md |
| 10 | Brand guidelines | Product, once with the first page, inherited after | brand/brand.md, brand/tokens.css | steps/10-brand-guidelines.md |
| 11 | Final design | Per page, Gate 2 after | pages/<page>/11-design/, pages/<page>/build/index.html | steps/11-final-design.md |
| 12 | Page visuals | Per page | pages/<page>/12-visuals.md | steps/12-page-visuals.md |
| 13 | Polish | Per page | pages/<page>/13-polish.md, updated build/ | steps/13-polish.md |
| 14 | Last checks | Per page, Gate 3 after | pages/<page>/14-checks.md | steps/14-last-checks.md |
| 15 | Ship | Per page | pages/<page>/15-ship.md | steps/15-ship.md |
| 16 | Measure and iterate | Per page, repeating loop | pages/<page>/16-measure.md | steps/16-measure-iterate.md |

Guide paths are relative to the guide folder: references/ in the skill, .lp/guide/ inside a workspace. Checklists used along the way live in checklists/: hero.md, seo-onpage.md, performance.md, accessibility.md, de-ai-copy.md.

## Product-level vs per-page

- **Product-level, done once:** research steps 1 to 6 and brand guidelines (step 10). They describe the product, the buyer, the market, the proof, the story, the keyword plan and the look. Every page reads them.
- **Per page:** steps 7 to 9 and 11 to 16, plus the three gates. Each page has its own primary keyword, structure, copy, design, checks and measurements.
- **Later pages inherit.** A second page (`lp page add pricing`) starts at step 7. Research is reused as is, and step 10 shows as "inherited" because brand/brand.md and brand/tokens.css already exist.
- **Research comes first.** If any of steps 1 to 6 is unfinished, `lp next` for any page points at the missing research step before page work.
- **One keyword per page.** Step 6 maps keywords to pages. Two pages with the same primary keyword is an error, because they would compete with each other in search.
- **Research goes stale.** Research files carry a `verified:` date. `lp stale` lists files older than 90 days so they can be re-checked before the next page or redesign.

## The agent loop

```
 lp next  ->  read the guide it names  ->  do the work  ->  lp done N  ->  repeat
```

1. Run `lp next` (add `--page <page>` to focus on one page, `--json` for machine output). It returns the step, the guide to read, the input files, the output file, the template and the done criteria.
2. Read the guide fully, then read every input file it lists.
3. Run `lp start N` to copy the template into place. It never overwrites an existing file.
4. Do the work. Use real data with sources. Never invent testimonials, numbers, logos, quotes or awards; write missing proof as a gap.
5. Run `lp done N` (with `--page <page>` for page steps). Fix whatever it reports and run it again.
6. If `lp next` reports a gate, stop and hand over to the human. Otherwise repeat.

Without the CLI the loop still works by hand: read the guide, copy the template from templates/, fill it in, tick the "Done when" list yourself, and update lp.json manually.

## The three modes

- **New product** (`lp init <product>`). Starts at step 1. Research, then the first page (`home`) from step 7 to 16.
- **Add a page** (`lp page add <slug> --keyword "..."`). For a product that already has research and a brand. The page starts at step 7, reuses research 1 to 6, inherits brand step 10, and goes through all three gates on its own.
- **Redesign an existing site** (`lp init <product> --mode redesign --url https://...`). Starts at step 0: crawl the live site, save the current copy per page, pull search data if available, build the URL map, and score each page. The audit pre-fills research 1 to 6 with evidence marked `source: live-site`. Each page chosen for rebuilding then starts at step 7. Step 15 requires a 301 redirect map for every changed URL.
