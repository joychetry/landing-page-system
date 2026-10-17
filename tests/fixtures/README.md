# Test fixtures

Sample data for the test suite and the release walkthrough. "Tidewater Plumbing" is a fictional
business; every name, quote, number and URL here is made up for testing and uses reserved
example domains. Never copy this content into a real page.

- `sample/` mirrors a workspace: filled research (steps 1 to 6), a redesign audit (step 0), brand
  files (step 10) and every output of the `home` page (steps 7 to 16). Its HTML and copy pass
  `lp check` with zero errors. Tests copy it into a fresh workspace and set `verified:` to today.
- `bad/` holds samples that break every `lp check` rule, one or more times each.
