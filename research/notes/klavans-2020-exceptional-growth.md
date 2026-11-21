# A novel approach to predicting exceptional growth in research (Klavans, Boyack & Murdick, 2020)

- **Source:** PLOS ONE 15(9): e0239177 · https://doi.org/10.1371/journal.pone.0239177 (pages = PDF pages, 24)
- **File:** `../papers/klavans-2020-predicting-exceptional-growth.pdf` (local)
- **Licence:** open access under the Creative Commons Attribution License, as a fetch agent read on the article
  page on 2026-11-21. The licence line was not read in the PDF: the file is kept local.
- **Evidence:** empirical · forecasts of growth for about 100,000 clusters of papers ("research communities") in
  Scopus, tested across forecast years 2006 to 2015 in two models (p. 1–2).
- **Read:** part of the text, on 2026-11-22: the abstract and introduction (p. 1–3), the definitions of share,
  growth and exceptional growth (p. 6–8), the first accuracy test (p. 14) and the weaknesses the authors state
  (p. 21–22). A fetch agent read the HTML edition through "Flaws and future directions" on 2026-11-21. Not read
  here: the background on clustering (p. 4–5), the indicators and the probit model (p. 9–13), tests 2 to 4
  (p. 15–20), the references.

## What it says
- Growth is measured on publication share, "rather than raw counts to account for annual fluctuations in the
  overall models due to database growth" (p. 6).
- Growth is measured from the community's peak year, not from the forecast year. Measured from a dip, the same
  series looked like 14.8% a year where it was 6.3% from the peak; a community first "has to make up for the dip"
  (p. 7).
- "Exceptional growth" is a yes or no: annual growth in share above 8% from the peak year to the target year,
  three years after the forecast (p. 6–8). The authors say the 8% "may seem arbitrary"; they take it from a
  business convention and from users' feedback (p. 8).
- A base rate: among communities with at least 20 papers in the forecast year, the share that reached exceptional
  growth was "relatively constant across models and years" at "about 1.5%" (p. 8).
- Small series mislead: a community with five papers "only needs to have seven papers" three years later to
  count as exceptional (p. 8). The analysis keeps communities of at least 20 papers (p. 8).
- Accuracy is scored with the Critical Success Index, hits over hits plus false alarms plus misses, against a
  threshold of 25% taken from three-day storm forecasts (p. 2–3). With all communities included, "neither model
  reaches the 25% CSI threshold in any year"; with the small ones left out, one model is above it in all years
  and the other in most (p. 14).
- The composite score ranks communities; it "does not predict growth rate" (p. 14).
- The window: bibliometric models "are not designed for very short-term forecasts (less than two years out)
  because of the inherent time delay of publications", and the authors expect them to be weaker beyond five years
  (p. 21).
- Limits the authors state: biases and gaps in the database carry into the forecast (p. 21); "Predictability in
  the past does not guarantee predictability in the future" (p. 21); forecasts made for years before the model
  was built used future information and "may not be actionable" (p. 8, 22); no indicator tells when a community
  is turning to maturity or decline (p. 21).

## What it means for the plugin
- `trends.py` reads shares, and it reports growth from the series' earlier peak as well as from last year, so
  a recovery after a dip is not read as a rise.
- A series below a minimum size is flagged before its growth is read. The plugin's default of 20 works a year
  is this paper's cut-off for clusters of papers, borrowed for searches; that it fits a search series is not shown.
- The 1.5% is the one published base rate this plugin holds for "exceptional growth is rare". It belongs to
  Scopus clusters, a three-year window and an 8% threshold. It is quoted with those three conditions, as a
  point of comparison, and never as the base rate of a project's own series.
- A reading of the next three years from publication counts is, by this paper's own test, right about a third of
  the time at best when the small series are excluded. `playbooks/trends.md` says a trend in counts is a lead
  for a forecast in the log, not a statement about the future.
- The study predicts clusters built from citations in Scopus. The plugin counts searches and topics in OpenAlex.
  The indicators there (among them one built on the peak year) were not used here.

## Quotes
- "Growth is based on publication share rather than raw counts to account for annual fluctuations in the overall models due to database growth" (p. 6)
- "Note that growth is measured from the peak year rather than the forecast year." (p. 7)
- "is relatively constant across models and years (dashed lines in Fig 2) at about 1.5%" (p. 8)
- "When all RCs are included, neither model reaches the 25% CSI threshold in any year." (p. 14)
- "Predictability in the past does not guarantee predictability in the future." (p. 21)
