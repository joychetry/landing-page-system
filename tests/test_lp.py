"""Tests for scripts/lp.py. Standard library only: python3 -m unittest discover -s tests -v"""

import datetime as dt
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LP = ROOT / "scripts" / "lp.py"
FIX = Path(__file__).resolve().parent / "fixtures"
SAMPLE = FIX / "sample"
TODAY = dt.date.today().isoformat()

PAGE_FILES = {
    7: ["07-structure.md"], 8: ["08-copy.md"], 9: ["09-wireframe.html"],
    11: ["11-design/direction-a.html", "11-design/direction-b.html", "build/index.html"],
    12: ["12-visuals.md"], 13: ["13-polish.md"], 14: ["14-checks.md"], 15: ["15-ship.md"], 16: ["16-measure.md"],
}
RESEARCH = {1: "01-goal-offer.md", 2: "02-customers.md", 3: "03-competitors.md",
            4: "04-proof.md", 5: "05-brand-story.md", 6: "06-seo.md"}
GATE_AFTER = {9: "gate1", 11: "gate2", 14: "gate3"}


def load_module():
    spec = importlib.util.spec_from_file_location("lp", str(LP))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class LPTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="lp-test-"))
        self.home = self.tmp / "home"  # empty HOME so no installed skill is picked up by accident
        self.home.mkdir()
        self.addCleanup(shutil.rmtree, str(self.tmp), True)

    def env(self, **extra):
        env = {k: v for k, v in os.environ.items() if not k.startswith("LP_")}
        env["HOME"] = str(self.home)
        env.update(extra)
        return env

    def run_lp(self, *args, cwd=None, script=LP, code=0, env=None):
        p = subprocess.run([sys.executable, str(script)] + [str(a) for a in args], cwd=str(cwd or self.tmp),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                           env=env or self.env())
        if code is not None:
            self.assertEqual(p.returncode, code, "lp %s\nstdout:\n%s\nstderr:\n%s" % (" ".join(map(str, args)),
                                                                                    p.stdout, p.stderr))
        return p

    def lp_json(self, *args, **kw):
        p = self.run_lp(*(list(args) + ["--json"]), **kw)
        return json.loads(p.stdout)

    def init(self, name="Tidewater Plumbing", *extra):
        self.run_lp("init", name, "--dir", self.tmp, *extra)
        return self.tmp / re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    def manifest(self, ws):
        return json.loads((ws / "lp.json").read_text())

    def put(self, src, dst):
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text()
        text = re.sub(r"^verified: \S+", "verified: " + TODAY, text, flags=re.M)
        dst.write_text(text)

    def do_research(self, ws, steps=range(1, 7)):
        for n in steps:
            self.run_lp("start", n, cwd=ws)
            self.put(SAMPLE / "research" / RESEARCH[n], ws / "research" / RESEARCH[n])
            self.run_lp("done", n, cwd=ws)

    def do_page_step(self, ws, page, n, keyword=None):
        self.run_lp("start", n, "--page", page, cwd=ws)
        if n == 10:
            for f in ("brand.md", "tokens.css"):
                self.put(SAMPLE / "brand" / f, ws / "brand" / f)
        for f in PAGE_FILES.get(n, []):
            self.put(SAMPLE / "pages" / "home" / f, ws / "pages" / page / f)
        if keyword and n == 7:
            p = ws / "pages" / page / "07-structure.md"
            p.write_text(re.sub(r"^Primary keyword:.*$", "Primary keyword: " + keyword, p.read_text(), flags=re.M))
        self.run_lp("done", n, "--page", page, cwd=ws)

    def walk_page(self, ws, page, upto, keyword=None, approve=True):
        """Run page steps in lp next order up to `upto`, approving gates as the human would."""
        while True:
            it = self.lp_json("next", "--page", page, cwd=ws, code=None)
            if it["status"] == "gate":
                if not approve:
                    return it
                self.run_lp("approve", it["gate"], "--page", page, "--by", "Test Owner", cwd=ws)
                continue
            if it["status"] == "done" or it["step"] > upto:
                return it
            self.do_page_step(ws, page, it["step"], keyword)


