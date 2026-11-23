# Rules (every playbook)

## Depth
Some rules hold at every depth; the rest are defaults, scaled to what is at stake. The user picks the depth, or the
project sets it with a `Depth:` line in its `CLAUDE.md` (read in every session, by every Poiesis plugin);
otherwise **standard**.
- **Always:** every statement says where it comes from; an observation is kept apart from its reading; a series
  passes the gate before it is read; numbers come from the scripts; a scenario is never given as a forecast; a
  forecast has a question, a probability and a date, and is logged before its outcome; a verdict is written once;
  nothing from memory unmarked; no step improvised.
- **Quick:** one pass, inline. One model probability, logged as one run.
- **Standard:** the playbook as written. Three independent model runs for a forecast.
- **Thorough:** also a second database or wording for every series where poiesis-research can count one, and five
  model runs.
- **The challenge at each depth,** who gives its verdict and how a scenario's verdict is stamped:
  `playbooks/challenge.md`, "Who gives the verdict" and "Stamping a scenario's verdict".

A default may be skipped at any depth if the report says which one and why. Every report ends with **Not
checked:** what was skipped, or "nothing". These rules limit what is reported as true, never what may be explored.

## Where a statement comes from
Every statement of fact carries one of these, in words:
- **a source,** with how much of it was read: full text, part of the text, abstract only, or title only. "Title
  only" means the work exists; nothing more is claimed about it;
- **an observation:** what a file in the project or a run shows; name the file or the run;
- **a number from a script,** pasted as printed, with the script named;
- **documentation,** with the date it was read;
- **a choice:** a decision of the plugin or of the user. A choice is not evidence.

Anything recalled and not checked is marked "from general knowledge, unverified". Everything else in a foresight
report is interpretation, and is labelled so: "the series shows" against "this suggests".

## No silent improvisation
When a step has no playbook or script, stop and say what is missing. Offer the choices: an existing method used
more narrowly, building the tool first, or skipping the step and recording it under "Not checked". Do not improvise
the step and report it as done. The same holds when an input is missing: no signals, no series, no scenarios.

## Numbers
- A series from poiesis-research is read only after `series_gate.py` accepts it: complete metadata, a database
  that answered, a complete run, and the same document types above and below the line of its share.
- A share with different document types on its two sides is refused. It is not recomputed another way. A share
  that counts every record type on both sides is shown and not read.
- The unfinished year is left out and named.
- Growth, distances from a series' own past, rates and base rates come from `trends.py`; scores from
  `forecasts.py`; what is due from `signposts.py`; ids from `ids.py`. Their output is pasted, not retyped.
- The limits those scripts use (2 standard deviations, 20 works, 20 cases, the windows) are choices and are said
  to be choices wherever a reading depends on one.
- "Not found" is not "does not exist". Keep the Coverage line of whatever poiesis-research ran, and name the
  databases that refused.

## Signals, scenarios, forecasts
- A signal is what was observed. What it might mean is its reading, on a separate line.
- A scenario describes a future that could be. It has no probability, and it is written to its advantage and to
  its cost.
- A forecast is a question someone else could settle, a probability and a date, logged before the outcome and
  not edited after.
- The model's probability is logged as the model's, beside the owner's, and both are scored. The model's
  judgment is never tested on events whose outcome is already known.
- A signpost has its trigger and its response written before the value is read.

## Ids and what a thing rests on
- A scenario has an id (SC-001), a signpost (SP-001), a forecast (F-001). `ids.py` gives the next one; a number is
  never used twice. Signals keep the ids poiesis-research gave them (SG-001).
- **Id** is one line under the heading: `- **Id:** SC-001`. **From** is one line listing what the thing rests on:
  ids and citation keys, separated by commas.
- When something named in a **From** line is later dropped, weakened or challenged again, what rests on it is
  stale. A review lists it; nothing rewrites it.
- In a table, no cell contains a `|`, so no link with an alias. A new column goes at the end.

## The challenge and its verdict
- Every conclusion goes through `playbooks/challenge.md` before it is reported: kept, weakened or dropped, with
  one line of reason.
- A verdict is written once, by the challenge. It is copied, never retyped, softened or upgraded. A second test
  gives a new, dated verdict beside the old one.
- Dropped conclusions are listed with the reason.

## Where these rules come from
Notes in `research/notes` of the plugin's repository. Each note's **Read** line says how much of the source was
read, and what was not.

Read in part, with the pages or sections in the note: the UK Government Office for Science's Futures Toolkit 2024 (the frame
of three questions, scanning, drivers, scenarios, wheels, stress-testing, three horizons; practitioner guidance,
and it says itself that the effect of futures work is hard to prove); Rotolo, Hicks & Martin 2015 (what
"emerging" needs besides growth); Klavans, Boyack & Murdick 2020 (shares, the earlier peak, small series, one
base rate); Flyvbjerg 2006 (the three steps of a base rate); Chang, Chen, Mellers & Tetlock 2016 (comparison
classes; looking back at misses was trained there and is not shown to help); Halawi et al. 2024, Schoenegger et al. 2024, Karger et al. 2025 and Paleka et
al. 2025 (what a model's forecast is worth, how to combine it, and why it is scored only forward); Sharpe et al.
2016 (the three horizons); Phadnis et al. 2015 (what scenarios did to experts' judgment); Walker, Marchau &
Kwakkel 2019 and Haasnoot, Warren & Kwakkel 2019 (signposts, triggers, responses, lead time).

Read as an abstract only, and said to be so where a rule leans on one: Kahneman & Lovallo 1993, Tversky & Kahneman
1983, Börjeson et al. 2006, Mancini et al. 2010, Spaniol & Rowland 2023, Cuhls 2020, Amanatidou et al. 2012,
Mellers et al. 2015, Benneyan et al. 2003, Haasnoot et al. 2013, Carley et al. 2018.

Known by title only: Hiltunen 2008, Inayatullah 1998, Meissner & Wulf 2013. Two passages that came from
poiesis-insight rest on the first two: the three parts of a signal, and the four layers. They are kept as they
came, and each says where it stands that its source was not read. Nothing is taken from the third.

An observation: one recorded run of the plugins on 2026-11-17 (the same document types on both sides; one year
is a lead; a verdict is copied).

Choices of this plugin, not findings: the script's limits and windows; the definitions of a jump and of what
followed it; the plain mean of the model's runs; equal weight for the owner and the model; the statuses of a
signpost; the id prefixes; using workshop methods with one person and a model.

Waiting for a source to be read: thresholds for emergence, which the plan expected from Carley et al. 2018 (its
abstract gives none; whether the paper does is not known). Kept from poiesis-insight and marked unverified until
their sources are read: the control-chart rules, what makes a signal weak, the four layers.
