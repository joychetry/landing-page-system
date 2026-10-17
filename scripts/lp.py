#!/usr/bin/env python3
"""lp: the landing-page-system CLI.

Walks any agent or human through the 16-step landing page method (plus step 0
for redesigns). Python 3.8+ standard library only, no network access.

Importable as a module: every command is a plain function; main() is a thin
argparse wrapper. The skill root is resolved from __file__, so the same file
works from any install path and from a workspace's vendored .lp/ copy.
"""

import argparse
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

__version__ = "1.0.0"
SCHEMA = 1
MANIFEST = "lp.json"
VENDOR = ".lp"
SKILL_NAME = "landing-page-system"

HERE = Path(__file__).resolve().parent
# Vendored copy: .lp/lp.py next to .lp/guide/. Skill copy: scripts/lp.py under the skill root.
SELF_ROOT = HERE if (HERE / "guide").is_dir() else HERE.parent

INSTALL_DIRS = [
    "~/.agents/skills", "~/.claude/skills", "~/.codex/skills", "~/.pi/agent/skills",
    "~/.config/opencode/skills", "~/.gemini/skills", "~/.factory/skills", "~/.cursor/skills",
]

P = "pages/{page}/"
RF = {
    1: "research/01-goal-offer.md", 2: "research/02-customers.md", 3: "research/03-competitors.md",
    4: "research/04-proof.md", 5: "research/05-brand-story.md", 6: "research/06-seo.md",
}
AUDIT = "audit/site-audit.md"
URLMAP = "audit/url-map.csv"
BRAND = ["brand/brand.md", "brand/tokens.css"]
BUILD = P + "build/index.html"


def _s(title, scope, guide, templates=(), extra=(), inputs=(), checklists=()):
    return {"title": title, "scope": scope, "guide": guide, "templates": list(templates),
            "extra": list(extra), "inputs": list(inputs), "checklists": list(checklists)}


ALL_CHECKLISTS = ["hero.md", "seo-onpage.md", "performance.md", "accessibility.md", "de-ai-copy.md"]
STEPS = {
    0: _s("Audit the existing site", "product", "00-audit-existing.md",
          [("00-site-audit.md", AUDIT), ("url-map.csv", URLMAP)], ["audit/pages/"], [],
          ALL_CHECKLISTS[:4]),
    1: _s("Goal and offer", "product", "01-goal-offer.md", [("01-goal-offer.md", RF[1])], [], [AUDIT]),
    2: _s("Customer research", "product", "02-customer-research.md", [("02-customers.md", RF[2])], [],
          [RF[1], AUDIT]),
    3: _s("Competitor research", "product", "03-competitor-research.md", [("03-competitors.md", RF[3])], [],
          [RF[1], RF[2], AUDIT]),
    4: _s("Proof and assets", "product", "04-proof-assets.md", [("04-proof.md", RF[4])], [],
          [RF[1], RF[2], RF[3], "assets/", AUDIT]),
    5: _s("Brand story", "product", "05-brand-story.md", [("05-brand-story.md", RF[5])], [],
          [RF[1], RF[2], RF[4]]),
    6: _s("SEO research", "product", "06-seo-research.md", [("06-seo.md", RF[6])], [],
          [RF[1], RF[2], RF[3], AUDIT]),
    7: _s("Page structure", "page", "07-page-structure.md", [("07-structure.md", P + "07-structure.md")], [],
          [RF[n] for n in range(1, 7)]),
    8: _s("Page copy", "page", "08-page-copy.md", [("08-copy.md", P + "08-copy.md")], [],
          [P + "07-structure.md", RF[1], RF[2], RF[4], RF[5], RF[6]], ["hero.md", "de-ai-copy.md", "seo-onpage.md"]),
    9: _s("Wireframe", "page", "09-wireframe.md", [("09-wireframe.html", P + "09-wireframe.html")], [],
          [P + "07-structure.md", P + "08-copy.md"], ["hero.md"]),
    10: _s("Brand guidelines", "brand", "10-brand-guidelines.md",
           [("10-brand.md", BRAND[0]), ("10-tokens.css", BRAND[1])], [],
           [P + "08-copy.md", P + "09-wireframe.html", RF[5], "assets/", AUDIT], ["accessibility.md"]),
    11: _s("Final design", "page", "11-final-design.md", [], [P + "11-design/", BUILD],
           [P + "08-copy.md", P + "09-wireframe.html"] + BRAND + ["assets/"], ["hero.md", "accessibility.md"]),
    12: _s("Page visuals", "page", "12-page-visuals.md", [("12-visuals.md", P + "12-visuals.md")], [],
           [P + "08-copy.md", RF[4], BUILD, "assets/"], ["performance.md", "accessibility.md"]),
    13: _s("Polish", "page", "13-polish.md", [("13-polish.md", P + "13-polish.md")], [BUILD],
           [BUILD, P + "12-visuals.md", BRAND[0]], ["accessibility.md", "performance.md"]),
    14: _s("Last checks", "page", "14-last-checks.md", [("14-checks.md", P + "14-checks.md")], [],
           [BUILD, P + "08-copy.md", RF[4], BRAND[0]], ALL_CHECKLISTS),
    15: _s("Ship", "page", "15-ship.md", [("15-ship.md", P + "15-ship.md")], [],
           [BUILD, P + "14-checks.md", P + "08-copy.md", URLMAP], ["seo-onpage.md", "performance.md"]),
    16: _s("Measure and iterate", "page", "16-measure-iterate.md", [("16-measure.md", P + "16-measure.md")], [],
           [P + "15-ship.md", RF[1]]),
}
PRODUCT_STEPS = [0, 1, 2, 3, 4, 5, 6]
PAGE_STEPS = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
PAGE_FLOW = [7, 8, 9, "gate1", 10, 11, "gate2", 12, 13, 14, "gate3", 15, 16]
GATES = {"gate1": (9, "wireframe"), "gate2": (11, "final design"), "gate3": (14, "ship and deploy")}
NEEDS_GATE = {10: "gate1", 11: "gate1", 12: "gate2", 13: "gate2", 14: "gate2", 15: "gate3", 16: "gate3"}
SOURCED_STEPS = (2, 3, 6)  # guides require 3+ source markers in these research files
FINISHED = ("done", "skipped", "inherited")

DEFAULT_BANNED = [
    "unlock", "unleash", "seamless", "elevate", "game-changer", "revolutionize", "cutting-edge",
    "state-of-the-art", "world-class", "best-in-class", "next-level", "supercharge", "harness the power",
    "look no further", "delve", "empower", "synergy", "transformative", "unparalleled",
    "real people, real results", "say goodbye to", "we've got you covered", "in today's fast-paced world",
    "see what our customers say",
]

PLACEHOLDER_RE = re.compile(r"\{\{[^{}]*\}\}|\bTODO\b|\bTBD\b|(?i:lorem ipsum)")
SOURCE_RE = re.compile(r"https?://\S+|provided by owner, \d{4}-\d{2}-\d{2}|source: live-site", re.I)
EM_DASH = "\u2014"


class LPError(Exception):
    def __init__(self, msg, code=2, data=None):
        super().__init__(msg)
        self.code = code
        self.data = data or {}


# ----------------------------------------------------------------- basics

def today():
    return dt.date.today()


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def read(path):
    return Path(path).read_text(encoding="utf-8", errors="replace")