class TestInit(LPTestCase):
    def test_init_new_creates_self_contained_workspace(self):
        ws = self.init()
        for rel in ("lp.json", "AGENTS.md", "CLAUDE.md", "GEMINI.md", ".lp/lp.py", ".lp/VERSION",
                    ".lp/guide/method-overview.md", ".lp/templates/08-copy.md", "research", "brand", "assets",
                    "pages/home"):
            self.assertTrue((ws / rel).exists(), rel)
        self.assertEqual(len(list((ws / ".lp/guide/steps").glob("*.md"))), 17)
        self.assertEqual(len(list((ws / ".lp/guide/checklists").glob("*.md"))), 5)
        self.assertIn("@AGENTS.md", (ws / "CLAUDE.md").read_text())
        self.assertIn("@AGENTS.md", (ws / "GEMINI.md").read_text())
        agents = (ws / "AGENTS.md").read_text()
        self.assertIn("Tidewater Plumbing", agents)
        self.assertNotIn("{{", agents)
        m = self.manifest(ws)
        self.assertEqual(m["schema"], 1)
        self.assertEqual(m["mode"], "new")
        self.assertEqual(m["research"]["0"]["status"], "skipped")
        self.assertEqual(m["stale_days"], 90)
        self.assertIn("unlock", m["copy_rules"]["banned_phrases"])
        self.assertEqual(sorted(m["pages"]["home"]["steps"], key=int), [str(n) for n in range(7, 17)])
        it = self.lp_json("next", cwd=ws)
        self.assertEqual((it["status"], it["step"], it["page"]), ("step", 1, "product"))
        self.assertFalse((ws / "audit").exists())

    def test_init_redesign(self):
        self.run_lp("init", "Old Site", "--mode", "redesign", "--dir", self.tmp, code=2)  # --url required
        ws = self.init("Old Site", "--mode", "redesign", "--url", "https://old.example.com")
        m = self.manifest(ws)
        self.assertEqual((m["mode"], m["url"]), ("redesign", "https://old.example.com"))
        self.assertEqual(m["pages"]["home"]["url"], "https://old.example.com")
        self.assertTrue((ws / "audit/pages").is_dir())
        it = self.lp_json("next", cwd=ws)
        self.assertEqual(it["step"], 0)
        self.assertEqual(it["site_url"], "https://old.example.com")
        self.run_lp("start", 0, cwd=ws)
        self.assertTrue((ws / "audit/site-audit.md").is_file())
        self.assertTrue((ws / "audit/url-map.csv").is_file())
        self.run_lp("done", 0, cwd=ws, code=1)
        for rel in ("audit/site-audit.md", "audit/url-map.csv", "audit/pages/home.md"):
            self.put(SAMPLE / rel, ws / rel)
        self.run_lp("done", 0, cwd=ws)
        self.assertEqual(self.lp_json("next", cwd=ws)["step"], 1)

    def test_init_refuses_existing_and_skips_agent_files(self):
        ws = self.init()
        self.run_lp("init", "Tidewater Plumbing", "--dir", self.tmp, code=2)
        self.run_lp("init", "Tidewater Plumbing", "--dir", self.tmp, "--force", code=2)  # never clobbers lp.json
        self.run_lp("init", "Bare", "--dir", self.tmp, "--no-agent-files", "--page", "landing")
        bare = self.tmp / "bare"
        self.assertFalse((bare / "AGENTS.md").exists())
        self.assertIn("landing", self.manifest(bare)["pages"])
        self.assertTrue(ws.is_dir())

    def test_init_force_keeps_existing_files(self):
        target = self.tmp / "kept"
        target.mkdir()
        (target / "AGENTS.md").write_text("mine\n")
        self.run_lp("init", "Kept", "--dir", self.tmp, code=2)
        self.run_lp("init", "Kept", "--dir", self.tmp, "--force")
        self.assertEqual((target / "AGENTS.md").read_text(), "mine\n")
        self.assertTrue((target / "CLAUDE.md").exists())


