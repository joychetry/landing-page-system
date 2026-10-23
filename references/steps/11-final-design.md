# Step 11: Final design

Explore 2 to 3 distinct design directions on the hero, let the human pick one, then build the full page around the approved copy.

## Scope

Per page. Runs once for every page, after Gate 1 is approved and the brand exists (step 10 done, or inherited). Gate 2 follows: a human must approve the built page before visuals and polish.

## Inputs

- `pages/<page>/09-wireframe.html`: the approved structure, section order and copy.
- `pages/<page>/08-copy.md`: the source of truth for every word.
- `brand/brand.md` and `brand/tokens.css`: colors, type, spacing, hero pattern, components.

## Do this

1. Re-read the hero copy and the hero pattern in `brand/brand.md`. The design serves the copy: every layout choice must make the headline, proof and CTA land harder. Ask of each direction: what message does this layout reinforce?
2. Design the hero only, in 2 or 3 genuinely distinct directions. Distinct means a different idea about what the hero should prove first, not a color swap. Typical ideas:
   - Product-led: a large real screenshot or product photo beside the headline.
   - Outcome-led: a before and after or the result itself dominates the visual.
   - Proof-led: the rating, review wall or one hard number gets the visual weight.
   - Explainer-led: a simple diagram of how it works, for complex or B2B offers.
   Pick the ideas that suit this offer: a visual offer earns a visual hero, a complex offer may need the diagram.
3. Each direction is a standalone HTML file that links `../../../brand/tokens.css`, uses the exact hero copy from `08-copy.md` (headline, subheadline, 2 proof items, 1 CTA, FUD reducers) and real assets from `brand/assets/` or `assets/`. Where the real visual does not exist yet, use a labelled grey box; never stock filler.
4. Check each direction at 360 px and 1280 px wide. The full hero stack must stay above the fold on a 360 by 640 px screen, the same rule the wireframe passed.
5. Save them as `pages/<page>/11-design/direction-a.html`, `direction-b.html` and, if made, `direction-c.html`. Add a comment at the top of each file with a one-line rationale.
6. If your agent has a design skill or tool, use it to generate and critique the directions; otherwise follow these steps and judge against `brand/brand.md`.
7. STOP and show the human the directions (file paths, plus screenshots at both widths if you can take them) with the rationale for each. Ask them to pick one, or to combine named elements. Do not pick for them.
8. Build the full page in `pages/<page>/build/index.html` using the chosen direction. Link `brand/tokens.css` (copy it into `build/` or reference it so the deployed page can load it), and use only token values for color, type and spacing. Put page CSS in `build/` and images in `build/img/`.
9. Follow `09-wireframe.html` section by section: same order, same ids, same copy, one `<h1>`, an `<h2>` per section. Copy changes go into `08-copy.md` first.
10. Apply the conversion rules in the layout: proof as a visible wall of cards (stacked on mobile, never a carousel); every value prop shows its benefit headline with a visual that explains that facet; how-it-works steps visibly numbered with benefit headlines; FAQ as simple `<details>` items; the closer as a mini hero with the form or pricing beside the recap.
11. Get the basics right now so later steps polish rather than rebuild: `<html lang>`, viewport meta, a title and meta description from the SEO copy in `08-copy.md`, `alt` on every image, real `href` values, semantic landmarks, visible focus styles, tap targets of 44 px or more.
12. Run `lp check --page <page>` and fix errors. Then run `lp done 11 --page <page>` and fix whatever it reports (it requires 2 or more files in `11-design/` and a non-trivial `build/index.html` with an `<h1>`).
13. STOP. This is Gate 2. Show the human the built page (open `build/index.html` in a browser; share screenshots at 360 and 1280 px if you can). Ask them to review it and choose Approve or Request changes (a question or button prompt if your agent has one). Only after they choose Approve, run `lp approve gate2 --page <page> --by "<their name>"` for them. Never approve without their answer. After approval, run `lp next`.

## Output

- `pages/<page>/11-design/direction-a.html`, `direction-b.html` (and optionally `direction-c.html`): hero directions.
- `pages/<page>/build/index.html` plus its CSS and images in `pages/<page>/build/`.

No template for this step; create the folders and files directly.

## Done when

- [ ] `pages/<page>/11-design/` holds at least 2 hero direction HTML files that differ in idea, not just color.
- [ ] Each direction uses the exact hero copy and real assets, and keeps the full hero above the fold at 360 px.
- [ ] The human picked the direction; the choice is noted at the top of `build/index.html` in a comment.
- [ ] `pages/<page>/build/index.html` has exactly one `<h1>`, every section from `07-structure.md` in order, and copy that matches `08-copy.md`.
- [ ] All colors, fonts and spacing come from `brand/tokens.css`; no off-brand values.
- [ ] `lp check --page <page>` reports zero errors.
- [ ] The agent has stopped, asked the human to Approve or Request changes, and ran `lp approve gate2` only after they chose Approve.

## Common mistakes

- Three directions that are the same layout in three colors. The human cannot make a real choice.
- Letting the design rewrite the copy: shortening the headline to fit a trendy layout, or dropping proof from the hero.
- Hiding reviews in a slider or tabs to make the page shorter.
- Decorative stock photos where a product screenshot or real result belongs.
- Hard-coding hex values and font sizes instead of using tokens, so the next page drifts.
- Building the full page before the human picks a direction.

## Redesign mode notes

- Include the current live hero, rebuilt with the new copy, as one reference point so the human can see the improvement is the copy and layout, not just a fresh coat of paint.
- Preserve anchor ids, form field names and tracking hooks the live page uses (check the saved page in `audit/pages/<slug>.md` and the live HTML) so integrations keep working.
