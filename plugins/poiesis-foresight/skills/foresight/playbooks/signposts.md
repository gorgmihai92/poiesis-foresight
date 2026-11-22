# Signposts: what to watch, and what to do when it moves

A signpost ties something that can be read again to a level that calls for a response, to the scenarios it tells
apart, and to the response prepared in advance.

## Read first
Notes in `research/notes` of the plugin's repository. Each says how much of its source was read.
- `walker-2019-dynamic-adaptive-planning`: read in part (sections 3.1, 3.2 and 3.5 of the chapter). The
  definitions of signpost and trigger, and the four kinds of response.
- `haasnoot-2019-adaptive-policy-pathways`: read in part (sections 4.2, 4.4 and 4.7). A signal has to come early
  enough to act on, and reliably; by the authors' account the study of signals is at an early stage.
- `haasnoot-2013-adaptive-policy-pathways`: abstract only. The origin the lab plan named; no rule rests on it.

Both chapters describe a planning method for public works over decades. In the sections read, neither reports a test of
whether signposts and triggers lead to better decisions, and one names their cost.

## Steps
1. **Start from what the decision rests on.** List the assumptions whose failure would undo it: each scenario's
   "Holds only if", each "needs modification" of a stress test, each critical uncertainty. An assumption is worth
   watching when plausible events could make it fail within the time that matters (Walker et al. 2019, 3.1).
2. **Find something that can be read again:** a series (poiesis-research's `counts.py` makes it), a count of
   signals, a page that is published on a schedule, an event that either happens or does not. Say where it is
   read. Say whether it is the outcome itself or a driver upstream of it: an indicator tied to the outcome may
   not give a timely signal, and a driver can serve instead (Haasnoot et al. 2019, 4.2).
3. **Set the trigger before reading the value:** the level or the event at which the response is due. A number
   when there is one (`>= 25`), so the script can compare.
4. **Say which scenarios it tells apart.** A signpost that would read the same in every scenario tells nothing:
   remove it.
5. **Prepare the response now** (Walker et al. 2019, 3.2, Step V). It is one of:
   - **defensive:** protect what is being done, leaving it unchanged;
   - **corrective:** adjust it;
   - **capitalizing:** take up an opportunity;
   - **reassessment:** the assumptions no longer hold; decide again;
   - or **look closer:** more research, which the second chapter counts as a valid answer to a signal (4.2).
6. **Give the lead time:** how long the response takes to prepare and to work. If the trigger would be reached
   later than that, move it earlier, watch a driver upstream, or write "too late to act on" at the start of its `response`
   cell (Haasnoot et al. 2019, 4.2).
7. **Log it** in `foresight/signposts.md` (`templates/signposts.md`): the id (`python3 -I $S/ids.py SP
   foresight`), status `watching`, and the date of the next check.

## Rules
- **A signpost without a response is a curiosity.** Drop it, or keep it with "watch only" in its `response` cell
  and say why.
- **As few as the decision needs.** Watching costs time for as long as it lasts, and setting it up is work
  (Walker et al. 2019, 3.5). No source read here gives a number.
- **The trigger is not moved to fit the value.** A changed trigger is a new row that names the old one.
- **Two ways to be wrong are recorded:** a signal that should have fired and did not, and one that fired for
  nothing (Haasnoot et al. 2019, 4.2: "no missed signal or false alarm"). `playbooks/review.md` records them.
- **Status** is `watching`, `reached` or `retired`. It is changed by hand in a review, never by a script.
- **Nothing here promises a signpost fires in time.** The second chapter calls the study of monitoring signals
  "very much at a nascent stage" (4.7).

## Then
`python3 -I $S/signposts.py foresight/signposts.md` lists what is due and what is out of order.
`playbooks/review.md` reads each signpost on its date.

## Save (see SKILL.md, "Saving")
The row in `foresight/signposts.md`; the reasoning in `foresight/<YYYY-MM-DD>-<topic>.md`, under "Signposts added
to the log". A signpost is always saved: it has a date to come back to.
