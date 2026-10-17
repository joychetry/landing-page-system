# Polish: home

## Responsive checks

| Width | Hero fully above the fold | Issues found | Fixed |
|---|---|---|---|
| 360px | yes | CTA wrapped to two lines | Shortened padding |
| 768px | yes | none | n/a |
| 1280px | yes | Photo too tall | Capped at 480 px |

## Motion

Only the CTA button lifts 1 px on hover over 200 ms. A prefers-reduced-motion rule removes the transition.

## Tap targets and forms

All buttons are 44 px tall or more; form inputs use tel and autocomplete, labels are visible, and required fields show an error message on submit.

## Layout shift

Every image has width and height, fonts are the system stack, and no banner loads after the page.

## Cohesion pass

Every section follows the hero pattern from brand/brand.md, spacing uses the token scale, and there is one primary CTA style.
