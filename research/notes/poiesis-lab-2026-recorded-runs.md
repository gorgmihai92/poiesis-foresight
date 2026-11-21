# A recorded run of the Poiesis plugins: the trend scan of 2026-11-17 (observation)

- **Source:** the Poiesis Lab notebook, a private repository: `fixtures/trend-scan/`, `fixtures/scripts/`,
  `fixtures/challenge-verdicts.json` and `fixtures/README.md`. The files are not in this repository.
- **File:** none here.
- **Licence:** the owner's own data, counted from OpenAlex.
- **Evidence:** observation (O) · one run of the plugins on five subject areas on 2026-11-17, kept as files.
- **Read:** observation, on 2026-11-22: `fixtures/README.md`, `challenge-verdicts.json`,
  `trend-scan/challenge.corrected.json`, `scripts/analyze.py` and `scripts/fetch_typed.py` in full;
  `scripts/fetch.py` and `scripts/build_data.py` in part; `trend-scan/openalex.json` and `analysis.json` by script.
  Every number below was computed again from `openalex.json` on that day by this repository's `trends.py` and
  its tests. The agents' own reports of the run were not saved as files, so they were not read.

## What it shows

### The database moved, and one measure moved with it
- From 2024 to 2025 the count of all OpenAlex works rose 29.3%, the count of articles, reviews and preprints rose
  17.9%, and the count of all other records rose 46.8%.
- For solid-state batteries, the share among all record types fell 3.6% in 2025, which is 2.5 standard deviations
  below that series' own earlier growth. The share among articles, reviews and preprints rose 6.7%, within its
  own earlier growth (z −1.3). The first pass read the first measure and concluded that the field "fell in
  2025"; the challenger's verdict was "weakened", with "a 2025 decline is not supported".
- Raw counts told a third story: in 2025 the raw count of three of the five areas was more than 2.8 standard
  deviations above its own earlier growth. On the share, one area was more than 2 above.

### What the run computed, and what `trends.py` reproduces
- `analyze.py` left 2026 out as an unfinished year, took the growth of 2013 to 2022 as each series' own past,
  and reported for 2023 to 2025 the growth and its distance from that past in standard deviations, plus the
  yearly rate over 2015–2020 and 2020–2025.
- Fed the same counts, `trends.py` gives the same 280 numbers for the five areas: 80 shares and, for each of
  four measures per area, the mean and standard deviation of the past, three growth figures, three z values and
  two rates. The largest difference is zero.

### What survived the challenge
- Of the six conclusions of this run, none was kept as written: all six were weakened. Across this run and a
  second one, 16 conclusions were sent to the challenger: 1 kept, 12 weakened, 2 dropped, 1 split.
- The one area whose growth stood out, synthetic biology in 2025 (+41.8% in share, 4.7 standard deviations above
  its own past), was restated by the challenger as an acceleration in one year, and by the session as "a lead to
  watch".
- Quantum computing looked ordinary on this measure partly because its own past includes its take-off, which
  widens the range it is compared with. That was the challenger's point, recorded in `challenge.corrected.json`.
- A verdict drifted when it was retyped by hand: the published file said "kept" where the challenger had said
  "weakened" (`fixtures/README.md`).

## What it means for the plugin
- The measure that is read is the share on the same document types above and below the line. `trends.py`
  refuses a share with different types on its two sides, and prints the raw count and the share among all record
  types as checks that are not read.
- The unfinished year is left out, and the report says which year that was.
- One year above a series' own past is written as exactly that. It becomes a forecast in the log or a signpost,
  not a statement about the future.
- The report says which years make up the "own past", and the playbook asks for a second choice of them.
- A verdict is copied, never retyped.
- One run, by one person, on five areas chosen in advance. It shows what went wrong once. It does not show how
  often it would.
