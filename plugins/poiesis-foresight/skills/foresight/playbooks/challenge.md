# Challenge

Every reading of a series, placement on a horizon, scenario logic, forecast and signpost goes through this before
it is reported. The goal is to find why it might be wrong, not to defend it.

## Read first
Notes in `research/notes` of the plugin's repository. Each says how much of its source was read.
- `flyvbjerg-2006-reference-class-forecasting`: read in part (p. 2–14, 16–17), and `kahneman-1993-outside-view`:
  abstract only. The base rate.
- `mancini-2010-contravision`: abstract only. Two versions of one future drew a wider range of reactions from
  people than one. Using contrast to test a scenario is this plugin's extension of that.
- `tversky-1983-conjunction-fallacy`: abstract only. People, experts among them, judged a detailed case more
  probable than a less detailed one that contains it. The arithmetic the third question rests on needs no source.
- `halawi-2024-llm-forecasting` and `schoenegger-2024-silicon-crowd`: read in part. In one study a model system
  rarely gave low probabilities; in the other, models leaned toward "yes".
- `poiesis-lab-2026-recorded-runs`: an observation. Of 16 conclusions sent to a challenger, 1 was kept as written.

## Three questions about the future
1. **Base rate.** How often do things like this go on, come true or arrive on time? Name the class and its count
   (`playbooks/base-rates.md`), or write "not available". A conclusion that starts from the story of this one case
   and has no class behind it is at most weakened.
2. **Futures in contrast.** Write the future that contradicts this one, as carefully. What would have to be true
   for it? Does the evidence tell the two apart, or would it look the same under both? For a scenario: write it to
   its advantage and to its cost, and see which reading the evidence supports.
3. **Detail adds no probability.** Count the conditions the conclusion needs. Each one more makes it less likely,
   never more: a scenario with five conditions cannot be more probable than the same scenario with three. If
   the detailed version feels more convincing, that is the feeling to distrust. Give the probability of the
   plainest version first.

## For a series
- Did it pass the gate, with the same document types above and below the line?
- Is the unfinished year out?
- Is it one year, or more? One year is a lead.
- Does it hold under a second choice of windows, and against a second database or other wordings?
- Does the raw count say the same as the share? If only the raw count moved, the database moved.

## For a forecast
- Is the question one a stranger could settle?
- Asked the other way round, do the two answers add up to about 1?
- Near 0 or 1: was it pulled toward the middle for comfort?
- Were the model's runs independent, and was the owner's probability given before theirs was shown?

## Verdict, with one line of reason
- **Kept:** survives the questions that apply; say how sure.
- **Weakened:** survives as a narrower claim or with less confidence; say what was narrowed.
- **Dropped:** it has no base rate and rests on the story of one case, or its contrary fits the evidence as well, or
  it needs more conditions than the evidence supports.

A verdict is written once. It is copied wherever it is shown and never retyped, softened or upgraded. Testing a
conclusion again gives a new, dated verdict beside the old one. Report the kept and the weakened, and list the
dropped briefly: what was dropped teaches as much.

Where it is written: for a scenario, as one line under its heading, the verdict word first:
`- **Challenge:** weakened · <the reason>`. For every other conclusion, as a row of the note's challenge table,
with the conclusion as one sentence as it stands after the challenge.

## With poiesis-insight
This playbook is short on purpose: it holds the questions that are about the future. poiesis-insight holds the
general challenge: rivals, diagnosticity, independence, chance, sensitivity, consistency, denominators,
replication.
- **When poiesis-insight is installed** (`claude plugin list`), run its `playbooks/challenge.md` as well, on the
  same conclusions. At thorough depth use its `challenger` agent: give it the conclusions and the data, not the
  reasoning.
- **When it is not,** say so once with its link, go on with the questions above, and write "the general challenge
  of poiesis-insight was not run" under "Not checked".
