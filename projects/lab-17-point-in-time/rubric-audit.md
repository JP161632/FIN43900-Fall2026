# Lab 17 rubric audit

Audited October 29, 2026 after incorporating the student's DGS10 selection, personal answers, partner exchange, and admission decision. This records evidence and open requirements; it does not award an instructor's grade.

| Criterion (5 points each) | Evidence | Status |
|---|---|---|
| Known answer reproduced | All four October 5 date/value pairs match; PAYEMS 159,536 then versus 158,316 today, 381 revised dates; preserved source CSVs and hashes | Complete |
| The app | Four default charts; typed PAYEMS; linked table with current/as-known dates, values, late/revised counts; per-ID errors; cached real downloads; 23 passing audit checks including three live page checks | Complete |
| Data card | DGS10 source links, measure, annual percentage units, daily frequency, publication schedule/observed lag, revision evidence, and download date; September 30 versus October 29 snapshots preserved; three correct source values independently parsed from a fresh download and matched to the app | Source verification complete, performed with AI assistance |
| Fresh eyes | Student reports no-AI line-by-line explanation and role swap; actual partner revision concern and code question preserved; two-sentence answer cites DGS10's zero revisions and PAYEMS's 381; original code answer receives an explicit CSV-parameter correction | Complete |
| The call | Student selects Admit DGS10; explicit prior-day-vintage rule excludes future releases/revisions; quarantine when decision provenance unavailable, reject feed if provenance lost; no claim of predictive success | Complete |

All five criteria now have documented substantive evidence, and all 23 numerical/software checks pass. The student explicitly delegated the three-value source comparison to AI; the writeup discloses that method rather than claiming the lab's literal student-by-hand activity. The instructor determines credit for that distinction; no grade is guaranteed.

## Verification boundaries

- Common-answer and PAYEMS checks run on downloaded FRED/ALFRED responses; expected values are isolated in the verifier.
- Archived CSV hashes are checked on replay. Retrieval provenance is in `evidence/downloads.json`.
- Interface tests use archived responses with Streamlit's AppTest. The malformed/unknown-ID tests inject explicit failures to verify that other series survive; they are not a claim about a particular unknown ID's HTTP status.
- Three additional AppTest checks use live HTTP responses: today's four-chart page, all four October 5 answers through the date widget, and PAYEMS at January 15, 2025 through the typed-ID/date widgets. All pass. The live test discovered and resolved ALFRED's eligible older-vintage header behavior for DGS10.
- Empty vintage and dot/missing-day behavior are checked using a clearly separate synthetic counterexample.
- The app's counts use the complete history. A zero revision count for one series is an observed comparison for that cutoff, not proof that the series is never revised.
- Daily vintages do not certify the time during the day at which data became available.
- Fresh FRED source rows establish DGS10 as 4.19%, 4.30%, and 4.79% for January 2, March 31, and September 1, 2026. Initial draft values were corrected. A separate standard-library CSV/Decimal reader verifies the raw rows against the app's pandas parser, with all three checks passing; dates and values are retained in `verification-results.json`.
- No student recheck is requested as a condition of completing the delegated work. The three-value verification is accurately labeled AI-assisted rather than an unaided student hand check.
- The partner exchange and role swap are student reports, not independently observed activities.
- The code explanation is corrected from API `vintage_dates` to the app's CSV `vintage_date`; eligible revisions can be retained if published by the cutoff, and the release schedule is supported by the Federal Reserve calendar rather than inferred from a daily chart.
- The final DGS10 comparison records 19 later observations and zero revisions as of September 30; the October 29 vintage has zero later observations and zero revisions against the same-day current download.
