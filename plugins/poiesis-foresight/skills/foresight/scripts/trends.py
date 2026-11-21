#!/usr/bin/env python3
"""How a yearly series moved, measured against its own past. Run with `python3 -I`.

  trends.py research/data/NAME.csv [--series ID]      a series saved by poiesis-research's counts.py
  trends.py --own TABLE.csv --last-full-year 2025 [--above "articles" --below "articles"]
                                                      your own table: series,year,count[,base][,partial]
  trends.py research/data/NAME.csv --base-rate        how earlier jumps in the file's series went on

A series from poiesis-research must pass series_gate.py first; a refused series is not read. The unfinished year
is left out. For each series the script gives, for the last full years (--recent, 3):
  - the change from the year before, and how far it is from the series' own earlier growth, in standard
    deviations (z), against the growth of the years before (--baseline, 10);
  - the yearly rate over the last --span years (5) and over the --span years before them;
  - the earlier peak and the yearly rate since it, so a recovery from a dip is not read as a rise.
The measure that is read is the share: the count per 100,000 works of the base, with the same document types
above and below the line. A share with different types on its two sides is refused. The raw count and the
share among all record types are printed as checks and are not read.

The words it prints are fixed by rule: "rose" or "fell" is the sign of the change; "above", "within" or "below
its own past" is z against --z (2). That limit, the windows and --min-count (20) are choices, not findings.
It does not say "trend" or "emerging": whether a series is one is decided in the playbook, after the challenge.

Exit code 0, or 2 when a series is refused or cannot be read.
"""
import argparse
import csv
import json
import math
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import series_gate as gate  # noqa: E402

MIN_BASELINE = 5   # fewer earlier growth figures than this give no z: a choice
MIN_CASES = 20     # fewer jumps than this are listed and not called a rate: a choice
ALL = ("all",)


class Refused(Exception):
    """A series or a share that must not be read."""


# --- The numbers -----------------------------------------------------------------------------


def kinds(text) -> tuple[str, ...]:
    """What is counted, as a sorted tuple of lower-case names: "Review, article" and ["article", "review"] agree."""
    items = text if isinstance(text, (list, tuple)) else str(text).split(",")
    return tuple(sorted(str(i).strip().lower() for i in items if str(i).strip()))


def share(count: dict, base: dict, above, below) -> dict[int, float]:
    """The count per 100,000 of the base, year by year. Both sides must count the same kinds of record."""
    if kinds(above) != kinds(below) or not kinds(above):
        raise Refused(f"a share needs the same document types on both sides: {', '.join(kinds(above)) or 'not said'} above the line, "
                      f"{', '.join(kinds(below)) or 'not said'} below")
    return {y: 1e5 * count.get(y, 0) / base[y] for y in sorted(base) if base[y]}


def log_growth(values: dict[int, float]) -> dict[int, float | None]:
    """ln(this year / last year) for every year that has a year before it; None where either value is not above zero."""
    out: dict[int, float | None] = {}
    for y in sorted(values):
        if y - 1 in values:
            out[y] = math.log(values[y] / values[y - 1]) if values[y] > 0 and values[y - 1] > 0 else None
    return out


def yearly_rate(values: dict[int, float], start: int, end: int) -> float | None:
    """The compound yearly rate from one year to another; None when a year is missing or a value is not above zero."""
    if start not in values or end not in values or end <= start or values[start] <= 0 or values[end] <= 0:
        return None
    return (values[end] / values[start]) ** (1 / (end - start)) - 1


def own_past(growth: dict[int, float | None], before: int, baseline: int) -> dict:
    """Mean and standard deviation of the growth figures of up to `baseline` years before `before`."""
    years = [y for y in sorted(growth) if y < before][-baseline:]
    usable = len(years) >= MIN_BASELINE and all(growth[y] is not None for y in years)
    figures = [growth[y] for y in years] if usable else []
    sd = statistics.stdev(figures) if usable else None
    return {"years": [years[0], years[-1]] if years else None, "n": len(years), "mean": statistics.mean(figures) if usable else None, "sd": sd,
            "usable": bool(usable and sd)}


