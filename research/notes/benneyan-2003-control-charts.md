# Statistical process control as a tool for research and healthcare improvement (Benneyan, Lloyd & Plsek, 2003)

- **Source:** Quality and Safety in Health Care 12(6): 458–464 · https://doi.org/10.1136/qhc.12.6.458
- **File:** none (the publisher's site refused the request with HTTP 403)
- **Licence:** free to read at the publisher, as OpenAlex records it; not open-licensed.
- **Evidence:** analytical · an overview of a method with examples from healthcare (abstract).
- **Read:** abstract only, as OpenAlex and Semantic Scholar returned it on 2026-11-22 through poiesis-research's
  `search.py`. poiesis-insight's note on this paper is marked "from general knowledge, unverified".

## What it says (from the abstract)
- Repeated measurements naturally give different values, and "even if nothing was done, a subsequent measurement
  might seem to indicate a better or worse performance".
- Statistical process control, with the control chart as its main tool, combines time-series analysis with a
  graphical presentation of the data.

## What it means for the plugin
- It supports one sentence of `playbooks/trends.md`: a change is read against the series' own usual variation,
  because a series moves even when nothing has changed.
- **Waiting:** the control-chart rules poiesis-insight's playbook names (limits at about three standard
  deviations, a run of points on one side). They are not in the abstract. `trends.py` reports how far a year's
  growth is from the series' own past in standard deviations, as the lab's recorded run did, and attaches no
  rule from this paper to that number.
