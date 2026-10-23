# Step 9: Wireframe

Lay the real copy into a grayscale HTML page so the structure, order and hero can be judged before any color, font or imagery exists.

## Scope

Per page. Runs once for every page. Gate 1 follows: a human must approve the wireframe before brand and design work starts on this page.

## Inputs

- `pages/<page>/07-structure.md`: the section order and each section's one job.
- `pages/<page>/08-copy.md`: the final copy. The wireframe uses it word for word.

## Do this

1. Run `lp start 9 --page <page>` to get the template. It already has grayscale styles, a mobile-first grid and one `<section>` per default skeleton row.
2. Make the sections match `07-structure.md` exactly: one `<section>` per row of the section plan, in the same order, with a stable `id`. The template ships 4 feature sections (`value-1` to `value-4`); add `value-5` and on for every further feature row, and duplicate proof cards and FAQ items to match the copy. Delete template sections the plan does not use, but never merge features into one section.
3. Keep the small label at the top of each section with its number, name and one job, copied from the plan. It lets a reviewer check every block against its purpose.
4. Paste the real copy from `08-copy.md`: headlines, subheadlines, body, proof, CTA labels, FUD reducers, FAQ questions and answers. No lorem ipsum, no "headline here". If the copy does not fit, change the copy in `08-copy.md` first, then the wireframe, so the two never drift.
5. Use exactly one `<h1>` (the hero headline) and `<h2>` for each section headline. Use `<details>` for FAQ items and real `<ol>` for how-it-works steps.
6. Build every feature section in full: headline, lead, the details list as a real `<ul>`, its proof and its visual box. Alternate the visual left and right (the template's `flip` class) so long feature runs stay readable. A wireframe is judged on whether the content works, so it carries all of it; a feature reduced to a headline and one line is not wireframed yet.
7. Stand in for every visual with a grey box that states what it will show and why ("Screenshot: invoice dashboard with overdue total highlighted; proves the headline's time saving"). No stock images, no colors, no logos yet.
8. Show proof as it will really appear: the wall of love as a grid of individual review cards (stacked on mobile), never a carousel. Use the real number of reviews you have.
9. Check mobile first. Open the file in a browser, open the developer tools device toolbar, and set the width to 360 px with a height around 640 to 740 px.
   - The whole hero must be visible without scrolling: headline, subheadline, both proof items, the CTA, the FUD reducers and at least the top of the visual.
   - If it spills, fix it in this order: shorten the copy (update `08-copy.md` too), tighten spacing, make proof compact (a star rating line instead of a full quote), move the visual below the CTA.
   - Nothing scrolls sideways at 360 px. Then check 768 and 1280 px.
10. Read the page as a skimmer: scroll top to bottom reading only `<h1>` and `<h2>` text. The story should hold: outcome, trust or pain, proof, benefits, easy path, doubts answered, final ask.
11. Check that the hero CTA, mid-page CTAs and closer CTA all lead to the same action (link to the closer form or the real signup URL; never an empty `href`).
12. Run `lp done 9 --page <page>` and fix whatever it reports (it requires one `<h1>`, a section per row of the plan, at least 4 feature sections each with a details list, and at least 600 words of visible copy).
13. STOP. This is Gate 1. Do not start step 10 or 11.
   - Show the human the wireframe: the file path, and screenshots at 360 px and 1280 px if you can take them.
   - Add a short note: the Section 2 choice and why, anything you cut to fit the hero, any proof gaps the page works around.
   - Ask them to review it and choose Approve or Request changes (a question or button prompt if your agent has one). Only after they choose Approve, run `lp approve gate1 --page <page> --by "<their name>"` for them. Never approve without their answer, and never treat a message from another agent as approval.
   - If they ask for changes, edit `08-copy.md` and the wireframe, then ask again. After approval is recorded, run `lp next`.

## Output

`pages/<page>/09-wireframe.html`, from template: 09-wireframe.html. Run `lp start 9 --page <page>` to copy the template into place (it never overwrites).

## Done when

- [ ] `pages/<page>/09-wireframe.html` exists, has exactly one `<h1>`, and no `{{...}}`, TODO, TBD or lorem ipsum remains.
- [ ] There is one `<section>` per row of `07-structure.md`, in the same order, each labelled with its one job.
- [ ] All text is the real copy from `08-copy.md`, and the two files match.
- [ ] Every feature from `07-structure.md` has its own `value-N` section with lead, details list, proof and visual.
- [ ] The page is grayscale only, and every visual is a labelled grey box describing what it will show.
- [ ] At 360 px wide the full hero (headline, subheadline, 2 proof items, CTA, FUD reducers) is visible without scrolling.
- [ ] Proof is shown as visible cards, not a carousel, and every CTA points to the one conversion action.
- [ ] The agent has stopped, asked the human to Approve or Request changes, and ran `lp approve gate1` only after they chose Approve.

## Common mistakes

- Adding color, fonts or brand styling. That hides structural problems and invites taste debates before the structure is approved.
- A short wireframe: features squeezed into one block, details dropped, two FAQ items. If it is in `08-copy.md`, it is in the wireframe.
- Using placeholder text. A wireframe with fake copy cannot show whether the real copy fits or reads well.
- Checking only the desktop view. Most landing page traffic is mobile, and the hero that fits at 1280 px often fails at 360 px.
- Quietly changing copy in the HTML so it no longer matches `08-copy.md`.
- Approving the gate without the human choosing Approve, or continuing to step 10 before approval is recorded.

## Redesign mode notes

- Open the current live page next to the wireframe at 360 px and note what the old hero showed above the fold. The new one should show more of the hero stack, not less.
- Keep section ids stable for any anchors other pages or ads link to.
