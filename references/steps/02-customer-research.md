# Step 2: Customer research

Find out who buys, what hurts, what they want instead, what stops them, and the exact words they
use, so the page can speak in their language instead of yours.

## Scope

Product-level, runs once. Every page reuses this file. The language bank built here feeds every
headline in step 8.

## Inputs

- `research/01-goal-offer.md` (the conversion action, dream outcome and offer facets).
- Owner-supplied material, if any: support tickets, sales call notes or recordings, survey answers,
  onboarding forms, cancellation reasons, customer emails.

## Do this

1. Run `lp start 2` to copy the template to `research/02-customers.md`. Set `verified:` to today's
   date.
2. Ask the owner for first-party sources before searching the web; they are the richest. Support
   tickets and chat logs (the last 50 to 100), sales call notes or recordings, intake and onboarding
   forms, survey answers ("what almost stopped you from buying?"), cancellation or refund reasons.
   Remove names, emails and other personal details before pasting anything. Mark these "provided by
   owner, YYYY-MM-DD".
3. Mine public reviews. Search for reviews of the product and of the two or three main competitors
   on the platforms where this market leaves them: Google Business Profile, Trustpilot, G2,
   Capterra, app stores, Amazon, Yelp, industry directories. Read the 3 and 4 star reviews closely:
   they name what is missing. Read 1 and 2 star reviews of competitors for unmet needs.
4. Mine conversations. Search the web for the problem in plain words with `site:reddit.com`, niche
   forums, public community groups, Quora, and comments under popular YouTube videos on the topic.
   Search the way a customer would ("how do I ...", "is it worth ...", "anyone tried ...",
   "<competitor> alternative"). Link to the specific comment, not the thread, when the platform
   allows it.
5. If the owner can arrange it, interview 3 to 5 recent buyers for 20 minutes each. Ask about the
   moment they decided to look for a solution, what they tried before, what nearly stopped them, and
   what changed after. Record their words, not your summary.
6. Copy quotes word for word into `## Verbatim quotes`, typos and slang included. Each row gets the
   segment or role, the source type and the source (a URL, or "provided by owner, YYYY-MM-DD"). How
   much is enough: at least 20 quotes from at least 3 different source types. Keep going until new
   quotes stop revealing new pains or objections; that is saturation (as a rule of thumb, often
   somewhere between 30 and 60 quotes in a focused market).
7. Tag and count. For each quote, note the pain, desire or objection it expresses. Rank `## Pains`
   by how often each one appears in the evidence, with the count in "Times seen", not by how
   important it feels to you or the owner. For each pain, write how it shows up in their day and
   what it costs them (time, money, stress, status).
8. Fill `## Who buys`: segments, the trigger moment that made them look now, what they tried before,
   and where they look for solutions. Choose the primary segment for the first page, ideally the one
   matching the traffic in step 1.
9. Write 3 to 5 jobs-to-be-done statements in the form "When [situation], I want to [motivation], so
   I can [expected outcome]", each grounded in quotes you collected.
10. Fill `## Desired outcomes` with the outcome in their words and a measurable version, and
    `## Objections and fears` with a verbatim example of each, the honest answer you can give, and
    the proof that answer will need in step 4. If there is no honest answer yet, say so; that
    becomes a gap.
11. Build the language bank: the words they use for the problem, for the outcome, phrases worth
    lifting into headlines, and the jargon from your own team or industry that customers never use.
    The last list is as useful as the first.
12. Log every source in `## Sources reviewed`: type, where, how many items you read, and the date.
13. When finished, run `lp done 2`, fix whatever it reports, then run `lp next`.

## Output

`research/02-customers.md` (template: 02-customers.md). Run `lp start 2` to copy the template into
place (it never overwrites).

## Done when

- [ ] Frontmatter has `verified: YYYY-MM-DD` (not in the future), every template `##` heading is present, and no `{{...}}`, `TODO` or `TBD` remains.
- [ ] The file has at least 3 source markers (URLs, "provided by owner, YYYY-MM-DD", or "source: live-site"); in practice every quote and every row has one.
- [ ] There are at least 20 verbatim quotes from at least 3 source types, copied exactly.
- [ ] Pains are ranked by how often they appear, with counts.
- [ ] Every objection has a verbatim example and either an honest answer or a note that proof is missing.
- [ ] The language bank lists their words for the problem and the outcome, reusable phrases, and jargon to avoid.
- [ ] A reader could name the primary segment and its trigger moment in one sentence.

## Common mistakes

- Paraphrasing. "Users find setup difficult" is your summary; "I spent a whole Saturday on this and
  still couldn't get the calendar to sync" is research. Only the second one writes headlines.
- Inventing a persona ("Marketing Mary, 34, loves yoga") instead of describing segments from
  evidence.
- Reading only five-star reviews of your own product. Happy customers tell you what worked; unhappy
  ones and competitors' customers tell you what the market is missing.
- Using public quotes from forums or competitor reviews as testimonials. These are research only.
  They never appear on the page as proof for this product.
- Letting the owner's view of the main pain override the counts. Record both, but rank by evidence.

## Redesign mode notes

Use the saved pages in `audit/pages/` for objections (the old FAQ shows what people asked) and the
Search Console queries in `audit/site-audit.md` for how people phrase the problem; queries are real
customer words. Testimonials already on the live site may be used as quotes if you can find their
original source; mark them `source: live-site` with the URL. Never count the old site's own
marketing copy as customer language.
