# Poiesis Foresight

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24501566.svg)](https://doi.org/10.5281/zenodo.24501566) [![Cognitive Centered Design Oath: signed](https://raw.githubusercontent.com/gorgmihai92/ccd-oath/main/badges/ccd-oath-signed.svg)](https://github.com/gorgmihai92/ccd-oath/blob/main/SIGNATORIES.md)

Foresight you can check, in Claude Code. Poiesis Foresight reads the signals, yearly counts and research a project
already holds and looks forward from them: what is changing, what it could mean, and what to watch. The numbers
come from scripts, the futures come in contrasting versions, and every forecast is written down with a date and
scored when the date passes.

For anyone who has to decide something that depends on the next few years: a research direction, a product bet, a
thesis topic, a grant. Poiesis Foresight is one of the five products in the
[Poiesis Toolkit](#part-of-the-poiesis-toolkit) and works on its own, as one plugin. Install it below and ask in
plain language.

It opens possibilities and makes them testable. It does not predict one future, and it says so wherever a reader
could take it that way.

## Part of the Poiesis Toolkit

The Poiesis Toolkit is five products for Claude Code, one for each step from a question to a finished product:
**Research** collects, **Insight** connects, **Foresight** anticipates, **Frontier** explores, **Design** creates.
Each installs and works on its own, and reads what the other steps left in your project, as plain files.

| Product | What it does | Agents | Reads | Leaves in your project |
|---|---|---|---|---|
| [Poiesis Research](https://github.com/gorgmihai92/poiesis-research) | **collect:** literature, evidence, grants, yearly counts, signals, prior art | `paper-scout`, `evidence-scout`, `funding-scout`, `signal-scout` | scholarly databases, official pages | `research/` |
| [Poiesis Insight](https://github.com/gorgmihai92/poiesis-insight) | **connect:** what the evidence or your data mean; every conclusion challenged | `insight-analyst`, `challenger` | `research/`, your own data | `insights/` |
| [Poiesis Foresight](https://github.com/gorgmihai92/poiesis-foresight) | **anticipate:** signals, trends, scenarios, forecasts, signposts | `foresight-analyst`, `forecaster` | `research/`, `insights/`, your own data | `foresight/` |
| [Poiesis Frontier](https://github.com/gorgmihai92/poiesis-frontier) | **explore:** new concepts, each with the smallest experiment that could kill it | `experimentalist` | `insights/`, `foresight/`, `research/` | `frontier/` |
| [Poiesis Design](https://github.com/gorgmihai92/poiesis-design) | **create:** how the interface looks, behaves and what it says | `ui-auditor`, `ux-tester`, `copy-reviewer` | your code, `.poiesis-design/` | design tokens, components |

```
Research ──► Insight ──► Foresight ──► Frontier ──► Design
collects     connects    anticipates   explores     creates
```

Foresight used to be a playbook inside Poiesis Insight. Until 1.4.3 Insight carried it, with a `foresight-analyst`
agent of its own; since Insight 2.0.0 only this plugin writes `foresight/`, with the same paths and fields.

- **One job each.** Research says what sources say and what the counts are. Foresight reads them forward. It does
  not scan, search or count.
- **None needs another.** When another product would really improve the answer, Claude says so once, in one line,
  and offers to install it. You can say no; the work goes on and the report says what was left out.
- **Depth you choose:** quick, standard (the default) or thorough, per request or as a line in your project's
  `CLAUDE.md`, e.g. `Depth: quick`. A few rules hold at every depth; every report ends with what was **not
  checked**.
- **Rules limit what is reported as true, never what may be explored.**

## Three questions

The playbooks follow the three questions of the UK Government Office for Science's
[Futures Toolkit](https://www.gov.uk/government/publications/futures-toolkit-for-policy-makers-and-analysts).

| You want to know | Playbook | What you get |
|---|---|---|
| **What is changing?** | | |
| Which signals matter | scan | the signals worth keeping, each with what was observed kept apart from what it might mean, and the kinds of source that are missing |
| Whether a subject is moving | trends | the yearly change against the series' own past, as numbers a script computed, with the unfinished year left out |
| How often such moves went on | base rates | of the earlier jumps in comparable series, how many kept going; or "not available" |
| Where each pattern sits | horizons | the current way, what is emerging, and what lies between |
| The forces behind it | drivers | the drivers that matter most, and the uncertain ones to build scenarios on |
| **What could it mean?** | | |
| Another way to see it | layers | the same issue read at four depths |
| What futures are possible | scenarios | two to four contrasting futures, each written to its advantage and to its cost, with what holds in all of them |
| What follows from one change | wheels | first effects, second effects and later ones, the unintended among them |
| What can be checked later | forecasts | a question, a probability and a date, with the model's independent runs and your own number logged apart |
| **What to do?** | | |
| Whether an idea survives | stress test | a concept or a decision read against every scenario: robust, needs changing, or redundant |
| What to watch | signposts | something that can be read again, the level that calls for a response, and the response prepared now |
| What happened since | review | forecasts scored, signposts read, and what became stale |

Before anything is reported it goes through a **challenge**: how often do things like this go on, what does the
contrary future look like, and does the detail add probability (it never does). Each conclusion comes out kept,
weakened or dropped, and the dropped ones are listed.

## Install

In Claude Code:

```
/plugin marketplace add gorgmihai92/poiesis-foresight
/plugin install poiesis-foresight@poiesis-foresight
```

It needs **Python 3**, which macOS and most Linux systems already have. It needs no keys and no account: its
scripts ask no database and send nothing anywhere. Signals and yearly counts come from
[Poiesis Research](https://github.com/gorgmihai92/poiesis-research), or from a table of your own.

## Ask in plain language

- *"Which of these signals should I keep an eye on?"*
- *"Is research on solid-state batteries still growing, or slowing?"*
- *"This topic jumped last year. How often does a jump like that last?"*
- *"Give me three contrasting futures for how designers work with AI in 2035."*
- *"Write five forecasts from this that we can check in three months."*
- *"Test this concept against each scenario."*
- *"What should I watch, and what would make me change course?"*
- *"Review my forecasts and signposts."*

## One skill picks a playbook; scripts do the counting

One skill, `foresight`, is the entry point. It says what input it found and what is missing, picks the playbooks
the request needs, and has every conclusion challenged before it is reported.

- **A series passes a gate first.** `series_gate.py` accepts a yearly series only when it says which database it
  came from, that the run was complete, and that the same document types were counted above and below the line of
  its share. It then adds the counts up again from the file that holds every type, and refuses a series whose
  types file is missing.
- **Growth is computed, not estimated.** `trends.py` gives each recent year's change, how far it is from the
  series' own earlier growth, the yearly rate over two spans, and the rate since the earlier peak. It prints the
  raw count and the share among all record types as checks, and does not read them.
- **The words are fixed by rule.** The script says "rose" or "fell", and growth "faster than", "in line with"
  or "slower than its own past". It never says "trend" or "emerging". Whether a subject is emerging takes more than growth, and the
  playbook asks for each part.
- **A forecast is three probabilities.** The model answers several times, independently; you give your own number
  before seeing the model's; the forecast of record is their mean. `forecasts.py --sources` scores each once outcomes are
  filled in.
- **Agents are model calls.** `foresight-analyst` takes one issue. `forecaster` gives one probability for one
  question and is run three times at standard depth. Claude says how many it will start.

## The same rules for every request

The rules are in `skills/foresight/rules.md`:

- **Every statement says where it comes from:** a source with how much of it was read, an observation, a number a
  script printed, documentation with its date, or a choice. Anything recalled and not checked is marked so.
- **An observation is kept apart from its reading.**
- **A share counts the same document types above and below the line,** or it is refused. A share on every
  record type is shown and not read.
- **The unfinished year is left out.**
- **One year is a lead,** not a trend.
- **A scenario is not a forecast** and has no probability.
- **A forecast is written before its outcome and never edited after.**
- **A model's judgment is never tested on events that already happened.**
- **A verdict is written once** and copied, never retyped.
- **No silent improvisation.** When a step has no playbook or script, Claude stops and says what is missing.
- **Every report ends with "Not checked".**

## Everything it writes stays in `foresight/`

```
foresight/
  <date>-<topic>.md     one piece of work: signals, series, drivers, horizons, scenarios, stress test, challenge
  forecasts.md          the forecast log: one row per forecast, scored when its date passes
  signposts.md          the signpost log: what is watched, its trigger, its response, its status
  reviews/<date>.md     what a review found
```

A scenario has an id (`SC-001`), a signpost (`SP-001`) and a forecast (`F-001`). A scenario says what it rests on
in a **From** line, so that when something it rests on is dropped later, a review can say what became stale.

## What it cannot do

- **It cannot show that foresight works.** The toolkit its methods come from says that proving the effect of
  futures work after the event "will be hard". In the parts read for this plugin, none of the method sources reports a test of whether its method leads to
  better decisions.
- **Counts say little about the next years.** They describe a database on the day it was read. The one method
  read here is not meant for less than two years ahead or more than five, and in between it cleared a modest bar
  only for clusters of 20 papers or more.
- **A model's forecast is not an expert's.** In the one benchmark read here, the best model scored about as well as
  the public's median forecast, with the crowd's forecast in hand for some questions, and behind the expert
  forecasters' median forecast. That is why the model's probability is logged
  beside yours and both are scored.
- **Its workshop methods were written for groups.** Scenarios, driver mapping, wheels and stress tests are
  described for groups: at least 6 people for drivers and wheels, at least 8 to 12 for scenarios, up to 16 for
  stress tests. Here one person works with a model. That swap is a choice and has
  not been tested.
- **Some rules are waiting.** Thresholds for calling a topic emergent were expected from a paper that could be
  read as an abstract only; whether it holds them is not known. The control-chart rules and the four layers that
  came from Poiesis Insight are kept, each marked where it stands as resting on a source not read here.
- **It has not been run in a real session yet.** The playbooks, the two agents and the eval cases were written,
  and tests check their files. What Claude does with them is not shown.
- **Signals and counts need Poiesis Research 2.4.0 or later.** With an older version, or none, give it a table of
  your own.

## What's in this repository

The repository is a Claude Code **marketplace** holding one **plugin**.

```
.claude-plugin/
  marketplace.json            the marketplace: its name and the plugins it lists (here, one)
plugins/
  poiesis-foresight/          the plugin
    .claude-plugin/
      plugin.json             name, version, description
    skills/foresight/         the skill: what Claude follows when you ask for foresight
      SKILL.md                entry point: says what input there is, picks the playbooks
      rules.md                where statements come from, numbers, ids, the verdict; shared by all playbooks
      playbooks/
        scan.md               which signals to keep
        trends.md             how a series moved against its own past
        base-rates.md         how often such moves went on
        horizons.md           the current way, the emerging one, and what lies between
        drivers.md            the forces that matter, and the uncertain ones
        layers.md             the same issue at four depths
        scenarios.md          contrasting futures
        wheels.md             the consequences of one change
        forecasts.md          questions with a probability and a date
        stress-test.md        one option against every scenario
        signposts.md          what to watch, and the response prepared for it
        review.md             a dated look back
        challenge.md          three questions about the future, and the verdict
      scripts/                Python 3, standard library only
        series_gate.py        accept or refuse a yearly series before it is read
        trends.py             growth against a series' own past; base rates of earlier jumps
        forecasts.py          score the forecast log, by source with --sources
        signposts.py          what is due, what reached its trigger, what is out of order
        ids.py                the next free id, and ids given twice
      templates/
        foresight.md          the outline of one piece of work
        signal.md             a signal that was kept
        scenario.md           a scenario
        forecasts.md          the forecast log
        signposts.md          the signpost log
        review.md             a review
    agents/
      foresight-analyst.md    foresight for one issue
      forecaster.md           one probability for one question
    evals/                    cases for `claude plugin eval`
research/                     the sources behind the rules: one note per source, each with how much was read
tests/                        tests of the scripts and of the plugin's files; they never use the network
CHANGELOG.md                  what changed in each version
LICENSE                       MIT
```

## Where the rules come from

Each playbook lists the notes its rules rest on, and there is one note per source in `research/notes`. Every note
has a **Read** line that says how much of the source was read and what was not. A rule with no source is a
choice and is said to be one. Two passages that came from Poiesis Insight rest on sources known here by title
only, and each says so where it stands.

- **The three questions, and the steps for scanning, drivers, scenarios, wheels and stress tests:** the UK
  Government Office for Science's Futures Toolkit (2024), read in part, with the pages in the note. Open
  Government Licence v3.0. It is practitioner guidance.
- **Growth is one part of emergence among five:** Rotolo, Hicks & Martin 2015, read in part.
- **Shares, not raw counts; growth from the earlier peak; small series mislead:** Klavans, Boyack & Murdick 2020,
  read in part.
- **The same document types on both sides, the unfinished year left out, one year is a lead:** one recorded run of
  these plugins, an observation. `trends.py` reproduces that run's 280 numbers.
- **Base rates in three steps:** Flyvbjerg 2006, read in part. Its subject is the cost of building projects; using
  it for research topics is an analogy.
- **Comparison classes first:** Chang, Chen, Mellers & Tetlock 2016, read in part. Looking back at misses was
  trained there and is not shown to help; doing it is this plugin's choice.
- **Several model runs, averaged with your own number, scored only forward:** Halawi et al. 2024, Schoenegger et
  al. 2024, Karger et al. 2025 and Paleka et al. 2025, each read in part. Those studies combined different models,
  or a model with a crowd; repeating one model and averaging it with one person are this plugin's choices.
- **Three horizons:** Sharpe et al. 2016, read in part.
- **What scenarios did to experts' judgment in three field studies:** Phadnis et al. 2015, read in part.
- **Signposts, triggers and prepared responses:** two chapters of Marchau, Walker, Bloemen & Popper (eds.) 2019,
  read in part.
- **Read as an abstract only,** and said to be so where a rule leans on one: Kahneman & Lovallo 1993, Tversky &
  Kahneman 1983, Börjeson et al. 2006, Mancini et al. 2010, Spaniol & Rowland 2023, Cuhls 2020, Amanatidou et al.
  2012, Mellers et al. 2015, Benneyan et al. 2003, Haasnoot et al. 2013, Carley et al. 2018.
- **Known by title only:** Hiltunen 2008, Inayatullah 1998, Meissner & Wulf 2013. The three parts of a signal and
  the four layers came from Poiesis Insight and rest on the first two; they are kept and marked.
- **Choices of this plugin, not findings:** the scripts' limits and windows, the definitions of a jump and of what
  followed it, the plain mean of the model's runs, equal weight for you and the model, the statuses of a signpost.

## Files shared with the other products

Writes `foresight/<date>-<topic>.md` (scenarios with what holds in all of them and what depends on one; signals
with **Horizon**) and `foresight/forecasts.md` (columns `id | question | probability | made | resolve by | outcome
| reasoning`). These are the paths and fields Poiesis Insight 1.4 wrote, unchanged, and Poiesis Frontier reads
them.

New in this plugin: three columns at the end of the forecast log (`model`, `owner`, `wording`);
`foresight/signposts.md`; `foresight/reviews/`; and the ids `SC-001` and `SP-001`, with a **From** line on each
scenario. When Poiesis Insight is installed, a scenario's verdict is stamped in `insights/challenge-stamps.jsonl`
by Poiesis Insight's own script.

Reads `research/signals/`, `research/data/`, `research/notes/` and `research/README.md` from Poiesis Research, and
`insights/` from Poiesis Insight. The paths and fields the products share are a contract: they change only in a
major version, noted in the changelog. A missing file or field is reported as unknown, never an error.

## Update or remove

```
/plugin marketplace update poiesis-foresight
/plugin update poiesis-foresight@poiesis-foresight
/plugin uninstall poiesis-foresight@poiesis-foresight
```

## Changing the plugin

Edit the files under `plugins/poiesis-foresight/`, then run the two checks from the repository's root:

```
python3 -I -m unittest discover -s tests
claude plugin validate plugins/poiesis-foresight
```

Validate at the plugin's path: `claude plugin validate .` at the root checks only the marketplace file. The tests
never use the network. A new rule starts with reading its source and a note in `research/notes/` that says how
much was read. Bump the version (major if a path or field under "Files shared" changes) in `plugin.json`,
`marketplace.json` and `CHANGELOG.md`.

## License

MIT. The steps of the scan, drivers, scenarios, wheels, stress-test and horizons playbooks are adapted from The
Futures Toolkit (Government Office for Science, 2024), © Crown copyright 2024, licensed under the
[Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