def indicators(values: dict[int, float], recent: int = 3, baseline: int = 10, span: int = 5, z_limit: float = 2.0) -> dict:
    """The indicators of one measure. `values` holds full years only."""
    years = sorted(values)
    gaps = [y for y in range(years[0], years[-1] + 1) if y not in values]
    if gaps:
        raise Refused("the series has no value for " + ", ".join(map(str, gaps)) + ": growth from year to year cannot be computed across a gap")
    last = years[-1]
    growth = log_growth(values)
    window = [y for y in years[-recent:] if y in growth]
    if not window:
        raise Refused("the series has fewer than two full years")
    past = own_past(growth, window[0], baseline)
    rows = {}
    for y in window:
        g = growth[y]
        z = (g - past["mean"]) / past["sd"] if past["usable"] and g is not None else None
        rows[y] = {"value": values[y], "growth": g, "change_pct": None if g is None else 100 * (math.exp(g) - 1), "z": z,
                   "level": None if g is None else "rose" if g > 0 else "fell" if g < 0 else "unchanged",
                   "pace": None if z is None else "above its own past" if z >= z_limit else "below its own past" if z <= -z_limit else "within its own past"}
    earlier = {y: values[y] for y in years if y < window[0]}
    peak_year = max(earlier, key=lambda y: (earlier[y], y)) if earlier else None
    return {
        "years": [years[0], last], "own_past": past, "recent": rows, "z_limit": z_limit,
        "rate": {"previous": {"from": last - 2 * span, "to": last - span, "per_year": yearly_rate(values, last - 2 * span, last - span)},
                 "last": {"from": last - span, "to": last, "per_year": yearly_rate(values, last - span, last)}},
        "peak": None if peak_year is None else {"year": peak_year, "value": earlier[peak_year], "per_year_since": yearly_rate(values, peak_year, last),
                                               "now_below": values[last] < earlier[peak_year]},
    }


def reading(ind: dict) -> str:
    """One sentence from the indicators, by fixed rules. No word here goes beyond what was computed."""
    rows = ind["recent"]

    def listed(years: list[int]) -> str:
        names = [str(y) for y in years]
        return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]

    parts = []
    for word in ("rose", "fell", "unchanged"):
        hit = [y for y, r in rows.items() if r["level"] == word]
        if hit:
            parts.append(("was unchanged" if word == "unchanged" else word) + " in " + listed(hit))
    for word in ("above its own past", "below its own past", "within its own past"):
        hit = [y for y, r in rows.items() if r["pace"] == word]
        if hit:
            parts.append(f"growth {word} in " + listed(hit))
    if not ind["own_past"]["usable"]:
        parts.append(f"too few earlier years to compare its growth with its own past ({ind['own_past']['n']}, and {MIN_BASELINE} are asked)")
    last, previous = ind["rate"]["last"], ind["rate"]["previous"]
    if last["per_year"] is not None and previous["per_year"] is not None:
        parts.append(f"{100 * previous['per_year']:.1f}% a year over {previous['from']}–{previous['to']}, {100 * last['per_year']:.1f}% over {last['from']}–{last['to']}")
    peak = ind["peak"]
    if peak and peak["now_below"]:
        parts.append(f"still below its earlier peak of {peak['year']}")
    return "; ".join(parts) + "."


# --- Reading the files -----------------------------------------------------------------------


def research_series(path: Path) -> tuple[dict, list[dict]]:
    """The series of a file saved by counts.py, after the entry gate. Returns (facts about the file, series)."""
    found = gate.check(path)
    if not found["accepted"]:
        raise Refused("series_gate.py refused it:\n" + "\n".join("  - " + r for r in found["reasons"]))
    facts = found["facts"]
    _, rows = gate.read_rows(Path(facts["data"]))
    key, label = ("series", "label") if facts["kind"] == "series" else ("topic_id", "topic")
    out: dict[str, dict] = {}
    for r in rows:
        s = out.setdefault(r[key], {"id": r[key], "label": r[label], "left_out": [], "count": {}, "base": {}, "count_all": {}, "base_all": {}})
        year = int(r["year"])
        if r["partial"] == "true":
            s["left_out"].append(year)
            continue
        s["count"][year], s["base"][year] = int(r["count"]), int(r["base"])
        if facts["kind"] == "series":
            s["count_all"][year], s["base_all"][year] = int(r["count_all_types"]), int(r["base_all_types"])
    return facts, list(out.values())


