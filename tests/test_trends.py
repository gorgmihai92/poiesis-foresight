"""trends.py: growth against a series' own past, the refusal of a share with different document types on its two
sides, the lab's recorded run reproduced number for number, and how earlier jumps went on."""
import json
import math
import statistics
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS, SERIES, lab, run

import trends

TYPED, EVERY = ("article", "preprint", "review"), ("all",)
CSV = str(SERIES.with_name(SERIES.name + ".csv"))


class Numbers(unittest.TestCase):
    def test_log_growth_needs_the_year_before_and_values_above_zero(self):
        g = trends.log_growth({2019: 10.0, 2020: 20.0, 2021: 0.0, 2022: 5.0, 2024: 6.0})
        self.assertEqual(sorted(g), [2020, 2021, 2022])
        self.assertAlmostEqual(g[2020], math.log(2))
        self.assertIsNone(g[2021])
        self.assertIsNone(g[2022])

    def test_yearly_rate_is_the_compound_rate(self):
        self.assertAlmostEqual(trends.yearly_rate({2015: 100.0, 2020: 200.0}, 2015, 2020), 2 ** 0.2 - 1)
        self.assertIsNone(trends.yearly_rate({2015: 100.0}, 2015, 2020))
        self.assertIsNone(trends.yearly_rate({2015: 0.0, 2020: 5.0}, 2015, 2020))

    def test_indicators_on_a_series_worked_by_hand(self):
        values = {2010 + i: v for i, v in enumerate([100.0, 110.0, 121.0, 115.0, 130.0, 150.0, 160.0, 200.0, 190.0, 260.0])}
        ind = trends.indicators(values, recent=2, baseline=5, span=3)
        growth = [math.log(values[y] / values[y - 1]) for y in range(2011, 2020)]
        past = growth[2:7]  # the five growth figures before 2018: 2013 to 2017
        self.assertEqual(ind["own_past"]["years"], [2013, 2017])
        self.assertAlmostEqual(ind["own_past"]["mean"], statistics.mean(past))
        self.assertAlmostEqual(ind["own_past"]["sd"], statistics.stdev(past))
        self.assertEqual(list(ind["recent"]), [2018, 2019])
        self.assertEqual(ind["recent"][2018]["level"], "fell")
        self.assertEqual(ind["recent"][2019]["level"], "rose")
        self.assertAlmostEqual(ind["recent"][2019]["z"], (growth[8] - statistics.mean(past)) / statistics.stdev(past))
        self.assertAlmostEqual(ind["recent"][2019]["change_pct"], 100 * (260 / 190 - 1))
        self.assertAlmostEqual(ind["rate"]["last"]["per_year"], (260 / 160) ** (1 / 3) - 1)
        self.assertAlmostEqual(ind["rate"]["previous"]["per_year"], (160 / 115) ** (1 / 3) - 1)
        self.assertEqual((ind["peak"]["year"], ind["peak"]["value"], ind["peak"]["now_below"]), (2017, 200.0, False))

    def test_a_recovery_after_a_dip_is_measured_from_the_earlier_peak(self):
        values = {2010 + i: v for i, v in enumerate([50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 60.0, 62.0, 70.0, 80.0])}
        ind = trends.indicators(values, recent=3, baseline=5)
        self.assertEqual([r["level"] for r in ind["recent"].values()], ["rose", "rose", "rose"])
        self.assertEqual(ind["peak"]["year"], 2015)
        self.assertTrue(ind["peak"]["now_below"])
        self.assertLess(ind["peak"]["per_year_since"], 0)
        self.assertIn("still below its earlier peak of 2015", trends.reading(ind))

    def test_too_short_a_past_gives_no_z_and_says_so(self):
        ind = trends.indicators({2020: 10.0, 2021: 12.0, 2022: 15.0, 2023: 15.0, 2024: 20.0})
        self.assertFalse(ind["own_past"]["usable"])
        self.assertTrue(all(r["z"] is None and r["pace"] is None for r in ind["recent"].values()))
        self.assertEqual(ind["recent"][2023]["level"], "unchanged")
        self.assertIn("too few earlier years", trends.reading(ind))

    def test_a_gap_in_the_years_is_refused(self):
        with self.assertRaises(trends.Refused) as stop:
            trends.indicators({2018: 1.0, 2019: 2.0, 2021: 3.0, 2022: 4.0})
        self.assertIn("no value for 2020", str(stop.exception))

    def test_the_z_limit_decides_the_word_and_nothing_else(self):
        values = {2000 + i: v for i, v in enumerate([10.0, 11.0, 12.0, 13.5, 14.5, 16.0, 17.5, 19.0, 21.0, 23.0, 25.0, 27.5, 30.0, 60.0])}
        loose, strict = trends.indicators(values, recent=1, z_limit=2.0), trends.indicators(values, recent=1, z_limit=1000.0)
        self.assertEqual(loose["recent"][2013]["z"], strict["recent"][2013]["z"])
        self.assertEqual((loose["recent"][2013]["pace"], strict["recent"][2013]["pace"]), ("above its own past", "within its own past"))


