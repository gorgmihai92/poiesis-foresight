"""forecasts.py, signposts.py and ids.py: the three scripts that read the project's logs and ids."""
import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import FIXTURES, SCRIPTS, SKILL, lab, run

import forecasts
import ids
import signposts

LOGS = FIXTURES / "logs"


def scored(*argv: str) -> str:
    """What forecasts.py prints (its main() reads the command line itself, as it did in poiesis-insight)."""
    out, saved = io.StringIO(), sys.argv
    sys.argv = ["forecasts.py", *argv]
    try:
        with contextlib.redirect_stdout(out):
            code = forecasts.main()
    finally:
        sys.argv = saved
    assert code == 0  # it always exits 0: what it prints is what is compared
    return out.getvalue()


DEFAULT = """Brier score: 0.127 over 6 resolved forecasts (0 = perfect, 0.25 = always 50%)
  F-001: said 80%, outcome 1 → 0.040
  F-002: said 35%, outcome 0 → 0.122
  F-003: said 70%, outcome 1 → 0.090
  F-004: said 90%, outcome 1 → 0.010
  F-005: said 50%, outcome 0 → 0.250
  F-006: said 50%, outcome 0 → 0.250

Past their date, outcome missing:
  F-008 (2020-01-01): Past its date with no outcome
"""

SOURCES = """
By source:
  Over the 3 resolved forecasts that have a model and an owner probability (0 = perfect, 0.25 = always 50%):
    of record: 0.074
    model, mean of its runs: 0.143
    model, median of its runs: 0.143
    owner: 0.113
    mean of owner and model: 0.124
  Fewer than 3 model runs: F-004
  Not in this comparison (no model or no owner probability): F-001, F-005
  Model or owner cell not understood: F-006
  The forecast of record is not the mean of the owner's and the model's: F-004 (0.90 logged, 0.60 is the mean)
"""


