"""series_gate.py: a series from poiesis-research is accepted only with complete metadata, a database that
answered, a complete run and the same document types on both sides of its share."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SERIES, SCRIPTS, research, run

import series_gate as gate


class GateCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def copy(self, change=None, drop: tuple[str, ...] = ()) -> Path:
        """A copy of the replayed series, with its metadata changed by `change(meta)` and files in `drop` removed."""
        for tail in (".csv", ".types.csv", ".meta.json"):
            if tail not in drop:
                shutil.copy(SERIES.with_name(SERIES.name + tail), self.tmp / (SERIES.name + tail))
        meta_path = self.tmp / (SERIES.name + ".meta.json")
        if change and meta_path.is_file():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            change(meta)
            meta_path.write_text(json.dumps(meta), encoding="utf-8")
        return self.tmp / (SERIES.name + ".csv")

    def reasons(self, path: Path) -> list[str]:
        found = gate.check(path)
        self.assertFalse(found["accepted"])
        return found["reasons"]


class Accepts(GateCase):
    def test_the_series_replayed_from_researchs_recording_is_accepted(self):
        found = gate.check(SERIES.with_name(SERIES.name + ".csv"))
        self.assertEqual(found["reasons"], [])
        self.assertTrue(found["accepted"])
        f = found["facts"]
        self.assertEqual((f["database"], f["fetched"], f["years"], f["partial_years"]), ("OpenAlex", "2026-11-21", [2015, 2026], [2026]))
        self.assertEqual(f["types_above"], ["article", "preprint", "review"])
        self.assertEqual(f["types_above"], f["types_below"])
        self.assertEqual(f["rows"], 24)

    def test_the_metadata_file_or_the_types_file_can_be_named_instead_of_the_csv(self):
        for tail in (".meta.json", ".types.csv"):
            self.assertTrue(gate.check(SERIES.with_name(SERIES.name + tail))["accepted"], tail)

    def test_an_untouched_copy_is_accepted_and_the_command_exits_0(self):
        code, text, _ = run(gate, [str(self.copy())])
        self.assertEqual(code, 0)
        self.assertTrue(text.startswith("ACCEPTED solid-state-batteries-2026-11-21: OpenAlex, fetched 2026-11-21, 2015–2026 (partial: 2026)"), text)
        self.assertIn("article, preprint, review", text)

    def test_the_order_and_case_of_type_names_do_not_matter(self):
        def change(meta):
            meta["share"]["numerator_types"] = ["Review", "article", "preprint"]
        self.assertTrue(gate.check(self.copy(change))["accepted"])


class Refuses(GateCase):
    def test_one_side_of_the_share_counting_other_types(self):
        def change(meta):
            meta["share"]["denominator_types"] = ["all"]
        reasons = self.reasons(self.copy(change))
        self.assertIn("the share counts different document types on its two sides: article, preprint, review above the line, every document type below", reasons)

    def test_a_series_marked_incomplete(self):
        def change(meta):
            meta["complete"] = False
            meta["stopped"] = "OpenAlex asks for a key past the first 200 topics"
        self.assertEqual(self.reasons(self.copy(change)), ['the series is marked incomplete (it stopped: "OpenAlex asks for a key past the first 200 topics")'])

    def test_a_series_with_no_database_named(self):
        def change(meta):
            del meta["database"]
        self.assertEqual(self.reasons(self.copy(change)), ["the series does not name its database"])

    def test_the_three_changed_copies_make_the_command_exit_1(self):
        def types(meta):
            meta["share"]["numerator_types"] = ["article"]

        def incomplete(meta):
            meta["complete"] = False

        def no_database(meta):
            meta["database"] = ""
        for change in (types, incomplete, no_database):
            code, text, _ = run(gate, [str(self.copy(change))])
            self.assertEqual(code, 1, text)
            self.assertTrue(text.startswith("REFUSED "), text)

    def test_a_coverage_line_in_which_the_database_did_not_answer(self):
        def refused(meta):
            meta["coverage"] = "Coverage (2026-11-21): OpenAlex refused (the daily budget is used up); Crossref answered (3 requests)."

        def absent(meta):
            del meta["coverage"]
        self.assertTrue(self.reasons(self.copy(refused))[0].startswith("the Coverage line does not say that OpenAlex answered"))
        self.assertEqual(self.reasons(self.copy(absent)), ["the series does not say which database answered: it has no Coverage line"])

    def test_metadata_with_fields_missing(self):
        def change(meta):
            del meta["fetched"], meta["script"], meta["share"]
        reasons = self.reasons(self.copy(change))
        self.assertIn("the metadata is incomplete: no `fetched`, `share`, `script`", reasons)

    def test_no_word_on_whether_the_run_was_complete(self):
        def change(meta):
            del meta["complete"]
        self.assertEqual(self.reasons(self.copy(change)), ["the metadata does not say whether the run was complete"])

    def test_no_metadata_file_at_all(self):
        reasons = self.reasons(self.copy(drop=(".meta.json",)))
        self.assertEqual(len(reasons), 1)
        self.assertIn("no metadata file", reasons[0])

    def test_metadata_that_is_not_json(self):
        path = self.copy()
        path.with_name(SERIES.name + ".meta.json").write_text("{not json", encoding="utf-8")
        self.assertIn("cannot be read", self.reasons(path)[0])

    def test_an_unfinished_year_that_is_not_marked_partial(self):
        def change(meta):
            meta["partial_years"] = []
        reasons = self.reasons(self.copy(change))
        self.assertIn("2026 was not over when the series was fetched (2026-11-21) and is not marked partial", reasons)

    def test_numbers_that_are_not_the_sum_of_the_declared_types(self):
        """The labels say the same types on both sides, and the base column holds every type: the numbers decide."""
        path = self.copy()
        lines = path.read_text(encoding="utf-8").splitlines()
        cells = lines[1].split(",")
        self.assertEqual(cells[:3], ["solid-state-batteries", "Solid-state batteries", "2015"])
        cells[5] = cells[8]  # base := base_all_types
        lines[1] = ",".join(cells)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        reasons = self.reasons(path)
        self.assertEqual(len(reasons), 1)
        self.assertIn("the counts are not the sum of the declared document types: solid-state-batteries 2015: `base` is 9329446 and the types file gives 5905543", reasons[0])

    def test_a_data_file_missing_or_with_other_columns(self):
        self.assertIn("is not beside the metadata", self.reasons(self.copy(drop=(".csv",)).with_name(SERIES.name + ".meta.json"))[0])
        path = self.copy()
        path.write_text("year,works\n2015,88\n", encoding="utf-8")
        self.assertIn("does not have the columns counts.py writes", self.reasons(path)[0])

    def test_a_series_without_a_types_file_is_accepted_and_says_the_counts_were_not_checked(self):
        code, text, _ = run(gate, [str(self.copy(drop=(".types.csv",)))])
        self.assertEqual(code, 0)
        self.assertIn("No types file: the counts were not checked against it.", text)

    def test_json_output_lists_every_reason(self):
        def change(meta):
            meta["complete"] = False
            meta["database"] = ""
        code, text, _ = run(gate, [str(self.copy(change)), "--json"])
        self.assertEqual(code, 1)
        found = json.loads(text)
        self.assertEqual(len(found[0]["reasons"]), 2)


class FromResearch(unittest.TestCase):
    """The committed series is what poiesis-research's counts.py gives from its own recording."""

    def test_counts_py_replay_gives_the_committed_files(self):
        repo = research()
        if not repo:
            self.skipTest("POIESIS_RESEARCH does not name a checkout of poiesis-research 2.4.0: the series was not made again")
        scripts = repo / "plugins" / "poiesis-research" / "skills" / "research" / "scripts"
        with tempfile.TemporaryDirectory() as tmp:
            done = subprocess.run(
                [sys.executable, "-I", str(scripts / "counts.py"), '"solid-state battery"', '"quantum computing" OR "quantum computer"',
                 "--label", "Solid-state batteries", "--label", "Quantum computing", "--from", "2015", "--to", "2026",
                 "--replay", str(repo / "tests" / "recordings" / "counts-series"), "--out", tmp],
                capture_output=True, text=True, env={"POIESIS_RESEARCH_CACHE": "off", "PATH": "/usr/bin:/bin"})
            self.assertEqual(done.returncode, 0, done.stderr)
            for tail in (".csv", ".types.csv"):
                self.assertEqual((Path(tmp) / (SERIES.name + tail)).read_bytes(), SERIES.with_name(SERIES.name + tail).read_bytes(), tail)
            self.assertTrue(gate.check(Path(tmp) / (SERIES.name + ".csv"))["accepted"])


class Script(unittest.TestCase):
    def test_it_runs_isolated_with_the_standard_library_only(self):
        done = subprocess.run([sys.executable, "-I", str(SCRIPTS / "series_gate.py"), str(SERIES.with_name(SERIES.name + ".csv"))], capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertTrue(done.stdout.startswith("ACCEPTED"))


if __name__ == "__main__":
    unittest.main()
