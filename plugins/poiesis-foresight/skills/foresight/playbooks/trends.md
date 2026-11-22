# Trends in data

Whether a yearly series moved, measured against its own past. The numbers come from a script. The words that
describe them are fixed by rule. Whether the movement means anything is decided after the challenge.

## Read first
Notes in `research/notes` of the plugin's repository. Each says how much of its source was read.
- `poiesis-lab-2026-recorded-runs`: an observation. In a recorded run a share fell only because the database had
  added other kinds of records, and raw counts made three areas of five look unusual where the share showed one.
- `klavans-2020-exceptional-growth`: read in part (p. 1–3, 6–8, 14, 21–22). Growth is measured on shares and from
  the earlier peak; small series mislead; counts say little about the next two years or beyond five.
- `rotolo-2015-emerging-technology`: read in part (p. 1, 10–15, 23–25, 30–33). Fast growth is one attribute of
  emergence among five, it is relative, and the choice of windows and thresholds can create the finding.
- `benneyan-2003-control-charts`: abstract only. A series varies when nothing has changed. The control-chart
  rules poiesis-insight's playbook names (limits at about three standard deviations, runs on one side) are not in
  the abstract. They are kept below as they came, marked unverified.
- `carley-2018-indicator-technical-emergence`: abstract only. The thresholds the lab plan expected from it wait.

## As it came from poiesis-insight
When the data have a time order (survey waves, usage logs, metrics), a trend is reported only after three checks:
- **Signal or noise:** is the change larger than the series' usual variation? Draw the series with its mean and
  limits at about three standard deviations, and look for points outside them or a long run on one side
  (control charts; Benneyan et al. 2003). Say how many points the series has; a few points give a lead, not a trend.
- **Base rate:** how often do similar changes, in similar series or past periods, continue? Start the forecast from
  that outside view and adjust it, not from the story of this case (Kahneman & Lovallo 1993).
- **Shape:** steady, speeding up, slowing down or leveling off; seasonal; a sudden break. Extrapolate only as a
  dated forecast in the log, never as a statement.

This passage is kept word for word. The limits at about three standard deviations and the run on one side come
from a source read here as an abstract only, which does not state them: they are marked "from general knowledge,
unverified", as poiesis-insight's own note marks them. `trends.py` computes the distance in standard deviations
(`--z 3` gives the passage's limit) and does not look for runs. For data that are not yearly, put the period's
number in the `year` column.

## Before a series is read
1. **The gate.** `python3 -I $S/series_gate.py research/data/<name>.csv`. A series is accepted only when its
   metadata names the database and shows that it answered, says the run was complete, and declares the same
   document types above and below the line. A refused series is not read. Give the reasons as printed and offer
   the choices: run `counts.py` again (poiesis-research), read the user's own table with `--own`, or leave the
   step out and record it under "Not checked".
2. **No series.** When the project has none, say so. poiesis-research counts them (`counts.py`); suggest it once.
   The user's own table works too. Never use numbers from memory.
3. **Windows before numbers.** The last three full years are read against the ten growth figures before them, and
   two five-year rates are compared. These are the script's defaults. Changing one after seeing the numbers means
   reporting both results.

## Compute
`python3 -I $S/trends.py research/data/<name>.csv` (one series: `--series <id>`). For a table of your own:
`python3 -I $S/trends.py --own table.csv --last-full-year <year> --above "<what is counted>" --below "<the same>"`.
Paste what it prints. Do not round it again, reword it or work out a figure by hand.

## The three checks
1. **Signal or noise.** Is the change larger than the series' usual variation (Benneyan et al. 2003, abstract
   only)? The script gives each recent year's
   growth as a distance from the series' own earlier growth, in standard deviations (z). With fewer than five
   earlier growth figures it gives none: the series is then a lead. Say how many years the series has.
2. **Base rate.** How often did a change like this go on? `playbooks/base-rates.md`.
3. **Shape.** Steady, speeding up, slowing or levelling off: compare the two yearly rates the script prints and
   the recent years, and say which as interpretation, in those words or plainer ones. Extrapolate only as a dated forecast in the log (`playbooks/forecasts.md`), never as a
   statement.