def strip_comments(text, name=""):
    if name.endswith(".css"):
        return re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def layout(root):
    """Where guide, templates and script live for a skill root or a vendored .lp/ dir."""
    root = Path(root)
    if (root / "references").is_dir():
        return {"guide": root / "references", "templates": root / "templates", "script": root / "scripts" / "lp.py"}
    return {"guide": root / "guide", "templates": root / "templates", "script": root / "lp.py"}


def script_version(script):
    try:
        m = re.search(r'^__version__ = "([^"]+)"', read(script), re.M)
        return m.group(1) if m else None
    except OSError:
        return None


def installed_skill():
    """The installed skill root (not a vendored copy), or None."""
    cands = []
    if (SELF_ROOT / "references").is_dir():
        cands.append(SELF_ROOT)
    if os.environ.get("LP_SKILL_HOME"):
        cands.append(Path(os.environ["LP_SKILL_HOME"]).expanduser())
    cands += [Path(d).expanduser() / SKILL_NAME for d in INSTALL_DIRS]
    for c in cands:
        if (c / "references").is_dir() and (c / "scripts" / "lp.py").is_file():
            return c.resolve()
    return None


def find_workspace(start):
    p = Path(start).expanduser().resolve()
    for d in [p] + list(p.parents):
        if (d / MANIFEST).is_file():
            return d
    return None


def workspace(args):
    start = getattr(args, "dir", None) or os.environ.get("LP_WORKSPACE") or os.getcwd()
    ws = find_workspace(start)
    if not ws:
        raise LPError("no lp.json found in %s or any parent. Run `lp init <product>` first, "
                      "or pass --dir / set LP_WORKSPACE." % start)
    return ws


def ws_layout(ws):
    """Prefer the workspace's vendored guide and templates; fall back to this script's own."""
    v = layout(ws / VENDOR)
    own = layout(SELF_ROOT)
    return {k: (v[k] if v[k].exists() else own[k]) for k in ("guide", "templates")}


def load(ws):
    path = ws / MANIFEST
    try:
        m = json.loads(read(path))
    except ValueError as e:
        raise LPError("%s is not valid JSON: %s" % (path, e))
    problems = manifest_problems(m)
    if problems:
        raise LPError("%s is invalid: %s" % (path, "; ".join(problems)))
    return m


def manifest_problems(m):
    out = []
    if not isinstance(m, dict):
        return ["top level is not an object"]
    if m.get("schema") != SCHEMA:
        out.append("schema must be %d (found %r)" % (SCHEMA, m.get("schema")))
    for k in ("name", "slug", "mode", "research", "brand", "pages", "copy_rules"):
        if k not in m:
            out.append("missing key %r" % k)
    if out:
        return out
    if m["mode"] not in ("new", "redesign"):
        out.append("mode must be new or redesign")
    for n in PRODUCT_STEPS:
        if str(n) not in m["research"]:
            out.append("research is missing step %d" % n)
    for slug, page in m["pages"].items():
        for n in PAGE_STEPS:
            if str(n) not in page.get("steps", {}):
                out.append("page %s is missing step %d" % (slug, n))
    return out


def save(ws, m):
    """Atomic write: temp file in the same directory, then rename."""
    fd, tmp = tempfile.mkstemp(prefix=".lp.json.", dir=str(ws))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(m, f, indent=2)
            f.write("\n")
        os.replace(tmp, str(ws / MANIFEST))
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def outputs_for(step, page):
    s = STEPS[step]
    return [o.format(page=page) for o in [t[1] for t in s["templates"]] + s["extra"]
            if page or "{page}" not in o]


def new_state(step, page=None, status="todo"):
    return {"status": status, "done_at": None, "outputs": outputs_for(step, page)}


def new_page(m, slug, keyword=None, url=None, start_step=7):
    steps = {str(n): new_state(n, slug) for n in PAGE_STEPS}
    if m["brand"]["status"] == "done":
        steps["10"]["status"] = "inherited"
    return {"created": today().isoformat(), "primary_keyword": keyword or None, "url": url or None,
            "start_step": start_step, "steps": steps, "approvals": {}}


def state(m, step, page=None):
    if step in PRODUCT_STEPS:
        return m["research"][str(step)]
    if step == 10 and not page:
        return m["brand"]
    return m["pages"][page]["steps"][str(step)]


def step_status(m, step, page=None):
    """Effective status. Step 10 follows the product-level brand state."""
    if step == 10:
        b = m["brand"]["status"]
        if b != "done" or not page:
            return b
        return m["pages"][page]["steps"]["10"]["status"]
    return state(m, step, page)["status"]


def is_finished(m, step, page=None):
    if step == 10:
        return m["brand"]["status"] in ("done", "skipped")
    return step_status(m, step, page) in FINISHED


def set_status(m, step, page, status):
    when = today().isoformat() if status == "done" else None
    if step == 10:
        m["brand"].update(status=status, done_at=when)
        for slug, p in m["pages"].items():
            s = p["steps"]["10"]
            if slug == page:
                s.update(status=status, done_at=when)
            elif status == "done" and s["status"] != "done":
                s.update(status="inherited", done_at=None)
        return
    state(m, step, page).update(status=status, done_at=when)


def approved(m, gate, page):
    return bool(m["pages"][page]["approvals"].get(gate))


def research_pending(m):
    return [n for n in PRODUCT_STEPS if not is_finished(m, n)]


def gates_missing(m, step, page):
    need = NEEDS_GATE.get(step)
    if not need:
        return []
    order = ["gate1", "gate2", "gate3"]
    gates = order[:order.index(need) + 1]
    if page is None:  # brand-level step 10: some page must have passed gate 1
        return [] if any(approved(m, "gate1", p) for p in m["pages"]) else ["gate1"]
    return [g for g in gates if not approved(m, g, page)]


def cmd_str(verb, step, page=None):
    s = "lp %s %s" % (verb, step)
    return s + (" --page %s" % page if page and STEPS[step]["scope"] != "product" else "")


def approve_cmd(gate, page):
    return 'lp approve %s --page %s --by "<your name>"' % (gate, page)


