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
| AI quiz answered before explanation | Student correctly retained rows 1 and 4, traced date comparison, and identified ticker-only history loss; AI feedback followed | Pass |
| Opening partner explanation | Student supplied explanation and explicitly confirmed five-minute exercise and reciprocal role swap | Pass, student-reported |
| No-AI rule-4 explanation, partner question and answer | Line-by-line explanation, same-day conflict question and ValueError answer, and reciprocal role swap explicitly reported | Pass, student-reported |
| Run partner file, original match, April 15 equality, undo | Student explicitly reports all four steps and correct values | Pass, student-reported |
| Three learn-on-your-own responses | Student responses incorporated; AAA intervals distinguished | Pass |
| Two reflection responses | Rule 3 / row 3 selected; naive backtest claim clarified to avoid unsupported trading-return assertions | Pass |
| Individual GitHub checkout links | Files pushed successfully to submission/main on October 27, 2026; links in writeup | Pass |

Additional checks passed: publication on the cutoff day is eligible; reversed input order preserves signals; a missing adjacent month is not treated as a monthly change. No third-party package is required. Raw data and row-level exclusions are preserved.

Instruction discrepancy: the repository's lessons/week-10/lab-16-provenance-gate.md describes a different Brightspace checkout (data card, source/claim disposition, attendance/session token, growth note). This implementation follows the student's pasted assignment as requested. No attendance declaration, session token, partner activity, or personal reflection has been invented. If the separate Brightspace checkout is also assigned, the student must complete its private classroom fields there rather than store personal information in this public repository.

Final audit: all deliverable requirements in the student's pasted assignment are met by the submitted files, executed checks, recorded quiz exchange, and student-reported partner activities. All known-answer values and the later-cutoff floor pass. No student-answer placeholders remain. This audit supports submission readiness; the instructor determines the grade. Thursday's own-series ALFRED work is a preview, not a required Lab 16 deliverable in the pasted instructions.
