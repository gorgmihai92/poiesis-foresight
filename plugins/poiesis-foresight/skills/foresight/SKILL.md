---
name: foresight
description: Foresight for a project, from signals, yearly counts and research it already has. What is changing (which signals to keep, whether a series moved against its own past, how often such moves go on, the forces behind them), what it could mean (contrasting scenarios, consequences of one change, forecasts with a date that are scored later) and what to do (a concept or decision tested against each scenario, signposts to watch, a dated review). Use when the user asks for foresight, trends, emerging topics, weak signals, drivers, scenarios, futures, forecasts, base rates, signposts or a review of earlier forecasts.
---

# Foresight

Research records what was observed and counted. This skill reads it forward: what is changing, what it could
mean, and what to watch. It opens possibilities and makes them testable; it does not predict one future.

The playbooks follow the three questions of the UK Government Office for Science's Futures Toolkit.

| The user wants… | Playbook | Script | Saved in |
|---|---|---|---|
| **What is changing** | | | |
| which signals to keep, and what each might mean | `playbooks/scan.md` | | the foresight note |
| whether a yearly series moved, against its own past | `playbooks/trends.md` | `series_gate.py`, `trends.py` | the foresight note |
| how often a move like this went on | `playbooks/base-rates.md` | `trends.py --base-rate` | the foresight note |
| where each pattern sits: current, transitional, emerging | `playbooks/horizons.md` | | the foresight note |
| the forces that matter, and which are uncertain | `playbooks/drivers.md` | | the foresight note |
| **What it could mean** | | | |
| the same issue read at four depths | `playbooks/layers.md` | | the foresight note |
| two to four contrasting futures | `playbooks/scenarios.md` | `ids.py SC` | the foresight note |
| what follows from one change, and from that | `playbooks/wheels.md` | | the foresight note |
| claims that can be checked later | `playbooks/forecasts.md` | `ids.py F`, `forecasts.py` | `foresight/forecasts.md` |
| **What to do** | | | |
| a concept or a decision tested against each scenario | `playbooks/stress-test.md` | | the foresight note |
| what to watch, and the response prepared for it | `playbooks/signposts.md` | `ids.py SP`, `signposts.py` | `foresight/signposts.md` |
| what happened to earlier forecasts and signposts | `playbooks/review.md` | `forecasts.py --sources`, `signposts.py` | `foresight/reviews/` |
| **Before anything is reported** | `playbooks/challenge.md` | | marks each conclusion kept, weakened or dropped |

The foresight note is `foresight/<YYYY-MM-DD>-<topic>.md`, from `templates/foresight.md`.

## Every request

1. **The scoping question:** what is asked, how far ahead, and which decision it informs. Say it in one line and
   start; ask only if it cannot be inferred.
2. **Input:** what the project holds (see "From poiesis-research" and "Your own data"). Say what was found and
   what is missing before reading anything into it. Thin input is said to be thin.
3. **Pick the playbooks** from the table. A full pass runs down it: scan, trends, base rates, drivers, scenarios,
   forecasts, stress test, signposts. Most requests need two or three.
4. **Scripts for numbers.** A series goes through `series_gate.py`, then `trends.py`. Paste what they print.
5. **Challenge** every conclusion with `playbooks/challenge.md` before reporting it, at the depth chosen
   (`rules.md`, "Depth"). Report what was kept, weakened and dropped, and why.
6. **Follow `rules.md`**, the same for every playbook.
7. **No step without a playbook or a script.** When the request needs one that none covers, stop and say what is
   missing. Offer the choices: an existing method used more narrowly, building the tool first, or skipping the
   step and recording it under "Not checked".

Scripts are in `${CLAUDE_SKILL_DIR}/scripts` (called `$S`; if that path does not exist, Glob for
`**/foresight/scripts/trends.py` under `~/.claude`). They need only Python 3; run them with `python3 -I`. None of
them asks a database or changes a file.

## From poiesis-research


What foresight reads from the research plugin, when the project has it. It works without it too.
- `research/README.md`: the index; start here.
- `research/signals/<date>-<name>.md`: one signal each, with **Id** (SG-001), **What**, **Where**, **When**,
  **How visible**, **How widespread**, **Kind of source**, **Read**. An observation with no reading: the reading
  is made here.
- `research/data/<name>.csv` with `<name>.meta.json` and `<name>.types.csv`: a yearly series. `series_gate.py`
  decides whether it may be read.
