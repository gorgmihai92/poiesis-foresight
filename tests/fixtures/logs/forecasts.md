# Forecast log (test fixture)

These are not real forecasts. Each row exercises one behaviour of `forecasts.py`. Dates are far in the past or far
in the future, so the result does not depend on the day the tests run.

| id | question (precise, checkable) | probability | made | resolve by | outcome | reasoning (note) | model (independent runs) | owner |
|---|---|---|---|---|---|---|---|---|
| F-001 | A row from before the new columns | 0.80 | 2019-01-01 | 2019-06-30 | 1 | fixture |
| F-002 | Both sources, of record is their mean | 0.35 | 2019-01-01 | 2019-06-30 | 0 | fixture | 0.20 0.30 0.40 | 0.40 |
| F-003 | Both sources, happened | 0.70 | 2019-01-01 | 2019-06-30 | 1 | fixture | 0.60 0.70 0.80 | 0.70 |
| F-004 | Of record is not the mean, and two runs only | 0.90 | 2019-01-01 | 2019-06-30 | 1 | fixture | 0.50 0.50 | 0.70 |
| F-005 | No owner probability | 0.50 | 2019-01-01 | 2019-06-30 | 0 | fixture | 0.40 0.50 0.60 |  |
| F-006 | Model cell is a word | 0.50 | 2019-01-01 | 2019-06-30 | 0 | fixture | likely | 0.30 |
| F-007 | Not due yet | 0.50 | 2019-01-01 | 2099-12-31 |  | fixture | 0.40 0.50 0.60 | 0.50 |
| F-008 | Past its date with no outcome | 0.60 | 2019-01-01 | 2020-01-01 |  | fixture | 0.55 0.60 0.65 | 0.60 |
