# Step 3: Competitor research

Map what the alternatives promise, charge and prove, and where their own customers say they fall
short, so the page can claim the gaps nobody else owns.

## Scope

Product-level, runs once. Every page reuses this file. The goal is positioning, not imitation: you
study competitors to say something different and provable, never to copy their layout or lines.

## Inputs

- `research/01-goal-offer.md` (offer, facets, traffic).
- `research/02-customers.md` (pains, objections, language bank, and any competitors customers
  mentioned).

## Do this

1. Run `lp start 3` to copy the template to `research/03-competitors.md`. Set `verified:` to today's
   date.
2. Build a long list from four places. Ask the owner who they lose deals to and who customers
   compare them with. Pull every competitor or workaround named in `research/02-customers.md` ("we
   switched from ...", "I was using a spreadsheet"). Search the web for the main problem keywords
   and the category name and note who ranks organically and who runs search ads on the results page.
   Check review-site category pages (G2, Capterra, app store categories, local directories) and
   searches like "<competitor> alternatives".
3. Cut it to 3 to 7 competitors that chase the same buyer, the same search or the same budget.
   Include the real alternative if that is what customers mostly choose: doing nothing, doing it
   themselves, hiring a person, or a spreadsheet. Fill `## Competitor list` with why each competes
   and the traffic they chase (search, social ads, marketplace, referrals).
4. Capture each hero. Open each competitor's homepage, and the landing page their ads point to if
   you can find it, in a browser. Copy the headline exactly, the subheadline, and the primary CTA
   label into `## Hero claims` with the URL and the date you saw it. Note whether the headline
   states an outcome or just describes the company.
5. Check what they run in ads, if relevant. The public ad libraries (Meta Ad Library, Google Ads
   Transparency Center) show active ads and their landing pages. Long-running ads are usually the
   ones that work for them.
6. Record offer and pricing from their pricing or offer page: what is included, price and billing
   terms, free trial, guarantee or cancellation terms. If the price is hidden ("contact us"), write
   that; it is a useful fact. Link every row.
7. List the proof each one shows: review counts and scores, client logos, numbers, case studies,
   press, certifications. Note their single strongest proof point. This tells you the proof bar your
   page must clear in step 4.
8. Mine their weaknesses from their own customers. Read 1 to 3 star reviews on G2, Capterra,
   Trustpilot, Google, app stores, and Reddit threads that name them. Copy complaints word for word
   with links, and note how often each comes up across the reviews you read (for example "8 of 40
   reviews"). Read at least 20 reviews per main competitor where that many exist.
9. Optional but useful: look at their homepage in the Wayback Machine (web.archive.org). A headline
   that changed several times shows what they tested; one that has not changed in years is probably
   working or neglected.
10. Find the gaps. A gap is something buyers want (it appears in `research/02-customers.md`),
    competitors do badly or do not say (it appears in this file), and you can prove. Write each in
    `## Gaps we can own` with its evidence. For the proof column, write the proof you believe exists
    and mark it "to confirm in step 4". In step 4 the proof is either confirmed or moved to the Gaps
    list in `research/04-proof.md`; a gap with no proof is dropped from this table.
11. Write the positioning statement: for [who] who [need], [product] is the [category] that [key
    benefit]. Unlike [main alternative], we [differentiator we can prove]. Use the customer's words
    for the need and benefit.
12. When finished, run `lp done 3`, fix whatever it reports, then run `lp next`.

## Output

`research/03-competitors.md` (template: 03-competitors.md). Run `lp start 3` to copy the template
into place (it never overwrites).

## Done when

- [ ] Frontmatter has `verified: YYYY-MM-DD` (not in the future), every template `##` heading is present, and no `{{...}}`, `TODO` or `TBD` remains.
- [ ] The file has at least 3 source markers; in practice every claim about a competitor links to the page or review where you saw it.
- [ ] Between 3 and 7 competitors are listed, including "do nothing" or "do it yourself" where customers really choose it.
- [ ] Every hero headline is copied exactly, with URL and date.
- [ ] Weaknesses are verbatim complaints from their customers, with links and a rough frequency.
- [ ] At least 3 gaps are listed, each tied to customer evidence and to proof you have or will confirm in step 4.
- [ ] The positioning statement names a differentiator you can prove.

## Common mistakes

- Listing every company in the category. Seven well-researched competitors beat twenty names with no
  detail.
- Ignoring the status quo. For many products the real competitor is a spreadsheet, an employee, or
  putting it off.
- Judging competitors by their design instead of their message, offer and proof.
- Copying a competitor's headline structure or claims. If your page could swap logos with theirs and
  still read true, the positioning has failed.
- Claiming a gap you cannot prove ("the only ...", "the fastest ..."). Superlatives need evidence,
  and naming a competitor negatively on the page needs even more.

## Redesign mode notes

Compare the old site's hero, saved in `audit/pages/`, against the competitors' heroes side by side.
If the old headline could belong to any competitor, record that as a weak section finding in
`audit/site-audit.md`. Search Console queries that mention competitor names show who searchers
compare you with; add them to the long list.
