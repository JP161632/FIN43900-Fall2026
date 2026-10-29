# Lab 17 rubric audit

Audited October 29, 2026 after incorporating the student's DGS10 selection, personal answers, partner exchange, and admission decision. This records evidence and open requirements; it does not award an instructor's grade.

| Criterion (5 points each) | Evidence | Status |
|---|---|---|
| Known answer reproduced | All four October 5 date/value pairs match; PAYEMS 159,536 then versus 158,316 today, 381 revised dates; preserved source CSVs and hashes | Complete |
| The app | Four default charts; typed PAYEMS; linked table with current/as-known dates, values, late/revised counts; per-ID errors; cached real downloads; 20 passing audit checks including three live page checks | Complete |
| Data card | DGS10 source links, measure, annual percentage units, daily frequency, publication schedule/observed lag, revision evidence, and download date; September 30 versus October 29 snapshots preserved. All three student-reported hand-check values disagreed with the source; corrected values documented and student recheck requested | One unresolved manual requirement |
| Fresh eyes | Student reports no-AI line-by-line explanation and role swap; actual partner revision concern and code question preserved; two-sentence answer cites DGS10's zero revisions and PAYEMS's 381; original code answer receives an explicit CSV-parameter correction | Complete |
| The call | Student selects Admit DGS10; explicit prior-day-vintage rule excludes future releases/revisions; quarantine when decision provenance unavailable, reject feed if provenance lost; no claim of predictive success | Complete |

Four criteria have evidence supporting the 5-point anchors. The data card is complete except for a corrected student hand check; a 25/25-ready submission cannot be claimed until that discrepancy is resolved.

## Verification boundaries

- Common-answer and PAYEMS checks run on downloaded FRED/ALFRED responses; expected values are isolated in the verifier.
- Archived CSV hashes are checked on replay. Retrieval provenance is in `evidence/downloads.json`.
- Interface tests use archived responses with Streamlit's AppTest. The malformed/unknown-ID tests inject explicit failures to verify that other series survive; they are not a claim about a particular unknown ID's HTTP status.
- Three additional AppTest checks use live HTTP responses: today's four-chart page, all four October 5 answers through the date widget, and PAYEMS at January 15, 2025 through the typed-ID/date widgets. All pass. The live test discovered and resolved ALFRED's eligible older-vintage header behavior for DGS10.
- Empty vintage and dot/missing-day behavior are checked using a clearly separate synthetic counterexample.
- The app's counts use the complete history. A zero revision count for one series is an observed comparison for that cutoff, not proof that the series is never revised.
- Daily vintages do not certify the time during the day at which data became available.
- The student's three reported DGS10 values (4.57%, 4.21%, 3.91%) do not match downloaded FRED data for January 2, March 31, and September 1, 2026 (4.19%, 4.30%, 4.79%). The writeup preserves both and labels the student recheck pending; AI source checks are not represented as student manual checks.
- The partner exchange and role swap are student reports, not independently observed activities.
- The code explanation is corrected from API `vintage_dates` to the app's CSV `vintage_date`; eligible revisions can be retained if published by the cutoff, and the release schedule is supported by the Federal Reserve calendar rather than inferred from a daily chart.
- The final DGS10 comparison records 19 later observations and zero revisions as of September 30; the October 29 vintage has zero later observations and zero revisions against the same-day current download.
