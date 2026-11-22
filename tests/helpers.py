"""Shared by the tests: the plugin's scripts on the import path, where the fixtures are, and a way to run a
script's main() and keep what it printed. Nothing here uses the network."""
import contextlib
import io
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "poiesis-foresight"
SKILL = PLUGIN / "skills" / "foresight"
SCRIPTS = SKILL / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
SERIES = FIXTURES / "research-series" / "solid-state-batteries-2026-11-21"
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True


def lab() -> Path | None:
    """The Poiesis Lab notebook, which holds the recorded runs. It is a private folder outside this repository:
    POIESIS_LAB names it, and ~/Poiesis Lab is tried next. None when it is not on this machine."""
    for place in (os.environ.get("POIESIS_LAB"), Path.home() / "Poiesis Lab"):
        if place and (Path(place) / "fixtures" / "trend-scan" / "openalex.json").is_file():
            return Path(place)
    return None


def research() -> Path | None:
    """A checkout of poiesis-research that has counts.py and its recording (2.4.0 or later). POIESIS_RESEARCH
    names it; None when it is not given or not there."""
    place = os.environ.get("POIESIS_RESEARCH")
    if place and (Path(place) / "plugins" / "poiesis-research" / "skills" / "research" / "scripts" / "counts.py").is_file():
        return Path(place)
    return None


def run(module, argv: list[str]) -> tuple[int, str, str]:
    """Run a script's main(argv) and return (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = module.main(argv)
        except SystemExit as e:  # argparse errors
            code = e.code
    return code, out.getvalue(), err.getvalue()
