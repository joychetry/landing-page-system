# Changelog

## 1.0.0 (2026-10-17)

First release.

### Added

- `SKILL.md` router in the Agent Skills format: modes, the agent loop, human gates, honesty
  rules and a manual fallback for agents that cannot run Python.
- The method: `references/method-overview.md`, 17 step guides (`steps/00` to `steps/16`) and
  5 checklists (hero, SEO on-page, performance, accessibility, de-AI copy).
- Templates for every step output, plus `AGENTS.md.tmpl` for workspaces.
- `scripts/lp.py`, a standard-library CLI: `init`, `next`, `status`, `start`, `done`, `redo`,
  `approve`, `page add`, `page list`, `check`, `stale`, `sync-guide`, `doctor`, all with `--json`.
  Gates after steps 9 and 11 and before step 15 are enforced; product research comes before page
  work; later pages start at step 7 and inherit the brand; workspaces vendor the CLI and guides.
- `bin/lp` POSIX wrapper and `install.sh` for `.agents`, Claude Code, Codex, Pi, OpenCode,
  Gemini CLI and Cursor.
- Tests: `tests/test_lp.py` (unittest), `tests/test_portability.sh`, fixtures.

### Verified

- `python3 -m unittest discover -s tests -v`: 31 tests pass.
- `bash tests/test_portability.sh`: 89 checks pass (fake HOMEs for `.agents`, `.claude`, `.codex`,
  `.pi/agent` and `.config/opencode` under `env -i`; wrapper lookup by own location, conventional
  dirs, `LP_SKILL_HOME`, symlink and vendored `.lp/lp.py`; workspace runs with the skill
  uninstalled and after a move; `install.sh` link, copy, idempotent rerun, no-clobber, uninstall).
- Dry walkthrough through `bin/lp` in a temp dir, using the sample content in `tests/fixtures/sample`:
  - `lp init "Tidewater Plumbing"` created the workspace, `.lp/` and the agent files.
  - `lp done 1` on the untouched template was refused (14 placeholders, untouched template, exit 1).
    With research filled, `lp done 1` to `lp done 6` passed.
  - Page `home`: steps 7, 8 and 9 done. `lp next` stopped at gate1 (exit 3) and printed
    `lp approve gate1 --page home --by "<your name>"`; `lp start 10` was refused (exit 1).
  - After the approval: steps 10 and 11 done, gate2 blocked and was approved, steps 12 to 14 done,
    `lp check --page home` reported 0 errors and 0 warnings, gate3 blocked `lp start 15` (exit 1).
  - After gate3: steps 15 and 16 done; `lp next` reported everything done and suggested
    `lp page add` or `lp redo 16`.
  - `lp page add pricing --keyword "same day plumber harbor city"` was refused as cannibalization
    (exit 1). With its own keyword, `pricing` started at step 7 with step 10 `inherited`.
  - `lp init "Tidewater Old Site" --mode redesign --url https://tidewater-plumbing.example.com`
    started at step 0 with the site URL and the audit guide.
- No em dashes and no machine- or person-specific names in the shipped files.
- `SKILL.md` description: 924 characters (limit 1024); compatibility: 304 characters (limit 500).