## Rules
- **The share is read; the checks are not.** The share counts the same document types above and below the line.
  The raw count and the share among all record types are printed as checks. A share among all record types falls
  when the database adds records the search does not find, and a raw count rises with the database
  (`poiesis-lab-2026-recorded-runs`; Klavans et al. 2020, p. 6).
- **A share with different types on its two sides is refused,** by the gate and by the script. Do not compute it
  another way.
- **The unfinished year is left out.** The report names it.
- **A recovery is not a rise.** When the series is still below an earlier peak, the script says so, and the growth
  is given from that peak (Klavans et al. 2020, p. 7).
- **Small numbers are flagged.** Below 20 works in a year, a few works move the figures. The limit is Klavans et
  al.'s cut-off for clusters of papers (p. 8), borrowed here as a choice.
- **A series belongs to its database and its day.** Two series fetched on different days are two series. Say both
  dates and do not join them.
- **One year is a lead.** One year above a series' own past is written as that. It becomes a forecast or a
  signpost, not a claim about what comes next.
- **Say what the own past is made of,** and try a second choice (`--baseline`, `--recent`). A past that contains
  the series' own take-off can make later years look ordinary (`poiesis-lab-2026-recorded-runs`), and the choice
  of window can create a finding (Rotolo et al. 2015, p. 30–31).
- **The script's words only:** "rose", "fell", and growth "faster than", "in line with" or "slower than its own
  past". A series can rise and still grow slower than before: that is not a fall. The limit between the three
  is 2 standard deviations (`--z`), which is a choice: no source that was read gives one.
- **A share on every record type is not read.** When both sides count "all", the script shows the numbers as a
  check and gives no reading. It is the measure that produced a false decline in the recorded run.

## Is it emerging?
Do not call a subject emerging because its count grew. In the definition read here (Rotolo et al. 2015, p. 13),
fast growth is one of five attributes, and each is addressed or marked "not assessed":
- **Radical novelty:** the nearest existing work, from poiesis-research's prior-art playbook. Not assessed here.
- **Relatively fast growth:** this playbook, against the series' own past. The paper asks for a comparison
  with other subjects in the same field as well; no script here makes one, so say it was not made. The paper gives no absolute level and calls one "rather meaningless" (p. 14).
- **Coherence:** whether the thing holds together and has its own identity. No script here measures it.
- **Prominent impact:** it lies in the future. Write it as a forecast.
- **Uncertainty and ambiguity:** say what could still go several ways.

One published point of comparison: among clusters of at least 20 papers in Scopus, about 1.5% reached "exceptional
growth", defined as more than 8% a year in share, measured from the cluster's peak year to three years after the forecast
(Klavans et al. 2020, p. 7–8). It belongs to those clusters and that definition. Quote it with its conditions or not at all.

## What the numbers cannot show
- The database of today, not that of each year. Counts for past years moved between two fetches four days apart (the lab's log of 2026-11-21, an observation).
- The latest years are the least settled: lags in indexing may add to this (Rotolo et al. 2015, p. 30).
- The next years. Publication counts are a weak guide under two years and beyond five. In the window between, the
  one published method read here stayed under its own accuracy bar in every year until communities of fewer than
  20 papers were left out (Klavans et al. 2020, p. 14, 21).
- Works the database does not hold, and words the search does not match.

## Then
Every reading goes through `playbooks/challenge.md` before it is reported.

## Report
- **For each series:** the gate's line, the script's output as printed, and the shape in one sentence.
- **How it was counted:** the database, the date fetched, the document types and what the search matched (the
  `search_field` line), as the series' metadata has them. Copy them; do not describe the search in other words.
- **Not checked:** for example a second database, a second choice of windows, the base rate.

## Save (see SKILL.md, "Saving")
In `foresight/<YYYY-MM-DD>-<topic>.md`, under "Series".
