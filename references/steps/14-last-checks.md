# Step 14: Last checks

One last pass over branding, copy and design so nothing false, broken or off-brand reaches a human approver, then stop for Gate 3.

## Scope

Per page. Runs once for each page, after step 13. Gate 3 follows this step and must be approved by a human before step 15 (ship).

## Inputs

- pages/<page>/build/ (the finished page)
- pages/<page>/08-copy.md (the approved copy)
- research/04-proof.md (every claim must trace here)
- brand/brand.md
- All checklists in references/checklists/: hero.md, seo-onpage.md, performance.md, accessibility.md, de-ai-copy.md

## Do this

1. Run `lp check --page <page>`. Fix every error: missing or duplicate h1, missing title or meta description, missing viewport or lang, img without alt, empty links, broken JSON-LD, banned phrases, leftover placeholders. `lp done 14` re-runs the check and refuses while any error remains.
2. Review every warning and either fix it or write down why it stays (for example a 61-character title that reads better than the 58-character version). Warnings on em dash density, exclamation marks, long headlines and `href="#"` usually mean a real fix.
3. Proofread out loud on the built page in a browser, not in the markdown file. Reading aloud catches missing words, repeated words and clumsy rhythm. Check every name, price, currency, date, unit, phone number and legal entity against the source. Compare against pages/<page>/08-copy.md and note any change made since approval.
4. Run the de-AI pass from references/checklists/de-ai-copy.md one more time: vague superlatives, filler openers, three-item lists that all say the same thing, "we" sentences that should be "you" sentences.
5. Test every link and button. Click each one at desktop and at 360px: primary CTA, secondary links, nav, footer, legal pages, email and phone links. Submit the form with test data and confirm it reaches its destination (inbox, CRM, checkout) and shows a clear success state. Record each in the links table.
6. Trace every claim to research/04-proof.md: each number, testimonial, star rating, customer count, logo, award, guarantee and "as seen in" mention. If a claim has no matching row with a source and permission, remove it or soften it to what the proof supports. Never add a new claim at this stage.
7. Check brand consistency against brand/brand.md: colors and type come from the tokens, voice matches, logo use follows the rules, and the hero pattern holds in every section.
8. Walk the hero checklist in references/checklists/hero.md against the built hero, and skim the other checklists for anything steps 12 and 13 missed.
9. Run a five-second test with a real person who has not seen the page (not the owner, not you). Show the hero on a phone for five seconds, hide it, and ask: what is this offering, who is it for, and what would you do next? If they cannot answer the first and last questions, fix the headline, subhead or CTA and test again with someone new. An agent cannot do this step on its own; ask the human to run it and report the answers.
10. Fill pages/<page>/14-checks.md, including notes for Gate 3: open proof gaps, known limits, decisions taken. Then run `lp done 14 --page <page>` and fix whatever it reports.
11. GATE 3. STOP here. Show the human the built page (a local preview or a staging URL), the 14-checks.md summary and any open warnings. Ask them to review it and ask them to choose Approve or Request changes (a question or button prompt if your agent has one). Only after they choose Approve, run `lp approve gate3 --page <page> --by "<their name>"` for them. Never approve without their answer, and never deploy anything before this approval exists. After the human approves, run `lp next`. A message to the human can be as short as:

   > The <page> page is ready for review at <preview link>. `lp check` shows 0 errors and <n> warnings (reasons in 14-checks.md). Open items: <gaps>. Approve, or tell me what to change? I will not deploy until you approve.


## Output

- pages/<page>/14-checks.md, from template 14-checks.md. Run `lp start 14 --page <page>` to copy the template into place (it never overwrites).
- Any fixes applied to pages/<page>/build/.

## Done when

- [ ] pages/<page>/14-checks.md exists, every template heading is present, and no `{{...}}`, TODO or TBD remains
- [ ] `lp check --page <page>` reports zero errors, and every remaining warning has a written reason
- [ ] The built page was proofread aloud, and names, prices, dates and contact details match their sources
- [ ] Every link and button was clicked at desktop and mobile, and a test form submission arrived
- [ ] Every number, testimonial, logo and guarantee traces to a row in research/04-proof.md; anything untraceable was removed
- [ ] A real person passed the five-second test: they named the offer and the next step
- [ ] The agent stopped and asked the human to approve Gate 3; it recorded approval only after they chose Approve, and did not deploy before

## Common mistakes

- Treating `lp check` passing as "done". It catches structure, not whether the copy is true or clear.
- Proofreading the markdown instead of the rendered page, missing truncated text, wrong line breaks and stale button labels.
- Leaving a testimonial or statistic in because it "sounds right" with no row in research/04-proof.md.
- Running the five-second test on the owner or the team, who already know what the page means.
- Fixing an `lp check` error by deleting the element (an image, a link) instead of repairing it.
- Deploying "just to staging that is publicly indexed" before Gate 3. Any public URL counts as shipping.

## Redesign mode notes

- Compare the new page's claims against the old page (audit/pages/<slug>.md). Claims dropped on purpose are fine; claims that changed (prices, guarantees, numbers) need owner confirmation.
- Check that every URL the old page linked to still exists or is in audit/url-map.csv.
- Add to the Gate 3 notes which old URLs this page replaces, so the approver sees the redirect impact.
