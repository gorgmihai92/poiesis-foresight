# Dynamic Adaptive Planning (DAP) (Walker, Marchau & Kwakkel, 2019)

- **Source:** chapter 3 of Marchau, Walker, Bloemen & Popper (eds.), *Decision Making under Deep Uncertainty: From
  Theory to Practice*, Springer, p. 53–69 · https://doi.org/10.1007/978-3-030-05252-2_3 (the publisher's HTML edition; no
  page numbers, cited by section)
- **File:** none here (the chapter is open to read at the publisher)
- **Licence:** Creative Commons Attribution 4.0, as the chapter's page states. Third-party material in it may be
  excluded.
- **Evidence:** analytical · a planning method described by its authors, with an illustration they call "(more or
  less) fictitious" in the abstract. Not a test of whether the method works.
- **Read:** part of the text, on 2026-11-22, in the browser: sections 3.1 "Introduction", 3.2 "The DAP Approach"
  and 3.5 "Conclusions" in full, and the abstract. Not read: 3.3 (the Schiphol airport illustration), 3.4
  (implementation and adaptation), the figures. Of the book's other chapters, only chapter 4 was read in part
  (see `haasnoot-2019-adaptive-policy-pathways`).

## What it says
- The premise: a static plan built on one future, or on a small set of futures, may fail when the future turns
  out different (3.1).
- The method in one sentence: set goals, assemble an initial plan, find how it might fail, add actions that
  protect it now, and establish "signposts to monitor the remaining uncertain vulnerabilities" (3.1).
- It borrows from Assumption-Based Planning: an assumption is load-bearing when its failure would mean the plan
  does not meet its objectives, and vulnerable when plausible events could make it fail within the plan's
  lifetime (3.1).
- Five design steps: stage setting; assembling an initial plan; increasing its robustness; setting up the
  monitoring system; preparing the trigger responses (3.2).
- "Signposts specify the types of information and variables that should be monitored" to show whether the plan is
  achieving its goals and whether the identified vulnerabilities and opportunities are getting in its way (3.2,
  Step IV).
- "Triggers are the critical signpost levels or events that, when they occur, signify that (contingent) actions
  should be taken" (3.2, Step IV).
- Responses are prepared before implementation, so that they can be used if a trigger event occurs (3.2, Step V).
- Four kinds of response to a trigger: defensive actions, which leave the plan unchanged; corrective actions,
  which adjust it; capitalizing actions, which take advantage of an opportunity; and reassessment, when the
  assumptions critical to the plan have lost validity (3.2, Step V).
- Five kinds of action taken at the start: mitigating (against likely vulnerabilities), hedging (against
  uncertain ones), seizing (likely opportunities), exploiting (uncertain new developments), shaping (acting on
  the outside conditions themselves) (3.2, Step III).
- Costs the authors name: the plan may cost more if no response is ever needed; "setting up the monitoring system
  may be complicated, the monitoring itself may be expensive over a long period"; and decision makers may resist
  committing to actions in advance (3.5).

## What it means for the plugin
- `playbooks/signposts.md` takes its two definitions from here: a signpost is what is watched, a trigger is the
  level or event at which a prepared response is taken. A signpost row in `foresight/signposts.md` holds both,
  with the response written before the trigger is reached.
- The response column uses the chapter's four kinds: defensive, corrective, capitalizing, reassessment.
- A signpost is tied to an assumption that the plan or the scenario rests on. A signpost that watches nothing
  the decision depends on is dropped.
- The chapter is written for public plans that run for decades. Using its vocabulary for a designer's or a
  researcher's project is this plugin's choice. The chapter reports no measurement of whether signposts and
  triggers lead to better decisions, and it names their cost.

## Quotes
- "Signposts specify the types of information and variables that should be monitored" ("3.2 The DAP Approach", Step IV)
- "Triggers are the critical signpost levels or events that, when they occur, signify that (contingent) actions should be taken" ("3.2 The DAP Approach", Step IV)
- "setting up the monitoring system may be complicated, the monitoring itself may be expensive over a long period" ("3.5 Conclusions")
