# Signpost log (test fixture)

Not real signposts. Each row exercises one behaviour of `signposts.py`, read as on 2030-06-01.

| id | watch (what, and where it is read) | trigger | points to | response | lead time | status | next check | last value | last checked |
|---|---|---|---|---|---|---|---|---|---|
| SP-001 | Due, numeric trigger not met | >= 25 | SC-001 | corrective: fixture | 6 months | watching | 2030-05-01 | 21.7 | 2029-11-01 |
| SP-002 | Not due yet | >= 25 | SC-001 | corrective: fixture | 6 months | watching | 2031-01-01 | 12 | 2030-01-01 |
| SP-003 | Reached, value meets the trigger | < 0.5 | SC-002 | reassessment: fixture | 1 year | reached | 2030-01-01 | 0.4 | 2030-01-01 |
| SP-004 | Value meets the trigger and status still says watching | > 100 | SC-002 | defensive: fixture | 3 months | watching | 2031-01-01 | 140 | 2030-01-01 |
| SP-005 | Status says reached and the value does not meet it | >= 50% | SC-001 | capitalizing: fixture | 3 months | reached | 2030-01-01 | 31% | 2030-01-01 |
| SP-006 | Trigger is a sentence | a second regulator adopts the rule | SC-003 | look closer: fixture | 2 months | watching | 2030-03-15 |  |  |
| SP-007 | Retired rows are passed over | >= 3 | SC-003 | none | none | retired | 2020-01-01 | 9 | 2020-01-01 |
| SP-008 | A status that is not one of the three | >= 3 | SC-003 | fixture | none | provisional | 2030-01-01 | 1 | 2030-01-01 |
| SP-009 | A date not written as a date | >= 3 | SC-003 | fixture | none | watching | next spring | 1 | 2030-01-01 |
| SP-010 | Too few cells | >= 3 | SC-003 |
| SP-011 | Value is a word, trigger compares with a number | >= 3 | SC-003 | fixture | none | watching | 2031-01-01 | several | 2030-01-01 |
| SP-012 | Watching with no date for the next check | >= 3 | SC-003 | fixture | none | watching |  | 1 | 2030-01-01 |
