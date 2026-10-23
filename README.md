# landing-page-system

**A research-first method for landing pages that any coding agent can follow, with a tiny CLI that keeps it honest.**

Point Claude Code, Codex, Gemini CLI, Cursor, Pi, OpenCode or Aider at a product and it works through 16 steps: research the buyer and the market, write the page in the customer's own words, design it, ship it with SEO and analytics, then measure and improve. It stops at three points and waits for a human to approve the work.

Research is done once per product. Every page after the first starts at the writing step and reuses it. The same workflow also redesigns an existing site, starting from an audit of what is live and what already ranks.

```sh
lp init "Acme Plumbing"     # creates ./acme-plumbing/ right where you are
cd acme-plumbing
lp next                     # tells you (or your agent) exactly what to do next
```

- **Works in any agent.** Follows the open [Agent Skills](https://agentskills.io) format, and every workspace also gets an `AGENTS.md`, `CLAUDE.md` and `GEMINI.md`, so agents without skill support still know the method.
- **No dependencies.** The CLI is one Python 3.8+ file using only the standard library, with no network calls. Workspaces are plain Markdown, HTML, CSS and JSON.
- **Portable workspaces.** Each workspace carries its own copy of the CLI, guides and templates. Move it, commit it, open it on another machine: it still works, with or without the skill installed.
- **Human gates the CLI enforces.** It will not move past the wireframe, the final design or the deploy until a person records an approval.
- **No invented proof.** Testimonials, numbers, logos and quotes need a source. Missing proof is written down as a gap, never filled in.

---

## Contents

- [Why this exists](#why-this-exists)
- [The 16 steps](#the-16-steps)
- [Install](#install)
- [Three ways to start](#three-ways-to-start)
- [How an agent uses it](#how-an-agent-uses-it)
- [Human gates](#human-gates)
- [Honesty rules](#honesty-rules)
- [Workspace layout](#workspace-layout)
- [CLI reference](#cli-reference)
- [Copy and HTML checks](#copy-and-html-checks)
- [Configuration](#configuration)
- [Using it without Python](#using-it-without-python)
- [FAQ](#faq)
- [Development](#development)
- [License](#license)

---

## Why this exists

Ask an agent for a landing page and you usually get a nice-looking template with generic copy: "Unlock your potential", three feature cards, a stock testimonial. It looks finished and converts badly, because nobody asked who buys, what hurts them, what competitors already say, or what proof exists.

Good landing pages are built in a fixed order: research, then copy, then design. This project writes that order down as step guides an agent can follow, and adds a small CLI that tracks progress, checks each step's output before marking it done, and refuses to skip ahead. The agent does the thinking. The CLI does the bookkeeping agents are bad at.

## The 16 steps

| Phase | # | Step | Scope | Output |
|---|---|---|---|---|
| **Audit** | 0 | Audit the existing site | Redesigns only | `audit/site-audit.md`, `audit/url-map.csv` |
| **Research** | 1 | Goal and offer | Product, once | `research/01-goal-offer.md` |
| | 2 | Customer research | Product, once | `research/02-customers.md` |
| | 3 | Competitor research | Product, once | `research/03-competitors.md` |
| | 4 | Proof and assets | Product, once | `research/04-proof.md` |
| | 5 | Brand story | Product, once | `research/05-brand-story.md` |
| | 6 | SEO research | Product, once | `research/06-seo.md` |
| **Write** | 7 | Page structure | Per page | `pages/<page>/07-structure.md` |
| | 8 | Page copy | Per page | `pages/<page>/08-copy.md` |
| **Design** | 9 | Wireframe | Per page | `pages/<page>/09-wireframe.html` |
| | | **Gate 1: a human approves the wireframe** | | |
| | 10 | Brand guidelines | Product, first page only | `brand/brand.md`, `brand/tokens.css` |
| | 11 | Final design | Per page | `pages/<page>/build/index.html` |
| | | **Gate 2: a human approves the final design** | | |
| | 12 | Page visuals | Per page | `pages/<page>/12-visuals.md` |
| **Launch** | 13 | Polish | Per page | `pages/<page>/13-polish.md` |
| | 14 | Last checks | Per page | `pages/<page>/14-checks.md` |
| | | **Gate 3: a human approves shipping** | | |
| | 15 | Ship | Per page | `pages/<page>/15-ship.md` |
| | 16 | Measure and iterate | Per page, repeats | `pages/<page>/16-measure.md` |

Each step has a guide in [`references/steps/`](references/steps) that says what to read, what to do, what to write and when it counts as done. Five checklists in [`references/checklists/`](references/checklists) cover the hero section, on-page SEO, performance, accessibility and AI-sounding copy. The whole method is on one page in [`references/method-overview.md`](references/method-overview.md).

## Install

You need `git` and, for the CLI, Python 3.8 or newer.

```sh
git clone https://github.com/joychetry/landing-page-system.git
cd landing-page-system
./install.sh
```

With no options, `install.sh`:

1. Symlinks the skill into `~/.agents/skills/landing-page-system`, the shared folder several agents read.
2. Symlinks it into the skills folder of every agent it finds on the machine.
3. Links `bin/lp` into `~/.local/bin` if that folder is on your `PATH`, so `lp` works in any terminal.

It is safe to run again and never overwrites a real folder unless you pass `--force`. Because it uses symlinks, a `git pull` updates every agent at once.

| Agent | Command | Installs to |
|---|---|---|
| Shared (`~/.agents/skills`) | `./install.sh --agent agents` | `~/.agents/skills/landing-page-system` |
| Claude Code | `./install.sh --agent claude` | `~/.claude/skills/landing-page-system` |
| Codex | `./install.sh --agent codex` | `~/.codex/skills/landing-page-system` |
| Gemini CLI | `./install.sh --agent gemini` | `~/.gemini/skills/landing-page-system` |
| Cursor | `./install.sh --agent cursor` | `~/.cursor/skills/landing-page-system` |
| Pi | `./install.sh --agent pi` | `~/.pi/agent/skills/landing-page-system` |
| OpenCode | `./install.sh --agent opencode` | `~/.config/opencode/skills/landing-page-system` |
| All of the above | `./install.sh --agent all` | every folder above |

Other options: `--copy` (copy files instead of symlinking), `--bin-dir DIR` (where to put `lp`), `--force`, `--uninstall`.

**Agents without skill support** (Aider, editors with a chat panel) don't need an install. Run `lp init` once and the workspace's `AGENTS.md` explains the method. `python3 .lp/lp.py` runs the CLI from inside it.

## Three ways to start

### 1. A new product

```sh
cd ~/projects
lp init "Acme Plumbing"
cd acme-plumbing
```

The workspace is created in the folder you're in (or under `--dir PATH`), never in a hidden or global location. It starts at step 1, with a first page called `home`.

### 2. Another page for the same product

```sh
lp page add pricing --keyword "plumber prices harbor city"
lp next --page pricing
```

The new page starts at step 7. It reads the product research and inherits the brand guidelines from the first page. The CLI refuses a target keyword another page already owns, so your own pages don't compete in search.

### 3. Redesigning a live site

```sh
lp init "Acme Plumbing" --mode redesign --url https://acme.example.com
cd acme-plumbing
lp next
```

This starts at step 0, an audit of the live site. The agent saves the current copy, fills the research files with what the site already says (marked `source: live-site`), records every URL that must survive in `audit/url-map.csv`, and decides which pages to rebuild. Step 15 won't complete without a redirect map, so a redesign doesn't quietly lose its rankings.

## How an agent uses it

Tell your agent something like:

> Use the landing-page-system skill to build a landing page for my product. Run `lp next` and follow it.

The agent then repeats one loop:

```
lp next  ->  read the guide it names  ->  lp start N  ->  do the work  ->  lp done N
```

1. **`lp next --json`** returns the step, the page, the guide to read, the input files, the output files, the template and the done criteria.
2. The agent reads the guide and the inputs. It works from the guide, not from memory.
3. **`lp start N`** marks the step in progress and copies the template into place.
4. The agent does the research or writing and fills in the file.
5. **`lp done N`** validates the output. If the template is untouched, placeholders remain, a heading was removed, the `verified:` date is missing or a step-specific rule fails, it says exactly what and refuses. Once it passes, it points to the next step.

When `lp next` reaches a gate, it exits with code `3` and prints the approval command for a human. The agent shows you the work and stops.

Here is `lp next` in a fresh workspace:

```
Next: step 1, Goal and offer (product, todo)
Guide:      .lp/guide/steps/01-goal-offer.md
Write:      research/01-goal-offer.md
Template:   .lp/templates/01-goal-offer.md -> research/01-goal-offer.md
Done when:
  - Frontmatter has `verified: YYYY-MM-DD` with today's date or earlier, and no `{{...}}`, `TODO` or `TBD` remains.
  - Every `##` heading from the template is still present.
  - There is exactly one conversion action, and what happens after the click is written down.
  - The dream outcome is about the customer, not the product, and any number in it has a source.
  - The offer is dissected into at least 8 distinct facets, each with its customer meaning.
  ...
Run:        lp start 1, do the work, then lp done 1
```

## Human gates

Three points need a person to look at the work before it continues:

| Gate | After | You're approving |
|---|---|---|
| `gate1` | Step 9 | The wireframe: structure, copy and section order, before any visual polish |
| `gate2` | Step 11 | The final design |
| `gate3` | Step 14 | Shipping the page to production |

At each gate your agent shows you the work and asks you to choose **Approve** or **Request changes**. In Claude Code that's a clickable prompt; other agents ask in chat. When you approve, the agent records it for you with your name. You can also approve from a terminal:

```sh
lp approve gate1 --page home --by "Your Name" --note "Swap sections 3 and 4 first"
```

Until a gate is approved, the CLI won't start the next step, even with `--force`. Reopening an earlier step with `lp redo` revokes the gates that come after it.

> **Note:** the CLI can't tell a human from an agent. Gates are enforced by the tool plus the instructions in `SKILL.md` and `AGENTS.md`, which tell agents to run `lp approve` only after you choose Approve. Each approval records who approved and when, so you can check.

## Honesty rules

These are written into every guide and checked where possible:

- Every research claim carries a source: a URL, a file, or "provided by owner" with a date.
- Customer language is quoted exactly as found, with a link.
- No invented testimonials, ratings, user counts, logos or quotes. If proof doesn't exist yet, step 4 lists it as a gap and the page is written without it.
- Anything the agent wrote without a source is marked as such, so a human can confirm or replace it.
- Research files carry a `verified:` date. `lp stale` flags anything older than 90 days before a new page relies on it.

## Workspace layout

```
<folder>/<product-slug>/
  lp.json                manifest: steps, pages, keywords, gates, copy rules
  AGENTS.md              method instructions for any agent opening this folder
  CLAUDE.md GEMINI.md    the same entry point for those agents
  .lp/                   bundled CLI, guides, templates and version
  research/              steps 1-6, shared by every page
  brand/                 step 10: brand.md, tokens.css, assets/
  assets/                logos, screenshots and photos you provide
  audit/                 redesigns only: site-audit.md, pages/, url-map.csv
  pages/
    home/                07-structure.md ... 16-measure.md, 11-design/, build/
    pricing/             starts at step 7
```

Commands find the workspace by walking up from the current folder to `lp.json`, the way git finds `.git`. Override with `--dir PATH` or the `LP_WORKSPACE` environment variable.

A workspace is just files, so you can commit it to git, share it, or open it in a different agent later.

## CLI reference

Every command accepts `--json` (machine-readable output) and `--help`.

| Command | What it does |
|---|---|
| `lp init <product> [--mode new\|redesign] [--url URL] [--dir PATH] [--page home] [--no-agent-files] [--force]` | Create a workspace at `PATH/<slug>` (default: the current folder) with its own copy of the CLI, guides and templates. |
| `lp next [--page P] [--force]` | What to do next: step, guide, inputs, outputs, template, done criteria, gate status. `--force` skips unfinished research, never a gate. |
| `lp status [--page P]` | Table of every step by page, plus gates and stale research. |
| `lp start N [--page P]` | Mark a step in progress and copy its template. Never overwrites an existing file. |
| `lp done N [--page P] [--force]` | Validate the step's output and mark it done, or list what's missing. `--force` skips validation, never a gate. |
| `lp redo N [--page P]` | Reopen a step. For page steps, revokes the gates after it. |
| `lp approve gate1\|gate2\|gate3 --page P --by NAME [--note TEXT]` | Record a human approval (agents run it only after you choose Approve). |
| `lp page add <slug> [--keyword K] [--url URL]` | Add a page starting at step 7. Refuses a keyword another page owns. |
| `lp page list` | Pages, their keywords and their next step. |
| `lp check [--page P] [FILE...]` | Lint copy and HTML, and check keyword overlap across pages. |
| `lp stale` | List research older than `stale_days`. |
| `lp sync-guide` | Update the workspace's `.lp/` from the installed skill. Your files are untouched. |
| `lp doctor` | Check Python, the workspace, the manifest and version drift. |
| `lp --version` | Print the version. |

**Exit codes:** `0` OK. `1` validation failed, a check found errors, or research is stale. `2` usage error or no workspace found. `3` waiting on a human gate. `127` the `bin/lp` wrapper couldn't find `lp.py` or Python 3.8+.

**Running the CLI**, in order of preference: `lp` if it's on your `PATH`; `python3 <skill folder>/scripts/lp.py`; or, inside any workspace, `python3 .lp/lp.py`.

## Copy and HTML checks

`lp check` runs on Markdown copy and built HTML. `lp done 8` and `lp done 14` run it too and refuse to pass with errors.

- **Copy:** banned AI-sounding phrases, long-dash density, leftover placeholders, exclamation marks, the ratio of "we" to "you", headline length.
- **HTML:** exactly one `h1`, `title` and meta description length, canonical link, viewport, `lang`, image `alt` text, empty links, Open Graph tags, valid JSON-LD.
- **Across pages:** two pages targeting the same keyword.

Findings are `error` (blocks the step), `warn` (fix it or write down why not) or `info`.

## Configuration

Settings live in the workspace's `lp.json`:

| Key | Default | Meaning |
|---|---|---|
| `stale_days` | `90` | Age at which research counts as stale |
| `copy_rules.banned_phrases` | built-in list | Phrases `lp check` flags |
| `copy_rules.extra_banned` | `[]` | Your additions, such as words your brand never uses |
| `copy_rules.max_em_dashes_per_1000_words` | `2` | Long-dash limit |

## Using it without Python

Everything is plain files, so the method works without the CLI. Read the "Manual fallback" section of [`SKILL.md`](SKILL.md), follow [`references/method-overview.md`](references/method-overview.md) and the step guides, copy templates by hand from [`templates/`](templates), and update `lp.json` yourself. You lose validation and gate enforcement, not the method.

## FAQ

**Does it build the page for me?**
Your agent builds it by following the guides. Step 9 produces an HTML wireframe and step 11 the real page in `build/`. Step 15 covers deploying it wherever you host.

**Does it need internet access?**
The CLI never touches the network. Your agent needs web access for the research steps (customers, competitors, SEO) and for auditing a live site.

**What does it output?**
Plain HTML and CSS by default, since every host and site builder accepts it. Your agent can port the approved design to React, Astro, WordPress or anything else in step 11 or 15.

**Can I skip steps?**
`lp done N --force` skips validation and `lp next --force` skips unfinished research. Neither skips a gate. Skipping research is usually how pages end up generic.

**What if I already have research?**
Paste it into the research files with its sources and run `lp done` on each step. If it passes, you've saved the time.

**Can a team share a workspace?**
Yes. Commit it to a repo. Approvals record who approved and when.

## Development

```
SKILL.md              agent-facing instructions (Agent Skills format)
install.sh            installer for every supported agent
bin/lp                POSIX sh wrapper that finds lp.py from any install location
scripts/lp.py         the CLI, also bundled into every workspace
references/           method-overview.md, steps/00-16, checklists/
templates/            one template per step output, plus AGENTS.md.tmpl
tests/                test_lp.py, test_portability.sh, fixtures/
```

Run the tests:

```sh
python3 -m unittest discover -s tests -v    # CLI behaviour: validation, gates, pages, checks
bash tests/test_portability.sh              # installs and runs under each agent's folder layout
```

Contributions are welcome. Keep the CLI to the standard library and Python 3.8, keep the guides agent-neutral, and add a test for any new rule. Changes are recorded in [`CHANGELOG.md`](CHANGELOG.md).

## License

[MIT](LICENSE)
