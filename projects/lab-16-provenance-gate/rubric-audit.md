# Lab 16 requirement audit

Scope: the full Lab 16 instructions pasted by the student in this session.

| Requirement | Evidence | Status |
|---|---|---|
| Same project organization as earlier labs | Dedicated lab-16-provenance-gate folder, writeup, code, saved output, verifier | Pass |
| State the shared decision question and cutoff | Writeup D; editable date 2026-03-31 | Pass |
| Preserve all 12 training rows | TABLE in asof.py | Pass |
| One standard-library implementation with editable inputs at top | asof.py | Pass |
| Four rules in specified order | filter_rows; latest_vintages | Pass |
| Counts and original row numbers for every step | Executed report; verifier assertions | Pass |
| Exact six-row panel | Assertions: 1, 4, 5, 6, 9, 12 | Pass |
| Six computed signals, signed two-decimal percentages and months | Executed output and known-answer assertions | Pass |
| CCC naive uses revised February value | Row 10 selected; +1.82% | Pass |
| AAA eligible revision wins | Row 4 retained, row 2 removed; +1.98% | Pass |
| Run command and actual execution | Writeup commands; verification-results.txt | Pass |
| Later cutoff yields naive values; delivered cutoff restored | April 15 in-memory experiment; March 31 asserted | Pass for submitted code |
| AI quiz answered before explanation | Await least-understood line and student's quiz answer | Pending student |
| Five-minute opening partner explanation and swap | Await student's report | Pending student |
| No-AI rule-4 explanation, partner question and answer, swap | Await student's report | Pending student |
| Run partner file, original match, April 15 equality, undo | Cannot substitute own-code test for partner-file activity | Pending student |
| Three learn-on-your-own responses | Await student's own answers | Pending student |
| Two reflection responses | Await student's own answers | Pending student |
| Individual GitHub checkout links | Files pushed successfully to submission/main on October 27, 2026; links in writeup | Pass |

Additional checks passed: publication on the cutoff day is eligible; reversed input order preserves signals; a missing adjacent month is not treated as a monthly change. No third-party package is required. Raw data and row-level exclusions are preserved.

Instruction discrepancy: the repository's lessons/week-10/lab-16-provenance-gate.md describes a different Brightspace checkout (data card, source/claim disposition, attendance/session token, growth note). This implementation follows the student's pasted assignment as requested. No attendance declaration, session token, partner activity, or personal reflection has been invented. If the separate Brightspace checkout is also assigned, the student must complete its private classroom fields there rather than store personal information in this public repository.

Full-points readiness cannot yet be certified: the pending student activities and answers must be completed before the final audit. Thursday's own-series ALFRED work is a preview, not a required Lab 16 deliverable in the pasted instructions.
