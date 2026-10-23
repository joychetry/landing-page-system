# Step 8: Page copy

Write every headline, line of body copy and CTA for the page in the customer's own words, before any design exists.

## Scope

Per page. Runs once for every page. Copy first, design second: steps 9 to 11 wrap the layout around this copy, so nothing visual is decided here except what the hero visual must show.

## Inputs

- `pages/<page>/07-structure.md`: the sections, their one job, the facet placement and the primary keyword.
- `research/02-customers.md`: the language bank, pains, objections.
- `research/04-proof.md`: the only allowed source of testimonials, numbers and logos.
- `research/05-brand-story.md`: one-liner, problem, plan, stakes, voice.
- `research/01-goal-offer.md`: the dream outcome, offer facets, guarantees that exist.
- `references/checklists/hero.md` and `references/checklists/de-ai-copy.md`.

## Do this

1. Write the hero first and spend the most time on it. As an industry rule of thumb, around 60 percent of visitors never scroll past it, so it carries most of the page. Write 10 headline options, shortlist the best 3, and ask the human to pick one (a question or button prompt if your agent has one, such as `AskUserQuestion` in Claude Code, otherwise plain text). Give each option a one-line reason, put your recommendation first, and let them write their own. Use the one they choose; their wording wins over yours.
2. Headline: the dream outcome, not who you are or what you do. Build it from three parts: the end result (quantified if you can prove it), a time period (only if true and typical), and the emotional payoff (how life feels after). Example shape: "Lose the first 10 pounds in 6 weeks and fit your clothes again". Readable in 5 seconds, 14 words or fewer, containing the primary keyword if it fits naturally.
3. Subheadline: the how. Open with a pain hook or pattern interrupt taken from the language bank ("Tired of chasing invoices?"), then name the 3 to 4 biggest value props that deliver the headline. One or two sentences.
4. Finish the hero stack. All of it must fit above the fold on a phone, so cut words until it does.
   - 2 proof items, copied exactly from `research/04-proof.md`: a rating with review count, a short testimonial, a client logo row, or a hard number. Two different types beat two of the same.
   - 1 CTA button: a verb plus what they get ("Get my free quote", "Start my 14-day trial"), never "Submit", "Learn more" or "Click here". One action only.
   - FUD reducers, only if true: no card needed, cancel anytime, money-back terms, warranty, response time.
   - Visual brief, one line: it shows the thing they get or the outcome they want, and proves the headline.
5. Section 2. Social proof version: a benefit-led headline that gives a reason to read ("Join 300 clinics that cut no-shows in half", only with real numbers), then the wall of love: many real reviews shown at once. Pain point version: problem (name the pain in their words and ask if it sounds familiar), agitate (what it costs them in time, money, stress, missed moments), solution (how this offer fixes it, backed by one proof point). For a visual offer, write before and after captions instead.
6. Proof sections: every headline leads with the benefit the customers got. Never "Our testimonials", "Our reviews", "See what our customers say" or "Real people, real results". Copy testimonials exactly, with name, role or location as permitted; trim only with an ellipsis and never change meaning.
7. Value props (4 to 8, one block per row of `## Feature definitions` in `07-structure.md`): turn each definition into a full feature section.
   - Headline: joins a benefit to the feature that delivers it ("See every shipping fee in one dashboard and stop overpaying"), readable on its own.
   - Lead: 2 to 3 sentences saying what the feature does and what changes for the customer.
   - Details: 3 to 5 bullets of concrete specifics from the definition (how it works, numbers, limits, timing, terms). A reader should be able to explain the feature to someone else after reading them. "Fast", "easy" and "powerful" are not details.
   - Proof: the row from `research/04-proof.md`, if the definition has one.
   - Visual: the brief from the definition.
   Test: read only the headlines, top to bottom. If a skimmer would not know what they get and why it matters, rewrite. Then read only one section's details: if they could describe any competitor's product, they are too vague.
