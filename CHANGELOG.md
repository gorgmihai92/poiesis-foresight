# Changelog

## 0.2.1
Two fixes. No path, field or column was renamed or removed; one column is added at the end of the forecast log.
- **One verdict, and it reaches the other plugins.** `playbooks/challenge.md` now holds the one rule for who gives
  the verdict, and `rules.md` points to it: at quick and standard depth, foresight's own inline challenge; at
  thorough, when poiesis-insight is installed, its `challenger` agent's verdict, which replaces the inline one.
  poiesis-insight's `playbooks/challenge.md` is no longer run "as well", so two challenges no longer compete for
  one conclusion. When poiesis-insight is installed, each scenario's verdict is stamped with its own
  `challenge_stamp.py`, on the scenario's heading, so frontier's gate and
  studio's report read it like any stamp. At thorough depth each scenario goes to the `challenger` in a call of its
  own, the answer is saved in `foresight/challenges/`, and a kept or dropped verdict is stamped from it with
  `--verdicts`, so it is not retyped and poiesis-insight 2.1.1 checks the answer's Claim against the scenario's
  name. A weakened scenario keeps its name, takes the narrower claim into **Holds only if**, and is stamped with
  `--id --verdict weakened`; an inline verdict is stamped with `--id --verdict`. The stamp binds the name, not the
  body: after an edit of substance the scenario is challenged again (`--again`). Insight's scripts are taken from
  the version `claude plugin list` shows enabled. Without poiesis-insight the scenario keeps its Challenge line
  only, and the report says the verdict is not stamped. The scenario template did not change: its heading with the Id line
  under it is what the stamp format reads (checked offline on 2026-11-23 with poiesis-insight 2.1.0's script and
  poiesis-frontier's gate). Rows of a note's challenge table are not stamped.
- **The other way round, in separate runs.** The `forecaster` agent no longer gives the probability that the event
  does not happen: inside one run that is only 1 − p and cannot show a lean toward "yes". Of the model's runs, about
  half get the question as written and the rest its negation; a negated answer p' is logged as 1 − p'. A new last
  column of the forecast log, `wording`, says which wording each run got, and `forecasts.py --sources` prints the
  gap between the two halves. A log without the column prints what it printed before.
- **Tests.** `test_logs.py`: the gap, a row in one wording only, cells that cannot be read, scores unchanged by the
  new column, and the template read with it.
- **Not checked in this version:** any run on a topic, the evals (not run: no model calls), and whether the
  `challenger` agent answers the foresight questions it is handed.

## 0.2.0
Everything is added: no path, field or column of 0.1.0 was renamed or removed, and the scripts read every file as
before.
- **Properties.** The templates of the report, the forecast log, the signpost log and a review start with a block of
  Obsidian properties (YAML between two `---` lines): `type`, `plugin`, `date` and `topic`; a review, which is one
  object, adds `id` and `from` (the two logs it reads). A report holds several scenarios and a log several rows, so
  their properties carry no id or verdict: those stay on the Id and Challenge lines and in the rows, which remain
  the record. The scenario and signal templates go inside a report and get no block.
- **Docs.** The README says Insight 2.0.0 has left foresight to this plugin. `SKILL.md` asks for the block to change
  in the same edit as what it copies.
- **Tests.** `test_templates.py`: the block in each template and its rules, and `forecasts.py`, `signposts.py` and
  `ids.py` giving the same results on logs with the block and without it.
- **Not checked in this version:** how Obsidian shows the properties (no vault was opened), and any run on a topic.

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
