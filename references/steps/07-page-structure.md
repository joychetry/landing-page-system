# Step 7: Page structure

Decide which sections the page has, in what order, and the one job each section does before any copy or design exists.

## Scope

Per page. Runs once for every page (home first, then each page added with `lp page add`). Research files 1 to 6 are shared across pages; the structure is not.

## Inputs

- `research/01-goal-offer.md`: conversion action, traffic source and temperature, the offer facets.
- `research/02-customers.md`: pains, objections, jobs to be done.
- `research/03-competitors.md`: gaps you can own.
- `research/04-proof.md`: what proof exists and its gaps.
- `research/05-brand-story.md`: one-liner, problem, plan, stakes.
- `research/06-seo.md`: this page's row in the keyword-to-page map and the questions assigned to it.

## Do this

1. Copy this page's primary keyword from the keyword-to-page map in `research/06-seo.md` into the `Primary keyword:` line. Keep that line exactly as labelled: `lp` reads it, stores it, and reports an error if two pages share a primary keyword. If the map has no row for this page, go back and add one in step 6 first.
2. Fill the page goal: one conversion action (from `research/01-goal-offer.md`) and the traffic source and temperature for this page. One page, one goal. Secondary links (login, docs) are allowed; secondary offers are not.
3. Make the Section 2 decision. Lead with social proof when traffic is warm or high intent (people searching for the service, branded search, search ads, referrals) and the offer is easy to grasp: they already want it and need trust to act. Lead with the pain point when traffic is cold or interruption based (social ads, display), or when the offer is complex, technical or B2B: they need to see the problem before the solution makes sense. Write the reason in one line.
4. If Section 2 is the pain point, choose its form: a visual before and after when the outcome can be shown (a room, a smile, a dashboard before and after), otherwise long-form problem, agitate, solution copy.
5. Lay out the skeleton in order, one row per section in the section plan:
   - Hero: land the dream outcome and get the click.
   - Section 2: social proof or pain point (step 3).
   - Proof: build trust. Plan 2 to 4 proof moments across the page, not one testimonial block. Show proof as a wall of love (many reviews visible at once, stacked one by one on mobile), never a carousel: as an industry rule of thumb only 1 to 2 percent of visitors click past the first slide.
   - Value props: 4 to 8 sections, each one benefit plus the feature that delivers it. Pull them from the offer facets.
   - How it works: show the path from sign-up to result in 3 to 5 steps so it feels easy.
   - FAQ and FUD reducers: answer real objections, surface guarantees, warranties or cancellation terms that actually exist.
   - Closer: a mini hero with a recap headline, CTA, proof, and the form or pricing.
6. Write each section's one job as a verb phrase ("prove other dental practices got results", "show setup takes one afternoon"). If a section has two jobs, split it. If two sections share a job, cut one.
7. Fill the "Content comes from" column with the research file for each section and the "Proof used" column with specific rows from `research/04-proof.md`. Where proof is missing, plan a section that works without it and leave the gap recorded in the proof file; never plan around proof you hope to get.
8. Place the offer facets. Every facet from `research/01-goal-offer.md` lands in a section and a form: headline, proof badge, value prop, how-it-works step or FAQ answer. Facets that reduce risk (trial, guarantee) belong near CTAs.
9. Map the questions from `research/06-seo.md` assigned to this page to the section that answers them, usually the FAQ. Put secondary keywords where they fit naturally: a value prop headline, a how-it-works step, an FAQ question.
10. Use the same CTA action in the hero and the closer. Mid-page CTAs repeat it; they never introduce a second action.

## Output

`pages/<page>/07-structure.md`, from template: 07-structure.md. Run `lp start 7 --page <page>` to copy the template into place (it never overwrites). When finished run `lp done 7 --page <page>`, fix whatever it reports, then `lp next`.

## Done when

- [ ] The `Primary keyword:` line is filled with this page's keyword from the map in `research/06-seo.md`, and no other page uses it.
- [ ] Every `## ` heading from the template is present and no `{{...}}`, TODO or TBD remains.
- [ ] The Section 2 decision names social proof or pain point with a reason tied to traffic temperature or offer complexity.
- [ ] The section plan follows Hero, Section 2, Proof, Value props (4 to 8), How it works, FAQ and FUD reducers, Closer.
- [ ] Every section has exactly one job, written as a verb phrase.
- [ ] Proof appears in 2 to 4 places and every proof item names a real row in `research/04-proof.md`; no carousel is planned.
- [ ] Every offer facet is placed in the facet table, and the questions assigned to this page are mapped to sections.
- [ ] The hero and closer share one primary CTA action.

## Common mistakes

- Leading with "About us" or the company story after the hero. Section 2 is proof or pain, chosen by traffic.
- One section trying to show features, pricing and testimonials at once. One job per block.
- A single testimonial block at the bottom. Proof should recur, starting near the top.
- Value props that are features with no benefit ("API access") instead of benefit plus feature.
- Planning a guarantee or a stat in the FAQ that the business does not actually offer or have.
- Copying the home page structure to every page. Each page has its own traffic, keyword and Section 2 decision.

## Redesign mode notes

- Read the saved current copy in `audit/pages/<slug>.md` and the weak sections listed in `audit/site-audit.md`. Keep sections that already do their job; rebuild the rest.
- Keep the page's existing primary keyword when it already ranks (see the map and `audit/url-map.csv`).
- Note which current sections are being removed so content that ranks is not lost; move useful answers into the FAQ.
