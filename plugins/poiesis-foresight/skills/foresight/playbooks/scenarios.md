# Scenarios

Two to four scenarios built on the most uncertain, most important drivers. Report what holds across all scenarios
(robust) and what depends on one (contingent); scenarios guide flexible choices, they are not forecasts.

## Read first
Notes in `research/notes` of the plugin's repository. Each says how much of its source was read.
- `go-science-2024-futures-toolkit`: its Scenarios section, read in full (p. 61–69), with the other ways to build
  scenarios (p. 108–111) and the glossary. Practitioner guidance. The steps below adapt its five steps (Open Government
  Licence v3.0).
- `phadnis-2015-scenario-planning`: read in part (p. 1–4). Three field studies with experts and no control group.
- `borjeson-2006-scenario-types`: abstract only. The three questions a user of scenarios may have.
- `mancini-2010-contravision`: abstract only. Two comparable versions of one future drew a wider range of
  reactions from people than one version.
- `spaniol-2023-ai-assisted-scenarios`: abstract only. A practitioners' reflection: scenarios written by a model
  are base material.
- `meissner-2013-scenario-planning-biases`: title only. Nothing is taken from it.

## Which question?
Ask first what the user needs to know (Börjeson et al. 2006, from the abstract):
- **what will happen:** that is a forecast. Use `playbooks/forecasts.md`;
- **what can happen:** this playbook;
- **how a given target can be reached:** working back from a target has no playbook in this version. Say so and
  offer the choices: scenarios of what can happen, read for the routes to the target, or leaving it out.

## Steps (toolkit, p. 64–69)
1. **Start from the critical uncertainties** of `playbooks/drivers.md`: drivers that are important and uncertain.
   The toolkit asks for at least ten to choose from (p. 64). With fewer, say how many there were.
2. **Make each an axis:** a line between two opposite outcomes of that driver. The ends are extremes, not a good
   end and a bad end (p. 64).
3. **Choose two axes that are independent of each other** (p. 65). If one moves the other, they are one axis. Two
   axes give four worlds. Use two or three scenarios when the fourth corner is not credible, and say which corner
   was left out and why.
4. **Describe each world** from `templates/scenario.md`: what is ordinary there, who does what, what has gone.
   Use the signals and series the project holds. A detail with no source is marked as imagined.
5. **Name each** so that the name says what it is and takes no side (p. 67).
6. **Write each one twice:** to its advantage, by someone it suits, and to its cost, by someone it harms. Most
   futures mix both (toolkit, p. 4, 8).
7. **Check each for consistency:** nothing in it that could not happen within its own logic (toolkit, p. 114).
8. **Read across them.** What holds in every scenario is robust. What holds in one is contingent. Report the two
   apart.
9. **Give each an id** (`python3 -I $S/ids.py SC foresight`) and a **From** line: the ids of the signals,
   insights, drivers and sources it rests on.

Other ways to build a set, when two axes do not fit: four standard archetypes (continued growth, decline and
collapse, disciplined society, transformation), and combining the outcomes of several uncertainties while ruling
out the pairs that could not occur together (toolkit, p. 109–110, which credits Dator 2009 and Ritchey 2009;
neither was read).

## Rules
- **A scenario has no probability.** "Scenarios are not plans or predictions of the future" (toolkit, p. 62). A
  claim inside one that can be checked becomes a forecast in the log.
- **Every option is read against every scenario.** In the one field study read here, experts' judgment of an
  investment moved with how it fared in the scenario they had used (Phadnis et al. 2015, p. 1).
- **Prefer what holds across scenarios and what keeps choices open.** In the same study experts preferred more
  flexible options after using several scenarios (p. 1). That is what they did, not proof that they decided better.
- **A scenario a model wrote is a draft.** The owner chooses, edits and names. Each one says which drivers it is
  built on and where they came from.
- **Not before five years out** unless the scoping question says so (toolkit, p. 63).
- **Each condition added makes a scenario less likely, never more** (`playbooks/challenge.md`).

## What this cannot claim
The toolkit writes these steps for a workshop of eight to twelve people over four to five hours (p. 62–63). Here
one person works with a model, and the comparison between groups is replaced by drafts made separately and then
compared. That replacement is this plugin's choice and has not been tested. Before the field study above,
evidence of what scenarios do to judgment was "almost nonexistent" by its authors' account (p. 2).

## Then
Scenario logic goes through `playbooks/challenge.md`. Then `playbooks/stress-test.md` and `playbooks/signposts.md`.

## Save (see SKILL.md, "Saving")
In `foresight/<YYYY-MM-DD>-<topic>.md`, under "Scenarios": one entry each, then what holds in all and what
depends on one.
