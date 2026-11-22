"""The properties block at the top of the report, the two logs and a review (0.2.0): what it holds, the rules it
keeps, and that the scripts read a log or a report with it as they read one without it."""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import FIXTURES, SKILL, run

import forecasts
import ids
import signposts

TEMPLATES = SKILL / "templates"
LOGS = FIXTURES / "logs"
COMMON = ["type", "plugin", "date", "topic"]
KEYS = {"foresight.md": COMMON, "forecasts.md": COMMON, "signposts.md": COMMON, "review.md": COMMON + ["id", "from"]}
FRAGMENTS = ("scenario.md", "signal.md")  # they go inside a report, so a block there would sit mid-file


def block_of(text: str) -> list[str]:
    lines = text.split("\n")
    if lines[0] != "---" or "---" not in lines[1:]:
        return []
    return lines[1: lines.index("---", 1)]


class TheBlock(unittest.TestCase):
    def test_each_file_template_starts_with_one_and_no_fragment_does(self):
        self.assertEqual(sorted(p.name for p in TEMPLATES.glob("*.md")), sorted([*KEYS, *FRAGMENTS]))
        for name, keys in KEYS.items():
            block = block_of((TEMPLATES / name).read_text(encoding="utf-8"))
            self.assertEqual([l.split(":", 1)[0] for l in block if not l.startswith(" ")], keys, name)
            self.assertIn("plugin: poiesis-foresight", block, name)
        for name in FRAGMENTS:
            self.assertFalse((TEMPLATES / name).read_text(encoding="utf-8").startswith("---"), name)

    def test_it_keeps_the_rules_the_other_plugins_need(self):
        for name in KEYS:
            for line in block_of((TEMPLATES / name).read_text(encoding="utf-8")):
                self.assertFalse(line.lstrip().startswith("#"), f"{name}: {line}")
                if line.startswith(" "):
                    self.assertRegex(line, r'^  - "\[\[[^\]|]+\]\]"$', name)
                else:
                    self.assertRegex(line, r'^[a-z]+:(?: (?:"[^"]*"|\[\]|<[^:"]*>|[a-z-]+))?$', f"{name}: {line}")


PROPERTIES = '---\ntype: forecast-log\nplugin: poiesis-foresight\ndate: 2026-11-22\ntopic: "tests"\n---\n'


def scored(*argv: str) -> str:
    out, saved = io.StringIO(), sys.argv
    sys.argv = ["forecasts.py", *argv]
    try:
        with contextlib.redirect_stdout(out):
            forecasts.main()
    finally:
        sys.argv = saved
    return out.getvalue()


class ReadTheSame(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def with_block(self, name: str) -> Path:
        path = self.folder / name
        path.write_text(PROPERTIES + (LOGS / name).read_text(encoding="utf-8"), encoding="utf-8")
        return path

    def test_forecasts_are_scored_the_same(self):
        path = self.with_block("forecasts.md")
        for extra in ([], ["--sources"]):
            self.assertEqual(scored(str(path), *extra).replace(str(path), "LOG"),
                             scored(str(LOGS / "forecasts.md"), *extra).replace(str(LOGS / "forecasts.md"), "LOG"))

    def test_signposts_are_read_the_same(self):
        path = self.with_block("signposts.md")
        with_ = run(signposts, [str(path), "--today", "2030-06-01"])
        without = run(signposts, [str(LOGS / "signposts.md"), "--today", "2030-06-01"])
        self.assertEqual(with_[0], without[0])
        self.assertEqual(with_[1].replace(str(path), "LOG"), without[1].replace(str(LOGS / "signposts.md"), "LOG"))

    def test_the_next_ids_are_the_same(self):
        plain = self.folder / "plain"
        plain.mkdir()
        for name in ("forecasts.md", "signposts.md"):
            (plain / name).write_text((LOGS / name).read_text(encoding="utf-8"), encoding="utf-8")
            self.with_block(name)
        for prefix in ("F", "SP", "SC"):
            self.assertEqual(run(ids, [prefix, str(self.folder / "forecasts.md"), str(self.folder / "signposts.md")])[:2],
                             run(ids, [prefix, str(plain / "forecasts.md"), str(plain / "signposts.md")])[:2], prefix)


if __name__ == "__main__":
    unittest.main()
