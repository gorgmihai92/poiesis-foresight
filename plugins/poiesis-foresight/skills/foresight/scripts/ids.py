#!/usr/bin/env python3
"""The next free id for a scenario, a signpost or a forecast, and the ids a project already uses. Run with
`python3 -I`.

  ids.py SC foresight                 the next scenario id: SC-001, SC-002, …
  ids.py SP foresight                 the next signpost id
  ids.py F foresight                  the next forecast id
  ids.py --list foresight research    every id given to something, and any id given twice

An id is two letters or one, a dash and at least three digits. A number is never used twice, so the next id is
one more than the highest number found anywhere in the folders' Markdown files, mentions included. An id is
"given" where a line reads `- **Id:** SC-001` or where it opens a table row, as in a log. Signals keep the ids
poiesis-research gave them (SG-001): this script lists them and never makes one.

Exit code 0, or 1 when --list finds an id given to two things.
"""
import argparse
import re
import sys
from pathlib import Path

PREFIXES = {"SC": "scenario", "SP": "signpost", "F": "forecast"}
READ_ONLY = {"SG": "signal (poiesis-research)"}
ANY = re.compile(r"(?<![A-Za-z0-9])(SC|SP|SG|F)-(\d{3,})(?![0-9])")
GIVEN = re.compile(r"^\s*(?:[-*]\s+\*\*Id:\*\*\s*|\|\s*)(SC|SP|SG|F)-(\d{3,})\b")


def files(places: list[Path]) -> list[Path]:
    out: list[Path] = []
    for place in places:
        out += sorted(place.rglob("*.md")) if place.is_dir() else [place] if place.is_file() else []
    return out


def scan(places: list[Path]) -> tuple[dict[str, int], dict[str, list[str]]]:
    """(the highest number seen per prefix, where each id is given)."""
    highest: dict[str, int] = {}
    given: dict[str, list[str]] = {}
    for path in files(places):
        for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            for prefix, digits in ANY.findall(line):
                highest[prefix] = max(highest.get(prefix, 0), int(digits))
            m = GIVEN.match(line)
            if m:
                given.setdefault(f"{m.group(1)}-{m.group(2)}", []).append(f"{path}:{n}")
    return highest, given


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("prefix", nargs="?", help="SC, SP or F")
    p.add_argument("places", nargs="*", type=Path, help="folders or Markdown files to read")
    p.add_argument("--list", action="store_true", help="every id given to something, and any id given twice")
    a = p.parse_args(argv)
    if a.list:
        places = ([Path(a.prefix)] if a.prefix else []) + a.places
        if not places:
            p.error("--list needs the folders or files to read")
        _, given = scan(places)
        twice = {i: where for i, where in given.items() if len(where) > 1}
        for i in sorted(given, key=lambda x: (x.split("-")[0], int(x.split("-")[1]))):
            print(f"{i}  {given[i][0]}")
        if not given:
            print("No id is given to anything in " + ", ".join(map(str, places)) + ".")
        for i, where in sorted(twice.items()):
            print(f"GIVEN TWICE {i}: " + ", ".join(where))
        return 1 if twice else 0
    if not a.prefix or a.prefix.upper() in READ_ONLY:
        p.error("say which id: SC (scenario), SP (signpost) or F (forecast). Signal ids come from poiesis-research.")
    prefix = a.prefix.upper()
    if prefix not in PREFIXES:
        p.error(f"{a.prefix} is not an id this plugin gives: SC (scenario), SP (signpost) or F (forecast)")
    if not a.places:
        p.error("say where to look, for example: ids.py SC foresight")
    highest, _ = scan(a.places)
    print(f"{prefix}-{highest.get(prefix, 0) + 1:03d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
