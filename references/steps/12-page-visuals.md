# Step 12: Page visuals

Give every section a visual that explains or proves what its copy claims, and ship those images fast and accessible.

## Scope

Per page. Runs once for each page, after Gate 2 (final design) is approved. Product-level assets in brand/assets/ and assets/ are reused across pages.

## Inputs

- pages/<page>/08-copy.md (the claims each visual must support)
- pages/<page>/11-design/ (the chosen hero direction)
- pages/<page>/build/index.html (the real page; visuals go in here)
- research/04-proof.md (screenshots, results, photos and their permission status)
- assets/ (logos, screenshots, photos supplied by the owner)

## Do this

1. Walk the page section by section in pages/<page>/08-copy.md. For each section write one question: "What would a visitor need to see to believe this?" A headline that promises "see every invoice in one place" needs the screen that shows every invoice in one place. If no visual makes a claim easier to believe, the section gets none.
2. Pick the type that explains best, in this order of preference:
   - Real product screenshots or short screen recordings (cropped to the part that matters, annotated with one or two callouts, not the whole UI at thumbnail size).
   - Before and after (for visual offers: the old state with its pain points beside it, the new state with its benefits beside it; this often is the pain point section).
   - Simple diagrams (how it works, what connects to what, a three-step flow drawn as three steps).
   - Real photos of the team, the place, the product in use, or actual customers who gave permission.
   - Data visuals of real results already recorded in research/04-proof.md.
3. Design the hero visual first. It must show the thing they get or the outcome they want, reinforce the headline, and still read on a 360px screen. Test it: crop the page to a phone viewport; if the visual is unreadable or pushes the CTA below the fold, crop tighter or swap it for a simpler shot.
4. Source real material before making anything. Check assets/ and research/04-proof.md first. Take fresh screenshots of the live product with realistic but non-sensitive data (no real customer names, emails or invoices without permission; use a demo account). Anything missing goes in the table as "need from owner" with a precise request (what screen, what state, what size).
5. Make diagrams and illustrations only where they explain something. If your agent has an image-generation tool, use it only for diagrams, icons and abstract illustrations. Never use it to fake a product screenshot, a customer photo, a team photo, a logo, a review card or a result. Prefer hand-built SVG for diagrams: it is sharp at every size, tiny, and editable.
6. Reject stock-photo filler. People shaking hands, smiling headset agents, laptops on a beach and abstract gradients prove nothing. If a stock image is the only option, the section is better with none. Record every rejected visual and the reason.
7. Write alt text for each image. Describe what it shows and why it matters in under about 125 characters, in plain language ("Dashboard showing 12 overdue invoices flagged in red"), not "image of dashboard". Purely decorative images get alt="" so screen readers skip them. Text inside an image must also appear in the HTML or the alt text.
8. Export for speed. Serve AVIF or WebP with a JPEG or PNG fallback via the picture element; SVG for diagrams, icons and logos. Produce 2 to 4 widths per raster image (for example 480, 960, 1440, 1920) and wire them with srcset and sizes. Keep hero images under about 200 KB and most others under about 100 KB at their largest served width.
9. Set width and height attributes on every img (the intrinsic size, so the browser reserves space and nothing shifts). Mark the hero image fetchpriority="high" and do not lazy-load it; add loading="lazy" and decoding="async" to images below the fold.
10. Put the files in pages/<page>/build/img/ with descriptive names (invoice-dashboard-960.avif, not IMG_2231.png), update build/index.html, and open the page in a browser at 360px and 1280px to confirm every image loads and reads.
11. Fill the visual list in pages/<page>/12-visuals.md: one row per visual with section, purpose, type, file, alt text and status. When finished run `lp done 12 --page <page>`, fix whatever it reports, then `lp next`.

## Output

- pages/<page>/12-visuals.md, from template 12-visuals.md. Run `lp start 12 --page <page>` to copy the template into place (it never overwrites).
- Image files in pages/<page>/build/img/ and an updated pages/<page>/build/index.html.

## Done when

- [ ] pages/<page>/12-visuals.md exists, every template heading is present, and no `{{...}}`, TODO or TBD remains
- [ ] Every visual in the table states what claim it proves or explains, its type, file path, alt text and status
- [ ] The hero visual shows the product or the outcome and stays readable with the CTA above the fold at 360px
- [ ] No stock-photo filler, and no generated image poses as a screenshot, customer, team member or result
- [ ] Every screenshot, photo and logo is real and listed in research/04-proof.md or assets/ with permission
- [ ] Raster images ship as AVIF or WebP with fallback, srcset and sizes, and explicit width and height
- [ ] Missing visuals are marked "need from owner" with a specific request, not filled with placeholders

## Common mistakes

- Full-screen product screenshots shrunk until nothing is legible. Crop to the one part that proves the claim.
- Decorative visuals that look nice but explain nothing, pushing the CTA below the fold on mobile.
- Alt text that repeats the file name or says "image", or keyword-stuffed alt text written for search engines.
- Lazy-loading the hero image, or forgetting width and height, which hurts LCP and causes layout shift.
- Mocked-up "customer" photos or generated logos used as social proof. That is invented proof.
- Carousels or sliders for screenshots or reviews. Most visitors never see past the first slide; stack them.

## Redesign mode notes

- Inventory the images already on the live page (from audit/pages/<slug>.md and the live site). Keep any that prove something, replace the filler.
- Keep the same image URLs where they rank in image search or are linked externally, or add them to audit/url-map.csv for redirects.
- Old screenshots of a UI that has since changed are a trust problem. Retake them.
