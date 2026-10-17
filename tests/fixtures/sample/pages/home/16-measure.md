# Measure and iterate: home

## Baseline

| Metric | Value | Period | Source |
|---|---|---|---|
| Visitors | 2,410 | 2026-10-12 to 2026-11-09 | analytics |
| Conversion rate | 4.2 percent | same period | analytics, booking_submitted |
| Primary CTA click rate | 9.8 percent | same period | analytics, cta_click |

## Funnel

| Stage | Visitors | Drop-off | Notes |
|---|---|---|---|
| Landed | 2,410 | n/a | 81 percent mobile |
| Scrolled past hero | 1,520 | 37 percent | normal for hot traffic |
| Clicked primary CTA | 236 | 84 percent | |
| Converted | 101 | 57 percent | form step loses most |

## Reviews

| Review | Date | What we saw | Decision |
|---|---|---|---|
| 14-day | 2026-10-26 | Form abandonment on the address field | Test fewer fields |
| 30-day | 2026-11-11 | Conversion up from 3.1 to 4.2 percent | Keep, run the form test |

## Hypothesis backlog

| # | If we change | Then | Because (evidence) | Impact 1-10 | Confidence 1-10 | Ease 1-10 | ICE |
|---|---|---|---|---|---|---|---|
| 1 | Ask for postcode instead of full address | More bookings complete | 57 percent drop on the form | 7 | 6 | 9 | 7.3 |

## Current test

Postcode instead of address; primary metric booking_submitted rate; 1,200 visitors per variant; started 2026-11-12; stop after 4 full weeks.

## Results log

| Test | Dates | Result | Confidence | Shipped |
|---|---|---|---|---|
| Launch versus old page | 2026-10-12 to 2026-11-09 | 3.1 to 4.2 percent | before and after, not a split test | yes |