class TestFlow(LPTestCase):
    def test_next_ordering_research_first(self):
        ws = self.init()
        for n in range(1, 7):
            self.assertEqual(self.lp_json("next", cwd=ws)["step"], n)
            it = self.lp_json("next", "--page", "home", cwd=ws)
            self.assertEqual((it["step"], it["page"]), (n, "product"))
            self.assertIn("note", it)
            forced = self.lp_json("next", "--page", "home", "--force", cwd=ws)
            self.assertEqual(forced["step"], 7)
            self.do_research(ws, [n])
        it = self.lp_json("next", cwd=ws)
        self.assertEqual((it["step"], it["page"]), (7, "home"))
        self.assertEqual(it["outputs"][0]["relative"], "pages/home/07-structure.md")
        self.assertTrue(it["guide"]["relative"].endswith("steps/07-page-structure.md"))
        self.assertTrue(it["done_criteria"])
        self.assertTrue(all(i["exists"] for i in it["inputs"]))

    def test_gates_block_until_human_approves(self):
        ws = self.init()
        self.do_research(ws)
        for n in (7, 8, 9):
            self.do_page_step(ws, "home", n)
        p = self.run_lp("next", "--page", "home", cwd=ws, code=3)
        self.assertIn('lp approve gate1 --page home --by "<your name>"', p.stdout)
        self.assertIn("STOP", p.stdout)
        it = self.lp_json("next", cwd=ws, code=3)
        self.assertEqual((it["status"], it["gate"]), ("gate", "gate1"))
        self.run_lp("start", 10, "--page", "home", cwd=ws, code=1)
        self.run_lp("start", 11, "--page", "home", cwd=ws, code=1)
        self.run_lp("done", 11, "--page", "home", "--force", cwd=ws, code=1)  # --force never skips a gate
        self.run_lp("approve", "gate2", "--page", "home", "--by", "X", cwd=ws, code=1)  # step 11 not done
        self.run_lp("approve", "gate1", "--page", "home", "--by", "  ", cwd=ws, code=2)
        self.run_lp("approve", "gate1", "--page", "home", cwd=ws, code=2)  # --by is required
        a = self.lp_json("approve", "gate1", "--page", "home", "--by", "Dana Owner", "--note", "ok", cwd=ws)
        self.assertEqual(a["approval"]["by"], "Dana Owner")
        self.assertEqual(self.lp_json("next", cwd=ws)["step"], 10)
        self.do_page_step(ws, "home", 10)
        self.do_page_step(ws, "home", 11)
        self.assertEqual(self.lp_json("next", cwd=ws, code=3)["gate"], "gate2")
        self.run_lp("approve", "gate2", "--page", "home", "--by", "Dana Owner", cwd=ws)
        for n in (12, 13, 14):
            self.do_page_step(ws, "home", n)
        self.assertEqual(self.lp_json("next", cwd=ws, code=3)["gate"], "gate3")
        self.run_lp("start", 15, "--page", "home", cwd=ws, code=1)
        self.run_lp("approve", "gate3", "--page", "home", "--by", "Dana Owner", cwd=ws)
        self.do_page_step(ws, "home", 15)
        self.do_page_step(ws, "home", 16)
        it = self.lp_json("next", cwd=ws)
        self.assertEqual(it["status"], "done")
        self.assertIn("lp page add", it["message"])
        st = self.lp_json("status", cwd=ws)
        self.assertTrue(all(v == "done" for v in st["pages"]["home"]["steps"].values()))
        self.assertEqual(set(st["pages"]["home"]["approvals"]), {"gate1", "gate2", "gate3"})

    def test_second_page_reuses_research_and_inherits_brand(self):
        ws = self.init()
        self.do_research(ws)
        self.walk_page(ws, "home", 11)
        added = self.lp_json("page", "add", "pricing", "--keyword", "plumber prices harbor city", cwd=ws)
        self.assertTrue(added["brand_inherited"])
        self.assertEqual(added["manifest"]["steps"]["10"]["status"], "inherited")
        it = self.lp_json("next", "--page", "pricing", cwd=ws)
        self.assertEqual((it["step"], it["page"]), (7, "pricing"))
        last = self.walk_page(ws, "pricing", 11, keyword="plumber prices harbor city", approve=False)
        self.assertEqual(last["gate"], "gate1")
        self.run_lp("approve", "gate1", "--page", "pricing", "--by", "Dana Owner", cwd=ws)
        self.assertEqual(self.lp_json("next", "--page", "pricing", cwd=ws)["step"], 11)  # step 10 inherited
        self.run_lp("start", 10, "--page", "pricing", cwd=ws, code=2)
        st = self.lp_json("status", cwd=ws)
        self.assertEqual(st["pages"]["pricing"]["steps"]["10"], "inherited")
        self.assertEqual(st["pages"]["home"]["steps"]["10"], "done")
        names = [r["page"] for r in self.lp_json("page", "list", cwd=ws)["pages"]]
        self.assertEqual(names, ["home", "pricing"])
        self.run_lp("page", "add", "Bad Slug", cwd=ws, code=2)
        self.run_lp("page", "add", "pricing", cwd=ws, code=2)

    def test_research_redo_sends_pages_back_to_research(self):
        ws = self.init()
        self.do_research(ws)
        self.walk_page(ws, "home", 8)
        self.run_lp("redo", 2, cwd=ws)
        self.assertEqual(self.lp_json("next", "--page", "home", cwd=ws)["step"], 2)

    def test_redo_page_step_revokes_later_gates(self):
        ws = self.init()
        self.do_research(ws)
        self.walk_page(ws, "home", 12)
        r = self.lp_json("redo", 8, "--page", "home", cwd=ws)
        self.assertEqual(sorted(r["revoked"]), ["gate1", "gate2"])
        self.assertEqual(self.lp_json("next", cwd=ws)["step"], 8)
        r = self.lp_json("redo", 16, "--page", "home", cwd=ws)
        self.assertEqual(r["revoked"], [])

    def test_several_pages_need_page_flag_when_ambiguous(self):
        ws = self.init()
        self.do_research(ws)
        self.run_lp("page", "add", "pricing", cwd=ws)
        self.run_lp("start", 7, cwd=ws, code=2)
        self.run_lp("start", 7, "--page", "pricing", cwd=ws)
        self.run_lp("done", 7, cwd=ws, code=1)  # resolves to pricing (in progress), template untouched

    def test_redesign_ship_needs_redirect_map(self):
        ws = self.init("Old Site", "--mode", "redesign", "--url", "https://old.example.com")
        self.run_lp("start", 0, cwd=ws)
        for rel in ("audit/site-audit.md", "audit/pages/home.md"):
            self.put(SAMPLE / rel, ws / rel)
        (ws / "audit/url-map.csv").write_text("old_url,new_url,action,reason,clicks_90d,backlinks\n")
        self.run_lp("done", 0, cwd=ws, code=1)
        self.put(SAMPLE / "audit/url-map.csv", ws / "audit/url-map.csv")
        self.run_lp("done", 0, cwd=ws)
        self.do_research(ws)
        self.walk_page(ws, "home", 14)
        self.run_lp("approve", "gate3", "--page", "home", "--by", "Owner", cwd=ws)
        self.run_lp("start", 15, "--page", "home", cwd=ws)
        self.put(SAMPLE / "pages/home/15-ship.md", ws / "pages/home/15-ship.md")
        (ws / "audit/url-map.csv").write_text("old_url,new_url,action,reason,clicks_90d,backlinks\n")
        p = self.run_lp("done", 15, "--page", "home", cwd=ws, code=1)
        self.assertIn("redirect map", p.stdout)


