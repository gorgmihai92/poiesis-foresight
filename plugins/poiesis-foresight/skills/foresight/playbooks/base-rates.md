# Base rates

Before a jump is read or a forecast is written: of the things that looked like this one, how many went on?

## Read first
Notes in `research/notes` of the plugin's repository. Each says how much of its source was read.
- `flyvbjerg-2006-reference-class-forecasting`: read in part (p. 2–14, 16–17). The three steps below are its
  method. It is about the cost and demand of building projects; using it for research topics is this plugin's
  analogy.
- `kahneman-1993-outside-view`: abstract only. The inside view anchors on the case; the outside view looks at
  the record of similar cases.
- `klavans-2020-exceptional-growth`: read in part. One published base rate for growth in research, with its
  conditions.
- `rotolo-2015-emerging-technology`: read in part. Studies of emergence often lack the cases that could have
  emerged and did not (p. 32).

## Steps (Flyvbjerg 2006, p. 7)
1. **Name the reference class** and say why its members are comparable. It "must be broad enough to be
   statistically meaningful but narrow enough to be truly comparable". Give its size. For a series, the class is
   other series of the same kind, from the same database, counted the same way, fetched the same day: the topics
   of a taxonomy scan (`counts.py --taxonomy` in poiesis-research), or the other series in the same file.
2. **Get its distribution.** `python3 -I $S/trends.py research/data/<class>.csv --base-rate --leave-out <the
   case's id>`. It finds every earlier jump in the class and reads what the series did three years later:
   - kept growing faster than before the jump;
   - kept the gain, at its earlier pace or slower;
   - gave back part of the gain;
   - fell back to where it started or lower.
   Paste the output. With fewer than 20 jumps it lists the cases and does not call them a rate.
3. **Place the case.** Start the probability from the class's rate. Move away from it only with a reason and the
   evidence for it, and write the two apart: the base rate, then the adjustment (Flyvbjerg 2006, p. 13).

## When there is no class
- **No precedent, or too few cases:** write "base rate: not available", with what was looked for. Do not put a
  guess in its place. The outside view fails where nothing like the case has happened before (Flyvbjerg 2006,
  p. 9–10). The forecast then says its probability rests on the case alone.
- **A class the gate refuses:** without a key, a taxonomy scan holds the first 200 topics by id and is marked
  incomplete. Offer the choices: the user gets the free key and the scan is run again (their step), a narrower
  class the gate accepts, or no base rate.
- **A comparison from the literature:** the 1.5% of Klavans et al. 2020 may be quoted with its three conditions
  (Scopus clusters of at least 20 papers, three years, more than 8% a year in share). It is not the project's
  base rate.

## For a question that is not about a series
The class is a list of similar past cases that can be counted, with its source: "of the last twelve standards
announced by this body, how many shipped within two years". A class recalled from memory is marked "from general
knowledge, unverified" and is not called a base rate.

## The definitions are this plugin's
No source read here defines "a jump" or "went on" for a research topic. The script's are fixed before the
numbers are seen: a jump is growth at least 2 standard deviations above the series' own earlier growth; the
outcome is read 3 years later; a jump with fewer than 20 works is left out; a jump too recent to follow is
listed and not counted. Change one (`--jump`, `--after`, `--min-count`) and report both results.

## Report
- The class, why it is comparable, its size, and the script's output as printed.
- The rate, or "not available" and why.
- **Not checked:** other classes that could have been used.