8. How it works: a section headline that sells ("Get a clean lawn in 4 simple steps"), then 3 to 5 steps whose words are benefits or easy actions ("Get your free estimate", "Sit back and enjoy the result"), never bare "Step 1". Follow each step title with one sentence on what happens and what the customer does.
9. FAQ: 5 to 8 real questions from the objections in `research/02-customers.md` and the questions assigned in `research/06-seo.md`, in the customer's wording. Answers are short and honest. Surface guarantees, warranties and terms only if they exist; never invent one to fill the slot.
10. Closer: a mini hero. Recap headline (the dream outcome again, said fresh), subheadline, the same CTA action as the hero, one proof item, and the form (3 to 4 bullets of what happens next, then the fields) or pricing.
11. SEO copy: title tag of 50 to 60 characters with the primary keyword near the start, meta description of 130 to 155 characters that sells the click, and the H1 (usually the hero headline) containing the primary keyword or its core phrase.
12. Fill the Claim trace table: every number, testimonial, logo, award, guarantee and comparison on the page gets a row pointing to its source row in `research/04-proof.md` or a research file. Anything you cannot trace, delete or soften to a claim you can support.
13. De-AI pass. Read every line aloud. Strip AI-isms and filler (unlock, unleash, seamless, elevate, game-changer, revolutionize, cutting-edge, supercharge, empower, leverage, delve, robust, transformative, "in today's fast-paced world"), vague superlatives with no proof (best, leading, world-class), stacked adjectives, rhetorical triplets, and em dashes (use commas, colons, periods). Swap generic phrases for language bank phrases. Check "you" outnumbers "we". Follow `references/checklists/de-ai-copy.md` and tick the De-AI pass boxes.
14. Run `lp check pages/<page>/08-copy.md` and fix every error and warning (banned phrases, placeholders, headline length, em dash density, exclamation marks).

## Output

`pages/<page>/08-copy.md`, from template: 08-copy.md. Run `lp start 8 --page <page>` to copy the template into place (it never overwrites). Repeat the Value prop and FAQ blocks as needed; keep every `## ` heading. When finished run `lp done 8 --page <page>`, fix whatever it reports, then `lp next`.

## Done when

- [ ] Every `## ` heading from the template is present and no `{{...}}`, TODO, TBD or lorem ipsum remains.
- [ ] The hero has a dream-outcome headline (never who you are), a how subheadline, 2 proof items, 1 CTA, true FUD reducers and a visual brief.
- [ ] Reading only the headlines, top to bottom, a stranger can say what they get, how, and what to do next.
- [ ] Every value prop headline pairs a benefit with a feature, and every proof headline leads with a benefit.
- [ ] There is one value prop block per feature definition (at least 4), each with a lead, 3 to 5 concrete details, proof and visual, and at least 5 FAQ questions (`lp done 8` checks the counts).
- [ ] Phrases from the language bank in `research/02-customers.md` appear in the hero and at least two other sections.
- [ ] Every claim on the page has a row in the Claim trace table; nothing is invented.
- [ ] Title tag (50 to 60 characters), meta description (130 to 155 characters) and H1 are written with the primary keyword.
- [ ] `lp check pages/<page>/08-copy.md` reports zero errors and the De-AI pass boxes are ticked.

## Common mistakes

- A headline that names the company or category ("Acme: AI-powered invoicing platform") instead of the outcome.
- A subheadline that repeats the headline instead of explaining how.
- Features with no "so what": the visitor will not do the translation for you.
- Polishing testimonials into marketing copy. Quote them exactly or not at all.
- Generic CTAs ("Submit", "Learn more", "Get started") that hide what the click gives them.
- Writing the copy inside a design tool or page builder so the layout decides the word count.

## Redesign mode notes

- Start from the saved copy in `audit/pages/<slug>.md`. Keep lines that already convert or rank (headings containing ranking terms, proven offers); rewrite the rest against this guide.
- Keep any wording legally required on the live page (pricing terms, disclaimers, regulated claims) and note it in the Claim trace table.
