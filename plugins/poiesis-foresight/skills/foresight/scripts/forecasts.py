#!/usr/bin/env python3
"""Score a forecast log (Markdown table) with the Brier score. Run with `python3 -I`.

  forecasts.py foresight/forecasts.md
  forecasts.py foresight/forecasts.md --sources     also score the model's and the owner's probabilities apart

Columns: id | question | probability | made | resolve by | outcome | reasoning. Outcome is 1, 0 or empty.
Brier score = mean of (probability - outcome)^2 over resolved forecasts: 0 is perfect, 0.25 is what always
saying 50% earns, lower is better. Also lists forecasts past their date with no outcome yet.

The first six columns are read by position, so columns added to a log go after `reasoning`. Two are understood
with --sources, by the name in the header row: `model` (the probabilities of the model's independent runs,
separated by spaces) and `owner` (the owner's own probability). `probability` stays the forecast of record.
Without --sources the output is what it was before those columns existed.

A third column, `wording`, says for each model run, in the order of `model`, whether it was given the question as
`written` or its negation (`negated`); a negated run's answer p' is logged in `model` as 1 - p'. With --sources,
when the log has that column, the script prints for each forecast with runs in both wordings the gap: the mean of
the written runs minus the mean of the negated ones, both as the probability of yes. A log without the column
prints what it printed before.

A row is "not understood", and left out of the score, when its probability is not a number from 0 to 1, its
outcome is anything but 1, 0 or empty, or it has no outcome and its resolve date is not written YYYY-MM-DD. A
table whose header does not start with `id` is another table and is passed over.
"""
import argparse
import datetime as dt
import math
import re
import statistics
import sys
from pathlib import Path


def cells_of(line: str) -> list[str]:
    return [c.strip() for c in line.strip("|").split("|")]


def tables(path: Path) -> list[tuple[list[str], list[list[str]]]]:
    """The forecast tables of a file, each as (header cells in lower case, rows). A table is a run of lines that
    start with `|`, indented or not. Its header is the line above the line of dashes. A table whose header does not
    start with `id` is not a forecast table."""
    found, block = [], []
    for line in [*path.read_text(encoding="utf-8-sig").splitlines(), ""]:
        line = line.strip()
        if line.startswith("|"):
            block.append(line)
            continue
        if block:
            dashes = [i for i, l in enumerate(block) if set(l) <= {"|", "-", ":", " "}]  # the line under the header, aligned or not
            head = [c.lower() for c in cells_of(block[dashes[0] - 1])] if dashes and dashes[0] > 0 else []
            if not head or head[0] == "id":
                body = [cells_of(l) for i, l in enumerate(block) if i not in dashes and not (dashes and i == dashes[0] - 1)]
                found.append((head, [c for c in body if c and c[0].lower() != "id" and not c[0].startswith("<")]))
            block = []
    return found


def rows(path: Path) -> list[list[str]]:
    return [r for _, body in tables(path) for r in body]


def probability(text: str) -> float | None:
    """A probability from 0 to 1, or None."""
    try:
        x = float(text)
    except ValueError:
        return None
    return x if math.isfinite(x) and 0 <= x <= 1 else None


def understood(r: list[str]) -> bool:
    """Whether a row can be scored or waited for: see the note at the top of this file."""
    if len(r) < 6 or probability(r[2]) is None or r[5] not in ("", "0", "1"):
        return False
    return bool(r[5]) or not r[4] or bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", r[4]))


def probabilities(cell: str) -> list[float] | None:
    """The probabilities written in one cell; None when a piece is not a number between 0 and 1."""
    try:
        found = [float(piece) for piece in re.split(r"[\s,;]+", cell.strip()) if piece]
    except ValueError:
        return None
    return found if found and all(0 <= x <= 1 for x in found) else None


def brier(pairs: list[tuple[float, int]]) -> float:
    return sum((p - o) ** 2 for p, o in pairs) / len(pairs)