def done_criteria(guide_file):
    try:
        text = read(guide_file)
    except OSError:
        return []
    m = re.search(r"^## Done when\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        return []
    return [re.sub(r"^\s*-\s*(\[[ x]\]\s*)?", "", line).strip()
            for line in m.group(1).splitlines() if line.strip().startswith("-")]


def resolve_page(m, page, step):
    """Which page a step command applies to. None for product-level work."""
    if STEPS[step]["scope"] == "product":
        return None
    if page:
        if page not in m["pages"]:
            raise LPError("no page %r. Pages: %s" % (page, ", ".join(m["pages"]) or "none"))
        return page
    pages = list(m["pages"])
    if len(pages) == 1:
        return pages[0]
    for test in (lambda p: state(m, step, p)["status"] == "in_progress",
                 lambda p: (next_for_page(m, p).get("step") == step)):
        hits = [p for p in pages if test(p)]
        if len(hits) == 1:
            return hits[0]
    if STEPS[step]["scope"] == "brand":
        return None
    raise LPError("several pages exist; pass --page (one of: %s)" % ", ".join(pages))


# ----------------------------------------------------------------- next

def next_for_page(m, page):
    for item in PAGE_FLOW:
        if isinstance(item, str):
            if not approved(m, item, page):
                return {"kind": "gate", "gate": item, "page": page}
        elif not is_finished(m, item, page):
            return {"kind": "step", "step": item, "page": page}
    return {"kind": "done", "page": page}


def describe(ws, m, step, page):
    lay = ws_layout(ws)
    s = STEPS[step]
    redesign = m["mode"] == "redesign"

    def entry(rel):
        return {"relative": rel, "path": str(ws / rel), "exists": (ws / rel).exists()}

    inputs = [i.format(page=page) for i in s["inputs"] if (page or "{page}" not in i)
              and (redesign or not i.startswith("audit/"))]
    guide = lay["guide"] / "steps" / s["guide"]
    item = {
        "status": "step", "step": step, "title": s["title"],
        "page": page if s["scope"] != "product" else "product", "scope": s["scope"],
        "state": step_status(m, step, page),
        "guide": {"relative": rel_to(guide, ws), "path": str(guide)},
        "inputs": [entry(i) for i in inputs],
        "outputs": [entry(o) for o in outputs_for(step, page)],
        "templates": [{"template": rel_to(lay["templates"] / t, ws), "output": o.format(page=page)}
                      for t, o in s["templates"]],
        "checklists": [rel_to(lay["guide"] / "checklists" / c, ws) for c in s["checklists"]],
        "done_criteria": done_criteria(guide),
        "commands": {"start": cmd_str("start", step, page), "done": cmd_str("done", step, page)},
    }
    if step == 0:
        item["site_url"] = m.get("url")
    if page:
        item["gates"] = gate_info(m, page)
    return item


def gate_info(m, page):
    return {g: m["pages"][page]["approvals"].get(g) or {"pending": True, "after_step": GATES[g][0]}
            for g in GATES}


def rel_to(path, ws):
    try:
        return str(Path(path).resolve().relative_to(ws))
    except ValueError:
        return str(path)


def next_item(ws, m, page=None, force=False):
    pending = research_pending(m)
    if pending and not force:
        it = describe(ws, m, pending[0], None)
        if page:
            it["note"] = "Product-level research comes first; page %s waits for it (use --force to skip ahead)." % page
        return it
    pages = [page] if page else list(m["pages"])
    if page and page not in m["pages"]:
        raise LPError("no page %r. Pages: %s" % (page, ", ".join(m["pages"]) or "none"))
    results = [next_for_page(m, p) for p in pages]
    steps = [r for r in results if r["kind"] == "step"]
    gates = [r for r in results if r["kind"] == "gate"]
    blocked = [{"gate": g["gate"], "page": g["page"], "approve_command": approve_cmd(g["gate"], g["page"])}
               for g in gates]
    if steps:
        it = describe(ws, m, steps[0]["step"], steps[0]["page"])
        if blocked:
            it["blocked"] = blocked
        return it
    if gates:
        g = gates[0]
        after, what = GATES[g["gate"]]
        return {
            "status": "gate", "gate": g["gate"], "page": g["page"], "after_step": after, "what": what,
            "approve_command": approve_cmd(g["gate"], g["page"]), "blocked": blocked,
            "message": ("STOP. %s (%s) for page %s needs a human. Show them the work and ask them to run: %s. "
                        "Agents never approve gates themselves." % (g["gate"], what, g["page"],
                                                                     approve_cmd(g["gate"], g["page"]))),
        }
    if not m["pages"]:
        return {"status": "done", "page": None, "message": "Research is done and there are no pages. "
                "Add one: lp page add home --keyword \"...\""}
    return {"status": "done", "page": page,
            "message": ("All steps are done%s. Start the next measure cycle with `lp redo 16 --page <page>`, "
                        "or add a page with `lp page add <slug> --keyword \"...\"`."
                        % (" for page %s" % page if page else ""))}


def format_next(it):
    if it["status"] == "gate":
        lines = [it["message"]]
        for b in it.get("blocked", [])[1:]:
            lines.append("Also waiting: %s for page %s: %s" % (b["gate"], b["page"], b["approve_command"]))
        return "\n".join(lines)
    if it["status"] == "done":
        return it["message"]
    where = "product" if it["page"] in ("product", None) else "page: %s" % it["page"]
    lines = ["Next: step %d, %s (%s, %s)" % (it["step"], it["title"], where, it["state"])]
    if it.get("note"):
        lines.append("Note: " + it["note"])
    if it.get("site_url"):
        lines.append("Site:       " + it["site_url"])
    lines.append("Guide:      " + it["guide"]["relative"])
    if it["inputs"]:
        lines.append("Read:       " + ", ".join(i["relative"] + ("" if i["exists"] else " (missing)")
                                                for i in it["inputs"]))
    lines.append("Write:      " + ", ".join(o["relative"] for o in it["outputs"]))
    for t in it["templates"]:
        lines.append("Template:   %s -> %s" % (t["template"], t["output"]))
    if it["checklists"]:
        lines.append("Checklists: " + ", ".join(it["checklists"]))
    if it["done_criteria"]:
        lines.append("Done when:")
        lines += ["  - " + c for c in it["done_criteria"]]
    lines.append("Run:        %s, do the work, then %s" % (it["commands"]["start"], it["commands"]["done"]))
    for b in it.get("blocked", []):
        lines.append("Waiting on a human: %s for page %s: %s" % (b["gate"], b["page"], b["approve_command"]))
    return "\n".join(lines)


# ----------------------------------------------------------------- validation

def md_headings(text):
    return [l.strip() for l in text.splitlines() if l.startswith("## ")]


def frontmatter_date(text):
    m = re.match(r"\ufeff?---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None, "no frontmatter block (--- verified: YYYY-MM-DD ---) at the top"
    v = re.search(r"^verified:\s*(\S+)\s*$", m.group(1), re.M)
    if not v:
        return None, "frontmatter has no `verified: YYYY-MM-DD` line"
    try:
        d = dt.date.fromisoformat(v.group(1))
    except ValueError:
        return None, "`verified:` is %r, not a YYYY-MM-DD date" % v.group(1)
    if d > today():
        return None, "`verified:` date %s is in the future" % d
    return d, None


def csv_rows(path):
    with open(str(path), newline="", encoding="utf-8") as f:
        rows = [r for r in csv.reader(f) if any(c.strip() for c in r)]
    return rows[0] if rows else [], rows[1:]


def file_problems(ws, rel, template):
    """Generic output checks: exists, not the template, no placeholders, template headings kept."""
    path = ws / rel
    if not path.is_file():
        return ["%s does not exist (run `lp start` to copy the template)" % rel]
    text = read(path)
    if rel.endswith(".csv"):
        head, rows = csv_rows(path)
        out = []
        if template and template.exists():
            want, _ = csv_rows(template)
            miss = [c for c in want if c not in head]
            if miss:
                out.append("%s header is missing columns: %s" % (rel, ", ".join(miss)))
        if not rows:
            out.append("%s has no data rows" % rel)
        return out
    out = []
    body = strip_comments(text, rel)
    hits = placeholders(body)
    if hits:
        out.append("%s still has %d placeholder(s): %s" % (rel, len(hits), ", ".join(hits[:6])))
    if template and template.exists():
        tpl = read(template)
        tbody = strip_comments(tpl, rel)
        if body.split() == tbody.split():
            out.append("%s is still the untouched template" % rel)
        else:
            added = len("".join(body.split())) - len("".join(PLACEHOLDER_RE.sub("", tbody).split()))
            if added < 40:
                out.append("%s is barely changed from the template (%d characters added)" % (rel, added))
        if rel.endswith(".md"):
            have = set(md_headings(text))
            miss = [h for h in md_headings(tpl) if h not in have]
            if miss:
                out.append("%s is missing required headings: %s" % (rel, ", ".join(miss)))
    return out


def validate(ws, m, step, page):
    lay = ws_layout(ws)
    s = STEPS[step]
    probs = []
    for tname, out in s["templates"]:
        probs += file_problems(ws, out.format(page=page), lay["templates"] / tname)
    if 1 <= step <= 6:
        rel = RF[step]
        if (ws / rel).is_file():
            text = read(ws / rel)
            _, err = frontmatter_date(text)
            if err:
                probs.append("%s: %s" % (rel, err))
            if step in SOURCED_STEPS:
                n = len(SOURCE_RE.findall(text))
                if n < 3:
                    probs.append("%s has %d source markers; need at least 3 (URLs, \"provided by owner, "
                                 "YYYY-MM-DD\" or \"source: live-site\")" % (rel, n))
            if step == 4 and not re.search(r"^## Gaps\s*$", text, re.M):
                probs.append("%s has no `## Gaps` section. Missing proof is listed there, never invented." % rel)
    if step == 0:
        pages_dir = ws / "audit" / "pages"
        if not pages_dir.is_dir() or not any(f.is_file() for f in pages_dir.iterdir()):
            probs.append("audit/pages/ has no saved page copy; save at least one page as audit/pages/<slug>.md")
    if step == 7:
        kw = keyword_in_file(ws, page)
        if not kw:
            probs.append("%s07-structure.md has no filled `Primary keyword:` line" % P.format(page=page))
        else:
            clash = [p for p in m["pages"] if p != page and norm_kw(page_keyword(ws, m, p)) == norm_kw(kw)]
            if clash:
                probs.append("primary keyword %r is already used by page %s (keyword cannibalization)"
                             % (kw, ", ".join(clash)))
    if step == 8 and (ws / (P + "08-copy.md").format(page=page)).is_file():
        f = [x for x in check_file(ws / (P + "08-copy.md").format(page=page), m["copy_rules"], ws)
             if x["severity"] == "error"]
        probs += ["lp check: %s: %s" % (x["rule"], x["message"]) for x in f]
    if step in (9, 11):
        rel = (P + ("09-wireframe.html" if step == 9 else "build/index.html")).format(page=page)
        if (ws / rel).is_file():
            hp = parse_html(read(ws / rel))
            if hp.h1 != 1:
                probs.append("%s must have exactly one <h1> (found %d)" % (rel, hp.h1))
            if step == 11:
                probs += file_problems(ws, rel, None)
                words = len(" ".join(hp.text).split())
                if words < 50:
                    probs.append("%s has only %d words of visible text; build the full page" % (rel, words))
        elif step == 11:
            probs.append("%s does not exist" % rel)
    if step == 11:
        d = ws / (P + "11-design").format(page=page)
        n = len([f for f in d.iterdir() if f.is_file()]) if d.is_dir() else 0
        if n < 2:
            probs.append("%s/ holds %d files; need at least 2 hero directions" % (rel_to(d, ws), n))
    if step == 13:
        build = ws / (P + "build").format(page=page)
        idx = build / "index.html"
        if not idx.is_file():
            probs.append("%s does not exist" % rel_to(idx, ws))
        else:
            if not parse_html(read(idx)).meta.get("viewport"):
                probs.append("%s has no <meta name=\"viewport\">" % rel_to(idx, ws))
            css = "".join(read(f) for f in build.rglob("*") if f.suffix in (".html", ".css") and f.is_file())
            if re.search(r"\b(animation|transition)\s*:", css) and "prefers-reduced-motion" not in css:
                probs.append("build/ animates but has no @media (prefers-reduced-motion: reduce) rule")
    if step == 14:
        f = [x for x in check_page(ws, m, page) if x["severity"] == "error"]
        probs += ["lp check: %s: %s: %s" % (x["file"], x["rule"], x["message"]) for x in f]
    if step == 15 and m["mode"] == "redesign":
        if not (ws / URLMAP).is_file() or not csv_rows(ws / URLMAP)[1]:
            probs.append("%s has no rows; a redesign needs a 301 redirect map for every changed URL" % URLMAP)
    return probs


def keyword_in_file(ws, page):
    path = ws / (P + "07-structure.md").format(page=page)
    if not path.is_file():
        return None
    mt = re.search(r"^Primary keyword:[ \t]*(.*)$", strip_comments(read(path)), re.M)
    kw = mt.group(1).strip() if mt else ""
    return kw if kw and not PLACEHOLDER_RE.search(kw) else None


def page_keyword(ws, m, page):
    return m["pages"][page].get("primary_keyword") or keyword_in_file(ws, page)


def norm_kw(kw):
    return " ".join((kw or "").lower().split())


# ----------------------------------------------------------------- check (lint)

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.title = None
        self.lang = None
        self.meta = {}
        self.canonical = None
        self.img_no_alt = 0
        self.empty_links = 0
        self.hash_links = 0
        self.jsonld = []
        self.text = []
        self.headings = []
        self._cap = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang", "").strip() or None
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical = a.get("href", "")
        elif tag == "img" and "alt" not in a:
            self.img_no_alt += 1
        elif tag == "a" and "href" in a:
            href = a["href"].strip()
            if not href:
                self.empty_links += 1
            elif href == "#":
                self.hash_links += 1
        if tag in ("script", "style", "title", "h1", "h2", "h3"):
            if tag == "h1":
                self.h1 += 1
            kind = tag
            if tag == "script" and a.get("type", "").strip().lower() == "application/ld+json":
                kind = "ld"
            self._cap.append((tag, kind, []))

    def handle_endtag(self, tag):
        if self._cap and self._cap[-1][0] == tag:
            _, kind, buf = self._cap.pop()
            s = "".join(buf)
            if kind == "ld":
                self.jsonld.append(s)
            elif kind == "title":
                self.title = " ".join(s.split())
            elif kind in ("h1", "h2", "h3"):
                self.headings.append(" ".join(s.split()))

    def handle_data(self, data):
        for _, _, buf in self._cap:
            buf.append(data)
        if not any(k in ("script", "style", "ld", "title") for _, k, _ in self._cap):
            self.text.append(data)


def parse_html(text):
    p = PageParser()
    p.feed(text)
    p.close()
    return p


def banned_pattern(phrase):
    p = phrase.lower().replace("\u2019", "'")
    if p.endswith("e") and " " not in p:
        tail = re.escape(p[:-1]) + r"(?:e\w{0,2}|ing)"
    else:
        tail = re.escape(p) + r"\w{0,3}"
    return re.compile(r"(?<![\w-])" + tail + r"(?![\w-])", re.I)


def finding(sev, f, rule, msg):
    return {"severity": sev, "file": f, "rule": rule, "message": msg}


def copy_lint(text, headlines, rules, fname):
    out = []
    text = text.replace("\u2019", "'")
    for phrase in list(rules.get("banned_phrases", DEFAULT_BANNED)) + list(rules.get("extra_banned", [])):
        hits = banned_pattern(phrase).findall(text)
        if hits:
            out.append(finding("error", fname, "banned-phrase", "%r appears %d time(s)" % (phrase, len(hits))))
    words = re.findall(r"[A-Za-z0-9']+", text)
    dashes = text.count(EM_DASH)
    limit = rules.get("max_em_dashes_per_1000_words", 2)
    if dashes > limit * max(len(words), 1000) / 1000.0:
        out.append(finding("warn", fname, "em-dash-density",
                           "%d long dashes in %d words (limit %s per 1000 words)" % (dashes, len(words), limit)))
    bangs = re.sub(r"!\[|<!", "", text).count("!")
    if bangs > 1:
        out.append(finding("warn", fname, "exclamation", "%d exclamation marks; use at most one on the page" % bangs))
    you = len(re.findall(r"\b(you|your|yours|you're|you'll|you've)\b", text, re.I))
    we = len(re.findall(r"\b(we|our|ours|us|we're|we'll|we've)\b", text, re.I))
    out.append(finding("info", fname, "we-you-ratio", "you/your: %d, we/our/us: %d%s"
                       % (you, we, " (talks about itself more than the reader)" if we > you else "")))
    for h in headlines:
        n = len(h.split())
        if n > 14:
            out.append(finding("warn", fname, "headline-length", "%d words (max 14): %s" % (n, h[:80])))
    return out


def placeholders(text):
    """Unique placeholders in order of appearance, long ones shortened for display."""
    seen = []
    for m in PLACEHOLDER_RE.finditer(text):
        h = m.group(0) if len(m.group(0)) <= 40 else m.group(0)[:36] + "...}}"
        if h not in seen:
            seen.append(h)
    return seen


def placeholder_lint(raw, fname):
    hits = placeholders(strip_comments(raw, fname))
    return [finding("error", fname, "placeholder", "%d unfilled: %s" % (len(hits), ", ".join(hits[:6])))] if hits else []


def html_lint(hp, fname, full=True):
    out = []
    if hp.h1 != 1:
        out.append(finding("error", fname, "h1", "exactly one <h1> required (found %d)" % hp.h1))
    if hp.img_no_alt:
        out.append(finding("error", fname, "img-alt", "%d <img> without an alt attribute" % hp.img_no_alt))
    if hp.empty_links:
        out.append(finding("error", fname, "empty-href", "%d link(s) with an empty href" % hp.empty_links))
    if hp.hash_links:
        out.append(finding("warn", fname, "hash-href", "%d link(s) with href=\"#\"" % hp.hash_links))
    if not full:
        return out
    if not hp.lang:
        out.append(finding("error", fname, "lang", "<html> has no lang attribute"))
    if not hp.meta.get("viewport"):
        out.append(finding("error", fname, "viewport", "no <meta name=\"viewport\">"))
    if not hp.title:
        out.append(finding("error", fname, "title", "no <title>"))
    elif not 50 <= len(hp.title) <= 60:
        out.append(finding("warn", fname, "title-length", "title is %d chars (want 50 to 60)" % len(hp.title)))
    desc = hp.meta.get("description", "").strip()
    if not desc:
        out.append(finding("error", fname, "meta-description", "no meta description"))
    elif not 130 <= len(desc) <= 155:
        out.append(finding("warn", fname, "meta-description-length",
                           "meta description is %d chars (want 130 to 155)" % len(desc)))
    if not hp.canonical:
        out.append(finding("warn", fname, "canonical", "no <link rel=\"canonical\">"))
    for og in ("og:title", "og:description", "og:image"):
        if not hp.meta.get(og):
            out.append(finding("warn", fname, "open-graph", "missing %s" % og))
    if not hp.meta.get("twitter:card"):
        out.append(finding("info", fname, "twitter-card", "no twitter:card meta tag"))
    if not hp.jsonld:
        out.append(finding("warn", fname, "json-ld", "no JSON-LD structured data"))
    for i, block in enumerate(hp.jsonld, 1):
        try:
            json.loads(block)
        except ValueError as e:
            out.append(finding("error", fname, "json-ld", "JSON-LD block %d does not parse: %s" % (i, e)))
    return out


def check_file(path, rules, ws=None):
    path = Path(path)
    fname = rel_to(path, ws) if ws else str(path)
    if not path.is_file():
        return [finding("error", fname, "missing", "file not found")]
    raw = read(path)
    out = placeholder_lint(raw, fname)
    if path.suffix.lower() in (".html", ".htm"):
        hp = parse_html(raw)
        full = not path.name.startswith("09-wireframe")  # wireframes skip head and SEO tags
        out += html_lint(hp, fname, full)
        out += copy_lint(" ".join(hp.text), hp.headings, rules, fname)
    else:
        body = strip_comments(raw, fname)
        heads = re.findall(r"^#{1,3}\s+(.+)$", body, re.M) + re.findall(r"\*\*Headline:\*\*\s*(.+)", body)
        out += copy_lint(body, [h.strip() for h in heads], rules, fname)
    return out


def page_files(ws, page):
    base = ws / P.format(page=page)
    files = [base / "08-copy.md", base / "09-wireframe.html"]
    files += sorted((base / "build").rglob("*.htm*")) if (base / "build").is_dir() else []
    return [f for f in files if f.is_file()]


def cannibalization(ws, m):
    seen = {}
    for p in m["pages"]:
        kw = norm_kw(page_keyword(ws, m, p))
        if kw:
            seen.setdefault(kw, []).append(p)
    return [finding("error", MANIFEST, "cannibalization",
                    "pages %s share the primary keyword %r" % (", ".join(ps), kw))
            for kw, ps in seen.items() if len(ps) > 1]


def check_page(ws, m, page):
    out = []
    for f in page_files(ws, page):
        out += check_file(f, m["copy_rules"], ws)
    return out + cannibalization(ws, m)


# ----------------------------------------------------------------- vendoring

def copy_tree(src, dst):
    for f in Path(src).rglob("*"):
        if f.is_file():
            t = Path(dst) / f.relative_to(src)
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(f), str(t))


def vendor(ws, source_root):
    src = layout(source_root)
    dest = ws / VENDOR
    dest.mkdir(exist_ok=True)
    copy_tree(src["guide"], dest / "guide")
    copy_tree(src["templates"], dest / "templates")
    if src["script"].resolve() != (dest / "lp.py").resolve():
        shutil.copy2(str(src["script"]), str(dest / "lp.py"))
    ver = script_version(dest / "lp.py") or __version__
    (dest / "VERSION").write_text(ver + "\n", encoding="utf-8")
    return ver


AGENT_FILES = {
    "CLAUDE.md": "@AGENTS.md\n\nClaude Code: follow AGENTS.md above; start every session with `python3 .lp/lp.py next`.\n",
    "GEMINI.md": "@AGENTS.md\n\nGemini CLI: follow AGENTS.md above; start every session with `python3 .lp/lp.py next`.\n",
}


def write_agent_files(ws, m):
    tpl = ws_layout(ws)["templates"] / "AGENTS.md.tmpl"
    first = "0 (audit the existing site)" if m["mode"] == "redesign" else "1 (goal and offer)"
    text = read(tpl)
    for k, v in {"product": m["name"], "slug": m["slug"], "mode": m["mode"], "url": m.get("url") or "none",
                 "first_step": first, "version": m["skill_version"]}.items():
        text = text.replace("{{%s}}" % k, v)
    files = dict(AGENT_FILES, **{"AGENTS.md": text})
    written, skipped = [], []
    for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        if (ws / name).exists():
            skipped.append(name)
        else:
            (ws / name).write_text(files[name], encoding="utf-8")
            written.append(name)
    return written, skipped


# ----------------------------------------------------------------- commands

def default_rules():
    return {"banned_phrases": list(DEFAULT_BANNED), "max_em_dashes_per_1000_words": 2, "extra_banned": []}


def cmd_init(args):
    slug = slugify(args.product)
    if not slug:
        raise LPError("product name %r has no letters or digits" % args.product)
    page = slugify(args.page or "home")
    if not page:
        raise LPError("invalid page slug %r" % args.page)
    if args.mode == "redesign" and not args.url:
        raise LPError("redesign mode needs --url https://... of the live site")
    parent = Path(args.dir or os.getcwd()).expanduser().resolve()
    ws = parent / slug
    if (ws / MANIFEST).exists():
        raise LPError("%s is already a workspace. Use `lp status` there, or `lp sync-guide` to refresh .lp/." % ws)
    if ws.exists() and any(ws.iterdir()) and not args.force:
        raise LPError("%s exists and is not empty; pass --force to use it (existing files are kept)" % ws)
    for d in ("research", "brand/assets", "assets", "pages/" + page):
        (ws / d).mkdir(parents=True, exist_ok=True)
    if args.mode == "redesign":
        (ws / "audit" / "pages").mkdir(parents=True, exist_ok=True)
    m = {
        "schema": SCHEMA, "name": args.product, "slug": slug, "mode": args.mode, "url": args.url or None,
        "created": today().isoformat(), "skill_version": __version__, "stale_days": 90,
        "research": {str(n): new_state(n, status="skipped" if n == 0 and args.mode == "new" else "todo")
                     for n in PRODUCT_STEPS},
        "brand": new_state(10),
        "gates": {g: {"after_step": a, "what": w} for g, (a, w) in GATES.items()},
        "pages": {}, "copy_rules": default_rules(),
    }
    m["pages"][page] = new_page(m, page, url=args.url if args.mode == "redesign" else None)
    save(ws, m)
    ver = vendor(ws, SELF_ROOT)
    written, skipped = ([], []) if args.no_agent_files else write_agent_files(ws, m)
    it = next_item(ws, m)
    data = {"ok": True, "workspace": str(ws), "mode": args.mode, "page": page, "vendored_version": ver,
            "agent_files": written, "agent_files_skipped": skipped, "next": it}
    text = ["Created workspace %s (%s mode, first page: %s)" % (ws, args.mode, page),
            "Vendored guide, templates and CLI into %s/ (v%s)" % (VENDOR, ver)]
    if written:
        text.append("Wrote " + ", ".join(written))
    if skipped:
        text.append("Kept existing " + ", ".join(skipped))
    text += ["", "cd %s && lp next   (or: python3 .lp/lp.py next)" % ws, "", format_next(it)]
    return data, "\n".join(text), 0


def cmd_next(args):
    ws = workspace(args)
    m = load(ws)
    it = next_item(ws, m, args.page, args.force)
    it["workspace"] = str(ws)
    return it, format_next(it), 3 if it["status"] == "gate" else 0


def cmd_status(args):
    ws = workspace(args)
    m = load(ws)
    pages = [args.page] if args.page else list(m["pages"])
    for p in pages:
        if p not in m["pages"]:
            raise LPError("no page %r" % p)
    rows = []
    for n in sorted(STEPS):
        if n == 0 and m["mode"] == "new":
            continue
        prod = m["research"][str(n)]["status"] if n in PRODUCT_STEPS else (m["brand"]["status"] if n == 10 else "")
        cells = ["" if n in PRODUCT_STEPS else step_status(m, n, p) for p in pages]
        rows.append([str(n), STEPS[n]["title"], prod] + cells)
    for g, (after, what) in GATES.items():
        cells = []
        for p in pages:
            a = m["pages"][p]["approvals"].get(g)
            cells.append("approved by %s" % a["by"] if a else "pending")
        rows.append([g, "after step %d (%s)" % (after, what), ""] + cells)
    head = ["step", "title", "product"] + pages
    widths = [max(len(r[i]) for r in rows + [head]) for i in range(len(head))]
    fmt = lambda r: "  ".join(c.ljust(w) for c, w in zip(r, widths)).rstrip()
    stale = stale_list(ws, m)
    text = ["%s (%s mode)%s" % (m["name"], m["mode"], ", " + m["url"] if m.get("url") else ""), "",
            fmt(head), fmt(["-" * w for w in widths])] + [fmt(r) for r in rows]
    if stale:
        text += ["", "Stale research (older than %d days):" % m["stale_days"]] + \
                ["  %s: %s" % (s["file"], s["reason"]) for s in stale]
    nxt = next_item(ws, m)
    text += ["", format_next(nxt).splitlines()[0]]
    data = {"product": m["name"], "slug": m["slug"], "mode": m["mode"], "url": m.get("url"),
            "workspace": str(ws),
            "research": {k: v["status"] for k, v in m["research"].items()}, "brand": m["brand"]["status"],
            "pages": {p: {"steps": {str(n): step_status(m, n, p) for n in PAGE_STEPS},
                          "approvals": m["pages"][p]["approvals"],
                          "primary_keyword": page_keyword(ws, m, p)} for p in pages},
            "stale": stale, "next": nxt}
    return data, "\n".join(text), 0


def cmd_start(args):
    ws = workspace(args)
    m = load(ws)
    step = args.step
    page = resolve_page(m, args.page, step)
    if step == 0 and m["mode"] != "redesign":
        raise LPError("step 0 (audit) only applies to redesign mode")
    if step == 10 and page and m["brand"]["status"] == "done":
        raise LPError("step 10 is product-level and already done; page %s inherits brand/. "
                      "Use `lp redo 10` only if the brand itself changes." % page)
    miss = gates_missing(m, step, page)
    if miss:
        raise LPError("step %d needs %s approved for page %s first. A human runs: %s"
                      % (step, ", ".join(miss), page, approve_cmd(miss[0], page or "<page>")), 1)
    lay = ws_layout(ws)
    copied, kept = [], []
    for tname, out in STEPS[step]["templates"]:
        dst = ws / out.format(page=page)
        if dst.exists():
            kept.append(rel_to(dst, ws))
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(lay["templates"] / tname), str(dst))
        copied.append(rel_to(dst, ws))
    for d in {0: ["audit/pages"], 11: [P + "11-design", P + "build"], 10: ["brand/assets"]}.get(step, []):
        (ws / d.format(page=page)).mkdir(parents=True, exist_ok=True)
    note = ""
    if step_status(m, step, page) == "done":
        note = "Step %d is already done; use `lp redo %d` to reopen it." % (step, step)
    else:
        set_status(m, step, page, "in_progress")
        save(ws, m)
    it = describe(ws, m, step, page)
    it.update(copied=copied, kept=kept, ok=True)
    lines = ["Step %d (%s) %s%s" % (step, STEPS[step]["title"], "in progress" if not note else "done",
                                     " for page " + page if page else "")]
    lines += ["Copied template -> " + c for c in copied] + ["Kept existing " + k for k in kept]
    if note:
        lines.append(note)
    lines.append("Read the guide: " + it["guide"]["relative"])
    lines.append("When finished: " + it["commands"]["done"])
    return it, "\n".join(lines), 0


