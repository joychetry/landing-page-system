# Step 4: Proof and assets

Build a complete, sourced inventory of every testimonial, number, logo, screenshot and guarantee the
page may use, and list honestly what is missing.

## Scope

Product-level, runs once and is updated whenever new proof arrives. Every page reuses this file. The
rule is absolute: nothing goes on any page that is not in this file, and nothing goes in this file
that is not real.

## Inputs

- `research/01-goal-offer.md` (offer facets of type proof, risk reversal terms).
- `research/02-customers.md` (objections, each needing proof).
- `research/03-competitors.md` (the proof bar competitors set, and gaps marked "to confirm in step
  4").
- `assets/` (logos, screenshots, photos and documents the owner supplied).

## Do this

1. Run `lp start 4` to copy the template to `research/04-proof.md`. Set `verified:` to today's date.
2. Send the owner one clear request: every review platform profile link; customer emails, messages
   or survey answers that praise results; case studies; client logos they have permission to show;
   press mentions; certifications, licenses and awards with issuer and year; the numbers they track
   (customers served, years in business, results achieved) and where those numbers come from;
   product screenshots and real photos of the team, work or location. Ask them to drop files into
   `assets/`.
3. Collect public reviews yourself. Open each review profile (Google Business Profile, Trustpilot,
   G2, Capterra, app stores, Facebook, industry directories) in a browser. Record the overall score,
   the review count and the date you checked, then copy the strongest reviews word for word with
   reviewer name as shown, date and the link.
4. Fill `## Proof inventory` one row per item: type, exact content, attribution, source (URL or
   "provided by owner, YYYY-MM-DD"), permission status, best use on the page. Copy testimonials
   exactly. Trimming with an ellipsis is allowed only if the meaning does not change; never
   strengthen wording, merge two reviews, or fix a claim to sound better.
5. Settle permission for each item. Testimonials from private emails, messages, calls or surveys
   need written permission from the customer before they are published: mark "yes", "no" or "asked
   YYYY-MM-DD". Client logos need the client's permission or a contract clause allowing it. Public
   third-party reviews can usually be quoted with attribution and a link, but check the platform's
   terms and confirm with the owner.
6. Verify every number in `## Numbers we can stand behind`. Write what it measures, how it was
   calculated (the denominator and the period), the "as of" date and the source. Round down, never
   up. "500+ customers" needs a count of at least 500 from a system the owner can show. If the owner
   cannot say where a number came from, it moves to Gaps.
7. Inventory visuals in `## Screenshots and product visuals`: file name in `assets/`, what it shows,
   whether it is a real capture or a mock-up, and whether it is usable as is (resolution, cropping,
   outdated UI, personal data visible). Stock photos presented as customers and AI-generated
   "customer" faces are never proof.
8. Record guarantees and risk reversal only with the exact terms the owner has confirmed in writing,
   with the date. If there are none, write "none". The page will not invent one.
9. Map proof to the page. Check that you have at least 2 strong proof items for the hero (a review
   score with count, a sharp testimonial, a hard number, a recognizable logo or press mention).
   Check that every objection in `research/02-customers.md` has a proof item that answers it. Check
   every gap in `research/03-competitors.md` marked "to confirm in step 4": confirm it here or move
   it to Gaps and remove it from the competitor file.
10. Plan the wall of love. Proof works by volume when shown as a visible wall of reviews, stacked
    one by one on mobile, never in a carousel (an industry rule of thumb is that only 1 to 2 percent
    of visitors click past the first slide). If there are only a handful of usable reviews, plan a
    score with count plus two or three strong quotes instead, and log the shortfall as a gap.
11. Write `## Gaps` as owner tasks, not writing problems: the missing proof, why the page needs it,
    how to get it (for example: email the 20 most recent happy customers asking for a review on the
    main platform; request a 3-question testimonial with permission to publish; pull the real number
    from the CRM; book a 20-minute case study interview), who does it, and by when. Then ask the
    owner to decide each gap that affects the hero or a main objection (a question or button prompt if your agent has one, such as `AskUserQuestion` in Claude Code, otherwise plain text):
    "I will get it by <date>" or "Ship without it". Write their answer in the Who and By when
    columns ("ship without" if they decline); the page is then planned around it in step 7.
12. When finished, run `lp done 4`, fix whatever it reports, then run `lp next`.

## Output

`research/04-proof.md` (template: 04-proof.md). Run `lp start 4` to copy the template into place (it
never overwrites).

## Done when

- [ ] Frontmatter has `verified: YYYY-MM-DD` (not in the future), every template `##` heading is present, and no `{{...}}`, `TODO` or `TBD` remains.
- [ ] A `## Gaps` section exists and lists every piece of proof the page needs but does not have.
- [ ] Every proof item has an exact source (URL or "provided by owner, YYYY-MM-DD") and a permission status.
- [ ] Every number states what it measures, how it was calculated and an "as of" date.
- [ ] The hero has 2 proof candidates, or the shortfall is a gap.
- [ ] Every objection from `research/02-customers.md` maps to a proof item or a gap.
- [ ] Nothing in the file is invented, estimated, paraphrased into something stronger, or borrowed from another business.

## Common mistakes

- Filling holes with plausible proof: a made-up testimonial "to be replaced later", a rounded-up
  customer count, a logo of a company that once had a trial. These ship by accident. Write a gap
  instead.
- Losing the source. A quote with no link or date cannot be checked in step 14 and must be cut.
- Publishing private testimonials without written permission.
- Treating forum quotes or competitor reviews from step 2 as proof for this product. They are
  research, not testimonials.
- Planning a carousel for reviews. Proof hidden behind slides is proof most visitors never see.
- Accepting "trusted by thousands" from the owner without a number and a source.

## Redesign mode notes

Start with the proof listed in `audit/site-audit.md` and saved in `audit/pages/`. Treat it as
unverified: each testimonial, logo and number on the old site needs its original source and
permission confirmed before it moves into the inventory, marked `source: live-site` plus the
confirming source. Numbers on the old site are often years out of date; get a current figure or move
them to Gaps.
