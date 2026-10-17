# Step 6: SEO research

Find the keywords each planned page should rank for and the questions searchers ask, then assign every keyword to exactly one page.

## Scope

Product-level. Done once per product. The keyword-to-page map covers every page you plan to build now or later, so each new page added with `lp page add` picks its primary keyword from this file instead of starting fresh. Revisit it when you add a page the map did not foresee.

## Inputs

- `research/01-goal-offer.md`: the offer, its facets, the conversion action and the traffic source.
- `research/02-customers.md`: the language bank. Customers' own words are your best seed keywords.
- `research/03-competitors.md`: competitor URLs to inspect for the pages and terms they target.
- Redesign mode: `audit/site-audit.md` and `audit/url-map.csv` (pages that already rank and must keep their terms).

## Do this

1. List the pages you plan to build (start with `home`, then likely pages such as pricing, a feature page per main offer facet, a page per audience or location). One row per page in the keyword-to-page map, even if the page is weeks away.
2. Write 15 to 30 seed terms: the product category, the dream outcome in plain words, the problem as customers describe it (from the language bank), competitor brand names plus "alternative", and "for <audience>" variants.
3. Pull real demand data, best source first:
   - If you have Search Console access: export the last 90 days of queries and pages (clicks, impressions, average position). Queries with impressions but few clicks are quick wins.
   - If you have a keyword tool: record volume and difficulty for each seed and its variants.
   - Otherwise use free signals. Search engine autocomplete for each seed (type the seed, then the seed plus each letter a to z for the main two or three seeds). The "People also ask" box. "Related searches" at the bottom of the results. The title tags and H1/H2 headings of the competitor pages in `research/03-competitors.md`.
   - Record free signals as demand signals ("appears in autocomplete", "PAA present", "3 competitors target it"), never as invented volumes.
4. Classify intent for every keyword: informational (wants to learn), commercial (comparing options), transactional (ready to buy or sign up), navigational (wants a specific brand). A landing page targets commercial or transactional intent. Informational terms go to an FAQ answer or a future article, not a landing page headline.
5. Run a SERP check on each candidate primary keyword. Search it in a private browser window, in the target country, and record the top 5 to 10 results: URL, page type (product page, listicle, comparison, article, directory, video), what they cover and what is missing. If the top results are all articles, a sales page will struggle for that term; pick a different primary keyword for the landing page and note the term as content for later.
6. Collect questions. Record People Also Ask questions word for word (open three or four to make more appear), plus questions from forums, review sites and support tickets already in `research/02-customers.md`. Aim for 10 to 20 questions. Note where each one was seen and which page will answer it.
7. Build the keyword-to-page map. Each page gets one primary keyword (commercial or transactional, realistic difficulty, matching what that page actually offers) and 2 to 5 secondary keywords (close variants and sub-topics). A keyword appears as primary on one page only. If two pages want the same term, merge them or give one a narrower term. `lp` treats duplicate primary keywords as an error because two pages competing for one query usually both rank worse.
8. Set the planned URL for each page: short, lowercase, hyphenated, containing the primary keyword or its core noun. In redesign mode keep the existing URL wherever the page already ranks.
9. Write content gaps: questions and sub-topics searchers want that no top result answers well, and the page that will cover each.
10. Fill the Data sources table with every source, what it gave you and the date. Add `verified: YYYY-MM-DD` frontmatter with today's date.

How much is enough: every planned page has one primary and at least two secondary keywords, every primary keyword has a SERP check, at least 10 real questions, and at least 3 cited sources. Do not chase hundreds of keywords; a landing page ranks for a cluster, not a spreadsheet.

## Output

`research/06-seo.md`, from template: 06-seo.md. Run `lp start 6` to copy the template into place (it never overwrites). When finished run `lp done 6`, fix whatever it reports, then `lp next`.

## Done when

- [ ] `research/06-seo.md` has `verified: YYYY-MM-DD` frontmatter with a real date that is not in the future.
- [ ] At least 3 source markers are present (URLs, "provided by owner, YYYY-MM-DD", or "source: live-site").
- [ ] Every `## ` heading from the template is present and no `{{...}}`, TODO or TBD remains.
- [ ] Every planned page has a row in the keyword-to-page map with one primary keyword, 2 or more secondary keywords, an intent and a planned URL.
- [ ] No primary keyword appears on two pages.
- [ ] Every primary keyword has a SERP check row showing what ranks and the angle you can win.
- [ ] At least 10 questions are recorded in exact wording, each assigned to a page.
- [ ] Every volume or demand figure names its source; nothing is estimated from memory.

## Common mistakes

- Picking a primary keyword because it has the biggest volume, when the results page is all articles or all giant brands. Match the page type that already ranks.
- Choosing informational terms ("what is X") as the primary keyword of a sales page.
- Giving home and a feature page the same primary keyword, so they cannibalize each other.
- Inventing search volumes. If you have no tool, write the demand signal you saw and where.
- Rewriting People Also Ask questions into your own words. Keep the searcher's wording: it feeds FAQ headings in step 8.
- Ignoring the customer language bank. Searchers type the words customers use, not the category name the company prefers.

## Redesign mode notes

- Start from Search Console or analytics data saved in the audit. Pages with clicks or backlinks keep their URL and their current ranking terms as primary keywords unless there is a strong reason to change.
- Check `audit/url-map.csv`: every page that will move or merge needs its old ranking terms carried into the new page's secondary keywords.
- Look for cannibalization already on the live site (two URLs ranking for one query) and fix it in the map by choosing one owner page.
- Mark facts taken from the live site or its data as `source: live-site`.
