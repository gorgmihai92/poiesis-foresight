---
type: forecast-log
plugin: poiesis-foresight
date: <YYYY-MM-DD, the day the log was started>
topic: "<the project, in a few words>"
---
# Forecast log

One line per forecast. `outcome` stays empty until the resolve date, then 1 (happened) or 0 (did not).
Score with: `python3 -I <scripts>/forecasts.py foresight/forecasts.md`, and with `--sources` to score the model's
and the owner's probabilities apart and to see the gap between the two wordings.

A row is written before its outcome is known and is not edited afterwards, apart from filling in `outcome`. A
changed view is a new row that names the old one. No cell contains a `|`. The first seven columns keep their
order; a new column goes at the end.

- `probability` is the forecast of record: the mean of `owner` and of the mean of `model`, or the one that exists.
- `model` holds the probabilities of the model's independent runs, separated by spaces, each as the probability
  that the question as written happens: a run given the negation, which answered p', is written as 1 − p'.
- `owner` holds the owner's own probability, written before seeing the model's.
- `wording` says for each run, in the order of `model`, which wording it was given: `written` or `negated`.

| id | question (precise, checkable) | probability | made | resolve by | outcome | reasoning (note) | model (independent runs) | owner | wording (of each model run) |
|---|---|---|---|---|---|---|---|---|---|
| <F-001> | <Will … by …?> | <0.30> | <YYYY-MM-DD> | <YYYY-MM-DD> |  | <link to foresight note> | <0.25 0.30 0.35> | <0.30> | <written negated written> |
