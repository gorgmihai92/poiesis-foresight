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
"""
import argparse
import datetime as dt
import re
import statistics
import sys
from pathlib import Path


def cells_of(line: str) -> list[str]:
    return [c.strip() for c in line.strip("|").split("|")]


def rows(path: Path) -> list[list[str]]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or set(line) <= {"|", "-", ":", " "}:  # the line under the header, aligned or not
            continue
        cells = cells_of(line)
        if cells and cells[0].lower() != "id" and not cells[0].startswith("<"):
            out.append(cells)
    return out


def header(path: Path) -> list[str]:
    """The cells of the header row, lower-case; empty when the log has none."""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("|") and cells_of(line)[0].lower() == "id":
            return [c.lower() for c in cells_of(line)]
    return []


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
    head = header(path)
    where = {name: next((i for i, cell in enumerate(head) if i >= 7 and cell.startswith(name)), None) for name in ("model", "owner")}
    print("\nBy source:")
    if where["model"] is None or where["owner"] is None:
        print("  The log has no `model` and `owner` columns after `reasoning`: nothing to compare.")
        return
    kept, left, bad, off = [], [], [], []
    for r in rows(path):
        if len(r) < 6 or r[5] not in ("0", "1"):
            continue
        try:
            record = float(r[2])
        except ValueError:
            continue
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
        if abs(record - both) > 0.005:
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


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("log", type=Path)
    p.add_argument("--sources", action="store_true", help="also score the `model` and `owner` columns, on the rows that have both")
    a = p.parse_args()
    today = dt.date.today().isoformat()
    scored, due, bad = [], [], []
    for r in rows(a.log):
        if len(r) < 6:
            bad.append(r[0])
            continue
        fid, question, prob, _made, resolve, outcome = r[:6]
        try:
            pr = float(prob)
        except ValueError:
            bad.append(fid)
            continue
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