def cmd_done(args):
    ws = workspace(args)
    m = load(ws)
    step = args.step
    page = resolve_page(m, args.page, step)
    if step == 0 and m["mode"] != "redesign":
        raise LPError("step 0 (audit) only applies to redesign mode")
    miss = gates_missing(m, step, page)
    if miss:  # --force never bypasses a human gate
        raise LPError("step %d needs %s approved for page %s first. A human runs: %s"
                      % (step, ", ".join(miss), page, approve_cmd(miss[0], page or "<page>")), 1)
    probs = [] if args.force else validate(ws, m, step, page)
    where = " for page %s" % page if page else ""
    if probs:
        data = {"ok": False, "step": step, "page": page, "problems": probs}
        return data, "Step %d%s is not done yet:\n%s" % (step, where, "\n".join("  - " + p for p in probs)), 1
    set_status(m, step, page, "done")
    if args.force:
        state(m, step, page)["forced"] = True
    if step == 7:
        m["pages"][page]["primary_keyword"] = keyword_in_file(ws, page) or m["pages"][page]["primary_keyword"]
    save(ws, m)
    it = next_item(ws, m, page if page else None)
    data = {"ok": True, "step": step, "page": page, "forced": bool(args.force), "next": it}
    return data, "Step %d (%s) done%s%s.\n\n%s" % (step, STEPS[step]["title"], where,
                                                   " (forced, validation skipped)" if args.force else "",
                                                   format_next(it)), 0


