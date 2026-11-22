# Tests

Tests for the scripts in `plugins/poiesis-foresight/skills/foresight/scripts` and for the plugin's own files. They
need Python 3 only and never use the network.

```
python3 -I -m unittest discover -s tests
```

This folder is not part of the plugin, so it is not installed with it.

| File | What it checks |
|---|---|
| `test_series_gate.py` | a series replayed from poiesis-research's recording is accepted; copies with one side's types changed, marked incomplete, or with no database named are refused |
| `test_trends.py` | the numbers of the lab's recorded run are reproduced for every area; a share with different document types on its two sides is refused; solid-state batteries do not come out as falling; own tables; base rates |
| `test_logs.py` | `forecasts.py` with and without the new columns, `signposts.py`, `ids.py` |
| `test_plugin_files.py` | every playbook starts with "Read first" and names notes that exist; every note has a Read line; the version is the same in three places; the eval cases have the files a case needs |

## Fixtures

- `fixtures/research-series/` is a series made by poiesis-research 2.4.0's `counts.py --replay` from that
  repository's own recording (`tests/recordings/counts-series`), at commit `d767017` on its `main`. The counts are OpenAlex's, fetched on
  2026-11-21 with no key. Set `POIESIS_RESEARCH` to a checkout of
  poiesis-research and one test makes the series again and compares it byte for byte; without it that test is
  skipped and says so.
- `fixtures/logs/` holds a forecast log and a signpost log written for the tests. They are not real forecasts.

Two tests read the recorded run kept in the Poiesis Lab notebook (`fixtures/trend-scan/`, `fixtures/logs/`), which
is a private folder outside this repository. Set `POIESIS_LAB` to the notebook's folder, or keep it at
`~/Poiesis Lab`. Without it those tests are skipped and say so: the other tests do not need it. A run that prints "skipped" has
not compared the recorded run, so on a machine without the notebook the suite passing does not show that.
