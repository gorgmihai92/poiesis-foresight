# Wisdom of the silicon crowd: LLM ensemble prediction capabilities rival human crowd accuracy (Schoenegger, Tuminauskaite, Park & Tetlock, 2024)

- **Source:** Science Advances 10(45): eadp1528 · https://doi.org/10.1126/sciadv.adp1528 (read as the preprint,
  arXiv:2402.19379v6, 22 July 2024; pages = PDF pages of the preprint, 20 in all)
- **File:** `../papers/schoenegger-2024-wisdom-silicon-crowd.pdf` (local only)
- **Licence:** not checked: kept local only. The publisher's page refused the request, so the published version
  was not read and may differ in wording.
- **Evidence:** empirical · study 1: twelve language models, three runs each, on 31 binary questions, against
  the median of 925 human forecasters in a three-month tournament; study 2: two models shown the human median
  (p. 1, 5, 7).
- **Read:** part of the text, on 2026-11-22: the abstract (p. 1), the passages on how forecasts were collected
  and aggregated (p. 5, 7), the bias toward positive answers (p. 9), the main comparisons (p. 10–11) and the
  comparison with a simple average (p. 14–15). A fetch agent read the whole HTML edition of the preprint on
  2026-11-21. Not read here: the introduction (p. 2–4), the calibration results, the discussion and limitations
  (p. 15–17).

## What it says
- The models' forecasts were combined by the median of all runs on each question (p. 7). Each model was asked
  three times per question (p. 5).
- The median of the twelve models scored a mean Brier of 0.20 over 31 questions; always saying 50% scores 0.25;
  the human crowd scored 0.19. The difference between models and humans was not statistically significant
  (p. 10–11).
- The authors say the result "only enables us to directly conclude that the LLM crowd is neither more nor less
  accurate than the human crowd in the question set studied here" (p. 11).
- Model forecasts leaned toward "yes": mean predictions were "significantly above 50%, despite an almost even
  split of positive and negative resolutions" (p. 1). The authors call it a machine equivalent of acquiescence
  bias (p. 9).
- Shown the human median, both models moved toward it and improved, but their updated forecasts were
  "significantly less accurate than a simple average between the machine and the human median forecasts" (p. 15).

## What it means for the plugin
- Several independent model forecasts are combined into one, and each run is kept in the log. This paper used
  the median, Halawi et al. 2024 a trimmed mean, and neither compared the two on the same questions with the
  same models. `forecasts.py` prints the mean and the median of the runs; the forecast of record uses the mean,
  which is this plugin's choice.
- The owner's probability and the model's are averaged; the model is not asked to "take the owner's view into
  account" and then trusted. In this study the plain average beat the model's own update.
- Every question is also asked the other way round where it can be ("Will X not happen by…?"), since the models
  here leaned toward yes. That check is this plugin's use of the finding; the paper did not test it as a remedy.
- Thirty-one questions and models of 2023. It supports the practice of combining; it does not say how good any
  current model is.

## Quotes
- "For the LLM ensemble approach, we computed the median from all non-missing forecasts on each question." (p. 7)
- "For each question, we prompted each model three times and recorded all predictions." (p. 5)
- "their updated forecasts are significantly less accurate than a simple average between the machine and the human median forecasts" (p. 15)