class Forecasts(unittest.TestCase):
    def test_columns_after_reasoning_do_not_change_the_score(self):
        self.assertEqual(scored(str(LOGS / "forecasts.md")), DEFAULT)

    def test_sources_scores_model_and_owner_on_the_rows_that_have_both(self):
        self.assertEqual(scored(str(LOGS / "forecasts.md"), "--sources"), DEFAULT + SOURCES)

    def test_a_log_without_the_new_columns_says_there_is_nothing_to_compare(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "forecasts.md"
            log.write_text("| id | question | probability | made | resolve by | outcome | reasoning |\n|---|---|---|---|---|---|---|\n"
                           "| F-001 | Old log | 0.80 | 2019-01-01 | 2019-06-30 | 1 | note | 0.70 | 0.65 |\n", encoding="utf-8")
            text = scored(str(log), "--sources")
        self.assertIn("Brier score: 0.040 over 1 resolved forecasts", text)
        self.assertIn("The log has no `model` and `owner` columns after `reasoning`: nothing to compare.", text)

    def test_a_table_aligned_or_padded_by_an_editor_reads_the_same(self):
        """Obsidian pads cells and can put colons in the line under the header."""
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "forecasts.md"
            log.write_text("| id    | question            | probability | made       | resolve by | outcome | reasoning |\n"
                           "| :---- | :------------------ | ----------: | :--------: | ---------- | ------- | --------- |\n"
                           "| F-001 | Padded and aligned  | 0.80        | 2019-01-01 | 2019-06-30 | 1       | note      |\n", encoding="utf-8")
            text = scored(str(log))
        self.assertEqual(text, "Brier score: 0.040 over 1 resolved forecasts (0 = perfect, 0.25 = always 50%)\n  F-001: said 80%, outcome 1 → 0.040\n")

    def write(self, tmp: str, body: str) -> str:
        log = Path(tmp) / "forecasts.md"
        log.write_text("| id | question | probability | made | resolve by | outcome | reasoning |\n|---|---|---|---|---|---|---|\n" + body, encoding="utf-8")
        return str(log)

    def test_the_wording_column_gives_the_gap_between_the_two_wordings(self):
        """`wording` says which runs were given the negation; --sources prints the gap, and the scores do not move."""
        head = ("| id | question | probability | made | resolve by | outcome | reasoning | model | owner | wording |\n"
                "|---|---|---|---|---|---|---|---|---|---|\n")
        body = ("| F-001 | Two and one | 0.70 | 2019-01-01 | 2019-06-30 | 1 | n | 0.70 0.80 0.60 | 0.70 | written written negated |\n"
                "| F-002 | Three and two, interleaved | 0.45 | 2019-01-01 | 2099-12-31 |  | n | 0.40 0.50 0.40 0.50 0.45 | 0.45 | written negated written negated written |\n"
                "| F-003 | One wording only | 0.50 | 2019-01-01 | 2099-12-31 |  | n | 0.50 0.50 0.50 | 0.50 | written written written |\n"
                "| F-004 | Fewer words than runs | 0.50 | 2019-01-01 | 2099-12-31 |  | n | 0.50 0.50 0.50 | 0.50 | written negated |\n"
                "| F-005 | A word that is not one of the two | 0.50 | 2019-01-01 | 2099-12-31 |  | n | 0.50 0.50 | 0.50 | yes no |\n"
                "| F-006 | No wording: a row from before the column | 0.50 | 2019-01-01 | 2099-12-31 |  | n | 0.50 0.50 | 0.50 |  |\n"
                "| F-007 | No gap | 0.40 | 2019-01-01 | 2099-12-31 |  | n | 0.40 0.40 | 0.40 | negated written |\n")
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "forecasts.md"
            log.write_text(head + body, encoding="utf-8")
            text = scored(str(log), "--sources")
            without = Path(tmp) / "without.md"
            without.write_text(head.replace(" wording |", "").replace("|---|\n", "\n", 1)
                               + "".join(line.rsplit(" |", 2)[0] + " |\n" for line in body.splitlines()), encoding="utf-8")
            before = scored(str(without), "--sources")
            self.assertEqual(scored(str(log)), scored(str(without)))
        self.assertTrue(text.startswith("Brier score: 0.090 over 1 resolved forecasts"))
        self.assertEqual(text, before + (
            "\nThe other way round (the mean of the runs given the question as written, minus the mean of those given its "
            "negation, both as the probability of yes):\n"
            "  F-001: +0.15 (2 written, mean 0.75; 1 negated, mean 0.60)\n"
            "  F-002: -0.08 (3 written, mean 0.42; 2 negated, mean 0.50)\n"
            "  F-007: +0.00 (1 written, mean 0.40; 1 negated, mean 0.40)\n"
            "  Mean gap over 3 forecasts: +0.02\n"
            "  One wording only: F-003\n"
            "  Model or wording cell not understood (one word per run, written or negated): F-004, F-005\n"))

    def test_a_wording_column_with_no_row_in_both_wordings_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "forecasts.md"
            log.write_text("| id | question | probability | made | resolve by | outcome | reasoning | model | owner | wording |\n"
                           "|---|---|---|---|---|---|---|---|---|---|\n"
                           "| F-001 | Quick depth | 0.70 | 2019-01-01 | 2099-12-31 |  | n | 0.70 | 0.70 | written |\n", encoding="utf-8")
            text = scored(str(log), "--sources")
        self.assertTrue(text.endswith("  No forecast has runs in both wordings yet.\n  One wording only: F-001\n"))

    def test_a_probability_an_outcome_or_a_date_that_is_not_one_is_not_understood(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = scored(self.write(tmp, "| F-001 | ok | 0.80 | 2019-01-01 | 2019-06-30 | 1 | n |\n| F-002 | percent | 80 | 2019-01-01 | 2019-06-30 | 1 | n |\n"
                                          "| F-003 | negative | -0.2 | 2019-01-01 | 2019-06-30 | 0 | n |\n| F-004 | nan | nan | 2019-01-01 | 2019-06-30 | 0 | n |\n"
                                          "| F-005 | word | 0.50 | 2019-01-01 | 2019-06-30 | yes | n |\n| F-006 | date | 0.50 | 2019-01-01 | 30.06.2019 |  | n |\n"
                                          "| F-007 | far | 0.50 | 2019-01-01 | 01.01.2099 |  | n |\n"))
        self.assertEqual(text, "Brier score: 0.040 over 1 resolved forecasts (0 = perfect, 0.25 = always 50%)\n  F-001: said 80%, outcome 1 → 0.040\n"
                               "\nRows not understood: F-002, F-003, F-004, F-005, F-006, F-007\n")

    def test_an_indented_table_is_read_and_another_table_is_passed_over(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "forecasts.md"
            log.write_text("- a list item\n  | id | question | probability | made | resolve by | outcome | reasoning |\n  |---|---|---|---|---|---|---|\n"
                           "  | F-001 | indented | 0.80 | 2019-01-01 | 2019-06-30 | 1 | n |\n\n"
                           "| database | what | share | from | to | answered | note |\n|---|---|---|---|---|---|---|\n| OpenAlex | works | 0.90 | 2019-01-01 | 2019-06-30 | 1 | n |\n", encoding="utf-8")
            text = scored(str(log))
        self.assertEqual(text, "Brier score: 0.040 over 1 resolved forecasts (0 = perfect, 0.25 = always 50%)\n  F-001: said 80%, outcome 1 → 0.040\n")

    def test_a_log_that_cannot_be_read_says_so(self):
        done = subprocess.run([sys.executable, "-I", str(SCRIPTS / "forecasts.py"), "no-such-log.md"], capture_output=True, text=True)
        self.assertEqual((done.returncode, done.stderr), (2, ""))
        self.assertTrue(done.stdout.startswith("The log cannot be read:"))

    def test_the_template_is_a_log_the_script_reads(self):
        text = scored(str(SKILL / "templates" / "forecasts.md"), "--sources")
        self.assertIn("No resolved forecasts yet.", text)
        self.assertIn("No resolved forecast has both a model and an owner probability yet.", text)
        self.assertIn("No forecast has runs in both wordings yet.", text)
        self.assertNotIn("not understood", text)

    def test_the_labs_log_gives_the_labs_expected_output_line_for_line(self):
        notebook = lab()
        if not notebook:
            self.skipTest("the Poiesis Lab notebook is not on this machine (POIESIS_LAB, or ~/Poiesis Lab): its check was not run")
        fixtures = notebook / "fixtures"
        done = subprocess.run([sys.executable, "-I", str(SCRIPTS / "forecasts.py"), str(fixtures / "logs" / "forecasts.md")], capture_output=True, text=True)
        self.assertEqual(done.returncode, 0)
        want = (fixtures / "expected" / "forecasts.txt").read_text(encoding="utf-8")
        self.assertEqual([line.rstrip() for line in done.stdout.splitlines()], [line.rstrip() for line in want.splitlines()])


SIGNPOSTS = """Signposts watched: 5. Reached: 2.

Due for a look:
  SP-001 (due 2030-05-01): Due, numeric trigger not met · trigger >= 25 · last value 21.7, read 2029-11-01
  SP-006 (due 2030-03-15): Trigger is a sentence · trigger a second regulator adopts the rule

Reached their trigger:
  SP-003: Reached, value meets the trigger · trigger < 0.5 · last value 0.4 · response: reassessment: fixture
  SP-005: Status says reached and the value does not meet it · trigger >= 50% · last value 31% · response: capitalizing: fixture

Trigger is a sentence, for a person to judge: SP-006

Rows not in order:
  SP-004: the last value 140 meets the trigger > 100, and the status still says watching
  SP-005: status says reached, and the last value 31% does not meet the trigger >= 50%
  SP-008: status "provisional" is not one of watching, reached, retired
  SP-009: a date is not written as YYYY-MM-DD
  SP-010: fewer than the eight cells a signpost needs
  SP-011: the last value "several" is not a number, and the trigger compares with one
  SP-012: no date for the next check
"""


class Signposts(unittest.TestCase):
    def test_the_log_is_read_as_on_a_given_day(self):
        code, text, _ = run(signposts, [str(LOGS / "signposts.md"), "--today", "2030-06-01"])
        self.assertEqual(text, SIGNPOSTS)
        self.assertEqual(code, 1)  # rows are not in order

    def test_a_log_in_order_exits_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "signposts.md"
            log.write_text("| id | watch | trigger | points to | response | lead time | status | next check | last value | last checked | note |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
                           "| SP-001 | Share of X | >= 25 | SC-001 | corrective: do Y | 6 months | watching | 2031-01-01 | 21.7 | 2030-05-01 | a column added later |\n", encoding="utf-8")
            code, text, _ = run(signposts, [str(log), "--today", "2030-06-01"])
        self.assertEqual((code, text), (0, "Signposts watched: 1. Reached: 0.\n"))

    def test_an_aligned_table_reads_the_same(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "signposts.md"
            log.write_text("| id | watch | trigger | points to | response | lead time | status | next check | last value | last checked |\n|:---|:---|---:|:---:|---|---|---|---|---|---|\n"
                           "| SP-001 | Share of X | >= 25 | SC-001 | corrective: do Y | 6 months | watching | 2031-01-01 | 21.7 | 2030-05-01 |\n", encoding="utf-8")
            code, text, _ = run(signposts, [str(log), "--today", "2030-06-01"])
        self.assertEqual((code, text), (0, "Signposts watched: 1. Reached: 0.\n"))

    def test_a_comma_is_not_read_as_a_decimal_point_and_a_missing_log_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "signposts.md"
            log.write_text("| id | watch | trigger | points to | response | lead time | status | next check | last value | last checked |\n|---|---|---|---|---|---|---|---|---|---|\n"
                           "| SP-001 | Share of X | >= 25 | SC-001 | corrective: do Y | 6 months | watching | 2031-01-01 | 9,5 | 2030-05-01 |\n", encoding="utf-8")
            code, text, _ = run(signposts, [str(log), "--today", "2030-06-01"])
            self.assertEqual(code, 1)
            self.assertIn('SP-001: the last value "9,5" is not a number', text)
            self.assertEqual(run(signposts, [str(log), "--today", "tomorrow"])[0], 2)
            self.assertEqual(run(signposts, [str(Path(tmp) / "none.md")])[0], 2)

    def test_the_template_is_a_log_the_script_reads(self):
        code, text, _ = run(signposts, [str(SKILL / "templates" / "signposts.md")])
        self.assertEqual((code, text), (0, "Signposts watched: 0. Reached: 0.\n"))


class Ids(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "foresight").mkdir()
        (self.root / "research" / "signals").mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, name: str, text: str) -> None:
        (self.root / name).write_text(text, encoding="utf-8")

    def test_the_first_id_of_each_kind(self):
        for prefix in ("SC", "SP", "F"):
            code, text, _ = run(ids, [prefix, str(self.root / "foresight")])
            self.assertEqual((code, text), (0, f"{prefix}-001\n"))

    def test_the_next_id_is_one_more_than_the_highest_seen_mentions_included(self):
        self.write("foresight/2030-01-01-a.md", "### One\n- **Id:** SC-001\n- **From:** SG-002, IN-004\n\n### Two\n- **Id:** SC-002\n")
        self.write("foresight/forecasts.md", "| id | question |\n|---|---|\n| F-001 | q |\n| F-003 | q |\n")
        self.write("foresight/2030-02-01-b.md", "SC-007 was dropped in January; see F-003. Rule F1 and K2 are design rules, not ids.\n")
        self.assertEqual(run(ids, ["SC", str(self.root / "foresight")])[1], "SC-008\n")
        self.assertEqual(run(ids, ["f", str(self.root / "foresight")])[1], "F-004\n")
        self.assertEqual(run(ids, ["SP", str(self.root / "foresight")])[1], "SP-001\n")

    def test_list_shows_what_is_given_and_fails_on_an_id_given_twice(self):
        self.write("foresight/a.md", "### One\n- **Id:** SC-001\n")
        self.write("research/signals/s.md", "# Seen\n\n- **Id:** SG-001\n")
        code, text, _ = run(ids, ["--list", str(self.root / "foresight"), str(self.root / "research")])
        self.assertEqual(code, 0)
        self.assertEqual([line.split()[0] for line in text.splitlines()], ["SC-001", "SG-001"])
        self.write("foresight/b.md", "### Again\n- **Id:** SC-001\n")
        code, text, _ = run(ids, ["--list", str(self.root / "foresight")])
        self.assertEqual(code, 1)
        self.assertIn("GIVEN TWICE SC-001", text)

    def test_signal_ids_are_not_made_here(self):
        code, _, err = run(ids, ["SG", str(self.root / "research")])
        self.assertEqual(code, 2)
        self.assertIn("Signal ids come from poiesis-research", err)

    def test_a_placeholder_in_a_template_is_not_an_id_in_use(self):
        self.write("foresight/forecasts.md", (SKILL / "templates" / "forecasts.md").read_text(encoding="utf-8"))
        self.write("foresight/signposts.md", (SKILL / "templates" / "signposts.md").read_text(encoding="utf-8"))
        self.assertEqual(run(ids, ["F", str(self.root / "foresight")])[1], "F-001\n")
        self.assertEqual(run(ids, ["SP", str(self.root / "foresight")])[1], "SP-001\n")
        self.assertEqual(run(ids, ["SC", str(self.root / "foresight")])[1], "SC-001\n")

    def test_a_folder_that_is_not_there_yet_gives_the_first_id_and_says_so(self):
        code, text, err = run(ids, ["SC", str(self.root / "nothing-here")])
        self.assertEqual((code, text), (0, "SC-001\n"))
        self.assertIn("Not there yet", err)
        self.assertEqual(run(ids, ["--list", str(self.root / "nothing-here")])[0], 2)

    def test_an_unknown_prefix_or_no_place_is_an_error(self):
        self.assertEqual(run(ids, ["IN", str(self.root)])[0], 2)
        self.assertEqual(run(ids, ["SC"])[0], 2)


if __name__ == "__main__":
    unittest.main()
