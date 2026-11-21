#!/usr/bin/env python3
"""Read a signpost log (Markdown table): which signposts are due for a look, which have reached their trigger,
and which rows are not in order. Run with `python3 -I`.

  signposts.py foresight/signposts.md

Columns, read by position: id | watch | trigger | points to | response | lead time | status | next check |
last value | last checked. A column added later goes after these ten.
  - status is watching, reached or retired;
  - next check and last checked are dates as YYYY-MM-DD;
  - a trigger written as a comparison with a number, such as `>= 25` or `< 0.5`, is compared with the last value
    by this script. Any other trigger is a sentence for a person to judge, and the script says so.

It prints what is due (status watching, next check today or earlier), what has reached its trigger, and every
row whose status and numbers disagree. It changes nothing: a status is changed by hand, in a review.
Exit code 0, or 1 when a row is not understood or its status disagrees with its numbers.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

STATUSES = ("watching", "reached", "retired")
TRIGGER = re.compile(r"^(>=|<=|>|<|=)\s*(-?\d+(?:\.\d+)?)\s*(%?)$")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
COMPARE = {">=": lambda v, t: v >= t, "<=": lambda v, t: v <= t, ">": lambda v, t: v > t, "<": lambda v, t: v < t, "=": lambda v, t: v == t}


def rows(path: Path) -> list[list[str]]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or set(line) <= {"|", "-", ":", " "}:  # the line under the header, aligned or not
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0].lower() != "id" and not cells[0].startswith("<"):
            out.append(cells)
    return out


def number(text: str) -> float | None:
    try:
        return float(text.strip().rstrip("%").replace(",", ""))
    except ValueError:
        return None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("log", type=Path)
    p.add_argument("--today", help="read the log as on this date (YYYY-MM-DD) instead of today")
    a = p.parse_args(argv)
    today = a.today or dt.date.today().isoformat()
    due, reached, wrong, judged, watching = [], [], [], [], 0
    for r in rows(a.log):
        if len(r) < 8:
            wrong.append(f"{r[0]}: fewer than the eight cells a signpost needs")
            continue
        sid, watch, trigger, _points, response, _lead, status, check = r[:8]
        value, checked = (r[8] if len(r) > 8 else ""), (r[9] if len(r) > 9 else "")
        status = status.lower()
        if status not in STATUSES:
            wrong.append(f"{sid}: status \"{r[6]}\" is not one of {', '.join(STATUSES)}")
            continue
        if any(d and not DATE.fullmatch(d) for d in (check, checked)):
            wrong.append(f"{sid}: a date is not written as YYYY-MM-DD")
            continue
        if status == "retired":
            continue
        rule = TRIGGER.match(trigger)
        met = None
        if rule and value:
            v = number(value)
            if v is None:
                wrong.append(f"{sid}: the last value \"{value}\" is not a number, and the trigger compares with one")
                continue
            met = COMPARE[rule.group(1)](v, float(rule.group(2)))
        elif not rule:
            judged.append(sid)
        if status == "reached":
            reached.append(f"{sid}: {watch} · trigger {trigger}" + (f" · last value {value}" if value else "") + f" · response: {response}")
            if met is False:
                wrong.append(f"{sid}: status says reached, and the last value {value} does not meet the trigger {trigger}")
            continue
        watching += 1
        if met:
            wrong.append(f"{sid}: the last value {value} meets the trigger {trigger}, and the status still says watching")
        if not check:
            wrong.append(f"{sid}: no date for the next check")
        elif check <= today:
            due.append(f"{sid} (due {check}): {watch} · trigger {trigger}" + (f" · last value {value}, read {checked}" if value and checked else ""))
    print(f"Signposts watched: {watching}. Reached: {len(reached)}.")
    if due:
        print("\nDue for a look:")
        print("\n".join("  " + d for d in due))
    if reached:
        print("\nReached their trigger:")
        print("\n".join("  " + d for d in reached))
    if judged:
        print("\nTrigger is a sentence, for a person to judge: " + ", ".join(judged))
    if wrong:
        print("\nRows not in order:")
        print("\n".join("  " + w for w in wrong))
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
