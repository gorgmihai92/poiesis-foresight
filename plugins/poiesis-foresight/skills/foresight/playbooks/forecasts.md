# Forecasts

Where a claim can be checked later, write it as a forecast: a precise question, a probability, a date to resolve
it. Add it to `foresight/forecasts.md` (`templates/forecasts.md`). When dates pass, score them:
`python3 -I $S/forecasts.py foresight/forecasts.md`. Scores show which reasoning to trust next time.

## Read first
Notes in `research/notes` of the plugin's repository. Each says how much of its source was read.
- `chang-2016-forecasting-training`: read in part (p. 1, 4–7). An hour of training improved forecasters' scores by
  6 to 11%; the principle tied to accuracy was using comparison classes. It trained and measured people.
- `halawi-2024-llm-forecasting`: read in part (p. 1–2, 4, 6–7, 9–13). A model system scored .179 against a
  crowd's .149, and .146 when the two were combined with four times the weight on the crowd; it combined six of
  its own forecasts. It is a test on past questions with date-limited search, the kind Paleka et al. question.
- `schoenegger-2024-silicon-crowd`: read in part, as a preprint (p. 1, 5, 7, 9–11, 14–15). A plain average of a
  model and a human median beat the model's own update; models leaned toward "yes".
- `karger-2025-forecastbench`: read in part (p. 1, 3, 8–9). Expert forecasters were ahead of the best model.
- `paleka-2025-evaluating-llm-forecasters`: read in part (p. 1–3, 9–10). Why a test on the past is hard
  to trust.
- `mellers-2015-superforecasters`: abstract only. The reference poiesis-insight gave for scored forecasts.

## Write the question
- **Precise and checkable:** one outcome, yes or no, that a stranger could settle from a named source by a date.
  "Will X publish Y by 2027-06-30, as shown on Z?" Not "Will X grow?".
- **Write it the other way round too** where that makes sense ("Will X not … by …?"). Separate model runs get the
  two wordings (step 3), and the gap between them is the check. In one study models leaned toward "yes"
  (Schoenegger et al. 2024, p. 1, 9). The check is this plugin's use of that finding.
- **Mix the dates.** Include questions that resolve within months: a log with no resolved rows teaches nothing.

## Give the probability
1. **The comparison class first** (`playbooks/base-rates.md`). Write the class and its rate, or "not available".
   Of the principles forecasters were trained in, this was the one whose use went with better scores in their
   own explanations (Chang et al. 2016, p. 6); the paper says the others "did not prove useful here" (p. 12).
2. **The owner's probability.** Ask the user for theirs before showing the model's, so the two are independent.
   No answer is an answer: leave `owner` empty and say the forecast of record is the model's alone.
3. **The model's, several times, independently.** Each run is the `forecaster` agent with the question, the
   source that will settle it, the date, the base rate and the evidence files. It does not see the other runs,
   the owner's number or this session's reasoning.
   - quick depth: one probability, inline, logged as one run;
   - standard: three runs, in parallel;
   - thorough: five.
   Each run is a model call. Say how many will be made before making them.
   - **The two wordings go to separate runs.** Of the runs, about half get the question as written and the rest
     its negation: two and one at standard, three and two at thorough. A run never sees the other wording. It
     answers the wording it was given; a negated run's answer p' is written as 1 − p' before anything is
     combined, so every number in `model` is the probability that the question as written happens.
   - **The gap is the check:** `python3 -I $S/forecasts.py foresight/forecasts.md --sources` prints, once the row
     is logged, the mean of the written runs minus the mean of the negated ones. Paste it into the reasoning. A
     positive gap is what a lean toward "yes" would give; with two runs and one it is also run-to-run noise. It is
     reported, not corrected for: the forecast of record is not adjusted by it (a choice).
   - At quick depth, or when the question has no sensible negation, every run gets the wording as written, and the
     report says under "Not checked" that the other way round was not asked.
4. **The forecast of record** is the mean of the owner's probability and the mean of the model's runs. Where one
   is missing it is the other.
5. **Log it:** the id (`python3 -I $S/ids.py F foresight`), the question, the probability, today's date, the
   resolve date, an empty outcome, the note that holds the reasoning, the model's runs, the owner's probability,
   and the wording of each run (`written` or `negated`, in the order of the runs).

## Rules
- **Written before the outcome, never edited after.** Only `outcome` is filled in later. A changed view is a new
  row that names the old one. No script can see a probability that was edited after the fact: it is a rule for whoever keeps the log, and the
  file's history is where a change shows.
- **Several runs, combined.** One study combined six forecasts by a trimmed mean (Halawi et al. 2024, p. 7),
  another twelve models by the median (Schoenegger et al. 2024, p. 7). Both combined different models or prompts. Repeating one agent with one brief, and the plain mean,
  are this plugin's choices and are not tested in them. The script also prints the score of the median.
- **Average the model with the owner; do not ask the model to adjust to the owner.** In one study the plain
  average was more accurate than the model's own update toward the human forecast (Schoenegger et al. 2024,
  p. 15). The comparison was exploratory, and it averaged a model with a crowd's median, not with one person: equal
  weight for one owner is a choice.
- **The model's probability is the model's.** In one benchmark the best model scored about as well as
  the public's median forecast (0.122 against 0.121, with the crowd's forecast in hand for some questions) and
  behind the expert forecasters' median forecast, 0.096 (Karger et al. 2025, p. 7–9).
- **Near 0 or 1, look again.** One system did worse than the crowd where the crowd was highly certain, "likely
  because it rarely outputs low probabilities" (Halawi et al. 2024, p. 10). The challenge asks whether a
  near-certain forecast was pulled toward the middle.
- **Never test the model on the past.** A question whose outcome is already known tests memory: training cut-offs
  are "more of a guideline than a guarantee", and search limited to a past date leaks (Paleka et al. 2025, p. 2).
  The paper shows how such tests leak, not how often; never
  running one is this plugin's choice. Only code that computes from counts may be tried on past years, and it
  still reads today's database.
- **A scenario gets no forecast of its own.** Its "would be wrong if" can.

## Score
- `python3 -I $S/forecasts.py foresight/forecasts.md --sources` gives the score of record and, on the rows that
  have both, the model's, the owner's and their mean. 0 is perfect; always saying 50% earns 0.25.
- **A score is a record to read the reasoning against.** The sentence this playbook opens with came from
  poiesis-insight; it holds only once many rows have resolved.
- **Few resolved rows say little.** The script prints how many it scored. With fewer than 20, report the scores
  and do not rank the sources: the number 20 is a choice.
- Scores from Chang et al. 2016 are on a scale from 0 to 2 (p. 4). Do not set them beside these.
- Calibration and the logarithmic score, which Paleka et al. 2025 also ask for (p. 9), are not computed in this
  version. Say so under "Not checked".
- **Read the misses again** in `playbooks/review.md`.

## Then
Every forecast goes through `playbooks/challenge.md` before it is logged.

## Save (see SKILL.md, "Saving")
The row in `foresight/forecasts.md`; the reasoning in `foresight/<YYYY-MM-DD>-<topic>.md`, under "Forecasts added
to the log". A forecast is always saved: it has a date to come back to.