- `research/notes/<section>/<slug>.md`: what a source says, with pages. Cite the note and the page.
- `insights/<date>-<topic>.md` (poiesis-insight): conclusions with their **Challenge** verdict. Start only from
  the kept and the weakened ones.

Foresight never edits these files. When they are missing it says so once and goes on with what the user gives.
It does not scan, search or count: that is poiesis-research's work, with its record of which databases answered.

## Your own data

- **Signals:** a link, a note or a list. Each needs what, where and when.
- **A table of yearly figures:** columns `series,year,count`, with `base` for a share and `partial` (true or false) for unfinished years. The `year` column may hold any
  whole-number period in a row (a wave, a week), though the script's words say "year". `python3 -I $S/trends.py --own table.csv --last-full-year <year>`; for a share add what is counted above
  and below the line (`--above`, `--below`), which must be the same.
- **A forecast log from poiesis-insight:** it is the same file. Its seven columns are read as before; the two
  new ones go at the end.

## Saving
Save the work when any of these holds: the depth is standard or thorough; the user asks; the project already has
a `foresight/` folder; or something has a date to come back to. A forecast, a signpost and a review are always saved; if the user wants no file, give
the forecast in the chat and say it will not be scored. Otherwise (quick depth, a one-off question) answer in the chat only, and end with one line offering to
save it. Never create a folder the user did not want.

## Answers
Short and direct: the answer first, then what it rests on, in bullets or a table; no preamble, no recap. When the
work is saved, the chat gets the summary, the "Not checked" line and the file's path.

- **Copy, do not retype.** What a script printed, a row an agent returned and a verdict are put in the answer and
  in saved files as they came.
- **An agent is a model call.** Use one only for independent parts that can run in parallel, for the independent
  runs of a forecast, or for the independent check at thorough depth. Say how many will run before starting them.
  `foresight-analyst` takes one issue; `forecaster` gives one probability for one question.

## Other Poiesis plugins
This plugin works alone. Suggest another one only when it would change the result: once, in one line, and go on
without it if the user says no (say what was left out). Check with `claude plugin list`; install only after the
user agrees, with `claude plugin marketplace add gorgmihai92/<repo>` and then
`claude plugin install <plugin>@<repo>` (it works after Claude Code restarts).
Every suggestion, from the skill or an agent, gives the plugin's link (below) and names the skill or agent to
use, e.g. "[poiesis-research](https://github.com/gorgmihai92/poiesis-research), `signal-scout`".
- **[poiesis-research](https://github.com/gorgmihai92/poiesis-research)**: when there are no signals or no
  series, or a series was refused by the gate and has to be counted again.
- **[poiesis-insight](https://github.com/gorgmihai92/poiesis-insight)**: for what the evidence means today, and
  for the general challenge of a conclusion (`challenger`), which runs beside this plugin's own.
- **[poiesis-frontier](https://github.com/gorgmihai92/poiesis-frontier)**: when the user wants concepts to build
  from a scenario, or an experiment that could prove one wrong.

## Files shared with other Poiesis plugins
These paths and fields are a contract between the Poiesis plugins: rename or remove one only in a major version,
and say so in the changelog; adding fields is free. Read other plugins' files tolerantly: a missing file or field
means "unknown", said in the report, never an error.
- Writes `foresight/<date>-<topic>.md`: scenarios with what holds in all of them and what depends on one; signals
  with **Horizon**. These are the path and fields poiesis-insight 1.4 wrote, unchanged.
- Writes `foresight/forecasts.md`: columns `id | question | probability | made | resolve by | outcome |
  reasoning`, in that order, then `model | owner`. A new column goes at the end.
- Writes `foresight/signposts.md`: columns `id | watch | trigger | points to | response | lead time | status |
  next check | last value | last checked`. Status is `watching`, `reached` or `retired`.
- Writes `foresight/reviews/<date>.md`.
- In a note, a scenario has **Id** (SC-001), **From**, **Answers**, **Year**, **Built on**, **Holds only if**,
  **Would be wrong if**, **Signposts** and **Challenge** (the line starts with `kept`, `weakened` or `dropped`).
  A signpost's id is SP-001; a forecast's is F-001.
- Reads `research/signals/`, `research/data/`, `research/notes/` and `research/README.md` (poiesis-research) and
  `insights/` (poiesis-insight).