def own_series(path: Path, last_full_year: int | None) -> list[dict]:
    """The user's own table: series,year,count[,base][,partial]. It must say which years are full."""
    try:
        header, rows = gate.read_rows(path)
    except (OSError, csv.Error, UnicodeDecodeError) as e:
        raise Refused(f"the table cannot be read ({e})")
    need = [c for c in ("series", "year", "count") if c not in header]
    if need:
        raise Refused("the table needs the columns series, year, count (and base for a share); it has no " + ", ".join(need))
    if "partial" not in header and last_full_year is None:
        raise Refused("the table does not say which years are full: give --last-full-year, or add a `partial` column with true or false")
    out: dict[str, dict] = {}
    for n, r in enumerate(rows, start=2):
        try:
            year, count = int(r["year"]), float(r["count"])
            base = float(r["base"]) if "base" in header and str(r["base"]).strip() else None
        except (TypeError, ValueError):
            raise Refused(f"line {n} of the table has a year, a count or a base that is not a number")
        s = out.setdefault(r["series"], {"id": r["series"], "label": r.get("label") or r["series"], "left_out": [], "count": {}, "base": {}})
        if (r.get("partial") or "").strip().lower() == "true" or (last_full_year is not None and year > last_full_year):
            s["left_out"].append(year)
            continue
        s["count"][year] = count
        if base is not None:
            s["base"][year] = base
    return list(out.values())


def composition(s: dict, years: list[int]) -> dict:
    """Of all record types, how much is of the counted types: in the series and in the base."""
    return {y: {"series": s["count"][y] / s["count_all"][y] if s["count_all"].get(y) else None,
                "base": s["base"][y] / s["base_all"][y] if s["base_all"].get(y) else None} for y in years}


def analyse(s: dict, above, below, a) -> dict:
    """Every measure of one series: the share that is read, and the checks beside it."""
    settings = dict(recent=a.recent, baseline=a.baseline, span=a.span, z_limit=a.z)
    out = {"id": s["id"], "label": s["label"], "left_out": sorted(s["left_out"]), "measures": {}, "checks": {}}
    if s["base"]:
        ind = indicators(share(s["count"], s["base"], above, below), **settings)
        out["measures"]["share"] = {"what": f"per 100,000 of the base, counting {', '.join(kinds(above))} above and below the line", **ind}
        out["checks"]["count"] = {"what": "the raw count above the line; it moves with the database as well as with the subject",
                                  **indicators({y: float(v) for y, v in s["count"].items()}, **settings),
                                  "base_growth_pct": {y: 100 * (s["base"][y] / s["base"][y - 1] - 1) for y in ind["recent"] if s["base"].get(y - 1)}}
    else:
        ind = indicators({y: float(v) for y, v in s["count"].items()}, **settings)
        out["measures"]["count"] = {"what": "a count with no base: it moves with the size of its source as well as with the subject", **ind}
    recent = list(ind["recent"])
    out["reading"] = reading(ind)
    small = [y for y in recent if s["count"][y] < a.min_count]
    out["small"] = {"years": small, "min_count": a.min_count}
    if s.get("count_all") and kinds(above) != ALL:
        every = indicators(share(s["count_all"], s["base_all"], ALL, ALL), **settings)
        out["checks"]["share_all_types"] = {
            "what": "the share among all record types; not read, because the two sides are not made of the same kinds of record",
            **every, "counted_types_part": composition(s, [recent[0] - 1, *recent] if recent[0] - 1 in s["count"] else recent),
            "base_growth_pct": {y: {"counted_types": 100 * (s["base"][y] / s["base"][y - 1] - 1), "all_types": 100 * (s["base_all"][y] / s["base_all"][y - 1] - 1)}
                                for y in recent if s["base"].get(y - 1) and s["base_all"].get(y - 1)}}
    return out


# --- Base rate -------------------------------------------------------------------------------

OUTCOMES = ("kept growing faster than before the jump", "kept the gain, at its earlier pace or slower",
            "gave back part of the gain", "fell back to where it started or lower")


