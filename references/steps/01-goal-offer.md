# Step 1: Goal and offer

Fix the one action the page exists to get, the outcome the customer is really buying, every piece of
the offer that delivers it, and the temperature of the traffic that will arrive.

## Scope

Product-level, runs once. Every page for this product reuses this file. Copy comes first and design
second, and this step is where the copy starts: nothing visual is decided here.

## Inputs

- A conversation with the owner (live, by call, or a written questionnaire).
- Analytics and ads accounts, if available: traffic sources, landing pages, current conversion rate.
- Redesign mode: `audit/site-audit.md` and any research files already pre-filled with
  `source: live-site` evidence.

## Do this

1. Run `lp start 1` to copy the template to `research/01-goal-offer.md`. Set the frontmatter
   `verified:` to today's date in `YYYY-MM-DD` form.
2. Interview the owner. Ask, and write down the answers with "provided by owner, YYYY-MM-DD": What
   should a visitor do on this page? What happens after they do it? Who is the best customer you
   have, and why did they buy? What do you sell, at what price, with what terms? What guarantee or
   trial really exists? Where does traffic come from today and where will it come from after launch?
   What is the current conversion rate? Ask for exact words, not polished summaries.
3. Pick the one conversion action. One page, one primary action: book a call, start a trial, buy,
   request a quote, join a waitlist. Secondary links (phone number, login) may exist, but they never
   compete visually with the primary CTA. Write why this action and not another, and exactly what
   happens after the click. If the owner wants two actions for two audiences, that is two pages;
   note it under open questions.
4. Write the dream outcome: the end result the customer wants, about them and not the product.
   Nobody wants software; they want hours back or more revenue. Use three parts: the end result
   (quantified only where a number can be proven), the time to first result (only if true and
   provable, otherwise "not applicable"), and the emotional payoff (how they feel once they have
   it). This becomes the hero headline later, so it must make sense to a stranger in five seconds.
5. Describe the offer exactly: name, price and terms, what is included, and risk reversal. Only list
   a guarantee, trial or cancellation term the owner has confirmed; if there is none, write "none".
   Never suggest the page will "add a guarantee" unless the owner commits to it.
6. Dissect the offer into facets: every unique piece that helps deliver the dream outcome. Aim for 8
   or more. Cover different angles using the template's types: feature, proof, risk reversal, effort
   (how little the customer must do), speed, support, bonus, price. For each facet write what it
   means for the customer in one line (the benefit behind the feature). Two facets that say the same
   thing in different words count as one. These facets become the value props, the subheadline and
   the FAQ answers in step 8, so the longer and sharper this list, the easier the copy.
7. Classify every traffic source by temperature. Cold: people who were not looking for this (social
   feed ads, display, cold outreach, most video). Warm: people aware of the problem or the brand
   (organic search for the problem, newsletter, retargeting, referrals, partner links). Hot: people
   looking for exactly this, now (branded search, high-intent search ads such as "<service> near
   me", returning visitors from a pricing email). Record share of visits with its source; if there
   is no data, write "unknown, no data yet".
8. Name the primary traffic temperature for the first page: the source that will send the most
   visits or the paid source the owner will spend on.
9. Rate offer complexity: simple (a stranger understands it in one sentence and knows they need it)
   or complex (software, B2B, a new category, anything that needs explaining or where the buyer does
   not yet know they have the problem).
10. Apply the section 2 rule and write the result. Warm or hot traffic with a simple offer: social
    proof comes right after the hero, because these visitors already want the thing and mostly need
    to trust you. Cold traffic or a complex offer: the pain point comes right after the hero,
    because these visitors do not yet know why they need it. Either cold traffic or complexity
    pushes to pain point first. If two big sources have different temperatures, build for the main
    one now and plan a second page for the other later with `lp page add`.
11. Set the success metric: baseline conversion rate with its source (or "unknown, no data yet"), a
    target, and how it is measured (tool and event name for the primary CTA).
12. List open questions for the owner: anything you assumed, any number without a source, any proof
    you will need in step 4.
13. When finished, run `lp done 1`, fix whatever it reports, then run `lp next`.

## Output

`research/01-goal-offer.md` (template: 01-goal-offer.md). Run `lp start 1` to copy the template into
place (it never overwrites).

## Done when

- [ ] Frontmatter has `verified: YYYY-MM-DD` with today's date or earlier, and no `{{...}}`, `TODO` or `TBD` remains.
- [ ] Every `##` heading from the template is still present.
- [ ] There is exactly one conversion action, and what happens after the click is written down.
- [ ] The dream outcome is about the customer, not the product, and any number in it has a source.
- [ ] The offer is dissected into at least 8 distinct facets, each with its customer meaning.
- [ ] Every traffic source has a temperature, and the section 2 rule result follows from the temperature and complexity recorded.
- [ ] Every fact the owner gave is marked "provided by owner, YYYY-MM-DD"; guarantees listed are only ones the owner confirmed.

## Common mistakes

- Two or three goals on one page ("book a call, or download the guide, or follow us"). Each extra
  CTA splits attention; choose one.
- A dream outcome that describes the product ("an AI-powered scheduling platform") instead of the
  result ("a full calendar without chasing anyone").
- Facets that are all features. Push for proof, effort, speed, risk reversal and support facets too.
- Inventing a money-back guarantee or a "results in 7 days" claim because it would convert better.
  If it is not real, it is not on the list.
- Guessing traffic temperature from the industry instead of from where the visits will actually come
  from.

## Redesign mode notes

Start from the evidence in `audit/site-audit.md`: the current primary CTA, the offer and price shown
today, and the top landing pages and queries. Confirm each with the owner before keeping it; the
live site may be out of date. If the old site pushed several CTAs, note which one actually produced
leads or sales (ask the owner or check analytics) and choose that one unless the owner decides
otherwise. Keep `source: live-site` markers on facts taken from the old site.
