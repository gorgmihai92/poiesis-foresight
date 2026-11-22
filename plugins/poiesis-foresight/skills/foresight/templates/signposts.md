# Signpost log

One line per signpost: what is watched, the level or event that calls for a response, the scenarios it points to,
and the response prepared in advance. Read with: `python3 -I <scripts>/signposts.py foresight/signposts.md`

- `watch`: the indicator and where it is read (a series, a source, a count), so that anyone can read it again.
  Say whether it is the outcome itself or a driver upstream of it.
- `trigger`: a comparison with a number (`>= 25`, `< 0.5`) when there is one, so the script can compare; otherwise
  a sentence a person can judge.
- `points to`: the ids of the scenarios it tells apart, such as `<SC-001>`.
- `response`: defensive, corrective, capitalizing or reassessment, or "look closer", and what will be done.
- `lead time`: how long the response takes to prepare and to work. A trigger reached later than that is too late.
- `status`: watching, reached or retired. It is changed by hand, in a review.

No cell contains a `|`. The first ten columns keep their order; a new column goes at the end.

| id | watch (what, and where it is read) | trigger | points to | response | lead time | status | next check | last value | last checked |
|---|---|---|---|---|---|---|---|---|---|
| <SP-001> | <share of … per 100,000 works, from research/data/…> | <>= 25> | <SC-001> | <corrective: …> | <6 months> | watching | <YYYY-MM-DD> | <21.7> | <YYYY-MM-DD> |
