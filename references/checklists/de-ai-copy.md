# Checklist: de-AI the copy

Used in step 8 (the de-AI pass on pages/<page>/08-copy.md) and step 14 (last checks on the built page). Run `lp check --page <page>` first; it catches banned phrases, long-dash density, exclamation spam, long headlines and the we/you ratio. Then read the copy as a skeptical customer would.

## Banned phrases (lp check reports these as errors)

- [ ] None of these appear anywhere on the page: unlock, unleash, seamless, elevate, game-changer, revolutionize, cutting-edge, state-of-the-art, world-class, best-in-class, next-level, supercharge, harness the power, look no further, delve, empower, synergy, transformative, unparalleled.
- [ ] None of these phrases appear: "real people, real results", "say goodbye to", "we've got you covered", "in today's fast-paced world", "see what our customers say".
- [ ] Any extra phrases the owner added to `copy_rules.extra_banned` in lp.json are gone too.

## Also watch for (not flagged by the CLI, remove on sight)

- [ ] No filler verbs: leverage, utilize, streamline, optimize, foster, facilitate, navigate (used figuratively), embark, unveil.
- [ ] No hollow adjectives: robust, innovative, comprehensive, holistic, dynamic, powerful, effortless, intuitive, tailored, bespoke, curated.
- [ ] No inflated nouns: journey, landscape, realm, tapestry, ecosystem, solution (as a stand-in for the actual product), peace of mind (unless the customers say it).
- [ ] No stock openers or closers: "Welcome to", "Are you ready to", "Imagine a world where", "Take your X to the next level", "Whether you're a X or a Y", "Join the revolution", "The future of X is here".
- [ ] No "designed to", "built to help", "aims to" where a plain verb would do ("cuts", "sends", "fixes").
- [ ] No "simply", "just", "easily" claims unless a real customer said it was easy.

## Claims and specifics

- [ ] No vague superlatives (best, fastest, leading, number one, most trusted) unless the proof sits right next to them and is in research/04-proof.md.
- [ ] Every number on the page traces to a source in research/04-proof.md or research/01-goal-offer.md.
- [ ] Adjectives have been swapped for specifics: "replies within 2 hours" instead of "fast support", "no subcontractors" instead of "quality team".
- [ ] Every value prop pairs a feature with what it does for the reader.
- [ ] Each section headline still makes sense to a reader who reads only the headlines.
- [ ] Headlines are 14 words or fewer.

## Customer voice

- [ ] At least three phrases on the page come straight from the language bank in research/02-customers.md.
- [ ] Pain points are described the way customers described them, not in industry jargon.
- [ ] "You" and "your" appear more often than "we", "our" and "us" (lp check reports the ratio).
- [ ] Sentences have the reader as the subject where possible ("You get a quote in 10 minutes", not "We provide fast quotes").

## Proof headlines

- [ ] No generic proof headlines: "Our testimonials", "Our reviews", "What our clients say", "Trusted by many", "Real people, real results".
- [ ] Proof headlines lead with the benefit customers got, using only true numbers.

## Punctuation and rhythm

- [ ] The long dash is rare: no more than the limit in lp.json per 1000 words (lp check warns). Commas, colons, periods or parentheses do the job instead.
- [ ] No exclamation marks in body copy, and at most one on the whole page.
- [ ] No rule-of-three padding: lists of three adjectives or three parallel clauses only where all three items are real and different ("fast, simple, and affordable" fails).
- [ ] No "It's not X, it's Y" or "This isn't just X. It's Y." constructions.
- [ ] No rhetorical question stacks (two or more questions in a row) outside the pain hook.
- [ ] Sentence length varies; not every sentence follows the same pattern.

## Hedging and padding

- [ ] No hedges that weaken a true claim: "may help", "can potentially", "in some cases", "arguably".
- [ ] No throat-clearing intros ("When it comes to X", "It's no secret that", "At the end of the day").
- [ ] No sentence that could be deleted without the reader losing information.
- [ ] No placeholders, sample names or bracketed notes left in the copy (lp check reports them).

## Read-aloud test

- [ ] Read the full page out loud: every sentence sounds like something a person who knows the customer would say across a table.
- [ ] Nothing makes you wince, pause to re-read, or sound like an ad voice-over.
- [ ] A customer from the interviews or reviews would recognise their own problem in the first two sections.
- [ ] The copy could not be moved to a competitor's page by swapping the brand name.
