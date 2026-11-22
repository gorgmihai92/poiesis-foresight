# ForecastBench: a dynamic benchmark of AI forecasting capabilities (Karger, Bastani, Yueh-Han, Jacobs, Halawi, Zhang & Tetlock, 2025)

- **Source:** ICLR 2025 · arXiv:2409.19839v5, 28 February 2025 · https://arxiv.org/abs/2409.19839 (pages = PDF
  pages, 37 in all)
- **File:** `../papers/karger-2025-forecastbench.pdf` (local only)
- **Licence:** not checked: kept local only.
- **Evidence:** empirical · language models, 500 members of the public and 39 expert forecasters on a random
  200 of 1,000 questions about events that had not happened yet; group sizes as a fetch agent read them in
  sections 4.1 and 4.2 (p. 1, 8–9).
- **Read:** part of the text, on 2026-11-22: the abstract (p. 1), the passage on leakage (p. 3), how the two human groups were scored (p. 7), the results paragraph and
  Table 2 (p. 8–9). A fetch agent read the HTML edition through section 8 on 2026-11-21. Not read
  here: how questions are generated and resolved (p. 4–7), the discussion, the appendices (p. 14–37).

## What it says
- The benchmark asks only "questions about future events that have no known answer at the time of submission",
  so that an answer cannot be in a model's training data (p. 1, 3).
- On the 200 questions also given to people, the median forecast of the expert forecasters scored a Brier of
  0.096, the median of the general public 0.121, and the best language model 0.122; the experts were ahead of
  both with p < 0.001 (p. 8, Table 2 on p. 9).
- Each human group is scored by its median forecast, not by a typical member (p. 7).
- The best models on that table had been given the crowd's forecast for the market questions; the best model
  without it scored 0.136 (p. 8).
- The abstract's own summary: "expert forecasters outperform the top-performing LLM (p-value < 0.001)" (p. 1).

## What it means for the plugin
- A model's probability is not treated as an expert's. It is logged as the model's, beside the owner's, and both
  are scored. In this study the best model matched the public's median forecast, with the crowd's forecast in
  hand for the market questions (0.136 without it), and was behind the experts' median forecast.
- The scores are medians of groups against single models of 2024, on that benchmark's questions. They say
  nothing certain about a current model, and nothing about one person's accuracy.
- Scoring happens only on questions asked before the outcome was known. A log of dated forecasts is that kind of
  test by construction, as long as a row is never edited after its outcome is known.

## Quotes
- "ForecastBench is comprised solely of questions about future events that have no known answer at the time of submission" (p. 1)
- "expert forecasters outperform the top-performing LLM (p-value < 0.001)" (p. 1)
- "The final resolution of each question is only determined in the future and cannot be leaked in any training data (by construction)." (p. 3)
