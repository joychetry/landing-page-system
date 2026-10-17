# Step 0: Audit the existing site

Capture what the live site says, what search traffic and links it has earned, and where it loses
visitors, so the redesign keeps what works and fixes what does not.

## Scope

Product-level, redesign mode only, runs once before step 1. New-site workspaces skip this step.
Everything here is evidence gathering: you change nothing on the live site.

## Inputs

- The live URL in `lp.json` (the `url` field).
- The site's `sitemap.xml` (try `/sitemap.xml`, `/sitemap_index.xml`, and the `Sitemap:` line in
  `/robots.txt`) and its header and footer navigation.
- Search Console data for the property, if the owner can give you access or an export.
- Analytics (conversion events, top landing pages), if available.
- Checklists for scoring: `references/checklists/hero.md`, `references/checklists/seo-onpage.md`,
  `references/checklists/performance.md`, `references/checklists/accessibility.md`.

## Do this

1. Run `lp start 0`. It copies the templates into `audit/site-audit.md` and `audit/url-map.csv` and
   never overwrites existing files. Create the folder `audit/pages/`.
2. Build the page list. Read the sitemap first. If there is none, open the homepage in a browser and
   collect every link in the header, footer and main navigation, then follow one level deeper. Add
   any page that gets clicks in Search Console even if it is not linked (old campaign pages often
   hide there). If your agent has a crawling tool or skill, use it; otherwise fetch pages one by
   one. For sites over about 50 pages, save copy for navigation pages and every page with search
   clicks, and list the rest only in the URL map.
3. Save the current copy of each important page to `audit/pages/<slug>.md`, one file per page.
   Record at the top: URL, date crawled, `<title>`, meta description, canonical, H1. Then copy the
   body section by section in page order, word for word: every heading, paragraph, button label with
   its link target, form fields, and every proof item shown (reviews, logos, numbers). This is the
   record of what existed; the live site will change.
4. Check history. Open the homepage and the main landing pages in the Wayback Machine
   (web.archive.org) and note any older headline, offer or price that differs from today. Changes
   often mark past tests or pivots the owner can explain. Record them in the audit with the archive
   URL.
5. Pull 90 days of search data if you have Search Console access: Performance report, last 3 months,
   export top queries and top pages with clicks, impressions, CTR and average position. Also open
   the Links report for the top linked pages. Without access, write "no Search Console access" and
   use free signals: a `site:` search for indexed pages, the queries the owner says customers use,
   and which pages rank when you search those terms. Fill `## Search data`.
6. List every URL that must survive. A URL must be preserved or 301-redirected if it has any search
   clicks in 90 days, ranks on page one for a query that matters, has external backlinks, receives
   paid ads traffic, or is printed on materials (cards, packaging, emails). Write each one into
   `audit/url-map.csv` with columns `old_url,new_url,action,reason,clicks_90d,backlinks`. Use
   `action` values `keep`, `301`, `merge` or `retire`. Write `unknown` where you have no data, never
   a guess. Fill `## URLs to preserve` with the important ones.
7. Score each saved page 0 to 5 per column in `## Page scores`. Hero: does the headline state the
   dream outcome, the subhead the how, with 2 proof items, one CTA and a FUD reducer visible on a
   360 px wide screen without scrolling (use the hero checklist). Proof: is real proof visible, near
   the claims it supports, not hidden in a carousel. Clarity of offer: could a stranger say what is
   sold, to whom, and what happens after the click. Mobile: open it at 360 px; check tap targets,
   text size, no sideways scroll. Speed: run it through PageSpeed Insights or Lighthouse and note
   LCP and CLS. SEO basics: one H1, title and meta description present and specific, sensible
   headings, image alt text.
8. Mark weak sections in `## Weak sections`: page, section, the problem in one line, and the
   evidence (a score, a metric, a screenshot, a quote from the saved copy). Typical finds: headline
   that says who the company is instead of what the customer gets, feature lists with no benefit,
   generic proof headlines such as "Our testimonials", several competing CTAs, FAQ that dodges
   price.
9. Collect evidence for research files 1 to 6 under `## Evidence for research`, grouped by file.
   Examples: current offer, price and guarantee (01), testimonials and review counts already shown
   (04), stated mission or founder story (05), queries and ranking pages (06). Mark every item
   `source: live-site` with its URL.
10. Pre-fill the research files. For each of steps 1 to 6, run `lp start N` (it only copies the
    template; it never overwrites) and paste the matching evidence into the right section with its
    `source: live-site` marker. Leave the rest of each file for its own step; those steps are not
    done until their guides are followed. Live-site copy is the company's words, not the customer's:
    it never counts as a verbatim customer quote in step 2.
11. Decide what to rebuild in `## Rebuild decisions`: rebuild, keep, merge or retire, with the new
    slug and the reason. Prefer rebuilding the few pages that carry traffic or conversions first.
    The `home` page already exists in the workspace. For each other page to rebuild, run
    `lp page add <slug> --url <old url>`; it starts at step 7 and reuses the product research. Make
    sure every rebuilt page with a changed URL has a `301` row in the URL map.
12. When finished, run `lp done 0`, fix whatever it reports, then run `lp next`.

## Output

- `audit/site-audit.md` (template: 00-site-audit.md)
- `audit/url-map.csv` (template: url-map.csv)
- `audit/pages/<slug>.md`, one per audited page (no template; plain Markdown copy of the page)

Run `lp start 0` to copy the templates into place (it never overwrites).

## Done when

- [ ] `audit/site-audit.md` has every `##` heading from the template and no `{{...}}`, `TODO` or `TBD` left.
- [ ] `audit/url-map.csv` has at least one data row, and every URL with search clicks, rankings, backlinks or ads traffic appears in it with an action.
- [ ] `audit/pages/` holds at least one saved page, and every page you plan to rebuild has its current copy saved word for word.
- [ ] Search data covers the last 90 days, or the audit says plainly that there was no access and which free signals were used.
- [ ] Every crawled page has a score in all six columns, and every weak section cites evidence.
- [ ] Evidence for research files 1 to 6 is listed and marked `source: live-site` with a URL.
- [ ] Every page marked rebuild has a slug and was added with `lp page add <slug> --url <old url>` (except `home`, which already exists).

## Common mistakes

- Starting the redesign from the old design instead of the old evidence. The audit records what the
  site says and earns; it does not decide the new layout.
- Dropping URLs that rank or have backlinks because they look unimportant. A deleted page with links
  throws away earned authority; redirect it to the closest relevant page instead.
- Summarizing the old copy instead of saving it verbatim. You lose the phrases that may be why a
  page ranks.
- Scoring pages on taste ("looks dated") instead of the checklists and numbers.
- Treating claims on the live site as verified. A "500+ happy clients" line on the old site still
  needs a source from the owner before it can appear in `research/04-proof.md`.
- Inventing click or backlink counts when there is no data. Write `unknown`.

## Redesign mode notes

This whole step is redesign mode. Two things carry forward: the URL map becomes the redirect plan
checked in step 15, and the saved copy in `audit/pages/` is the baseline you compare against in step
16. Record the current conversion rate for each rebuilt page now, if analytics has it, so the
redesign can be judged against a real number.