def cmd_approve(args):
    ws = workspace(args)
    m = load(ws)
    gate = args.gate
    if not args.by or not args.by.strip():
        raise LPError("--by \"<name of the human approving>\" is required")
    pages = list(m["pages"])
    page = args.page or (pages[0] if len(pages) == 1 else None)
    if not page or page not in m["pages"]:
        raise LPError("pass --page (one of: %s)" % ", ".join(pages))
    after = GATES[gate][0]
    if not is_finished(m, after, page):
        raise LPError("%s comes after step %d, which is not done for page %s" % (gate, after, page), 1)
    rec = {"by": args.by.strip(), "at": dt.datetime.now().replace(microsecond=0).isoformat(), "note": args.note or ""}
    m["pages"][page]["approvals"][gate] = rec
    save(ws, m)
    it = next_item(ws, m, page)
    return ({"ok": True, "gate": gate, "page": page, "approval": rec, "next": it},
            "%s approved for page %s by %s.\n\n%s" % (gate, page, rec["by"], format_next(it)), 0)


def cmd_redo(args):
    ws = workspace(args)
    m = load(ws)
    step = args.step
    page = resolve_page(m, args.page, step)
    if step == 0 and m["mode"] != "redesign":
        raise LPError("step 0 (audit) only applies to redesign mode")
    set_status(m, step, page, "in_progress")
    revoked = []
    if page and step != 10:
        for g, (after, _) in GATES.items():
            if step <= after and m["pages"][page]["approvals"].pop(g, None):
                revoked.append(g)
    save(ws, m)
    lines = ["Step %d (%s) reopened%s." % (step, STEPS[step]["title"], " for page %s" % page if page else "")]
    if revoked:
        lines.append("Revoked %s for page %s: the approved work changed, so a human must approve again."
                     % (", ".join(revoked), page))
    if step == 10:
        lines.append("The brand is shared: re-check every built page after changing it.")
    if step in PRODUCT_STEPS:
        lines.append("Research is product-level: `lp next` points here before any page work until it is done again.")
    return {"ok": True, "step": step, "page": page, "revoked": revoked}, "\n".join(lines), 0


