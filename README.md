# landing-page-system

A portable skill and CLI that walks any coding agent (Claude Code, Codex, Gemini CLI, Pi,
OpenCode, Cursor, Aider and others), or a human in a terminal, through a 16-step method for
landing pages: research the product, write the copy in the customer's words, design, ship with
SEO and analytics, then measure and iterate. It also handles extra pages for the same product
and redesigns of existing sites.

- **One method, every time.** Research once per product (goal and offer, customers, competitors,
  proof, brand story, SEO), then per page: structure, copy, wireframe, brand, design, visuals,
  polish, checks, ship, measure. Copy first, design second.
- **Human gates.** The CLI refuses to move past the wireframe, the final design or the deploy
  until a person records an approval. Agents are told never to approve for themselves.
- **Honest by default.** No invented testimonials, numbers or logos. Missing proof is a listed
  gap. Every research claim carries a source.
- **No lock-in.** Follows the [Agent Skills](https://agentskills.io) format. The CLI is one Python
  3.8+ file using only the standard library, no network. Workspaces are plain Markdown, HTML and
  JSON, and carry their own copy of the CLI and guides, so they work on any machine.

## Install

```sh
git clone <this repo> landing-page-system
cd landing-page-system
./install.sh
```

By default `install.sh` symlinks the skill into `~/.agents/skills/landing-page-system` and into
the skills folder of every agent whose home folder exists on the machine, then links `bin/lp`
into `~/.local/bin` if that is on your PATH. It is idempotent and never replaces a real folder
without `--force`.

| Agent | Command | Skill folder |
|---|---|---|
| Any agent reading `~/.agents/skills` | `./install.sh --agent agents` | `~/.agents/skills/landing-page-system` |
| Claude Code | `./install.sh --agent claude` | `~/.claude/skills/landing-page-system` |
| Codex | `./install.sh --agent codex` | `~/.codex/skills/landing-page-system` |
| Pi | `./install.sh --agent pi` | `~/.pi/agent/skills/landing-page-system` |
| OpenCode | `./install.sh --agent opencode` | `~/.config/opencode/skills/landing-page-system` |
| Gemini CLI | `./install.sh --agent gemini` | `~/.gemini/skills/landing-page-system` |
| Cursor | `./install.sh --agent cursor` | `~/.cursor/skills/landing-page-system` |
| All of the above | `./install.sh --agent all` | all of the above |

Other options: `--copy` (copy instead of symlink), `--bin-dir DIR` (where to link `lp`),
`--force`, `--uninstall`.

Agents without a skills folder (Aider, plain editors) do not need the install: every workspace
gets an `AGENTS.md` that explains the loop, and `python3 .lp/lp.py` runs from inside it.

## Quickstart

### 1. New product

```sh
cd ~/projects
lp init "Acme Plumbing"          # creates ./acme-plumbing/
cd acme-plumbing
lp next                          # step 1: goal and offer
lp start 1                       # copies the template to research/01-goal-offer.md
# ...fill it in...
lp done 1                        # validates, then points at step 2
```

Tell your agent: "Use the landing-page-system skill. Run `lp next` and follow it." The agent
loops through research, then the `home` page. At each gate it stops and asks you to run, for
example:

```sh
lp approve gate1 --page home --by "Your Name"
```

### 2. Another page for the same product

```sh
lp page add pricing --keyword "plumber prices harbor city"
lp next --page pricing           # starts at step 7; research reused, brand inherited
```

### 3. Redesign an existing site

```sh
lp init "Acme Plumbing" --mode redesign --url https://acme.example.com
cd acme-plumbing
lp next                          # step 0: audit the live site, save its copy, map URLs
```

The audit pre-fills research with `source: live-site` evidence, records every URL that must
survive in `audit/url-map.csv`, and decides which pages to rebuild. Step 15 refuses to finish
without a redirect map.

## Workspace layout

```
<dir>/<product-slug>/
  lp.json                    manifest: every step, page, gate and copy rule
  AGENTS.md CLAUDE.md GEMINI.md
  .lp/                       vendored lp.py, guide/, templates/, VERSION
  research/                  01-goal-offer.md ... 06-seo.md (product-level)
  brand/                     brand.md, tokens.css, assets/ (product-level, step 10)
  assets/                    logos, screenshots and photos from the owner
  audit/                     redesign only: site-audit.md, pages/, url-map.csv
  pages/<slug>/              07-structure.md ... 16-measure.md, 11-design/, build/
```

Commands find the workspace by walking up from the current folder to `lp.json`, like git finds
`.git`. Override with `--dir PATH` or `LP_WORKSPACE`.

## CLI reference

All commands accept `--json` and `--help`.

| Command | What it does |
|---|---|
| `lp init <product> [--mode new\|redesign] [--url URL] [--dir PATH] [--page home] [--no-agent-files] [--force]` | Create a workspace in `PATH/<slug>` (default: current folder). Vendors the guide, templates and CLI into `.lp/`. |
| `lp next [--page P] [--force]` | The single entry point for agents: next step, guide, inputs, outputs, template, done criteria, gate status. `--force` skips unfinished research. |
| `lp status [--page P]` | Table of steps x pages, gates and stale research. |
| `lp start N [--page P]` | Mark a step in progress and copy its template. Never overwrites. |
| `lp done N [--page P] [--force]` | Validate outputs (exist, not the template, no placeholders, headings kept, `verified:` date, step-specific rules) and mark done. Prints exactly what is missing. `--force` skips validation but never a gate. |
| `lp redo N [--page P]` | Reopen a step. For page steps, revokes the gates after it. |
| `lp approve gate1\|gate2\|gate3 --page P --by NAME [--note TEXT]` | Record a human approval. For people, not agents. |
| `lp page add <slug> [--keyword K] [--url URL]` | Add a page; it starts at step 7. Refuses a keyword another page owns. |
| `lp page list` | Pages, keywords and their next step. |
| `lp check [--page P] [FILE...]` | Copy lint (banned phrases, long dash density, placeholders, exclamation marks, we/you ratio, headline length) and HTML lint (one h1, title and meta description length, canonical, viewport, lang, img alt, empty links, Open Graph, JSON-LD validity), plus keyword cannibalization across pages. |
| `lp stale` | Research files whose `verified:` date is older than `stale_days` (default 90). |
| `lp sync-guide` | Refresh `.lp/` from the installed skill. Your files are not touched. |
| `lp doctor` | Python version, workspace, manifest and vendored versus installed version. |
| `lp --version` | Print the version. |

Exit codes: `0` ok; `1` validation failed, check found errors, or stale research; `2` usage
error or no workspace; `3` `lp next` is waiting on a human gate; `127` the `bin/lp` wrapper found
no `lp.py` or no Python 3.8+.

`check` severities: `error` (fails the command and blocks `lp done 8` and `lp done 14`), `warn`
(fix or write down why not), `info` (report only). Add your own banned phrases under
`copy_rules.extra_banned` in `lp.json`.

## Without Python

Everything is plain files. Read `SKILL.md` ("Manual fallback"), follow
`references/method-overview.md` and the step guides, copy templates by hand, and update
`lp.json` yourself.

## Repository layout

```
SKILL.md                 agent-facing router (Agent Skills format)
install.sh               installer for every agent
bin/lp                   POSIX sh wrapper that finds lp.py
scripts/lp.py            the CLI (also vendored into every workspace)
references/              method-overview.md, steps/00..16, checklists/
templates/               one template per step output, plus AGENTS.md.tmpl
tests/                   test_lp.py, test_portability.sh, fixtures/
```

## Tests

```sh
python3 -m unittest discover -s tests -v
bash tests/test_portability.sh
```

## License

MIT. See `LICENSE`.
