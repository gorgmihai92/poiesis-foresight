# Developing expert political judgment: the impact of training and practice on judgmental accuracy in geopolitical forecasting tournaments (Chang, Chen, Mellers & Tetlock, 2016)

- **Source:** Judgment and Decision Making 11(5): 509–526 · https://doi.org/10.1017/S1930297500004599 (the
  journal's own PDF; pages = PDF pages, 18 in all, so p. 1 is the printed p. 509)
- **File:** `../papers/chang-2016-developing-expert-political-judgment.pdf` (local)
- **Licence:** Creative Commons Attribution 3.0, as the article states (p. 1).
- **Evidence:** empirical · a randomised training experiment in a four-year forecasting tournament, with 97 to
  205 forecasters per condition and year (p. 7, Table 4).
- **Read:** part of the text, on 2026-11-22: the abstract (p. 1), the scoring rule (p. 4), the training design and
  the two tables of principles (p. 5–6), the first results passage and Table 4 (p. 6–7), one passage of the discussion (p. 12). A fetch agent read the
  whole HTML edition on 2026-11-21 and its report led the search. Not read here: the literature review
  (p. 2–3), the results on practice, mediation and individual differences (p. 8–14), the discussion (p. 15–16).

## What it says
- A training module of less than one hour "consistently improved accuracy (Brier scores) by 6 to 11% over the
  control condition" in each of four years (p. 1). Table 4 gives 10% and 11% in year 1 (two kinds of training),
  12% in year 2, 6% in year 3 and 7% in year 4 (p. 7).
- What the training taught: event base rates; updating belief in step with the weight of new evidence; "the
  value of averaging independent evidence"; the difference between calibration and resolution; the pros and
  cons of statistical models; common biases in probability judgment (p. 5).
- From year 3 the principles were listed as CHAMPS KNOW: Comparison classes, Hunt for the right information,
  Adjust and update forecasts when appropriate, Mathematical and statistical models, Post-mortem analysis, Select
  the right questions to answer; Know the power players and their preferences, Norms and protocols of
  institutions, Other perspectives should inform forecasts, Wildcards, accidents and black swans (p. 6, Table 3).
- Of the principles, the one tied to accuracy in the forecasters' own explanations was the first: "self-reported
  use of comparison classes was correlated with lower Brier scores" (p. 6).
- Of the other principles the paper says they "did not prove useful here", and that it would be premature to
  conclude only comparison classes matter (p. 12).
- The scores are on the original Brier scale, which runs from 0 to 2 (p. 4). They cannot be set beside scores on
  the 0 to 1 scale that `forecasts.py` prints.
- The authors call the effects "likely to be lower-bound estimates", and say future work should find which parts
  of the training did the work (p. 1).

## What it means for the plugin
- `playbooks/forecasts.md` puts the comparison class first: before a probability is written, the forecast names
  the class of similar cases and its rate (`playbooks/base-rates.md`).
- A forecast is updated when evidence arrives, and the update is a new row in the log, not an edit of the old one.
- When dates pass, the scored forecasts are read again for what went wrong. The paper trained this as
  "post-mortem analysis" and does not show it helping: `playbooks/review.md` does it as this plugin's choice.
- The study trained people and measured people. That the same list improves a language model's forecasts is not
  shown by it. The list is used here as a checklist for the owner's own probability, and as the order of the
  forecast note.
- The political principles (KNOW) are about geopolitical questions and are not carried over.

## Quotes
- "it consistently improved accuracy (Brier scores) by 6 to 11% over the control condition" (p. 1)
- "Training evolved from year 1 to 4, but was never designed to take more than an hour." (p. 5)
- "the value of averaging independent evidence" (p. 5)