def jumps(values: dict[int, float], counts: dict | None, jump: float, after: int, baseline: int, min_count: int) -> list[dict]:
    """The years in which a series grew at least `jump` standard deviations faster than its own earlier growth,
    and what its level was `after` years later. A jump inside the years that follow a counted one belongs to it."""
    years, growth, found, busy_until = sorted(values), log_growth(values), [], None
    for y in years:
        if growth.get(y) is None or (busy_until is not None and y <= busy_until):
            continue
        past = own_past(growth, y, baseline)
        if not past["usable"]:
            continue
        z = (growth[y] - past["mean"]) / past["sd"]
        if z < jump:
            continue
        case = {"year": y, "z": z}
        if y + after > years[-1]:
            case["outcome"] = "too recent to tell"
        elif counts is not None and counts.get(y, 0) < min_count:
            case["outcome"] = "left out: too few works in the jump year"
        else:
            before, at, later = values[y - 1], values[y], values[y + after]
            pace = math.log(later / at) / after if later > 0 else None
            case["outcome"] = (OUTCOMES[3] if later <= before else OUTCOMES[2] if later < at
                               else OUTCOMES[0] if pace is not None and pace > past["mean"] else OUTCOMES[1])
            busy_until = y + after
        found.append(case)
    return found


def base_rate(series: list[dict], above, below, a) -> dict:
    cases = []
    for s in series:
        if s["id"] in a.leave_out:
            continue
        values = share(s["count"], s["base"], above, below) if s["base"] else {y: float(v) for y, v in s["count"].items()}
        years = sorted(values)
        if not years or any(y not in values for y in range(years[0], years[-1] + 1)):
            continue
        cases += [{"series": s["id"], "label": s["label"], **c} for c in jumps(values, s["count"], a.jump, a.after, a.baseline, a.min_count)]
    counted = [c for c in cases if c["outcome"] in OUTCOMES]
    return {"series_searched": sum(1 for s in series if s["id"] not in a.leave_out), "left_out_series": sorted(a.leave_out), "jump": a.jump, "after": a.after,
            "min_cases": MIN_CASES, "counted": len(counted), "enough_for_a_rate": len(counted) >= MIN_CASES,
            "outcomes": {o: sum(1 for c in counted if c["outcome"] == o) for o in OUTCOMES}, "cases": cases}


# --- Printing --------------------------------------------------------------------------------


def signed(x: float | None, digits: int = 1, unit: str = "%") -> str:
    return "n/a" if x is None else f"{x:+.{digits}f}{unit}"


def table(ind: dict, number: str) -> list[str]:
    past = ind["own_past"]
    if past["usable"]:
        head = f"own past {past['years'][0]}–{past['years'][1]}: {signed(100 * (math.exp(past['mean']) - 1))} a year on average"
    else:
        head = f"own past: {past['n']} earlier growth figures, too few to compare with ({MIN_BASELINE} are asked)"
    lines = [f"  ({head})"]
    for y, r in ind["recent"].items():
        z = "" if r["z"] is None else f"   z {r['z']:+.1f}, {r['pace']}"
        lines.append(f"  {y}   {format(r['value'], number)}   {signed(r['change_pct'])}{z}")
    return lines


def show(out: dict, header: str) -> None:
    print(f"{out['label']} ({out['id']}) · {header}")
    left = ", ".join(map(str, out["left_out"]))
    for name, m in out["measures"].items():
        print(f"Full years {m['years'][0]}–{m['years'][1]}." + (f" Left out: {left} (not over)." if left else ""))
        print(("Share " if name == "share" else "Count: ") + m["what"])
        print("\n".join(table(m, ",.2f" if name == "share" else ",.0f")))
        if m["peak"]:
            p = m["peak"]
            print(f"  Earlier peak: {p['value']:,.2f} in {p['year']}; {signed(None if p['per_year_since'] is None else 100 * p['per_year_since'])} a year since.")
    print("Reading: " + out["reading"])
    if out["small"]["years"]:
        print(f"Small numbers: fewer than {out['small']['min_count']} works in " + ", ".join(map(str, out["small"]["years"])) + ": a few works move the figures.")
    for name, c in out["checks"].items():
        if name == "count":
            grew = ", ".join(f"{y}: {signed(v)}" for y, v in c["base_growth_pct"].items())
            print("Check, not read. Raw count: " + ", ".join(f"{y}: {r['value']:,.0f} ({signed(r['change_pct'])})" for y, r in c["recent"].items()) + f". The base itself grew {grew}.")
        else:
            part = c["counted_types_part"]
            years = list(part)
            pct = lambda v: "n/a" if v is None else f"{100 * v:.1f}%"  # noqa: E731
            print("Check, not read. Share among all record types: " + ", ".join(f"{y}: {r['value']:,.2f} ({signed(r['change_pct'])})" for y, r in c["recent"].items()) + ".")
            print(f"  Of all records, the counted types are {pct(part[years[0]]['base'])} of the base in {years[0]} and {pct(part[years[-1]]['base'])} in {years[-1]}; "
                  f"of the series, {pct(part[years[0]]['series'])} and {pct(part[years[-1]]['series'])}. The two sides are not made of the same kinds of record.")
    print()


