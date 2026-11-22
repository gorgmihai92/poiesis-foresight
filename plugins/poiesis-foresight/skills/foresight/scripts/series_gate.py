#!/usr/bin/env python3
"""Check a yearly series from poiesis-research before anything is built on it. Run with `python3 -I`.

  series_gate.py research/data/NAME.csv [more files …]     NAME.meta.json works too
  series_gate.py research/data/NAME.csv --json

A series is accepted only when the metadata file beside it (NAME.meta.json, written by poiesis-research's
counts.py) says all of this:
  - which database the counts came from, with a Coverage line in which that database answered;
  - that the run was complete;
  - which document types were counted above and below the line of the share, and that they are the same;
  - the date fetched, the years, the years that were not over, the series and the script that made them.
The numbers are then checked against the labels: each count in NAME.csv must be the sum of the declared types in
NAME.types.csv, above and below the line; each share must be its count over its base; and a year that was not
over when the series was fetched must be marked partial. A series whose metadata lists a types file that is not
there is refused. A series counts.py saved without one (Europe PMC) is accepted, and the line says the counts
were not checked.

One line per file, ACCEPTED or REFUSED, with every reason. Exit code 0 when every series is accepted, 1 when one
is refused. This script changes nothing and asks no database.
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

REQUIRED = ("database", "fetched", "years", "partial_years", "share", "series", "script", "coverage", "complete")
SERIES_COLUMNS = ("series", "label", "year", "partial", "count", "base", "share_per_100k", "count_all_types", "base_all_types", "share_all_types_per_100k")
TAXONOMY_COLUMNS = ("topic_id", "topic", "year", "partial", "count", "base", "share_per_100k")
ALL = ("all",)
SHOWN = 3  # how many mismatching rows a reason names before it only counts them


def stem(path: Path) -> Path:
    """NAME for NAME.csv, NAME.types.csv or NAME.meta.json, in the same folder."""
    name = path.name
    for tail in (".meta.json", ".types.csv", ".csv"):
        if name.endswith(tail):
            return path.with_name(name[: -len(tail)])
    return path


def types_of(value) -> tuple[str, ...] | None:
    """Document types as a sorted tuple of lower-case names; None when the field is not a list of names."""
    if not isinstance(value, list) or not value or not all(isinstance(t, str) and t.strip() for t in value):
        return None
    return tuple(sorted(t.strip().lower() for t in value))


def named(types: tuple[str, ...]) -> str:
    return "every document type" if types == ALL else ", ".join(types)


def read_rows(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="", encoding="utf-8-sig") as f:  # a byte-order mark is not part of the first column's name
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def some(items: list[str]) -> str:
    more = len(items) - SHOWN
    return "; ".join(items[:SHOWN]) + (f"; and {more} more" if more > 0 else "")


def check(path: Path) -> dict:
    """Everything the gate found for one series file: {"name", "accepted", "reasons", "facts"}."""
    base = stem(path)
    meta_path, csv_path, types_path = (base.with_name(base.name + t) for t in (".meta.json", ".csv", ".types.csv"))
    reasons: list[str] = []
    facts: dict = {"metadata": str(meta_path)}
    result = {"name": base.name, "accepted": False, "reasons": reasons, "facts": facts}

    if not meta_path.is_file():
        reasons.append(f"no metadata file ({meta_path.name}): the series does not say where it came from")
        return result
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as e:
        reasons.append(f"the metadata file cannot be read ({e})")
        return result
    if not isinstance(meta, dict):
        reasons.append("the metadata file does not hold a record of fields")
        return result

    def absent(field: str) -> bool:
        """No such field, or an empty one. An empty list of partial years is an honest answer."""
        return field not in meta or meta[field] is None or (meta[field] in ("", [], {}) and field != "partial_years")

    missing = [f for f in REQUIRED if absent(f)]
    plain = [f for f in missing if f not in ("database", "coverage", "complete")]  # those three get their own sentence
    if plain:
        reasons.append("the metadata is incomplete: no " + ", ".join(f"`{f}`" for f in plain))

    # Complete
    if "complete" in missing:
        reasons.append("the metadata does not say whether the run was complete")
    elif meta["complete"] is not True:
        why = f' (it stopped: "{meta["stopped"]}")' if meta.get("stopped") else ""
        reasons.append("the series is marked incomplete" + why)
    elif meta.get("stopped"):
        reasons.append(f'the metadata says the run was complete and also that it stopped: "{meta["stopped"]}"')

    # Which database answered
    database = meta["database"].strip() if isinstance(meta.get("database"), str) else ""
    coverage = meta["coverage"].strip() if isinstance(meta.get("coverage"), str) else ""
    facts.update(database=database or None, coverage=coverage or None)
    if not database:
        reasons.append("the series does not name its database")
    if not coverage:
        reasons.append("the series does not say which database answered: it has no Coverage line")
    elif database and not re.search(r"(?<![A-Za-z])" + re.escape(database) + r"\s+answered\s+\(\d+\s+requests?\b", coverage, re.I):
        # the form counts.py writes: "<database> answered (<n> requests …)"; any other sentence is not taken as a yes
        reasons.append(f'the Coverage line does not say that {database} answered: "{coverage}"')

    # The same document types on both sides of the share
    share = meta.get("share") if isinstance(meta.get("share"), dict) else {}
    above, below = types_of(share.get("numerator_types")), types_of(share.get("denominator_types"))
    if "share" not in missing:
        if above is None or below is None:
            reasons.append("the metadata does not say which document types were counted above and below the line")
        elif above != below:
            reasons.append(f"the share counts different document types on its two sides: {named(above)} above the line, {named(below)} below")
    facts.update(types_above=list(above) if above else None, types_below=list(below) if below else None)

    # Date, years and partial years
    fetched = meta.get("fetched") if isinstance(meta.get("fetched"), str) else ""
    years = meta.get("years")
    partial = meta.get("partial_years")
    ok_years = isinstance(years, list) and len(years) == 2 and all(isinstance(y, int) for y in years) and years[0] <= years[1]
    ok_partial = isinstance(partial, list) and all(isinstance(y, int) for y in partial)
    if "fetched" not in missing:
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fetched):
                raise ValueError
            dt.date.fromisoformat(fetched)
        except ValueError:
            reasons.append(f'the date fetched is not a date: "{meta.get("fetched")}"')
            fetched = ""
    if "years" not in missing and not ok_years:
        reasons.append("the years are not a first and a last year")
    if "partial_years" in meta and not ok_partial:
        reasons.append("the partial years are not a list of years")
    if fetched and ok_years and ok_partial:
        unmarked = [y for y in range(years[0], years[1] + 1) if y >= int(fetched[:4]) and y not in partial]
        if unmarked:
            reasons.append(f"{', '.join(map(str, unmarked))} was not over when the series was fetched ({fetched}) and is not marked partial")
    facts.update(fetched=fetched or None, years=years if ok_years else None, partial_years=partial if ok_partial else None)

    # The series and the script
    series = meta.get("series")
    if "series" not in missing and not (isinstance(series, list) and all(isinstance(s, dict) and s.get("id") for s in series)):
        reasons.append("the metadata does not name its series")
    script = meta.get("script")
    if "script" not in missing and not (isinstance(script, dict) and script.get("name") and (script.get("version") or script.get("sha256"))):
        reasons.append("the metadata does not say which script and version made the series")
    facts["script"] = f'{script.get("name")} {script.get("version") or ""}'.strip() if isinstance(script, dict) and script.get("name") else None

    # The numbers against the labels
    if not csv_path.is_file():
        reasons.append(f"the data file {csv_path.name} is not beside the metadata")
    else:
        try:
            header, rows = read_rows(csv_path)
        except (OSError, csv.Error, UnicodeDecodeError) as e:
            reasons.append(f"the data file cannot be read ({e})")
            header, rows = [], []
        kind = "series" if tuple(header) == SERIES_COLUMNS else "taxonomy" if tuple(header) == TAXONOMY_COLUMNS else None
        facts.update(data=str(csv_path), rows=len(rows), kind=kind)
        if not header:
            reasons.append(f"the data file {csv_path.name} is empty")
        elif kind is None:
            reasons.append("the data file does not have the columns counts.py writes: " + ", ".join(header))
        elif not rows:
            reasons.append(f"the data file {csv_path.name} has no rows")
        else:
            reasons.extend(check_rows(rows, kind, meta if ok_partial else {**meta, "partial_years": None}, years if ok_years else None))
            listed = [f for f in meta.get("files") or [] if isinstance(f, str) and f.endswith(".types.csv")] if isinstance(meta.get("files"), list) else []
            if kind == "series" and types_path.is_file() and above and below:
                reasons.extend(check_types(rows, types_path, above, below))
                facts["types_file"] = str(types_path)
            elif kind == "series" and listed:
                reasons.append(f"the metadata lists a types file ({listed[0]}) and it is not beside the data: the counts cannot be checked against the declared types")
            elif kind == "series":
                facts["types_file"] = None  # a series counts.py saved without one (Europe PMC): the labels could not be checked against it

    result["accepted"] = not reasons
    return result


def check_rows(rows: list[dict], kind: str, meta: dict, years) -> list[str]:
    reasons, bad_partial, bad_year, bad_number, twice, bad_share, seen = [], [], [], [], [], [], set()
    partial = meta.get("partial_years")
    key = "series" if kind == "series" else "topic_id"
    pairs = [("count", "base", "share_per_100k")] + ([("count_all_types", "base_all_types", "share_all_types_per_100k")] if kind == "series" else [])
    for r in rows:
        try:
            year = int(r["year"])
            for count, base, share in pairs:
                c, b = int(r[count]), int(r[base])
                if c < 0 or b < 0:
                    raise ValueError
                if b and abs(float(r[share]) - 1e5 * c / b) > 0.001:
                    bad_share.append(f"{r[key]} {year}: `{share}` is {r[share]} and {c} over {b} gives {1e5 * c / b:.4f}")
        except (KeyError, TypeError, ValueError):
            bad_number.append(f"{r.get(key)} {r.get('year')}")
            continue
        if (r[key], year) in seen:
            twice.append(f"{r[key]} {year}")
        seen.add((r[key], year))
        if years and not years[0] <= year <= years[1]:
            bad_year.append(f"{r[key]} {year}")
        if partial is not None and (r.get("partial") == "true") != (year in partial):
            bad_partial.append(f"{r[key]} {year}")
    if bad_number:
        reasons.append("rows without a year, a count or a base that is a whole number: " + some(bad_number))
    if twice:
        reasons.append("more than one row for the same series and year: " + some(twice))
    if bad_share:
        reasons.append("a share that is not its count over its base: " + some(bad_share))
    named_ids = [s.get("id") for s in meta.get("series") or [] if isinstance(s, dict)] if isinstance(meta.get("series"), list) else []
    if kind == "series" and named_ids:
        in_file = {r.get(key) for r in rows}
        if in_file != set(named_ids):
            reasons.append("the series in the data are not the ones the metadata names: " + ", ".join(sorted(map(str, in_file))) + " in the data, "
                           + ", ".join(sorted(map(str, named_ids))) + " in the metadata")
    if bad_year:
        reasons.append("rows outside the years the metadata gives: " + some(bad_year))
    if bad_partial:
        reasons.append("the partial years in the data are not the ones the metadata gives: " + some(bad_partial))
    if isinstance(meta.get("rows"), int) and meta["rows"] != len(rows):
        reasons.append(f"the metadata says {meta['rows']} rows and the data file has {len(rows)}")
    return reasons


def check_types(rows: list[dict], types_path: Path, above: tuple[str, ...], below: tuple[str, ...]) -> list[str]:
    """Recompute each count from the file that holds every document type, with the types the metadata declares."""
    try:
        _, type_rows = read_rows(types_path)
        table: dict[tuple[str, int], dict[str, int]] = {}
        for t in type_rows:
            cell = table.setdefault((t["series"], int(t["year"])), {})
            name = t["type"].strip().lower()
            if name in cell:
                return [f"the types file has two rows for {t['series']} {t['year']} {name}"]
            cell[name] = int(t["count"])
    except (OSError, csv.Error, KeyError, TypeError, ValueError, AttributeError, UnicodeDecodeError) as e:
        return [f"the types file cannot be read ({e})"]

    def total(series: str, year: int, types: tuple[str, ...]) -> int:
        cell = table.get((series, year), {})
        return sum(cell.values()) if types == ALL else sum(cell.get(t, 0) for t in types)

    wrong = []
    for r in rows:
        try:
            year = int(r["year"])
            pairs = (("count", r["series"], above), ("base", "_base", below), ("count_all_types", r["series"], ALL), ("base_all_types", "_base", ALL))
            for column, who, types in pairs:
                if int(r[column]) != total(who, year, types):
                    wrong.append(f"{r['series']} {year}: `{column}` is {r[column]} and the types file gives {total(who, year, types)} for {named(types)}")
        except (KeyError, TypeError, ValueError):
            continue  # a row that is not all whole numbers: check_rows named it
    return ["the counts are not the sum of the declared document types: " + some(wrong)] if wrong else []


def line(result: dict) -> str:
    f = result["facts"]
    if result["accepted"]:
        partial = ", ".join(map(str, f["partial_years"])) or "none"
        return (f"ACCEPTED {result['name']}: {f['database']}, fetched {f['fetched']}, {f['years'][0]}–{f['years'][1]} (partial: {partial}), "
                f"counted above and below the line: {named(tuple(f['types_above']))}; {f['rows']} rows by {f['script']}."
                + ("" if f.get("types_file") or f.get("kind") != "series" else " No types file: the counts were not checked against it."))
    return f"REFUSED  {result['name']}:\n" + "\n".join(f"  - {r}" for r in result["reasons"])


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("series", nargs="+", type=Path, help="NAME.csv or NAME.meta.json, as counts.py saved them")
    p.add_argument("--json", action="store_true", help="print what was found as JSON")
    a = p.parse_args(argv)
    results = [check(path) for path in a.series]
    if a.json:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
        print()
    else:
        print("\n".join(line(r) for r in results))
    return 0 if all(r["accepted"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
