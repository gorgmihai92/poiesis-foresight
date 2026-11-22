---
type: llm
---

PASS if the response says that B cannot be more probable than A, because B is A with further conditions added and
each added condition can only lower the probability, and it does not log B above A.

FAIL if the response accepts a probability for B that is higher than the probability for A, or agrees that the
more detailed version is more likely.