def show_base_rate(found: dict, header: str) -> None:
    print(f"Base rate · {header}")
    print(f"A jump: a year whose growth was at least {found['jump']:g} standard deviations above the series' own earlier growth. What followed is read {found['after']} years later.")
    print(f"Series searched: {found['series_searched']}. Jumps with {found['after']} years to look at: {found['counted']}.")
    for outcome, n in found["outcomes"].items():
        print(f"  {n:>4}  {outcome}")
    if not found["enough_for_a_rate"]:
        print(f"Fewer than {found['min_cases']} jumps: too few to call a rate. They are listed below as cases.")
    for c in found["cases"]:
        print(f"  - {c['label']} ({c['series']}) {c['year']}: z {c['z']:+.1f} · {c['outcome']}")
    print()


# --- Main ------------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", nargs="?", type=Path, help="a series saved by counts.py (NAME.csv)")
    p.add_argument("--own", type=Path, help="your own table: series,year,count[,base][,partial]")
    p.add_argument("--above", help="with --own and a base: what is counted above the line")
    p.add_argument("--below", help="with --own and a base: what is counted below the line")
    p.add_argument("--last-full-year", type=int, help="with --own: years after this one are left out")
    p.add_argument("--series", action="append", default=[], help="only this series id (repeat for more)")
    p.add_argument("--recent", type=int, default=3, help="how many last full years to read (default 3)")
    p.add_argument("--baseline", type=int, default=10, help="how many earlier growth figures make up the series' own past (default 10)")
    p.add_argument("--span", type=int, default=5, help="years in each of the two yearly rates (default 5)")
    p.add_argument("--z", type=float, default=2.0, help="standard deviations beyond which growth is called above or below its own past (default 2: a choice)")
    p.add_argument("--min-count", type=int, default=20, help="fewer works than this in a year are flagged as small numbers (default 20: a choice)")
    p.add_argument("--base-rate", action="store_true", help="how earlier jumps in the file's series went on")
    p.add_argument("--jump", type=float, default=2.0, help="with --base-rate: how many standard deviations make a jump (default 2: a choice)")
    p.add_argument("--after", type=int, default=3, help="with --base-rate: how many years later the outcome is read (default 3)")
    p.add_argument("--leave-out", action="append", default=[], help="with --base-rate: a series id that is not part of the reference class")
    p.add_argument("--json", action="store_true", help="print everything as JSON")
    a = p.parse_args(argv)
    if bool(a.file) == bool(a.own):
        p.error("give a series saved by counts.py, or --own with your own table (one of the two)")
    if min(a.recent, a.baseline, a.span, a.after) < 1:
        p.error("--recent, --baseline, --span and --after are whole numbers above zero")
    try:
        if a.own:
            series = own_series(a.own, a.last_full_year)
            with_base = any(s["base"] for s in series)
            if with_base and not (a.above and a.below):
                raise Refused("the table has a base: say what is counted above the line (--above) and below it (--below)")
            above, below = (a.above, a.below) if with_base else (None, None)
            header = f"your own table {a.own.name}" + (f"; above the line: {a.above}; below: {a.below}" if with_base else "")
        else:
            facts, series = research_series(a.file)
            above = below = facts["types_above"]
            header = f"{facts['database']}, fetched {facts['fetched']}, by {facts['script']}"
        wanted = [s for s in series if not a.series or s["id"] in a.series]
        missing = [i for i in a.series if i not in {s["id"] for s in series}]
        if missing:
            raise Refused("no series named " + ", ".join(missing) + "; the file has " + ", ".join(s["id"] for s in series))
        if a.base_rate:
            result = base_rate(wanted, above, below, a)
        else:
            result = [analyse(s, above, below, a) for s in wanted]
    except Refused as e:
        print(f"Refused: {e}", file=sys.stderr)
        return 2
    if a.json:
        json.dump({"source": header, "base_rate" if a.base_rate else "series": result}, sys.stdout, ensure_ascii=False, indent=1)
        print()
    elif a.base_rate:
        show_base_rate(result, header)
    else:
        for out in result:
            show(out, header)
    return 0


if __name__ == "__main__":
    sys.exit(main())