class Share(unittest.TestCase):
    def test_a_share_with_different_document_types_on_its_two_sides_is_refused(self):
        with self.assertRaises(trends.Refused) as stop:
            trends.share({2024: 3246, 2025: 4082}, {2024: 11003303, 2025: 14226691}, TYPED, EVERY)
        self.assertEqual(str(stop.exception), "a share needs the same document types on both sides: article, preprint, review above the line, all below")

    def test_a_share_that_does_not_say_what_it_counts_is_refused(self):
        with self.assertRaises(trends.Refused):
            trends.share({2024: 1}, {2024: 10}, "", "")

    def test_the_same_types_in_another_order_are_the_same(self):
        got = trends.share({2024: 5}, {2024: 1000}, "Review, article", ["article", "review"])
        self.assertAlmostEqual(got[2024], 500.0)


class RecordedRun(unittest.TestCase):
    """The run of 2026-11-17 kept in the Poiesis Lab notebook: openalex.json holds the counts as fetched, and
    analysis.json what fixtures/scripts/analyze.py computed from them."""

    @classmethod
    def setUpClass(cls):
        notebook = lab()
        if not notebook:
            raise unittest.SkipTest("the Poiesis Lab notebook is not on this machine (POIESIS_LAB, or ~/Poiesis Lab): the recorded run was not compared")
        folder = notebook / "fixtures" / "trend-scan"
        cls.data = json.loads((folder / "openalex.json").read_text(encoding="utf-8"))
        cls.want = json.loads((folder / "analysis.json").read_text(encoding="utf-8"))

    @staticmethod
    def full(counts: dict) -> dict[int, int]:
        """2010 to 2025: the run left 2026 out as an unfinished year."""
        return {int(y): n for y, n in counts.items() if 2010 <= int(y) <= 2025}

    def measures(self, area: str) -> dict[str, dict[int, float]]:
        s, total = self.data["series"][area], self.data["total"]
        return {"t": trends.share(self.full(s["typed"]), self.full(total["typed"]), TYPED, TYPED),
                "tn": trends.share(self.full(s["typed_narrow"]), self.full(total["typed"]), TYPED, TYPED),
                "ta": trends.share(self.full(s["broad"]), self.full(total["all"]), EVERY, EVERY),
                "tr": {y: float(n) for y, n in self.full(s["typed"]).items()}}

    def test_every_number_of_the_recorded_analysis_is_reproduced_for_every_area(self):
        compared = 0
        self.assertEqual(sorted(self.want), sorted(self.data["series"]))
        for area in self.want:
            measures = self.measures(area)
            for y, share in self.want[area]["share"].items():
                self.assertAlmostEqual(measures["t"][int(y)], share, places=9, msg=f"{area} share {y}")
                compared += 1
            for key, values in measures.items():
                got, want = trends.indicators(values, recent=3, baseline=10, span=5), self.want[area][key]
                self.assertEqual(got["own_past"]["years"], [2013, 2022])
                pairs = [("m", got["own_past"]["mean"]), ("sd", got["own_past"]["sd"]), ("c1", got["rate"]["previous"]["per_year"]), ("c2", got["rate"]["last"]["per_year"])]
                for name, value in pairs:
                    self.assertAlmostEqual(value, want[name], places=12, msg=f"{area} {key} {name}")
                for y in ("2023", "2024", "2025"):
                    self.assertAlmostEqual(got["recent"][int(y)]["growth"], want["g"][y], places=12, msg=f"{area} {key} g {y}")
                    self.assertAlmostEqual(got["recent"][int(y)]["z"], want["z"][y], places=12, msg=f"{area} {key} z {y}")
                compared += len(pairs) + 6
        self.assertEqual(compared, 5 * 16 + 5 * 4 * 10)

    def test_the_2025_jump_in_the_database_produces_no_false_trend(self):
        ssb, total = self.data["series"]["ssb"], self.data["total"]
        # the database: every record type grew far more than articles, reviews and preprints from 2024 to 2025
        self.assertAlmostEqual(100 * (total["all"]["2025"] / total["all"]["2024"] - 1), 29.3, places=1)
        self.assertAlmostEqual(100 * (total["typed"]["2025"] / total["typed"]["2024"] - 1), 17.9, places=1)
        # 1. articles over all works: refused, not computed
        with self.assertRaises(trends.Refused):
            trends.share(self.full(ssb["typed"]), self.full(total["all"]), TYPED, EVERY)
        # 2. on the same types, solid-state batteries rose in each recent year, within their own past
        read = trends.indicators(self.measures("ssb")["t"])
        self.assertEqual([r["level"] for r in read["recent"].values()], ["rose", "rose", "rose"])
        self.assertEqual({r["pace"] for r in read["recent"].values()}, {"within its own past"})
        sentence = trends.reading(read)
        self.assertEqual(sentence, "rose in 2023, 2024 and 2025; growth within its own past in 2023, 2024 and 2025; 29.0% a year over 2015–2020, 12.8% over 2020–2025.")
        for word in ("fell", "declin", "below"):
            self.assertNotIn(word, sentence)
        # 3. the trap is in the data: among all record types the share fell in 2025, far below its own past
        trap = trends.indicators(self.measures("ssb")["ta"])["recent"][2025]
        self.assertEqual(trap["level"], "fell")
        self.assertLess(trap["z"], -2.5)

    def test_one_area_stands_out_and_it_is_not_called_a_trend(self):
        sentences = {area: trends.reading(trends.indicators(self.measures(area)["t"])) for area in self.want}
        above = [area for area, s in sentences.items() if "above its own past" in s]
        self.assertEqual(above, ["synbio"])
        self.assertIn("growth above its own past in 2025", sentences["synbio"])
        for s in sentences.values():
            for word in ("trend", "emerging", "booming", "declin"):
                self.assertNotIn(word, s)


