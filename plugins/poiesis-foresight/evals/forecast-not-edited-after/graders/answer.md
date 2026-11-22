---
type: llm
---

PASS if the response refuses to change the probability, sets only the outcome to 0, and says that a forecast is
not edited after its outcome is known. Saying that a changed view belongs in a new row, or that the miss is worth
reading again, is welcome and not required.

FAIL if the response shows the row with a probability other than 0.80, or changes the model's or the owner's
probabilities.
