# Pitfalls in evaluating language model forecasters (Paleka, Goel, Geiping & Tramèr, 2025)

- **Source:** arXiv:2506.00723v1, 31 May 2025 · https://arxiv.org/abs/2506.00723 (a preprint; pages = PDF pages,
  20 in all)
- **File:** `../papers/paleka-2025-pitfalls-evaluating-forecasters.pdf` (local only)
- **Licence:** not checked: kept local only.
- **Evidence:** analytical · an argument with examples taken from earlier forecasting benchmarks (p. 1–2).
- **Read:** part of the text, on 2026-11-22: the abstract and the overview of the two challenges (p. 1–2), the
  opening of the section on logical leakage (p. 3), the recommendation on metrics (p. 9) and the closing
  recommendations (p. 10). Not read: the detailed analyses and examples (p. 3–9 apart from those passages), the
  section on optimising forecasters, the appendices (p. 11–20).

## What it says
- The sound way to evaluate a forecaster is to ask about future events, collect predictions and score them as
  the events resolve; this can take months or years, so researchers test on the past instead (p. 2).
- Testing on the past leaks the answer in several ways. The choice of questions can give it away. Search limited
  to a past date is unreliable, because dates on documents are often wrong and the search model itself was
  trained on later data. And a model's training cut-off is "more of a guideline than a guarantee" (p. 2).
- Claims that models match people may be circular: where the questions come from forecasting platforms, the
  human forecasts are probably available to the model, which "might simply be copying human forecasts" (p. 2).
- A benchmark can reward a bold bet over an honest estimate of uncertainty (p. 2).
- Metrics pull in different directions; the authors recommend "computing at least Brier score, calibration, and
  logarithmic score" (p. 9).
- They recommend that evaluations "collect their own questions about events that are as recent as possible"
  (p. 10).

## What it means for the plugin
- The plugin does not test a model's judgement on past events. "Would this method have spotted X in 2017?" is
  allowed only for indicators that code computes from counts, and even those read today's database.
- A forecast counts only if it was written before the outcome. The log keeps the date made, and `review` scores
  nothing that was added or changed afterwards.
- `forecasts.py` prints the Brier score. Calibration and the logarithmic score, which the authors also ask for,
  are not computed in 0.1.0: a log needs many resolved forecasts before either says anything, and the script
  says how many it has.
- An argument paper, read in part. It tells what can go wrong in a test; it gives no measure of how often it does.

## Quotes
- "cutoffs are more of a guideline than a guarantee" (p. 2)
- "the models might simply be copying human forecasts rather than demonstrating independent ability" (p. 2)
- "we recommend computing at least Brier score, calibration, and logarithmic score" (p. 9)