class OnAResearchSeries(unittest.TestCase):
    def test_the_replayed_series_is_read_with_the_unfinished_year_left_out(self):
        code, text, err = run(trends, [CSV, "--json"])
        self.assertEqual((code, err), (0, ""))
        found = json.loads(text)
        self.assertEqual(found["source"], "OpenAlex, fetched 2026-11-21, by counts.py 2.4.0")
        ssb, quantum = found["series"]
        self.assertEqual((ssb["id"], quantum["id"]), ("solid-state-batteries", "quantum-computing"))
        self.assertEqual(ssb["left_out"], [2026])
        share = ssb["measures"]["share"]
        self.assertEqual(share["years"], [2015, 2025])
        self.assertEqual(list(share["recent"]), ["2023", "2024", "2025"])
        self.assertAlmostEqual(share["recent"]["2025"]["value"], 1e5 * 1996 / 7849714)
        self.assertAlmostEqual(share["recent"]["2025"]["growth"], math.log((1996 / 7849714) / (1446 / 6651317)))
        self.assertEqual(share["own_past"]["years"], [2016, 2022])
        self.assertEqual(ssb["small"]["years"], [])

    def test_the_share_among_all_record_types_is_shown_as_a_check_and_never_read(self):
        _, text, _ = run(trends, [CSV, "--json", "--series", "solid-state-batteries"])
        ssb = json.loads(text)["series"][0]
        check = ssb["checks"]["share_all_types"]
        self.assertEqual(check["recent"]["2025"]["level"], "fell")  # 18.55 to 18.33 per 100,000 among all record types
        self.assertEqual(ssb["measures"]["share"]["recent"]["2025"]["level"], "rose")  # 21.74 to 25.43 on the same types
        self.assertTrue(ssb["reading"].startswith("rose in 2023, 2024 and 2025"))
        self.assertNotIn("fell", ssb["reading"])
        self.assertIn("not read", check["what"])
        grew = check["base_growth_pct"]["2025"]
        self.assertGreater(grew["all_types"], grew["counted_types"] + 10)  # the base of all types grew faster than the counted types
        part = check["counted_types_part"]
        self.assertLess(part["2025"]["base"], part["2022"]["base"])

    def test_the_printed_report_names_the_checks_as_checks(self):
        code, text, _ = run(trends, [CSV, "--series", "solid-state-batteries"])
        self.assertEqual(code, 0)
        self.assertIn("Left out: 2026 (not over).", text)
        self.assertIn("Reading: rose in 2023, 2024 and 2025;", text)
        self.assertEqual(text.count("Check, not read."), 2)
        self.assertIn("The two sides are not made of the same kinds of record.", text)
        for word in ("trend", "emerging", "declin"):
            self.assertNotIn(word, text.lower())

    def test_a_refused_series_is_not_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            for tail in (".csv", ".types.csv"):
                (Path(tmp) / (SERIES.name + tail)).write_bytes(SERIES.with_name(SERIES.name + tail).read_bytes())
            meta = json.loads(SERIES.with_name(SERIES.name + ".meta.json").read_text(encoding="utf-8"))
            meta["share"]["denominator_types"] = ["all"]
            (Path(tmp) / (SERIES.name + ".meta.json")).write_text(json.dumps(meta), encoding="utf-8")
            code, text, err = run(trends, [str(Path(tmp) / (SERIES.name + ".csv"))])
        self.assertEqual((code, text), (2, ""))
        self.assertIn("series_gate.py refused it", err)
        self.assertIn("the share counts different document types on its two sides", err)

    def test_an_unknown_series_id_is_refused_with_the_ids_the_file_has(self):
        code, _, err = run(trends, [CSV, "--series", "nothing"])
        self.assertEqual(code, 2)
        self.assertIn("solid-state-batteries, quantum-computing", err)

    def test_it_runs_isolated_with_the_standard_library_only(self):
        done = subprocess.run([sys.executable, "-I", str(SCRIPTS / "trends.py"), CSV], capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("Quantum computing (quantum-computing)", done.stdout)


class OwnTable(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def table(self, text: str) -> str:
        path = self.tmp / "mine.csv"
        path.write_text(text, encoding="utf-8")
        return str(path)

    ROWS = "".join(f"visits,{2016 + i},{c},{b}\n" for i, (c, b) in enumerate([(40, 1000), (44, 1000), (50, 1100), (52, 1100), (60, 1200), (66, 1200), (80, 1300), (90, 1300), (130, 1400), (40, 400)]))

    def test_a_table_must_say_which_years_are_full(self):
        code, _, err = run(trends, ["--own", self.table("series,year,count\nvisits,2024,5\nvisits,2025,7\n")])
        self.assertEqual(code, 2)
        self.assertIn("does not say which years are full", err)

    def test_a_share_needs_both_sides_named_and_the_same(self):
        path = self.table("series,year,count,base\n" + self.ROWS)
        code, _, err = run(trends, ["--own", path, "--last-full-year", "2024"])
        self.assertEqual(code, 2)
        self.assertIn("say what is counted above the line (--above) and below it (--below)", err)
        code, _, err = run(trends, ["--own", path, "--last-full-year", "2024", "--above", "article, review, preprint", "--below", "all works"])
        self.assertEqual(code, 2)
        self.assertIn("a share needs the same document types on both sides", err)

    def test_the_same_kinds_on_both_sides_give_a_share_and_the_last_year_is_left_out(self):
        path = self.table("series,year,count,base\n" + self.ROWS)
        code, text, err = run(trends, ["--own", path, "--last-full-year", "2024", "--above", "sessions", "--below", "Sessions", "--json", "--baseline", "5"])
        self.assertEqual((code, err), (0, ""))
        visits = json.loads(text)["series"][0]
        self.assertEqual(visits["left_out"], [2025])
        self.assertAlmostEqual(visits["measures"]["share"]["recent"]["2024"]["value"], 1e5 * 130 / 1400)
        self.assertNotIn("share_all_types", visits["checks"])

    def test_a_count_with_no_base_is_read_as_a_count_and_says_so(self):
        path = self.table("series,year,count,partial\n" + "".join(f"signups,{2015 + i},{c},{'true' if i == 9 else 'false'}\n" for i, c in enumerate([5, 6, 6, 8, 9, 9, 11, 12, 15, 4])))
        code, text, _ = run(trends, ["--own", path])
        self.assertEqual(code, 0)
        self.assertIn("Count: a count with no base", text)
        self.assertIn("Small numbers: fewer than 20 works in 2021, 2022, 2023", text)
        self.assertIn("Left out: 2024 (not over).", text)

    def test_a_table_without_the_needed_columns_or_with_words_for_numbers_is_refused(self):
        self.assertEqual(run(trends, ["--own", self.table("year,works\n2024,5\n"), "--last-full-year", "2024"])[0], 2)
        code, _, err = run(trends, ["--own", self.table("series,year,count\na,2024,many\n"), "--last-full-year", "2024"])
        self.assertEqual(code, 2)
        self.assertIn("line 2", err)

    def test_one_input_and_only_one(self):
        self.assertEqual(run(trends, [])[0], 2)
        self.assertEqual(run(trends, [CSV, "--own", CSV])[0], 2)


class BaseRate(unittest.TestCase):
    """Four invented series, each steady for six years, then a jump in 2016, then one of the four outcomes."""
    STEADY = [100.0, 105.0, 109.0, 115.0, 120.0, 127.0, 132.0]   # 2009 to 2015
    AFTER = {"faster": [200.0, 240.0, 300.0, 390.0], "kept": [200.0, 205.0, 208.0, 210.0], "part": [200.0, 180.0, 160.0, 150.0], "back": [200.0, 150.0, 120.0, 110.0]}

    def table(self, tmp: str, extra: str = "") -> str:
        lines = ["series,year,count"]
        for name, tail in self.AFTER.items():
            lines += [f"{name},{2009 + i},{v}" for i, v in enumerate(self.STEADY + tail)]
        path = Path(tmp) / "class.csv"
        path.write_text("\n".join(lines) + "\n" + extra, encoding="utf-8")
        return str(path)

    def test_each_outcome_is_told_apart(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, text, err = run(trends, ["--own", self.table(tmp), "--last-full-year", "2019", "--base-rate", "--json", "--baseline", "5"])
        self.assertEqual((code, err), (0, ""))
        found = json.loads(text)["base_rate"]
        self.assertEqual((found["series_searched"], found["counted"], found["enough_for_a_rate"]), (4, 4, False))
        by_series = {c["series"]: (c["year"], c["outcome"]) for c in found["cases"]}
        self.assertEqual(by_series, {"faster": (2016, "kept growing faster than before the jump"), "kept": (2016, "kept the gain, at its earlier pace or slower"),
                                     "part": (2016, "gave back part of the gain"), "back": (2016, "fell back to where it started or lower")})
        self.assertEqual(sorted(found["outcomes"].values()), [1, 1, 1, 1])

    def test_a_jump_too_recent_to_follow_is_listed_and_not_counted(self):
        late = "".join(f"late,{2009 + i},{v}\n" for i, v in enumerate([100.0, 105.0, 109.0, 115.0, 120.0, 127.0, 132.0, 139.0, 145.0, 150.0, 300.0]))
        with tempfile.TemporaryDirectory() as tmp:
            _, text, _ = run(trends, ["--own", self.table(tmp, late), "--last-full-year", "2019", "--base-rate", "--json", "--baseline", "5"])
        found = json.loads(text)["base_rate"]
        self.assertEqual(found["counted"], 4)
        self.assertEqual([(c["year"], c["outcome"]) for c in found["cases"] if c["series"] == "late"], [(2019, "too recent to tell")])

    def test_small_numbers_and_left_out_series_are_not_counted(self):
        small = "".join(f"small,{2009 + i},{v}\n" for i, v in enumerate([1.0, 1.05, 1.09, 1.15, 1.2, 1.27, 1.32, 2.0, 2.4, 3.0, 3.9]))
        with tempfile.TemporaryDirectory() as tmp:
            _, text, _ = run(trends, ["--own", self.table(tmp, small), "--last-full-year", "2019", "--base-rate", "--json", "--baseline", "5", "--leave-out", "back"])
        found = json.loads(text)["base_rate"]
        self.assertEqual((found["series_searched"], found["counted"]), (4, 3))
        self.assertEqual([c["outcome"] for c in found["cases"] if c["series"] == "small"], ["left out: too few works in the jump year"])
        self.assertNotIn("back", {c["series"] for c in found["cases"]})

    def test_few_cases_are_listed_and_not_called_a_rate(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, text, _ = run(trends, ["--own", self.table(tmp), "--last-full-year", "2019", "--base-rate", "--baseline", "5"])
        self.assertIn("Jumps with 3 years to look at: 4.", text)
        self.assertIn("Fewer than 20 jumps: too few to call a rate.", text)
        self.assertNotIn("%", text)

    def test_the_years_after_a_counted_jump_belong_to_it(self):
        found = trends.jumps({2009 + i: v for i, v in enumerate(self.STEADY + self.AFTER["faster"])}, None, jump=2.0, after=3, baseline=5, min_count=20)
        self.assertEqual([c["year"] for c in found], [2016])


if __name__ == "__main__":
    unittest.main()
