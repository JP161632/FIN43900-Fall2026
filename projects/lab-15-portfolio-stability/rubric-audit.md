# Lab 15 rubric audit

Audited against the five merit criteria supplied in this conversation, which differ from the older repository handout. Each five-point anchor below has supporting evidence in the local submission. This is an evidence audit, not a guaranteed grade.

| Criterion (5 points each) | Evidence addressing the five-point anchor | Verification and limits |
|---|---|---|
| Training reproduced | Actual Streamlit page matches Meridian 0/20/25/55 at 6.51% return and 9.44% volatility; equity estimate 8% → 7% gives 0/10/10/80 at 6.53% and 12.94%; largest change 25 points; changing both engine correlation cells to 0.50 gives 0/40/0/60 at 6.52% and 9.73% | Executed AppTest and isolated source-edit probe in verify_lab15.py; original CLI output compared byte for byte with Lab 14; delivered correlations restored to 0.25 |
| Data and sources | Every ticker has a Yahoo source link and actual 2026-10-22 download timestamp; 61 month-end adjusted prices produce 60 complete monthly returns; estimates labelled historical arithmetic, gross of fees, not forecasts | All 244 monthly prices independently reconciled to saved daily source responses; source/CSV hashes checked; no partial October 2026. Student reports instructor approval for the four-stock universe instead of funds |
| Search under your mandate | NVDA/MSFT/TSM/QCOM universe; 10% gross objective and 0% reserve rule applied unchanged; long-only, fully invested, 5-point grid; all-month mix 0/70/25/5 and last-36 mix 0/55/45/0 | Same engine used by app and offline analysis; return and reserve infeasibility cases tested honestly; no objective reduction to force a mix |
| Stability and fresh eyes | All-month and last-36 results recorded; largest window weight change 20 points; partner's one-point TSM attack gives 0-point weight change; corrected two-sentence response explains the result | Personal results also tested through the app. Partner's actual entry/read-aloud, code question, and discussion are attributed to the student's supplied report; prior incorrect prediction is distinguished from measured outcome |
| The call | Student chooses provisional PILOT of all-month mix; reject for a change above 15 points between consecutive future rolling-36-month recommendations or realized volatility above 22%; adopt only after a stable 12-month pilot with out-of-sample evidence | Quarterly rolling-window review is explicit. Current 20-point all-month-versus-36-month difference is distinguished from the future consecutive-window trigger. Estimated and realized volatility are distinguished; no future pilot success is claimed |

The writeup also includes the decision question, source conventions, Mermaid flowchart, paper-drawing account and recursion clarification, reported no-AI code explanation, partner's floating-point question, estimation-risk explanation, and supplied reflection/evidence needed before adoption. Instructor permission and classroom activities are student-reported; AI did not independently witness them.

The future live pilot still needs an operational realized-volatility convention before it starts. That is a future implementation detail, not evidence that the pilot has already occurred or a missing historical lab result.

**Submission files complete:** app, engine, sourced prices, raw source snapshots, provenance, personal results, writeup, and reproducible audit. All six software tests pass in verification-results.txt. The final document-only edits do not change those tested calculations.

**Individual checkout:** use the GitHub links in the writeup to submit through Brightspace and complete any required attendance/receipt fields. Brightspace submission is the student's remaining step.
