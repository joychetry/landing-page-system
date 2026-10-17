# Checklist: accessibility (WCAG 2.2 AA basics)

Used in step 13 (polish) and step 14 (last checks). Test with a keyboard, a browser zoom, a narrow window and, if your agent has an accessibility checker such as axe or Lighthouse, run it too. Automated tools catch only part of the problems, so do the manual items as well.

## Color and contrast

- [ ] Body text has a contrast ratio of at least 4.5:1 against its background.
- [ ] Large text (24px and up, or 18.66px and up when bold) has at least 3:1.
- [ ] Buttons, form field borders, icons that carry meaning and focus indicators have at least 3:1 against what is next to them.
- [ ] Text over images or video stays at these ratios across the whole image (use an overlay if needed).
- [ ] Color is never the only way information is shown (errors, required fields, links in body text, chart series).

## Keyboard and focus

- [ ] Every link, button, form field and interactive widget can be reached and used with Tab, Shift+Tab, Enter and Space.
- [ ] Tab order follows the visual reading order.
- [ ] Focus is always visible with a clear outline; `outline: none` is never used without a visible replacement.
- [ ] The focused element is never hidden behind a sticky header, cookie banner or chat widget.
- [ ] There is no keyboard trap: focus can always move out of menus, modals and embeds.
- [ ] Modals and mobile menus move focus inside when opened, close with Escape, and return focus to the trigger.
- [ ] FAQ drop-downs are real buttons (or details and summary elements) that expose their open or closed state.

## Structure

- [ ] A "Skip to main content" link is the first focusable element and becomes visible on focus.
- [ ] Landmarks are used: one `header`, one `nav` per navigation, one `main`, one `footer`.
- [ ] There is exactly one H1, and headings go in order without skipping levels.
- [ ] Lists are marked up as lists, and buttons as `button`, not clickable `div` elements.
- [ ] `<html lang="...">` matches the page language, and passages in another language have their own lang attribute.
- [ ] The page title describes the page.

## Forms

- [ ] Every field has a visible label tied to it with `for` and `id` (placeholder text is not a label).
- [ ] Required fields are marked in text, not only by color or an asterisk without explanation.
- [ ] Fields use the right input type and `autocomplete` value (email, tel, name).
- [ ] Error messages appear in text next to the field, say what is wrong and how to fix it, and are announced to screen readers.
- [ ] Entered data is kept when the form shows an error.
- [ ] The submit button label says what happens ("Get my quote").

## Images and media

- [ ] Informative images have alt text that gives the same information the image does.
- [ ] Decorative images have alt="" so screen readers skip them.
- [ ] Alt text does not start with "image of" or repeat the caption or nearby text word for word.
- [ ] Screenshots and charts that carry data have the key point in alt text or in nearby text.
- [ ] Nothing plays sound automatically.
- [ ] Videos with speech have captions; audio-only content has a transcript.
- [ ] Any motion that runs longer than 5 seconds (carousels, looping video, tickers) has a pause control.

## Motion

- [ ] A `prefers-reduced-motion: reduce` rule turns off or reduces non-essential animation, parallax and auto-scrolling.
- [ ] Nothing flashes more than three times per second.
- [ ] Content is fully visible even if scroll-triggered animations never run.

## Touch and pointer

- [ ] Tap targets are at least 44 by 44 CSS pixels for primary actions, and never smaller than 24 by 24 (the WCAG 2.2 minimum) for anything else.
- [ ] Small adjacent targets (footer links, inline icons) have enough spacing that a thumb does not hit the wrong one.
- [ ] Nothing requires hovering, dragging or a multi-finger gesture without a simple tap alternative.

## Links

- [ ] Link text makes sense out of context ("Read the pricing details", not "click here" or "learn more" alone).
- [ ] Links that open a new tab or download a file say so.
- [ ] Links in body text are distinguishable without color alone (underline or another visual cue).

## Zoom and reflow

- [ ] At 200% browser zoom, all text is readable and no content or function is lost.
- [ ] At 320 CSS pixels wide, content reflows into one column with no horizontal scrolling (except for data tables and maps).
- [ ] Text spacing can be increased (line height 1.5, paragraph spacing 2x font size) without text being cut off.
- [ ] Nothing is locked to portrait or landscape orientation.
- [ ] The viewport meta tag does not disable zoom (no `user-scalable=no` or `maximum-scale=1`).