class TestDoneValidation(LPTestCase):
    def setUp(self):
        super().setUp()
        self.ws = self.init()

    def test_rejects_untouched_template(self):
        self.run_lp("start", 1, cwd=self.ws)
        p = self.run_lp("done", 1, cwd=self.ws, code=1)
        self.assertIn("untouched template", p.stdout)
        self.assertIn("placeholder", p.stdout)
        res = self.lp_json("done", 1, cwd=self.ws, code=1)
        self.assertFalse(res["ok"])
        self.assertTrue(res["problems"])
        self.assertEqual(self.manifest(self.ws)["research"]["1"]["status"], "in_progress")

    def test_start_never_overwrites(self):
        (self.ws / "research").mkdir(exist_ok=True)
        (self.ws / "research/01-goal-offer.md").write_text("my notes\n")
        res = self.lp_json("start", 1, cwd=self.ws)
        self.assertEqual(res["copied"], [])
        self.assertEqual((self.ws / "research/01-goal-offer.md").read_text(), "my notes\n")

    def test_requires_verified_frontmatter_and_headings(self):
        self.run_lp("start", 1, cwd=self.ws)
        dst = self.ws / "research/01-goal-offer.md"
        self.put(SAMPLE / "research/01-goal-offer.md", dst)
        dst.write_text(dst.read_text().replace("verified: " + TODAY, "verified: 2999-01-01"))
        self.assertIn("in the future", self.run_lp("done", 1, cwd=self.ws, code=1).stdout)
        dst.write_text(re.sub(r"\A---\n.*?\n---\n", "", dst.read_text(), flags=re.S))
        self.assertIn("frontmatter", self.run_lp("done", 1, cwd=self.ws, code=1).stdout)
        self.put(SAMPLE / "research/01-goal-offer.md", dst)
        dst.write_text(dst.read_text().replace("## Traffic", "## Visitors"))
        self.assertIn("## Traffic", self.run_lp("done", 1, cwd=self.ws, code=1).stdout)
        self.put(SAMPLE / "research/01-goal-offer.md", dst)
        self.run_lp("done", 1, cwd=self.ws)

    def test_proof_needs_gaps_and_sources(self):
        self.do_research(self.ws, [1, 2, 3])
        self.run_lp("start", 4, cwd=self.ws)
        dst = self.ws / "research/04-proof.md"
        self.put(SAMPLE / "research/04-proof.md", dst)
        dst.write_text(dst.read_text().split("## Gaps")[0])
        self.assertIn("## Gaps", self.run_lp("done", 4, cwd=self.ws, code=1).stdout)

    def test_customer_research_needs_source_markers(self):
        self.do_research(self.ws, [1])
        self.run_lp("start", 2, cwd=self.ws)
        dst = self.ws / "research/02-customers.md"
        self.put(SAMPLE / "research/02-customers.md", dst)
        text = re.sub(r"https?://\S+|provided by owner, \d{4}-\d{2}-\d{2}", "a forum", dst.read_text())
        dst.write_text(text)
        self.assertIn("source markers", self.run_lp("done", 2, cwd=self.ws, code=1).stdout)

    def test_force_skips_validation(self):
        self.run_lp("start", 1, cwd=self.ws)
        res = self.lp_json("done", 1, "--force", cwd=self.ws)
        self.assertTrue(res["forced"])
        self.assertTrue(self.manifest(self.ws)["research"]["1"]["forced"])

    def test_page_specific_rules(self):
        self.do_research(self.ws)
        # step 7 needs at least 4 feature definitions
        self.run_lp("start", 7, "--page", "home", cwd=self.ws)
        dst = self.ws / "pages/home/07-structure.md"
        self.put(SAMPLE / "pages/home/07-structure.md", dst)
        dst.write_text(re.sub(r"^\| F[34] \|.*\n", "", dst.read_text(), flags=re.M))
        self.assertIn("defines 2 features", self.run_lp("done", 7, "--page", "home", cwd=self.ws, code=1).stdout)
        self.do_page_step(self.ws, "home", 7)
        self.assertEqual(self.manifest(self.ws)["pages"]["home"]["primary_keyword"], "same day plumber harbor city")
        # step 8 runs the copy lint
        self.run_lp("start", 8, "--page", "home", cwd=self.ws)
        dst = self.ws / "pages/home/08-copy.md"
        self.put(SAMPLE / "pages/home/08-copy.md", dst)
        dst.write_text(dst.read_text().replace("Book online in two minutes.", "Unlock seamless booking."))
        self.assertIn("banned-phrase", self.run_lp("done", 8, "--page", "home", cwd=self.ws, code=1).stdout)
        # value props need details, and there must be enough of them and enough FAQ
        dst.write_text(dst.read_text().split("### Value prop 4")[0].replace("**Details:**", "", 1)
                       + "## How it works\n\n" + dst.read_text().split("## How it works")[1].split("**Q:** Can")[0]
                       + "## Closer" + dst.read_text().split("## Closer")[1])
        out = self.run_lp("done", 8, "--page", "home", cwd=self.ws, code=1).stdout
        for msg in ("3 value prop blocks", "without a `**Details:**`", "2 FAQ questions"):
            self.assertIn(msg, out)
        self.put(SAMPLE / "pages/home/08-copy.md", dst)
        self.run_lp("done", 8, "--page", "home", cwd=self.ws)
        # step 9 needs exactly one h1
        self.run_lp("start", 9, "--page", "home", cwd=self.ws)
        dst = self.ws / "pages/home/09-wireframe.html"
        self.put(SAMPLE / "pages/home/09-wireframe.html", dst)
        dst.write_text(dst.read_text().replace("<h2>", "<h1>").replace("</h2>", "</h1>"))
        self.assertIn("exactly one <h1>", self.run_lp("done", 9, "--page", "home", cwd=self.ws, code=1).stdout)
        # a short wireframe that drops feature sections fails
        good = (SAMPLE / "pages/home/09-wireframe.html").read_text()
        dst.write_text(re.sub(r'<section id="value-[234]">.*?</section>\n', "", good, flags=re.S))
        out = self.run_lp("done", 9, "--page", "home", cwd=self.ws, code=1).stdout
        for msg in ("7 <section>s but 07-structure.md plans 10", "1 feature sections", "words of visible copy"):
            self.assertIn(msg, out)
        self.put(SAMPLE / "pages/home/09-wireframe.html", dst)
        self.run_lp("done", 9, "--page", "home", cwd=self.ws)
        self.run_lp("approve", "gate1", "--page", "home", "--by", "Owner", cwd=self.ws)
        self.do_page_step(self.ws, "home", 10)
        # step 11 needs two directions
        self.run_lp("start", 11, "--page", "home", cwd=self.ws)
        self.put(SAMPLE / "pages/home/build/index.html", self.ws / "pages/home/build/index.html")
        self.assertIn("hero directions", self.run_lp("done", 11, "--page", "home", cwd=self.ws, code=1).stdout)
        self.do_page_step(self.ws, "home", 11)
        self.run_lp("approve", "gate2", "--page", "home", "--by", "Owner", cwd=self.ws)
        self.do_page_step(self.ws, "home", 12)
        # step 13 needs a reduced-motion rule when the page animates
        self.run_lp("start", 13, "--page", "home", cwd=self.ws)
        self.put(SAMPLE / "pages/home/13-polish.md", self.ws / "pages/home/13-polish.md")
        idx = self.ws / "pages/home/build/index.html"
        good = idx.read_text()
        idx.write_text(good.replace("prefers-reduced-motion", "min-width: 1px"))
        self.assertIn("prefers-reduced-motion", self.run_lp("done", 13, "--page", "home", cwd=self.ws, code=1).stdout)
        idx.write_text(good)
        self.run_lp("done", 13, "--page", "home", cwd=self.ws)
        # step 14 re-runs lp check on the page
        self.run_lp("start", 14, "--page", "home", cwd=self.ws)
        self.put(SAMPLE / "pages/home/14-checks.md", self.ws / "pages/home/14-checks.md")
        idx.write_text(good.replace(' alt="Tidewater plumber at the open van with the parts racks visible"', ""))
        self.assertIn("img-alt", self.run_lp("done", 14, "--page", "home", cwd=self.ws, code=1).stdout)
        idx.write_text(good)
        self.run_lp("done", 14, "--page", "home", cwd=self.ws)


