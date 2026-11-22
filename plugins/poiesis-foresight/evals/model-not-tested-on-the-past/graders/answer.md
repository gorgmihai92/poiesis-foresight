---
type: llm
---

PASS if the response says that this test would not measure forecasting, because the model may already know the
outcomes of past events (its training data, or search results, can carry them), and proposes scoring the agent
only on questions that resolve after the forecast is made. It may add that indicators computed by code from
counts can be tried on past years, with the caveat that they read today's database.

FAIL if the response sets up or endorses the backtest as a valid measure of the agent's accuracy, or reports a
Brier score for it.
