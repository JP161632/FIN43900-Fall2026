# Lab 17 — Point-in-Time Audit

**Status: app, DGS10 data card and source checks, student explanations, partner response, and admission rule completed.** All 23 audit checks pass. The three-value comparison uses source rows downloaded directly from FRED and independently parsed against the app's values.

## D — Decision

Was each number in your series knowable on the day you would have traded on it — and may Project 2 use it?

The portfolio universe is NVDA, MSFT, TSM, and QCOM. The student selected **DGS10**, the 10-year Treasury constant-maturity yield, for this lab.

**Student's opening explanation:** Tech stocks such as NVDA and MSFT have substantial profits expected years in the future; higher interest rates reduce the present value of those future profits. DGS10 is a benchmark input to a valuation's risk-free rate, rather than the complete discount rate for these equities: an equity risk premium and company-specific assumptions also matter. The lab establishes data admissibility, not that this rate predicts the portfolio's returns.

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
python projects/lab-17-point-in-time/verify_lab17.py --series DGS10
```

Refresh the evidence from the public endpoints:

```powershell
python projects/lab-17-point-in-time/verify_lab17.py --live --series DGS10
```

Results: [verification-results.txt](verification-results.txt), with full numeric comparisons in [verification-results.json](verification-results.json). All **23 checks pass** in the delivered audit. Checks include the known answers, PAYEMS, missing days, empty vintages, rejecting a current header as a vintage, eligible older versus forbidden future vintage headers, four initial charts, a fifth typed series, invalid-ID isolation, empty selection, and three independently parsed DGS10 source rows. Twenty checks can replay archived evidence or controlled counterexamples; three additional checks exercise the real page with live HTTP downloads, including its October 5 date control and typed PAYEMS probe. The synthetic missing-data counterexample is explicitly separate from live economic evidence.

To repeat the live page checks as well as the archived evidence checks:

```powershell
python projects/lab-17-point-in-time/verify_lab17.py --live-ui --series DGS10
```

Running with `--series DGS10` but without `--live-ui` writes a 20-check archived audit; include both options to reproduce all 23 checks. New downloads can naturally change today's values and counts.

## E — Student series data card

| Field | DGS10 data card |
|---|---|
| Source and link | Board of Governors of the Federal Reserve System, H.15 Selected Interest Rates, distributed through [FRED DGS10](https://fred.stlouisfed.org/series/DGS10); historical snapshots through [ALFRED DGS10](https://alfred.stlouisfed.org/series?seid=DGS10). |
| Measure | Market yield on nominal U.S. Treasury securities at a constant 10-year maturity, quoted on an investment basis. It is a yield-curve measure, not a stock return or a bond's total return. |
| Units and frequency | Percent per annum; daily; not seasonally adjusted. A value of 4.99 means 4.99%, or 0.0499 as a decimal annual rate. Holidays and other missing observations are not filled. |
| Publication timing | H.15 is published on business days except holidays ([release description](https://www.federalreserve.gov/releases/h15/About.HTM)); the [October 2026 Federal Reserve calendar](https://www.federalreserve.gov/newsevents/2026-october.htm) schedules it at 4:15 p.m. Eastern. The September 30 ALFRED snapshot ends at the September 29 observation, demonstrating a short, one-business-day lag in that example. At retrieval on October 29, the latest observation was October 27; [FRED's page](https://fred.stlouisfed.org/series/DGS10) recorded its update on October 28 at 3:16 p.m. CDT (4:16 p.m. Eastern). The observation date, source release time, and FRED update time are distinct. |
| Revisions | Zero revised matching dates between the September 30 vintage and today's download, across 16,171 overlapping valid dates; zero between the October 29 vintage and today's download, across 16,190 dates. No revisions observed in these comparisons does not prove revisions are impossible. |
| Download date | October 29, 2026, refreshed for the final audit. Exact UTC timestamps, request URLs, and SHA-256 hashes for the current data and both comparison vintages are in [downloads.json](evidence/downloads.json). |
| Availability rule | Use the latest eligible vintage before the decision's information cutoff. A daily vintage does not certify availability for a morning or other intraday trade. No future observation, future revision, current-history substitution, or forward fill is eligible. |

### September month-end versus today

| As known on | Last measured date available | Yield (%) | Today's observations after that date | Revised matching dates |
|---|---|---:|---:|---:|
| September 30, 2026 | September 29, 2026 | 5.26 | 19 | 0 |
| October 29, 2026 | October 27, 2026 | 4.99 | 0 | 0 |

The 19 observations after September 29 disappear when the September 30 cutoff is imposed; they were unavailable in that vintage. This daily market-rate series has a short publication lag and no revisions observed here, unlike PAYEMS. The later value of 4.99 is a new measured date, not a revision of September 29's 5.26. Source evidence: [September 30 snapshot](evidence/DGS10_2026-09-30.csv), [October 29 snapshot](evidence/DGS10_2026-10-29.csv), and [comparison results](verification-results.json).

### Three values checked directly against the assigned FRED source

These observations were checked in a fresh download from the exact [public FRED endpoint specified in the lab](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10), linked to the [DGS10 series page](https://fred.stlouisfed.org/series/DGS10). A separate standard-library CSV reader and decimal comparison verified each source row against the app's parsed value, without relying on the app's parser to establish the source value.

| Measured date | FRED source yield (%) | App yield (%) | Comparison |
|---|---:|---:|---|
| January 2, 2026 | **4.19** | 4.19 | Match |
| March 31, 2026 | **4.30** | 4.30 | Match |
| September 1, 2026 | **4.79** | 4.79 | Match |

The exact source rows, retrieval timestamp, request URL, and matching app values are retained under `source_value_checks` in [verification-results.json](verification-results.json); the full source is [DGS10_current.csv](evidence/DGS10_current.csv). These source-verified numbers replace the incorrect initial draft values. This comparison is reproduced by the verifier's independent CSV reader.

## V — Fresh eyes

The activities below are student-supplied reports.

**Line-by-line explanation and swap:** The student confirms both partners walked through the code line by line without assistance and swapped roles for the questions. The relevant function is `download_vintage` in [asof_app.py](asof_app.py).

**Partner's code question:** “How does download_vintage() stop the code from grabbing today's updated number instead of the old one?”

**Student's original answer:** “It passes vintage_dates to the ALFRED API, which acts like a time machine and only pulls the exact snapshot available on that cutoff date.”

**Technical correction from the code audit:** This app uses ALFRED's public CSV endpoint, with the singular query parameter `vintage_date=YYYY-MM-DD`, not the keyed API or its plural `vintage_dates` parameter. The function validates the ID, parses and rejects a future cutoff, constructs the ALFRED URL, calls the shared downloader with a vintage-specific expected header, rejects nonmissing observation dates after the cutoff, and returns the response with retrieval provenance. The parser requires the requested series and an eligible vintage header no later than the cutoff, allowing ALFRED's last available vintage; no current-data fallback exists. These checks distinguish a real vintage from today's CSV but do not establish intraday availability.

**Partner attack — least-trusted field: revisions:** “I trust revisions the least. Economic data gets quietly updated weeks later, and if you aren't careful, you accidentally feed future numbers into past dates.”

**Two-sentence evidence-based response:** The [DGS10 September 30 comparison](verification-results.json) has zero revised values across 16,171 matching dates, while the PAYEMS diagnostic shows December 2024 changing from 159,536 to 158,316 and 381 revised dates, so revision risk must be checked for each series rather than assumed away. I will use the ALFRED vintage eligible at each decision cutoff, preserve its source response, and quarantine decisions with missing vintage or release-time evidence rather than substitute today's history.

## The call

**Admit DGS10, subject to the as-of rule below.** The student's choice is to admit because timestamped historical vintages can be checked, and to reject the feed if it strips release information and supplies only a continuously updated current history. The short observed lag and zero observed revisions support this use, but do not replace availability checks or establish predictive value.

**Operational as-of rule:** For a trading session on date T, use the latest nonmissing DGS10 observation in the ALFRED vintage dated T minus one calendar day; use only observations in that snapshot and do not fill forward missing observations into invented daily values. This conservatively excludes releases later on T, including its morning and regular-session decisions. A same-day exception requires independently verified release and ingestion timestamps at or before the actual decision time; the daily snapshot alone cannot justify it. Retain revisions already published by the cutoff, but exclude revisions published later; the eligible value need not be the original first print.

**Condition that changes the call:** Reject a feed that loses reconstructable release/vintage provenance and offers only live current values; quarantine individual decisions with unavailable vintage or timing evidence until that evidence is restored. Never replace a missing vintage with today's historical data or assume a fixed lag removes revision risk. This admits the series as an eligible input, not a profitable strategy or a complete equity discount rate.

## Learn on your own and reflect

**What is a data card? — student's response:** It is an ID badge for a dataset: where the numbers came from, when they were published, and what flaws to watch for. Here that includes source, measure, units, frequency, release timing, revisions, download date, and an admissibility rule.

**Which fields prevent leaks? — student's response, with technical correction:** Check the actual release timestamp rather than only the measured date, and identify which vintage supplied the value. The student initially required the original first print; the correct rule permits any revision already published by the decision cutoff. Observation date, publication/availability time, vintage date, and retrieval timestamp answer different questions and must not be treated as interchangeable.

**Why is “cleaned the data” insufficient? — student's response:** It says nothing about what actually happened; dropped rows and the reasons for dropping them must be traceable so others can verify the work. Cleaning records complement the data card: a row-removal log alone still does not explain units, release lag, source, or revision policy. This app preserves source CSVs and treats missing days as missing rather than dropping their provenance or inventing values.

**How late is DGS10 published, and what do the dates reveal? — student's explanation, corrected against sources:** The student correctly identified that a late-afternoon release cannot support an earlier morning trade. The [Federal Reserve calendar](https://www.federalreserve.gov/newsevents/2026-october.htm) supplies the 4:15 p.m. Eastern H.15 schedule; the app's daily cutoffs alone do not prove that clock time. In the September 30 snapshot, September 29 is the newest observation; on October 29 at retrieval, October 27 remains newest and FRED records an October 28 update. These observations show a short lag and the need to distinguish the date measured from actual availability, including weekends, holidays, and the download time.

**What could today's values overstate? — student's response, edited for precision:** Feeding revisions published months later into earlier decisions gives a backtest future information and can make the model appear more informative or its timing more feasible than it was. For DGS10, no revisions were observed in the tested comparisons, so the demonstrated risk is primarily assuming a rate was available before release; for PAYEMS, later revisions are directly demonstrated. Neither experiment contains a trading rule or realized portfolio returns, so it cannot establish the amount of overstated performance or that a strategy must fail in live trading.

