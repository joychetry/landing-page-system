# Step 13: Polish

Turn the built page into one cohesive, quietly animated page that works on every screen, from a small phone to a wide desktop.

## Scope

Per page. Runs once for each page, after step 12. Works on pages/<page>/build/ only; the brand tokens stay product-level.

## Inputs

- pages/<page>/build/index.html (plus its css/ and img/)
- brand/tokens.css (colors, type scale, spacing, radii, motion durations)
- brand/brand.md (the hero pattern and rules every section follows)
- references/checklists/performance.md
- references/checklists/accessibility.md

## Do this

1. Confirm the basics before polishing: `<meta name="viewport" content="width=device-width, initial-scale=1">` in the head, `<html lang="...">` set, and all colors, fonts and spacing coming from brand/tokens.css rather than one-off values.
2. Test at three widths: 360px (small Android), 768px (tablet portrait) and 1280px (laptop). Open the page in a browser and resize, or use device emulation. If your agent has a browser automation tool, take a screenshot at each width and look at it. For each width record: is the full hero (headline, subhead, two proof items, CTA, FUD reducer, visual) visible without scrolling, and what broke.
3. Fix what breaks, mobile first: no horizontal scroll at 360px, no text under 16px for body copy, line length around 45 to 75 characters on desktop, headlines that wrap cleanly (no single orphaned word), images that scale, tables and pricing grids that stack. On mobile the hero stacks; trim or tighten until it still fits above the fold.
4. Add motion only where it helps the visitor understand: a subtle fade or rise as sections enter, a hover and press state on buttons, a diagram that draws its steps in order. Keep durations about 150 to 400 ms with ease-out curves, animate only transform and opacity, and never delay or hide the hero headline or CTA behind an animation.
5. Respect reduced motion. Wrap or override every animation and transition with `@media (prefers-reduced-motion: reduce)` so they are removed or reduced to an instant change. Content must be fully visible without JavaScript and without animation. `lp done 13` checks that this rule exists if the page animates. A minimal safety net:

   ```css
   @media (prefers-reduced-motion: reduce) {
     *, *::before, *::after {
       animation-duration: 0.01ms !important;
       animation-iteration-count: 1 !important;
       transition-duration: 0.01ms !important;
       scroll-behavior: auto !important;
     }
   }
   ```

6. Check tap targets and forms. Every button, link and input is at least 44 by 44 px with at least 8px between neighbors. Inputs use the right type (email, tel, number), autocomplete attributes, visible labels (not placeholder-only), clear focus styles, and inline error messages next to the field. The form submits with the keyboard alone.
7. Remove layout shift. Every img, video and iframe has width and height (or aspect-ratio). Web fonts use font-display: swap with a metric-matched fallback (size-adjust or a close system font), and the main font file is preloaded. Nothing (cookie banners, chat widgets, late-loading embeds) pushes content down after load; reserve its space or overlay it.
8. Run an accessibility pass from references/checklists/accessibility.md: color contrast at least 4.5:1 for body text and 3:1 for large text, heading levels in order, visible keyboard focus, a skip link if there is navigation, and nothing conveyed by color alone.
9. Run a cohesion pass against brand/brand.md. Scroll the whole page at desktop and mobile and ask: does every section follow the hero pattern, is the spacing rhythm consistent, is there exactly one primary button style for the main CTA, do icons share one style, do photos share one treatment? Fix outliers; one odd section makes the whole page look assembled.
10. Run a quick speed sanity check from references/checklists/performance.md: no unused CSS frameworks, no render-blocking scripts in the head, third-party scripts deferred. Full measurement happens in step 15.
11. Record what you checked and fixed in pages/<page>/13-polish.md. When finished run `lp done 13 --page <page>`, fix whatever it reports, then `lp next`.

## Output

- pages/<page>/13-polish.md, from template 13-polish.md. Run `lp start 13 --page <page>` to copy the template into place (it never overwrites).
- An updated pages/<page>/build/ (index.html, CSS, images).

## Done when

- [ ] pages/<page>/13-polish.md exists, every template heading is present, and no `{{...}}`, TODO or TBD remains
- [ ] build/index.html has a viewport meta tag, and any CSS animation or transition has a prefers-reduced-motion rule
- [ ] The page was tested at 360, 768 and 1280 px with no horizontal scroll, and the full hero sits above the fold on mobile
- [ ] Every tap target is at least 44 by 44 px and the form works by keyboard with visible labels and errors
- [ ] Every image, video and embed has reserved space, fonts use font-display swap, and nothing shifts after load
- [ ] Motion uses only transform and opacity and never hides the headline or CTA
- [ ] A cohesion pass against brand/brand.md is recorded, with one primary CTA style across the page

## Common mistakes

- Testing only in a resized desktop browser at 1280px and calling it responsive. Check 360px first.
- Scroll-triggered reveals that leave content invisible if JavaScript fails or the visitor prefers reduced motion.
- Animating width, height, top or margin, which janks on mid-range phones and causes layout shift.
- Sticky headers and chat widgets that cover the CTA or the form on small screens.
- Several button styles competing for attention, so no single action looks primary.
- Tiny inline text links as the only CTA on mobile.

## Redesign mode notes

- Compare the new build against the old page (audit/pages/<slug>.md and the live site) at the same three widths. Anything the old page did better on mobile, match it.
- Keep visible elements that returning customers rely on (login link, phone number, support link) in the same places where possible.