def cmd_page_add(args):
    ws = workspace(args)
    m = load(ws)
    slug = slugify(args.slug)
    if not slug or slug != args.slug.strip().lower():
        raise LPError("page slug must be lowercase letters, digits and dashes (try %r)" % (slug or "page"))
    if slug in m["pages"]:
        raise LPError("page %r already exists" % slug)
    if args.keyword:
        clash = [p for p in m["pages"] if norm_kw(page_keyword(ws, m, p)) == norm_kw(args.keyword)]
        if clash:
            raise LPError("keyword %r is already the primary keyword of page %s (cannibalization)"
                          % (args.keyword, ", ".join(clash)), 1)
    m["pages"][slug] = new_page(m, slug, args.keyword, args.url)
    (ws / "pages" / slug).mkdir(parents=True, exist_ok=True)
    save(ws, m)
    it = next_item(ws, m, slug)
    inherited = m["pages"][slug]["steps"]["10"]["status"] == "inherited"
    text = "Added page %s (starts at step 7; research reused%s).\n\n%s" % (
        slug, ", brand inherited" if inherited else "", format_next(it))
    return {"ok": True, "page": slug, "start_step": 7, "brand_inherited": inherited,
            "manifest": m["pages"][slug], "next": it}, text, 0


def cmd_page_list(args):
    ws = workspace(args)
    m = load(ws)
    rows = []
    for p, d in m["pages"].items():
        n = next_for_page(m, p)
        nxt = {"step": "step %s" % n.get("step"), "gate": "waiting on %s" % n.get("gate"), "done": "done"}[n["kind"]]
        rows.append({"page": p, "primary_keyword": page_keyword(ws, m, p), "url": d.get("url"), "next": nxt})
    text = "\n".join("%-16s %-32s %s" % (r["page"], r["primary_keyword"] or "(no keyword yet)", r["next"])
                     for r in rows) or "No pages."
    return {"pages": rows}, text, 0


