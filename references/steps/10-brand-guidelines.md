# Step 10: Brand guidelines

Set the colors, type, spacing and hero pattern every page of the product follows, as a written guide plus CSS tokens.

## Scope

Product-level. Done once, together with the first page (usually `home`), after that page passes Gate 1. Every later page inherits it: `lp` shows step 10 as "inherited" for them, and their designs use the same `brand/tokens.css`. Reopen it with `lp redo 10` only when the brand itself changes, and then check every built page.

## Inputs

- `research/05-brand-story.md`: voice, one-liner, how the customer should feel.
- `pages/<page>/08-copy.md`: the approved copy of the first page; the system must serve its headline lengths, proof types and CTA.
- `assets/`: owner-supplied logos, brand files, fonts, photos, screenshots.
- Redesign mode: `audit/site-audit.md` and the live site.

## Do this

1. Inventory real assets. List every file in `assets/` in the Source assets table with its origin. You need at minimum a logo file (SVG preferred, else a high-resolution PNG). If there is no logo and no brand, ask the owner. If they have none, set the logo as the product name in the heading font and say so in `brand/brand.md`. Never generate, draw or download a stand-in logo, and never use placeholder images.
2. Redesign mode or an existing brand: extract before you invent. Open the live site in a browser and open the developer tools.
   - Inspect the body text, H1, H2, primary button, links and page background. Read the computed styles: color, background-color, font-family, font-weight, font-size, line-height, border-radius.
   - Note the exact hex values and the font names actually loaded (check the network panel for font files).
   - Save the logo in its original format (SVG from the page source if available) to `brand/assets/`, plus the favicon.
   - Copy two or three typical sentences to capture the current voice.
   - Mark each of these as extracted from the live site.
3. Color. Define the roles in the template: background, surface, text, muted text, primary (reserved for the primary CTA and nothing else that competes with it), primary text, accent, border. Keep the palette small: one primary, one accent, neutrals. Pick a primary that stands out against the background and against the hero visual.
4. Check contrast for every text and background pair you will use, with a contrast checker (search the web for "WCAG contrast checker", or use the color picker in the browser developer tools):
   - Body text and muted text against the background and the surface color: at least 4.5:1.
   - CTA label against the primary color: at least 4.5:1.
   - Large text (24 px, or 19 px bold), button edges and focus rings: at least 3:1.
   - Record each ratio in the Color table. Adjust the hex value until it passes; never record a ratio you did not measure.
5. Typography. At most two families (one is fine). Choose for legibility at 16 px on a phone. Prefer the system stack or a self-hosted woff2 with `font-display: swap` and only the weights you use. Set H1, H2, body and small sizes for mobile and desktop; make sure the hero headline from `08-copy.md` fits in 2 to 4 lines at 360 px.
   Before writing any tokens, ask the human to choose the look (a question or button prompt if your agent has one, such as `AskUserQuestion` in Claude Code, otherwise plain text): offer 2 options, each a palette (hex values for primary, accent, background, text with their measured contrast ratios) and a type pair, plus a one-line mood. Show swatches or a small HTML sample if you can. Redesign mode or an existing brand: skip the choice and ask them to confirm the extracted values instead.
6. Spacing and layout: a spacing scale (the token steps), max content width, section padding for mobile and desktop, grid columns, radius.
7. Hero pattern: write the layout rule the hero sets and every section echoes: where headlines sit, which side visuals go on, how proof cards look, how the CTA is styled. This keeps the page coherent when the design grows.
8. Components: primary and secondary buttons, proof card, review wall, FAQ item, form field. Define hover, focus (a visible focus ring) and disabled states, and a minimum tap target of 44 by 44 px.
9. Imagery and motion: what real visuals look like (product screenshots, real team, real before and after), what is banned (stock filler, fake dashboards, AI faces), animation durations and easing, and the reduced-motion fallback.
10. Voice: summarize from `research/05-brand-story.md` in 3 to 5 do and do not pairs with example lines from the approved copy.
11. Write `brand/tokens.css` so every value matches `brand/brand.md` exactly. Keep the variable names from the template; later steps and every page depend on them.
12. If your agent has a design skill or tool for brand systems, color or typography, use it for steps 3 to 9 and record its output here; otherwise follow these steps as written.
13. When finished run `lp done 10 [--page <page>]`, fix whatever it reports, then `lp next`.

## Output

`brand/brand.md` (template: 10-brand.md) and `brand/tokens.css` (template: 10-tokens.css). Logo and other brand files go in `brand/assets/`. Run `lp start 10 [--page <page>]` to copy both templates into place (it never overwrites).

## Done when

- [ ] `brand/brand.md` and `brand/tokens.css` exist, every `## ` heading from the template is present, and no `{{...}}`, TODO or TBD remains.
- [ ] Every asset listed is a real file in `assets/` or `brand/assets/` with its origin; there is no placeholder or invented logo.
- [ ] Every text and background pair in the Color table shows a measured contrast ratio of at least 4.5:1 (3:1 for large text and UI edges).
- [ ] Every hex value, font and size in `brand/brand.md` matches the token in `brand/tokens.css`.
- [ ] The primary color is reserved for the primary CTA.
- [ ] The hero headline from `08-copy.md` fits in 4 lines or fewer at 360 px with the chosen H1 size.
- [ ] In redesign mode, colors, fonts, logo and voice were extracted from the live site before any change was proposed.

## Common mistakes

- Inventing a new palette or logo when the business already has a brand.
- Using the primary color for links, icons and headings too, so the CTA no longer stands out.
- Light grey body text that fails contrast.
- Loading four font weights from a third-party server, which slows the hero.
- Writing brand rules in `brand.md` that the CSS tokens do not implement.
- Redoing the brand for each new page instead of inheriting it.

## Redesign mode notes

- Treat the live brand as the default. Change a color or font only to fix a contrast, legibility or performance problem, and record why in the Do and do not table.
- Read colors from computed styles, not from screenshots: image compression shifts hex values.
- Mark extracted facts as `source: live-site` in the Source assets table.
