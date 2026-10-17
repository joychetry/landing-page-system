# Checklist: performance

Used in step 13 (polish), step 14 (last checks) and step 15 (ship). Measure on the deployed or locally served page, not from memory. If your agent has a tool for Lighthouse or PageSpeed Insights, use it; otherwise open the page in a browser with developer tools, or search the web for PageSpeed Insights and test the public URL.

## Core Web Vitals targets

- [ ] Largest Contentful Paint (LCP) is under 2.5 seconds.
- [ ] Cumulative Layout Shift (CLS) is under 0.1.
- [ ] Interaction to Next Paint (INP) is under 200 milliseconds.
- [ ] Targets are judged at the 75th percentile of real visits once field data exists; before launch, lab tests on throttled mobile meet them.
- [ ] The tested results and the date are recorded in pages/<page>/13-polish.md or 15-ship.md.

## Hero and LCP element

- [ ] You know which element is the LCP element (usually the hero image or the headline) and have checked it in the performance report.
- [ ] The hero image is preloaded or has `fetchpriority="high"`, and is not lazy-loaded.
- [ ] The hero image is in the initial HTML, not injected by JavaScript or set as a CSS background that loads late.
- [ ] The hero text renders without waiting for a web font or a script.

## Images

- [ ] Photos are served as AVIF or WebP, with a JPEG or PNG fallback only where needed.
- [ ] Responsive images use `srcset` and `sizes`, so a 360px phone does not download a 2400px file.
- [ ] Every image has `width` and `height` attributes (or a CSS aspect-ratio) so space is reserved before it loads.
- [ ] Images below the fold use `loading="lazy"`; images above the fold do not.
- [ ] No image is larger than about twice its largest displayed size.
- [ ] Icons and simple diagrams are SVG, not raster images.

## Fonts

- [ ] No more than two font families and four font files load on first view.
- [ ] Fonts are WOFF2, subset to the characters and languages the page uses.
- [ ] `font-display: swap` (or optional) is set, so text is visible while fonts load.
- [ ] The main text font is preloaded if it is self-hosted and used above the fold.
- [ ] Fallback font metrics are close enough that the swap causes no visible layout shift.

## CSS and JavaScript

- [ ] Critical CSS for the hero is inlined or loads in one small render-blocking file; the rest does not block rendering.
- [ ] Unused CSS from frameworks has been removed.
- [ ] Scripts use `defer` or `async`, or load at the end of the body; none block the first render.
- [ ] The page works and the CTA can be clicked before non-essential scripts finish loading.
- [ ] No long tasks over 200 milliseconds run during load or on CTA click (check the performance panel).
- [ ] Animations use transform and opacity, not properties that trigger layout.

## Third-party scripts

- [ ] Every third-party script (analytics, chat, heatmaps, tag managers, embeds) is listed with its purpose.
- [ ] Third-party scripts stay within a budget: at most about 3 vendors and 100 KB compressed in total, or a written reason to exceed it.
- [ ] Chat widgets, video embeds and maps load on interaction or after the page is idle, using a lightweight placeholder.
- [ ] Removing any single third-party script does not break the page.

## Weight budget

- [ ] Total page weight on first load is under about 1.5 MB on mobile, and under 1 MB where the design allows.
- [ ] JavaScript is under about 150 KB compressed.
- [ ] CSS is under about 75 KB compressed.
- [ ] The number of requests on first load is under about 50.

## Delivery

- [ ] Text assets (HTML, CSS, JS, SVG) are served compressed with Brotli or gzip.
- [ ] Static assets have long cache lifetimes with versioned file names; HTML is cached briefly or revalidated.
- [ ] The site is served over HTTPS with HTTP/2 or HTTP/3.
- [ ] A CDN serves static files if the audience is spread across regions.
- [ ] Server response time (TTFB) is under about 800 milliseconds.

## Testing conditions

- [ ] Tested with mobile emulation and network throttling (slow 4G or similar) and CPU slowdown, not only on a fast desktop.
- [ ] Tested with an empty cache.
- [ ] Re-tested after the final deploy at the real URL, not only on a local copy.
- [ ] Layout shift checked by scrolling the full page at 360px with throttling on: nothing jumps.
