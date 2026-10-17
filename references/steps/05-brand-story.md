# Step 5: Brand story

Write the story the page will tell, with the customer as the hero and the brand as the guide who
helps them win, using a StoryBrand-style structure built from real research.

## Scope

Product-level, runs once. Every page reuses this file. It sets the narrative order and the voice; it
is not page copy yet. Step 8 turns it into headlines.

## Inputs

- `research/01-goal-offer.md` (conversion action, dream outcome, offer facets).
- `research/02-customers.md` (segments, pains, desired outcomes, objections, language bank).
- `research/04-proof.md` (the only allowed source for authority claims).

## Do this

1. Run `lp start 5` to copy the template to `research/05-brand-story.md`. Set `verified:` to today's
   date.
2. Character. Name the primary segment from `research/02-customers.md` and the one thing they want,
   tied to the dream outcome in `research/01-goal-offer.md`. One want, not three. A story where the
   hero wants everything has no tension. Use their words from the language bank.
3. Villain. Name the cause of the problem, not a person or a competitor: the thing that keeps
   getting in their way (manual follow-ups, hidden fees, guesswork, a broken process). A clear
   villain makes the pain section easy to write later.
4. Problem on three levels. External: the practical, visible problem (the top-ranked pain in
   `research/02-customers.md`). Internal: how it makes them feel, taken from the emotional quotes
   (frustrated, embarrassed, anxious, stuck). Philosophical: why it is simply wrong that this
   happens ("small teams should not need a full-time person just to send invoices"). People buy to
   solve the internal problem; name it honestly, without melodrama.
5. Guide. The brand is the guide, never the hero. Write empathy first: one or two sentences that
   show you understand, mirroring a real pain in their words. Then authority: why they can trust
   you, using only items from `research/04-proof.md` (review score and count, verified numbers,
   years in business, certifications, recognizable clients with permission). If authority proof is
   thin, say so here and point to the Gaps in the proof file; do not fill it with claims.
6. Plan. Three steps, four at most, that show how easy it is to get from where they are to the
   outcome (for example: book a call, get your plan, see results). Name each step by what the
   customer gets, not what you do. This becomes the How it works section, whose step headlines are
   benefits.
7. Call to action. The direct CTA is the one conversion action from `research/01-goal-offer.md`,
   word for word. A transitional CTA (a guide, a calculator, a sample) is optional, only if it
   really exists, and never competes visually with the direct one.
8. Failure. What it costs them to do nothing, drawn from the costs recorded against pains in
   `research/02-customers.md`: time, money, missed chances, stress. Keep it true and specific.
   Inflated fear reads as manipulation and lowers trust.
9. Success. What life looks like after, in concrete, visible terms taken from the desired outcomes.
   This feeds the hero headline and the closer.
10. One-liner. Problem, solution, result in two or three sentences a customer could repeat to a
    friend. Test it: read it aloud; it should make sense to a stranger with no context, use the
    customer's words, and contain no jargon from the avoid list. Write two or three versions and
    keep the clearest.
11. Voice. Describe how the brand sounds and never sounds, with words to use and words to avoid.
    Pull "words to use" from the language bank and "words to avoid" from its jargon list, plus
    filler such as unlock, seamless, elevate and game-changer.
12. Check the story against the page skeleton it will feed: success and want map to the hero, the
    problem and failure map to the pain section, the guide maps to proof, the plan maps to how it
    works, and the CTA maps to every button. If one part has nothing behind it, fix the research,
    not the story.
13. When finished, run `lp done 5`, fix whatever it reports, then run `lp next`.

## Output

`research/05-brand-story.md` (template: 05-brand-story.md). Run `lp start 5` to copy the template
into place (it never overwrites).

## Done when

- [ ] Frontmatter has `verified: YYYY-MM-DD` (not in the future), every template `##` heading is present, and no `{{...}}`, `TODO` or `TBD` remains.
- [ ] The customer is the hero throughout; the brand appears only as the guide.
- [ ] The problem is written on all three levels (external, internal, philosophical), grounded in quotes from `research/02-customers.md`.
- [ ] Every authority claim traces to an item in `research/04-proof.md`.
- [ ] The plan has 3 or 4 steps, each named by what the customer gets.
- [ ] The direct CTA matches the conversion action in `research/01-goal-offer.md`.
- [ ] The one-liner makes sense to a stranger when read aloud and uses the customer's words.

## Common mistakes

- Making the brand the hero ("our journey", "our passion", founder story first). Visitors care about
  their own story; the brand earns attention by helping.
- Skipping the internal problem. The external problem explains the purchase; the internal one drives
  it.
- Authority with no proof ("industry-leading experts"). If it is not in the proof file, it does not
  go in the story.
- A plan with seven steps or steps that describe your process ("we analyze, we strategize"). Keep it
  short and about the customer.
- A one-liner that is a tagline ("Innovation for tomorrow") instead of problem, solution, result.

## Redesign mode notes

Read the About page and homepage saved in `audit/pages/` and note who the current hero is. Most
older sites make the company the hero; record that as a weak section in `audit/site-audit.md`. Keep
any real founder story or origin detail as authority material if it is true and the owner confirms
it, marked `source: live-site`. If customers already repeat a phrase from the old site in reviews,
keep it in the voice: it has proven itself.
