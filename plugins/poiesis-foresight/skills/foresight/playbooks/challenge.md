# Challenge

Every reading of a series, placement on a horizon, scenario logic and forecast goes through this before
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
2. **Futures in contrast** (an extension of Mancini et al. 2010, abstract only). Write the future that contradicts
   this one, as carefully. What would have to be true
   for it? Does the evidence tell the two apart, or would it look the same under both? For a scenario: write it to
   its advantage and to its cost, and see which reading the evidence supports.
3. **Detail adds no probability** (the arithmetic is certain; that people judge otherwise is Tversky & Kahneman
   1983, abstract only). Count the conditions the conclusion needs. One more cannot make it more likely: a scenario with five conditions cannot be more probable than the same scenario with three. If
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
- Asked the other way round (the runs given the negation, `playbooks/forecasts.md`), how far apart are the two
  halves, as `forecasts.py --sources` prints the gap?
- Near 0 or 1: was it pulled toward the middle for comfort?
- Were the model's runs independent, and was the owner's probability given before theirs was shown?

## Verdict, with one line of reason
- **Kept:** survives the questions that apply; say how sure.
- **Weakened:** survives as a narrower claim or with less confidence; say what was narrowed.
- **Dropped:** its contrary fits the evidence as well, or it needs more conditions than the evidence supports. A
  conclusion with no class behind it is weakened, not dropped, and says it rests on the case alone.

A verdict is written once. It is copied wherever it is shown and never retyped, softened or upgraded. Testing a
conclusion again gives a new, dated verdict beside the old one. Report the kept and the weakened, and list the
dropped briefly: what was dropped teaches as much.

Where it is written: for a scenario, as one line under its heading, the verdict word first:
`- **Challenge:** weakened · <the reason>`. For every other conclusion, as a row of the note's challenge table,
with the conclusion as one sentence as it stands after the challenge.

## Who gives the verdict
This playbook is short on purpose: it holds the questions that are about the future. poiesis-insight holds the
general challenge: rivals, diagnosticity, independence, chance, sensitivity, consistency, denominators,
replication. Each conclusion gets one verdict, from one of the two, never both. This is the one place the rule is
written; `rules.md` points here.
- **Quick and standard depth:** the verdict is this playbook's own challenge, inline: the questions above. Write
  "the general challenge of poiesis-insight was not run" under "Not checked".
- **Thorough depth, when poiesis-insight is installed** (`claude plugin list`): the verdict is its `challenger`
  agent's. Give it the conclusions, the data and the questions above, not the reasoning. Its verdict replaces the
  inline one: it is the verdict, not a second one beside it. Each scenario goes in a call of its own, with its id,
  its name as the sentence to judge, and its body and data, because `--verdicts` (below) refuses a whole answer
  when one block in it cannot be stamped. The other conclusions go together in one more call; their verdicts go in
  the challenge table and are not stamped.
  Say how many calls will be made before making them. Save each answer as it came, before anything else is done
  with it: `foresight/challenges/<YYYY-MM-DD>-<topic>-SC-001.md` for a scenario.
- **Without poiesis-insight,** the inline challenge at every depth. At thorough, say once, with its link, that the
  independent challenger was not run, and write "the general challenge of poiesis-insight was not run" under "Not
  checked".

poiesis-insight's `playbooks/challenge.md` is not run on foresight's conclusions: its general questions come in
through its `challenger`, at thorough depth.

## Stamping a scenario's verdict
Other plugins read a verdict from its stamp, not from the note: poiesis-frontier's gate and poiesis-studio's
report. A stamp is written by poiesis-insight's own script; this plugin writes none of its own.
- **When poiesis-insight is installed,** once the verdict is on the scenario's Challenge line, stamp it, one
  scenario at a time, from the project's root. `$I` is poiesis-insight's scripts folder, in the version that
  `claude plugin list` shows enabled: `~/.claude/plugins/cache/poiesis-insight/poiesis-insight/<version>/skills/insight/scripts`
  (only if that cannot be read, Glob for `**/poiesis-insight/*/skills/insight/scripts/challenge_stamp.py` there
  and take the highest version folder).
  - **The challenger's verdict, kept or dropped:** from its saved answer, so the verdict is not typed by hand and
    the script checks that the answer's Claim is the scenario's name:
    `python3 -I $I/challenge_stamp.py write --note foresight/<YYYY-MM-DD>-<topic>.md --verdicts foresight/challenges/<YYYY-MM-DD>-<topic>-SC-001.md --by agent`
  - **The challenger's verdict, weakened:** a scenario's name is not a claim, so it is not renamed to the narrower
    claim; that claim goes, word for word, into the scenario's **Holds only if**, and the Challenge line says
    `weakened`. `--verdicts` would refuse it (it wants the heading to be the narrower claim), so copy the verdict
    word from the saved answer:
    `python3 -I $I/challenge_stamp.py write --note foresight/<YYYY-MM-DD>-<topic>.md --id SC-001 --verdict weakened --by agent`
  - **The inline challenge** (no agent answer exists):
    `python3 -I $I/challenge_stamp.py write --note foresight/<YYYY-MM-DD>-<topic>.md --id SC-001 --verdict <kept, weakened or dropped> --by inline`

  The stamp goes in `insights/challenge-stamps.jsonl`, the one file for every kind of object. Paste what the
  script prints. A `REFUSED` line is reported as printed, and that scenario is unstamped.
- **What the stamp covers:** the scenario's heading, its name, and the verdict; not its body. A renamed scenario
  no longer verifies, but an edit to its body after the challenge is not detected: the gate still lets it
  through. So after any edit of substance to the world, the conditions or what would prove it wrong, challenge it
  again and stamp the new verdict with `--again "<why>"`; no line is edited.
- **When poiesis-insight is not installed,** the scenario keeps its Challenge line only. Write under "Not
  checked": "the scenarios' verdicts are not stamped (poiesis-insight is not installed), so other plugins read
  them as unstamped".
- The other conclusions, the rows of the note's challenge table, have no heading and Id line, and are not
  stamped.
