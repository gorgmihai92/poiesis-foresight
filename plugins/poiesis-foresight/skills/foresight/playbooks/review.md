# Review: a dated look back

What happened to what was written: forecasts that came due, signposts that moved, series that were counted
again, and conclusions whose footing changed.

## Read first
No new source backs this playbook: it puts the checks of the other playbooks on a date. Three notes in
`research/notes` of the plugin's repository carry its rules:
- `chang-2016-forecasting-training`: read in part. Looking back at forecasts ("post-mortem analysis") was one of
  the principles forecasters were trained in (p. 6).
- `haasnoot-2019-adaptive-policy-pathways`: read in part. A signal is judged by missed signals and false alarms
  (4.2).
- `paleka-2025-evaluating-llm-forecasters`: read in part. A forecast counts only if it was made before its outcome.

The lab plan cites Claude Code's documentation on scheduled tasks for running a review on a schedule. That
documentation was not read for this version: here a review is run when the user asks for one.

## Steps
1. **Forecasts.** `python3 -I $S/forecasts.py foresight/forecasts.md --sources`. For each row past its date, find
   the outcome in the source the row names and cite it. Fill in `outcome` and nothing else. An outcome that
   cannot be settled stays empty, with the reason in the review.
2. **Signposts.** `python3 -I $S/signposts.py foresight/signposts.md`. For each one due, read the indicator where
   the row says. Write the value, the date read and the next check. If the trigger is met, set the status to
   `reached` and say which response is now due.
3. **Series.** A series is read again only from a new file: poiesis-research's `counts.py` fetches it. Run the
   gate and `trends.py` on the new file, and set its reading beside the earlier one with both dates. Two files
   are two series: do not join them.
4. **What became stale.** For each scenario, forecast and signpost, read its **From** line. If something named
   there was dropped, weakened or challenged again since, say so. Nothing is rewritten: it is listed.
5. **The misses.** Read the worst-scored forecasts again. One line each on what the reasoning had and lacked. If
   the misses share something, say what.
6. **Signals that failed.** A signpost that should have fired and did not, or fired for nothing, is recorded as
   a missed signal or a false alarm.
7. **Write the review** from `templates/review.md`, with the two scripts' output pasted as printed.

## Rules
- **A review changes four things:** a forecast's `outcome`; a signpost's `status`, `last value`, `last checked`
  and `next check`. Probabilities, triggers, questions and verdicts stay as written.
- **This plugin fetches nothing.** Counting a series again is poiesis-research's work. If it is not installed,
  say so once, read what the user provides, and record the rest under "Not checked".
- **A challenge verdict is not revised here.** A conclusion that needs testing again goes back through
  `playbooks/challenge.md` and gets a new, dated verdict next to the old one.
- **Few resolved forecasts say little.** Report the scores with how many rows they rest on.

## Save
`foresight/reviews/<YYYY-MM-DD>.md`. A review is always saved: it is the record that the look back happened.
