# Lab 17 rubric audit

Audited October 29, 2026. This records evidence and open requirements; it does not award an instructor's grade.

| Criterion (5 points each) | Evidence | Status |
|---|---|---|
| Known answer reproduced | All four October 5 date/value pairs match; PAYEMS 159,536 then versus 158,316 today, 381 revised dates; preserved source CSVs and hashes | Complete |
| The app | Four default charts; typed PAYEMS; linked table with current/as-known dates, values, late/revised counts; per-ID errors; cached real downloads; 20 passing audit checks including three live page checks | Complete |
| Data card | Structure prepared; prework ID, series-specific source metadata, two-date experiment, and three student by-hand checks still needed | Pending |
| Fresh eyes | Requires actual partner attack, two-sentence evidence-based answer, and student report of code explanation/question/swap | Pending |
| The call | General as-of admission rule recorded; student's series-specific decision, reason, and condition still needed | Pending |

The two completed criteria have evidence meeting the 5-point anchors. A 25/25-ready submission cannot be claimed while the other three remain pending.

## Verification boundaries

- Common-answer and PAYEMS checks run on downloaded FRED/ALFRED responses; expected values are isolated in the verifier.
- Archived CSV hashes are checked on replay. Retrieval provenance is in `evidence/downloads.json`.
- Interface tests use archived responses with Streamlit's AppTest. The malformed/unknown-ID tests inject explicit failures to verify that other series survive; they are not a claim about a particular unknown ID's HTTP status.
- Three additional AppTest checks use live HTTP responses: today's four-chart page, all four October 5 answers through the date widget, and PAYEMS at January 15, 2025 through the typed-ID/date widgets. All pass. The live test discovered and resolved ALFRED's eligible older-vintage header behavior for DGS10.
- Empty vintage and dot/missing-day behavior are checked using a clearly separate synthetic counterexample.
- The app's counts use the complete history. A zero revision count for one series is an observed comparison for that cutoff, not proof that the series is never revised.
- Daily vintages do not certify the time during the day at which data became available.
- Student-only and partner exercises remain pending rather than being fabricated.
