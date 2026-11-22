"""The plugin's own files: every rule points to a note that says how much of its source was read, the scripts
need the standard library only, the version is the same in three places, and nothing personal is in the files."""
import ast
import json
import re
import subprocess
import sys
import unicodedata
import unittest
from pathlib import Path

from helpers import PLUGIN, ROOT, SCRIPTS, SKILL

NOTES = ROOT / "research" / "notes"
PLAYBOOKS = sorted((SKILL / "playbooks").glob("*.md"))
NOTE_NAME = re.compile(r"`([a-z][a-z-]*-\d{4}-[a-z0-9-]+)`")
LEVELS = ("full text", "part of the text", "abstract only", "title only", "observation")
SAID = ("read in part", "read in full", "abstract only", "title only", "an observation")
EXPECTED = ["base-rates", "challenge", "drivers", "forecasts", "horizons", "layers", "review", "scan", "scenarios", "signposts", "stress-test", "trends", "wheels"]


def plain(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)).lower()


def read_first(text: str) -> str:
    m = re.search(r"^## Read first\n(.*?)(?=^## )", text, re.M | re.S)
    return m.group(1) if m else ""


class Playbooks(unittest.TestCase):
    def test_the_thirteen_playbooks_are_there(self):
        self.assertEqual([p.stem for p in PLAYBOOKS], EXPECTED)

    def test_each_starts_with_read_first(self):
        for p in PLAYBOOKS:
            headings = re.findall(r"^## (.+)$", p.read_text(encoding="utf-8"), re.M)
            self.assertEqual(headings[0], "Read first", p.name)

    def test_each_note_named_under_read_first_exists_and_its_read_level_is_said(self):
        for p in PLAYBOOKS:
            section = read_first(p.read_text(encoding="utf-8"))
            names = NOTE_NAME.findall(section)
            self.assertTrue(names, f"{p.name} names no note under Read first")
            for name in names:
                self.assertTrue((NOTES / f"{name}.md").is_file(), f"{p.name} names a note that does not exist: {name}")
            for bullet in re.split(r"\n(?=- )", section):
                if NOTE_NAME.search(bullet):
                    self.assertTrue(any(word in bullet.lower() for word in SAID), f"{p.name}: this line names a note and not how much was read:\n{bullet}")

    def test_a_playbook_never_says_more_was_read_than_the_note_does(self):
        """`abstract only` or `title only` in a note must be said wherever a playbook names that note under Read first."""
        for p in PLAYBOOKS:
            for bullet in re.split(r"\n(?=- )", read_first(p.read_text(encoding="utf-8"))):
                for name in NOTE_NAME.findall(bullet):
                    read_line = next(l for l in (NOTES / f"{name}.md").read_text(encoding="utf-8").splitlines() if l.startswith("- **Read:**")).lower()
                    for level in ("abstract only", "title only"):
                        if read_line.startswith(f"- **read:** {level}"):
                            self.assertIn(level, bullet.lower(), f"{p.name} names {name} without saying it was read as {level}")

    def test_every_note_named_anywhere_in_the_skill_exists(self):
        for path in [*SKILL.rglob("*.md"), *(PLUGIN / "agents").glob("*.md")]:
            for name in NOTE_NAME.findall(path.read_text(encoding="utf-8")):
                self.assertTrue((NOTES / f"{name}.md").is_file(), f"{path.name} names a note that does not exist: {name}")

    def test_the_skill_names_every_playbook_script_and_template(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        everything = skill + "".join(p.read_text(encoding="utf-8") for p in PLAYBOOKS)
        for p in PLAYBOOKS:
            self.assertIn(f"playbooks/{p.name}", skill)
        for script in sorted(SCRIPTS.glob("*.py")):
            self.assertIn(script.name, everything)
        for template in sorted((SKILL / "templates").glob("*.md")):
            self.assertIn(f"templates/{template.name}", everything)

    def test_the_moved_passages_are_still_there_word_for_word(self):
        """What came from poiesis-insight's foresight playbook, each passage in the playbook that took it over."""
        moved = {
            "horizons": "Place each pattern: **H1** the current way, losing its fit; **H3** an emerging pattern on the fringes; **H2** the\ntransitional innovations, either feeding H3 (H2+) or being absorbed back into H1 (H2−). All three exist at once.",
            "layers": "For the main issue, write four readings: the **litany** (the headline trend), the **social causes**, the\n**worldview** behind them, the **myth or metaphor**. Conclusions that only appear at the deeper layers are the\nuncommon ones; they still go through `playbooks/challenge.md`.",
            "scenarios": "Two to four scenarios built on the most uncertain, most important drivers. Report what holds across all scenarios\n(robust) and what depends on one (contingent); scenarios guide flexible choices, they are not forecasts.",
            "forecasts": "Where a claim can be checked later, write it as a forecast: a precise question, a probability, a date to resolve\nit. Add it to `foresight/forecasts.md` (`templates/forecasts.md`). When dates pass, score them:\n`python3 -I $S/forecasts.py foresight/forecasts.md`. Scores show which reasoning to trust next time.",
        }
        moved["scan"] = 'Collect signals from the input (and, if the user asks, from new research via the research plugin). Log each one with\n`templates/signal.md`, keeping three things apart (Hiltunen 2008): the **signal** (what was observed, how visible),\nthe **issue** (how widespread), the **interpretation** (what it might mean to us). A weak signal is low on\nvisibility and spread; it is not yet a trend.'
        moved["trends"] = "When the data have a time order (survey waves, usage logs, metrics), a trend is reported only after three checks:\n- **Signal or noise:** is the change larger than the series' usual variation? Draw the series with its mean and\n  limits at about three standard deviations, and look for points outside them or a long run on one side\n  (control charts; Benneyan et al. 2003). Say how many points the series has; a few points give a lead, not a trend.\n- **Base rate:** how often do similar changes, in similar series or past periods, continue? Start the forecast from\n  that outside view and adjust it, not from the story of this case (Kahneman & Lovallo 1993).\n- **Shape:** steady, speeding up, slowing down or leveling off; seasonal; a sudden break. Extrapolate only as a\n  dated forecast in the log, never as a statement."
        for name, passage in moved.items():
            self.assertIn(passage, (SKILL / "playbooks" / f"{name}.md").read_text(encoding="utf-8"), name)


class Notes(unittest.TestCase):
    def test_every_note_says_how_much_of_its_source_was_read(self):
        notes = sorted(NOTES.glob("*.md"))
        self.assertGreaterEqual(len(notes), 28)
        for note in notes:
            lines = [l for l in note.read_text(encoding="utf-8").splitlines() if l.startswith("- **Read:**")]
            self.assertEqual(len(lines), 1, note.name)
            self.assertTrue(any(lines[0].lower().startswith(f"- **read:** {level}") for level in LEVELS), f"{note.name}: {lines[0]}")

    def test_a_note_read_as_an_abstract_or_a_title_cites_no_page(self):
        for note in sorted(NOTES.glob("*.md")):
            text = note.read_text(encoding="utf-8")
            read = next(l for l in text.splitlines() if l.startswith("- **Read:**")).lower()
            if read.startswith(("- **read:** abstract only", "- **read:** title only")):
                body = text.split("## ", 1)[1] if "## " in text else ""
                self.assertIsNone(re.search(r"\(p\. \d", body), f"{note.name} gives a page for a source that was not read past its abstract")
            if read.startswith("- **read:** title only"):
                self.assertNotIn("## What it says", text, f"{note.name} says what a source says, and only its title was read")

    def test_the_rules_name_every_source_at_the_level_it_was_read(self):
        rules = plain((SKILL / "rules.md").read_text(encoding="utf-8").split("## Where these rules come from", 1)[1])
        sections = {"part of the text": "read in part", "abstract only": "read as an abstract only", "title only": "known by title only", "observation": "an observation"}
        for note in sorted(NOTES.glob("*.md")):
            author = {"go-science": "government office for science", "poiesis-lab": "recorded run"}.get("-".join(note.stem.split("-")[:2]), note.stem.split("-")[0])
            self.assertIn(author, rules, f"rules.md does not name the source of {note.name}")
            read = next(l for l in note.read_text(encoding="utf-8").splitlines() if l.startswith("- **Read:**")).lower()
            level = next(v for k, v in sections.items() if read.startswith(f"- **read:** {k}"))
            start = rules.index(level)
            end = min([rules.index(v, start + 1) for v in sections.values() if v != level and v in rules[start + 1:]] + [len(rules)])
            self.assertIn(author, rules[start:end], f"rules.md does not list {note.name} under \"{level}\"")

    def test_the_index_links_every_note(self):
        index = (ROOT / "research" / "README.md").read_text(encoding="utf-8")
        for note in sorted(NOTES.glob("*.md")):
            self.assertIn(f"notes/{note.name}", index)


class Scripts(unittest.TestCase):
    LOCAL = {"series_gate"}

    def test_each_runs_with_python3_dash_i_and_the_standard_library_only(self):
        scripts = sorted(SCRIPTS.glob("*.py"))
        self.assertEqual([s.name for s in scripts], ["forecasts.py", "ids.py", "series_gate.py", "signposts.py", "trends.py"])
        for script in scripts:
            text = script.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("#!/usr/bin/env python3\n"), script.name)
            tree = ast.parse(text)
            self.assertIn("python3 -I", ast.get_docstring(tree) or "", script.name)
            for node in ast.walk(tree):
                names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) else []
                for name in names:
                    top = name.split(".")[0]
                    self.assertTrue(top in sys.stdlib_module_names or top in self.LOCAL, f"{script.name} imports {name}")
            done = subprocess.run([sys.executable, "-I", str(script), "--help"], capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, f"{script.name} --help: {done.stderr}")

    def test_no_script_opens_a_connection_or_writes_a_file(self):
        for script in sorted(SCRIPTS.glob("*.py")):
            text = script.read_text(encoding="utf-8")
            for word in ("urllib", "socket", "http.client", "import requests", "subprocess", ".write_text(", ".write_bytes(", "os.remove", "unlink("):
                self.assertNotIn(word, text, f"{script.name} uses {word}")
            self.assertIsNone(re.search(r"open\([^)]*[\"'][wa]", text), f"{script.name} opens a file for writing")


