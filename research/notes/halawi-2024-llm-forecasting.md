# Approaching Human-Level Forecasting with Language Models (Halawi, Zhang, Yueh-Han & Steinhardt, 2024)

- **Source:** arXiv:2402.18563v1, 28 February 2024 · https://arxiv.org/abs/2402.18563 (a preprint; pages = PDF
  pages, 37 in all)
- **File:** `../papers/halawi-2024-human-level-forecasting.pdf` (local only)
- **Licence:** not checked on the arXiv page: kept local only.
- **Evidence:** empirical · a retrieval system built on language models, scored on 914 binary questions from
  five forecasting platforms against the platforms' crowd forecasts (p. 4, 6).
- **Read:** part of the text: the abstract and the passages on the test set, the evaluation, the ensembling, the
  results, the comparison with the crowd and the conclusion (p. 1–2, 4, 6–7, 9–13), found by searching the
  extracted text on 2026-11-22. A fetch agent read sections 1 to 8 of the HTML edition on 2026-11-21 and its
  report led the search. Not read: the appendices (p. 14–37), which hold the prompts and the trimming rule.

## What it says
- On the test set the system's Brier score was .179 and the crowd's .149; accuracy was 71.5% and 77.0% (p. 6,
  Table 3; p. 9).
- A weighted average of the system and the crowd, with four times the weight on the crowd, scored .146 (p. 6,
  12). The weight was chosen on the validation set (p. 12).
- The system's own forecast is an ensemble: six forecasts, three from a base model and three from a fine-tuned
  one, combined by a trimmed mean, which did best on the validation set among the methods tried (p. 7).
- The system does worse than the crowd where the crowd is highly certain, "likely because it rarely outputs low
  probabilities" (p. 10). The authors' guess at the cause is the model hedging; they call it a hypothesis (p. 10).
- Where the crowd's forecast was between .3 and .7, the system's Brier score was .238 and the crowd's .240 on the
  test set (p. 6, Table 3).
- Test questions were opened after the models' knowledge cut-off, so the answer could not be in the training data
  (p. 2, 4). The paper gives the date as June 1, 2023 on p. 2 and as June 1, 2024 on p. 4; this note does not say
  which is right.

## What it means for the plugin
- A model's forecast is taken several times, independently, and combined. `playbooks/forecasts.md` asks for at
  least three runs and logs each one. The plain mean used there is this plugin's choice: the paper used a
  trimmed mean of six, and how it trims is in an appendix that was not read.
- The owner's probability is logged beside the model's, and the forecast of record combines them. The paper
  combined a model with a crowd of many forecasters, not with one person, and weighted the crowd four times: that
  one person plus a model does better than either alone is not shown here.
- A model's forecasts are scored only on questions that resolve after they are made. Scoring a model on questions
  from before its training cut-off tests its memory.
- Near-certain questions are where the system lost most. The challenge step asks whether a forecast near 0 or 1
  was pulled toward the middle.

## Quotes
- "our averaged Brier score is .179, while the crowd achieves .149" (p. 9)
- "This gives us 6 forecasts in total: 3 from the base model, and 3 from the fine-tuned model." (p. 7)
- "4x weight for the crowd, which we find optimal on the validation set" (p. 12)
- "likely because it rarely outputs low probabilities" (p. 10)
