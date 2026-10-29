# Lab 17 — Point-in-Time Audit

**Status: app and common verification complete; student series and personal/partner responses pending.** This is a working submission, not a claim that the remaining exercises were performed.

## D — Decision

Was each number in your series knowable on the day you would have traded on it — and may Project 2 use it?

The prior portfolio universe is NVDA, MSFT, TSM, and QCOM. The opening rate explanation and partner's recorded reason are awaiting the student's response. The student's prework series has not yet been supplied; no series is presented as their selection without confirmation.

## R — Real public data

The app uses one public CSV request per series for each current/vintage download on a cache miss. No key or account is required. [FRED](https://fred.stlouisfed.org/) supplies current observations; [ALFRED](https://alfred.stlouisfed.org/) supplies actual historical vintages. Raw downloaded CSVs, request URLs, UTC retrieval times, and SHA-256 hashes are preserved in [evidence/downloads.json](evidence/downloads.json).

The four initial IDs are [BAA](https://fred.stlouisfed.org/series/BAA), [FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS), [DGS10](https://fred.stlouisfed.org/series/DGS10), and [MORTGAGE30US](https://fred.stlouisfed.org/series/MORTGAGE30US). [PAYEMS](https://fred.stlouisfed.org/series/PAYEMS) is the required revision diagnostic, not a substitute for the student's prework choice.

## I — Run the app

From the repository root, in the course Python environment:

```powershell
python -m pip install -r projects/lab-17-point-in-time/requirements.txt
python -m streamlit run projects/lab-17-point-in-time/asof_app.py
```

Open the terminal's Local URL, usually `http://localhost:8501`. All four series start selected, the chart start date is January 1, 2020, and the as-known date defaults to the computer's current date. Type an additional ID in the sidebar. Set the as-known date to October 5, 2026 for the common proof; use PAYEMS and January 15, 2025 for the revision probe. A failed ID produces a per-series error while other series remain available.

Each chart displays today's values from the chosen chart start, with the last measured date known at the cutoff below it. The linked comparison table includes last measured dates and values for both vintages, later observations, revised matching dates, and the number of dates compared. Counts cover the entire downloaded history, independently of chart start. A dot or blank is missing, never zero or a carried-forward observation. Monthly CSV dates such as `2026-09-01` label September, not its release date.

Both download functions are cached for one hour. The cache keys include the series, download day, and (for ALFRED) vintage date. Refresh downloads clears both caches. Every series displays the real UTC retrieval timestamps. The app never substitutes a current FRED response for an ALFRED failure; a vintage-specific CSV header must match the requested series and have a vintage date no later than the cutoff. ALFRED can label the CSV with its latest available vintage: a DGS10 request for October 29 returned the October 28 header. Accepting that eligible older vintage fixes today's default page without admitting future data.

## V — Known-answer proof

Downloaded October 29, 2026; values below are calculated from saved public responses, not entered into the app. Expected answers exist only in the separate verifier.

| Series | Last measured period known October 5 | Expected | Downloaded | Result |
|---|---|---:|---:|---|
| BAA | September 2026 | 6.47 | 6.47 | Match |
| FEDFUNDS | September 2026 | 3.75 | 3.75 | Match |
| DGS10 | October 2, 2026 | 5.28 | 5.28 | Match |
| MORTGAGE30US | October 1, 2026 | 7.28 | 7.28 | Match |

For PAYEMS, the January 15, 2025 vintage ends at December 2024, **159,536 thousand persons**. Today's value for the **same December 2024 observation** is **158,316**, a decline of 1,220 thousand. Across the full overlapping history, **381 dates** differ; today's series has 21 measured months after December 2024. The comparison distinguishes revision of the same month from the addition of newer months.

Reproduce the preserved evidence and interface checks without requesting new data:

```powershell
python projects/lab-17-point-in-time/verify_lab17.py
```

Refresh the evidence from the public endpoints:

```powershell
python projects/lab-17-point-in-time/verify_lab17.py --live
```

Results: [verification-results.txt](verification-results.txt), with full numeric comparisons in [verification-results.json](verification-results.json). All **20 checks pass** in the delivered audit. Checks include the known answers, PAYEMS, missing days, empty vintages, rejecting a current header as a vintage, eligible older versus forbidden future vintage headers, four initial charts, a fifth typed series, invalid-ID isolation, and empty selection. Seventeen checks use archived evidence or controlled counterexamples; three additional checks exercise the real page with live HTTP downloads, including its October 5 date control and typed PAYEMS probe. The synthetic missing-data counterexample is explicitly separate from live economic evidence.

To repeat the live page checks as well as the archived evidence checks:

```powershell
python projects/lab-17-point-in-time/verify_lab17.py --live-ui
```

Running without `--live-ui` writes a 17-check archived audit; include it to reproduce all 20 checks. New downloads can naturally change today's values and counts.

## E — Student series data card

Pending the student's prework ID. The completed card must identify its source and link, measure, units/seasonal adjustment, publication timing with evidence, revision behavior, and actual download date. The audit must compare September 30, 2026 with October 29, 2026 and preserve both vintage responses. An observation date alone cannot establish its publication day.

**Three values checked by hand:** pending the student's own comparison against the FRED page, including each measured date, value, and whether it matched. Automated checks above do not stand in for this requirement.

## V — Fresh eyes

**No-AI line-by-line explanation and swap:** awaiting the student's report. Open `download_vintage` in [asof_app.py](asof_app.py) for the exercise.

**Partner's code question and student's answer:** pending.

**Partner attack:** pending the partner's least-trusted data-card field and specific concern.

**Two-sentence evidence-based response:** pending the actual attack and the selected series evidence.

## The call

**Student's admit/quarantine/reject choice, series-specific reason, and condition for changing it:** pending.

Required admission rule: for each decision, use the vintage actually available by that decision's information cutoff. ALFRED's date specifies a daily snapshot and does not establish an intraday release time. Use the prior calendar day's vintage for a conservative next-session rule unless a verified release timestamp permits a same-day observation. Never use today's historical values merely shifted by a fixed lag. Quarantine any decision whose required vintage or availability evidence cannot be verified.

## Learn on your own and reflect

Awaiting the student's own answers: what a data card is; which fields prevent a leak; why “cleaned the data” is insufficient; how late the chosen series is published and what the two as-known dates reveal; and what a backtest on today's values would have overstated. The app can establish differences in data availability and revisions; those differences alone do not quantify strategy performance.

## AI assistance and checkout

AI built the app, sourced the public CSVs, wrote the verifier, and drafted this evidence record. Personal explanations, by-hand checks, and partner exercises are recorded only when supplied by the student. No partner activity is claimed as observed by AI.

- [Writeup](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-17-point-in-time/lab-17-writeup.md)
- [asof_app.py](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-17-point-in-time/asof_app.py)
- [Verifier](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-17-point-in-time/verify_lab17.py)
- [Executed results](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-17-point-in-time/verification-results.txt)
- [Rubric audit](rubric-audit.md)

The Brightspace quiz and submission are student actions and have not been completed by this app or audit.
