# Changelog

## 0.1.0
The first version. Foresight becomes a plugin of its own; until now it was a playbook inside poiesis-insight.
Nothing was removed from poiesis-insight, and the files both plugins write are the same.

- **Moved from poiesis-insight 1.4.3,** first copied as they were: the foresight playbook, `forecasts.py`, the
  `foresight-analyst` agent, and the forecast and signal templates. The playbook is now six: `scan`,
  `trends`, `horizons`, `layers`, `scenarios` and `forecasts`, each keeping its passage word for word. `forecasts.py` prints what it printed before, with one difference: the
  line under a table's header is skipped when it carries alignment colons (`|:---|`), where it used to be listed
  under "Rows not understood".
- **Thirteen playbooks,** grouped by the three questions of the UK Government Office for Science's Futures
  Toolkit. What is changing: `scan`, `trends`, `base-rates`, `horizons`, `drivers`. What it could mean: `layers`,
  `scenarios`, `wheels`, `forecasts`. What to do: `stress-test`, `signposts`, `review`. And `challenge`. Each
  starts with "Read first": the notes its rules rest on and how much of each source was read.
- **`series_gate.py`:** a yearly series from poiesis-research is read only when its metadata names the database
  and a Coverage line in which it answered, says the run was complete, and declares the same document types above
  and below the line of its share. The counts are then added up again from the types file, and a
  series whose types file is missing is refused.
- **`trends.py`:** growth against a series' own past, with the unfinished year left out; the yearly rate over two
  spans; the rate since the earlier peak. A share with different document types on its two sides is refused,
  and one that counts every record type on both sides is shown and not read. The raw count is printed as a check. `--base-rate` lists how
  earlier jumps in a file's series went on. `--own` reads a table of your own.
- **Forecasts with three probabilities:** the model's independent runs (the `forecaster` agent, one per run), the
  owner's own number, and their mean as the forecast of record. Two columns at the end of the log, `model` and
  `owner`; `forecasts.py --sources` scores each on the rows that have both.
- **Signposts:** `foresight/signposts.md`, with a trigger, the scenarios it tells apart, a prepared response, a
  lead time and a status (`watching`, `reached`, `retired`); `signposts.py` says what is due and what is out of
  order.
- **Ids:** `SC-001` for a scenario, `SP-001` for a signpost, `F-001` for a forecast, from `ids.py`; a **From**
  line on each scenario. Signals keep the ids poiesis-research gave them.
- **A challenge of its own,** with three questions about the future: the base rate, the contrary future, and
  detail that adds no probability. When poiesis-insight is installed its general challenge runs as well.
- **Agents:** `foresight-analyst` reads this plugin's playbooks, returns fixed sections, no longer searches the
  web and no longer gives probabilities: it proposes the questions, and `forecaster`, which is new, and the owner
  give the numbers.
- **Twenty-eight notes** in `research/notes`, each with a **Read** line. Thirteen sources were read in part,
  eleven as an abstract only, three by title only, and one is an observation.
- **Waiting:** thresholds for emergence, expected from Carley et al. 2018, which could be read as an abstract
  only. **Kept from poiesis-insight and marked unverified:** the control-chart rules (Benneyan et al. 2003,
  abstract only), what makes a signal weak (Hiltunen 2008, title only) and the four layers (Inayatullah 1998,
  title only).
- **Not checked in this version:** the playbooks and the two agents in a real session; the eval cases, which were
  written and not run; a taxonomy scan as a reference class, which needs an OpenAlex key.
- Tests in `tests/`, run with `python3 -I -m unittest discover -s tests`; eval cases in the plugin's `evals/`.