class Manifest(unittest.TestCase):
    def test_the_version_is_the_same_in_three_places(self):
        plugin = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        changelog = re.search(r"^## (\d+\.\d+\.\d+)$", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.M).group(1)
        self.assertEqual(plugin["version"], "0.1.0")
        self.assertEqual([p["version"] for p in market["plugins"]], [plugin["version"]])
        self.assertEqual(changelog, plugin["version"])
        self.assertEqual((plugin["name"], market["plugins"][0]["name"], market["plugins"][0]["source"]), ("poiesis-foresight", "poiesis-foresight", "./plugins/poiesis-foresight"))

    def test_agents_have_a_name_a_description_a_model_and_read_only_tools(self):
        agents = sorted((PLUGIN / "agents").glob("*.md"))
        self.assertEqual([a.stem for a in agents], ["forecaster", "foresight-analyst"])
        for agent in agents:
            front = agent.read_text(encoding="utf-8").split("---")[1]
            fields = dict(line.split(": ", 1) for line in front.strip().splitlines())
            self.assertEqual(fields["name"], agent.stem)
            self.assertTrue(fields["description"].strip() and fields["model"].strip())
            tools = {t.strip() for t in fields["tools"].split(",")}
            self.assertFalse(tools & {"Write", "Edit", "NotebookEdit", "WebSearch", "WebFetch"}, f"{agent.name}: {tools}")

    def test_the_skill_has_its_front_matter(self):
        front = (SKILL / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
        self.assertIn("name: foresight\n", front)
        self.assertIn("description: ", front)


class Readme(unittest.TestCase):
    def test_the_file_tree_in_the_readme_names_every_file_of_the_plugin(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        tree = readme.split("## What's in this repository", 1)[1].split("## ", 1)[0]
        for folder in ("playbooks", "scripts", "templates"):
            for path in sorted((SKILL / folder).glob("*.*")):
                self.assertIn(path.name, tree, f"the README's tree does not list {folder}/{path.name}")
        for path in sorted((PLUGIN / "agents").glob("*.md")):
            self.assertIn(path.name, tree)

    def test_the_readmes_say_five_products_and_give_the_install_lines(self):
        for path in (ROOT / "README.md", PLUGIN / "README.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("five products", text, path.name)
            self.assertIn("/plugin marketplace add gorgmihai92/poiesis-foresight", text)
            self.assertIn("/plugin install poiesis-foresight@poiesis-foresight", text)


class Evals(unittest.TestCase):
    def test_each_case_has_a_prompt_and_graders_in_the_format_of_a_blank_case(self):
        cases = sorted(p for p in (PLUGIN / "evals").iterdir() if p.is_dir() and p.name != "results")
        self.assertEqual(len(cases), 8)
        for case in cases:
            prompt = (case / "prompt.md").read_text(encoding="utf-8")
            self.assertTrue(prompt.startswith("---\n"), case.name)
            front, body = prompt.split("---\n", 2)[1:]
            for field in ("max_turns: ", "allowed_tools: [Read, Glob, Grep, Skill]", "runs: 1", "description: "):
                self.assertIn(field, front, f"{case.name}: {field}")
            self.assertGreater(len(body.strip()), 80, case.name)
            graders = sorted((case / "graders").glob("*.md"))
            self.assertGreaterEqual(len(graders), 2, case.name)
            types = [re.search(r"^type: (\w+)$", g.read_text(encoding="utf-8"), re.M).group(1) for g in graders]
            self.assertIn("llm", types, case.name)
            self.assertIn("tool_used", types, case.name)
            self.assertTrue(set(types) <= {"llm", "regex", "tool_used"}, f"{case.name}: {types}")
            for g in graders:
                m = re.search(r"^pattern: '(.+)'$", g.read_text(encoding="utf-8"), re.M)
                if m:
                    re.compile(m.group(1))  # a pattern that does not compile fails here

    def test_the_regex_graders_match_what_they_are_meant_to(self):
        def pattern(case: str, grader: str):
            text = (PLUGIN / "evals" / case / "graders" / f"{grader}.md").read_text(encoding="utf-8")
            flags = re.I if re.search(r"^flags: i$", text, re.M) else 0
            return re.compile(re.search(r"^pattern: '(.+)'$", text, re.M).group(1), flags)
        row = pattern("forecast-not-edited-after", "row-keeps-its-probability")
        self.assertTrue(row.search("| F-003 | Will the standard be published? | 0.80 | 2026-05-02 | 2026-10-31 | 0 | note | 0.70 0.80 0.80 | 0.85 |"))
        self.assertFalse(row.search("| F-003 | Will the standard be published? | 0.30 | 2026-05-02 | 2026-10-31 | 0 | note | 0.70 0.80 0.80 | 0.85 |"))
        verdict = pattern("verdict-copied-not-retyped", "first-verdict-kept-as-given")
        self.assertTrue(verdict.search("- Raw counts overstate 2025 growth in every area: **weakened**."))
        self.assertFalse(verdict.search("- Raw counts overstate 2025 growth in every area: kept.\n- Synthetic biology accelerated in 2025: weakened."))
        self.assertTrue(pattern("no-signals-no-invention", "says-not-checked").search("**Not checked:** a scan"))
        fired = (PLUGIN / "evals" / "one-year-is-a-lead" / "graders" / "skill-fired.md").read_text(encoding="utf-8")
        match = re.compile(re.search(r"^input_match: '(.+)'$", fired, re.M).group(1))
        self.assertTrue(match.search('{"skill": "poiesis-foresight:foresight"}') and match.search('{"skill":"foresight"}'))
        self.assertFalse(match.search('{"skill": "poiesis-insight:insight"}'))


class NothingPersonal(unittest.TestCase):
    def test_no_home_path_private_address_or_key_is_in_the_repository(self):
        listed = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-co", "--exclude-standard"], capture_output=True, text=True)
        if listed.returncode != 0:
            self.skipTest("not a git checkout: the list of files could not be read")
        for name in listed.stdout.splitlines():
            path = ROOT / name
            if path.suffix in (".pdf", ".png") or not path.is_file() or path.name == "test_plugin_files.py":
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for needle in ("/Users/", "@gmail", "mailto:", "OPENALEX_API_KEY=", "S2_API_KEY="):
                self.assertNotIn(needle, text, f"{name} contains {needle}")


if __name__ == "__main__":
    unittest.main()
