# What is an emerging technology? (Rotolo, Hicks & Martin, 2015)

- **Source:** Research Policy 44(10): 1827–1843 · https://doi.org/10.1016/j.respol.2015.06.006 (the accepted
  manuscript, arXiv:1503.00673v4, dated 5 January 2016; pages = PDF pages of that copy, 44 in all)
- **File:** `../papers/rotolo-2015-what-is-emerging-technology.pdf` (local only)
- **Licence:** the copy states "Distributed under CC-BY-NC-ND" (p. 1): kept local only. The publisher's page
  refused the request, so the licence of the published version was not read.
- **Evidence:** analytical · a definition built from 12 studies that define emerging technologies, and a review
  of scientometric methods found by a search in Scopus (p. 13, 15).
- **Read:** part of the text, on 2026-11-22: the abstract (p. 1), the definition and its five attributes
  (p. 10–15, and the same definition on p. 4 and p. 34), "Relatively fast growth" (p. 23–25) and the discussion
  (p. 30–33). A fetch agent read sections 1 to 4 of the HTML edition on 2026-11-21. Not read here: the
  introduction and the concept of emergence (p. 2–9), the table of methods and "Radical novelty" (p. 16–22),
  "Coherence", "Prominent impact" and "Uncertainty and ambiguity" (p. 26–29), the conclusions beyond the
  definition (p. 34–36).

## What it says
- The definition: an emerging technology is "a radically novel and relatively fast growing technology
  characterised by a certain degree of coherence persisting over time and with the potential to exert a
  considerable impact on the socio-economic domain(s)" (p. 13). Its most prominent impact lies in the future, so
  in the emergence phase it is still uncertain and ambiguous (p. 13).
- Five attributes: radical novelty, relatively fast growth, coherence, prominent impact, uncertainty and
  ambiguity (p. 13).
- Growth is relative: a technology grows fast "in comparison with other technologies in the same domain(s)"
  (p. 10). To pin the attributes "down to some absolute level is rather meaningless" (p. 14).
- Coherence means the thing holds together and has detached from its parents for some time; it is a process, not
  a final state (p. 10–11).
- Prominent impact may be narrow: a technology that reshapes one domain counts (p. 11).
- The attributes move in opposite directions over time. Before emergence: high novelty, low impact, low
  coherence, slow growth, high uncertainty; "the technology may not even emerge" (p. 14). In emergence the levels
  change sharply; afterwards growth and impact level off or decline and novelty is lost (p. 14). The authors call
  these curves "stylised" (p. 14, 15).
- On growth in current data: "The assessment of this attribute is particularly problematic for contemporary
  analyses" (p. 23).
- Yearly counts always move, so "the problem becomes one of setting a criterion by which to distinguish the
  signal from the noise" (p. 23).
- The criteria it reviews differ from study to study: a positive slope with no decline of 10% or more in the
  last period (Bengisu 2003); a fitted logistic curve; a burst of activity; the top 5% by an increment rate
  (Ohniwa et al. 2010); a growing number of authors (p. 24–25). The review reports them; it does not test one
  against another.
- Scientometric techniques are "intrinsically more effective for retrospective analyses than contemporary
  examinations" (p. 30). Lags in database indexing add to this (p. 30).
- A detected emergence "may be merely an artefact of the method used": models, data, thresholds and time windows
  differ, and their choice may bias what is found (p. 30). Results may vary with the number and length of the
  time windows (p. 31).
- Studies often analyse emerging technologies with no comparison sample of technologies that could have emerged
  and did not (p. 32).
- Publications and patents give a limited view; the paper points to funding data and attention data as possible
  early indications of growth, and says these are not yet understood (p. 23, 32–33).

## What it means for the plugin
- `playbooks/trends.md` treats fast growth as one attribute of five. A count that grows fast says nothing by
  itself about novelty, coherence, impact or uncertainty, so a series that passes the growth check is called
  "growing faster than its own past", never "emerging".
- Growth is judged against something: the series' own earlier years, and other series in the same field. No
  absolute threshold is taken from this paper, because it gives none and says a fixed level would be meaningless.
- The last years of a series are the least reliable ones. The report says so, with the indexing lag as one reason.
- Every indicator names its windows and thresholds, and the result is shown under a second choice of them, since
  the paper warns that the choice can create the finding.
- The base-rate step asks for the cases that jumped and did not continue. The paper names their absence as a gap
  in the literature; it does not supply such a sample.
- The paper is about technologies. Applying its attributes to research topics counted in a publication database
  is this plugin's reading.

## Quotes
- "we define an emerging technology as a radically novel and relatively fast growing technology characterised by a certain degree of coherence persisting over time" (p. 13)
- "The assessment of this attribute is particularly problematic for contemporary analyses." (p. 23)
- "the problem becomes one of setting a criterion by which to distinguish the signal from the noise" (p. 23)
- "The risk that detected technological emergence may be merely an artefact of the method used adds to these limitations." (p. 30)