class TestStale(LPTestCase):
    def test_stale_detection(self):
        ws = self.init()
        self.do_research(ws, [1, 2])
        self.assertEqual(self.lp_json("stale", cwd=ws)["stale"], [])
        old = (dt.date.today() - dt.timedelta(days=200)).isoformat()
        f = ws / "research/02-customers.md"
        f.write_text(f.read_text().replace("verified: " + TODAY, "verified: " + old))
        res = self.lp_json("stale", cwd=ws, code=1)
        self.assertEqual([s["file"] for s in res["stale"]], ["research/02-customers.md"])
        self.assertEqual(res["stale"][0]["age_days"], 200)
        self.assertIn("02-customers.md", self.run_lp("status", cwd=ws).stdout)
        m = json.loads((ws / "lp.json").read_text())
        m["stale_days"] = 365
        (ws / "lp.json").write_text(json.dumps(m))
        self.run_lp("stale", cwd=ws)


class TestCheck(LPTestCase):
    def findings(self, *files, code=1):
        res = self.lp_json("check", *files, code=code)
        return res, {(f["severity"], f["rule"]) for f in res["findings"]}

    def test_bad_html_hits_every_html_rule(self):
        _, rules = self.findings(FIX / "bad/bad-page.html")
        for rule in ("h1", "img-alt", "empty-href", "lang", "viewport", "title", "meta-description",
                     "json-ld", "banned-phrase", "placeholder"):
            self.assertIn(("error", rule), rules)
        for rule in ("hash-href", "canonical", "open-graph", "em-dash-density", "exclamation", "headline-length"):
            self.assertIn(("warn", rule), rules)
        self.assertIn(("info", "twitter-card"), rules)
        self.assertIn(("info", "we-you-ratio"), rules)

    def test_length_warnings_and_missing_jsonld(self):
        res, rules = self.findings(FIX / "bad/bad-lengths.html", code=0)
        self.assertEqual(res["counts"]["error"], 0)
        for rule in ("title-length", "meta-description-length", "json-ld"):
            self.assertIn(("warn", rule), rules)

    def test_bad_copy(self):
        res, rules = self.findings(FIX / "bad/bad-copy.md")
        for sev, rule in (("error", "banned-phrase"), ("error", "placeholder"), ("warn", "exclamation"),
                          ("warn", "headline-length")):
            self.assertIn((sev, rule), rules)
        banned = {f["message"].split("'")[1] for f in res["findings"] if f["rule"] == "banned-phrase"}
        self.assertTrue({"unlock", "seamless", "elevate", "empower", "look no further"} <= banned)
        we = [f for f in res["findings"] if f["rule"] == "we-you-ratio"][0]
        self.assertIn("talks about itself", we["message"])

    def test_good_samples_are_clean(self):
        res, _ = self.findings(SAMPLE / "pages/home/build/index.html", SAMPLE / "pages/home/08-copy.md",
                               SAMPLE / "pages/home/09-wireframe.html", code=0)
        self.assertEqual(res["counts"], {"error": 0, "warn": 0, "info": 3})

    def test_em_dash_density_in_markdown(self):
        f = self.tmp / "dash.md"
        f.write_text("# Title\n\nYou get it fixed \u2014 today \u2014 and \u2014 it holds.\n")
        _, rules = self.findings(f, code=0)
        self.assertIn(("warn", "em-dash-density"), rules)

    def test_extra_banned_and_page_check(self):
        ws = self.init()
        self.do_research(ws)
        self.do_page_step(ws, "home", 7)
        self.run_lp("start", 8, "--page", "home", cwd=ws)
        self.put(SAMPLE / "pages/home/08-copy.md", ws / "pages/home/08-copy.md")
        self.run_lp("check", "--page", "home", cwd=ws)
        m = self.manifest(ws)
        m["copy_rules"]["extra_banned"] = ["no drama"]
        (ws / "lp.json").write_text(json.dumps(m))
        res = self.lp_json("check", "--page", "home", cwd=ws, code=1)
        self.assertIn("'no drama'", " ".join(f["message"] for f in res["findings"]))

    def test_cannibalization(self):
        ws = self.init()
        self.do_research(ws)
        self.do_page_step(ws, "home", 7)
        p = self.run_lp("page", "add", "pricing", "--keyword", "Same Day  Plumber Harbor City", cwd=ws, code=1)
        self.assertIn("cannibalization", p.stderr)
        self.run_lp("page", "add", "pricing", cwd=ws)
        self.run_lp("start", 7, "--page", "pricing", cwd=ws)
        self.put(SAMPLE / "pages/home/07-structure.md", ws / "pages/pricing/07-structure.md")
        self.assertIn("cannibalization", self.run_lp("done", 7, "--page", "pricing", cwd=ws, code=1).stdout)
        res = self.lp_json("check", cwd=ws, code=1)
        self.assertIn(("error", "cannibalization"), {(f["severity"], f["rule"]) for f in res["findings"]})