def stale_list(ws, m):
    out = []
    limit = m.get("stale_days", 90)
    for n in range(1, 7):
        rel = RF[n]
        if not (ws / rel).is_file():
            continue
        d, err = frontmatter_date(read(ws / rel))
        if d is None:
            if m["research"][str(n)]["status"] == "done":
                out.append({"file": rel, "step": n, "verified": None, "reason": err})
            continue
        age = (today() - d).days
        if age > limit:
            out.append({"file": rel, "step": n, "verified": d.isoformat(), "age_days": age,
                        "reason": "verified %s, %d days ago" % (d, age)})
    return out


def cmd_stale(args):
    ws = workspace(args)
    m = load(ws)
    s = stale_list(ws, m)
    if not s:
        return {"stale": [], "stale_days": m["stale_days"]}, "No stale research (limit %d days)." % m["stale_days"], 0
    text = ["Stale research (older than %d days). Re-check the facts, update `verified:`, and use "
            "`lp redo N` if anything changed:" % m["stale_days"]]
    text += ["  step %d  %s: %s" % (x["step"], x["file"], x["reason"]) for x in s]
    return {"stale": s, "stale_days": m["stale_days"]}, "\n".join(text), 1


def cmd_check(args):
    ws = None
    try:
        ws = workspace(args)
    except LPError:
        if not args.files:
            raise
    m = load(ws) if ws else None
    rules = m["copy_rules"] if m else default_rules()
    findings = []
    if args.files:
        for f in args.files:
            findings += check_file(Path(f).expanduser().resolve(), rules, ws)
        if m:
            findings += cannibalization(ws, m)
    else:
        pages = [args.page] if args.page else list(m["pages"])
        for p in pages:
            if p not in m["pages"]:
                raise LPError("no page %r" % p)
            files = page_files(ws, p)
            if not files:
                findings.append(finding("info", P.format(page=p), "nothing", "no copy or HTML files yet"))
            for f in files:
                findings += check_file(f, rules, ws)
        findings += cannibalization(ws, m)
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in ("error", "warn", "info")}
    order = {"error": 0, "warn": 1, "info": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["file"]))
    lines = ["%-5s %s: %s: %s" % (f["severity"], f["file"], f["rule"], f["message"]) for f in findings]
    lines.append("%d error(s), %d warning(s), %d info" % (counts["error"], counts["warn"], counts["info"]))
    return ({"ok": counts["error"] == 0, "findings": findings, "counts": counts}, "\n".join(lines),
            1 if counts["error"] else 0)