def by_source(path: Path) -> None:
    """Score the forecast of record, the model's runs and the owner's probability on the same resolved rows."""
    print("\nBy source:")
    with_columns, named = [], False
    for head, body in tables(path):
        where = {name: next((i for i, cell in enumerate(head) if i >= 7 and cell.startswith(name)), None) for name in ("model", "owner")}
        if where["model"] is not None and where["owner"] is not None:
            named = True
            with_columns += [(where, r) for r in body]
    if not named:
        print("  The log has no `model` and `owner` columns after `reasoning`: nothing to compare.")
        return
    kept, left, bad, off = [], [], [], []
    for where, r in with_columns:
        if not understood(r) or r[5] not in ("0", "1"):
            continue
        record = float(r[2])
        cell = {name: r[i] if i < len(r) else "" for name, i in where.items()}
        if not cell["model"] or not cell["owner"]:
            left.append(r[0])
            continue
        runs, own = probabilities(cell["model"]), probabilities(cell["owner"])
        if runs is None or own is None or len(own) != 1:
            bad.append(r[0])
            continue
        both = (statistics.mean(runs) + own[0]) / 2
        kept.append((r[0], int(r[5]), record, statistics.mean(runs), statistics.median(runs), own[0], both, len(runs)))
        if abs(record - both) > 0.0051:  # a mean such as 0.345 logged as 0.35 or 0.34 is the mean
            off.append(f"{r[0]} ({record:.2f} logged, {both:.2f} is the mean)")
    if kept:
        print(f"  Over the {len(kept)} resolved forecasts that have a model and an owner probability (0 = perfect, 0.25 = always 50%):")
        names = ("of record", "model, mean of its runs", "model, median of its runs", "owner", "mean of owner and model")
        for n, name in enumerate(names, start=2):
            print(f"    {name}: {brier([(k[n], k[1]) for k in kept]):.3f}")
        few = [k[0] for k in kept if k[7] < 3]
        if few:
            print("  Fewer than 3 model runs: " + ", ".join(few))
    else:
        print("  No resolved forecast has both a model and an owner probability yet.")
    if left:
        print("  Not in this comparison (no model or no owner probability): " + ", ".join(left))
    if bad:
        print("  Model or owner cell not understood: " + ", ".join(bad))
    if off:
        print("  The forecast of record is not the mean of the owner's and the model's: " + ", ".join(off))


def other_way_round(path: Path) -> None:
    """The gap between the model's runs on the question as written and on its negation, per forecast."""
    with_column, named = [], False
    for head, body in tables(path):
        where = {name: next((i for i, cell in enumerate(head) if i >= 7 and cell.startswith(name)), None) for name in ("model", "wording")}
        if where["model"] is not None and where["wording"] is not None:
            named = True
            with_column += [(where, r) for r in body]
    if not named:
        return
    print("\nThe other way round (the mean of the runs given the question as written, minus the mean of those given its negation, both as the probability of yes):")
    gaps, one, bad = [], [], []
    for where, r in with_column:
        cell = {name: r[i] if i < len(r) else "" for name, i in where.items()}
        if not cell["wording"].strip():
            continue
        runs, words = probabilities(cell["model"]), cell["wording"].split()
        if runs is None or len(words) != len(runs) or any(w not in ("written", "negated") for w in words):
            bad.append(r[0])
            continue
        written = [x for x, w in zip(runs, words) if w == "written"]
        negated = [x for x, w in zip(runs, words) if w == "negated"]
        if not written or not negated:
            one.append(r[0])
            continue
        gap = statistics.mean(written) - statistics.mean(negated)
        gaps.append(gap)
        print(f"  {r[0]}: {round(gap, 2) or 0.0:+.2f} ({len(written)} written, mean {statistics.mean(written):.2f}; {len(negated)} negated, mean {statistics.mean(negated):.2f})")
    if len(gaps) > 1:
        print(f"  Mean gap over {len(gaps)} forecasts: {round(statistics.mean(gaps), 2) or 0.0:+.2f}")
    if not gaps:
        print("  No forecast has runs in both wordings yet.")
    if one:
        print("  One wording only: " + ", ".join(one))
    if bad:
        print("  Model or wording cell not understood (one word per run, written or negated): " + ", ".join(bad))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("log", type=Path)
    p.add_argument("--sources", action="store_true", help="also score the `model` and `owner` columns, on the rows that have both, and print the gap between the two wordings")
    a = p.parse_args()
    today = dt.date.today().isoformat()
    scored, due, bad = [], [], []
    try:
        found = rows(a.log)
    except (OSError, UnicodeDecodeError) as e:
        print(f"The log cannot be read: {e}")
        return 2
    for r in found:
        if not understood(r):
            bad.append(r[0])
            continue
        fid, question, prob, _made, resolve, outcome = r[:6]
        pr = float(prob)
        if outcome in ("0", "1"):
            scored.append((fid, pr, int(outcome)))
        elif resolve and resolve <= today:
            due.append(f"{fid} ({resolve}): {question}")
    if scored:
        brier_score = sum((pr - o) ** 2 for _, pr, o in scored) / len(scored)
        print(f"Brier score: {brier_score:.3f} over {len(scored)} resolved forecasts (0 = perfect, 0.25 = always 50%)")
        for fid, pr, o in scored:
            print(f"  {fid}: said {pr:.0%}, outcome {o} → {(pr - o) ** 2:.3f}")
    else:
        print("No resolved forecasts yet.")
    if due:
        print("\nPast their date, outcome missing:")
        for d in due:
            print("  " + d)
    if bad:
        print("\nRows not understood: " + ", ".join(bad))
    if a.sources:
        by_source(a.log)
        other_way_round(a.log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
