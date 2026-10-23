# Step 16: Measure and iterate

Find where visitors drop off, test one evidence-backed fix at a time, and feed what you learn back into the research.

## Scope

Per page, repeating. Each cycle starts after the page is live: `lp done 16 --page <page>` closes a cycle, `lp redo 16 --page <page>` opens the next one. Learnings that change the product-level research go back to steps 1 to 6.

## Inputs

- pages/<page>/15-ship.md (live URL, events, deploy date)
- research/01-goal-offer.md (the one goal and the conversion action)
- pages/<page>/16-measure.md (previous cycles: baseline, backlog, results log)
- The owner's analytics tool; Search Console and session recordings or heatmaps if available

## Do this

1. Confirm the data is trustworthy before reading it: events still fire, the conversion event fires on success only, internal traffic and bots are filtered, and there is enough of it. Under roughly 100 conversions a month, treat numbers as directional and lean on qualitative evidence.
2. Record the baseline: visitors, conversion rate and primary CTA click rate for a clear period (full weeks), split by device and traffic source. Mobile and desktop, search and paid social, behave like different pages.
3. Build the funnel: landed, scrolled past the hero, clicked the primary CTA, converted. Use the scroll depth events for "scrolled past hero". The biggest drop is where to look first.
4. Read the drop-off. Big loss at the hero: the headline, subhead or offer does not match what the traffic expected (check ad copy and search queries). People scroll but do not click: proof, objections or the CTA itself. People click but do not convert: the form, the price, or the next page. Add evidence: session recordings, heatmaps, form field drop-off, Search Console queries, support questions, and short on-page or post-purchase surveys ("What nearly stopped you today?").
5. Hold the 14-day review: is tracking right, is anything broken, does traffic match the intended temperature and source? Fix bugs now; do not judge the copy yet. Hold the 30-day review: compare against the baseline, decide what is the biggest leak, and pick the next test. Log both in the reviews table.
6. Write hypotheses in the form "If we change X, then metric Y moves, because evidence Z." Every hypothesis cites real evidence (a funnel number, a recording pattern, a customer quote). Score each on Impact, Confidence and Ease from 1 to 10 and multiply or average them for ICE. Sort the backlog by ICE. An example row:

   | If we change | Then | Because (evidence) | I | C | E |
   |---|---|---|---|---|---|
   | Hero headline from feature to outcome | Hero-to-CTA click rate rises | 62% of mobile visitors leave before 25% scroll; top customer quote names the outcome, not the feature | 8 | 6 | 9 |

7. Ask the owner which test to run next (a question or button prompt if your agent has one, such as `AskUserQuestion` in Claude Code, otherwise plain text): offer the top 3 hypotheses by ICE, each with its evidence and a rough duration from step 8, the highest first. Run one test at a time on the page, on the one they pick. Change one idea per variant (a new headline is one idea; a new headline plus a new hero image is two). Use a proper split-testing tool if traffic allows; otherwise run a before and after comparison and label it as weaker evidence.
8. Size the test before starting. Use a sample size calculator with your baseline conversion rate and the smallest lift worth detecting; write the visitors needed per variant and the planned duration. Run whole weeks (at least two) to cover weekday and weekend behavior. Set the stop rule in advance: stop at the planned sample, not when the result looks good. No peeking and stopping early. If the needed sample would take months, test bigger changes or use qualitative methods instead.
9. Log every result in the results log, including losers and flat tests: dates, variants, result, confidence, and whether it shipped. A loser that disproves a belief is worth as much as a winner.
10. Feed learnings back. If a test shows the customer cares about a different pain, the competitor gap is wrong, or the offer needs to change, update the research: run `lp redo N` for that step (for example `lp redo 2` for customers or `lp redo 1` for the offer), update the file, and run `lp done N` again. Page-only learnings go back to step 8 with `lp redo 8 --page <page>`. Any changed claim must still trace to research/04-proof.md.
11. When a new search query cluster or audience segment deserves its own page, add one with `lp page add <slug> --keyword "<keyword>"`; it starts at step 7 and reuses the research and brand.
12. Close the cycle: fill pages/<page>/16-measure.md, run `lp done 16 --page <page>`, fix whatever it reports, then `lp next`. To start the next cycle, run `lp redo 16 --page <page>` and keep the previous results log in the same file.

## Output

- pages/<page>/16-measure.md, from template 16-measure.md. Run `lp start 16 --page <page>` to copy the template into place (it never overwrites). Later cycles add to the same file.

## Done when

- [ ] pages/<page>/16-measure.md exists, every template heading is present, and no `{{...}}`, TODO or TBD remains
- [ ] Baseline and funnel are filled from real analytics for a stated period, with the source named
- [ ] The 14-day and 30-day reviews are logged with a decision each
- [ ] Every backlog hypothesis cites evidence and has an ICE score, sorted highest first
- [ ] The current test has one change, a primary metric, a sample size, a duration in full weeks and a stop rule set in advance
- [ ] Every finished test is in the results log, including losers and flat results
- [ ] Learnings that change research or copy were fed back with `lp redo N`

## Common mistakes

- Stopping a test the day it looks like a winner. Early leads often vanish by the planned end.
- Testing button colors while the hero promises the wrong outcome to the traffic it gets.
- Running several tests on the same page at once, so no result can be attributed.
- Calling a winner on a few dozen conversions, or on one week that included a holiday or a campaign spike.
- Deleting losing tests from the log, then retesting the same idea six months later.
- Optimizing CTA clicks while the real conversion (paid, booked, qualified) does not move.

## Redesign mode notes

- Compare the new page against the old page's numbers from audit/site-audit.md for the same season and traffic mix, not just the weeks before launch.
- Watch organic clicks for the URLs in audit/url-map.csv for at least 30 days. A drop on a redirected URL usually means a missed or wrong redirect, not bad copy.