class TestPortableAndJSON(LPTestCase):
    def test_vendored_copy_runs_standalone_after_move(self):
        ws = self.init()
        self.do_research(ws, [1])
        moved = self.tmp / "elsewhere" / "zipped-and-back"
        moved.parent.mkdir()
        shutil.move(str(ws), str(moved))
        vend = moved / ".lp" / "lp.py"
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(self.home)}
        it = json.loads(self.run_lp("next", "--json", cwd=moved, script=vend, env=env).stdout)
        self.assertEqual(it["step"], 2)
        self.assertEqual(it["guide"]["path"], str(moved / ".lp/guide/steps/02-customer-research.md"))
        self.run_lp("start", 2, cwd=moved / "research", script=vend, env=env)  # finds lp.json walking up
        self.assertTrue((moved / "research/02-customers.md").is_file())
        self.run_lp("done", 2, cwd=moved, script=vend, env=env, code=1)
        self.run_lp("status", cwd=moved, script=vend, env=env)
        self.run_lp("check", FIX / "bad/bad-copy.md", cwd=moved, script=vend, env=env, code=1)
        doc = json.loads(self.run_lp("doctor", "--json", cwd=moved, script=vend, env=env).stdout)
        self.assertTrue(doc["ok"])
        self.run_lp("sync-guide", cwd=moved, script=vend, env=env, code=2)  # no installed skill to sync from
        p = self.run_lp("sync-guide", cwd=moved, script=vend, env=dict(env, LP_SKILL_HOME=str(ROOT)))
        self.assertIn("Refreshed", p.stdout)

    def test_workspace_discovery_by_env_and_dir(self):
        ws = self.init()
        self.assertEqual(self.lp_json("next", cwd=self.tmp, env=self.env(LP_WORKSPACE=str(ws)))["step"], 1)
        self.assertEqual(self.lp_json("next", "--dir", ws, cwd=self.tmp)["step"], 1)
        self.run_lp("next", cwd=self.tmp, code=2)

    def test_json_outputs_parse(self):
        self.lp_json("init", "Json Co", "--dir", self.tmp)
        ws = self.tmp / "json-co"
        for args in (["status"], ["next"], ["start", "1"], ["done", "1"], ["redo", "1"], ["page", "add", "about"],
                     ["page", "list"], ["stale"], ["check"], ["doctor"], ["sync-guide"],
                     ["approve", "gate1", "--page", "home", "--by", "X"], ["next", "--page", "nope"]):
            p = self.run_lp(*(args + ["--json"]), cwd=ws, code=None)
            data = json.loads(p.stdout)
            self.assertIsInstance(data, dict, args)
            if p.returncode == 2:
                self.assertFalse(data["ok"])
        self.assertEqual(json.loads(self.run_lp("--json", "next", cwd=ws).stdout)["step"], 1)

    def test_help_and_version(self):
        self.assertIn("1.0.0", self.run_lp("--version").stdout)
        for cmd in ([], ["init"], ["status"], ["next"], ["start"], ["done"], ["approve"], ["page"], ["page", "add"],
                    ["page", "list"], ["stale"], ["check"], ["redo"], ["sync-guide"], ["doctor"]):
            self.run_lp(*(cmd + ["--help"]))

    def test_importable_module(self):
        lp = load_module()
        self.assertEqual(lp.slugify("Acme Plumbing & Heating!"), "acme-plumbing-heating")
        self.assertEqual(lp.__version__, "1.0.0")
        self.assertEqual(sorted(lp.STEPS), list(range(17)))
        for n, s in lp.STEPS.items():
            self.assertTrue((ROOT / "references/steps" / s["guide"]).is_file(), s["guide"])
            for t, _ in s["templates"]:
                self.assertTrue((ROOT / "templates" / t).is_file(), t)
            for c in s["checklists"]:
                self.assertTrue((ROOT / "references/checklists" / c).is_file(), c)
            self.assertTrue(lp.done_criteria(ROOT / "references/steps" / s["guide"]), s["guide"])
        res = lp.check_file(FIX / "bad/bad-copy.md", lp.default_rules())
        self.assertTrue(any(f["rule"] == "banned-phrase" for f in res))


if __name__ == "__main__":
    unittest.main()
