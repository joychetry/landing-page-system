# Checklist: on-page SEO

Used in step 8 (SEO copy), step 14 (last checks) and step 15 (ship). Run `lp check --page <page>` first; it covers the items marked (lp check), and a reviewer covers the rest.

## Keyword and intent

- [ ] The page has exactly one primary keyword, taken from the keyword-to-page map in research/06-seo.md and recorded in pages/<page>/07-structure.md.
- [ ] No other page in the workspace or on the live site targets the same primary keyword (lp check reports cannibalization).
- [ ] The page content matches the search intent seen in the current top results (a buying page for a buying query, a guide for an informational one).
- [ ] Secondary keywords and People Also Ask questions from research/06-seo.md are answered in headings, value props or the FAQ, in natural language.

## Title and meta description

- [ ] A `<title>` exists (lp check).
- [ ] The title is 50 to 60 characters (lp check warns outside this range).
- [ ] The primary keyword appears in the title, near the start.
- [ ] The title is unique across the site and reads like a promise, not a keyword list.
- [ ] A meta description exists (lp check).
- [ ] The meta description is 130 to 155 characters (lp check warns outside this range).
- [ ] The meta description states the outcome, one proof point or reducer, and the action, and includes the primary keyword once.

## Headings

- [ ] There is exactly one H1 (lp check).
- [ ] The H1 contains the primary keyword or a close variant, worded for people first.
- [ ] Headings go in order (H1, then H2, then H3) with no skipped levels used for styling.
- [ ] Each H2 describes its section so a reader who scans only headings understands the page.

## Head tags

- [ ] `<html lang="...">` is set to the page language (lp check).
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">` is present (lp check).
- [ ] A canonical link points to the page's own final URL, absolute, with the chosen protocol and trailing slash style (lp check warns if missing).
- [ ] og:title, og:description and og:image are set (lp check), og:url matches the canonical, and og:image is at least 1200 by 630 pixels.
- [ ] twitter:card is set to summary_large_image (lp check reports it as info).
- [ ] A favicon is linked.

## Structured data

- [ ] JSON-LD is present in a `<script type="application/ld+json">` block (lp check warns if missing) and parses as valid JSON (lp check).
- [ ] The type fits the page: Organization or LocalBusiness on the home page, Product or SoftwareApplication for a product page, Service for a service page, FAQPage only if the FAQ is visible on the page, BreadcrumbList for nested pages.
- [ ] Every value in the JSON-LD matches what is visible on the page (no ratings, prices or reviews that the page does not show).
- [ ] The markup passes a structured data validator (search the web for the official rich results test or the schema.org validator).

## Images and links

- [ ] Every `<img>` has an alt attribute (lp check); informative images describe what they show, decorative images use alt="".
- [ ] Image file names are descriptive (team-at-install.webp, not IMG_2041.jpg).
- [ ] The page links to at least two relevant internal pages, and at least one existing page links to it.
- [ ] Anchor text describes the destination ("see pricing plans"), never "click here" or a bare URL.
- [ ] No link has an empty href (lp check) or href="#" (lp check warns).
- [ ] No internal link points to a URL that redirects or returns 404.

## URL and indexing

- [ ] The URL slug is short, lowercase, hyphenated and contains the primary keyword (for example /solar-panel-cleaning).
- [ ] The page is not blocked: no `noindex` meta tag or header, not disallowed in robots.txt.
- [ ] robots.txt exists at the site root and lists the sitemap URL.
- [ ] sitemap.xml includes the page's canonical URL and no redirected or noindexed URLs.
- [ ] If you have Search Console access, the sitemap is submitted and the page URL is inspected after launch.

## Redesigns and changed URLs

- [ ] Every old URL in audit/url-map.csv has an action: keep, 301 redirect, or retire with a reason.
- [ ] Every changed URL has a 301 (permanent) redirect to its closest new equivalent, not to the home page by default.
- [ ] No redirect chains: each old URL reaches its final URL in one hop.
- [ ] Pages with clicks or backlinks in the last 90 days keep their URL or get a 301; none are left to 404.
- [ ] Internal links, canonical tags and the sitemap use the new final URLs, not the redirected ones.
