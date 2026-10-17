# Step 15: Ship

Get on-page SEO, speed and analytics right, then deploy the approved page and confirm it works live.

## Scope

Per page. Runs once for each page, only after a human has approved Gate 3 for that page with `lp approve gate3`. If Gate 3 is missing, stop and ask the human; do not deploy.

## Inputs

- pages/<page>/build/ (the approved page)
- pages/<page>/07-structure.md (the primary keyword)
- research/06-seo.md (keywords, intent, questions for this page)
- references/checklists/seo-onpage.md
- references/checklists/performance.md
- Redesign only: audit/url-map.csv (old_url,new_url,action,reason,clicks_90d,backlinks)

## Do this

1. Confirm Gate 3 is recorded: run `lp status --page <page>`. If it is not approved, stop and ask the human to review and run `lp approve gate3 --page <page> --by "<their name>"`.
2. Set the head tags. Title 50 to 60 characters, primary keyword near the front, brand at the end. Meta description 130 to 155 characters that states the outcome and the next step (it is ad copy for the search result). Exactly one h1 that contains the primary keyword in natural words. A self-referencing canonical with the final absolute URL. Open Graph tags (og:title, og:description, og:image at 1200 by 630, og:url, og:type) and twitter:card set to summary_large_image.
3. Check the body against references/checklists/seo-onpage.md: secondary keywords and People Also Ask questions from research/06-seo.md answered in headings and FAQ, heading levels in order, descriptive link text, alt text on every meaningful image, and no content hidden in images only.
4. Add structured data as JSON-LD: Organization (or LocalBusiness) plus the type that fits the offer (Product, SoftwareApplication, Service), and FAQPage only if the FAQ is visible on the page. Never mark up reviews or ratings that are not shown on the page and sourced in research/04-proof.md. Validate with a rich results or schema validator if you can reach one, and confirm `lp check` parses it.
5. Make the page indexable: no stray noindex, robots.txt allows it and lists the sitemap, the page is in sitemap.xml with its canonical URL, and it is linked from at least one other page (nav or footer) so it is not an orphan.
6. Hit the performance budget: LCP under 2.5 s, CLS under 0.1, INP under 200 ms on mobile. Measure with PageSpeed Insights on a public URL or Lighthouse in a browser on a local or staging build, mobile profile, three runs, take the median. If the budget fails, fix the usual causes: oversized or lazy-loaded hero image, render-blocking CSS or fonts, heavy third-party scripts, long JavaScript tasks. Subset and self-host fonts, preload the one main font file, inline critical CSS if it helps. Once real traffic arrives, check field data too.
7. Install analytics with the owner's tool and consent setup (cookie banner or privacy notice as their jurisdiction requires). Track at least three events: primary CTA click (cta_click, with a location label such as hero or closer), scroll depth (25, 50, 75 and 100 percent), and the conversion itself (form submitted, booking made or purchase completed, fired on success, not on click). Open the tool's debug or real-time view, trigger each event yourself, and confirm it arrives with the right parameters.
8. Redesigns: open audit/url-map.csv and make sure every old URL that changes has a 301 to the most relevant new URL (never a blanket redirect to the home page). Implement the redirects on the host, then test each one: it returns 301 (not 302), lands on a 200 page in one hop, and has no chains or loops. `lp done 15` refuses in redesign mode if the map has no rows.
9. Deploy to wherever the owner hosts: a static host, a CMS (paste or port the build into its page builder or theme), or their existing stack (hand the build to their developer with the head tags, events and redirects listed). Keep the deploy reversible: note the previous version or keep a backup. Record where, when, by whom and the Gate 3 approval reference.
10. Run post-deploy checks on the live URL: loads over HTTPS without errors, canonical and OG tags render (paste the URL into a link preview or sharing debugger), forms deliver to the real destination, analytics events arrive from live traffic, robots and sitemap are reachable, and redirects work on the live domain. If you have Search Console access, submit the sitemap and request indexing for the page.
11. Fill pages/<page>/15-ship.md. When finished run `lp done 15 --page <page>`, fix whatever it reports, then `lp next`.

## Output

- pages/<page>/15-ship.md, from template 15-ship.md. Run `lp start 15 --page <page>` to copy the template into place (it never overwrites).
- The deployed page, plus updated sitemap.xml, robots.txt and (redesign) redirect rules on the host.

## Done when

- [ ] pages/<page>/15-ship.md exists, every template heading is present, and no `{{...}}`, TODO or TBD remains
- [ ] Gate 3 was approved by a human before anything was deployed
- [ ] Title, meta description, single keyword h1, canonical, OG and Twitter tags meet the limits, and JSON-LD validates
- [ ] Mobile LCP under 2.5 s, CLS under 0.1 and INP under 200 ms, with tool and date recorded
- [ ] CTA click, scroll depth and conversion events were each seen arriving in the analytics debug or real-time view
- [ ] Redesigns: every changed URL in audit/url-map.csv returns a single-hop 301 to a live page, tested on the live domain
- [ ] Post-deploy checks pass on the live URL, and the page is in the sitemap and indexable

## Common mistakes

- Deploying first and asking for approval afterwards. Gate 3 comes before any public URL.
- Copying the same title and meta description across pages, or writing a title that is a keyword list.
- Firing the conversion event on button click instead of on confirmed success, which inflates conversions.
- Redirecting every old URL to the home page, which throws away rankings and confuses visitors.
- Loading analytics, chat and pixel scripts synchronously in the head, which wrecks LCP and INP.
- Leaving a staging noindex tag or a disallow rule in place after launch.

## Redesign mode notes

- Sort audit/url-map.csv by clicks_90d and backlinks; test the top rows first and twice.
- Keep the old URL where it ranks well and the content still fits. A redirect you do not need is a risk you do not need.
- After launch, watch Search Console coverage and 404 reports for the first two weeks and add redirects for any missed URLs.