def cmd_sync_guide(args):
    ws = workspace(args)
    m = load(ws)
    src = installed_skill()
    if not src:
        raise LPError("no installed skill found (set LP_SKILL_HOME or install with install.sh); "
                      "the vendored copy in .lp/ keeps working as is")
    old = (read(ws / VENDOR / "VERSION").strip() if (ws / VENDOR / "VERSION").is_file() else None)
    ver = vendor(ws, src)
    m["skill_version"] = ver
    save(ws, m)
    return ({"ok": True, "source": str(src), "from_version": old, "to_version": ver},
            "Refreshed %s/ from %s (%s -> %s). Your files outside %s/ were not touched."
            % (VENDOR, src, old, ver, VENDOR), 0)


def cmd_doctor(args):
    checks = []

    def add(name, ok, detail):
        checks.append({"check": name, "ok": ok, "detail": detail})

    add("python", sys.version_info >= (3, 8), sys.version.split()[0])
    add("cli", True, "%s (v%s)" % (Path(__file__).resolve(), __version__))
    inst = installed_skill()
    add("installed skill", True, str(inst) if inst else "not found (fine if you only use the vendored .lp/)")
    ws = find_workspace(getattr(args, "dir", None) or os.environ.get("LP_WORKSPACE") or os.getcwd())
    add("workspace", ws is not None, str(ws) if ws else "no lp.json here or in any parent")
    if ws:
        try:
            m = json.loads(read(ws / MANIFEST))
            probs = manifest_problems(m)
            add("manifest", not probs, "valid (schema %s)" % m.get("schema") if not probs else "; ".join(probs))
        except ValueError as e:
            add("manifest", False, "not valid JSON: %s" % e)
        vfile = ws / VENDOR / "VERSION"
        vver = read(vfile).strip() if vfile.is_file() else None
        add("vendored guide", bool(vver) and (ws / VENDOR / "guide").is_dir(),
            "v%s" % vver if vver else ".lp/ missing; run `lp sync-guide`")
        if inst and vver:
            iver = script_version(inst / "scripts" / "lp.py")
            add("versions", vver == iver, "vendored v%s, installed v%s%s"
                % (vver, iver, "" if vver == iver else "; run `lp sync-guide` to update"))
    ok = all(c["ok"] for c in checks if c["check"] != "versions")
    text = "\n".join("%-4s %-15s %s" % ("ok" if c["ok"] else "FAIL", c["check"], c["detail"]) for c in checks)
    return {"ok": ok, "checks": checks}, text, 0 if ok else 1


# ----------------------------------------------------------------- argparse

def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="machine-readable output")
    common.add_argument("--dir", default=argparse.SUPPRESS,
                        help="workspace directory (default: walk up from cwd, or $LP_WORKSPACE)")
    pagearg = argparse.ArgumentParser(add_help=False)
    pagearg.add_argument("--page", help="page slug (default: the only page, or the one in progress)")

    ap = argparse.ArgumentParser(prog="lp", description="Landing page system: research, write, design, ship "
                                 "and iterate landing pages, one step at a time. Agents: run `lp next`.")
    ap.add_argument("--version", action="version", version="lp %s" % __version__)
    ap.add_argument("--json", action="store_true", default=False, help="machine-readable output")
    ap.add_argument("--dir", default=None, help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest="cmd", metavar="command")

    p = sub.add_parser("init", parents=[common], help="create a workspace for a product")
    p.add_argument("product", help="product name, e.g. \"Acme Plumbing\"")
    p.add_argument("--mode", choices=["new", "redesign"], default="new")
    p.add_argument("--url", help="live site URL (required for redesign)")
    p.add_argument("--page", default="home", help="first page slug (default: home)")
    p.add_argument("--no-agent-files", action="store_true", help="skip AGENTS.md, CLAUDE.md, GEMINI.md")
    p.add_argument("--force", action="store_true", help="allow a non-empty target folder (files are kept)")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("status", parents=[common, pagearg], help="steps x pages, gates, stale research")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("next", parents=[common, pagearg], help="the next actionable step (agent entry point)")
    p.add_argument("--force", action="store_true", help="skip ahead of unfinished product research")
    p.set_defaults(func=cmd_next)

    for name, func, hlp in (("start", cmd_start, "mark a step in progress and copy its template"),
                            ("done", cmd_done, "validate a step's outputs and mark it done"),
                            ("redo", cmd_redo, "reopen a step")):
        p = sub.add_parser(name, parents=[common, pagearg], help=hlp)
        p.add_argument("step", type=int, choices=sorted(STEPS), metavar="step", help="step number 0-16")
        if name == "done":
            p.add_argument("--force", action="store_true", help="skip output validation (never skips gates)")
        p.set_defaults(func=func)

    p = sub.add_parser("approve", parents=[common, pagearg], help="record a HUMAN gate approval")
    p.add_argument("gate", choices=list(GATES))
    p.add_argument("--by", required=True, help="name of the human approving")
    p.add_argument("--note", help="optional note")
    p.set_defaults(func=cmd_approve)

    p = sub.add_parser("page", parents=[common], help="add or list pages")
    psub = p.add_subparsers(dest="page_cmd", metavar="add|list")
    psub.required = True
    pa = psub.add_parser("add", parents=[common], help="add a page; it starts at step 7")
    pa.add_argument("slug")
    pa.add_argument("--keyword", help="primary keyword from research/06-seo.md")
    pa.add_argument("--url", "--from-url", dest="url", help="current URL of the page (redesigns)")
    pa.set_defaults(func=cmd_page_add)
    pl = psub.add_parser("list", parents=[common], help="list pages")
    pl.set_defaults(func=cmd_page_list)

    p = sub.add_parser("stale", parents=[common], help="research older than stale_days (exit 1 if any)")
    p.set_defaults(func=cmd_stale)

    p = sub.add_parser("check", parents=[common, pagearg], help="copy and HTML lint (exit 1 on errors)")
    p.add_argument("files", nargs="*", help="files to check (default: every page's copy and HTML)")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("sync-guide", parents=[common], help="refresh vendored .lp/ from the installed skill")
    p.set_defaults(func=cmd_sync_guide)

    p = sub.add_parser("doctor", parents=[common], help="check python, workspace, manifest and versions")
    p.set_defaults(func=cmd_doctor)
    return ap


def main(argv=None):
    ap = build_parser()
    args = ap.parse_args(argv)
    if not getattr(args, "func", None):
        ap.print_help()
        return 2
    as_json = getattr(args, "json", False)
    try:
        data, text, code = args.func(args)
    except LPError as e:
        if as_json:
            print(json.dumps(dict({"ok": False, "error": str(e)}, **e.data), indent=2))
        else:
            sys.stderr.write("lp: %s\n" % e)
        return e.code
    print(json.dumps(data, indent=2) if as_json else text)
    return code


if __name__ == "__main__":
    sys.exit(main())
