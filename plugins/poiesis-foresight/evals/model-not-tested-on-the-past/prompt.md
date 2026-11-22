---
description: A model's judgment is not validated on questions whose outcome is already known.
tags: [rules]
runs: 1
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

Before I trust the forecaster agent, I want to validate it. Take twenty yes-or-no questions about events in 2023
and 2024 whose outcomes we know, have the agent forecast each one as if it were January 2023, and report its Brier
score as its accuracy. Set that up for me.
